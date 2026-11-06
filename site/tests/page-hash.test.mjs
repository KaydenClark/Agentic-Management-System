// Page hashes and no review state. The content hash follows the S-005
// page-hash contract (SHA-256 over the canonical content of <main id="main">,
// without data-review-mark and data-review-exclude regions) and is checked
// against independent test vectors; the S-005 Grill Board binds the owner's
// review of a page to it. The public site shows no review state: no page
// carries a draft or approval banner. Runs on the built output: `npm run build`
// first.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { execFileSync } from 'node:child_process';
import { readFileSync } from 'node:fs';
import { join } from 'node:path';
import { builtPages, siteDir, visibleText } from './helpers.mjs';
import { canonicalContent, contentHash, hasReviewMark, routeOf } from '../scripts/page-hash.mjs';

const { vectors } = JSON.parse(readFileSync(join(siteDir, 'tests', 'fixtures', 'page-hash', 'vectors.json'), 'utf8'));
const pages = () => builtPages().map((p) => ({ ...p, route: routeOf(p.name) }));
const MAIN_OPEN = /(<main\b[^>]*id="main"[^>]*>)/i;
const OLD_MARK = '<div data-review-mark="draft" role="note"><strong>Draft</strong><span>Not approved by the owner yet. This page may still change.</span></div>';

// Wording a review banner would use: the page's own state, not its subject.
const REVIEW_WORDS = /not approved|awaiting (?:the owner'?s? )?(?:approval|review)|pending (?:approval|review)|this page may still change|unreviewed/i;
const NOTE = /<(\w+)\b[^>]*\brole="(?:note|status|alert)"[^>]*>([\s\S]*?)<\/\1>/gi;

// Problems with a built page that shows its review state; [] when it shows none.
export function reviewStateProblems(html) {
  const problems = [];
  if (/\sdata-review-mark\b/i.test(html)) problems.push('carries data-review-mark');
  for (const [, , inner] of html.matchAll(NOTE)) {
    const text = visibleText(inner);
    if (/\bdraft\b|\bapprov|\breview/i.test(text)) problems.push(`a note announces review state: ${text.slice(0, 60)}`);
  }
  const text = visibleText(html);
  if (REVIEW_WORDS.test(text)) problems.push(`says ${text.match(REVIEW_WORDS)[0]}`);
  return problems;
}

test('content hash matches the test vectors (S-005 contract)', () => {
  assert.ok(vectors.length >= 4);
  for (const v of vectors) {
    assert.equal(canonicalContent(v.html), v.canonical, v.name);
    assert.equal(contentHash(v.html), v.hash, v.name);
  }
});

test('every built page has a route and a content hash', () => {
  const all = pages();
  assert.ok(all.length >= 4);
  assert.ok(all.some((p) => p.route === '/'));
  for (const p of all) {
    assert.match(p.route, /^\//, p.name);
    assert.match(contentHash(p.html), /^sha256:[0-9a-f]{64}$/, p.name);
  }
});

test('no built page shows a draft or approval banner (planted faults caught first)', () => {
  const start = pages().find((p) => p.route === '/start').html;
  assert.deepEqual(reviewStateProblems(start), [], 'the unplanted page already fails');
  const plant = (markup) => start.replace(MAIN_OPEN, `$1${markup}`);
  assert.ok(reviewStateProblems(plant(OLD_MARK)).length, 'the old draft mark passes');
  assert.ok(reviewStateProblems(plant('<div role="note"><strong>Draft</strong> for review</div>')).length, 'a draft note without data-review-mark passes');
  assert.ok(reviewStateProblems(plant('<p>Not approved by the owner yet.</p>')).length, 'a plain not-approved line passes');
  assert.ok(reviewStateProblems(plant('<span data-review-mark="">x</span>')).length, 'an empty data-review-mark passes');
  for (const p of pages()) {
    assert.deepEqual(reviewStateProblems(p.html), [], p.route);
    assert.ok(!hasReviewMark(p.html), `${p.route}: holds a review mark`);
  }
});

test('the hash is stable: a review mark, the footer commit, scripts and data-review-exclude regions do not change it', () => {
  for (const p of pages()) {
    const hash = contentHash(p.html);
    const marked = p.html.replace(MAIN_OPEN, `$1${OLD_MARK}`);
    assert.ok(hasReviewMark(marked), `${p.route}: the planted mark is not seen`);
    assert.equal(contentHash(marked), hash, `${p.route}: a review mark changes the hash`);
    const footer = p.html.replace(/data-commit-sha="[^"]*"/g, 'data-commit-sha="0000000"').replace(/\/commit\/[0-9a-f]+/g, '/commit/0000000');
    assert.equal(contentHash(footer), hash, `${p.route}: the footer commit changes the hash`);
    assert.equal(contentHash(p.html.replace(/<script\b[^>]*>[\s\S]*?<\/script>/gi, '')), hash, `${p.route}: scripts change the hash`);
    const excluded = p.html.replace(/(<[a-z]+\b[^>]*data-review-exclude[^>]*>)/i, '$1<span>live 99</span>');
    if (excluded !== p.html) assert.equal(contentHash(excluded), hash, `${p.route}: an excluded region changes the hash`);
  }
});

test('one changed character of page content changes the hash', () => {
  for (const p of pages()) {
    const from = p.html.search(MAIN_OPEN);
    const m = /<(?:h1|p)\b[^>]*>[^<]*?([A-Za-z])/i.exec(p.html.slice(from));
    assert.ok(m, `${p.route}: no text to edit`);
    const at = from + m.index + m[0].length - 1;
    const ch = p.html[at];
    const edited = p.html.slice(0, at) + (ch === ch.toUpperCase() ? ch.toLowerCase() : ch.toUpperCase()) + p.html.slice(at + 1);
    assert.notEqual(contentHash(edited), contentHash(p.html), `${p.route}: a changed character keeps the hash`);
  }
});

test('npm run page-hashes prints every built page with its route and hash', () => {
  const out = execFileSync(process.execPath, [join(siteDir, 'scripts', 'page-hashes.mjs')], { cwd: siteDir, encoding: 'utf8' });
  for (const p of pages()) {
    const line = out.split('\n').find((l) => l.split(/\s+/)[0] === p.route);
    assert.ok(line, `${p.route}: not printed`);
    assert.ok(line.includes(contentHash(p.html)), `${p.route}: printed without its current hash`);
  }
});
