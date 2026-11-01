#!/usr/bin/env node
// S-013 TK-001 (ADR-002T): read-only check of how far `dev` runs ahead of and
// behind `main`. Needs only `git`; no secret, no network beyond `git fetch`.
// Non-blocking (ADR-000H, S-013 contract): it always exits 0 on a measurement,
// breach or not; it exits 2 only when it cannot measure.
//
// Days = whole days from the oldest commit on one side that the other side lacks
// (committer date) to the measurement time: how long unmerged work has waited.
import { execFileSync } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import { pathToFileURL } from 'node:url';

export const DEFAULTS = Object.freeze({ remote: 'origin', base: 'main', head: 'dev', thresholdCommits: 20, thresholdDays: 7 });
const DAY_MS = 86_400_000;

function git(repo, args) {
  return execFileSync('git', args, { cwd: repo, encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'] }).trim();
}

function side(repo, from, to, nowMs) {
  const range = `${from}..${to}`;
  const commits = Number(git(repo, ['rev-list', '--count', range]));
  if (!commits) return { commits: 0, days: 0, oldest: null };
  const times = git(repo, ['log', '--format=%cI', range]).split('\n').filter(Boolean);
  const oldest = times.map((t) => Date.parse(t)).reduce((a, b) => Math.min(a, b));
  return { commits, days: Math.floor((nowMs - oldest) / DAY_MS), oldest: new Date(oldest).toISOString() };
}

export function measureDrift(options = {}) {
  const o = { ...DEFAULTS, repo: process.cwd(), fetch: true, ...options };
  if (o.fetch) git(o.repo, ['fetch', '--quiet', o.remote, o.base, o.head]);
  const ref = (b) => (o.fetch ? `${o.remote}/${b}` : b);
  const baseRef = ref(o.base);
  const headRef = ref(o.head);
  const measuredAt = o.now ?? new Date().toISOString();
  const nowMs = Date.parse(measuredAt);
  const ahead = side(o.repo, baseRef, headRef, nowMs);
  const behind = side(o.repo, headRef, baseRef, nowMs);
  const reasons = [];
  if (ahead.commits > o.thresholdCommits) reasons.push('commits');
  if (ahead.days > o.thresholdDays) reasons.push('days');
  return {
    measuredAt,
    base: o.base,
    head: o.head,
    baseRef,
    headRef,
    baseSha: git(o.repo, ['rev-parse', baseRef]),
    headSha: git(o.repo, ['rev-parse', headRef]),
    ahead,
    behind,
    threshold: { commits: o.thresholdCommits, days: o.thresholdDays, breached: reasons.length > 0, reasons },
  };
}

export function renderReport(r) {
  const t = r.threshold;
  const verdict = t.breached ? `BREACH (${t.reasons.join(', ')})` : 'within threshold';
  return [
    `# Drift report: \`${r.head}\` vs \`${r.base}\``,
    '',
    `- **Measured at (UTC):** ${r.measuredAt}`,
    `- **\`${r.base}\`:** \`${r.baseSha}\` (${r.baseRef})`,
    `- **\`${r.head}\`:** \`${r.headSha}\` (${r.headRef})`,
    `- **Threshold:** more than ${t.commits} commits or ${t.days} days ahead. **Result:** ${verdict}`,
    `- **Check:** \`node workbench/tools/coherence-drift.mjs\` (S-013 TK-001, non-blocking)`,
    '',
    '| Direction | Commits | Days | Oldest unmerged commit |',
    '|---|---|---|---|',
    `| \`${r.head}\` ahead of \`${r.base}\` | ${r.ahead.commits} | ${r.ahead.days} | ${r.ahead.oldest ?? 'none'} |`,
    `| \`${r.head}\` behind \`${r.base}\` | ${r.behind.commits} | ${r.behind.days} | ${r.behind.oldest ?? 'none'} |`,
    '',
    'Days count from the oldest commit one side lacks to the measurement time. A breach raises a Grill Board item once S-013 TK-005 lands; until then it is reported here only.',
    '',
  ].join('\n');
}

function parseArgs(argv) {
  const o = {};
  let json = false;
  let write = null;
  for (let i = 0; i < argv.length; i += 1) {
    const a = argv[i];
    const next = () => argv[++i];
    if (a === '--json') json = true;
    else if (a === '--no-fetch') o.fetch = false;
    else if (a === '--write') write = next();
    else if (a === '--repo') o.repo = next();
    else if (a === '--remote') o.remote = next();
    else if (a === '--base') o.base = next();
    else if (a === '--head') o.head = next();
    else if (a === '--now') o.now = next();
    else if (a === '--threshold-commits') o.thresholdCommits = Number(next());
    else if (a === '--threshold-days') o.thresholdDays = Number(next());
    else throw new Error(`Unknown argument: ${a}`);
  }
  return { o, json, write };
}

if (import.meta.url === pathToFileURL(process.argv[1] ?? '').href) {
  try {
    const { o, json, write } = parseArgs(process.argv.slice(2));
    const r = measureDrift(o);
    const out = json ? `${JSON.stringify(r, null, 2)}\n` : renderReport(r);
    if (write) {
      fs.mkdirSync(path.dirname(write), { recursive: true });
      fs.writeFileSync(write, out);
    }
    process.stdout.write(out);
  } catch (error) {
    process.stderr.write(`coherence-drift: ${error.message}\n`);
    process.exit(2);
  }
}
