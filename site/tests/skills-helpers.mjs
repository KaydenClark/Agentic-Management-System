// Shared checks for the S-008 skills wiki tests. Each check is a pure
// function over built HTML (or article front matter) so the tests can run it
// on the real build and on planted faults. Run `npm run build` first.
import { readdirSync } from 'node:fs';
import { join } from 'node:path';
import {
  FAQ_RANGE, FIXED_SECTIONS, LEADING_SECTIONS, ORIGINAL_CREDIT, PRIVATE_SKILLS_REPO, SKILLS_PIN, SKILLS_PIN_SHORT,
  TRAILING_SECTIONS, chartSkills, contentDir,
} from '../app/skills/content.mjs';
import { siteDir, visibleText } from './helpers.mjs';
import { mainOf } from './tour-helpers.mjs';

// The Spec's count of chart skills per stage at the pin (S-008 Desired
// Behavior): 39 skills.
export const STAGE_COUNTS = { route: 5, align: 12, prepare: 2, journey: 7, judge: 1, complete: 4, improve: 8 };
// Old chart names and the names the skills repository gave them (owner,
// 2026-11-01).
export const RETIRED_NAMES = { 'grill-me': 'align-concept', 'grill-with-docs': 'align-docs' };

// Problems with the article loader's site routes (content.mjs SITE_ROUTES)
// against the site's reading order: the same routes in the same order, so a
// page added to or removed from nav.ts cannot leave an article link allowed
// to a missing page or refused to a real one.
export function siteRouteProblems(siteRoutes, order) {
  const problems = [];
  for (const r of order) if (!siteRoutes.includes(r)) problems.push(`SITE_ROUTES lacks ${r}`);
  for (const r of siteRoutes) if (!order.includes(r)) problems.push(`SITE_ROUTES has ${r}, which is not in the reading order`);
  if (!problems.length && siteRoutes.join('|') !== order.join('|')) problems.push(`SITE_ROUTES order ${siteRoutes.join(', ')} differs from ${order.join(', ')}`);
  return problems;
}

export const INDEX_PAGE = 'skills.html';
export const articlePage = (name) => `skills/${name}.html`;
const ARTICLE_PAGE = /^skills[\\/]([a-z0-9-]+)\.html$/;
export const articleNameOf = (builtName) => builtName.match(ARTICLE_PAGE)?.[1] ?? null;

// The article names in content/skills/ (file names, without .md).
export function contentNames(dir = contentDir(siteDir)) {
  try {
    return readdirSync(dir).filter((f) => f.endsWith('.md')).map((f) => f.slice(0, -3)).sort();
  } catch {
    return [];
  }
}
export const contentFile = (name, dir = contentDir(siteDir)) => join(dir, `${name}.md`);

const escape = (s) => s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
const text = (html) => visibleText(html).replace(/&lt;/g, '<').replace(/&gt;/g, '>');

export function articleOf(html) {
  const m = html.match(/<article\b[^>]*\bdata-skill="([^"]+)"[^>]*>([\s\S]*?)<\/article>/i);
  return m ? { name: m[1], inner: m[2] } : null;
}

// The article's ## sections: title and inner HTML up to the next ## or the
// end of the article.
export function sectionsOf(inner) {
  const heads = [...inner.matchAll(/<h2\b[^>]*>([\s\S]*?)<\/h2>/gi)];
  return heads.map((m, k) => ({
    title: text(m[1]),
    html: inner.slice(m.index + m[0].length, k + 1 < heads.length ? heads[k + 1].index : undefined),
  }));
}

// Problems with a built article's shape (S-008 Article shape): sections 1-5
// and 7-9 in order, extras only between 5 and 7, FAQs as question headings
// with answers, a list in It's working when, a credit line and the pin.
export function articleShapeProblems(html) {
  const art = articleOf(html);
  if (!art) return ['no <article data-skill>'];
  const problems = [];
  const h1 = art.inner.match(/<h1\b[^>]*>([\s\S]*?)<\/h1>/i);
  if (!h1 || text(h1[1]) !== art.name) problems.push(`title is not the skill name ${art.name}`);
  const sections = sectionsOf(art.inner.replace(/<div\b[^>]*data-credit-block[\s\S]*$/i, ''));
  const titles = sections.map((s) => s.title);
  for (const t of FIXED_SECTIONS) if (!titles.includes(t)) problems.push(`no "${t}" section`);
  const lead = titles.slice(0, LEADING_SECTIONS.length);
  const trail = titles.slice(-TRAILING_SECTIONS.length);
  const middle = titles.slice(LEADING_SECTIONS.length, -TRAILING_SECTIONS.length);
  if (lead.join('|') !== LEADING_SECTIONS.join('|') || trail.join('|') !== TRAILING_SECTIONS.join('|') || middle.some((t) => FIXED_SECTIONS.includes(t))) {
    problems.push(`sections out of order: ${titles.join(', ')}`);
  }

  const faqs = sections.find((s) => s.title === 'FAQs');
  if (faqs) {
    const qs = [...faqs.html.matchAll(/<h3\b[^>]*>([\s\S]*?)<\/h3>/gi)];
    if (!qs.length) problems.push('FAQs has no question headings');
    else if (qs.length < FAQ_RANGE[0] || qs.length > FAQ_RANGE[1]) problems.push(`FAQs has ${qs.length} questions, not ${FAQ_RANGE[0]} to ${FAQ_RANGE[1]}`);
    if (qs.length && text(faqs.html.slice(0, qs[0].index))) problems.push('FAQs has text before its first question');
    qs.forEach((q, k) => {
      const question = text(q[1]);
      if (!question.endsWith('?')) problems.push(`FAQ heading "${question}" is not a question ending in ?`);
      const answer = faqs.html.slice(q.index + q[0].length, k + 1 < qs.length ? qs[k + 1].index : undefined);
      if (!text(answer)) problems.push(`FAQ "${question}" has no answer`);
    });
  }

  const working = sections.find((s) => s.title === "It's working when");
  if (working) {
    const list = working.html.match(/<ul\b[^>]*>([\s\S]*?)<\/ul>/i);
    if (!list || !/<li\b/i.test(list[1])) problems.push("It's working when has no list");
    else if (text(working.html.replace(list[0], ''))) problems.push("It's working when has text outside its list");
  }

  const credit = art.inner.match(/<p\b[^>]*\bdata-credit="(original|adapted)"[^>]*>([\s\S]*?)<\/p>/i);
  if (!credit || !text(credit[2])) problems.push('no credit line');
  if (!/\bdata-pin="[0-9a-f]{40}"/.test(art.inner) || !text(art.inner).includes(`Skills commit ${SKILLS_PIN_SHORT}`)) {
    problems.push(`does not name the skills commit (Skills commit ${SKILLS_PIN_SHORT}, full SHA in data-pin)`);
  }
  return problems;
}

// Problems with the pin a built article names.
export function pinProblems(html) {
  const pins = [...html.matchAll(/\bdata-pin="([^"]*)"/g)].map((m) => m[1]);
  if (pins.length !== 1) return [`names ${pins.length} pins, expected one`];
  if (pins[0] !== SKILLS_PIN) return [`pin ${pins[0]} is not the skills commit ${SKILLS_PIN}`];
  if (!text(articleOf(html)?.inner ?? '').includes(`Skills commit ${SKILLS_PIN_SHORT}`)) return [`does not show Skills commit ${SKILLS_PIN_SHORT}`];
  return [];
}

// Problems with an article's credit front matter (S-008 Credit): an adapted
// skill names its source and license and is never labeled original.
export function creditProblems(data) {
  const problems = [];
  if (data.credit === 'original') {
    if (data.credit_text !== ORIGINAL_CREDIT) problems.push(`original credit_text is not "${ORIGINAL_CREDIT}"`);
    if (data.credit_license) problems.push('original credit carries a credit_license');
  } else if (data.credit === 'adapted') {
    if (!data.credit_license) problems.push('adapted credit has no credit_license');
    if (!data.credit_text || /^\s*original\b/i.test(data.credit_text)) problems.push('adapted skill labeled original (credit_text must name the source)');
  } else {
    problems.push(`credit is ${data.credit ?? 'missing'}, not original or adapted`);
  }
  return problems;
}

// Problems with how a built article shows its credit.
export function creditPageProblems(html, data) {
  const art = articleOf(html);
  const credit = art?.inner.match(/<p\b[^>]*\bdata-credit="([^"]*)"[^>]*>([\s\S]*?)<\/p>/i);
  if (!credit) return ['no credit line'];
  const problems = [];
  if (credit[1] !== data.credit) problems.push(`credit line is ${credit[1]}, front matter says ${data.credit}`);
  if (data.credit === 'original' && text(credit[2]) !== ORIGINAL_CREDIT) problems.push('original credit line is not the original text');
  if (data.credit === 'adapted') {
    if (/^\s*original\b/i.test(text(credit[2]))) problems.push('adapted skill shown as original');
    if (!text(art.inner).includes(`Source license: ${data.credit_license}`)) problems.push(`does not show Source license: ${data.credit_license}`);
  }
  return problems;
}

// Problems with the set of articles against the chart (S-008 Coverage).
export function coverageProblems(names, chart) {
  const problems = [];
  const expected = chartSkills(chart).map((s) => s.name);
  for (const [old, current] of Object.entries(RETIRED_NAMES)) if (names.includes(old)) problems.push(`article named ${old}; the skills repository calls it ${current}`);
  const extra = names.filter((n) => !expected.includes(n) && !(n in RETIRED_NAMES));
  if (extra.length) problems.push(`articles for skills not on the chart: ${extra.join(', ')}`);
  const missing = expected.filter((n) => !names.includes(n));
  if (missing.length) problems.push(`${missing.length} chart skills have no article: ${missing.join(', ')}`);
  for (const stage of chart) {
    if (!stage.main.length && !stage.used.length) problems.push(`stage ${stage.name} names no skill (orphan stage)`);
    else if (![...stage.main, ...stage.used].some((n) => names.includes(n))) problems.push(`stage ${stage.name} has no article`);
  }
  return problems;
}

// Problems with the built index against the chart and the article set (S-008
// Index): every article under its chart stage, stages in chart order, main
// flow first in order, then the others, each linking /skills/<name>.
export function indexProblems(html, names, chart) {
  const problems = [];
  const main = mainOf(html);
  const sections = [...main.matchAll(/<section\b[^>]*\bdata-stage="([^"]+)"[^>]*>([\s\S]*?)<\/section>/gi)];
  const ids = sections.map((m) => m[1]);
  if (ids.join('|') !== chart.map((st) => st.id).join('|')) problems.push(`stages are ${ids.join(', ')}; the chart's are ${chart.map((st) => st.id).join(', ')}`);
  const seen = new Map();
  for (const [open, id, inner] of sections) {
    const stage = chart.find((st) => st.id === id);
    if (!stage) continue;
    if (!new RegExp(`\\bid="${escape(id)}"`).test(open)) problems.push(`stage ${stage.name} has no id="${id}" anchor`);
    const head = inner.match(/<h2\b[^>]*>([\s\S]*?)<\/h2>/i);
    if (!head || text(head[1]) !== stage.name) problems.push(`stage ${id} is not headed ${stage.name}`);
    if (!text(inner).includes(stage.gloss)) problems.push(`stage ${stage.name} does not show its gloss`);
    if (stage.note && !text(inner).includes(stage.note)) problems.push(`stage ${stage.name} does not show its note`);
    const entries = [...inner.matchAll(/<li\b([^>]*\bdata-skill="([^"]+)"[^>]*)>([\s\S]*?)<\/li>/gi)].map((m) => ({
      name: m[2],
      flow: m[1].match(/\bdata-flow="([^"]+)"/)?.[1],
      body: m[3],
    }));
    const expected = [
      ...stage.main.filter((n) => names.includes(n)).map((name) => ({ name, flow: 'main' })),
      ...stage.used.filter((n) => names.includes(n)).map((name) => ({ name, flow: 'used' })),
    ];
    const got = entries.map((e) => `${e.name}:${e.flow}`).join(', ');
    const want = expected.map((e) => `${e.name}:${e.flow}`).join(', ');
    if (got !== want) problems.push(`stage ${stage.name} lists ${got || 'nothing'}; expected ${want || 'nothing'} (main flow first, in order)`);
    for (const e of entries) {
      seen.set(e.name, (seen.get(e.name) ?? 0) + 1);
      if (!new RegExp(`<a\\b[^>]*href="/skills/${escape(e.name)}"`).test(e.body)) problems.push(`index entry ${e.name} does not link /skills/${e.name}`);
      if (!text(e.body.match(/<p\b[^>]*\bdata-summary[^>]*>([\s\S]*?)<\/p>/i)?.[1] ?? '')) problems.push(`index entry ${e.name} has no summary`);
    }
  }
  for (const n of names) if (!seen.has(n)) problems.push(`article ${n} is not listed on the index`);
  for (const [n, count] of seen) if (count > 1) problems.push(`${n} is listed ${count} times`);
  return problems;
}

// Problems with a built article's stage label: it names the chart stage and
// links that stage's anchor on the index.
export function stageLabelProblems(html, chart) {
  const art = articleOf(html);
  if (!art) return ['no <article data-skill>'];
  const stage = chart.find((st) => st.main.includes(art.name) || st.used.includes(art.name));
  if (!stage) return [`${art.name} is not on the chart`];
  const link = art.inner.match(/<a\b[^>]*\bdata-stage-link="([^"]*)"[^>]*>([\s\S]*?)<\/a>/i);
  if (!link) return ['no stage label link'];
  const problems = [];
  if (link[1] !== stage.id || !new RegExp(`href="/skills#${escape(stage.id)}"`).test(link[0])) problems.push(`stage label does not link /skills#${stage.id}`);
  if (!text(link[2]).includes(stage.name)) problems.push(`stage label does not name ${stage.name}`);
  return problems;
}

// Marks saying a skill was used to build this site (S-008 No used marks):
// visible text in that sense, a heading over a list of uses, or a data-used
// badge attribute. Phrases are anchored on the site so an article may still
// say what a skill is used for.
export const USED_MARK_TEXT = [
  /\bused\s+(?:to|in|for|while|when)\s+(?:build|make|creat|develop|writ|design)\w*(?:\W+\w+){0,4}?\W+(?:site|website|wiki|pages?|AMS)\b/i,
  /\bused\s+(?:on|in|for|by)\s+(?:this|the|our)\s+(?:site|website|wiki)\b/i,
  /\b(?:this|the|our)\s+(?:site|website|wiki)\s+(?:was|is|were)\s+(?:built|made|created|developed|written)\s+(?:with|using|by)\b/i,
  /\bbuilt\s+(?:this|the|our)\s+(?:site|website|wiki)\b/i,
];
const USED_HEADING = /<h[1-6]\b[^>]*>\s*(?:used\s+(?:in|on|by|for|to)\b|where\s+(?:it\s+was|it's\s+been|we)\s+used\b|uses\s+on\s+this\s+site)/i;
const USED_ATTR = /\sdata-used(?:-[\w-]+)?(?=[\s=>])/i;

export function usedMarkProblems(html) {
  const problems = [];
  const body = text(mainOf(html));
  for (const re of USED_MARK_TEXT) if (re.test(body)) problems.push(`says a skill was used to build the site (${re})`);
  if (USED_HEADING.test(mainOf(html))) problems.push('heads a list of where a skill was used');
  if (USED_ATTR.test(html)) problems.push('carries a data-used mark');
  return problems;
}

// Problems with a wiki page's links: /skills/<name> must be a built article,
// /skills#<id> an id on the index, any other internal link a built page; the
// private skills repository is never linked.
export function wikiLinkProblems(html, { articles, pages, indexIds }) {
  const problems = [];
  for (const [, href] of html.matchAll(/<a\b[^>]*\bhref="([^"]+)"/gi)) {
    const target = href.replace(/&amp;/g, '&');
    if (PRIVATE_SKILLS_REPO.test(target)) { problems.push(`links the private skills repository: ${target}`); continue; }
    if (!target.startsWith('/')) continue;
    const [path, frag] = target.split('#');
    const skill = path.match(/^\/skills\/([^/]+)$/);
    if (skill) { if (!articles.has(skill[1])) problems.push(`links ${target}, which has no article`); continue; }
    if (path === '/skills' && frag !== undefined && !indexIds.has(frag)) { problems.push(`links ${target}, which is no id on the index`); continue; }
    const name = path === '/' ? 'index.html' : `${path.slice(1)}.html`;
    if (!pages.has(name)) problems.push(`links ${target}, which is no built page`);
  }
  return problems;
}
