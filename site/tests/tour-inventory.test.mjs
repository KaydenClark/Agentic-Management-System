// S-003 TK-002 and TK-003 acceptance: every tour page the Spec names exists in the built output with a
// plain-language opener that uses no undefined term, then go deeper; a
// placeholder page fails. Owner quotes link their dated source and are
// verbatim; a paraphrase is not shown as a quote. GitHub links name files that
// exist. Run `npm run build` first.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { builtPage, builtPages, visibleText } from './helpers.mjs';
import { TOUR, builtName, mainOf, pageProblems, quoteProblems, repoLinks } from './tour-helpers.mjs';

const filler = (n) => Array.from({ length: n }, (_, i) => `word${i}`).join(' ');
const page = ({ h1 = '<h1>T</h1>', opener, body = `<h2>A</h2><p>${filler(150)}</p><h2>B</h2><p>${filler(150)}</p>` }) =>
  `<html><body><main>${h1}${opener === null ? '' : `<p data-opener="">${opener}</p>`}${body}</main></body></html>`;
const PLAIN = 'This page explains in ordinary words how a person asks for work, how the work is checked and how anyone can see what was done and why it was done.';

test('the checks catch faults (self-test)', () => {
  assert.deepEqual(pageProblems(page({ opener: PLAIN })), []);
  assert.ok(pageProblems(page({ opener: null })).some((p) => /no plain-language opener/.test(p)));
  assert.ok(pageProblems(page({ opener: 'Under construction.' })).length, 'placeholder opener passes');
  assert.ok(pageProblems(page({ opener: PLAIN, body: '<h2>A</h2><p>Coming soon.</p>' })).length, 'placeholder page passes');
  assert.ok(pageProblems(page({ opener: `${PLAIN} Each Spec is reviewed.` })).some((p) => /"Spec"/.test(p)), 'undefined term passes');
  assert.deepEqual(pageProblems(page({ opener: `${PLAIN} Each <dfn>Spec</dfn>, a written plan, is reviewed.` })), []);
  assert.deepEqual(pageProblems(page({ opener: `${PLAIN} Each <a href="#spec">Spec</a> is reviewed.`, body: `<h2 id="spec">A</h2><p>${filler(150)}</p><h2>B</h2><p>${filler(150)}</p>` })), []);
  assert.ok(pageProblems(page({ opener: `${PLAIN} Each <a href="#nowhere">Spec</a> is reviewed.` })).length, 'link to a missing definition passes');

  const src = 'https://github.com/KaydenClark/Agentic-Management-System/blob/dev/workbench/wiki/context-ams-purpose.md';
  const fig = (said, caption) => `<main><figure data-owner-quote=""><blockquote><p>${said}</p></blockquote><figcaption>${caption}</figcaption></figure></main>`;
  const real = 'my full tool belt I use to work with AI wrapped up into one RSI loop that builds a website explaining itself.';
  assert.deepEqual(quoteProblems(fig(real, `Kayden, 2026-10-31, <a href="${src}">record</a>`)), []);
  assert.ok(quoteProblems(fig(real, 'Kayden, 2026-10-31')).length, 'quote without source passes');
  assert.ok(quoteProblems(fig(real, `Kayden, <a href="${src}">record</a>`)).length, 'undated quote passes');
  assert.ok(quoteProblems(fig('a tidy paraphrase of what the owner meant', `Kayden, 2026-10-31, <a href="${src}">record</a>`)).length, 'paraphrase shown as quote passes');
  assert.deepEqual(quoteProblems('<main><p>A page that quotes no one passes.</p></main>'), [], 'a page with no quote fails');
  assert.ok(quoteProblems('<main><p>Kayden called it “a tool belt wrapped in one loop”.</p></main>').length, 'loose quote marks pass');
});

for (const { href, title } of TOUR) {
  test(`${href} exists in the built output with its title, a plain-language opener and deeper sections`, () => {
    const { html } = builtPage(builtName(href));
    assert.match(visibleText(html.match(/<h1[\s\S]*?<\/h1>/i)?.[0] ?? ''), new RegExp(title), `${href}: <h1> is not "${title}"`);
    assert.match(html, new RegExp(`<title>${title} \\| Agentic Management System</title>`), `${href}: <title> missing`);
    assert.deepEqual(pageProblems(html), [], href);
  });

  test(`${href}: owner quotes are verbatim with a dated source; no paraphrase is shown as a quote`, () => {
    assert.deepEqual(quoteProblems(builtPage(builtName(href)).html), [], href);
  });
}

test('/start says what the AMS refuses to do', () => {
  const main = mainOf(builtPage('start.html').html);
  assert.match(main, /<h2\b[^>]*>[^<]*refuses[^<]*<\/h2>/i, 'no "refuses" section heading');
  const refusals = main.match(/<ul\b[^>]*data-refusals[^>]*>([\s\S]*?)<\/ul>/i);
  assert.ok(refusals, 'no refusal list (data-refusals)');
  const items = [...refusals[1].matchAll(/<li\b[\s\S]*?<\/li>/gi)].map((m) => m[0]);
  assert.ok(items.length >= 5, `only ${items.length} refusals listed`);
  for (const item of items) assert.ok(repoLinks(item).length, `refusal without a source record: ${visibleText(item)}`);
});

test('/how-it-works links one real Spec and one real Task to their files on GitHub', () => {
  const links = repoLinks(builtPage('how-it-works.html').html);
  assert.ok(links.some((l) => /\/SPEC\.md$/.test(l.path) && l.exists), 'no link to an existing SPEC.md');
  assert.ok(links.some((l) => /\/TASK\.md$/.test(l.path) && l.exists), 'no link to an existing TASK.md');
});

test('every GitHub link on a built page names a file that exists in this repository', () => {
  for (const { name, html } of builtPages()) {
    for (const link of repoLinks(html)) assert.ok(link.exists, `${name}: ${link.href} names a missing file`);
  }
});
