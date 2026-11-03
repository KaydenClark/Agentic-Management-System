import './tsx-register.mjs';
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { createElement } from 'react';
import { renderToStaticMarkup } from 'react-dom/server';
import { readFile } from 'node:fs/promises';

const { RepairEvidence } = await import('../app/rsi/repair.tsx');
const { repairEvidence } = await import('../app/rsi/repair-data.ts');
const html = () => renderToStaticMarkup(createElement(RepairEvidence));

test('actual development predicates have linked counts and never become an Alignment score', () => {
  assert.deepEqual(repairEvidence.baseline.runs.map(r => [r.passed, r.checks]), [[9, 11], [10, 11], [10, 11]]);
  const out = html();
  assert.equal((out.match(/data-predicate-run=/g) ?? []).length, 3);
  assert.match(out, /not an Alignment Score/);
  assert.match(out, /Source-injected/);
  assert.match(out, /effort high/);
  assert.match(out, /consecutive-Task behavior remains untested/);
  for (const run of repairEvidence.baseline.runs) {
    assert.ok(out.includes(`href="${run.source}"`));
    assert.ok(out.includes(`${run.passed} of ${run.checks}`));
  }
});

test('missing audit and installation evidence has no fabricated score or accepted disposition', () => {
  const out = html();
  assert.match(out, /Candidate comparison pending/);
  assert.match(out, /Audit pending/);
  assert.match(out, /Installation and later use pending/);
  assert.ok(!out.includes('data-audit-score'));
  assert.match(out, /No demonstrated improvement/);
  assert.match(out, /authority interpretation remains unqualified/);
});

test('the actual failed candidate and incomplete audit remain visible without becoming accepted evidence', () => {
  assert.deepEqual(repairEvidence.candidate.runs.map(r => [r.passed, r.checks]), [[9, 11], [8, 11], [7, 11]]);
  assert.equal(repairEvidence.candidate.audit.qualification, 'unqualified');
  const out = html();
  assert.equal((out.match(/data-candidate-run=/g) ?? []).length, 3);
  assert.match(out, /Broken, 11 of 78 applicable checks passed/);
  assert.match(out, /earlier provisional workflow tally was 6 of 78/);
  assert.match(out, /Evidence is incomplete/);
  assert.match(out, /Not accepted for merge or installation/);
  assert.match(out, /do not establish source cause or a qualified regression/);
  assert.ok(out.includes(repairEvidence.candidate.source));
});

test('the separate pruning suite retains goal misses and its own incomplete audit denominator', () => {
  assert.deepEqual(repairEvidence.pruning.observations.map(r => [r.before, r.after]), [[2983, 2897], [1142, 1065], [793, 708], [343, 218]]);
  const out = html();
  assert.match(out, /Broken, 6 of 51 applicable checks passed/);
  assert.match(out, /earlier provisional pruning tally was 3 of 51/);
  assert.match(out, /Target unmet/);
  assert.match(out, /Approximate goal missed/);
  assert.match(out, /counts are not pooled/);
  assert.match(out, /not full semantic/);
});

test('the distinct documentation failure retains failed attempts, target and ceiling with source links', () => {
  assert.deepEqual(repairEvidence.documentation.observations.map(r => r.characters), [2983, 3336, 3116, 3036, 3025, 1193]);
  const out = html();
  assert.match(out, /900–1500/);
  assert.match(out, /3000/);
  assert.match(out, /separate from the frozen skill comparison/);
  for (const observation of repairEvidence.documentation.observations) assert.ok(out.includes(`href="${observation.source}"`));
});

test('safe feed contains no raw session, host paths, prompt or private skill source', () => {
  const out = html();
  assert.doesNotMatch(out, /\/Users\/|\/private\/|session_0|github\.com\/KaydenClark\/skills|raw\.githubusercontent/);
  assert.match(out, /Development evidence/);
  assert.match(out, /not native activation/);
});

test('RSI page introduces itself before repair evidence and trial charts', async () => {
  const { RsiView } = await import('../app/rsi/view.tsx');
  const { seriesViews } = await import('../app/rsi/data.ts');
  const out = renderToStaticMarkup(createElement(RsiView, {
    views: seriesViews({ runs: [], results: [] }), unavailable: false,
  }, createElement(RepairEvidence)));
  const title = out.indexOf('<h1>RSI results</h1>');
  const repair = out.indexOf('id="repair-title"');
  const trials = out.indexOf('id="rsi-split-held-out"');
  assert.ok(title >= 0 && repair > title && trials > repair,
    'page title must precede repair evidence, followed by trial charts');
});

test('RSI repair evidence heading covers tool repair and earlier skill delivery work', () => {
  const out = html();
  assert.match(out, /id="repair-title">Project tools and shared-skill repair evidence</);
  assert.match(out, /bounded checker repair to AMS project tooling alongside earlier shared-skill delivery attempts/);
});

test('checker repair evidence shows the sourced false-met case and bounded disposition', () => {
  const out = html();
  assert.match(out, /false <code>met<\/code>/);
  assert.match(out, /reports checked criteria as <code>unknown<\/code>/);
  assert.match(out, /three false <code>met<\/code> results/);
  assert.match(out, /33 focused checks passed/);
  assert.match(out, /809 passed, 5 skipped, 1 failed/);
  assert.match(out, /inherited AGENTS\.md length check/);
  assert.match(out, /not a checker assertion/);
  assert.match(out, /included in recovery assembly/);
  assert.match(out, /Task is closed/);
  assert.match(out, /Current combined recovery checks and review status/);
  assert.match(out, /recovery PR 139/);
  assert.doesNotMatch(out, /candidate is awaiting assembly|assembled checks remain pending/);
  assert.match(out, /S-001 returned 0 met, 6 not met, 2 unknown/);
  assert.match(out, /S-003 it returned 0 met, 8 not met, 0 unknown/);
  assert.match(out, /required owner and root intervention/);
  assert.match(out, /not evidence of a fully autonomous end-to-end learning cycle/);
  assert.ok(out.includes(repairEvidence.checker.report));
  assert.ok(out.includes(repairEvidence.checker.source));
  assert.ok(out.includes(repairEvidence.checker.assemblySource));
  assert.ok(out.includes(repairEvidence.checker.recoveryPR));
  assert.ok(out.includes(repairEvidence.checker.baselineSource));
  assert.ok(out.includes(repairEvidence.checker.fixtureSource));
  assert.ok(out.includes(repairEvidence.checker.candidateSource));
  assert.ok(!out.includes('data-audit-score'));
});

test('orientation page copy describes Specs as destinations and distinguishes working tools from assembled RSI', async () => {
  const how = await readFile(new URL('../app/how-it-works/page.tsx', import.meta.url), 'utf8');
  const start = await readFile(new URL('../app/start/page.tsx', import.meta.url), 'utf8');
  for (const out of [how, start]) {
    assert.match(out, /Spec.{0,150}bounded destination/s);
    assert.match(out, /Tasks.{0,180}(plan and carry out execution|plans execution)/s);
    assert.match(out, /Workbench Node lifecycle/);
    assert.match(out, /Python command-line tools/);
    assert.match(out, /assembled RSI/);
    assert.doesNotMatch(out, /runtime software does not exist/);
    assert.doesNotMatch(out, /written plan for a change/);
  }
});
