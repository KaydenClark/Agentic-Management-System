// S-008 acceptance over the built skills wiki: article shape, coverage of the
// chart, the index, credit and pin, no used marks and links. Each check runs
// its planted-fault self-test first. Run `npm run build` first.
// Coverage fails until every chart skill has an article in content/skills/.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { SKILLS_PIN, loadArticles, contentDir, parseFrontMatter } from '../app/skills/content.mjs';
import { stages } from '../app/start/skills.mjs';
import { builtPage, builtPages, servedFiles, siteDir } from './helpers.mjs';
import {
  INDEX_PAGE, STAGE_COUNTS, articleNameOf, articlePage, articleShapeProblems, contentFile, contentNames, coverageProblems,
  creditPageProblems, creditProblems, indexProblems, pinProblems, stageLabelProblems, usedMarkProblems, wikiLinkProblems,
} from './skills-helpers.mjs';

// A built article in the renderer's shape, with sections replaceable.
const SECTIONS = {
  'What it does': '<p>Does a thing.</p>',
  'When to use it': '<p>When needed.</p>',
  'Example request': '<blockquote><p>Do the thing.</p></blockquote>',
  'What it requires': '<p>A Workbench.</p>',
  'What it does not authorize': '<p>Merging.</p>',
  FAQs: '<h3>Is it safe?</h3><p>Yes.</p><h3>Can I stop?</h3><p>Yes.</p><h3>Does it write?</h3><p>No.</p>',
  'It&#x27;s working when': '<ul><li>It asks one question.</li></ul>',
  'Where it fits in the workflow': '<p>Align stage.</p>',
};
const credit = (kind = 'adapted', body = 'Adapted from a source, MIT License.') =>
  `<div data-credit-block=""><p data-credit="${kind}">${body}</p><p>Skills commit <code title="${SKILLS_PIN}" data-pin="${SKILLS_PIN}">8782412</code>${kind === 'adapted' ? ' · Source license: MIT' : ''}</p></div>`;
const article = ({ name = 'grilling', sections = Object.entries(SECTIONS), tail = credit(), stage = '<a href="/skills#align" data-stage-link="align">Align stage</a>' } = {}) =>
  `<html><body><main><article data-skill="${name}"><header><p>${stage}</p><h1>${name}</h1></header>` +
  sections.map(([t, html]) => `<section><h2 id="x">${t}</h2>${html}</section>`).join('') +
  `${tail}</article></main></body></html>`;
const without = (title) => Object.entries(SECTIONS).filter(([t]) => t !== title);
const swap = (a, b) => {
  const e = Object.entries(SECTIONS);
  const i = e.findIndex(([t]) => t === a);
  const j = e.findIndex(([t]) => t === b);
  [e[i], e[j]] = [e[j], e[i]];
  return e;
};
const withExtra = (at) => { const e = Object.entries(SECTIONS); e.splice(at, 0, ['Rounds and the frontier', '<p>Extra.</p>']); return e; };
const replace = (title, html) => Object.entries(SECTIONS).map(([t, h]) => [t, t === title ? html : h]);

test('the article shape check catches faults (self-test)', () => {
  assert.deepEqual(articleShapeProblems(article()), []);
  assert.deepEqual(articleShapeProblems(article({ sections: withExtra(5) })), [], 'a skill-specific section between 5 and 7 fails');
  assert.ok(articleShapeProblems(article({ sections: without('FAQs') })).length, 'no FAQs passes');
  assert.ok(articleShapeProblems(article({ sections: without('It&#x27;s working when') })).length, "no It's working when passes");
  assert.ok(articleShapeProblems(article({ sections: without('What it does not authorize') })).length, 'no What it does not authorize passes');
  assert.ok(articleShapeProblems(article({ sections: swap('When to use it', 'Example request') })).length, 'sections out of order pass');
  assert.ok(articleShapeProblems(article({ sections: swap('FAQs', 'Where it fits in the workflow') })).length, 'trailing sections out of order pass');
  assert.ok(articleShapeProblems(article({ sections: withExtra(2) })).length, 'an extra section inside the leading five passes');
  assert.ok(articleShapeProblems(article({ sections: withExtra(8) })).length, 'an extra section after the trailing three passes');
  assert.ok(articleShapeProblems(article({ sections: replace('FAQs', '<p>No questions here.</p>') })).length, 'FAQs without question headings pass');
  assert.ok(articleShapeProblems(article({ sections: replace('FAQs', '<h3>A statement.</h3><p>a</p><h3>Two?</h3><p>b</p><h3>Three?</h3><p>c</p>') })).length, 'a FAQ heading without ? passes');
  assert.ok(articleShapeProblems(article({ sections: replace('FAQs', '<h3>One?</h3><h3>Two?</h3><p>b</p><h3>Three?</h3><p>c</p>') })).length, 'a FAQ without an answer passes');
  assert.ok(articleShapeProblems(article({ sections: replace('It&#x27;s working when', '<p>It works.</p>') })).length, "It's working when without a list passes");
  assert.ok(articleShapeProblems(article({ tail: '' })).length, 'no credit line or pin passes');
  assert.ok(articleShapeProblems(article({ tail: '<div data-credit-block=""><p data-credit="original">Original to Kayden Clark.</p></div>' })).length, 'no pin passes');
  assert.ok(articleShapeProblems('<main><p>Not an article.</p></main>').length, 'a page with no article passes');
});

test('the coverage check catches faults (self-test)', () => {
  const all = stages.flatMap((s) => [...s.main, ...s.used]);
  assert.deepEqual(coverageProblems(all, stages), []);
  assert.ok(coverageProblems(all.filter((n) => n !== 'land'), stages).some((p) => /land/.test(p)), 'a missing chart skill passes');
  assert.ok(coverageProblems([...all.filter((n) => n !== 'align-concept'), 'grill-me'], stages).some((p) => /grill-me/.test(p)), 'an article named grill-me passes');
  assert.ok(coverageProblems([...all, 'grill-with-docs'], stages).some((p) => /grill-with-docs/.test(p)), 'an article named grill-with-docs passes');
  assert.ok(coverageProblems([...all, 'ponder'], stages).some((p) => /ponder/.test(p)), 'an article for a skill not on the chart passes');
  const orphan = [...stages, { id: 'extra', name: 'Extra', gloss: 'None', main: [], used: [] }];
  assert.ok(coverageProblems(all, orphan).some((p) => /orphan stage/.test(p)), 'an orphan stage passes');
});

test('the chart names 39 skills in the Spec counts per stage, every stage at least one', () => {
  assert.deepEqual(Object.fromEntries(stages.map((s) => [s.id, s.main.length + s.used.length])), STAGE_COUNTS);
  for (const s of stages) assert.ok(s.main.length + s.used.length > 0, `stage ${s.name} names no skill`);
});

test('every chart skill has exactly one article under its repository name, and no other article exists', () => {
  assert.deepEqual(coverageProblems(contentNames(), stages), []);
});

test('the index check catches faults (self-test)', () => {
  const st = [
    { id: 'align', name: 'Align', gloss: 'Shared concept', main: ['grilling', 'readback'], used: ['jot'] },
    { id: 'judge', name: 'Judge', gloss: 'Review, verify', main: ['code-review'], used: [], note: 'Findings become a new Journey.' },
  ];
  const li = (n, flow) => `<li data-skill="${n}" data-flow="${flow}"><a href="/skills/${n}">${n}</a><p data-summary="">Summary of ${n}.</p></li>`;
  const sec = (id, name, gloss, items, note = '') => `<section id="${id}" data-stage="${id}"><h2>${name}</h2><p>${gloss}</p>${note}${items}</section>`;
  const index = (align, judge = li('code-review', 'main'), note = '<p>Findings become a new Journey.</p>') =>
    `<main>${sec('align', 'Align', 'Shared concept', align)}${sec('judge', 'Judge', 'Review, verify', judge, note)}</main>`;
  const names = ['grilling', 'readback', 'jot', 'code-review'];
  const good = li('grilling', 'main') + li('readback', 'main') + li('jot', 'used');
  assert.deepEqual(indexProblems(index(good), names, st), []);
  assert.ok(indexProblems(index(li('grilling', 'main') + li('readback', 'main')), names, st).length, 'an article missing from the index passes');
  assert.ok(indexProblems(index(li('readback', 'main') + li('grilling', 'main') + li('jot', 'used')), names, st).length, 'main flow out of order passes');
  assert.ok(indexProblems(index(li('jot', 'used') + li('grilling', 'main') + li('readback', 'main')), names, st).length, 'used before main flow passes');
  assert.ok(indexProblems(index(li('grilling', 'main') + li('readback', 'main'), li('code-review', 'main') + li('jot', 'used')), names, st).length, 'a skill under the wrong stage passes');
  assert.ok(indexProblems(index(good.replace('href="/skills/jot"', 'href="/skills"')), names, st).length, 'an entry with no article link passes');
  assert.ok(indexProblems(index(good.replace('Summary of jot.', '')), names, st).length, 'an entry with no summary passes');
  assert.ok(indexProblems(index(good, li('code-review', 'main'), ''), names, st).length, 'a stage without its note passes');
  assert.ok(indexProblems(`<main>${sec('judge', 'Judge', 'Review, verify', li('code-review', 'main'), '<p>Findings become a new Journey.</p>')}${sec('align', 'Align', 'Shared concept', good)}</main>`, names, st).length, 'stages out of chart order pass');
});

test('the stage label check catches faults (self-test)', () => {
  assert.deepEqual(stageLabelProblems(article(), stages), []);
  assert.ok(stageLabelProblems(article({ stage: '<a href="/skills#judge" data-stage-link="judge">Judge stage</a>' }), stages).length, 'a wrong stage passes');
  assert.ok(stageLabelProblems(article({ stage: 'Align stage' }), stages).length, 'an unlinked stage label passes');
});

test('the credit and pin checks catch faults (self-test)', () => {
  const adapted = { credit: 'adapted', credit_text: 'Adapted from a source, MIT License.', credit_license: 'MIT' };
  const original = { credit: 'original', credit_text: 'Original to Kayden Clark.' };
  assert.deepEqual(creditProblems(adapted), []);
  assert.deepEqual(creditProblems(original), []);
  assert.ok(creditProblems({ ...adapted, credit_license: '' }).length, 'adapted without a license passes');
  assert.ok(creditProblems({ ...adapted, credit_text: 'Original to Kayden Clark.' }).length, 'an adapted skill labeled original passes');
  assert.ok(creditProblems({ ...original, credit_text: 'Written by Kayden.' }).length, 'original without the original text passes');
  assert.ok(creditProblems({ ...original, credit_license: 'MIT' }).length, 'original with a license passes');
  assert.ok(creditProblems({ credit: 'borrowed', credit_text: 'x' }).length, 'an unknown credit kind passes');
  assert.deepEqual(creditPageProblems(article(), adapted), []);
  assert.ok(creditPageProblems(article({ tail: credit('original', 'Original to Kayden Clark.') }), adapted).length, 'an adapted skill shown as original passes');
  assert.ok(creditPageProblems(article({ tail: credit('adapted').replace(' · Source license: MIT', '') }), adapted).length, 'an adapted page without its license passes');
  assert.deepEqual(pinProblems(article()), []);
  assert.ok(pinProblems(article({ tail: credit().replaceAll(SKILLS_PIN, '0'.repeat(40)) })).length, 'a wrong pin passes');
  assert.ok(pinProblems(article({ tail: '' })).length, 'no pin passes');
});

test('the used-mark check catches faults (self-test)', () => {
  const page = (body) => `<html><body><main>${body}</main></body></html>`;
  assert.deepEqual(usedMarkProblems(page('<p>Use it to build each Task test-first; it is used for planning.</p>')), []);
  assert.ok(usedMarkProblems(page('<p>This skill was used to build this site.</p>')).length, 'a used-to-build sentence passes');
  assert.ok(usedMarkProblems(page('<p>Used in building the AMS website pages.</p>')).length, 'a used-in-building sentence passes');
  assert.ok(usedMarkProblems(page('<p>The site was built with grilling and map.</p>')).length, 'a built-with sentence passes');
  assert.ok(usedMarkProblems(page('<span class="badge" data-used="">Used</span>')).length, 'a data-used badge passes');
  assert.ok(usedMarkProblems(page('<h2>Used on this site</h2><ul><li>/start</li></ul>')).length, 'a list of uses passes');
});

test('the link check catches faults (self-test)', () => {
  const ctx = { articles: new Set(['grilling']), pages: new Set(['start.html', 'skills.html', 'index.html']), indexIds: new Set(['align']) };
  assert.deepEqual(wikiLinkProblems('<a href="/skills/grilling">g</a><a href="/skills#align">a</a><a href="/start">s</a><a href="https://example.com">e</a>', ctx), []);
  assert.ok(wikiLinkProblems('<a href="/skills/readback">r</a>', ctx).length, 'a link to a missing article passes');
  assert.ok(wikiLinkProblems('<a href="/skills#nowhere">n</a>', ctx).length, 'a link to a missing index anchor passes');
  assert.ok(wikiLinkProblems('<a href="/glossary">g</a>', ctx).length, 'a link to a missing page passes');
  assert.ok(wikiLinkProblems('<a href="https://github.com/KaydenClark/skills/blob/main/grilling/SKILL.md">src</a>', ctx).length, 'a link to the private skills repository passes');
});

// The real build.
const articles = () => loadArticles(contentDir(siteDir));
const builtArticles = () => builtPages().filter((p) => articleNameOf(p.name));

test('every content file is built as a static article page, and nothing else is', () => {
  const built = builtArticles().map((p) => articleNameOf(p.name)).sort();
  assert.deepEqual(built, contentNames());
});

test('every built article has sections 1-5 and 7-9 in order, FAQs, a working-when list, a credit line and the pin', () => {
  for (const { name, html } of builtArticles()) assert.deepEqual(articleShapeProblems(html), [], name);
});

test('every built article names its chart stage and links it on the index', () => {
  for (const { name, html } of builtArticles()) assert.deepEqual(stageLabelProblems(html, stages), [], name);
});

test('/skills lists every article under its chart stage, main flow first in order, each linking its page', () => {
  assert.deepEqual(indexProblems(builtPage(INDEX_PAGE).html, contentNames(), stages), []);
});

test('every article credits its source as its front matter states and names the pinned skills commit', () => {
  for (const name of contentNames()) {
    const { data } = parseFrontMatter(readFileSync(contentFile(name), 'utf8'), name);
    assert.deepEqual(creditProblems(data), [], name);
    assert.equal(data.pin, SKILLS_PIN, `${name}: front matter pin`);
    const { html } = builtPage(articlePage(name));
    assert.deepEqual(creditPageProblems(html, data), [], name);
    assert.deepEqual(pinProblems(html), [], name);
  }
});

test('no page marks a skill as used to build the site', () => {
  for (const { name, html } of builtPages()) assert.deepEqual(usedMarkProblems(html), [], name);
});

test('wiki links resolve to built articles, index anchors or pages, and nothing links the private skills repository', () => {
  const pages = new Set(builtPages().map((p) => p.name));
  const ctx = {
    articles: new Set(builtArticles().map((p) => articleNameOf(p.name))),
    pages,
    indexIds: new Set([...builtPage(INDEX_PAGE).html.matchAll(/\sid="([^"]+)"/g)].map((m) => m[1])),
  };
  for (const { name, html } of [builtPage(INDEX_PAGE), ...builtArticles()]) assert.deepEqual(wikiLinkProblems(html, ctx), [], name);
  for (const { name, text } of servedFiles()) assert.doesNotMatch(text, /github\.com\/KaydenClark\/skills(?![\w.-])/i, `${name} links the private skills repository`);
});

test('the loader reads every article without error, in index order', () => {
  const order = stages.flatMap((s) => [...s.main, ...s.used]);
  const names = articles().map((a) => a.name);
  assert.deepEqual(names, [...names].sort((a, b) => order.indexOf(a) - order.indexOf(b)));
});
