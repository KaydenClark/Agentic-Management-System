import './tsx-register.mjs';
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { createElement } from 'react';
import { renderToStaticMarkup } from 'react-dom/server';

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
