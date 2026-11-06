import { test } from 'node:test';
import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { readFileSync } from 'node:fs';
import charts from '../content/governance/spec-flows.json' with { type: 'json' };

const root = new URL('../../', import.meta.url);
const pinned = {
  'workbench/tools/spec-workbench.mjs': '7610b38a04af2f9996455a814b3d5454dbd75464ad79c5f573028029eecb78a5',
  'workbench/tools/spec-report.mjs': 'e0e7ae8ff8d89319f67952559d5713c0082288d305681738181b2952f4f17a30',
  'workbench/docs/adr/001J-the-workflow-map.md': '5720af500bafad17ff5b14cf6b4006be4c9a888e28ad01af2c79ba39ccb3a670',
  'workbench/wiki/vocabulary-workflow-verbs.md': '421ed363768bab595edf168e2c6cc95ec07da353eb8629f32e9e2da9fd409671',
};
const read = path => readFileSync(new URL(path, root), 'utf8');
const sort = items => [...items].sort();
const edgeKeys = edges => edges.map(({from,to}) => `${from}:${to}`);
const observed = read('workbench/tools/spec-workbench.mjs').match(/const SPEC_STATUSES = new Set\(\[([^\]]+)\]\)/)?.[1];
assert.ok(observed, 'cannot locate the runtime Spec status set');
const specStates = [...observed.matchAll(/'([^']+)'/g)].map(match => match[1]);
// Source fingerprints make these audited handler paths a mandatory reinspection
// point, rather than presenting a copied transition model as runtime execution.
const specEdges = ['planned:active', 'active:complete', 'needs-review:complete'];
const reviewStages = ['Candidate', 'Independent review', 'Verify', 'Corrective work', 'New candidate', 'Owner QA'];
const reviewEdges = ['Candidate:Independent review', 'Independent review:Corrective work', 'Corrective work:New candidate', 'New candidate:Independent review', 'Independent review:Verify', 'Verify:Owner QA', 'Owner QA:Corrective work'];
function check(chart, states, edges) {
  assert.deepEqual(sort(chart.states), sort(states));
  assert.deepEqual(sort(edgeKeys(chart.transitions)), sort(edges));
}
function faults(chart, states, edges) {
  assert.throws(() => check({...chart, states:[...chart.states,'unknown']},states,edges));
  assert.throws(() => check({...chart, states:chart.states.slice(1)},states,edges));
  assert.throws(() => check({...chart, transitions:[...chart.transitions,{from:'unknown',to:'unknown'}]},states,edges));
  assert.throws(() => check({...chart, transitions:chart.transitions.slice(1)},states,edges));
}
test('Spec states and audited transitions stay bound to native sources', () => {
  for (const [file, expected] of Object.entries(pinned)) assert.equal(createHash('sha256').update(read(file)).digest('hex'), expected, `${file} changed; re-audit the charts`);
  check(charts.spec, specStates, specEdges);
});
test('workflow stages and return paths stay complete', () => {
  const stages = ['Explore','Promote','Prepare','Journey','Judge','Complete'];
  const adr = read('workbench/docs/adr/001J-the-workflow-map.md');
  let previous = -1;
  for (const stage of stages) { const position = adr.indexOf(stage, previous + 1); assert.ok(position > previous, `${stage} missing or out of order`); previous = position; }
  const edges = stages.slice(1).map((to, i) => `${stages[i]}:${to}`);
  check(charts.delivery, stages, edges);
  check(charts.review, reviewStages, reviewEdges);
});
test('missing or unknown states and arrows fail all three diagrams', () => {
  faults(charts.spec, specStates, specEdges);
  const stages=['Explore','Promote','Prepare','Journey','Judge','Complete'];
  faults(charts.delivery, stages, stages.slice(1).map((to,i)=>`${stages[i]}:${to}`));
  faults(charts.review, reviewStages, reviewEdges);
});
