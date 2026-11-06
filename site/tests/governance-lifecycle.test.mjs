import { test } from 'node:test';
import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { readFileSync } from 'node:fs';
import { TASK_STATUSES } from '../../workbench/tools/task-record.mjs';
import chart from '../content/governance/task-lifecycle.json' with { type: 'json' };

// These sources implement Task state writes. A change requires re-inspection of
// every transition below; a fingerprint is not itself proof of correctness.
const sources = {
  'task-record.mjs': 'cf33e729619e1ca7eef15fff684e8df754e40104e4dad014074aba431efe9d8a',
  'spec-workbench.mjs': '7610b38a04af2f9996455a814b3d5454dbd75464ad79c5f573028029eecb78a5',
  'spec-report.mjs': 'e0e7ae8ff8d89319f67952559d5713c0082288d305681738181b2952f4f17a30',
};
const runtimeEdges = [
  ['ready', 'in-progress'], ['ready', 'blocked'], ['blocked', 'in-progress'],
  ['in-progress', 'blocked'], ['in-progress', 'done'], ['done', 'ready'],
];
const sorted = values => [...values].sort();
function check(candidate) {
  assert.deepEqual(sorted(candidate.states), sorted(TASK_STATUSES));
  assert.deepEqual(sorted(candidate.transitions.map(({from, to}) => `${from}:${to}`)),
    sorted(runtimeEdges.map(([from, to]) => `${from}:${to}`)));
}
test('Task lifecycle agrees with the inspected runtime', () => {
  for (const [file, expected] of Object.entries(sources)) {
    const actual = createHash('sha256').update(readFileSync(new URL(`../../workbench/tools/${file}`, import.meta.url))).digest('hex');
    assert.equal(actual, expected, `${file} changed: inspect its transitions before updating the chart`);
  }
  check(chart);
});
test('unknown or missing states and edges are rejected', () => {
  assert.throws(() => check({...chart, states: [...chart.states, 'unknown']}));
  assert.throws(() => check({...chart, states: chart.states.slice(1)}));
  assert.throws(() => check({...chart, transitions: [...chart.transitions, {from:'ready', to:'done'}]}));
  assert.throws(() => check({...chart, transitions: chart.transitions.slice(1)}));
});
