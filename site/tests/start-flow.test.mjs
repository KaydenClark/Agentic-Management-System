// S-003 /start: the lifecycle diagram, the toy's no-JS fallback and the toy
// itself all read one data file, app/start/flow.mjs, so they cannot disagree.
// Over the built output: every stage in flow.mjs appears in the diagram and in
// the no-JS fallback; the returned branch exists and uses the returned token;
// only the holder hues colour the page; the toy's source makes no request and
// stores nothing. Keyboard play to the last stage, zero requests and empty
// storage while playing are checked live in tests/browser.check.mjs.
// Run `npm run build` first. The data is plain JavaScript (flow.mjs, typed
// by flow.d.mts), so this runs on every Node that runs `npm test`.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { join } from 'node:path';
import { pathToFileURL } from 'node:url';
import { builtPage, siteDir, sourceFiles, visibleText } from './helpers.mjs';
import { mainOf } from './tour-helpers.mjs';

const flow = await import(pathToFileURL(join(siteDir, 'app', 'start', 'flow.mjs')).href);

// Inner HTML of the first element carrying `attr`, nesting of the same tag
// included; null when there is none.
export function elementWith(html, attr) {
  const open = html.match(new RegExp(`<([a-z][\\w-]*)\\b[^>]*\\s${attr}(?:=|[\\s>])[^>]*>`, 'i'));
  if (!open) return null;
  const tag = open[1].toLowerCase();
  const start = open.index + open[0].length;
  const re = new RegExp(`<(/?)${tag}\\b[^>]*>`, 'gi');
  re.lastIndex = start;
  let depth = 1;
  for (let m = re.exec(html); m; m = re.exec(html)) {
    depth += m[1] ? -1 : 1;
    if (depth === 0) return html.slice(start, m.index);
  }
  return null;
}

// Problems with one rendering of the stages (the diagram or the fallback):
// each stage must appear once with its name and the hue class of its holder.
export function stageProblems(fragment, stages, hueOf, where) {
  if (fragment === null) return [`${where}: not found`];
  const problems = [];
  for (const s of stages) {
    const items = [...fragment.matchAll(new RegExp(`<li\\b[^>]*data-stage="${s.id}"[^>]*>`, 'g'))];
    if (items.length !== 1) { problems.push(`${where}: stage ${s.id} appears ${items.length} times`); continue; }
    const body = elementWith(fragment.slice(items[0].index), `data-stage="${s.id}"`) ?? '';
    if (!visibleText(body).includes(s.name)) problems.push(`${where}: stage ${s.id} does not show its name ${s.name}`);
    if (!new RegExp(`class="[^"]*\\b${hueOf(s.holder)}\\b`).test(items[0][0])) problems.push(`${where}: stage ${s.id} lacks ${hueOf(s.holder)}`);
  }
  return problems;
}

const hueOf = (holder) => flow.HOLDERS[holder].hue;
const html = builtPage('start.html').html;
const main = mainOf(html);

test('flow.mjs: a lifecycle from a request to done, with real stage names and sources', () => {
  const ids = flow.stages.map((s) => s.id);
  assert.ok(flow.stages.length >= 8, 'too few stages for the lifecycle');
  assert.equal(new Set(ids).size, ids.length, 'duplicate stage ids');
  assert.equal(flow.stages[0].holder, 'owner', 'work starts with the owner');
  assert.equal(flow.stages.at(-1).holder, 'done', 'the last stage is done');
  for (const name of ['Confirm', 'Spec', 'Task', 'Claim', 'Build', 'Check', 'Review', 'Approve']) {
    assert.ok(flow.stages.some((s) => s.name === name), `no ${name} stage`);
  }
  for (const s of flow.stages) {
    assert.ok(s.line && s.sources.length, `${s.id}: no line or no source`);
    for (const src of s.sources) assert.ok(readFileSync(join(siteDir, '..', src.path)), `${s.id}: ${src.path}`);
    for (const c of [s.next, s.back].filter(Boolean)) assert.ok(ids.includes(c.to), `${s.id}: choice to unknown ${c.to}`);
  }
  // Holders are exactly the four signals the page states.
  assert.deepEqual(Object.keys(flow.HOLDERS).sort(), ['agent', 'done', 'owner', 'returned']);
  assert.deepEqual(Object.values(flow.HOLDERS).map((h) => h.hue).sort(), ['h-agent', 'h-none', 'h-owner', 'h-returned']);
});

test('the stage check catches a missing, unnamed or wrongly coloured stage (self-test)', () => {
  const stages = [{ id: 'a', name: 'Ask', holder: 'owner' }, { id: 'b', name: 'Build', holder: 'agent' }];
  const hue = (h) => ({ owner: 'h-owner', agent: 'h-agent' })[h];
  const ok = '<li data-stage="a" class="tone h-owner">Ask</li><li data-stage="b" class="tone h-agent">Build</li>';
  assert.deepEqual(stageProblems(ok, stages, hue, 'x'), []);
  assert.ok(stageProblems('<li data-stage="a" class="tone h-owner">Ask</li>', stages, hue, 'x').length, 'missing stage passes');
  assert.ok(stageProblems(ok.replace('>Build<', '>?<'), stages, hue, 'x').length, 'unnamed stage passes');
  assert.ok(stageProblems(ok.replace('h-agent', 'h-heat'), stages, hue, 'x').length, 'wrong hue passes');
  assert.ok(stageProblems(null, stages, hue, 'x').length, 'absent rendering passes');
  assert.equal(elementWith('<ol data-x=""><li><ol><li>i</li></ol></li></ol><ol><li>after</li></ol>', 'data-x'), '<li><ol><li>i</li></ol></li>');
});

test('/start: every stage in flow.mjs appears in the lifecycle diagram', () => {
  assert.deepEqual(stageProblems(elementWith(main, 'data-flow-diagram'), flow.stages, hueOf, 'diagram'), []);
});

test('/start: every stage in flow.mjs appears in the no-JS fallback, numbered and server-rendered', () => {
  const fallback = elementWith(main, 'data-toy-fallback');
  assert.deepEqual(stageProblems(fallback, flow.stages, hueOf, 'fallback'), []);
  assert.match(main, /<ol\b[^>]*data-toy-fallback/, 'the fallback is not a numbered list');
  for (const s of flow.stages) assert.ok(visibleText(fallback).includes(visibleText(s.line)), `fallback lacks the text of ${s.id}`);
});

test('/start: the returned branch exists and uses the returned token', () => {
  const returned = flow.stages.filter((s) => s.holder === 'returned');
  assert.equal(returned.length, 1, 'no single returned stage');
  const into = flow.stages.filter((s) => s.back?.to === returned[0].id);
  assert.ok(into.length >= 1, 'no choice sends work back');
  assert.ok(returned[0].next && flow.stages.find((s) => s.id === returned[0].next.to)?.holder === 'agent', 'returned work does not go back to an agent');
  assert.equal(flow.HOLDERS.returned.hue, 'h-returned');
  const tokens = readFileSync(join(siteDir, 'app', 'theme', 'tokens.css'), 'utf8');
  assert.match(tokens, /\.h-returned\s*\{\s*--hue:\s*var\(--returned\);/, 'h-returned does not set the returned token');
  assert.match(elementWith(main, 'data-flow-diagram') ?? '', /data-stage="[^"]+"[^>]*class="[^"]*\bh-returned\b|class="[^"]*\bh-returned\b[^"]*"[^>]*data-stage/, 'diagram shows no returned stage in h-returned');
});

test('/start: only the holder hues colour the page, each through the tone tokens', () => {
  const hues = new Set([...main.matchAll(/\bh-(heat|worth|owner|agent|returned|none)\b/g)].map((m) => m[0]));
  for (const h of hues) assert.ok(['h-owner', 'h-agent', 'h-returned', 'h-none'].includes(h), `${h} on /start has no meaning here`);
  for (const f of sourceFiles('app/start', ['.css'])) {
    assert.doesNotMatch(f.text, /var\(--(?:heat|worth|owner|agent|returned)\)/, `${f.name}: raw hue token; use the .tone mixes`);
  }
});

test('/start: the toy source makes no request and stores nothing', () => {
  const toy = sourceFiles('app/start', ['.tsx', '.ts', '.mjs']);
  assert.ok(toy.some((f) => /"use client"/.test(f.text)), 'no client component for the toy');
  for (const f of toy) {
    assert.doesNotMatch(f.text, /\b(?:fetch|XMLHttpRequest|WebSocket|EventSource|sendBeacon|localStorage|sessionStorage|indexedDB|document\.cookie|caches)\b/, `${f.name}: network or storage API`);
  }
});

test('/start: no owner quote is shown', () => {
  assert.doesNotMatch(main, /data-owner-quote|<blockquote\b/i);
});
