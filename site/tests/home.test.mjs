// TK-001 acceptance: the home page text is present in the server-rendered
// HTML, and the shell (navigation, theme toggle) is on every page.
// Owner feedback 11/01/2026: the reading-order navigation lives in the top
// bar, there is no side navigation, and the reading position ("n of N") sits
// with the back/forward links.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { builtPage, builtPages, visibleText } from './helpers.mjs';
import { READING_ORDER, builtName } from './tour-helpers.mjs';

const READING_NAV = /<nav[^>]*aria-label="Reading order"[\s\S]*?<\/nav>/i;
const HEADER = /<header\b[\s\S]*?<\/header>/i;
const PAGE_ORDER = /<nav[^>]*aria-label="Page order"[\s\S]*?<\/nav>/i;

test('home page heading and plain-language opener are server-rendered', () => {
  const { html } = builtPage('index.html');
  assert.match(visibleText(html.match(/<h1[\s\S]*?<\/h1>/i)?.[0] ?? ''), /Agentic Management System/, 'home <h1> missing');
  const opener = html.match(/<p[^>]*data-opener[^>]*>([\s\S]*?)<\/p>/i);
  assert.ok(opener, 'home page has no opener paragraph (data-opener)');
  assert.ok(visibleText(opener[1]).split(' ').length >= 15, 'opener is too short to explain anything');
  assert.doesNotMatch(visibleText(html), /under construction/i, 'home still shows the scaffold placeholder');
});

test('every page carries the shell: main landmark, reading-order navigation, theme toggle', () => {
  for (const { name, html } of builtPages()) {
    assert.match(html, /<main[\s>]/i, `${name}: no <main>`);
    const nav = html.match(READING_NAV);
    assert.ok(nav, `${name}: no reading-order <nav>`);
    assert.match(nav[0], /<a[^>]*href="\/"/i, `${name}: nav has no link to home`);
    assert.match(html, /<button[^>]*data-theme-toggle/i, `${name}: no theme toggle button`);
  }
});

test('home is marked as the current reading position', () => {
  const nav = builtPage('index.html').html.match(READING_NAV)[0];
  const current = [...nav.matchAll(/<a\b[^>]*>/gi)].map((m) => m[0]).filter((a) => /aria-current="page"/.test(a));
  assert.equal(current.length, 1, 'exactly one nav entry should be current');
  assert.match(current[0], /href="\/"/, 'the current entry is not home');
});

test('the reading-order navigation is in the top bar, in reading order, and there is no side navigation', () => {
  for (const { name, html } of builtPages()) {
    const header = html.match(HEADER)?.[0];
    assert.ok(header, `${name}: no <header>`);
    const nav = header.match(READING_NAV)?.[0];
    assert.ok(nav, `${name}: the reading-order <nav> is not inside the <header>`);
    const hrefs = [...nav.matchAll(/<a\b[^>]*href="([^"]+)"/gi)].map((m) => m[1]);
    assert.deepEqual(hrefs, READING_ORDER, `${name}: header links are not the reading order`);
    assert.equal((html.match(/aria-label="Reading order"/gi) ?? []).length, 1, `${name}: more than one reading-order nav`);
    assert.doesNotMatch(html, /<aside\b/i, `${name}: has an <aside> (side navigation)`);
    assert.doesNotMatch(html, /class="[^"]*\bsidebar\b/i, `${name}: has a sidebar element`);
  }
});

test('each page in the reading order marks itself current and states its position by the back/forward links', () => {
  READING_ORDER.forEach((href, i) => {
    const { html } = builtPage(builtName(href));
    const links = [...html.match(READING_NAV)[0].matchAll(/<a\b[^>]*>/gi)].map((m) => m[0]);
    const current = links.filter((a) => /aria-current="page"/.test(a));
    assert.equal(current.length, 1, `${href}: exactly one header link should be current`);
    assert.match(current[0], new RegExp(`href="${href}"`), `${href}: the current header link is not this page`);
    const order = html.match(PAGE_ORDER)?.[0] ?? '';
    assert.match(visibleText(order), new RegExp(`\\b${i + 1} of ${READING_ORDER.length}\\b`), `${href}: no "${i + 1} of ${READING_ORDER.length}" by the back/forward links`);
  });
});

test('a page outside the reading order marks no header link current', () => {
  const { html } = builtPage('_not-found.html');
  assert.doesNotMatch(html.match(READING_NAV)[0], /aria-current="page"/, 'not-found marks a reading-order page current');
});

test('no third-party scripts, styles or fonts in built pages', () => {
  for (const { name, html } of builtPages()) {
    for (const m of html.matchAll(/<(script|link|img|iframe)\b[^>]*\b(?:src|href)="([^"]+)"/gi)) {
      assert.ok(!/^(https?:)?\/\//i.test(m[2]), `${name}: external ${m[1]} ${m[2]}`);
    }
    assert.doesNotMatch(html, /fonts\.googleapis|fonts\.gstatic|@import\s+url\(\s*["']?https?:/i, `${name}: external font`);
  }
});
