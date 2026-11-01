// S-013 TK-001: fixture test for the dev-vs-main drift check.
// Builds a throwaway Git repository with known drift and fixed dates, then checks
// that the report gives the exact ahead/behind counts, days and threshold result.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { execFileSync } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { measureDrift, renderReport } from './coherence-drift.mjs';

function git(cwd, args, date) {
  const env = { ...process.env, GIT_AUTHOR_NAME: 't', GIT_AUTHOR_EMAIL: 't@example.invalid', GIT_COMMITTER_NAME: 't', GIT_COMMITTER_EMAIL: 't@example.invalid' };
  if (date) { env.GIT_AUTHOR_DATE = date; env.GIT_COMMITTER_DATE = date; }
  return execFileSync('git', args, { cwd, env, encoding: 'utf8' }).trim();
}

function commit(cwd, name, date) {
  fs.writeFileSync(path.join(cwd, name), name);
  git(cwd, ['add', name]);
  git(cwd, ['commit', '-q', '-m', name], date);
}

// Fixture: base on 10/01; dev adds 3 commits from 10/10; main adds 1 commit on 10/20.
function fixture() {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'drift-'));
  git(dir, ['init', '-q', '-b', 'main']);
  commit(dir, 'base', '2026-10-01T00:00:00Z');
  git(dir, ['branch', 'dev']);
  git(dir, ['checkout', '-q', 'dev']);
  commit(dir, 'd1', '2026-10-10T00:00:00Z');
  commit(dir, 'd2', '2026-10-12T00:00:00Z');
  commit(dir, 'd3', '2026-10-15T00:00:00Z');
  git(dir, ['checkout', '-q', 'main']);
  commit(dir, 'm1', '2026-10-20T00:00:00Z');
  return dir;
}

const NOW = '2026-11-01T00:00:00Z';

test('reports known ahead and behind counts and days', () => {
  const repo = fixture();
  const r = measureDrift({ repo, base: 'main', head: 'dev', fetch: false, now: NOW, thresholdCommits: 20, thresholdDays: 14 });
  assert.equal(r.ahead.commits, 3);
  assert.equal(r.behind.commits, 1);
  // Oldest dev-only commit 10/10 -> 22 days unmerged at 11/01.
  assert.equal(r.ahead.days, 22);
  // Oldest main-only commit 10/20 -> 12 days not yet in dev.
  assert.equal(r.behind.days, 12);
  assert.equal(r.measuredAt, NOW);
  assert.match(r.baseSha, /^[0-9a-f]{40}$/);
  assert.match(r.headSha, /^[0-9a-f]{40}$/);
  // 22 days > 14-day threshold: breach on days, not on commits.
  assert.equal(r.threshold.breached, true);
  assert.deepEqual(r.threshold.reasons, ['days']);
});

test('no breach when under both thresholds', () => {
  const repo = fixture();
  const r = measureDrift({ repo, base: 'main', head: 'dev', fetch: false, now: NOW, thresholdCommits: 20, thresholdDays: 30 });
  assert.equal(r.threshold.breached, false);
  assert.deepEqual(r.threshold.reasons, []);
});

test('zero drift reports zero days', () => {
  const repo = fixture();
  const r = measureDrift({ repo, base: 'main', head: 'main', fetch: false, now: NOW, thresholdCommits: 20, thresholdDays: 14 });
  assert.equal(r.ahead.commits, 0);
  assert.equal(r.ahead.days, 0);
  assert.equal(r.threshold.breached, false);
});

test('report names time, both SHAs and counts', () => {
  const repo = fixture();
  const r = measureDrift({ repo, base: 'main', head: 'dev', fetch: false, now: NOW, thresholdCommits: 20, thresholdDays: 14 });
  const md = renderReport(r);
  assert.ok(md.includes(NOW));
  assert.ok(md.includes(r.baseSha));
  assert.ok(md.includes(r.headSha));
  assert.match(md, /ahead of `main` \| 3 \| 22/);
  assert.match(md, /BREACH/);
});
