// Isolated synthetic build fixtures exercise the real reader and copied CLI.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { copyFileSync, mkdirSync, mkdtempSync, readFileSync, readdirSync, renameSync, rmSync, symlinkSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { contentHash, readBuiltPages } from '../scripts/page-hash.mjs';
import { readBuild } from '../scripts/page-inventory.mjs';

const artifacts = [
  ['index.html', '/page', '/'],
  ['skills.html', '/skills/page', '/skills'],
  ['skills/alpha.html', '/skills/[name]/page', '/skills/alpha'],
  ['_not-found.html', '/_not-found/page', '/_not-found'],
  ['_global-error.html', '/_global-error/page', '/_global-error'],
];
function fixture() {
  const site = mkdtempSync(join(tmpdir(), 'ams-page-artifacts-'));
  const put = (name, data) => { const file = join(site, name); mkdirSync(join(file, '..'), { recursive: true }); writeFileSync(file, data); return file; };
  const json = (name, data) => put(name, JSON.stringify(data));
  json('.next/app-path-routes-manifest.json', Object.fromEntries(artifacts.map(([, entry, route]) => [entry, route === '/skills/alpha' ? '/skills/[name]' : route])));
  json('.next/prerender-manifest.json', { routes: Object.fromEntries(artifacts.map(([, , route]) => [route, {}])) });
  for (const [name, , route] of artifacts) put(`.next/server/app/${name}`, `<html><title>${route}</title><main id="main"><h1>Fixture ${route}</h1></main></html>`);
  // Copy the candidate's actual script graph, not a replacement hash/CLI.
  const scripts = fileURLToPath(new URL('../scripts/', import.meta.url));
  mkdirSync(join(site, 'scripts'));
  for (const file of readdirSync(scripts).filter(name => name.endsWith('.mjs'))) copyFileSync(join(scripts, file), join(site, 'scripts', file));
  return { site, put, json, cleanup: () => rmSync(site, { recursive: true, force: true }) };
}
function cache(f) {
  const files = {};
  for (const [name, entry] of artifacts) {
    const target = join(f.site, '.next/server/route-cache/APP_PAGE', createHash('sha256').update(entry).digest('hex'), '$', name);
    mkdirSync(join(target, '..'), { recursive: true });
    renameSync(join(f.site, '.next/server/app', name), target); files[name] = target;
  }
  return files;
}
const rows = site => readBuiltPages(site).map(page => ({ route: page.route, hash: contentHash(page.html) }));
const cli = site => spawnSync(process.execPath, [join(site, 'scripts/page-hashes.mjs'), '--json'], { cwd: site, encoding: 'utf8' });

test('reader and CLI cover the same complete classic and APP_PAGE path/hash set', () => {
  const f = fixture();
  try {
    const classic = rows(f.site); assert.equal(classic.length, 4);
    assert.ok(classic.some(page => page.route === '/_not-found'));
    assert.deepEqual(classic.map(page => page.route).sort(), readBuild(f.site).pages.map(page => page.path).sort());
    const before = cli(f.site); assert.equal(before.status, 0, before.stderr); assert.deepEqual(JSON.parse(before.stdout), classic);
    cache(f);
    assert.deepEqual(rows(f.site), classic);
    const after = cli(f.site); assert.equal(after.status, 0, after.stderr); assert.deepEqual(JSON.parse(after.stdout), classic);
  } finally { f.cleanup(); }
});

const faults = [
  ['missing', (_f, files) => rmSync(files['skills/alpha.html']), /missing/],
  ['extra', f => f.put('.next/server/app/extra.html', '<title>Extra</title><main id="main">Extra</main>'), /extra/],
  ['duplicate layouts', (f, files) => f.put('.next/server/app/skills/alpha.html', readFileSync(files['skills/alpha.html'])), /duplicate/],
  ['duplicate logical cache route', (f, files) => { const owner = createHash('sha256').update('/skills/[name]/page').digest('hex'); f.put(`.next/server/route-cache/APP_PAGE/${owner}/$/skills/alpha/index.html`, readFileSync(files['skills/alpha.html'])); }, /duplicate/],
  ['wrong owner', (f, files) => { const bytes = readFileSync(files['skills/alpha.html']); rmSync(files['skills/alpha.html']); f.put(`.next/server/route-cache/APP_PAGE/${'a'.repeat(64)}/$/skills/alpha.html`, bytes); }, /owner/],
  ['malformed', f => f.put('.next/server/route-cache/APP_PAGE/not-a-hash/skills/alpha.html', '<title>Bad</title>'), /cache.*artifact|layout/],
  ['file symlink', (_f, files) => { rmSync(files['skills/alpha.html']); symlinkSync(files['skills.html'], files['skills/alpha.html']); }, /symlink/],
  ['directory symlink', f => { const base = join(f.site, '.next/server'); renameSync(join(base, 'route-cache/APP_PAGE'), join(base, 'saved-pages')); symlinkSync(join(base, 'saved-pages'), join(base, 'route-cache/APP_PAGE')); }, /symlink/],
];
for (const [name, change, expected] of faults) test(`manifest-backed reader and CLI refuse ${name}`, () => {
  const f = fixture();
  try {
    change(f, cache(f));
    assert.throws(() => readBuiltPages(f.site), expected);
    const result = cli(f.site); assert.notEqual(result.status, 0); assert.match(result.stderr, expected);
  } finally { f.cleanup(); }
});

test('the explicit-directory API refuses a site-root symlink', () => {
  const f = fixture();
  try {
    const alias = join(f.site, 'alias');
    symlinkSync(f.site, alias);
    assert.throws(() => readBuiltPages(alias), /symlink/);
    // The CLI has no directory input: an aliased script is not this API call.
  } finally { f.cleanup(); }
});

test('a published route manifest cannot silently produce zero pages', () => {
  const f = fixture();
  try {
    rmSync(join(f.site, '.next/server/app'), { recursive: true });
    mkdirSync(join(f.site, '.next/server/app'));
    assert.throws(() => readBuiltPages(f.site), /missing|coverage/);
    assert.notEqual(cli(f.site).status, 0);
  } finally { f.cleanup(); }
});
