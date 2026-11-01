// Shared checks for the S-003 tour tests (TK-002). Each check is a pure
// function over built HTML so the tests can run it on the real build and on
// planted faults. Run `npm run build` first.
import { existsSync, readFileSync } from 'node:fs';
import { join } from 'node:path';
import { siteDir, visibleText } from './helpers.mjs';

export const repoRoot = join(siteDir, '..');
export const REPO_BLOB = 'https://github.com/KaydenClark/Agentic-Management-System/blob/dev/';

// The reading order the tour must follow, in order (owner of the list:
// app/nav.ts; this is the expectation it is tested against).
export const READING_ORDER = ['/', '/start', '/how-it-works', '/skills', '/rsi'];

// The tour pages this Task delivers.
export const TOUR = [
  { href: '/start', title: 'Start here' },
  { href: '/how-it-works', title: 'How it works' },
];

// Route -> prerendered file name under .next/server/app/.
export const builtName = (href) => (href === '/' ? 'index.html' : `${href.slice(1)}.html`);

// Words a non-engineer may not know. If one appears in an opener it must be
// defined there (<dfn>) or linked to its definition (an on-page anchor or the
// Glossary). Matching is case-insensitive on whole words, plural allowed.
export const JARGON = [
  'AMS', 'agent', 'RSI', 'Spec', 'Task', 'record', 'repository', 'repo', 'commit', 'branch', 'merge',
  'pull request', 'PR', 'Workbench', 'lifecycle', 'orchestrator', 'deployment', 'deploy', 'Glossary',
  'Taskboard', 'ADR', 'DDR', 'CDR', 'skill', 'workflow', 'intent', 'acceptance', 'claim', 'eval',
];

const PLACEHOLDER = /under construction|placeholder|lorem ipsum|coming soon|\bTODO\b|\bTBD\b|\bFIXME\b|\[title\]/i;

export function opener(html) {
  const m = html.match(/<p\b[^>]*data-opener[^>]*>([\s\S]*?)<\/p>/i);
  return m ? m[1] : null;
}

// The <main> element's inner HTML, without the shell around it.
export function mainOf(html) {
  return html.match(/<main\b[^>]*>([\s\S]*?)<\/main>/i)?.[1] ?? '';
}

const escape = (s) => s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
const wordRe = (term) => new RegExp(`(?<![\\w-])${escape(term)}(?:e?s)?(?![\\w-])`, 'i');

// Terms an opener defines or links: <dfn> text, and link text whose target is
// an id on the page or the Glossary.
export function markedTerms(openerHtml, pageHtml) {
  const terms = [...openerHtml.matchAll(/<dfn\b[^>]*>([\s\S]*?)<\/dfn>/gi)].map((m) => visibleText(m[1]));
  for (const m of openerHtml.matchAll(/<a\b[^>]*href="([^"]+)"[^>]*>([\s\S]*?)<\/a>/gi)) {
    const href = m[1];
    const onPage = href.startsWith('#') && new RegExp(`\\sid="${escape(href.slice(1))}"`).test(pageHtml);
    if (onPage || /GLOSSARY\.md/.test(href) || href === '/glossary') terms.push(visibleText(m[2]));
  }
  return terms.map((t) => t.toLowerCase());
}

// Problems with a tour page's opener and content; empty when it passes.
export function pageProblems(html) {
  const problems = [];
  if (!/<h1\b/i.test(html)) problems.push('no <h1>');
  const op = opener(html);
  if (!op) return [...problems, 'no plain-language opener (<p data-opener>)'];
  const text = visibleText(op);
  if (text.split(' ').length < 25) problems.push(`opener is ${text.split(' ').length} words; too short to explain anything`);
  const marked = markedTerms(op, html);
  for (const term of JARGON) {
    if (!wordRe(term).test(text)) continue;
    if (!marked.some((m) => wordRe(term).test(m))) problems.push(`opener uses "${term}" without defining or linking it`);
  }
  const main = visibleText(mainOf(html));
  if (PLACEHOLDER.test(main)) problems.push(`placeholder text: ${main.match(PLACEHOLDER)[0]}`);
  const sections = (mainOf(html).match(/<h2\b/gi) ?? []).length;
  if (sections < 2) problems.push(`${sections} deeper section(s); a tour page goes deeper than its opener`);
  if (main.split(' ').length < 250) problems.push('page body is too short to go deeper than the opener');
  return problems;
}

// Problems with a page's forward/back links for its place in READING_ORDER.
export function orderProblems(html, index, order = READING_ORDER) {
  const problems = [];
  const block = html.match(/<nav\b[^>]*aria-label="Page order"[^>]*>([\s\S]*?)<\/nav>/i)?.[1];
  if (!block) return ['no forward/back links (<nav aria-label="Page order">)'];
  const links = [...block.matchAll(/<a\b[^>]*>/gi)].map((m) => m[0]);
  const find = (rel) => links.find((a) => new RegExp(`\\brel="${rel}"`).test(a));
  const prev = order[index - 1];
  const next = order[index + 1];
  const expect = (rel, href) => {
    const a = find(rel);
    if (!href) { if (a) problems.push(`has a ${rel} link but is at that end of the reading order`); return; }
    if (!a) problems.push(`no ${rel} link (expected ${href})`);
    else if (!new RegExp(`href="${escape(href)}"`).test(a)) problems.push(`${rel} link is ${a}, expected href="${href}"`);
  };
  expect('prev', prev);
  expect('next', next);
  if (!prev && !next) problems.push('a page with neither forward nor back link is a dead end');
  return problems;
}

// A built page outside the reading order must be a child of a page in it:
// its route sits one level under that page's route (/skills/grilling under
// /skills), the parent's content links it and it links back to the parent, so
// no page is an orphan or a dead end. `parents` maps a route to its built
// HTML. Empty when it passes.
export function childProblems(route, html, parents, order = READING_ORDER) {
  const parts = route.split('/').filter(Boolean);
  const parent = `/${parts.slice(0, -1).join('/')}`;
  if (parts.length < 2 || !order.includes(parent)) return [`${route} is outside the reading order and under no page in it (orphan)`];
  const links = (h, target) => new RegExp(`href="${escape(target)}(?:#[^"]*)?"`).test(mainOf(h));
  const problems = [];
  if (!links(parents.get(parent) ?? '', route)) problems.push(`${parent} does not link ${route} (orphan)`);
  if (!links(html, parent)) problems.push(`${route} does not link back to ${parent} (dead end)`);
  return problems;
}

// Every link into this repository on GitHub (blob/dev) and whether its file
// exists in this checkout.
export function repoLinks(html) {
  return [...html.matchAll(/href="(https:\/\/github\.com\/KaydenClark\/Agentic-Management-System\/blob\/dev\/([^"#?]+))[^"]*"/gi)]
    .map((m) => ({ href: m[1], path: decodeURIComponent(m[2]), exists: existsSync(join(repoRoot, decodeURIComponent(m[2]))) }));
}

const decode = (s) => s.replace(/&amp;/g, '&').replace(/&#x27;|&#39;/g, "'").replace(/&quot;/g, '"').replace(/&lt;/g, '<').replace(/&gt;/g, '>');

// Owner quotes: each <blockquote data-owner-quote> must carry a source link to
// a committed record and a dated attribution, and its text must appear
// verbatim in that record. Quote marks elsewhere in the page body would
// present words as quoted without a source.
export function quoteProblems(html) {
  const problems = [];
  const main = mainOf(html);
  const quotes = [...main.matchAll(/<figure\b[^>]*data-owner-quote[^>]*>([\s\S]*?)<\/figure>/gi)];
  for (const [, inner] of quotes) {
    const said = decode(visibleText(inner.match(/<blockquote\b[^>]*>([\s\S]*?)<\/blockquote>/i)?.[1] ?? ''));
    const caption = inner.match(/<figcaption\b[^>]*>([\s\S]*?)<\/figcaption>/i)?.[1] ?? '';
    const link = repoLinks(caption)[0];
    if (!said) { problems.push('owner quote with no <blockquote> text'); continue; }
    if (!link) { problems.push(`quote "${said}" has no source link to a committed record`); continue; }
    if (!link.exists) { problems.push(`quote source ${link.path} does not exist`); continue; }
    if (!/\b20\d\d-\d\d-\d\d\b/.test(visibleText(caption))) problems.push(`quote "${said}" has no dated attribution`);
    const source = readFileSync(join(repoRoot, link.path), 'utf8').replace(/\s+/g, ' ');
    if (!source.includes(said)) problems.push(`quote "${said}" is not verbatim in ${link.path}`);
  }
  const rest = decode(visibleText(main.replace(/<figure\b[^>]*data-owner-quote[^>]*>[\s\S]*?<\/figure>/gi, ' ')));
  const quoted = rest.match(/[“"][^”"]{12,}[”"]/);
  if (quoted) problems.push(`quoted words outside an owner-quote figure: ${quoted[0]}`);
  if (/<q\b/i.test(main.replace(/<figure\b[^>]*data-owner-quote[^>]*>[\s\S]*?<\/figure>/gi, ''))) problems.push('<q> outside an owner-quote figure');
  return problems;
}
