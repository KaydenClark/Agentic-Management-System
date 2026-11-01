// TK-001 acceptance: the home page text is present in the server-rendered
// HTML, and the shell (navigation, theme toggle) is on every page.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { builtPage, builtPages, visibleText } from './helpers.mjs';

const READING_NAV = /<nav[^>]*aria-label="Reading order"[\s\S]*?<\/nav>/i;

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
  assert.match(visibleText(nav), /\b1 of \d+\b/, 'nav does not state the reading position');
});

test('no third-party scripts, styles or fonts in built pages', () => {
  for (const { name, html } of builtPages()) {
    for (const m of html.matchAll(/<(script|link|img|iframe)\b[^>]*\b(?:src|href)="([^"]+)"/gi)) {
      assert.ok(!/^(https?:)?\/\//i.test(m[2]), `${name}: external ${m[1]} ${m[2]}`);
    }
    assert.doesNotMatch(html, /fonts\.googleapis|fonts\.gstatic|@import\s+url\(\s*["']?https?:/i, `${name}: external font`);
  }
});
