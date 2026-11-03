// Shared checks for the S-003 tour tests (TK-002, TK-003). Each check is a pure
// function over built HTML so the tests can run it on the real build and on
// planted faults. Run `npm run build` first.
import { existsSync, readFileSync } from 'node:fs';
import { execFileSync } from 'node:child_process';
import { join } from 'node:path';
import { siteDir, visibleText } from './helpers.mjs';

export const repoRoot = join(siteDir, '..');
export const REPO_BLOB = 'https://github.com/KaydenClark/Agentic-Management-System/blob/dev/';

// The reading order the tour must follow, in order (owner of the list:
// app/nav.ts; this is the expectation it is tested against).
// One entry per line, so adding or dropping a page touches only its own line.
export const READING_ORDER = [
  '/',
  '/start',
  '/why',
  '/how-it-works',
  '/skills',
  '/rsi',
  '/glossary',
];

// Every tour page the Spec names (S-003 Desired Behavior, Tour pages).
export const TOUR = [
  { href: '/start', title: 'About' },
  { href: '/why', title: 'Why' },
  { href: '/how-it-works', title: 'How it works' },
  { href: '/glossary', title: 'Glossary' },
  { href: '/about', title: 'About' },
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
  // /about is retained as a canonical alias, not a second reading-order page.
  // Require equivalent content and the same About position to avoid allowing
  // arbitrary top-level orphan pages through this exception.
  if (route === '/about') {
    const target = parents.get('/start');
    const problems = [];
    if (!target || visibleText(mainOf(html)) !== visibleText(mainOf(target))) problems.push('About alias differs from /start');
    const headerNav = html.match(/<nav[^>]*aria-label="Reading order"[\s\S]*?<\/nav>/)?.[0] ?? '';
    if (!/href="\/start"[^>]*aria-current="page"[^>]*>About<\/a>/.test(headerNav)) problems.push('About alias lacks its shared navigation position');
    return problems;
  }
  const parts = route.split('/').filter(Boolean);
  const parent = `/${parts.slice(0, -1).join('/')}`;
  if (parts.length < 2 || !order.includes(parent)) return [`${route} is outside the reading order and under no page in it (orphan)`];
  const links = (h, target) => new RegExp(`href="${escape(target)}(?:#[^"]*)?"`).test(mainOf(h));
  const problems = [];
  if (!links(parents.get(parent) ?? '', route)) problems.push(`${parent} does not link ${route} (orphan)`);
  if (!links(html, parent)) problems.push(`${route} does not link back to ${parent} (dead end)`);
  return problems;
}

// Moving dev links resolve in the checkout; immutable evidence links resolve
// against their actual Git revision, even after records move or retire.
export function repoLinks(html) {
  return [...html.matchAll(/href="(https:\/\/github\.com\/KaydenClark\/Agentic-Management-System\/blob\/(dev|[a-f0-9]{40})\/([^"#?]+))[^"]*"/gi)]
    .map((m) => {
      const path = decodeURIComponent(m[3]);
      let exists = false;
      if (m[2] === 'dev') exists = existsSync(join(repoRoot, path));
      else {
        try {
          execFileSync('git', ['cat-file', '-e', `${m[2]}:${path}`], { cwd: repoRoot, stdio: 'ignore' });
          exists = true;
        } catch { /* A missing revision or path remains a broken source link. */ }
      }
      return { href: m[1], path, exists };
    });
}

const decode = (s) => s.replace(/&amp;/g, '&').replace(/&#x27;|&#39;/g, "'").replace(/&quot;/g, '"').replace(/&lt;/g, '<').replace(/&gt;/g, '>');

// The site quotes no one: a tour page holds no owner-quote figure, no
// <blockquote>, no <q> and no words in quote marks. A point from the owner is
// paraphrased in plain prose and links the committed record it comes from.
export function quoteProblems(html) {
  const problems = [];
  const main = mainOf(html);
  if (/\sdata-owner-quote\b/i.test(main)) problems.push('an owner-quote figure (data-owner-quote); the site quotes no one');
  if (/<blockquote\b/i.test(main)) problems.push('a <blockquote>; paraphrase instead of quoting');
  if (/<q\b/i.test(main)) problems.push('a <q>; paraphrase instead of quoting');
  const quoted = decode(visibleText(main)).match(/[“"][^”"]{12,}[”"]/);
  if (quoted) problems.push(`quoted words: ${quoted[0]}`);
  return problems;
}

// Any built page (tour or not) carrying the owner-quote feature.
export function ownerQuoteProblems(pages) {
  return pages.filter(({ html }) => /\sdata-owner-quote\b/i.test(html)).map(({ name }) => `${name}: has data-owner-quote; the site quotes no one`);
}
