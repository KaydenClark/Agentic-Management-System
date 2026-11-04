import './tsx-register.mjs';
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { createElement } from 'react';
import { renderToStaticMarkup } from 'react-dom/server';
import { contentHash } from '../scripts/page-hash.mjs';
const data = await import('../app/rsi/data.ts');
const { RsiView } = await import('../app/rsi/view.tsx');
const { run, results, V1, V2 } = await import('../app/rsi/fixtures/cases.ts');

const render = (rows, readAt = '2026-11-01T10:00:00Z') => renderToStaticMarkup(createElement(RsiView, {
  views: data.seriesViews(rows), unavailable: false, readAt,
  runEvidence: data.runsWithoutResults?.(rows),
}));
const hash = (html) => contentHash(`<main id="main">${html}</main>`);

test('RSI review identity ignores read time but changes with trial evidence and availability', () => {
  const r = run({ id: 1, version: V1, started: '2026-11-01T10:00:00Z' });
  const rows = { runs: [r], results: results(r, 'fixture-task', 'dev', [true]) };
  const first = render(rows);
  const refreshed = render(rows, '2026-11-02T12:00:00Z');
  assert.notEqual(first, refreshed, 'freshness must remain visible');
  assert.equal(hash(first), hash(refreshed), 'freshness alone cannot invalidate review');
  const changed = structuredClone(rows);
  changed.results[0].passed = false;
  assert.notEqual(hash(first), hash(render(changed)), 'real results must remain review-bound');
  const unavailable = renderToStaticMarkup(createElement(RsiView, { views: data.seriesViews(data.emptyData), unavailable: true }));
  assert.notEqual(hash(render(data.emptyData)), hash(unavailable));
});

for (const version of [V1, V2]) test(`graders stay separate with ${version === V1 ? 'identical' : 'changed'} system commits`, () => {
  const a = run({ id: 1, version: V1, started: '2026-11-01T10:00:00Z' });
  const b = { ...run({ id: 2, version, started: '2026-11-02T10:00:00Z' }), grader_version: 'e'.repeat(40) };
  const rows = { runs: [a, b], results: [...results(a, 'fixture-task', 'dev', [true]), ...results(b, 'fixture-task', 'dev', [false])] };
  for (const view of data.seriesViews(rows).filter((v) => v.split === 'dev')) {
    assert.equal(view.series.length, 2);
    assert.deepEqual(new Set(view.series.map((s) => s.graderVersion)), new Set([a.grader_version, b.grader_version]));
    assert.ok(view.series.every((s) => s.points.length === 1 && s.points[0].counts[0].of === 1));
    assert.ok(view.series.every((s) => s.points.every((p) => !p.marks.some((m) => m.kind === 'regression'))));
  }
  const html = render(rows);
  assert.match(html, new RegExp(`data-grader="${b.grader_version}"`));
  assert.match(html, new RegExp(`Grader <code[^>]*>${b.grader_version}</code>`));
});

test('run-only stops and failures keep provenance and marks without inventing trial points', () => {
  const stopped = run({ id: 11, version: V1, state: 'stopped', started: '2026-11-01T10:00:00Z', detail: { stop_rule: 'owner_stop', stop_note: 'fixture safe stop' } });
  const failed = run({ id: 12, version: V2, state: 'failed', started: '2026-11-02T10:00:00Z' });
  const hidden = { ...failed, id: 13, is_test: true, source_ref: 'fixture-secret-test' };
  const rows = { runs: [failed, hidden, stopped], results: [] };
  assert.equal(typeof data.runsWithoutResults, 'function');
  assert.deepEqual(data.runsWithoutResults(rows).map((e) => e.run.id), [11, 12]);
  const html = render(rows);
  for (const value of ['data-run-id="11"', 'data-run-id="12"', 'fixture safe stop', 'the owner stopped the loop', failed.source_ref, failed.model, failed.grader_version, 'Failed run', 'No trial result rows']) assert.ok(html.includes(value), value);
  assert.doesNotMatch(html, /fixture-secret-test|data-point=|data-number=|data-row-id=/);
  const mixed = { ...rows, results: results(failed, 'fixture-task', 'dev', [false]) };
  assert.deepEqual(data.runsWithoutResults(mixed).map((e) => e.run.id), [11], 'result-backed failure belongs to its point only');
  assert.notEqual(hash(html), hash(render({ runs: [stopped], results: [] })), 'run failure is review-bound');
});
