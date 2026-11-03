// S-003 TK-002 and TK-003 acceptance: every tour page the Spec names exists in the built output with a
// plain-language opener that uses no undefined term, then go deeper; a
// placeholder page fails. The site quotes no one: no page carries an owner
// quote, and a tour page holds no blockquote, <q> or quote marks. GitHub links
// name files that exist. Run `npm run build` first.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { builtPage, builtPages, visibleText } from './helpers.mjs';
import { TOUR, builtName, mainOf, ownerQuoteProblems, pageProblems, quoteProblems, repoLinks } from './tour-helpers.mjs';

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

  const fig = (said) => `<main><figure data-owner-quote=""><blockquote><p>${said}</p></blockquote><figcaption>Kayden, 2026-10-31</figcaption></figure></main>`;
  assert.ok(quoteProblems(fig('words the owner said, set out as a quotation')).length, 'an owner-quote figure passes');
  assert.ok(quoteProblems('<main><blockquote><p>words set out as a quotation</p></blockquote></main>').length, 'a blockquote passes');
  assert.ok(quoteProblems('<main><p>He called it <q>one loop for everything</q>.</p></main>').length, 'a <q> passes');
  assert.deepEqual(quoteProblems('<main><p>A page that quotes no one passes.</p></main>'), [], 'a page with no quote fails');
  assert.ok(quoteProblems('<main><p>Kayden called it “a tool belt wrapped in one loop”.</p></main>').length, 'loose quote marks pass');
  assert.deepEqual(ownerQuoteProblems([{ name: 'a.html', html: '<main><p>No quotes.</p></main>' }]), []);
});

for (const { href, title } of TOUR) {
  test(`${href} exists in the built output with its title, a plain-language opener and deeper sections`, () => {
    const { html } = builtPage(builtName(href));
    assert.match(visibleText(html.match(/<h1[\s\S]*?<\/h1>/i)?.[0] ?? ''), new RegExp(title), `${href}: <h1> is not "${title}"`);
    assert.match(html, new RegExp(`<title>${title} \\| Agentic Management System</title>`), `${href}: <title> missing`);
    assert.deepEqual(pageProblems(html), [], href);
  });

  test(`${href}: quotes no one (no owner-quote figure, blockquote, <q> or quote marks)`, () => {
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

// The quickstart on /start (S-003 Quickstart): a reading route of at least
// four linked stops with nothing to run, then a step telling the reader to use
// the setup-workbench skill, linked to its article and sourced to a record.
export function quickstartProblems(main) {
  const problems = [];
  const section = main.match(/<section\b[^>]*aria-labelledby="quickstart"[^>]*>([\s\S]*?)<\/section>/i)?.[1];
  if (!section) return ['no quickstart section (aria-labelledby="quickstart")'];
  const route = section.match(/<ol\b[^>]*data-route[^>]*>([\s\S]*?)<\/ol>/i)?.[1] ?? '';
  const stops = [...route.matchAll(/<li\b[\s\S]*?<\/li>/gi)].map((m) => m[0]);
  if (stops.length < 4) problems.push(`the reading route has ${stops.length} stops, fewer than four`);
  for (const s of stops) if (!/<a\b[^>]*href="[/#]/.test(s)) problems.push(`a route stop links nowhere on the site: ${visibleText(s).slice(0, 40)}`);
  if (/<pre\b|data-command/i.test(section)) problems.push('the quickstart shows commands to run');
  const setup = section.match(/<div\b[^>]*data-setup-step[^>]*>([\s\S]*?)<\/div>/i)?.[1] ?? '';
  if (!/\buse the\b[\s\S]*setup-workbench/i.test(visibleText(setup))) problems.push('no step telling the reader to use setup-workbench');
  if (!/href="\/skills\/setup-workbench"/.test(setup)) problems.push('the setup step does not link the setup-workbench article');
  if (!repoLinks(setup).some((l) => l.exists)) problems.push('the setup step cites no committed record');
  return problems;
}

test('the quickstart check catches faults (self-test)', () => {
  const main = mainOf(builtPage('start.html').html);
  assert.deepEqual(quickstartProblems(main), []);
  assert.ok(quickstartProblems(main.replace(/aria-labelledby="quickstart"/, 'aria-labelledby="x"')).length, 'a page without the quickstart passes');
  assert.ok(quickstartProblems(main.replace(/(<ol\b[^>]*data-route[^>]*>)<li\b[\s\S]*?<\/li>/i, '$1')).length, 'a three-stop route passes');
  assert.ok(quickstartProblems(main.replace(/(<ol\b[^>]*data-route[^>]*>)/i, '$1<pre data-command="x">git clone</pre>')).length, 'a command in the quickstart passes');
  assert.ok(quickstartProblems(main.replace(/href="\/skills\/setup-workbench"/g, 'href="/skills"')).length, 'a setup step without the article link passes');
  assert.ok(quickstartProblems(main.replace(/(data-setup-step[^>]*>[\s\S]*?)use the/i, '$1see the')).length, 'a setup step that does not say to use it passes');
});

test('/start ends with the quickstart: a reading route and the setup-workbench step', () => {
  assert.deepEqual(quickstartProblems(mainOf(builtPage('start.html').html)), []);
});

test('/how-it-works links one real Spec and one real Task to their files on GitHub', () => {
  const links = repoLinks(builtPage('how-it-works.html').html);
  assert.ok(links.some((l) => /\/SPEC\.md$/.test(l.path) && l.exists), 'no link to an existing SPEC.md');
  assert.ok(links.some((l) => /\/TASK\.md$/.test(l.path) && l.exists), 'no link to an existing TASK.md');
});

test('no built page carries an owner quote (data-owner-quote), with a planted fault caught', () => {
  const pages = builtPages();
  assert.deepEqual(ownerQuoteProblems(pages), []);
  const planted = pages.map((p, i) => (i === 0 ? { ...p, html: p.html.replace('</main>', '<figure data-owner-quote=""><blockquote><p>planted words</p></blockquote></figure></main>') } : p));
  assert.equal(ownerQuoteProblems(planted).length, 1, 'a planted owner quote on a built page passes');
});

test('every GitHub link on a built page names a file that exists in this repository', () => {
  for (const { name, html } of builtPages()) {
    for (const link of repoLinks(html)) assert.ok(link.exists, `${name}: ${link.href} names a missing file`);
  }
});

function historicalExampleProblems(html) {
  const section = html.match(/<section\b[^>]*aria-labelledby="example"[^>]*>([\s\S]*?)<\/section>/)?.[1];
  if (!section) return ['historical example section missing'];
  const links = repoLinks(section);
  const expected = ['SPEC.md', 'tasks/TK-001/TASK.md', 'tasks/TK-002/TASK.md'];
  const problems = [];
  for (const path of expected) {
    const link = links.find((l) => l.path.endsWith(`S-003-showcase-site/${path}`));
    if (!link) problems.push(`missing source: ${path}`);
    else {
      if (!/\/blob\/[a-f0-9]{40}\//.test(link.href)) problems.push(`mutable source: ${path}`);
      if (!link.exists) problems.push(`missing evidence: ${path}`);
    }
  }
  return problems;
}

test('historical example links stay pinned and resolve in their evidence revision', () => {
  const html = builtPage('how-it-works.html').html;
  assert.deepEqual(historicalExampleProblems(html), []);
  // A moving contextual source outside the example is valid. Inside the
  // example the same mutation must still fail the immutable-source contract.
  const contextual = '<a href="https://github.com/KaydenClark/Agentic-Management-System/blob/dev/workbench/landmarks/LMK-003-ams-website/specs/S-003-showcase-site/SPEC.md">context</a>';
  assert.deepEqual(historicalExampleProblems(contextual + html), []);
  const changed = html.replace(/(<section\b[^>]*aria-labelledby="example"[^>]*>[\s\S]*?)\/blob\/[a-f0-9]{40}\//, '$1/blob/dev/');
  assert.ok(historicalExampleProblems(changed).some((p) => p.startsWith('mutable source:')));
  const bad = repoLinks('<a href="https://github.com/KaydenClark/Agentic-Management-System/blob/ce39c6a89f92dffaebecb468b367c49ab6577bd8/no-such-record.md">missing</a>');
  assert.equal(bad[0].exists, false);
});
