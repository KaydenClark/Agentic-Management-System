// S-009 acceptance over the built demo Grill Board (/grill-board-demo).
// Run `npm run build` first. What a browser does on interaction (no request,
// no cookie) is checked by `npm run check:browser`; these tests read the
// prerendered page, its served RSC payload and the board's source.
//
// The page prerenders the list rows and the open card; every card's full
// text and fields travel in the RSC payload the board hydrates from, so the
// card checks read the cards from there and match them to the HTML.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { join } from 'node:path';
import { appOut, builtPage, siteDir, sourceFiles, visibleText } from './helpers.mjs';
import { mainOf } from './tour-helpers.mjs';

const PAGE = 'grill-board-demo.html';
const RSC = join(appOut, 'grill-board-demo.rsc');

// --- Checkers, each a pure function so the self-tests can plant faults. ---

// Engineering subjects a sample may not ask about (DDR-000V, S-009): code,
// pull requests, branches, commits, repositories, deploys and tooling.
// "PR" is matched case-sensitively so ordinary words are not caught.
const ENGINEERING = /\b(?:code[sd]?|coding|pull[- ]requests?|branch(?:es|ed|ing)?|commit(?:s|ted|ting)?|repos?|repositor(?:y|ies)|deploy(?:s|ed|ing|ments?)?|tooling|git|github|merge[sd]?|merging|programming|software|api)\b/i;
const PR = /\bPRs?\b/;
export function engineeringTerms(text) {
  return [text.match(ENGINEERING)?.[0], text.match(PR)?.[0]].filter(Boolean);
}

const GRADE = { p: /^P[1-4]$/, v: /^V[1-4]$/ };
const TEXT_FIELDS = ['short', 'title', 'pWhy', 'vWhy', 'q', 'why', 'rec', 'owner', 'kind', 'changes', 'impact', 'history', 'historyCount', 'flagText'];

// Problems with one card's data; [] when it has the real card's parts.
export function cardProblems(card) {
  const out = [];
  if (!GRADE.p.test(card.p ?? '')) out.push(`${card.id}: Priority grade ${card.p} is not P1-P4`);
  if (!GRADE.v.test(card.v ?? '')) out.push(`${card.id}: Value grade ${card.v} is not V1-V4`);
  for (const k of ['pWhy', 'vWhy']) if (typeof card[k] !== 'string' || card[k].trim().split(/\s+/).length < 4) out.push(`${card.id}: no ${k === 'pWhy' ? 'Priority' : 'Value'} reason`);
  for (const k of ['title', 'q']) if (typeof card[k] !== 'string' || !card[k].trim()) out.push(`${card.id}: no ${k}`);
  const texts = [
    ...TEXT_FIELDS.map((k) => card[k]).filter((v) => typeof v === 'string'),
    ...(card.options ?? []).flatMap((o) => [o.label, o.hint]),
    ...(card.concerns ?? []).flatMap((c) => [c.name, c.note]),
    ...(card.wiki ?? []),
  ];
  for (const t of texts) for (const term of engineeringTerms(t)) out.push(`${card.id}: asks about engineering ("${term}" in "${t.slice(0, 60)}")`);
  return out;
}

// Problems with the open card's prerendered markup for `card`.
export function openCardProblems(html, card) {
  const out = [];
  if (!/\bSample\b/.test(visibleText(html))) out.push('open card is not labeled Sample');
  for (const [grade, label, why] of [[card.p, 'Priority', card.pWhy], [card.v, 'Value', card.vWhy]]) {
    const re = new RegExp(`<span class="grade n[1-4]">${grade}</span><span>${label} · why this grade</span>`);
    if (!re.test(html)) out.push(`open card shows no ${label} grade ${grade} in ink`);
    const reason = visibleText(why ?? '');
    if (!reason || !visibleText(html).includes(reason)) out.push(`open card shows no ${label} reason`);
  }
  const rating = html.match(/<span[^>]*role="group"[^>]*aria-label="Rate this question, one to five"[^>]*>([\s\S]*?)<\/span>/);
  const stars = rating ? [...rating[1].matchAll(/<button[^>]*aria-label="([1-5]) of 5"/g)].map((m) => m[1]) : [];
  if (stars.join('') !== '12345') out.push(`open card rating is not 1-5 (${stars.join(',') || 'none'})`);
  if (!/<button[^>]*class="taxing"[^>]*aria-pressed="(?:true|false)"[^>]*>Too taxing<\/button>/.test(html)) out.push('open card has no "Too taxing" flag');
  return out;
}

// The cards and topics the board hydrates from, read from the served payload.
function jsonArrayAfter(text, key) {
  const start = text.indexOf(`"${key}":[`);
  if (start < 0) return null;
  let i = text.indexOf('[', start);
  const from = i;
  let depth = 0;
  let inString = false;
  for (; i < text.length; i += 1) {
    const ch = text[i];
    if (inString) { if (ch === '\\') i += 1; else if (ch === '"') inString = false; continue; }
    if (ch === '"') inString = true;
    else if (ch === '[' || ch === '{') depth += 1;
    else if (ch === ']' || ch === '}') { depth -= 1; if (depth === 0) return JSON.parse(text.slice(from, i + 1)); }
  }
  return null;
}
const payload = () => readFileSync(RSC, 'utf8');
const cards = () => jsonArrayAfter(payload(), 'cards') ?? [];
const topics = () => jsonArrayAfter(payload(), 'topics') ?? [];
const html = () => builtPage(PAGE).html;
const boardOf = (page) => {
  const start = page.indexOf('<div class="gb-root">');
  assert.ok(start >= 0, 'no board (.gb-root) in the page');
  return page.slice(start, page.indexOf('</main>', start));
};
const rows = (page) => [...page.matchAll(/<button[^>]*data-card-row="([^"]+)"[^>]*>([\s\S]*?)<\/button>/g)].map((m) => ({ id: m[1], text: visibleText(m[2]) }));
const openCard = (page) => {
  const start = page.indexOf('data-open-card=');
  assert.ok(start > 0, 'the open card is prerendered');
  return { id: page.slice(start).match(/data-open-card="([^"]+)"/)[1], html: page.slice(start, page.indexOf('</article>', start)) };
};

// --- Self-tests: each checker fails on a planted fault. ---

const GOOD = {
  id: 'X', p: 'P2', v: 'V1', title: 'Pick a venue', q: 'Which hall should host the party?',
  pWhy: 'The hall holds the date only until Friday.', vWhy: 'The venue decides travel, food and cost.',
  options: [{ label: 'Lakeside hall', hint: 'Fits everyone.' }], concerns: [{ name: 'Party plan', note: 'Venue section' }], wiki: ['Guest list'],
};

test('the checkers catch faults (self-test)', () => {
  assert.deepEqual(cardProblems(GOOD), []);
  assert.ok(cardProblems({ ...GOOD, vWhy: '' }).some((p) => /no Value reason/.test(p)), 'a card missing a reason passes');
  assert.ok(cardProblems({ ...GOOD, pWhy: undefined }).some((p) => /no Priority reason/.test(p)), 'a card missing a reason passes');
  assert.ok(cardProblems({ ...GOOD, p: 'High' }).length, 'a card with no Priority grade passes');
  for (const q of ['Should we merge this pull request?', 'Which branch ships first?', 'Is the PR ready?', 'Who reviews the commit?', 'Where does the repo live?', 'When do we deploy?', 'Which tooling do we pick?', 'Is the code ready?']) {
    assert.ok(cardProblems({ ...GOOD, q }).some((p) => /engineering/.test(p)), `engineering question passes: ${q}`);
  }
  assert.ok(cardProblems({ ...GOOD, options: [{ label: 'Rebase the branch', hint: '' }] }).length, 'engineering option passes');
  assert.deepEqual(engineeringTerms('Spend $600 on garden tools and print the lunch order.'), []);

  const card = (rate = [1, 2, 3, 4, 5], taxing = true, why = GOOD.vWhy) => `<article data-open-card="X"><span class="sample">Sample</span>`
    + `<summary><span class="grade n2">P2</span><span>Priority · why this grade</span></summary><p>${GOOD.pWhy}</p>`
    + `<summary><span class="grade n1">V1</span><span>Value · why this grade</span></summary><p>${why}</p>`
    + `<span role="group" aria-label="Rate this question, one to five" class="gb-stars">${rate.map((k) => `<button type="button" class="star" aria-pressed="false" aria-label="${k} of 5">★</button>`).join('')}</span>`
    + (taxing ? '<button type="button" class="taxing" aria-pressed="false">Too taxing</button>' : '');
  assert.deepEqual(openCardProblems(card(), GOOD), []);
  assert.ok(openCardProblems(card([1, 2, 3]), GOOD).some((p) => /rating/.test(p)), 'a 1-3 rating passes');
  assert.ok(openCardProblems(card(undefined, false), GOOD).some((p) => /Too taxing/.test(p)), 'a card with no flag passes');
  assert.ok(openCardProblems(card(undefined, true, ''), GOOD).some((p) => /Value reason/.test(p)), 'an open card missing a reason passes');
  assert.ok(openCardProblems(card().replace('Sample', 'Item'), GOOD).some((p) => /Sample/.test(p)), 'an unlabeled card passes');
});

// --- The built page. ---

test('the payload carries every sample card and topic', () => {
  const list = cards();
  assert.ok(list.length >= 6, `only ${list.length} cards in the payload`);
  assert.ok(topics().length >= 2, 'fewer than two topics');
  assert.equal(new Set(list.map((c) => c.id)).size, list.length, 'card ids repeat');
  for (const c of list) assert.match(c.id, /^GB-S\d+$/, `${c.id}: a sample id (GB-S…) so it cannot pass for a real card`);
});

test('every card is labeled as a sample', () => {
  const page = html();
  const list = rows(page);
  assert.deepEqual(list.map((r) => r.id).sort(), cards().map((c) => c.id).sort(), 'every card has a row in the page');
  for (const r of list) assert.match(r.text, /\bSample\b/, `row ${r.id} is not labeled Sample`);
  assert.match(visibleText(openCard(page).html), /\bSample\b/, 'the open card is not labeled Sample');
  assert.match(visibleText(boardOf(page)), /A demo board with sample questions/, 'the board does not say it is a demo');
});

test('no sample asks about code, pull requests, branches, commits, repos, deploys or tooling', () => {
  for (const c of cards()) assert.deepEqual(cardProblems(c).filter((p) => /engineering/.test(p)), [], c.id);
  for (const t of topics()) assert.deepEqual([t.label, t.frame, t.goal].flatMap(engineeringTerms), [], t.key);
  const page = html();
  assert.deepEqual(engineeringTerms(visibleText(boardOf(page))), [], 'board text');
  assert.deepEqual(engineeringTerms(visibleText(page.match(/<header class="gb-intro">[\s\S]*?<\/header>/)?.[0] ?? '')), [], 'page intro');
});

test('each card has Priority and Value with a reason for each', () => {
  for (const c of cards()) assert.deepEqual(cardProblems(c), [], c.id);
});

test('the open card shows Priority, Value, both reasons, a 1-5 rating and a too-taxing flag', () => {
  const page = html();
  const open = openCard(page);
  const card = cards().find((c) => c.id === open.id);
  assert.ok(card, `open card ${open.id} is not in the payload`);
  assert.deepEqual(openCardProblems(open.html, card), []);
});

test('grades are ink, never a signal hue (S-004 card shape, DDR-000Y)', () => {
  const board = boardOf(html());
  const grades = [...board.matchAll(/<span class="([^"]*\bgrade\b[^"]*)">([PV][1-4])<\/span>/g)];
  assert.ok(grades.length >= rows(html()).length * 2, 'rows do not all show both grades');
  for (const [, cls, g] of grades) {
    assert.match(cls, new RegExp(`^grade n${g[1]}$`), `${g}: grade class "${cls}" is not ink weight n${g[1]}`);
  }
});

test('the page explains where a confirmed answer goes', () => {
  const page = html();
  const where = page.match(/<section[^>]*id="where-answers-go"[^>]*>([\s\S]*?)<\/section>/)?.[1];
  assert.ok(where, 'no #where-answers-go section');
  assert.match(where, /<h2[^>]*>Where a confirmed answer goes<\/h2>/);
  const text = visibleText(where);
  assert.match(text, /written straight into the record that owns the question/, 'does not say the answer lands in its owning record');
  assert.match(text, /nothing is sent, saved or shared/, 'does not say the demo keeps nothing');
  assert.match(text, /too taxing/i, 'does not explain the flag');
  assert.match(text, /Each color means one thing/, 'does not state the color meanings (DDR-000M)');
  assert.match(mainOf(page), /<p data-opener="">[\s\S]*?href="#where-answers-go"/, 'the intro does not link the explanation');
});

test('the board loads nothing from elsewhere and has no form that submits', () => {
  const board = boardOf(html());
  assert.doesNotMatch(board, /\s(?:src|href|action|formaction|srcset|poster)="(?:[a-z][a-z0-9+.-]*:)?\/\//i, 'the board references another origin');
  assert.doesNotMatch(board, /<form\b/i, 'the board has a form');
  const css = sourceFiles('app/grill-board-demo', ['.css']).map((f) => f.text).join('\n');
  assert.doesNotMatch(css, /url\(|@import/i, 'board CSS loads a resource');
});

test('the board source has no way to send or store anything', () => {
  const SENDS = /\b(?:fetch|XMLHttpRequest|sendBeacon|WebSocket|EventSource|localStorage|sessionStorage|indexedDB|document\.cookie|cookieStore|navigator\.serviceWorker|import\()\b/;
  const files = sourceFiles('app/grill-board-demo', ['.ts', '.tsx']);
  assert.ok(files.length >= 3, 'board source not found');
  for (const f of files) {
    const code = f.text.replace(/\/\/.*$/gm, '').replace(/\/\*[\s\S]*?\*\//g, '');
    assert.doesNotMatch(code, SENDS, f.name);
  }
  assert.ok(readFileSync(join(siteDir, 'app', 'grill-board-demo', 'Board.tsx'), 'utf8').startsWith('"use client"'), 'Board is not a client component');
});
