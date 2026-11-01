// Shared helpers for the build-output tests. Run `npm run build` first:
// these tests read the prerendered HTML Next writes to .next/server/app/.
import { execFileSync } from 'node:child_process';
import { existsSync, readdirSync, readFileSync, statSync } from 'node:fs';
import { join, relative } from 'node:path';
import { fileURLToPath } from 'node:url';

export const siteDir = fileURLToPath(new URL('..', import.meta.url));
export const appOut = join(siteDir, '.next', 'server', 'app');

// Next's own fallback for errors thrown in the root layout; it does not use
// the shell, so it is not a page a reader navigates to.
const NOT_A_PAGE = new Set(['_global-error.html']);

function walk(dir, keep) {
  const out = [];
  for (const name of readdirSync(dir)) {
    const path = join(dir, name);
    if (statSync(path).isDirectory()) out.push(...walk(path, keep));
    else if (keep(path)) out.push(path);
  }
  return out;
}

export function builtPages() {
  if (!existsSync(appOut)) throw new Error('No build output: run `npm run build` in site/ before `npm test`.');
  return walk(appOut, (p) => p.endsWith('.html') && !NOT_A_PAGE.has(relative(appOut, p)))
    .map((path) => ({ path, name: relative(appOut, path), html: readFileSync(path, 'utf8') }));
}

export function builtPage(name) {
  const page = builtPages().find((p) => p.name === name);
  if (!page) throw new Error(`Built page ${name} not found in ${appOut}`);
  return page;
}

// The commit the build is expected to show: Vercel's build variable when set,
// else the checkout's HEAD. Written independently of the site's resolver so a
// broken resolver cannot pass its own test.
export function expectedCommit() {
  if (process.env.VERCEL_GIT_COMMIT_SHA) return process.env.VERCEL_GIT_COMMIT_SHA;
  return execFileSync('git', ['rev-parse', 'HEAD'], { cwd: siteDir, encoding: 'utf8' }).trim();
}

export function sourceFiles(dir, exts) {
  const root = join(siteDir, dir);
  if (!existsSync(root)) return [];
  return walk(root, (p) => exts.some((e) => p.endsWith(e)))
    .map((path) => ({ path, name: relative(siteDir, path), text: readFileSync(path, 'utf8') }));
}

// Visible text of an HTML fragment, with scripts and styles removed.
export function visibleText(html) {
  return html
    .replace(/<script[\s\S]*?<\/script>/gi, ' ')
    .replace(/<style[\s\S]*?<\/style>/gi, ' ')
    .replace(/<[^>]+>/g, ' ')
    .replace(/&amp;/g, '&').replace(/&#x27;|&#39;/g, "'").replace(/&quot;/g, '"')
    .replace(/\s+/g, ' ')
    .trim();
}
