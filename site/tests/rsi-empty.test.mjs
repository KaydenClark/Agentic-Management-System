// S-007 TK-001: the /rsi page with zero rows shows every planned series place
// and the honest "no trials yet" state (DDR-000T: places exist from the start,
// nothing is fabricated). Reads the prerendered HTML from `npm run build`, so a
// pass also proves the content is server-rendered.
//
// RSI_HTML may point at another HTML file; the planted-fault runs in the PR use
// it to show each check fails on a page with that fault.
import './tsx-register.mjs';
import { test } from 'node:test';
import { createElement } from 'react';
import { renderToStaticMarkup } from 'react-dom/server';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { CHECKS, readPage } from './rsi-html.mjs';
const { RsiView } = await import('../app/rsi/view.tsx');
const { emptyData, seriesViews } = await import('../app/rsi/data.ts');

const siteDir = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const htmlPath = process.env.RSI_HTML ?? path.join(siteDir, '.next/server/app/rsi.html');
const cssPath = path.join(siteDir, 'app/rsi/rsi.module.css');

function loadHtml() {
  // Successful-empty behavior uses an explicit successful read. A missing build
  // environment is unavailable and must never be asserted to contain no rows.
  return renderToStaticMarkup(createElement(RsiView, { views: seriesViews(emptyData), unavailable: false }));
}

test('the server-rendered page distinguishes an unavailable read from a successful empty read', () => {
  assert.ok(fs.existsSync(htmlPath), `prerendered /rsi page missing at ${htmlPath}; run npm run build`);
  const html = fs.readFileSync(htmlPath, 'utf8').replace(/<(script|style)\b[^>]*>[\s\S]*?<\/\1>/gi, '');
  assert.ok(html.includes('data-rsi-page'));
  assert.equal((html.match(/data-chart-place=/g) ?? []).length, 4);
  if (html.includes('data-load-note')) {
    assert.ok(!html.includes('data-empty-message'), 'failed read was presented as empty');
    assert.equal((html.match(/data-unavailable-message/g) ?? []).length, 4);
  } else {
    assert.ok(html.includes('data-empty-message') || html.includes('data-point='));
  }
});

for (const [name, check] of Object.entries(CHECKS)) test(name, () => check(readPage(loadHtml())));

test('the /rsi stylesheet hides nothing', () => {
  assert.ok(fs.existsSync(cssPath), `missing ${cssPath}`);
  const css = fs.readFileSync(cssPath, 'utf8').replace(/\s+/g, '').toLowerCase();
  assert.doesNotMatch(css, /display:none|visibility:hidden|opacity:0(?![.\d])/, 'the /rsi stylesheet hides content');
});

// Must-fail proof (S-007 TK-001 acceptance): each fault, planted once in a copy
// of the built page, makes the named check fail. A fault that no longer
// applies to the markup fails here too, so the proof cannot go stale silently.
const [C_PLACES, C_SPLITS, C_EXPLAIN, C_DIGITS, C_SAMPLE, C_HIDDEN] = Object.keys(CHECKS);
const FAULTS = [
  ['a dropped series place', C_PLACES, (h) => h.replace(/<figure[^>]*data-chart-place="dev-per-version"[\s\S]*?<\/figure>/, '')],
  ['held-out and dev merged into one section', C_SPLITS, (h) => h.replace('data-split="dev"', 'data-split="held-out"')],
  ['a missing empty-state message', C_EXPLAIN, (h) => h.replace('data-empty-message="">No trials are recorded yet.', 'data-empty-message="">Coming soon.')],
  ['a missing explanation', C_EXPLAIN, (h) => h.replace(/<dl[^>]*data-explanation=""[\s\S]*?<\/dl>/, '')],
  ['a missing next expected event', C_EXPLAIN, (h) => h.replace(/<p[^>]*data-next-event=""[\s\S]*?<\/p>/, '')],
  ['a digit inside a chart place', C_DIGITS, (h) => h.replace('No trials are recorded yet.', 'No trials are recorded yet. 0%')],
  ['a placeholder number in the page intro', C_DIGITS, (h) => h.replace('<h1>RSI results</h1>', '<h1>RSI results: 42</h1>')],
  ['a sample chart drawn in a plot area', C_SAMPLE, (h) => h.replace(/(data-plot=""[^>]*>)<\/div>/, '$1<svg><path d="M0 0L1 1"></path></svg></div>')],
  ['a hidden series place', C_HIDDEN, (h) => h.replace('data-chart-place="held-out-per-task"', 'data-chart-place="held-out-per-task" hidden=""')],
  ['a split section hidden by style', C_HIDDEN, (h) => h.replace('data-split="dev"', 'data-split="dev" style="display:none"')],
  ['an aria-hidden plot area', C_HIDDEN, (h) => h.replace('data-plot=""', 'data-plot="" aria-hidden="true"')]
];

test('each planted fault makes its check fail', async (t) => {
  const html = loadHtml();
  for (const [fault, checkName, plant] of FAULTS) {
    await t.test(`${fault} fails "${checkName}"`, () => {
      const planted = plant(html);
      assert.notEqual(planted, html, `the fault "${fault}" no longer applies to the page markup`);
      assert.throws(() => CHECKS[checkName](readPage(planted)), assert.AssertionError);
    });
  }
});
