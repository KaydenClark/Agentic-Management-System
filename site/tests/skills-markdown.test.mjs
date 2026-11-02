// S-008: the skills wiki's restricted Markdown and article loader. The
// fixture articles in tests/fixtures/skills/ parse; every syntax outside the
// article contract, and every contract breach in front matter or section
// order, is refused with the file named, so the build fails loudly.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { join } from 'node:path';
import { SKILLS_PIN, loadArticles, parseArticle } from '../app/skills/content.mjs';
import { inlineText, parseMarkdown, slug } from '../app/skills/markdown.mjs';
import { siteDir } from './helpers.mjs';

const FIXTURES = join(siteDir, 'tests', 'fixtures', 'skills');
const fixture = (name) => readFileSync(join(FIXTURES, `${name}.md`), 'utf8');

test('the fixture articles load in index order with every supported block', () => {
  const articles = loadArticles(FIXTURES);
  assert.deepEqual(articles.map((a) => a.name), ['grilling', 'readback', 'map']);
  const g = articles[0];
  assert.equal(g.stage.id, 'align');
  assert.equal(g.flow, 'main');
  assert.equal(g.step, 1);
  assert.equal(g.credit, 'adapted');
  assert.equal(g.creditLicense, 'MIT');
  assert.equal(g.pin, SKILLS_PIN);
  assert.deepEqual(g.sections.map((s) => s.title), ['What it does', 'When to use it', 'Example request', 'What it requires', 'What it does not authorize', 'Rounds and the frontier', 'FAQs', "It's working when", 'Where it fits in the workflow']);
  assert.equal(g.sections.find((s) => s.title === "It's working when").id, 'its-working-when');
  const types = new Set(g.sections.flatMap((s) => s.blocks.map((b) => b.type)));
  for (const t of ['paragraph', 'list', 'table', 'blockquote', 'code', 'heading']) assert.ok(types.has(t), `fixture has no ${t}`);
  const table = g.sections[1].blocks.find((b) => b.type === 'table');
  assert.equal(table.rows.length, 3);
  assert.match(inlineText(table.rows[2][0]), /a pipe \| inside/);
  assert.ok(g.links.includes('/skills#align') && g.links.includes('https://example.com/skills'));
  assert.equal(articles[1].credit, 'original');
});

test('inline Markdown: code, bold, italic, links and escapes', () => {
  const [p] = parseMarkdown('A `code` **bold *nested*** and *it* [link](/start) \\*not\\* 5 * 3 snake_case.', 'x.md');
  assert.deepEqual(p.inline.map((n) => n.type), ['text', 'code', 'text', 'strong', 'text', 'em', 'text', 'link', 'text']);
  assert.equal(inlineText(p.inline), 'A code bold nested and it link *not* 5 * 3 snake_case.');
  assert.equal(slug("It's working when"), 'its-working-when');
});

const refused = [
  ['# Title', /# headings/],
  ['#### Deep', /#### headings/],
  ['##No space', /followed by a space/],
  ['<div>raw</div>', /raw HTML/],
  ['Some <b>bold</b> text', /raw HTML/],
  ['See <https://example.com>', /autolinks/],
  ['![alt](/x.png)', /images/],
  ['A note[^1]', /footnotes/],
  ['[^1]: note', /footnotes/],
  ['[ref]: https://example.com', /reference link/],
  ['A [ref][x] link', /reference links/],
  ['- one\n  - nested', /nested lists/],
  ['* star bullet', /use - for bullet/],
  ['+ plus bullet', /use - for bullet/],
  ['1) paren', /1\. markers/],
  ['Some _underscore_ emphasis', /underscore/],
  ['~~gone~~', /strikethrough/],
  ['---', /thematic breaks/],
  ['Heading\n===', /setext/],
  ['    indented code', /indented/],
  ['~~~\ncode\n~~~', /~~~ fences/],
  ['```\nunclosed', /unclosed ``` fence/],
  ['Use &mdash; here', /character references/],
  ['An `unclosed code', /unclosed inline code/],
  ['An **unclosed bold', /unclosed \*\*bold\*\*/],
  ['An *unclosed italic', /unclosed \*italic\*/],
  ['A [link](with space)', /has spaces/],
  ['| a | b |\n| --- | --- |\n| 1 |', /row has 1 cells/],
  ['| a | b |\n| 1 | 2 |', /separator row/],
  ['> > nested', /nested blockquotes/],
  ['> - list in quote', /only paragraphs/],
  ['***strong em***', /\*\*\* emphasis/],
];

for (const [src, why] of refused) {
  test(`refuses unsupported Markdown: ${JSON.stringify(src)}`, () => {
    assert.throws(() => parseMarkdown(src, 'x.md'), (e) => e.name === 'MarkdownError' && why.test(e.message) && /^x\.md:\d+:/.test(e.message));
  });
}

// Planted faults in a valid fixture article, each refused by the loader.
const grilling = fixture('grilling');
const readback = fixture('readback');
const cut = (src, heading) => src.replace(new RegExp(`## ${heading}\\n[\\s\\S]*?(?=\\n## |$)`), '');
const article = [
  ['no FAQs section', cut(grilling, 'FAQs'), /no ## FAQs/],
  ["no It's working when section", cut(grilling, "It's working when"), /no ## It's working when/],
  ['no What it does not authorize section', cut(grilling, 'What it does not authorize'), /no ## What it does not authorize/],
  ['sections out of order', grilling.replace('## When to use it', '## TMP').replace('## Example request', '## When to use it').replace('## TMP', '## Example request'), /out of order|Example request must open/],
  ['an extra section before the fifth', grilling.replace('## What it requires', '## Extra\n\nText.\n\n## What it requires'), /skill-specific sections go only between/],
  ['an extra section at the end', `${grilling}\n## Afterword\n\nText.\n`, /skill-specific sections go only between/],
  ['a FAQ heading without ?', grilling.replace('### Can I stop early?', '### Can I stop early'), /does not end with \?/],
  ['a FAQ with no answer', grilling.replace('Yes, say so.\n', ''), /has no answer/],
  ['too few FAQs', readback.replace(/### Does it link anything\?[\s\S]*?(?=\n## )/, ''), /takes 3 to 6/],
  ["It's working when without a list", grilling.replace('- Each round asks one question.\n- You can say what was settled.', 'It works.'), /single - bullet list/],
  ['an example request without a blockquote', grilling.replace('> Grill me on this plan before we write the Spec.', 'Grill me.'), /> blockquote/],
  ['a When to use it table with another header', grilling.replace('| What you have | Reach for |', '| Have | Use |'), /What you have \| Reach for/],
  ['Where it fits not naming its stage', grilling.replace('of the Align stage', 'of its stage'), /does not name its stage, Align/],
  ['a name not matching its file', grilling.replace('name: grilling', 'name: readback'), /does not match the file name/],
  ['an article for a skill not on the chart', grilling.replace('name: grilling', 'name: ponder'), /not a skill on the chart/],
  ['an article named grill-me', grilling.replace('name: grilling', 'name: grill-me'), /not a skill on the chart/],
  ['a wrong pin', grilling.replace(SKILLS_PIN, '1'.repeat(40)), /is not the skills commit/],
  ['an adapted skill labeled original', grilling.replace(/credit_text: .*/, 'credit_text: Original to Kayden Clark.'), /never labeled original/],
  ['an adapted skill with no license', grilling.replace(/credit_license: .*\n/, ''), /needs credit_license/],
  ['an original skill with other credit text', readback.replace('credit_text: Original to Kayden Clark.', 'credit_text: By Kayden.'), /credit: original needs credit_text/],
  ['an unknown front matter key', grilling.replace('pin:', 'stage: align\npin:'), /unknown front matter key stage/],
  ['a summary over 160 characters', grilling.replace(/summary: .*/, `summary: ${'x'.repeat(161)}`), /at most 160/],
  ['a link to the private skills repository', grilling.replace('https://example.com/skills', 'https://github.com/KaydenClark/skills'), /private skills repository/],
  ['a link to a skill not on the chart', grilling.replace('(/skills/map)', '(/skills/teach)'), /not a chart skill/],
  ['a link to an unknown site route', grilling.replace('(/start)', '(/glossary)'), /not a site route/],
  ['an http link', grilling.replace('https://example.com/skills', 'http://example.com/skills'), /only \/skills\/<name>/],
  ['a # title in the body', grilling.replace('## What it does\n', '# grilling\n\n## What it does\n'), /# headings/],
  ['text before the first section', grilling.replace('## What it does\n', 'Intro.\n\n## What it does\n'), /open with a ## section/],
];

for (const [label, src, why] of article) {
  test(`refuses an article with ${label}`, () => {
    const file = label === 'a name not matching its file' ? 'skills/grilling.md' : `skills/${src.match(/^name: (.*)$/m)?.[1] ?? 'x'}.md`;
    assert.throws(() => parseArticle(src, { file }), (e) => why.test(e.message) && e.message.startsWith('skills/'), label);
  });
}
