// One manifest-bound HTML enumeration seam for inventory and review hashes.
// Only classic app and the explicit source-owner APP_PAGE cache are supported.
import { createHash } from 'node:crypto';
import { existsSync, lstatSync, readFileSync, readdirSync } from 'node:fs';
import { join, relative } from 'node:path';
import { fileURLToPath } from 'node:url';
const DEFAULT_SITE = fileURLToPath(new URL('..', import.meta.url));
const INTERNAL = '_global-error.html';
const ROUTE = /^\/(?:[A-Za-z0-9_-]+(?:\/[A-Za-z0-9_-]+)*)?$/;
const json = file => JSON.parse(readFileSync(file, 'utf8'));
const fail = message => { throw new Error(`Page artifacts: ${message}`); };
const compare = (a, b) => a < b ? -1 : a > b ? 1 : 0;

export function walkFiles(directory) {
  if (!existsSync(directory)) return [];
  return readdirSync(directory).sort().flatMap(name => {
    const file = join(directory, name);
    const stat = lstatSync(file);
    if (stat.isSymbolicLink()) fail('source/build symlinks cannot supply page ownership');
    return stat.isDirectory() ? walkFiles(file) : [file];
  });
}

export function routePattern(route) {
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

function buildPath(root, name) {
  let file = root;
  if (lstatSync(root).isSymbolicLink()) fail('build symlinks cannot supply public artifacts');
  for (const part of name.split('/')) {
    file = join(file, part);
    try { if (lstatSync(file).isSymbolicLink()) fail('build symlinks cannot supply public artifacts'); }
    catch (error) { if (error.code !== 'ENOENT') throw error; }
  }
  return file;
}

export function routeOf(name) {
  const path = name.replace(/\\/g, '/').replace(/\.html$/, '');
  if (path === 'index') return '/';
  return `/${path.replace(/\/index$/, '')}`;
}

export function readPageArtifacts(site = DEFAULT_SITE) {
  const next = buildPath(site, '.next');
  const manifest = json(buildPath(next, 'app-path-routes-manifest.json'));
  const prerendered = Object.keys(json(buildPath(next, 'prerender-manifest.json')).routes);
  const expected = new Set();
  const owners = new Map();
  for (const [entry, route] of Object.entries(manifest)) {
    if (!entry.endsWith('/page')) continue;
    const paths = route.includes('[') ? prerendered.filter(path => routePattern(route)(path) !== null) : [route];
    if (!paths.length) fail(`route ${route} has no verifiable prerendered artifact`);
    for (const path of paths) {
      if (route !== '/_global-error') expected.add(path);
      if (!owners.has(path)) owners.set(path, new Set());
      owners.get(path).add(createHash('sha256').update(entry).digest('hex'));
    }
  }
  const app = buildPath(next, 'server/app');
  const cache = buildPath(next, 'server/route-cache/APP_PAGE');
  // Next16's supported adapter uses getRouteCacheKey: APP_PAGE/source hash/$/route.
  // Read that exact owner-bound layout, never unrelated adapter/fallback outputs.
  const artifacts = [
    ...walkFiles(app).filter(file => file.endsWith('.html')).map(file => ({ file, artifact: relative(app, file).replace(/\\/g, '/') })),
    ...walkFiles(cache).filter(file => file.endsWith('.html')).map(file => {
      const name = relative(cache, file).replace(/\\/g, '/');
      const match = /^([a-f0-9]{64})\/\$\/(.+\.html)$/.exec(name);
      if (!match) fail(`unsupported APP_PAGE cache artifact ${name}`);
      const path = routeOf(match[2]);
      if (!owners.get(path)?.has(match[1])) fail(`APP_PAGE cache owner differs for ${path}`);
      return { file, artifact: match[2] };
    }),
  ];
  const pages = [];
  const excluded = {};
  for (const { file, artifact } of artifacts) {
    if (artifact === INTERNAL) { excluded[artifact] = 'internal framework fallback'; continue; }
    const path = routeOf(artifact);
    if (!ROUTE.test(path) || pages.some(page => page.route === path)) fail(`unsupported/duplicate artifact route ${path}`);
    const html = readFileSync(file, 'utf8');
    pages.push({ name: artifact, route: path, html });
  }
  const have = new Set(pages.map(page => page.route));
  const missing = [...expected].filter(path => !have.has(path)).sort(compare);
  const extra = [...have].filter(path => !expected.has(path)).sort(compare);
  if (!have.size || missing.length || extra.length) fail(`route manifest/artifact coverage differs: missing=${JSON.stringify(missing)}; extra=${JSON.stringify(extra)}`);
  return { pages: pages.sort((a, b) => compare(a.route, b.route)), excluded };
}
