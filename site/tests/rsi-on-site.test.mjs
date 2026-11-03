import './tsx-register.mjs';
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { createElement } from 'react';
import { renderToStaticMarkup } from 'react-dom/server';
const { RepairEvidence } = await import('../app/rsi/repair.tsx');
const { RsiView } = await import('../app/rsi/view.tsx');
const { seriesViews } = await import('../app/rsi/data.ts');
const { linkCoverageCase } = await import('../app/rsi/fixtures/cases.ts');
const { Footer } = await import('../app/shell/Footer.tsx');

test('RSI presents a paired chart and its real underlying comparison on-site', () => {
  const html = renderToStaticMarkup(createElement(RepairEvidence));
  assert.match(html, /data-evidence-chart="workflow"/);
  assert.match(html, /id="workflow-comparison-data"/);
  assert.ok(html.indexOf('data-evidence-chart="workflow"') < html.indexOf('data-checker-repair'), 'chart must precede the long evidence accounts');
  for (const [run, baseline, candidate] of [[1, 9, 9], [2, 10, 8], [3, 10, 7]]) {
    assert.match(html, new RegExp(`data-comparison-run="${run}"[\\s\\S]*?Baseline[\\s\\S]*?${baseline} of 11[\\s\\S]*?Candidate[\\s\\S]*?${candidate} of 11`));
  }
  assert.match(html, /not an Alignment Score/);
  assert.match(html, /No demonstrated improvement/);
});

test('all RSI evidence links remain on-site and fragment links resolve', () => {
  const data = structuredClone(linkCoverageCase);
  for (const row of [...data.runs, ...data.results]) row.source_url = 'https://github.com/example/repository/commit/example';
  const html = renderToStaticMarkup(createElement(RsiView, { views: seriesViews(data), unavailable: false }, createElement(RepairEvidence))) + renderToStaticMarkup(createElement(Footer));
  const ids = [...html.matchAll(/\sid="([^"]+)"/g)].map(m => m[1]);
  assert.equal(new Set(ids).size, ids.length, 'evidence destinations must be unique');
  for (const [, href] of html.matchAll(/href="([^"]+)"/g)) {
    assert.ok(href.startsWith('#') || href.startsWith('/'), `outbound evidence link: ${href}`);
    if (href.startsWith('#')) assert.ok(ids.includes(href.slice(1)), `missing on-site evidence: ${href}`);
  }
  assert.match(html, /Source:/);
  assert.match(html, /Strength:/);
});
