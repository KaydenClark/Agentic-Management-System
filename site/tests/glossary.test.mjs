// S-003 TK-003: the Glossary page is generated from GLOSSARY.md, the one home
// of the project's terms, and cannot diverge from it.
// 1. app/glossary/glossary.json equals what scripts/gen-glossary.mjs makes from
//    ../GLOSSARY.md, byte for byte (`npm run glossary:gen` rewrites it).
// 2. Over the built /glossary page, read independently of the generator: every
//    term in GLOSSARY.md is a <dt> with an id, followed by its definition word
//    for word, and the page defines no term GLOSSARY.md lacks.
// Run `npm run build` first.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { join } from 'node:path';
import { pathToFileURL } from 'node:url';
import { builtPage, siteDir, visibleText } from './helpers.mjs';
import { mainOf, repoRoot } from './tour-helpers.mjs';

const gen = await import(pathToFileURL(join(siteDir, 'scripts', 'gen-glossary.mjs')).href);

// Terms and definitions straight from the Markdown: a paragraph that starts
// with **Term**: and its following lines. Links keep their text, emphasis
// and code marks are dropped.
const plain = (md) => md.replace(/\[([^\]]+)\]\([^)]+\)/g, '$1').replace(/\*\*|`/g, '').replace(/\s+/g, ' ').trim();
export function markdownTerms(md) {
  return md.split(/\n\s*\n/).map((p) => p.trim().match(/^\*\*(.+?)\*\*:\s*([\s\S]+)$/)).filter(Boolean)
    .map(([, term, def]) => ({ term: term.trim(), definition: plain(def) }));
}

// Terms and definitions on a built page: each <dt> and the <dd> after it.
export function pageTerms(html) {
  return [...mainOf(html).matchAll(/<dt\b([^>]*)>([\s\S]*?)<\/dt>\s*<dd\b[^>]*>([\s\S]*?)<\/dd>/gi)]
    .map(([, attrs, dt, dd]) => ({ id: attrs.match(/\sid="([^"]+)"/)?.[1] ?? null, term: visibleText(dt), definition: visibleText(dd) }));
}

export function glossaryProblems(md, html) {
  const want = markdownTerms(md);
  const have = pageTerms(html);
  const problems = [];
  if (!want.length) problems.push('GLOSSARY.md has no terms');
  for (const { term, definition } of want) {
    const found = have.find((h) => h.term === term);
    if (!found) { problems.push(`term ${term} is not on the page`); continue; }
    if (!found.id) problems.push(`term ${term} has no id to link to`);
    if (found.definition !== definition) problems.push(`term ${term}: page says "${found.definition}", GLOSSARY.md says "${definition}"`);
  }
  for (const { term } of have) if (!want.some((w) => w.term === term)) problems.push(`page defines ${term}, which GLOSSARY.md lacks`);
  return problems;
}

const MD = '# G\n\nIntro.\n\n## Language\n\n### A\n\n**Alpha**:\nFirst [letter](x.md).\n\n**Beta**:\nSecond letter.\n';
const HTML = (alpha = 'First letter.', extra = '') => `<main><dl><dt id="alpha">Alpha</dt><dd>${alpha}</dd><dt id="beta">Beta</dt><dd>Second letter.</dd>${extra}</dl></main>`;

test('the glossary check catches faults (self-test)', () => {
  assert.deepEqual(glossaryProblems(MD, HTML()), []);
  assert.ok(glossaryProblems(MD, HTML().replace(/<dt id="beta">[\s\S]*?<\/dd>/, '')).length, 'a missing term passes');
  assert.ok(glossaryProblems(MD, HTML('First letter, roughly.')).length, 'a reworded definition passes');
  assert.ok(glossaryProblems(MD, HTML(undefined, '<dt id="gamma">Gamma</dt><dd>Invented.</dd>')).length, 'an invented term passes');
  assert.ok(glossaryProblems(MD, HTML().replace(' id="alpha"', '')).length, 'a term with no id passes');
  const json = gen.glossaryJson(MD);
  assert.notEqual(gen.glossaryJson(MD.replace('Second', 'Other')), json, 'the generator ignores a changed definition');
});

test('app/glossary/glossary.json is the generator output for GLOSSARY.md (npm run glossary:gen)', () => {
  const md = readFileSync(join(repoRoot, 'GLOSSARY.md'), 'utf8');
  const committed = readFileSync(join(siteDir, 'app', 'glossary', 'glossary.json'), 'utf8');
  assert.equal(committed, gen.glossaryJson(md), 'glossary.json is stale: run npm run glossary:gen');
});

test('/glossary shows every GLOSSARY.md term with its definition word for word, and no other term', () => {
  const md = readFileSync(join(repoRoot, 'GLOSSARY.md'), 'utf8');
  assert.deepEqual(glossaryProblems(md, builtPage('glossary.html').html), []);
});
