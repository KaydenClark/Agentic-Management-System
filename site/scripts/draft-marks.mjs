// Draft marks (S-003 TK-004): a page's content hash and the committed approval
// records that can remove its draft mark. Plain JavaScript so the build script,
// the hash printer and the tests share it without a TypeScript loader.
//
// Content hash (the S-005 page-hash contract): "sha256:" + SHA-256 hex of the
// canonical content of the served page's <main id="main">:
//   - drop <script> and <style> elements, comments, and every subtree whose
//     element carries data-review-mark (the draft mark) or data-review-exclude
//     (live or generated regions);
//   - take, in document order, each text node and each href, src and alt
//     attribute value (attributes in the order written, before the element's
//     content), with character references decoded;
//   - join them with single spaces, collapse runs of ASCII whitespace (tab, LF,
//     FF, CR, space) to one space and trim;
//   - encode as UTF-8.
// The footer is outside <main>, so a rebuild at a new commit changes no hash.
import { createHash } from 'node:crypto';
import { existsSync, readFileSync, readdirSync, statSync } from 'node:fs';
import { join, relative } from 'node:path';
import { fileURLToPath } from 'node:url';

export const siteDir = fileURLToPath(new URL('..', import.meta.url));
export const APPROVALS_FILE = join(siteDir, 'approvals.json');

const VOID = new Set(['area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr']);
const RAW = new Set(['script', 'style']);
const KEPT_ATTRS = new Set(['href', 'src', 'alt']);
const NAMED = { amp: '&', lt: '<', gt: '>', quot: '"', apos: "'", nbsp: ' ' };
const ASCII_WS = /[\t\n\f\r ]+/g;

function decode(s) {
  return s.replace(/&(#x[0-9a-f]+|#[0-9]+|[a-z]+);/gi, (whole, ref) => {
    if (ref[0] === '#') {
      const code = ref[1] === 'x' || ref[1] === 'X' ? parseInt(ref.slice(2), 16) : parseInt(ref.slice(1), 10);
      return Number.isFinite(code) && code <= 0x10ffff ? String.fromCodePoint(code) : whole;
    }
    return NAMED[ref.toLowerCase()] ?? whole;
  });
}

function attributes(source) {
  const out = [];
  const re = /([^\s"'>/=]+)(?:\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s"'=<>`]+)))?/g;
  for (const m of source.matchAll(re)) out.push([m[1].toLowerCase(), decode(m[2] ?? m[3] ?? m[4] ?? '')]);
  return out;
}

// Tokenize HTML into start tags, end tags and text; comments are skipped and
// raw-text elements (script, style) are emitted as one skipped element.
function* tokens(html) {
  const re = /<!--[\s\S]*?-->|<!\[CDATA\[[\s\S]*?\]\]>|<![^>]*>|<\/\s*([a-zA-Z][^\s/>]*)[^>]*>|<([a-zA-Z][^\s/>]*)((?:[^>"']|"[^"]*"|'[^']*')*?)(\/?)>/g;
  let last = 0;
  let m;
  while ((m = re.exec(html))) {
    if (m.index > last) yield { type: 'text', text: html.slice(last, m.index) };
    last = re.lastIndex;
    if (m[1]) yield { type: 'end', name: m[1].toLowerCase() };
    else if (m[2]) {
      const name = m[2].toLowerCase();
      if (RAW.has(name)) {
        const close = new RegExp(`</${name}\\s*>`, 'ig');
        close.lastIndex = re.lastIndex;
        const c = close.exec(html);
        last = re.lastIndex = c ? close.lastIndex : html.length;
        continue;
      }
      yield { type: 'start', name, attrs: attributes(m[3]), selfClosing: m[4] === '/' || VOID.has(name) };
    }
  }
  if (last < html.length) yield { type: 'text', text: html.slice(last) };
}

// The pieces of <main id="main"> that the hash covers, plus whether it holds a
// draft mark. Throws when the page has no <main id="main">.
function readMain(html) {
  const pieces = [];
  let depth = -1; // depth inside <main id="main">; -1 = not yet inside
  let skipDepth = -1; // depth at which an excluded subtree opened
  const stack = [];
  let mark = false;
  let found = false;
  for (const t of tokens(html)) {
    if (depth < 0) {
      if (t.type === 'start' && t.name === 'main' && t.attrs.some(([k, v]) => k === 'id' && v === 'main')) {
        depth = 0;
        found = true;
        stack.push('main');
      }
      continue;
    }
    if (t.type === 'text') {
      if (skipDepth < 0) pieces.push(decode(t.text));
    } else if (t.type === 'start') {
      const names = new Set(t.attrs.map(([k]) => k));
      if (names.has('data-review-mark')) mark = true;
      const excluded = names.has('data-review-mark') || names.has('data-review-exclude');
      if (skipDepth < 0 && !excluded) for (const [k, v] of t.attrs) if (KEPT_ATTRS.has(k)) pieces.push(v);
      if (t.selfClosing) continue;
      stack.push(t.name);
      if (skipDepth < 0 && excluded) skipDepth = stack.length;
    } else {
      const at = stack.lastIndexOf(t.name);
      if (at < 0) continue; // stray end tag
      stack.length = at;
      if (skipDepth > stack.length) skipDepth = -1;
      if (stack.length === 0) break; // </main>
    }
  }
  if (!found) throw new Error('page has no <main id="main">');
  return { pieces, mark };
}

export function canonicalContent(html) {
  return readMain(html).pieces.join(' ').replace(ASCII_WS, ' ').replace(/^ | $/g, '');
}

export function contentHash(html) {
  return `sha256:${createHash('sha256').update(canonicalContent(html), 'utf8').digest('hex')}`;
}

// True when <main id="main"> holds an element carrying data-review-mark.
export function hasDraftMark(html) {
  return readMain(html).mark;
}

// The route of a prerendered file under .next/server/app: index.html is "/",
// start.html is "/start", a/b.html is "/a/b".
export function routeOf(name) {
  const path = name.replace(/\\/g, '/').replace(/\.html$/, '');
  if (path === 'index') return '/';
  return `/${path.replace(/\/index$/, '')}`;
}

// The not-found page is served at every unknown address, so its mark cannot
// depend on a route; it stays a draft.
export const UNAPPROVABLE = new Set(['/_not-found']);
const FIELDS = ['route', 'hash', 'approver', 'date', 'source'];
const REPO_LINK = /^https:\/\/github\.com\/KaydenClark\/Agentic-Management-System\/\S+$/;

// Problems with an approvals document ({ approvals: [...] }); [] when valid.
export function validateApprovals(doc) {
  if (!doc || !Array.isArray(doc.approvals)) return ['approvals file has no "approvals" list'];
  const problems = [];
  doc.approvals.forEach((a, i) => {
    const at = `approval ${i + 1}${a && a.route ? ` (${a.route})` : ''}`;
    if (!a || typeof a !== 'object') return problems.push(`${at}: not an object`);
    for (const k of Object.keys(a)) if (!FIELDS.includes(k)) problems.push(`${at}: unknown field "${k}"`);
    if (typeof a.route !== 'string' || !a.route.startsWith('/')) problems.push(`${at}: route must start with /`);
    else if (UNAPPROVABLE.has(a.route)) problems.push(`${at}: ${a.route} cannot be approved`);
    if (typeof a.hash !== 'string' || !/^sha256:[0-9a-f]{64}$/.test(a.hash)) problems.push(`${at}: hash must be sha256: plus 64 hex digits`);
    if (typeof a.approver !== 'string' || !a.approver.trim()) problems.push(`${at}: no approver`);
    if (typeof a.date !== 'string' || !/^\d{4}-\d{2}-\d{2}$/.test(a.date) || Number.isNaN(Date.parse(a.date))) problems.push(`${at}: date must be YYYY-MM-DD`);
    if (typeof a.source !== 'string' || !REPO_LINK.test(a.source)) problems.push(`${at}: source must link the dated record of the approval in this repository on GitHub`);
  });
  return problems;
}

export function readApprovals(file = APPROVALS_FILE) {
  return JSON.parse(readFileSync(file, 'utf8'));
}

// Routes approved at their current hash. pages: [{ route, hash }].
export function approvedRoutes(pages, records) {
  const approved = new Set();
  for (const { route, hash } of pages) {
    if (UNAPPROVABLE.has(route)) continue;
    if (records.some((a) => a.route === route && a.hash === hash)) approved.add(route);
  }
  return approved;
}

// Disagreements between built pages ([{ route, html }]) and the approval
// records: a page without its mark needs an approval at its current hash, and
// an approved page must not show the mark.
export function markProblems(pages, records) {
  const problems = [];
  for (const p of pages) {
    const hash = contentHash(p.html);
    const approved = approvedRoutes([{ route: p.route, hash }], records).has(p.route);
    const marked = hasDraftMark(p.html);
    if (!marked && !approved) problems.push(`${p.route}: no draft mark, but no approval names its current hash ${hash}`);
    if (marked && approved) problems.push(`${p.route}: approved at ${hash} but still shows the draft mark`);
  }
  return problems;
}

// Every prerendered page in a build: [{ name, route, html }]. Next's own
// _global-error.html does not use the shell, so it is not a page.
export function readBuiltPages(dir = siteDir) {
  const out = join(dir, '.next', 'server', 'app');
  if (!existsSync(out)) throw new Error('No build output: run `npm run build` in site/ first.');
  const walk = (d) => readdirSync(d).flatMap((n) => {
    const p = join(d, n);
    return statSync(p).isDirectory() ? walk(p) : [p];
  });
  return walk(out)
    .filter((p) => p.endsWith('.html') && relative(out, p) !== '_global-error.html')
    .map((p) => ({ name: relative(out, p), route: routeOf(relative(out, p)), html: readFileSync(p, 'utf8') }))
    .sort((a, b) => a.route.localeCompare(b.route));
}
