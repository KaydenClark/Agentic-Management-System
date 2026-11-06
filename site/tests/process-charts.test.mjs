import { test } from 'node:test';
import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { readFileSync } from 'node:fs';
import charts from '../content/governance/process-charts.json' with { type:'json' };
import { builtPage, visibleText } from './helpers.mjs';

const root = new URL('../../', import.meta.url);
const sources = {
  'RUNBOOK.md':'b34c35c177c4598bf230ff18c16f317245392d608270ef872b7bea55eeb1ef6a',
  'workbench/docs/adr/002Z-three-orchestrators-split-the-work-by-risk.md':'9c899a47bfef64a263239100af8b637bd79b7e4fe93c7e4fb495d1fe71041866',
  'workbench/docs/adr/003H-supabase-holds-the-rsi-data-and-the-service-key-stays-local.md':'d3842d1b96f1f926fee82dc0a2412f785e4ae42b87b3658757ac2055251b52f9',
  'workbench/wiki/context-owner-answers-coherence.md':'30f12e2cc7ef609593f3606d991737cc95401cf060ae62e3f1345777b730e638',
  'workbench/landmarks/LMK-004-rsi-loop-during-build/specs/S-002-rsi-loop/SPEC.md':'ba7d5baa57e4715bed46a28e183c7f04d04ecaaabbe734705a344fd592ae3153',
};
const read = path => readFileSync(new URL(path,root),'utf8');
const rsiSource = 'workbench/wiki/context-feedback-improvement-loop-plan.md';
// These exact revisions were independently audited against the diagram. New revisions require re-audit.
const rsiDigests = new Set([
  '6d1f8a40507f458a311dfcdb50895f5a98454a6340d443ed26695d0931487b34',
  '62b11ce4fd248e8048f45e595e05c2ee9fc4ae4a07fdd060cc2b138df0b1b6f7',
]);
export function checkRsiMeaning(text) {
  assert.match(text, /initial attempt → retry → retry → stop, baseline excluded/i);
  assert.match(text, /repairs or renames reset no counter or stopped campaign/i);
  assert.match(text, /Adoption and later observed use are distinct from source publication/i);
  assert.match(text, /Merge, installation, observed loading, Human QA and website promotion retain separate authority/i);
}
export function checkRsiSource(text) {
  const digest = createHash('sha256').update(text).digest('hex');
  assert.ok(rsiDigests.has(digest), `${rsiSource} changed; re-audit chart meaning`);
  checkRsiMeaning(text);
}
const expected = {
  branches:{states:['Website feature','Checked dev','Main','Non-site feature'], edges:['Website feature:Checked dev','Checked dev:Main','Non-site feature:Main']},
  responsibilities:{states:['A: Website','B: Local work','C: Coherence','Site and presentation','Local Python writer','Independent checks'], edges:['A: Website:Site and presentation','B: Local work:Local Python writer','C: Coherence:Independent checks']},
  rsi:{states:['Observed friction','Diagnosis','Bounded change','Qualified comparison','Disposition','No adoption','Authorized adoption','Later use','Baseline 0','Attempt 1','Attempt 2','Attempt 3','Stop'], edges:['Observed friction:Diagnosis','Diagnosis:Bounded change','Bounded change:Qualified comparison','Qualified comparison:Disposition','Disposition:No adoption','Disposition:Authorized adoption','Authorized adoption:Later use','Baseline 0:Attempt 1','Attempt 1:Attempt 2','Attempt 2:Attempt 3','Attempt 3:Stop']},
};
const sort = a=>[...a].sort();
function check(chart, want) {
  assert.deepEqual(sort(chart.states),sort(want.states));
  assert.deepEqual(sort(chart.transitions.map(({from,to})=>`${from}:${to}`)),sort(want.edges));
  assert.ok(chart.transitions.every(edge=>typeof edge.action==='string' && edge.action.trim()));
}
function planted(chart,want) {
  assert.throws(()=>check({...chart,states:[...chart.states,'Unknown']},want));
  assert.throws(()=>check({...chart,states:chart.states.slice(1)},want));
  assert.throws(()=>check({...chart,transitions:[...chart.transitions,{from:'Unknown',to:'Unknown',action:'x'}]},want));
  assert.throws(()=>check({...chart,transitions:chart.transitions.slice(1)},want));
}
test('audited process charts stay bound to their source contracts',()=>{
  for(const [file,hash] of Object.entries(sources)) assert.equal(createHash('sha256').update(read(file)).digest('hex'),hash,`${file} changed; re-audit chart meaning`);
  assert.match(read('RUNBOOK.md'), /Site: feature -> checked dev; only owner merges dev -> main/);
  assert.match(read('workbench/wiki/context-owner-answers-coherence.md'), /Orchestrator C keeps them attached and never uses them/);
  assert.match(read('workbench/landmarks/LMK-004-rsi-loop-during-build/specs/S-002-rsi-loop/SPEC.md'), /Baseline 0: no strike/);
  checkRsiSource(read(rsiSource));
  for(const key of Object.keys(expected)) check(charts[key],expected[key]);
});
test('RSI source guard rejects unknown bytes and changed workflow meaning',()=>{
  const source=read(rsiSource);
  assert.throws(()=>checkRsiSource(source+'\nunknown change'));
  const changed=source.replace('initial attempt → retry → retry → stop, baseline excluded', 'initial attempt → retry indefinitely');
  assert.notEqual(changed,source);
  assert.throws(()=>checkRsiMeaning(changed));
  assert.throws(()=>checkRsiSource(changed));
});
test('process charts reject added and omitted states and arrows',()=>{
  for(const key of Object.keys(expected)) planted(charts[key],expected[key]);
  assert.throws(()=>check({...charts.rsi,transitions:charts.rsi.transitions.filter(e=>e.to!=='No adoption')},expected.rsi));
});
const inventory=['governance','task','spec','delivery','review','branches','responsibilities','rsi'];
function inventoryProblems(html) {
  const figures=[...html.matchAll(/<figure\b[^>]*data-chart="([^"]+)"[^>]*>([\s\S]*?)<\/figure>/g)];
  const found=figures.map(m=>m[1]);
  const counts={governance:6,task:6,spec:3,delivery:5,review:8,branches:3,responsibilities:3,rsi:11};
  const problems=[];
  if(JSON.stringify(sort(found))!==JSON.stringify(sort(inventory))) problems.push(`expected exactly eight chart identities, found ${found.join(', ')}`);
  for(const [,name,body] of figures) if((body.match(/<li\b/g)??[]).length!==counts[name]) problems.push(`${name}: missing or extra content`);
  const nav=html.match(/<nav\b[^>]*aria-label="Chart inventory"[^>]*>([\s\S]*?)<\/nav>/)?.[1] ?? '';
  const targets=['governance-stack','task-states','spec-states','delivery-flow','review-flow','branch-flow','responsibility-flow','rsi-flow'];
  const links=[...nav.matchAll(/href="#([^"]+)"/g)].map(m=>m[1]);
  if(JSON.stringify(sort(links))!==JSON.stringify(sort(targets))) problems.push('chart links missing or extra');
  for(const id of targets) if(!new RegExp(`\\bid="${id}"`).test(html)) problems.push(`missing target ${id}`);
  return problems;
}
test('built page has the complete chart inventory exactly once',()=>{
  const html=builtPage('governance.html').html;
  assert.deepEqual(inventoryProblems(html),[]);
  assert.ok(inventoryProblems(html.replace('data-chart="branches"','data-chart="missing"')).length);
  assert.ok(inventoryProblems(html.replace('data-chart="rsi"','data-chart="branches"')).length);
  assert.ok(inventoryProblems(html.replace('data-chart="rsi"','data-chart="extra"')).length);
  assert.ok(inventoryProblems(html.replace(/(<figure[^>]*data-chart="branches"[^>]*>)[\s\S]*?(<\/figure>)/, '$1$2')).length);
  assert.ok(inventoryProblems(html.replace('href="#rsi-flow"','href="#wrong"')).length);
});

function boundaryProblems(html) {
  const text=visibleText(html), problems=[];
  for(const phrase of ['Only the owner promotes dev to main', 'C never uses the shared connectors', 'Python writer owns protected RSI data writes', 'Baseline 0 is excluded', 'do not reset the same exhausted improvement chain', 'does not demonstrate an autonomous loop']) if(!text.includes(phrase)) problems.push(`missing boundary: ${phrase}`);
  return problems;
}
test('built charts retain owner, connector and attempt boundaries',()=>{
  const html=builtPage('governance.html').html;
  assert.deepEqual(boundaryProblems(html),[]);
  assert.ok(boundaryProblems(html.replace('Only the owner promotes dev to main','Anyone promotes dev to main')).length);
  assert.ok(boundaryProblems(html.replace('C never uses the shared connectors','C uses the shared connectors')).length);
  assert.ok(boundaryProblems(html.replace('Baseline 0 is excluded','Baseline 0 is included')).length);
});
