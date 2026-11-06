// The page list is a build projection. Owner declarations and existing origin
// receipts remain inputs; the collector supplies the current candidate identity.
import { existsSync, lstatSync, readFileSync, readdirSync, renameSync, unlinkSync, writeFileSync } from 'node:fs';
import { dirname, join, relative, resolve } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { parseArgs } from 'node:util';
import { decodeHTMLText, routeOf } from './page-hash.mjs';

const DEFAULT_SITE = fileURLToPath(new URL('..', import.meta.url));
const INTERNAL = '_global-error.html';
const ID = { spec: /^S-[A-Za-z0-9]{3,}$/, task: /^TK-[A-Za-z0-9]{3,}$/ };
const ROUTE = /^\/(?:[A-Za-z0-9_-]+(?:\/[A-Za-z0-9_-]+)*)?$/;
const SHA = /^(?:[a-f0-9]{40}|[a-f0-9]{64})$/;
const json = (file) => JSON.parse(readFileSync(file, 'utf8'));
const fail = (message) => { throw new Error(`Page inventory: ${message}`); };
const compare = (a, b) => a < b ? -1 : a > b ? 1 : 0;

function walk(directory) {
  if (!existsSync(directory)) return [];
  return readdirSync(directory).sort().flatMap(name => {
    const file = join(directory, name);
    const stat = lstatSync(file);
    if (stat.isSymbolicLink()) fail('source/build symlinks cannot supply page ownership');
    return stat.isDirectory() ? walk(file) : [file];
  });
}

function safeRelative(name) {
  if (typeof name !== 'string' || !name || name.startsWith('/') || name.includes('\\') || /[\r\n]/.test(name) || name.split('/').some(part => part === '..' || part === '.git' || part.startsWith('.env') || part.startsWith('.jot-private-'))) {
    fail('source ownership paths must be public repository-relative paths');
  }
  return name;
}

function ownerRecords(project) {
  const manifest = json(join(project, 'workbench', 'manifest.json'));
  const roots = [manifest.lanes.specs, manifest.collections.landmarks].filter(Boolean);
  const specs = new Set();
  const tasks = new Set();
  const field = (text, name) => text.split(/^## /m)[0].match(new RegExp(`^\\*\\*${name}:\\*\\*\\s*(\\S+)`, 'm'))?.[1];
  for (const root of roots) {
    for (const file of walk(join(project, safeRelative(root)))) {
      if (relative(project, file).split('/').some(part => ['archive', 'retired', 'discarded'].includes(part))) continue;
      if (!file.endsWith('/SPEC.md') && !file.endsWith('/TASK.md')) continue;
      const text = readFileSync(file, 'utf8');
      const spec = field(text, 'Spec ID');
      if (file.endsWith('/SPEC.md') && ID.spec.test(spec ?? '')) {
        specs.add(spec);
        const table = text.split('## Vertical Implementation Slices')[1]?.split(/^## /m)[0] ?? '';
        for (const match of table.matchAll(/^\|\s*(TK-[A-Za-z0-9]{3,})\s*\|/gm)) tasks.add(`${spec}/${match[1]}`);
      } else if (ID.spec.test(spec ?? '')) {
        const task = field(text, 'Task ID');
        if (ID.task.test(task ?? '')) tasks.add(`${spec}/${task}`);
      }
    }
  }
  return { specs, tasks };
}

function routePattern(route) {
  if (typeof route !== 'string' || !route.startsWith('/')) fail('owner rule needs a route');
  const names = [];
  const pieces = route === '/' ? [] : route.slice(1).split('/');
  let source = '^';
  for (const part of pieces) {
    const variable = /^(?:\[\[\.\.\.([A-Za-z][A-Za-z0-9_]*)\]\]|\[(\.\.\.)?([A-Za-z][A-Za-z0-9_]*)\])$/.exec(part);
    if (variable) {
      const name = variable[1] ?? variable[3];
      if (names.includes(name)) fail('duplicate owner route parameter');
      names.push(name);
      source += variable[1] ? '(?:/(.*))?' : variable[2] ? '/(.+)' : '/([^/]+)';
    } else {
      if (!/^[A-Za-z0-9_-]+$/.test(part)) fail('unsupported owner route pattern');
      source += '/' + part;
    }
  }
  if (!pieces.length) source += '/';
  const expression = new RegExp(source + '$');
  return path => {
    const matched = expression.exec(path);
    return matched ? Object.fromEntries(names.map((name, index) => [name, matched[index + 1] ?? ''])) : null;
  };
}

export function readBuild(site = DEFAULT_SITE) {
  const next = join(site, '.next');
  const manifest = json(join(next, 'app-path-routes-manifest.json'));
  const prerendered = Object.keys(json(join(next, 'prerender-manifest.json')).routes);
  const expected = new Set();
  for (const [entry, route] of Object.entries(manifest)) {
    if (!entry.endsWith('/page') || route === '/_global-error') continue;
    const paths = route.includes('[') ? prerendered.filter(path => routePattern(route)(path) !== null) : [route];
    if (!paths.length) fail(`route ${route} has no verifiable prerendered artifact`);
    for (const path of paths) expected.add(path);
  }
  const app = join(next, 'server', 'app');
  if (!existsSync(app)) fail('build has no public artifacts');
  const pages = [];
  const excluded = {};
  for (const file of walk(app).filter(file => file.endsWith('.html'))) {
    const artifact = relative(app, file).replace(/\\/g, '/');
    if (artifact === INTERNAL) { excluded[artifact] = 'internal framework fallback'; continue; }
    const path = routeOf(artifact);
    if (!ROUTE.test(path) || pages.some(page => page.path === path)) fail(`unsupported/duplicate artifact route ${path}`);
    const html = readFileSync(file, 'utf8');
    const head = html.split(/<\/head>/i)[0].replace(/<script\b[\s\S]*?<\/script>/gi, '');
    const title = head.match(/<title\b[^>]*>([\s\S]*?)<\/title>/i)?.[1];
    if (!title) fail(`artifact ${path} has no title`);
    pages.push({ path, title: decodeHTMLText(title).replace(/\s+/g, ' ').trim(), kind: path === '/_not-found' ? 'visitor-404' : 'page' });
  }
  const have = new Set(pages.map(page => page.path));
  if (!have.size || expected.size !== have.size || [...expected].some(path => !have.has(path))) fail('route manifest/artifact coverage differs');
  return { pages: pages.sort((a, b) => compare(a.path, b.path)), excluded };
}

function validateOwner(row, records, project) {
  if (!ID.spec.test(row.spec ?? '') || !ID.task.test(row.task ?? '') || !records.specs.has(row.spec) || !records.tasks.has(`${row.spec}/${row.task}`)) fail(`missing current owner record for ${row.path ?? row.route}`);
  if (!Array.isArray(row.sources) || !row.sources.length) fail('owner needs public source paths');
  for (const source of row.sources) if (!existsSync(join(project, safeRelative(source)))) fail(`owner source does not exist: ${source}`);
  const kind = row.provenance_kind ?? 'historical-landing';
  if (!['historical-landing', 'verified-containment', 'pending-candidate'].includes(kind)) fail('unsupported provenance kind');
  if (kind === 'pending-candidate') {
    if (row.landed !== null) fail('pending candidate must have landed:null');
  } else if (!row.landed || !SHA.test(row.landed.commit ?? '')) fail('historical/verified containment needs an immutable commit');
  if (row.landed !== null) {
    if (typeof row.landed?.branch !== 'string' || !/^[A-Za-z0-9][A-Za-z0-9/._-]*$/.test(row.landed.branch)) fail('provenance needs an explicit branch');
    if (row.landed.pr != null && (!Number.isSafeInteger(row.landed.pr) || row.landed.pr < 1)) fail('provenance PR must be positive or unknown');
  }
}

export function generateInventory(site = DEFAULT_SITE, { write = false, check = false } = {}) {
  site = resolve(site);
  const project = dirname(site);
  const file = join(site, 'page-list.json');
  const original = readFileSync(file, 'utf8');
  const listed = JSON.parse(original);
  const build = readBuild(site);
  const records = ownerRecords(project);
  const rules = (listed.owner_rules ?? []).map(rule => ({ value: rule, match: routePattern(rule.route) }));
  const existing = new Map();
  for (const row of listed.pages ?? []) {
    if (!ROUTE.test(row.path ?? '') || existing.has(row.path)) fail('duplicate or invalid inventory route');
    validateOwner(row, records, project);
    existing.set(row.path, row);
  }
  const routes = new Set(build.pages.map(page => page.path));
  if ([...existing.keys()].some(path => !routes.has(path))) fail('inventory contains a route with no public artifact');
  const projected = new Map(existing);
  const kinds = {};
  for (const page of build.pages) {
    kinds[page.path] = page.kind;
    const matches = rules.map(rule => ({ rule: rule.value, parameters: rule.match(page.path) })).filter(match => match.parameters !== null);
    if (matches.length > 1) fail(`ambiguous owner rules for ${page.path}`);
    const prior = existing.get(page.path);
    if (prior && (prior.provenance_kind ?? 'historical-landing') === 'historical-landing') {
      if (matches.length && (matches[0].rule.spec !== prior.spec || matches[0].rule.task !== prior.task)) fail('historical owner conflicts with a declaration');
      continue;
    }
    if (!matches.length) fail(`no declared owner for ${page.path}`);
    const { rule, parameters } = matches[0];
    if (!Array.isArray(rule.sources) || rule.sources.some(source => typeof source !== 'string')) fail('owner needs public source paths');
    const sources = rule.sources.map(source => source.replace(/\{([A-Za-z][A-Za-z0-9_]*)\}/g, (_match, name) => {
      if (!Object.hasOwn(parameters, name)) fail('source template names an unknown route parameter');
      return parameters[name];
    }));
    const kind = rule.provenance_kind ?? prior?.provenance_kind ?? 'pending-candidate';
    const landed = Object.hasOwn(rule, 'landed') ? rule.landed : prior?.landed ?? null;
    const row = { ...prior, path: page.path, title: page.title, spec: rule.spec, task: rule.task, sources, provenance_kind: kind, landed };
    validateOwner(row, records, project);
    projected.set(page.path, row);
  }
  const inventory = { ...listed, pages: [...projected.values()], excluded: build.excluded };
  const rendered = JSON.stringify(inventory, null, 2) + '\n';
  const changed = original !== rendered;
  if (check && changed) fail('page-list projection is stale; run pages:generate after a build');
  if (write && changed) {
    const temporary = file + `.tmp-${process.pid}`;
    let created = false;
    try { writeFileSync(temporary, rendered, { flag: 'wx' }); created = true; renameSync(temporary, file); }
    finally { if (created && existsSync(temporary)) unlinkSync(temporary); }
  }
  return { inventory, kinds, changed };
}

if (process.argv[1] && import.meta.url === pathToFileURL(resolve(process.argv[1])).href) {
  const { values } = parseArgs({ options: { site: { type: 'string' }, write: { type: 'boolean' }, check: { type: 'boolean' } } });
  const result = generateInventory(values.site ?? DEFAULT_SITE, values);
  console.log(`page inventory: ${result.inventory.pages.length} public surfaces; ${Object.keys(result.inventory.excluded).length} internal fallback; ${result.changed ? 'projection updated' : 'unchanged'}`);
}
