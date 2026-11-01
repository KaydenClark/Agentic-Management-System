// S-003 TK-006 acceptance: /under-the-hood renders S-006's build_events rows
// in time order, returns and corrections included, each linking its source;
// every history sentence comes from a row; test rows never render; agent
// session links are stripped; no rows gives the empty state with the next
// expected event. The renderer is app/under-the-hood/history.ts, the same
// module the page uses, rendered here with react-dom/server on fixtures (Node
// strips the TypeScript types). The built-page tests read `npm run build`.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { createElement } from 'react';
import { renderToStaticMarkup } from 'react-dom/server';
import { readdirSync, readFileSync, statSync } from 'node:fs';
import { join } from 'node:path';
import { builtPage, servedFiles, siteDir, visibleText } from './helpers.mjs';
import { hygieneFindings } from './hygiene.mjs';
import { mainOf, pageProblems } from './tour-helpers.mjs';
import { FIXTURE_ORDER, FIXTURE_ROWS } from './fixtures/build-events.mjs';
import { History, CATEGORIES, categoryOf, eventTime, groupLabel, historyView, kindLabel, readBuildEvents, stripSessionLinks, toneOf } from '../app/under-the-hood/history.ts';

const render = (rows, note = null) => renderToStaticMarkup(createElement(History, { view: historyView(rows), note }));
const decode = (s) => s.replace(/&amp;/g, '&').replace(/&#x27;|&#39;/g, "'").replace(/&quot;/g, '"').replace(/&lt;/g, '<').replace(/&gt;/g, '>');
const text = (html) => decode(visibleText(html));
const attr = (tag, name) => decode(tag.match(new RegExp(`\\s${name}="([^"]*)"`, "i"))?.[1] ?? "");
const field = (html, name) => {
  const m = html.match(new RegExp(`<([a-z]+)\\b[^>]*data-field="${name}"[^>]*>([\\s\\S]*?)</\\1>`));
  return m ? { tag: m[0], text: text(m[2]) } : null;
};

// The history region: everything inside <section data-history>.
const historyOf = (html) => html.match(/<section\b[^>]*data-history[^>]*>([\s\S]*?)<\/section>/)?.[1] ?? '';
const eventsOf = (html) => [...historyOf(html).matchAll(/<li\b[^>]*data-event[^>]*>[\s\S]*?<\/li>/g)].map((m) => m[0]);
const rowIds = (html) => eventsOf(html).map((li) => Number(attr(li, 'data-row-id')));

// Problems with the history region's provenance; empty when every sentence in
// it comes from a row. Each event's text must be exactly its row's fields
// (kind label, time, summary, subject), its link the row's source_url; each
// group heading must be its rows' time and count; anything else in the
// region (a hand-written sentence) is a problem.
function historyProblems(html, rows) {
  const problems = [];
  const byId = new Map(rows.map((r) => [r.id, r]));
  let rest = historyOf(html);
  if (!rest) return ['no history region (<section data-history>)'];
  for (const li of eventsOf(html)) {
    const id = Number(attr(li, 'data-row-id'));
    const row = byId.get(id);
    rest = rest.replace(li, ' ');
    if (!row) { problems.push(`event ${id || '(no id)'} does not come from a row`); continue; }
    if (row.is_test !== false) problems.push(`event ${id} is a test row`);
    const want = { kind: kindLabel(row.kind), time: eventTime(row.occurred_at), summary: stripSessionLinks(row.summary), subject: stripSessionLinks(row.subject) };
    const got = {};
    for (const name of Object.keys(want)) {
      got[name] = field(li, name)?.text;
      if (got[name] !== want[name]) problems.push(`event ${id} ${name} is "${got[name]}", its row says "${want[name]}"`);
    }
    const link = li.match(/<a\b[^>]*>/)?.[0] ?? '';
    if (attr(link, 'href') !== row.source_url) problems.push(`event ${id} links "${attr(link, 'href')}", its row's source is "${row.source_url}"`);
    const time = field(li, 'time');
    if (time && attr(time.tag, 'datetime') !== row.occurred_at) problems.push(`event ${id} datetime is not its row's occurred_at`);
    if (text(li) !== Object.values(want).join(' ')) problems.push(`event ${id} has words that are not its row's: "${text(li)}"`);
  }
  for (const m of rest.matchAll(/<details\b[^>]*data-group="([^"]*)"[^>]*>\s*<summary\b[^>]*>([\s\S]*?)<\/summary>/g)) {
    const members = rows.filter((r) => r.is_test === false && r.source_url && groupLabel(r.occurred_at) === text(field(m[2], 'when')?.tag ?? ''));
    const count = field(m[2], 'count')?.text;
    if (!members.length) problems.push(`group "${text(m[2])}" names a time no row has`);
    if (!/^\d+ events?$/.test(count ?? '')) problems.push(`group count "${count}" is not a row count`);
    if (text(m[2]) !== `${field(m[2], 'when')?.text} ${count}`) problems.push(`group heading has words that are not from rows: "${text(m[2])}"`);
    rest = rest.replace(m[2], ' ');
  }
  // Filter controls: fixed category names with derived counts.
  rest = rest.replace(/<fieldset\b[^>]*data-filter[^>]*>[\s\S]*?<\/fieldset>/, (fs) => {
    const legend = text(fs.match(/<legend\b[^>]*>([\s\S]*?)<\/legend>/)?.[1] ?? '');
    if (legend !== 'Show') problems.push(`filter legend "${legend}"`);
    for (const lab of fs.matchAll(/<label\b[^>]*>([\s\S]*?)<\/label>/g)) {
      const t = text(lab[1]);
      if (!CATEGORIES.some((c) => new RegExp(`^${c.label} \\(\\d+\\)$`).test(t))) problems.push(`filter label "${t}" is not a category with a count`);
    }
    return ' ';
  });
  // The count line: derived numbers only.
  rest = rest.replace(/<p\b[^>]*data-totals[^>]*>([\s\S]*?)<\/p>/, (p, inner) => {
    if (!/^\d+ events?, oldest first\.( \d+ rows? not shown because (it has|they have) no https source link or no text\.)?$/.test(text(inner))) problems.push(`totals line "${text(inner)}" is not derived from rows`);
    return ' ';
  });
  const left = text(rest);
  if (left) problems.push(`history text not from a row: "${left}"`);
  // Grouped events must sit inside a group whose time is theirs.
  for (const g of historyOf(html).matchAll(/<details\b[^>]*data-group="[^"]*"[^>]*>([\s\S]*?)<\/details>/g)) {
    const when = field(g[1], 'when')?.text;
    for (const li of g[1].matchAll(/<li\b[^>]*data-event[^>]*>/g)) {
      const row = byId.get(Number(attr(li[0], 'data-row-id')));
      if (row && groupLabel(row.occurred_at) !== when) problems.push(`event ${row.id} is in group "${when}"`);
    }
    const n = [...g[1].matchAll(/<li\b[^>]*data-event/g)].length;
    const count = Number(field(g[1], 'count')?.text.split(' ')[0]);
    if (n !== count) problems.push(`group "${when}" says ${count} events and shows ${n}`);
  }
  return problems;
}

test('the provenance check catches hand-written history (self-test)', () => {
  const html = render(FIXTURE_ROWS);
  assert.deepEqual(historyProblems(html, FIXTURE_ROWS), []);
  const plant = (from, to) => historyProblems(html.replace(from, to), FIXTURE_ROWS);
  const firstLi = eventsOf(html)[0];
  assert.ok(plant('</ol>', '<li data-event="" data-row-id="777"><a href="https://github.com/x">We fixed everything</a></li></ol>').length, 'an event with no row passes');
  assert.ok(plant('</ol>', '</ol><p>Then the team shipped the whole site in an hour.</p>').length, 'a hand-written sentence passes');
  assert.ok(plant('Load fixture card contents', 'Rewrote fixture card contents').length, 'an edited summary passes');
  assert.ok(plant(firstLi, firstLi.replace('</li>', ' and it went well</li>')).length, 'an added clause passes');
  assert.ok(plant(/href="https:\/\/github.com\/KaydenClark\/Agentic-Management-System\/pull\/26"/, 'href="https://github.com/elsewhere"').length, 'a wrong source link passes');
  assert.ok(plant(/(data-field="count"[^>]*>)\d+/, '$1123').length, 'a made-up group count passes');
  assert.ok(historyProblems('<main><p>no region</p></main>', FIXTURE_ROWS).length, 'a page with no history region passes');
});

test('a fixture with a return and a correction renders both, in time order, with their source links', () => {
  const html = render(FIXTURE_ROWS);
  assert.deepEqual(rowIds(html), FIXTURE_ORDER, 'events are not in occurred_at order');
  for (const kind of ['correction', 'return']) {
    const row = FIXTURE_ROWS.find((r) => r.kind === kind);
    const li = eventsOf(html).find((l) => Number(attr(l, 'data-row-id')) === row.id);
    assert.ok(li, `${kind} row not rendered`);
    assert.equal(attr(li.match(/<a\b[^>]*>/)[0], 'href'), row.source_url, `${kind} does not link its source`);
    assert.equal(field(li, 'summary').text, row.summary);
  }
  assert.ok(rowIds(html).indexOf(30) < rowIds(html).indexOf(40), 'the correction does not come before the later return');
});

test('every history sentence comes from a row', () => {
  assert.deepEqual(historyProblems(render(FIXTURE_ROWS), FIXTURE_ROWS), []);
});

test('a test row never renders, and a row with no https source is counted, not shown', () => {
  const html = render(FIXTURE_ROWS);
  assert.ok(!rowIds(html).includes(99), 'test row rendered');
  assert.doesNotMatch(html, /HIDDEN TEST ROW|test999/);
  assert.ok(!rowIds(html).includes(98), 'unlinked row rendered');
  assert.doesNotMatch(html, /UNLINKED ROW/);
  assert.match(text(historyOf(html)), /1 row not shown because it has no https source link or no text\./);
  assert.ok(historyView(FIXTURE_ROWS).events.every((e) => e.row.is_test === false));
  // Only the test row and only test rows: still the empty state.
  const onlyTest = FIXTURE_ROWS.filter((r) => r.is_test);
  assert.match(render(onlyTest), /data-empty-state/);
});

test('agent session links are stripped from the rendered rows', () => {
  const html = render(FIXTURE_ROWS);
  assert.doesNotMatch(html, /claude\.ai\/code|session_0|Claude-Session/i);
  assert.deepEqual(hygieneFindings(html), []);
  assert.equal(field(eventsOf(html)[2], 'summary').text, 'Add the fixture page');
  assert.equal(stripSessionLinks('Wire it (see https://claude.ai/code/session_0abcdefghijklmnopqrstuvw)'), 'Wire it');
  assert.equal(stripSessionLinks('No trailer here'), 'No trailer here');
  // The rows themselves are untouched.
  assert.match(FIXTURE_ROWS.find((r) => r.id === 20).summary, /Claude-Session/);
});

test('with no rows the empty state says so and names the next expected event', () => {
  const html = render([]);
  assert.equal(eventsOf(html).length, 0);
  assert.match(html, /data-empty-state/);
  assert.match(text(html), /No build events are recorded yet\./);
  const next = html.match(/<p\b[^>]*data-next-event[^>]*>([\s\S]*?)<\/p>/);
  assert.ok(next, 'no next expected event');
  assert.match(next[1], /href="https:\/\/github\.com\/KaydenClark\/Agentic-Management-System\/blob\/dev\/[^"]+S-006[^"]*SPEC\.md"/);
  assert.deepEqual(historyProblems(html, []).filter((p) => !/no history region/.test(p)), []);
  const failed = render([], 'Supabase could not be read: it answered 503.');
  assert.match(text(failed), /Supabase could not be read: it answered 503\./);
  assert.match(failed, /data-empty-state/);
});

test('colors keep one meaning each: purple returned, green agent work, grey everything else', () => {
  assert.equal(toneOf({ kind: 'correction', detail: {} }), 'returned');
  assert.equal(toneOf({ kind: 'return', detail: {} }), 'returned');
  assert.equal(toneOf({ kind: 'task_claimed', detail: {} }), 'agent');
  assert.equal(toneOf({ kind: 'task_receipt', detail: {} }), 'agent');
  assert.equal(toneOf({ kind: 'commit', detail: { author: 'Claude' } }), 'agent');
  assert.equal(toneOf({ kind: 'commit', detail: { author: 'Kayden Clark' } }), 'none');
  for (const kind of ['spec', 'task', 'pr_opened', 'merge', 'spec_event', 'correction_fix', 'something_new']) assert.equal(toneOf({ kind, detail: {} }), 'none', kind);
  const html = render(FIXTURE_ROWS);
  for (const li of eventsOf(html)) {
    const row = FIXTURE_ROWS.find((r) => r.id === Number(attr(li, 'data-row-id')));
    const hues = [...li.matchAll(/\bh-([a-z]+)\b/g)].map((m) => m[1]);
    assert.deepEqual([...new Set(hues)], [toneOf(row)], `row ${row.id} uses ${hues}`);
  }
  assert.doesNotMatch(html, /\bh-(?:heat|worth|owner)\b/, 'a signal with another meaning is used');
});

test('kinds group into filter categories; unknown kinds still render with a plain label', () => {
  assert.equal(categoryOf('correction'), categoryOf('return'));
  assert.equal(categoryOf('commit'), categoryOf('correction_fix'));
  assert.equal(kindLabel('something_new'), 'Something new');
  const row = { id: 1, kind: 'something_new', subject: 's', summary: 'A new kind of event', occurred_at: '2026-11-01T13:00:00+00:00', source_url: 'https://github.com/x', is_test: false, detail: {} };
  const html = render([row]);
  assert.deepEqual(rowIds(html), [1]);
  assert.deepEqual(historyProblems(html, [row]), []);
});

test('readBuildEvents: plain REST read with the publishable key, test rows filtered, pages followed', async () => {
  const calls = [];
  const page = (n, from) => Array.from({ length: n }, (_, i) => ({ ...FIXTURE_ROWS[0], id: from + i }));
  const fetchImpl = async (url, init) => {
    calls.push({ url: String(url), init });
    const offset = Number(new URL(url).searchParams.get('offset'));
    return new Response(JSON.stringify(offset === 0 ? page(1000, 0) : page(3, 1000)), { status: 200 });
  };
  const got = await readBuildEvents({ url: 'https://example.supabase.co', key: 'sb_publishable_fixture', fetchImpl });
  assert.equal(got.note, null);
  assert.equal(got.rows.length, 1003);
  assert.equal(calls.length, 2);
  const u = new URL(calls[0].url);
  assert.equal(u.pathname, '/rest/v1/build_events');
  assert.equal(u.searchParams.get('is_test'), 'is.false');
  assert.equal(u.searchParams.get('order'), 'occurred_at.asc,id.asc');
  assert.equal(new Headers(calls[0].init.headers).get('apikey'), 'sb_publishable_fixture');
  assert.equal(calls[0].init.method ?? 'GET', 'GET');
});

test('readBuildEvents: missing settings or a failed read give no rows and a note, never a throw', async () => {
  const none = await readBuildEvents({ url: undefined, key: undefined, fetchImpl: async () => { throw new Error('must not be called'); } });
  assert.deepEqual(none.rows, []);
  assert.match(none.note, /not set/);
  const bad = await readBuildEvents({ url: 'https://example.supabase.co', key: 'k', fetchImpl: async () => new Response('nope', { status: 503 }) });
  assert.deepEqual(bad.rows, []);
  assert.match(bad.note, /503/);
  const thrown = await readBuildEvents({ url: 'https://example.supabase.co', key: 'k', fetchImpl: async () => { throw new Error('offline'); } });
  assert.deepEqual(thrown.rows, []);
  assert.ok(thrown.note);
  const junk = await readBuildEvents({ url: 'https://example.supabase.co', key: 'k', fetchImpl: async () => new Response('{"a":1}', { status: 200 }) });
  assert.deepEqual(junk.rows, []);
  assert.ok(junk.note);
  for (const r of [none, bad, thrown, junk]) assert.doesNotMatch(r.note, /example\.supabase|sb_publishable/);
});

// The built page.

test('/under-the-hood is built with its title, a plain-language opener and the history region', () => {
  const { html } = builtPage('under-the-hood.html');
  assert.match(html, /<title>Under the hood \| Agentic Management System<\/title>/);
  assert.match(visibleText(html.match(/<h1[\s\S]*?<\/h1>/i)?.[0] ?? ''), /Under the hood/);
  assert.match(html, /<section\b[^>]*data-history|data-empty-state/);
  // The tour inventory rules apply to the page's own prose; the rows are data.
  const prose = html.replace(/<section\b[^>]*data-history[^>]*>[\s\S]*?<\/section>/, '<section></section>');
  assert.deepEqual(pageProblems(prose), []);
});

test('the built page shows rows with source links, or the empty state', () => {
  const { html } = builtPage('under-the-hood.html');
  const events = eventsOf(mainOf(html));
  if (!events.length) {
    assert.match(html, /data-empty-state/);
    assert.match(html, /data-next-event/);
    return;
  }
  for (const li of events) {
    assert.ok(attr(li, 'data-row-id'), 'event without a row id');
    assert.match(attr(li.match(/<a\b[^>]*>/)?.[0] ?? '', 'href'), /^https:\/\//, 'event without a source link');
  }
});

// The key is read on the server at render time; it must not be inlined into
// any build output, served or not (server chunks, manifests, caches).
const KEY_SHAPE = /sb_(?:publishable|secret)_[A-Za-z0-9_-]{8,}/;
function* buildFiles(dir) {
  for (const name of readdirSync(dir)) {
    const path = join(dir, name);
    if (statSync(path).isDirectory()) yield* buildFiles(path);
    else yield path;
  }
}

test('no build output file carries a Supabase key, the publishable one included', () => {
  for (const f of servedFiles()) assert.doesNotMatch(f.text, KEY_SHAPE, f.name);
  for (const path of buildFiles(join(siteDir, '.next'))) {
    assert.doesNotMatch(readFileSync(path, 'latin1'), KEY_SHAPE, path.slice(siteDir.length));
  }
});
