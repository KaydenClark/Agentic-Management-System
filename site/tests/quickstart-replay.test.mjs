// S-003 TK-003 acceptance, Quickstart replays: a test runs the quickstart's
// commands on a fresh clone and gets the shown output.
// The page and this test read one file, app/quickstart/quickstart.mjs, for the
// commands and their output. This test checks (1) the built /quickstart page
// shows exactly those commands and outputs, in order, and (2) replaying the
// commands on a fresh clone of the commit under test prints that output. The
// clone source and the only normalisation are described in
// tests/quickstart-replay.mjs. Run `npm run build` first.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { builtPage, visibleText } from './helpers.mjs';
import { mainOf } from './tour-helpers.mjs';
import { normalise, quickstart, replay } from './quickstart-replay.mjs';

const decode = (s) => s.replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&quot;/g, '"').replace(/&#x27;|&#39;/g, "'").replace(/&amp;/g, '&');

// What a built page shows: each data-command and data-output, by step id.
export function shown(html) {
  const main = mainOf(html);
  const grab = (attr) => [...main.matchAll(new RegExp(`<(code|pre)\\b[^>]*\\s${attr}="([^"]+)"[^>]*>([\\s\\S]*?)<\\/\\1>`, 'gi'))]
    .map(([, , id, inner]) => ({ id, text: normalise(decode(inner.replace(/<[^>]+>/g, ''))) }));
  return { commands: grab('data-command'), outputs: grab('data-output') };
}

export function pageProblems(html, steps) {
  const { commands, outputs } = shown(html);
  const problems = [];
  assert.ok(steps.length >= 2, 'the quickstart has fewer than two steps');
  if (commands.map((c) => c.id).join() !== steps.map((s) => s.id).join()) problems.push(`page shows commands ${commands.map((c) => c.id)}, data has ${steps.map((s) => s.id)}`);
  for (const step of steps) {
    const c = commands.find((x) => x.id === step.id);
    if (c && c.text !== step.command) problems.push(`step ${step.id}: page shows command "${c.text}", data has "${step.command}"`);
    const o = outputs.find((x) => x.id === step.id);
    if (step.output === null) { if (o) problems.push(`step ${step.id}: page shows output the replay does not compare`); continue; }
    if (!o) problems.push(`step ${step.id}: page shows no output`);
    else if (o.text !== normalise(step.output)) problems.push(`step ${step.id}: page output differs from the data`);
  }
  return problems;
}

export function replayProblems(results, steps) {
  const problems = [];
  for (const step of steps) {
    const r = results.find((x) => x.id === step.id);
    if (!r) { problems.push(`step ${step.id} did not run`); continue; }
    if (step.output !== null && r.output !== normalise(step.output)) {
      problems.push(`step ${step.id}: replay printed\n${r.output}\n--- but the page shows\n${normalise(step.output)}`);
    }
  }
  return problems;
}

const STEPS = [
  { id: 'a', command: 'cd x', output: null },
  { id: 'b', command: 'node run', output: 'ok\nline two' },
];
const PAGE = (out = 'ok\nline two', cmd = 'node run') =>
  `<main><code data-command="a">cd x</code><code data-command="b">${cmd}</code><pre data-output="b">${out}</pre></main>`;

test('the quickstart checks catch faults (self-test)', () => {
  assert.deepEqual(pageProblems(PAGE(), STEPS), []);
  assert.ok(pageProblems(PAGE('ok'), STEPS).length, 'a page showing different output passes');
  assert.ok(pageProblems(PAGE(undefined, 'node walk'), STEPS).length, 'a page showing a different command passes');
  assert.ok(pageProblems(PAGE().replace(/<pre[\s\S]*<\/pre>/, ''), STEPS).length, 'a page missing an output passes');
  assert.deepEqual(replayProblems([{ id: 'a', output: '' }, { id: 'b', output: 'ok\nline two' }], STEPS), []);
  assert.ok(replayProblems([{ id: 'a', output: '' }, { id: 'b', output: 'ok\nline 2' }], STEPS).length, 'a replay printing other output passes');
  assert.ok(replayProblems([{ id: 'a', output: '' }], STEPS).length, 'a step that did not run passes');
  assert.throws(() => replay({ ...quickstart, steps: [{ id: 'x', command: 'echo hi | cat', output: null }] }), /not a plain command/);
});

test('/quickstart shows exactly the commands and output in app/quickstart/quickstart.mjs', () => {
  const html = builtPage('quickstart.html').html;
  assert.deepEqual(pageProblems(html, quickstart.steps), []);
  assert.match(visibleText(mainOf(html)), /Node\.js 20/, 'the page does not say which Node.js it needs');
});

test('replaying the quickstart on a fresh clone prints the output the page shows', { timeout: 120000 }, () => {
  const { results } = replay();
  assert.deepEqual(replayProblems(results, quickstart.steps), []);
});
