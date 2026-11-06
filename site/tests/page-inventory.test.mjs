import { test } from 'node:test';
import assert from 'node:assert/strict';
import { mkdtempSync, mkdirSync, readFileSync, writeFileSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { generateInventory } from '../scripts/page-inventory.mjs';

const legacy = { path: '/', title: 'Original home title', spec: 'S-003', task: 'TK-001', landed: { branch: 'dev', commit: 'a'.repeat(40), pr: 1 }, sources: ['site/app/page.tsx'], status: 'draft' };
const html = (title) => `<html><head><title>${title}</title></head><body><main id="main"><h1>${title}</h1></main></body></html>`;

function fixture() {
  const root = mkdtempSync(join(tmpdir(), 'ams-page-inventory-'));
  const site = join(root, 'site');
  const put = (name, body) => { const file = join(root, name); mkdirSync(join(file, '..'), { recursive: true }); writeFileSync(file, body); };
  const json = (name, value) => put(name, JSON.stringify(value, null, 2) + '\n');
  json('workbench/manifest.json', { lanes: { specs: 'workbench/specs' }, collections: {} });
  put('workbench/specs/S-003-site/SPEC.md', '**Spec ID:** S-003\n\n## Vertical Implementation Slices\n\n| TK-001 | Shell | done | none | proof |\n');
  put('workbench/specs/S-008-skills/SPEC.md', '**Spec ID:** S-008\n');
  put('workbench/specs/S-008-skills/tasks/TK-001/TASK.md', '**Task ID:** TK-001\n**Spec ID:** S-008\n');
  put('workbench/specs/S-008-skills/tasks/TK-002/TASK.md', '**Task ID:** TK-002\n**Spec ID:** S-008\n');
  put('site/app/page.tsx', 'home');
  put('site/app/layout.tsx', 'shell');
  put('site/app/skills/page.tsx', 'index');
  put('site/app/skills/[name]/page.tsx', 'article');
  const rules = [
    { route: '/skills', spec: 'S-008', task: 'TK-001', sources: ['site/app/skills/page.tsx'] },
    { route: '/skills/[name]', spec: 'S-008', task: 'TK-002', sources: ['site/app/skills/[name]/page.tsx', 'site/content/skills/{name}.md'] },
    { route: '/_not-found', spec: 'S-003', task: 'TK-001', sources: ['site/app/layout.tsx'] },
  ];
  json('site/page-list.json', { about: 'fixture', owner_rules: rules, pages: [legacy] });
  const paths = { '/page': '/', '/skills/page': '/skills', '/skills/[name]/page': '/skills/[name]', '/_not-found/page': '/_not-found', '/_global-error/page': '/_global-error' };
  json('site/.next/app-path-routes-manifest.json', paths);
  const prerender = { routes: { '/': {}, '/skills': {}, '/_not-found': {} } };
  const addArticle = (name) => {
    prerender.routes[`/skills/${name}`] = { srcRoute: '/skills/[name]' };
    json('site/.next/prerender-manifest.json', prerender);
    put(`site/.next/server/app/skills/${name}.html`, html(name));
    put(`site/content/skills/${name}.md`, name);
  };
  put('site/.next/server/app/index.html', html('Current home title'));
  put('site/.next/server/app/skills.html', html('Skills'));
  put('site/.next/server/app/_not-found.html', html('404: Not found'));
  put('site/.next/server/app/_global-error.html', '<html>Internal fallback</html>');
  addArticle('alpha'); addArticle('beta');
  return { root, site, put, json, rules, paths, prerender, addArticle, cleanup: () => rmSync(root, { recursive: true, force: true }) };
}

test('a build automatically supplies ownership for each article and visitor404 without changing historical metadata', () => {
  const f = fixture();
  try {
    const first = generateInventory(f.site, { write: true });
    assert.deepEqual(first.inventory.pages.find(row => row.path === '/'), legacy);
    assert.deepEqual(first.inventory.pages.map(row => row.path).sort(), ['/', '/_not-found', '/skills', '/skills/alpha', '/skills/beta']);
    const article = first.inventory.pages.find(row => row.path === '/skills/alpha');
    assert.equal(article.spec, 'S-008'); assert.equal(article.task, 'TK-002');
    assert.equal(article.provenance_kind, 'pending-candidate'); assert.equal(article.landed, null);
    assert.ok(article.sources.includes('site/content/skills/alpha.md'));
    assert.equal(first.kinds['/_not-found'], 'visitor-404');
    assert.deepEqual(first.inventory.excluded, { '_global-error.html': 'internal framework fallback' });
    const bytes = readFileSync(join(f.site, 'page-list.json'), 'utf8');
    assert.equal(generateInventory(f.site, { write: true }).changed, false);
    assert.equal(readFileSync(join(f.site, 'page-list.json'), 'utf8'), bytes);
    f.addArticle('gamma');
    const next = generateInventory(f.site, { write: true });
    assert.equal(next.inventory.pages.find(row => row.path === '/skills/gamma').task, 'TK-002');
    assert.equal(next.inventory.pages.length, 6);
  } finally { f.cleanup(); }
});

test('missing or ambiguous owners and invented record identities refuse before writing', () => {
  for (const change of [
    (f) => f.rules.splice(1, 1),
    (f) => f.rules.push({ ...f.rules[1] }),
    (f) => { f.rules[1].task = 'TK-999'; },
    (f) => { f.rules[1].spec = 'S-999'; },
  ]) {
    const f = fixture();
    try {
      change(f); f.json('site/page-list.json', { owner_rules: f.rules, pages: [legacy] });
      const before = readFileSync(join(f.site, 'page-list.json'), 'utf8');
      assert.throws(() => generateInventory(f.site, { write: true }), /owner|record|ambiguous/i);
      assert.equal(readFileSync(join(f.site, 'page-list.json'), 'utf8'), before);
    } finally { f.cleanup(); }
  }
});

test('actual artifacts and Next route manifests must agree; public404 cannot silently disappear', () => {
  for (const change of [
    (f) => rmSync(join(f.site, '.next/server/app/_not-found.html')),
    (f) => f.put('site/.next/server/app/unregistered.html', html('Unregistered')),
    (f) => { f.prerender.routes['/skills/missing'] = { srcRoute: '/skills/[name]' }; f.json('site/.next/prerender-manifest.json', f.prerender); },
  ]) {
    const f = fixture();
    try { change(f); assert.throws(() => generateInventory(f.site), /artifact|route|coverage/i); }
    finally { f.cleanup(); }
  }
});

test('verified containment remains a real pin and never becomes a creation assertion', () => {
  const f = fixture();
  try {
    Object.assign(f.rules[0], { provenance_kind: 'verified-containment', landed: { branch: 'dev', commit: 'b'.repeat(40), pr: 176 } });
    f.json('site/page-list.json', { owner_rules: f.rules, pages: [legacy] });
    const result = generateInventory(f.site);
    const index = result.inventory.pages.find(row => row.path === '/skills');
    assert.equal(index.provenance_kind, 'verified-containment');
    assert.deepEqual(index.landed, f.rules[0].landed);
    f.rules[0].landed.commit = 'b'.repeat(41);
    f.json('site/page-list.json', { owner_rules: f.rules, pages: [legacy] });
    assert.throws(() => generateInventory(f.site), /commit/i);
    f.rules[0].landed = null;
    f.json('site/page-list.json', { owner_rules: f.rules, pages: [legacy] });
    assert.throws(() => generateInventory(f.site), /provenance|containment|commit/i);
  } finally { f.cleanup(); }
});

test('generated rows remain projections of current declarations rather than a second owner store', () => {
  const f = fixture();
  try {
    generateInventory(f.site, { write: true });
    f.rules[1].task = 'TK-999';
    const current = JSON.parse(readFileSync(join(f.site, 'page-list.json'), 'utf8'));
    current.owner_rules = f.rules; f.json('site/page-list.json', current);
    assert.throws(() => generateInventory(f.site), /owner|record/i);
    f.put('workbench/specs/S-008-skills/tasks/TK-003/TASK.md', '**Task ID:** TK-003\n**Spec ID:** S-008\n');
    Object.assign(f.rules[1], { task: 'TK-003', provenance_kind: 'verified-containment', landed: { branch: 'dev', commit: 'c'.repeat(40), pr: 2 } });
    current.owner_rules = f.rules; f.json('site/page-list.json', current);
    const next = generateInventory(f.site, { write: true });
    const alpha = next.inventory.pages.find(row => row.path === '/skills/alpha');
    assert.equal(alpha.task, 'TK-003');
    assert.equal(alpha.provenance_kind, 'verified-containment');
    assert.deepEqual(next.inventory.pages.find(row => row.path === '/'), legacy);
  } finally { f.cleanup(); }
});

test('the normal generation command runs without Git or inherited host configuration', () => {
  const f = fixture();
  try {
    const script = fileURLToPath(new URL('../scripts/page-inventory.mjs', import.meta.url));
    const result = spawnSync(process.execPath, [script, '--site', f.site, '--write'], { encoding: 'utf8', env: { PATH: '' } });
    assert.equal(result.status, 0, result.stderr);
    assert.equal(JSON.parse(readFileSync(join(f.site, 'page-list.json'), 'utf8')).pages.length, 5);
    const check = spawnSync(process.execPath, [script, '--site', f.site, '--check'], { encoding: 'utf8', env: { PATH: '' } });
    assert.equal(check.status, 0, check.stderr);
    f.addArticle('gamma');
    const stale = spawnSync(process.execPath, [script, '--site', f.site, '--check'], { encoding: 'utf8', env: { PATH: '' } });
    assert.notEqual(stale.status, 0);
    assert.match(stale.stderr, /projection is stale/);
  } finally { f.cleanup(); }
});

test('pending provenance cannot claim a landing and public source paths cannot escape the tree', () => {
  for (const change of [
    (f) => Object.assign(f.rules[0], { provenance_kind: 'pending-candidate', landed: { commit: 'd'.repeat(40) } }),
    (f) => { f.rules[0].sources = [f.root]; },
    (f) => { f.rules[1].sources = ['site/content/skills/{unknown}.md']; },
  ]) {
    const f = fixture();
    try {
      change(f); f.json('site/page-list.json', { owner_rules: f.rules, pages: [legacy] });
      const before = readFileSync(join(f.site, 'page-list.json'), 'utf8');
      assert.throws(() => generateInventory(f.site, { write: true }), /pending|source|parameter/i);
      assert.equal(readFileSync(join(f.site, 'page-list.json'), 'utf8'), before);
    } finally { f.cleanup(); }
  }
});

test('a later article cannot inherit an earlier verified containment receipt', () => {
  const f = fixture();
  try {
    const first = generateInventory(f.site);
    for (const page of first.inventory.pages.filter(page => page.path !== '/')) {
      page.provenance_kind = 'verified-containment';
      page.landed = { branch: 'dev', commit: 'b'.repeat(40), pr: 176 };
    }
    f.json('site/page-list.json', first.inventory);
    f.addArticle('gamma');
    const next = generateInventory(f.site);
    assert.equal(next.inventory.pages.find(page => page.path === '/skills/alpha').landed.commit, 'b'.repeat(40));
    const added = next.inventory.pages.find(page => page.path === '/skills/gamma');
    assert.equal(added.provenance_kind, 'pending-candidate');
    assert.equal(added.landed, null);
  } finally { f.cleanup(); }
});

test('the current real build and committed review projection have exact coverage', () => {
  const result = generateInventory(undefined, { check: true });
  assert.equal(result.changed, false);
  assert.equal(result.kinds['/_not-found'], 'visitor-404');
  assert.deepEqual(result.inventory.excluded, { '_global-error.html': 'internal framework fallback' });
});
