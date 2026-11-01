// npm run build: `next build` with draft marks applied (S-003 TK-004).
// Pass 1 builds with no page approved, so every page carries its draft mark,
// and matches each built page's content hash against approvals.json. If any
// approval matches, pass 2 rebuilds with AMS_APPROVED_ROUTES naming those
// routes; the build fails unless every hash is unchanged and the built output
// agrees with the approvals. Writes .next/draft-marks.json.
import { spawnSync } from 'node:child_process';
import { createRequire } from 'node:module';
import { writeFileSync } from 'node:fs';
import { join } from 'node:path';
import { approvedRoutes, contentHash, hasDraftMark, markProblems, readApprovals, readBuiltPages, siteDir, validateApprovals } from './draft-marks.mjs';

const nextBin = createRequire(join(siteDir, 'package.json')).resolve('next/dist/bin/next');

function fail(message) {
  console.error(`draft marks: ${message}`);
  process.exit(1);
}

function nextBuild(routes) {
  const r = spawnSync(process.execPath, [nextBin, 'build'], {
    cwd: siteDir,
    stdio: 'inherit',
    env: { ...process.env, AMS_APPROVED_ROUTES: JSON.stringify(routes) },
  });
  if (r.status !== 0) process.exit(r.status ?? 1);
  return readBuiltPages().map((p) => ({ ...p, hash: contentHash(p.html) }));
}

const doc = readApprovals();
const invalid = validateApprovals(doc);
if (invalid.length) fail(`approvals.json is invalid:\n  ${invalid.join('\n  ')}`);
const records = doc.approvals;

let pages = nextBuild([]);
const approved = approvedRoutes(pages, records);
const firstHash = new Map(pages.map((p) => [p.route, p.hash]));

for (const a of records) {
  if (!firstHash.has(a.route)) console.log(`draft marks: the approval for ${a.route} names no built page`);
  else if (firstHash.get(a.route) !== a.hash) console.log(`draft marks: the approval for ${a.route} at ${a.hash} does not match its current hash ${firstHash.get(a.route)}; it stays a draft`);
}

if (approved.size) {
  console.log(`draft marks: rebuilding with ${[...approved].join(', ')} approved`);
  pages = nextBuild([...approved]);
  for (const p of pages) {
    if (firstHash.get(p.route) !== p.hash) fail(`${p.route} changed content between builds (${firstHash.get(p.route)} -> ${p.hash})`);
  }
}

const problems = markProblems(pages, records);
if (problems.length) fail(`built output disagrees with approvals.json:\n  ${problems.join('\n  ')}`);

const report = pages.map((p) => ({ route: p.route, hash: p.hash, status: hasDraftMark(p.html) ? 'draft' : 'approved' }));
writeFileSync(join(siteDir, '.next', 'draft-marks.json'), `${JSON.stringify({ pages: report }, null, 2)}\n`);
for (const p of report) console.log(`draft marks: ${p.status.padEnd(8)} ${p.route} ${p.hash}`);
