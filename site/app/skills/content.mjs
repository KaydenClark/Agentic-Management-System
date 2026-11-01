// The skills wiki's articles (S-008): one Markdown file per chart skill in
// content/skills/<name>.md, in the shape of the S-008 article contract.
// Loading validates the front matter, the nine-section order and every link,
// and throws naming the file on anything outside the contract, so the build
// fails instead of publishing a malformed article. Stage and order come from
// app/start/skills.mjs, the chart's one encoding; an article never states its
// stage. Coverage (every chart skill has an article) is a test, not a build
// rule, so the site still builds while articles are being written.
// Plain JavaScript so the tests import it on any Node; types in content.d.mts.
import { existsSync, readdirSync, readFileSync } from 'node:fs';
import { basename, join } from 'node:path';
import { stages } from '../start/skills.mjs';
import { inlineText, parseInline, parseMarkdown, slug } from './markdown.mjs';

// The skills repository commit every article is derived from (owner,
// 2026-11-01). A later pin updates the affected articles.
export const SKILLS_PIN = '878241202bf7ec97c0952287f1633f6f0ddf1a6e';
export const SKILLS_PIN_SHORT = SKILLS_PIN.slice(0, 7);
export const ORIGINAL_CREDIT = 'Original to Kayden Clark.';

// The article's fixed sections, in order; optional skill-specific sections go
// between the leading five and the trailing three.
export const LEADING_SECTIONS = ['What it does', 'When to use it', 'Example request', 'What it requires', 'What it does not authorize'];
export const TRAILING_SECTIONS = ['FAQs', "It's working when", 'Where it fits in the workflow'];
export const FIXED_SECTIONS = [...LEADING_SECTIONS, ...TRAILING_SECTIONS];
export const REACH_FOR_HEADER = ['What you have', 'Reach for'];
export const FAQ_RANGE = [3, 6];

// Site routes an article may link besides /skills/<name>: the reading order
// of app/nav.ts (a test keeps the two equal; nav.ts is TypeScript, which
// this plain module cannot import).
export const SITE_ROUTES = ['/', '/start', '/how-it-works', '/skills', '/rsi'];
// The skills repository is private: a link to it is a 404 for readers.
export const PRIVATE_SKILLS_REPO = /github\.com\/KaydenClark\/skills(?![\w.-])/i;

const KEYS = ['name', 'summary', 'pin', 'credit', 'credit_text', 'credit_license'];
const SUMMARY_MAX = 160;

export const contentDir = (siteDir = process.cwd()) => join(siteDir, 'content', 'skills');

// Every chart skill in index order: each stage in chart order, its main-flow
// skills in the order they run, then the skills also used at that stage.
export function chartSkills(chart = stages) {
  const out = [];
  for (const stage of chart) {
    stage.main.forEach((name, k) => out.push({ name, stage, flow: 'main', step: k + 1 }));
    stage.used.forEach((name) => out.push({ name, stage, flow: 'used', step: null }));
  }
  return out;
}

class ArticleError extends Error {
  constructor(file, message) {
    super(`${file}: ${message}`);
    this.name = 'ArticleError';
  }
}

export function parseFrontMatter(src, file) {
  const text = src.replace(/\r\n?/g, '\n');
  if (!text.startsWith('---\n')) throw new ArticleError(file, 'must open with a --- front matter line');
  const end = text.indexOf('\n---\n', 3);
  if (end < 0) throw new ArticleError(file, 'front matter is not closed with a --- line');
  const data = {};
  const lines = text.slice(4, end).split('\n');
  lines.forEach((line, k) => {
    if (!line.trim()) return;
    const m = line.match(/^([a-z_]+):[ \t]*(.*)$/);
    if (!m) throw new ArticleError(file, `front matter line ${k + 2} is not key: value`);
    const [, key, rawValue] = m;
    if (!KEYS.includes(key)) throw new ArticleError(file, `unknown front matter key ${key} (allowed: ${KEYS.join(', ')})`);
    if (key in data) throw new ArticleError(file, `front matter key ${key} appears twice`);
    let value = rawValue.trim();
    if (value.length >= 2 && value.startsWith('"') && value.endsWith('"')) value = value.slice(1, -1);
    data[key] = value;
  });
  const body = text.slice(end + 5);
  const bodyLine = text.slice(0, end + 5).split('\n').length;
  return { data, body, bodyLine };
}

function walkInline(nodes, visit) {
  for (const n of nodes) {
    visit(n);
    if (n.children) walkInline(n.children, visit);
  }
}

function blockInlines(block) {
  switch (block.type) {
    case 'heading':
    case 'paragraph':
      return [block.inline];
    case 'list':
      return block.items;
    case 'table':
      return [...block.header, ...block.rows.flat()];
    case 'blockquote':
      return block.paragraphs;
    default:
      return [];
  }
}

const blockText = (block) => (block.type === 'code' ? block.text : blockInlines(block).map(inlineText).join(' '));

// Why a link target is not allowed in an article, or null when it is.
export function hrefProblem(href, chart = stages) {
  if (href.startsWith('/')) {
    if (SITE_ROUTES.includes(href)) return null;
    const skill = href.match(/^\/skills\/([a-z0-9-]+)$/);
    if (skill) return chartSkills(chart).some((s) => s.name === skill[1]) ? null : `links /skills/${skill[1]}, which is not a chart skill`;
    const stage = href.match(/^\/skills#([a-z0-9-]+)$/);
    if (stage && chart.some((st) => st.id === stage[1])) return null;
    return `links ${href}, which is not a site route an article may link (${SITE_ROUTES.join(', ')}, /skills/<name>, /skills#<stage>)`;
  }
  if (/^https:\/\//.test(href)) {
    let url;
    try { url = new URL(href); } catch { return `links ${href}, which is not a valid URL`; }
    if (PRIVATE_SKILLS_REPO.test(`${url.host}${url.pathname}`)) return 'links the private skills repository (readers get a 404); name the commit instead';
    return null;
  }
  return `links ${href}; only /skills/<name>, a site route or a public https:// URL are allowed`;
}

// One article's source to its validated, renderable form.
export function parseArticle(src, { file = 'article.md', chart = stages } = {}) {
  const { data, body, bodyLine } = parseFrontMatter(src, file);
  const fail = (message) => { throw new ArticleError(file, message); };
  const inline = (text, key) => parseInline(text, (message) => fail(`${key}: ${message}`));

  for (const key of ['name', 'summary', 'pin', 'credit', 'credit_text']) if (!data[key]) fail(`front matter has no ${key}`);
  const { name } = data;
  if (!/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(name)) fail(`name ${name} is not a skill folder name`);
  if (file.endsWith('.md') && basename(file, '.md') !== name) fail(`name ${name} does not match the file name ${basename(file)}`);
  const place = chartSkills(chart).find((s) => s.name === name);
  if (!place) fail(`${name} is not a skill on the chart (app/start/skills.mjs); only chart skills get articles`);

  if (data.summary.length > SUMMARY_MAX) fail(`summary is ${data.summary.length} characters; at most ${SUMMARY_MAX}`);
  if (data.pin !== SKILLS_PIN) fail(`pin ${data.pin} is not the skills commit ${SKILLS_PIN}`);

  if (data.credit === 'original') {
    if (data.credit_text !== ORIGINAL_CREDIT) fail(`credit: original needs credit_text: ${ORIGINAL_CREDIT}`);
    if (data.credit_license) fail('credit: original takes no credit_license');
  } else if (data.credit === 'adapted') {
    if (!data.credit_license) fail('credit: adapted needs credit_license (the source license, e.g. MIT)');
    if (/^\s*original\b/i.test(data.credit_text)) fail('an adapted skill is never labeled original; credit_text must name the source');
  } else {
    fail(`credit is ${data.credit}; it must be original or adapted`);
  }

  const summary = inline(data.summary, 'summary');
  const creditText = inline(data.credit_text, 'credit_text');
  const blocks = parseMarkdown(body, file, bodyLine);

  // Sections: split at each ## heading.
  if (!blocks.length) fail('has no body');
  if (blocks[0].type !== 'heading' || blocks[0].level !== 2) fail('the body must open with a ## section heading');
  const sections = [];
  for (const block of blocks) {
    if (block.type === 'heading' && block.level === 2) {
      const title = inlineText(block.inline).trim();
      sections.push({ title, id: slug(title), blocks: [], line: block.line });
    } else {
      sections[sections.length - 1].blocks.push(block);
    }
  }
  const titles = sections.map((s) => s.title);
  for (const s of sections) if (!s.blocks.length) fail(`section ${s.title} is empty`);
  const dupe = titles.find((t, k) => titles.indexOf(t) !== k);
  if (dupe) fail(`section ${dupe} appears twice`);
  for (const t of FIXED_SECTIONS) if (!titles.includes(t)) fail(`has no ## ${t} section`);
  const fixedOrder = titles.filter((t) => FIXED_SECTIONS.includes(t));
  if (fixedOrder.join('|') !== FIXED_SECTIONS.join('|')) fail(`sections are out of order: ${fixedOrder.join(', ')}; expected ${FIXED_SECTIONS.join(', ')}`);
  const lead = titles.slice(0, LEADING_SECTIONS.length);
  const trail = titles.slice(-TRAILING_SECTIONS.length);
  if (lead.join('|') !== LEADING_SECTIONS.join('|') || trail.join('|') !== TRAILING_SECTIONS.join('|')) {
    fail(`skill-specific sections go only between ${LEADING_SECTIONS.at(-1)} and ${TRAILING_SECTIONS[0]}; found ${titles.join(', ')}`);
  }
  const section = (title) => sections.find((s) => s.title === title);

  const example = section('Example request').blocks;
  if (example[0].type !== 'blockquote') fail('Example request must open with the request as a > blockquote');
  if (example.filter((b) => b.type === 'blockquote').length !== 1) fail('Example request has exactly one > blockquote');
  if (example.slice(1).some((b) => b.type !== 'paragraph')) fail('Example request takes only a sentence or two after the blockquote');

  for (const b of section('When to use it').blocks) {
    if (b.type === 'table' && b.header.map((h) => inlineText(h).trim()).join('|') !== REACH_FOR_HEADER.join('|')) {
      fail(`a table in When to use it has the header | ${REACH_FOR_HEADER.join(' | ')} |`);
    }
  }

  const faqs = section('FAQs').blocks;
  if (!(faqs[0].type === 'heading' && faqs[0].level === 3)) fail('FAQs must open with a ### question');
  const questions = faqs.filter((b) => b.type === 'heading');
  faqs.forEach((b, k) => {
    if (b.type !== 'heading') return;
    if (b.level !== 3) fail('FAQs uses ### for each question');
    if (!inlineText(b.inline).trim().endsWith('?')) fail(`FAQ question ${inlineText(b.inline)} does not end with ?`);
    const next = faqs[k + 1];
    if (!next || next.type === 'heading') fail(`FAQ question ${inlineText(b.inline)} has no answer`);
  });
  if (questions.length < FAQ_RANGE[0] || questions.length > FAQ_RANGE[1]) fail(`FAQs has ${questions.length} questions; it takes ${FAQ_RANGE[0]} to ${FAQ_RANGE[1]}`);

  const working = section("It's working when").blocks;
  if (working.length !== 1 || working[0].type !== 'list' || working[0].ordered) fail("It's working when is a single - bullet list and nothing else");

  const fits = section('Where it fits in the workflow').blocks;
  if (!new RegExp(`\\b${place.stage.name}\\b`).test(fits.map(blockText).join(' '))) fail(`Where it fits in the workflow does not name its stage, ${place.stage.name}`);

  // Ids: sections by title, ### headings by text, unique on the page.
  const used = new Set(['main', ...chart.map((st) => st.id)]);
  const unique = (base) => {
    let id = base;
    for (let n = 2; used.has(id); n++) id = `${base}-${n}`;
    used.add(id);
    return id;
  };
  for (const s of sections) {
    s.id = unique(s.id);
    for (const b of s.blocks) if (b.type === 'heading') b.id = unique(slug(inlineText(b.inline)));
  }

  // Links anywhere in the article.
  const links = [];
  const collect = (nodes) => walkInline(nodes, (n) => { if (n.type === 'link') links.push(n.href); });
  collect(summary);
  collect(creditText);
  for (const b of blocks) blockInlines(b).forEach(collect);
  for (const href of links) {
    const problem = hrefProblem(href, chart);
    if (problem) fail(problem);
  }

  return {
    name,
    file,
    summary,
    summaryText: inlineText(summary),
    pin: data.pin,
    credit: data.credit,
    creditText,
    creditLicense: data.credit_license || null,
    stage: place.stage,
    flow: place.flow,
    step: place.step,
    sections: sections.map(({ title, id, blocks: b }) => ({ title, id, blocks: b })),
    links,
    body,
  };
}

// Every article in `dir`, in index order. A missing folder is no articles.
// Read only while pages are prerendered at build time (every wiki route is
// static), so the reads are kept out of Turbopack's output file tracing.
export function loadArticles(dir = contentDir(), { chart = stages } = {}) {
  if (!existsSync(/* turbopackIgnore: true */ dir)) return [];
  const label = basename(dir);
  const files = readdirSync(/* turbopackIgnore: true */ dir).filter((f) => !f.startsWith('.')).sort();
  const odd = files.find((f) => !f.endsWith('.md'));
  if (odd) throw new ArticleError(`${label}/${odd}`, 'only <name>.md article files belong in the skills content folder');
  const articles = files.map((f) => parseArticle(readFileSync(/* turbopackIgnore: true */ join(dir, f), 'utf8'), { file: `${label}/${f}`, chart }));
  const order = chartSkills(chart).map((s) => s.name);
  return articles.sort((a, b) => order.indexOf(a.name) - order.indexOf(b.name));
}
