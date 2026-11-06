// Browser check of the actual CSS cascade, without network or a server.
// PLAYWRIGHT_MODULE may name an existing host installation of Playwright.
import fs from 'node:fs/promises';
import assert from 'node:assert/strict';
import './tsx-register.mjs';
import { createElement } from 'react';
import { renderToStaticMarkup } from 'react-dom/server';
const { RsiView } = await import('../app/rsi/view.tsx');
const { seriesViews, runsWithoutResults } = await import('../app/rsi/data.ts');
const { run, V1 } = await import('../app/rsi/fixtures/cases.ts');
const { chromium } = await import(process.env.PLAYWRIGHT_MODULE || 'playwright');
const css = await fs.readFile(new URL('../app/rsi/rsi.module.css', import.meta.url), 'utf8');
const tokens = await fs.readFile(new URL('../app/theme/tokens.css', import.meta.url), 'utf8');
const shell = await fs.readFile(new URL('../app/globals.css', import.meta.url), 'utf8');
const browser = await chromium.launch({ headless: true, ...(process.env.BROWSER_CHANNEL ? { channel: process.env.BROWSER_CHANNEL } : {}) });
try {
  const page = await browser.newPage();
  await page.route('**/*', (route) => route.abort());
  const contrast = (a, b) => {
    const luminance = (rgb) => rgb.match(/[\d.]+/g).slice(0, 3).map(Number).map((v) => v / 255).map((v) => v <= .04045 ? v / 12.92 : ((v + .055) / 1.055) ** 2.4).reduce((n, v, i) => n + v * [.2126, .7152, .0722][i], 0);
    const values = [luminance(a), luminance(b)].sort((x, y) => y - x);
    return (values[0] + .05) / (values[1] + .05);
  };
  for (const theme of ['light', 'dark', 'system-dark']) {
    await page.emulateMedia({ colorScheme: theme === 'system-dark' ? 'dark' : 'light' });
    const html = `<html${theme === 'system-dark' ? '' : ` data-theme="${theme}"`}><style>${tokens}\n${css}</style><body><span class="armBar" id="baseline"></span><span class="armBar candidateBar" id="candidate"></span><span class="comparisonBar candidateBar" id="comparison"></span></body></html>`;
    await page.setContent(html);
    const read = () => page.evaluate(() => Object.fromEntries(['baseline', 'candidate', 'comparison'].map((id) => {
      const s = getComputedStyle(document.getElementById(id));
      return [id, { fill: s.backgroundColor, border: s.borderTopColor, style: s.borderTopStyle }];
    })));
    const check = (values) => {
      for (const id of ['candidate', 'comparison']) {
        assert.notEqual(values[id].fill, values.baseline.fill, `${theme}: distinct ${id} fill`);
        assert.equal(values[id].style, 'double');
        assert.ok(contrast(values[id].fill, values[id].border) >= 3, `${theme}: ${id} border/interior contrast`);
      }
    };
    const values = await read();
    check(values);
    await page.addStyleTag({ content: '.candidateBar { background: var(--ink) !important; }' });
    const broken = await read();
    assert.throws(() => check(broken), 'planted solid candidate must fail');
    console.log(theme, values);
  }
  const rows = { runs: [run({ id: 11, version: V1, state: 'stopped', started: '2026-11-01T10:00:00Z', detail: { stop_rule: 'owner_stop', stop_note: 'Fixture stop note' } }), run({ id: 12, version: V1, state: 'failed', started: '2026-11-02T10:00:00Z' })], results: [] };
  const body = renderToStaticMarkup(createElement(RsiView, { views: seriesViews(rows), runEvidence: runsWithoutResults(rows), unavailable: false }));
  for (const width of [375, 1280]) for (const theme of ['light', 'dark']) {
    await page.setViewportSize({ width, height: 900 });
    await page.setContent(`<html data-theme="${theme}"><style>${tokens}\n${shell}\n${css}\nbody { margin: 16px; }</style><body><main>${body}</main></body></html>`);
    assert.equal(await page.locator('[data-run-id]').count(), 2);
    assert.equal(await page.locator('[data-point], [data-number]').count(), 0);
    assert.ok(await page.locator('[data-run-evidence]').isVisible());
    assert.ok(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth), `${theme}/${width}: no overflow`);
    if (process.env.SHOTS_DIR) await page.screenshot({ path: `${process.env.SHOTS_DIR}/run-only-${theme}-${width}.png`, fullPage: true });
    console.log(`run-only ${theme}/${width}: visible, no fabricated points, no overflow`);
  }
} finally { await browser.close(); }
