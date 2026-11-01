// S-003 TK-004 end-to-end draft-mark check: real `npm run build` runs on a
// temporary copy of site/ (the checkout's own files are never edited). The
// copy is a hidden .draft-marks-check-* folder inside site/ without its own
// lockfile, so Turbopack resolves packages from site/node_modules.
//   1. No approvals: every page shows the draft mark.
//   2. A fixture approval bound to the home page's hash, plus one with a wrong
//      hash for /how-it-works: home loses its mark, every other page keeps it.
//   3. One character of the home page's source changed: home's hash changes
//      and its mark is back, though the approval record is unchanged.
// Four `next build` runs; takes a few minutes. Not part of `npm test`.
// Usage: node tests/draft-marks-build.check.mjs   (npm run check:draft-marks)
import { execFileSync } from 'node:child_process';
import { cpSync, existsSync, mkdtempSync, readFileSync, readdirSync, rmSync, statSync, writeFileSync } from 'node:fs';
import { join, relative } from 'node:path';
import { fileURLToPath } from 'node:url';
import { contentHash, hasDraftMark, markProblems, routeOf } from '../scripts/draft-marks.mjs';

const siteDir = fileURLToPath(new URL('..', import.meta.url));
const PREFIX = '.draft-marks-check-';
const SKIP = new Set(['node_modules', '.next', '.vercel', 'package-lock.json']);
const ZERO = `sha256:${'0'.repeat(64)}`;
const SOURCE = 'https://github.com/KaydenClark/Agentic-Management-System/blob/dev/site/tests/fixtures/draft-marks/approvals.json';

let failures = 0;
function check(name, ok, detail = '') {
  console.log(`${ok ? 'PASS' : 'FAIL'} ${name}${detail ? ` (${detail})` : ''}`);
  if (!ok) failures += 1;
}

function walk(dir) {
  return readdirSync(dir).flatMap((n) => {
    const p = join(dir, n);
    return statSync(p).isDirectory() ? walk(p) : [p];
  });
}

function built(copy) {
  const out = join(copy, '.next', 'server', 'app');
  return walk(out)
    .filter((p) => p.endsWith('.html') && !p.endsWith('_global-error.html'))
    .map((p) => {
      const html = readFileSync(p, 'utf8');
      return { route: routeOf(relative(out, p)), html, hash: contentHash(html), marked: hasDraftMark(html) };
    });
}

function build(copy, label) {
  console.log(`-- npm run build (${label})`);
  execFileSync('npm', ['run', 'build'], { cwd: copy, stdio: ['ignore', 'inherit', 'inherit'], env: { ...process.env, NEXT_TELEMETRY_DISABLED: '1' } });
  return built(copy);
}

function writeApprovals(copy, approvals) {
  writeFileSync(join(copy, 'approvals.json'), `${JSON.stringify({ about: 'Fixture approvals for the draft-mark build check only.', approvals }, null, 2)}\n`);
}

if (!existsSync(join(siteDir, 'node_modules'))) throw new Error('Run `npm ci` in site/ first.');
const copy = mkdtempSync(join(siteDir, PREFIX));
try {
  for (const name of readdirSync(siteDir)) {
    if (!SKIP.has(name) && !name.startsWith(PREFIX)) cpSync(join(siteDir, name), join(copy, name), { recursive: true });
  }

  writeApprovals(copy, []);
  const first = build(copy, 'no approvals');
  check('built pages found', first.length >= 4, `${first.length} pages`);
  check('no approvals: every page shows the draft mark', first.every((p) => p.marked), first.filter((p) => !p.marked).map((p) => p.route).join(', '));

  const home = first.find((p) => p.route === '/');
  const approvals = [
    { route: '/', hash: home.hash, approver: 'fixture-owner', date: '2026-11-01', source: SOURCE },
    { route: '/how-it-works', hash: ZERO, approver: 'fixture-owner', date: '2026-11-01', source: SOURCE },
  ];
  writeApprovals(copy, approvals);
  const second = build(copy, 'fixture approval for / at its hash');
  const home2 = second.find((p) => p.route === '/');
  check('approval at the hash: home has no draft mark', !home2.marked);
  check('approval at the hash: home content hash unchanged by removing the mark', home2.hash === home.hash, `${home.hash} -> ${home2.hash}`);
  check('wrong-hash approval: /how-it-works keeps its draft mark', second.find((p) => p.route === '/how-it-works')?.marked === true);
  check('every other page keeps its draft mark', second.filter((p) => p.route !== '/').every((p) => p.marked));
  check('built output agrees with the approvals', markProblems(second, approvals).length === 0, markProblems(second, approvals).join('; '));

  const pageFile = join(copy, 'app', 'page.tsx');
  const source = readFileSync(pageFile, 'utf8');
  const edited = source.replace('Each piece of work', 'each piece of work');
  check('home source edited by one character', edited !== source && edited.length === source.length);
  writeFileSync(pageFile, edited);
  const third = build(copy, 'home edited, approval unchanged');
  const home3 = third.find((p) => p.route === '/');
  check('edited home: content hash changed', home3.hash !== home.hash);
  check('edited home: draft mark restored', home3.marked);
  check('edited home: no page lost its mark', third.every((p) => p.marked));
  check('built output agrees with the approvals after the edit', markProblems(third, approvals).length === 0, markProblems(third, approvals).join('; '));
} finally {
  rmSync(copy, { recursive: true, force: true });
}

console.log(failures ? `${failures} draft-mark build check(s) failed` : 'draft-mark build checks passed');
process.exit(failures ? 1 : 0);
