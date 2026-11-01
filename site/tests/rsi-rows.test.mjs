// S-007 TK-002: /rsi renders Supabase result rows per task and per version.
// Each case renders the page's own view component on a labeled fixture
// (app/rsi/fixtures/cases.ts) with React's server renderer, so these tests
// see the same HTML the server sends. The markup contract they read:
//   [data-chart-place]           one per planned series (TK-001)
//   [data-series]                one line; data-provider/-model/-effort/-arm
//   [data-provenance]            the series' provider, model and effort
//   [data-point][data-version]   one system version on that line
//   a[data-number]               a rendered number; href="#<rows id>" and
//                                data-row-ids naming exactly those rows
//   [data-rows][id] > [data-row] the rows behind a number, each with a
//                                [data-strength] label
//   [data-mark]                  regression | variant | removed | stop-rule
//   [data-label]                 an identifier (model, commit, task), not a number
//   [data-load-note]             the "could not be loaded" note
import './tsx-register.mjs';
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { createElement } from 'react';
import { renderToStaticMarkup } from 'react-dom/server';
import { CHECKS, decode, parseAttrs, readPage } from './rsi-html.mjs';

const cases = await import('../app/rsi/fixtures/cases.ts');
const { seriesViews } = await import('../app/rsi/data.ts');
const { RsiView } = await import('../app/rsi/view.tsx');
const { loadRsiData } = await import('../app/rsi/supabase.ts');

const render = (data, unavailable = false) => renderToStaticMarkup(createElement(RsiView, { views: seriesViews(data), unavailable }));

const VOID = new Set(['area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'source', 'track', 'wbr']);
const STRENGTHS = /^(Recorded fact|Anecdote|Single trial|Repeated trials|Held-out with interval)$/;

// Every element as { name, attrs, ancestors, text } and every text node as
// { text, ancestors }, from React's well-formed output.
function walk(html) {
  const body = html.replace(/<!--[\s\S]*?-->/g, '').replace(/<(script|style|template)\b[^>]*>[\s\S]*?<\/\1>/gi, '');
  const stack = [];
  const elements = [];
  const texts = [];
  let last = 0;
  const addText = (raw) => {
    const text = decode(raw);
    if (!text) return;
    texts.push({ text, ancestors: [...stack] });
    for (const el of stack) el.text += text;
  };
  for (const m of body.matchAll(/<(\/?)([a-zA-Z][\w-]*)([^>]*?)(\/?)>/g)) {
    addText(body.slice(last, m.index));
    last = m.index + m[0].length;
    const [, closing, rawName, rawAttrs, selfClose] = m;
    const name = rawName.toLowerCase();
    if (closing) {
      const at = stack.map((f) => f.name).lastIndexOf(name);
      if (at >= 0) stack.length = at;
      continue;
    }
    const el = { name, attrs: parseAttrs(rawAttrs), ancestors: [...stack], text: '' };
    elements.push(el);
    if (!VOID.has(name) && !selfClose) stack.push(el);
  }
  addText(body.slice(last));
  return { elements, texts };
}

const has = (el, attr) => attr in el.attrs;
const inside = (el, ancestor) => el.ancestors.includes(ancestor);
const placeOf = (doc, id) => doc.elements.find((e) => e.attrs['data-chart-place'] === id);
const seriesIn = (doc, place) => doc.elements.filter((e) => has(e, 'data-series') && inside(e, place));
const pointsIn = (doc, series) => doc.elements.filter((e) => has(e, 'data-point') && inside(e, series));
const marksIn = (doc, el, kind) => doc.elements.filter((e) => e.attrs['data-mark'] === kind && inside(e, el));

// Link coverage. Throws on a bare number, a number whose link does not reach
// its rows, or a row without a strength label.
function checkLinkCoverage(html) {
  const doc = walk(html);
  const numbers = doc.elements.filter((e) => e.name === 'a' && has(e, 'data-number'));
  assert.ok(numbers.length > 0, 'no rendered number found; the fixture should render numbers');
  for (const n of numbers) {
    const href = n.attrs.href ?? '';
    assert.match(href, /^#./, `number "${n.text}" does not link to its rows`);
    const target = doc.elements.find((e) => e.attrs.id === href.slice(1));
    assert.ok(target && has(target, 'data-rows'), `number "${n.text}" links to ${href}, which is not a row list`);
    const rows = doc.elements.filter((e) => has(e, 'data-row') && inside(e, target));
    const want = (n.attrs['data-row-ids'] ?? '').split(/\s+/).filter(Boolean).sort();
    assert.ok(want.length > 0, `number "${n.text}" names no rows`);
    assert.deepEqual(rows.map((r) => r.attrs['data-row-id']).sort(), want, `number "${n.text}" links to rows other than its own`);
    for (const row of rows) {
      const [strength] = doc.elements.filter((e) => has(e, 'data-strength') && inside(e, row));
      assert.ok(strength, `row ${row.attrs['data-row-id']} shows no strength label`);
      assert.match(strength.text.trim(), STRENGTHS, `row ${row.attrs['data-row-id']} strength label`);
    }
  }
  // No digit in a chart place outside a number link, a row list (the rows
  // themselves) or a labeled identifier such as a model name or a commit.
  for (const { text, ancestors } of doc.texts) {
    if (!/\d/.test(text)) continue;
    if (!ancestors.some((a) => has(a, 'data-chart-place'))) continue;
    const ok = ancestors.some((a) => (a.name === 'a' && has(a, 'data-number')) || has(a, 'data-rows') || has(a, 'data-label'));
    assert.ok(ok, `bare number in a chart place: "${text.trim()}"`);
  }
}

test('link coverage: every rendered number links to exactly its rows, each with a strength label', () => {
  checkLinkCoverage(render(cases.linkCoverageCase));
});

test('link coverage: the check fails on a bare number and on a link to the wrong rows', () => {
  const html = render(cases.linkCoverageCase);
  const bare = html.replace(/<a([^>]*)data-number=""([^>]*)>([^<]*)<\/a>/, '<span>$3</span>');
  assert.notEqual(bare, html, 'the bare-number fault no longer applies');
  assert.throws(() => checkLinkCoverage(bare), assert.AssertionError);
  const wrong = html.replace(/(<a[^>]*data-number=""[^>]*data-row-ids=")([^"]*)"/, '$1$2 999999"');
  const wrong2 = wrong === html ? html.replace(/(<a[^>]*data-row-ids=")([^"]*)("[^>]*data-number="")/, '$1$2 999999$3') : wrong;
  assert.notEqual(wrong2, html, 'the wrong-rows fault no longer applies');
  assert.throws(() => checkLinkCoverage(wrong2), assert.AssertionError);
  const noStrength = html.replace(/data-strength=""/g, 'data-x=""');
  assert.throws(() => checkLinkCoverage(noStrength), assert.AssertionError);
});

test('every case renders every planned place, held-out and dev apart, and each place passes link coverage', () => {
  for (const name of ['linkCoverageCase', 'modelChangeCase', 'regressionCase', 'dispositionCase', 'testRowCase']) {
    const html = render(cases[name]);
    CHECKS['every planned series place is rendered once, no unplanned place appears'](readPage(html));
    CHECKS['held-out and dev places sit in separate, labeled split sections'](readPage(html));
    checkLinkCoverage(html);
  }
});

test('each series shows provider, model, effort, arm and the system version of each point', () => {
  const doc = walk(render(cases.linkCoverageCase));
  const all = doc.elements.filter((e) => has(e, 'data-series'));
  assert.ok(all.length > 0);
  for (const s of all) {
    const [prov] = doc.elements.filter((e) => has(e, 'data-provenance') && inside(e, s));
    assert.ok(prov, `series ${s.attrs['data-series']} has no provenance`);
    for (const key of ['provider', 'model', 'effort']) {
      assert.ok(s.attrs[`data-${key}`], `series lacks data-${key}`);
      assert.ok(prov.text.includes(s.attrs[`data-${key}`]), `provenance does not show ${key}`);
    }
    for (const p of pointsIn(doc, s)) {
      const [runtime, controls, skills] = p.attrs['data-version'].split('.');
      for (const c of [runtime, controls, skills]) assert.ok(p.text.includes(c.slice(0, 7)), `point does not show commit ${c.slice(0, 7)}`);
    }
  }
});

test('model change: two models render as two series, never one line', () => {
  const doc = walk(render(cases.modelChangeCase));
  const place = placeOf(doc, 'dev-per-task');
  const series = seriesIn(doc, place);
  assert.equal(series.length, 2, 'a model change must start a new series');
  assert.deepEqual(series.map((s) => s.attrs['data-model']).sort(), ['fixture-model-a', 'fixture-model-b']);
  for (const s of series) assert.equal(pointsIn(doc, s).length, 1, `series ${s.attrs['data-model']} must hold only its own model's version`);
  // A drawn line never spans a model change: every polyline sits in one
  // series and joins only that series' points.
  for (const line of doc.elements.filter((e) => e.name === 'polyline')) {
    const owners = line.ancestors.filter((a) => has(a, 'data-series'));
    assert.equal(owners.length, 1, 'a line must sit inside exactly one series');
    const pairs = (line.attrs.points ?? '').trim().split(/\s+/).filter(Boolean).length;
    assert.equal(pairs, pointsIn(doc, owners[0]).length, 'a line joins only its own series points');
  }
  const perVersion = seriesIn(doc, placeOf(doc, 'dev-per-version'));
  assert.equal(perVersion.length, 2, 'the per-version view also splits on the model');
  // Control: with one model across the same two versions, one series and
  // one line join both points, so the split above is the model's doing.
  const same = walk(render(cases.regressionCase));
  const [one, ...extra] = seriesIn(same, placeOf(same, 'dev-per-task'));
  assert.equal(extra.length, 0);
  const lines = same.elements.filter((e) => e.name === 'polyline' && inside(e, one));
  assert.equal(lines.length, 1);
  assert.equal(lines[0].attrs.points.trim().split(/\s+/).length, 2);
});

test('regression: a version that passes fewer trials than the prior one is marked as a regression', () => {
  const doc = walk(render(cases.regressionCase));
  for (const id of ['dev-per-task', 'dev-per-version']) {
    const [series] = seriesIn(doc, placeOf(doc, id));
    const [first, second] = pointsIn(doc, series);
    assert.equal(marksIn(doc, first, 'regression').length, 0, `${id}: the first version is not a regression`);
    const [mark] = marksIn(doc, second, 'regression');
    assert.ok(mark, `${id}: the regression is not marked`);
    assert.match(mark.text, /regression/i);
  }
  // The improving case carries no regression mark.
  const up = walk(render(cases.linkCoverageCase));
  const [alpha] = seriesIn(up, placeOf(up, 'dev-per-task'));
  assert.equal(marksIn(up, alpha, 'regression').length, 0);
});

// S-002 row contract: detail.variant, detail.disposition ("retain", "revise",
// "remove"), detail.version, state "stopped" with detail.stop_rule and
// detail.stop_note, and state "failed" as a failed run, not a stop.
test('variants, removed versions and fired stop rules are marked from the S-002 row contract', () => {
  const doc = walk(render(cases.dispositionCase));
  const [series] = seriesIn(doc, placeOf(doc, 'dev-per-task'));
  const [v1, v2, v3] = pointsIn(doc, series);
  assert.match(marksIn(doc, v1, 'variant')[0]?.text ?? '', /variant/i, 'detail.variant true is not marked');
  assert.ok(v1.text.includes('fixture-candidate-one'), 'the candidate version label (detail.version) is not shown');
  assert.match(marksIn(doc, v2, 'removed')[0]?.text ?? '', /removed/i, 'disposition "remove" is not marked removed');
  assert.equal(marksIn(doc, v2, 'variant').length, 0);
  const [stop] = marksIn(doc, v3, 'stop-rule');
  assert.ok(stop, 'the fired stop rule is not marked');
  assert.match(stop.text, /stop rule/i);
  assert.match(stop.text, /three strikes/i, 'the rule is not in plain words');
  assert.doesNotMatch(stop.text, /three_strikes/, 'the rule shows its raw code');
  assert.ok(stop.text.includes(cases.STOP_NOTE), 'the stop note is not shown');
  assert.equal(marksIn(doc, v3, 'failed-run').length, 0, 'a stop is not a failed run');
});

test('each stop rule code reads in plain words', async () => {
  const { STOP_RULE_TEXT } = await import('../app/rsi/data.ts');
  for (const code of ['three_strikes', 'paid_plan_requested', 'meter_spent', 'owner_stop']) {
    assert.ok(STOP_RULE_TEXT[code], `no plain words for ${code}`);
    assert.doesNotMatch(STOP_RULE_TEXT[code], /_/);
  }
});

test('a revise disposition is not a variant, a failed run is marked distinctly, and missing detail keys are absent', () => {
  const doc = walk(render(cases.failedRunCase));
  const [series] = seriesIn(doc, placeOf(doc, 'dev-per-task'));
  const [revise, failed, bare] = pointsIn(doc, series);
  assert.equal(marksIn(doc, revise, 'variant').length, 0, 'revise must not read as a variant');
  assert.equal(marksIn(doc, revise, 'removed').length, 0);
  const [f] = marksIn(doc, failed, 'failed-run');
  assert.ok(f, 'a failed run is not marked');
  assert.match(f.text, /failed run/i);
  assert.equal(marksIn(doc, failed, 'stop-rule').length, 0, 'a failed run is not a stop');
  assert.equal(doc.elements.filter((e) => has(e, 'data-mark') && inside(e, bare)).length, 0, 'a run with no detail carries no mark');
  checkLinkCoverage(render(cases.failedRunCase));
});

test('test rows never render', () => {
  const html = render(cases.testRowCase);
  assert.ok(!html.includes(cases.TEST_ROW_MARKER), 'a test row rendered');
  const doc = walk(html);
  const rows = doc.elements.filter((e) => has(e, 'data-row'));
  const testIds = new Set(cases.testRowCase.results.filter((r) => r.is_test).map((r) => String(r.id)));
  assert.ok(rows.length > 0, 'the real row should render');
  for (const r of rows) assert.ok(!testIds.has(r.attrs['data-row-id']), `test row ${r.attrs['data-row-id']} rendered`);
  // The held-out places only had test rows, so they stay empty.
  for (const id of ['held-out-per-task', 'held-out-per-version']) {
    const place = placeOf(doc, id);
    assert.ok(doc.elements.some((e) => has(e, 'data-empty-message') && inside(e, place)), `${id} must stay empty`);
  }
});

test('empty state: zero rows keep every TK-001 empty-state check, with no number and no load note', () => {
  const html = render(cases.emptyCase);
  for (const check of Object.values(CHECKS)) check(readPage(html));
  assert.ok(!html.includes('data-load-note'), 'a successful empty read must not claim a load failure');
});

test('unavailable: a failed read renders the empty state with a short "could not be loaded" note', () => {
  const html = render(cases.emptyCase, true);
  for (const check of Object.values(CHECKS)) check(readPage(html));
  const note = walk(html).elements.find((e) => has(e, 'data-load-note'));
  assert.ok(note, 'no load note');
  assert.match(note.text, /could not be loaded/i);
});

// The Supabase read: plain fetch to PostgREST with the publishable key, test
// rows filtered in the query and again on receipt, and any failure reported
// as unavailable instead of thrown.
const ENV = { NEXT_PUBLIC_SUPABASE_URL: 'https://fixture.supabase.co', NEXT_PUBLIC_SUPABASE_ANON_KEY: 'fixture-publishable-key' };
const ok = (body) => ({ ok: true, status: 200, json: async () => body });

test('load: reads both tables with apikey and bearer headers and an explicit is_test=is.false filter', async () => {
  const calls = [];
  const fetchImpl = async (url, init) => {
    calls.push({ url: String(url), headers: init?.headers ?? {} });
    return ok(String(url).includes('rsi_runs') ? cases.testRowCase.runs : cases.testRowCase.results);
  };
  const out = await loadRsiData({ env: ENV, fetchImpl });
  assert.equal(out.ok, true);
  const tables = calls.map((c) => new URL(c.url).pathname).sort();
  assert.deepEqual(tables, ['/rest/v1/rsi_results', '/rest/v1/rsi_runs']);
  for (const c of calls) {
    const u = new URL(c.url);
    assert.equal(u.searchParams.get('is_test'), 'is.false', `${u.pathname} must filter test rows`);
    assert.ok(u.searchParams.get('select'), `${u.pathname} must name its columns`);
    assert.equal(c.headers.apikey, ENV.NEXT_PUBLIC_SUPABASE_ANON_KEY);
    assert.equal(c.headers.Authorization, `Bearer ${ENV.NEXT_PUBLIC_SUPABASE_ANON_KEY}`);
  }
  // Rows marked as test that reach the page anyway are dropped on receipt.
  assert.ok(out.data.results.every((r) => r.is_test === false));
  assert.ok(out.data.runs.every((r) => r.is_test === false));
  assert.equal(out.data.results.length, 1);
});

test('load: missing env, a refused request, an error status or a bad body each give the empty, unavailable state', async () => {
  let called = false;
  const never = async () => { called = true; return ok([]); };
  const missing = await loadRsiData({ env: {}, fetchImpl: never });
  assert.equal(missing.ok, false);
  assert.equal(called, false, 'no request without both env vars');
  const failures = [
    async () => { throw new Error('network down'); },
    async () => ({ ok: false, status: 503, json: async () => ({}) }),
    async () => ok({ not: 'an array' }),
  ];
  for (const fetchImpl of failures) {
    const out = await loadRsiData({ env: ENV, fetchImpl });
    assert.equal(out.ok, false);
    assert.deepEqual(out.data, { runs: [], results: [] });
    assert.ok(!JSON.stringify(out).includes(ENV.NEXT_PUBLIC_SUPABASE_ANON_KEY), 'a failure report must not carry the key');
  }
});
