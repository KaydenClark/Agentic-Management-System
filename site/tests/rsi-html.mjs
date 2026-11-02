// Shared readers and the empty-state checks for the /rsi page (S-007). Used by
// the built-page test (rsi-empty) and the fixture render tests (rsi-rows), so
// the empty state is held to one definition wherever it is rendered.
import assert from 'node:assert/strict';

// The planned series: per task and per version, held-out and dev (S-007
// Desired Behavior). Listed here, not imported, so a dropped place fails.
export const SERIES = [
  { id: 'held-out-per-task', split: 'held-out' },
  { id: 'held-out-per-version', split: 'held-out' },
  { id: 'dev-per-task', split: 'dev' },
  { id: 'dev-per-version', split: 'dev' }
];

const VOID = new Set(['area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'source', 'track', 'wbr']);
export const TRACKED = ['data-rsi-page', 'data-split', 'data-chart-place', 'data-plot', 'data-empty-message', 'data-explanation', 'data-next-event'];
const CHART_MARKS = new Set(['svg', 'canvas', 'path', 'polyline', 'polygon', 'rect', 'circle', 'line', 'img', 'picture', 'iframe', 'object']);

export function parseAttrs(source) {
  const attrs = {};
  for (const m of source.matchAll(/([^\s=/>]+)(?:\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s>]+)))?/g)) {
    attrs[m[1].toLowerCase()] = m[2] ?? m[3] ?? m[4] ?? '';
  }
  return attrs;
}

export function decode(text) {
  return text
    .replace(/&nbsp;/g, ' ')
    .replace(/&#x([0-9a-f]+);/gi, (_, h) => String.fromCodePoint(parseInt(h, 16)))
    .replace(/&#(\d+);/g, (_, d) => String.fromCodePoint(Number(d)))
    .replace(/&quot;/g, '"').replace(/&#39;/g, "'").replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&amp;/g, '&');
}

// A small tag-stack reader: enough for React's well-formed output. Records,
// for every element carrying a tracked attribute, its visible text, its
// ancestors' attributes and the tag names inside it.
export function readPage(html, trackedAttrs = TRACKED) {
  const body = html.replace(/<!--[\s\S]*?-->/g, '').replace(/<(script|style|template)\b[^>]*>[\s\S]*?<\/\1>/gi, '');
  const stack = [];
  const tracked = [];
  const tagRe = /<(\/?)([a-zA-Z][\w-]*)([^>]*?)(\/?)>/g;
  let last = 0;
  const addText = (text) => {
    if (!text) return;
    for (const frame of stack) if (frame.record) frame.record.text += decode(text);
  };
  for (const m of body.matchAll(tagRe)) {
    addText(body.slice(last, m.index));
    last = m.index + m[0].length;
    const [, closing, rawName, rawAttrs, selfClose] = m;
    const name = rawName.toLowerCase();
    if (closing) {
      const at = stack.map((f) => f.name).lastIndexOf(name);
      if (at >= 0) stack.length = at;
      continue;
    }
    const attrs = parseAttrs(rawAttrs);
    for (const frame of stack) if (frame.record) frame.record.inner.push({ name, attrs });
    const frame = { name, attrs, record: null };
    if (trackedAttrs.some((a) => a in attrs)) {
      frame.record = { name, attrs, ancestors: stack.map((f) => ({ name: f.name, attrs: f.attrs })), inner: [], text: '' };
      tracked.push(frame.record);
    }
    if (!VOID.has(name) && !selfClose) stack.push(frame);
  }
  addText(body.slice(last));
  return tracked;
}

export function hiddenMarker({ name, attrs }) {
  if ('hidden' in attrs) return `${name}[hidden]`;
  if ('inert' in attrs) return `${name}[inert]`;
  if ((attrs['aria-hidden'] ?? '').toLowerCase() === 'true') return `${name}[aria-hidden=true]`;
  const style = (attrs.style ?? '').replace(/\s+/g, '').toLowerCase();
  if (/display:none|visibility:hidden|opacity:0(?![.\d])|height:0(?![.\d])/.test(style)) return `${name}[style=${attrs.style}]`;
  if (name === 'details' && !('open' in attrs)) return 'details (collapsed)';
  return null;
}

export const places = (tracked) => tracked.filter((r) => 'data-chart-place' in r.attrs);
export const placeById = (tracked, id) => places(tracked).find((r) => r.attrs['data-chart-place'] === id);
export const within = (tracked, place, attr) => tracked.filter((r) => attr in r.attrs && r.ancestors.some((a) => a.attrs === place.attrs));

// Each check throws on the fault it names. The tests below run every check on
// the built page, then again on planted-fault copies to prove each one fails.
export const CHECKS = {
  'every planned series place is rendered once, no unplanned place appears': (tracked) => {
    assert.ok(tracked.some((r) => 'data-rsi-page' in r.attrs), 'the /rsi page root is missing');
    const ids = places(tracked).map((r) => r.attrs['data-chart-place']).sort();
    assert.deepEqual(ids, SERIES.map((s) => s.id).sort());
  },

  'held-out and dev places sit in separate, labeled split sections': (tracked) => {
    const splits = tracked.filter((r) => 'data-split' in r.attrs);
    assert.deepEqual(splits.map((r) => r.attrs['data-split']).sort(), ['dev', 'held-out']);
    for (const split of splits) assert.match(split.text, split.attrs['data-split'] === 'dev' ? /\bdev\b/i : /\bheld-out\b/i);
    for (const { id, split } of SERIES) {
      const place = placeById(tracked, id);
      assert.ok(place, `place ${id} missing`);
      const owners = place.ancestors.filter((a) => 'data-split' in a.attrs).map((a) => a.attrs['data-split']);
      assert.deepEqual(owners, [split], `place ${id} must sit only in the ${split} section`);
    }
  },

  'each place says no trials are recorded, explains task, trial and version, and names the next expected event': (tracked) => {
    for (const { id } of SERIES) {
      const place = placeById(tracked, id);
      assert.ok(place, `place ${id} missing`);
      const [empty] = within(tracked, place, 'data-empty-message');
      assert.ok(empty, `place ${id} has no empty-state message`);
      assert.match(empty.text, /no trials are recorded yet/i, `place ${id} empty message`);
      const [explanation] = within(tracked, place, 'data-explanation');
      assert.ok(explanation, `place ${id} has no explanation`);
      for (const term of ['task', 'trial', 'version']) {
        assert.match(explanation.text, new RegExp(`\\b${term}\\b[^.]*\\b(is|means)\\b`, 'i'), `place ${id} does not explain "${term}"`);
      }
      const [next] = within(tracked, place, 'data-next-event');
      assert.ok(next, `place ${id} names no next expected event`);
      assert.match(next.text, /next expected event/i, `place ${id} next-event label`);
      assert.ok(next.inner.some((t) => t.name === 'a' && /^https:\/\//.test(t.attrs.href ?? '')), `place ${id} next event must link its source record`);
    }
  },

  'no digit appears in any chart place or anywhere in the page content': (tracked) => {
    const root = tracked.find((r) => 'data-rsi-page' in r.attrs);
    assert.ok(root, 'the /rsi page root is missing');
    for (const place of places(tracked)) {
      assert.doesNotMatch(place.text, /\d/, `place ${place.attrs['data-chart-place']} contains a digit: ${place.text.match(/.{0,30}\d.{0,30}/)?.[0]}`);
    }
    assert.doesNotMatch(root.text, /\d/, `page content contains a digit: ${root.text.match(/.{0,30}\d.{0,30}/)?.[0]}`);
  },

  'no sample chart: each place has an empty plot area and no drawn marks': (tracked) => {
    for (const place of places(tracked)) {
      const id = place.attrs['data-chart-place'];
      const marks = place.inner.filter((t) => CHART_MARKS.has(t.name)).map((t) => t.name);
      assert.deepEqual(marks, [], `place ${id} draws ${marks.join(', ')}`);
      const [plot] = within(tracked, place, 'data-plot');
      assert.ok(plot, `place ${id} has no plot area`);
      assert.equal(plot.inner.length, 0, `place ${id} plot area must be empty`);
      assert.equal(plot.text.trim(), '', `place ${id} plot area must hold no text`);
    }
  },

  'no place, its section or anything inside it is hidden': (tracked) => {
    for (const record of tracked) {
      const attr = TRACKED.find((a) => a in record.attrs);
      const found = [record, ...record.ancestors, ...record.inner].map(hiddenMarker).filter(Boolean);
      assert.deepEqual(found, [], `${record.name}[${attr}=${record.attrs[attr]}] is hidden by ${found.join(', ')}`);
    }
  }
};
