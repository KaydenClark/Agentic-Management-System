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
import { normalise, quickstart, readerEnv, replay } from './quickstart-replay.mjs';

const decode = (s) => s.replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&quot;/g, '"').replace(/&#x27;|&#39;/g, "'").replace(/&amp;/g, '&');

// Each data-exit element's step id and the exit status it states.
const grabExit = (main) => [...main.matchAll(/<(\w+)\b[^>]*\sdata-exit="([^"]+)"[^>]*>([\s\S]*?)<\/\1>/gi)]
  .map(([, , id, inner]) => ({ id, status: Number((decode(inner.replace(/<[^>]+>/g, '')).match(/exit status (\d+)/) ?? [])[1]) }));

// What a built page shows: each data-command, data-output and data-exit, by step id.
export function shown(html) {
  const main = mainOf(html);
  const grab = (attr) => [...main.matchAll(new RegExp(`<(code|pre)\\b[^>]*\\s${attr}="([^"]+)"[^>]*>([\\s\\S]*?)<\\/\\1>`, 'gi'))]
    .map(([, , id, inner]) => ({ id, text: normalise(decode(inner.replace(/<[^>]+>/g, ''))) }));
  return { commands: grab('data-command'), outputs: grab('data-output'), exits: grabExit(main) };
}

export function pageProblems(html, steps) {
  const { commands, outputs, exits } = shown(html);
  const problems = [];
  assert.ok(steps.length >= 2, 'the quickstart has fewer than two steps');
  if (commands.map((c) => c.id).join() !== steps.map((s) => s.id).join()) problems.push(`page shows commands ${commands.map((c) => c.id)}, data has ${steps.map((s) => s.id)}`);
  for (const step of steps) {
    const c = commands.find((x) => x.id === step.id);
    if (c && c.text !== step.command) problems.push(`step ${step.id}: page shows command "${c.text}", data has "${step.command}"`);
    const expected = step.exitCode ?? 0;
    const e = exits.filter((x) => x.id === step.id);
    if (expected !== 0 && (e.length !== 1 || e[0].status !== expected)) problems.push(`step ${step.id}: page does not show exactly one data-exit stating exit status ${expected}`);
    if (expected === 0 && e.length) problems.push(`step ${step.id}: page shows an exit status for a step that succeeds`);
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
    if ((r.exitCode ?? 0) !== (step.exitCode ?? 0)) problems.push(`step ${step.id}: replay ended with exit status ${r.exitCode}, the page shows ${step.exitCode ?? 0}`);
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
  assert.ok(replayProblems([{ id: 'a', output: '', exitCode: 0 }, { id: 'b', output: 'ok\nline two', exitCode: 1 }], STEPS).length, 'a replay ending with an exit status the page does not show passes');
  const FAILS = [STEPS[0], { ...STEPS[1], exitCode: 1 }];
  assert.ok(replayProblems([{ id: 'a', output: '', exitCode: 0 }, { id: 'b', output: 'ok\nline two', exitCode: 0 }], FAILS).length, 'a replay succeeding where the page shows a failure passes');
  assert.deepEqual(replayProblems([{ id: 'a', output: '', exitCode: 0 }, { id: 'b', output: 'ok\nline two', exitCode: 1 }], FAILS), []);
  assert.ok(pageProblems(PAGE(), FAILS).length, 'a page hiding a non-zero exit status passes');
  assert.deepEqual(pageProblems(PAGE().replace('</main>', '<p data-exit="b">exit status 1</p></main>'), FAILS), []);
  assert.ok(pageProblems(PAGE().replace('</main>', '<p data-exit="b">exit status 2</p></main>'), FAILS).length, 'a page showing the wrong exit status passes');
  assert.ok(pageProblems(PAGE().replace('</main>', '<p data-exit="b">exit status 1</p></main>'), STEPS).length, 'a page showing a failure for a step that succeeds passes');
  const env = readerEnv('/tmp/reader-home', { HOME: '/Users/someone', USERPROFILE: 'C:\\Users\\someone', WORKBENCH_SKILLS_ROOT: '/skills', PATH: '/bin' });
  assert.deepEqual(env, { HOME: '/tmp/reader-home', USERPROFILE: '/tmp/reader-home', PATH: '/bin' }, 'the replay can see a personal skill catalog');
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
