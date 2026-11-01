// S-003 TK-004 acceptance (Spec: Draft marks): every built page shows a draft
// mark until a committed approval record names its route and its current
// content hash; editing the page restores the mark; an approval whose hash does
// not match never removes it. The content hash follows the S-005 contract
// (SHA-256 over the canonical content of <main id="main">, without the review
// mark and data-review-exclude regions) and is checked against independent
// test vectors. Runs on the built output: `npm run build` first.
// The full rebuild with a fixture approval is `npm run check:draft-marks`.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { execFileSync } from 'node:child_process';
import { readFileSync } from 'node:fs';
import { join } from 'node:path';
import { builtPages, siteDir, visibleText } from './helpers.mjs';
import {
  approvedRoutes,
  canonicalContent,
  contentHash,
  hasDraftMark,
  markProblems,
  readApprovals,
  routeOf,
  validateApprovals,
} from '../scripts/draft-marks.mjs';

const fixtureFile = (name) => JSON.parse(readFileSync(join(siteDir, 'tests', 'fixtures', 'draft-marks', name), 'utf8'));
const { vectors } = fixtureFile('vectors.json');
const pages = () => builtPages().map((p) => ({ ...p, route: routeOf(p.name) }));
const MARK = /<div\b[^>]*data-review-mark[^>]*>[\s\S]*?<\/div>/i;

// Fixture approvals with the placeholder hash bound to a built page's hash.
function fixtureApprovals(hashOf) {
  return fixtureFile('approvals.json').approvals.map((a) => (a.hash === 'HASH_OF_BUILT_PAGE' ? { ...a, hash: hashOf(a.route) } : a));
}

// Change one character of the page's own content: the first letter of the
// first text run in <main> after the draft mark.
function editOneChar(html) {
  const main = html.search(/<main\b[^>]*id="main"/i);
  const markEnd = html.slice(main).match(MARK);
  const from = markEnd ? main + markEnd.index + markEnd[0].length : main;
  const m = /<(?:h1|p)\b[^>]*>[^<]*?([A-Za-z])/i.exec(html.slice(from));
  assert.ok(m, 'no text to edit after the mark');
  const at = from + m.index + m[0].length - 1;
  const ch = html[at];
  return html.slice(0, at) + (ch === ch.toUpperCase() ? ch.toLowerCase() : ch.toUpperCase()) + html.slice(at + 1);
}

test('content hash matches the test vectors (S-005 contract)', () => {
  assert.ok(vectors.length >= 4);
  for (const v of vectors) {
    assert.equal(canonicalContent(v.html), v.canonical, v.name);
    assert.equal(contentHash(v.html), v.hash, v.name);
  }
});

test('approval records are validated (self-test) and the committed records are well-formed', () => {
  const ok = { route: '/start', hash: `sha256:${'a'.repeat(64)}`, approver: 'Kayden', date: '2026-11-02', source: 'https://github.com/KaydenClark/Agentic-Management-System/blob/main/grill-board/page-approvals.md' };
  assert.deepEqual(validateApprovals({ approvals: [ok] }), []);
  for (const [why, bad] of [
    ['no hash', { ...ok, hash: undefined }],
    ['short hash', { ...ok, hash: 'sha256:abc' }],
    ['no approver', { ...ok, approver: '' }],
    ['undated', { ...ok, date: undefined }],
    ['bad date', { ...ok, date: '11/02/2026' }],
    ['no source', { ...ok, source: undefined }],
    ['source not a repository link', { ...ok, source: 'in chat' }],
    ['route without slash', { ...ok, route: 'start' }],
    ['not-found approved', { ...ok, route: '/_not-found' }],
    ['unknown field', { ...ok, approved: true }],
  ]) {
    assert.ok(validateApprovals({ approvals: [bad] }).length, `${why} passes`);
  }
  assert.ok(validateApprovals({}).length, 'missing approvals list passes');
  assert.deepEqual(validateApprovals(readApprovals()), [], 'site/approvals.json has a malformed record');
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

test('a page with no approval shows the draft mark: visible, readable text, server-rendered', () => {
  const records = readApprovals().approvals;
  for (const p of pages()) {
    const approved = approvedRoutes([{ route: p.route, hash: contentHash(p.html) }], records).has(p.route);
    if (approved) continue;
    assert.ok(hasDraftMark(p.html), `${p.route}: no draft mark`);
    const mark = p.html.match(MARK)?.[0] ?? '';
    assert.match(mark, /role="note"/, `${p.route}: the mark is not a note`);
    assert.doesNotMatch(mark.match(/<div\b[^>]*>/)[0], /\bhidden\b|aria-hidden/, `${p.route}: the mark is hidden`);
    assert.match(visibleText(mark), /\bDraft\b/, `${p.route}: the mark does not say Draft`);
    assert.match(visibleText(mark), /not approved/i, `${p.route}: the mark does not say the page is not approved`);
  }
});

test('the built output agrees with the committed approvals (an approved mark on changed content fails)', () => {
  assert.deepEqual(markProblems(pages(), readApprovals().approvals), []);
});

test('a fixture approval bound to the page hash approves it; one changed character restores the draft', () => {
  for (const p of pages().filter((x) => x.route !== '/_not-found')) {
    const hash = contentHash(p.html);
    const record = { ...fixtureApprovals(() => hash)[0], route: p.route };
    assert.ok(approvedRoutes([{ route: p.route, hash }], [record]).has(p.route), `${p.route}: approval at its hash does not approve it`);
    const edited = editOneChar(p.html);
    assert.notEqual(edited, p.html);
    assert.notEqual(contentHash(edited), hash, `${p.route}: a changed character keeps the hash`);
    assert.ok(!approvedRoutes([{ route: p.route, hash: contentHash(edited) }], [record]).has(p.route), `${p.route}: approval survives an edit`);
  }
});

test('an approval whose hash does not match never removes the mark', () => {
  const all = pages();
  const hashOf = (route) => contentHash(all.find((p) => p.route === route).html);
  const records = fixtureApprovals(hashOf);
  const current = all.map((p) => ({ route: p.route, hash: contentHash(p.html) }));
  const approved = approvedRoutes(current, records);
  assert.ok(approved.has('/start'), 'fixture approval at /start hash does not approve /start');
  assert.ok(!approved.has('/how-it-works'), 'an approval with a wrong hash approves /how-it-works');
  assert.ok(!approvedRoutes(current, [{ ...records[0], route: '/how-it-works' }]).has('/how-it-works'), "another page's hash approves /how-it-works");

  // Planted faults on built pages: the mark removed without a matching approval.
  const start = all.find((p) => p.route === '/start');
  const unmarked = start.html.replace(MARK, '');
  assert.ok(!hasDraftMark(unmarked));
  assert.deepEqual(markProblems([{ route: '/start', html: unmarked }], records), [], 'approved page without its mark reported');
  assert.ok(markProblems([{ route: '/start', html: editOneChar(unmarked) }], records).length, 'approved mark on changed content passes');
  assert.ok(markProblems([{ route: '/how-it-works', html: all.find((p) => p.route === '/how-it-works').html.replace(MARK, '') }], records).length, 'mark removed under a mismatched approval passes');
  assert.ok(markProblems([{ route: '/start', html: start.html }], records).length, 'approved page still showing its mark passes');
});

test('the hash is stable: the mark, the footer commit, scripts and data-review-exclude regions do not change it', () => {
  for (const p of pages()) {
    const hash = contentHash(p.html);
    assert.equal(contentHash(p.html.replace(MARK, '')), hash, `${p.route}: removing the mark changes the hash`);
    const footer = p.html.replace(/data-commit-sha="[^"]*"/g, 'data-commit-sha="0000000"').replace(/\/commit\/[0-9a-f]+/g, '/commit/0000000');
    assert.equal(contentHash(footer), hash, `${p.route}: the footer commit changes the hash`);
    assert.equal(contentHash(p.html.replace(/<script\b[^>]*>[\s\S]*?<\/script>/gi, '')), hash, `${p.route}: scripts change the hash`);
    const excluded = p.html.replace(/(<[a-z]+\b[^>]*data-review-exclude[^>]*>)/i, '$1<span>live 99</span>');
    if (excluded !== p.html) assert.equal(contentHash(excluded), hash, `${p.route}: an excluded region changes the hash`);
  }
});

test('npm run page-hashes prints every built page with its route, hash and status', () => {
  const out = execFileSync(process.execPath, [join(siteDir, 'scripts', 'page-hashes.mjs')], { cwd: siteDir, encoding: 'utf8' });
  for (const p of pages()) {
    const line = out.split('\n').find((l) => l.split(/\s+/)[0] === p.route);
    assert.ok(line, `${p.route}: not printed`);
    assert.ok(line.includes(contentHash(p.html)), `${p.route}: printed without its current hash`);
    assert.match(line, /\b(draft|approved)\b/, `${p.route}: no status`);
  }
});
