// Page hashes: each built page's content hash, for the S-005 Grill Board,
// which binds the owner's review of a page to the exact content it saw. The
// public site shows no review state; nothing here changes what a page shows.
// Plain JavaScript so the hash printer and the tests share it without a
// TypeScript loader.
//
// Content hash (the S-005 page-hash contract): "sha256:" + SHA-256 hex of the
// canonical content of the served page's <main id="main">:
//   - drop <script> and <style> elements, comments, and every subtree whose
//     element carries data-review-exclude (live or generated regions) or
//     data-review-mark (kept in the contract; no page carries one);
//   - take, in document order, each text node and each href, src and alt
//     attribute value (attributes in the order written, before the element's
//     content), with character references decoded;
//   - join them with single spaces, collapse runs of ASCII whitespace (tab, LF,
//     FF, CR, space) to one space and trim;
//   - encode as UTF-8.
// The footer is outside <main>, so a rebuild at a new commit changes no hash.
import { createHash } from 'node:crypto';
import { fileURLToPath } from 'node:url';
import { readPageArtifacts } from './page-artifacts.mjs';
export { routeOf } from './page-artifacts.mjs';

export const siteDir = fileURLToPath(new URL('..', import.meta.url));

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

export { decode as decodeHTMLText };

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
// review mark. Throws when the page has no <main id="main">.
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
export function hasReviewMark(html) {
  return readMain(html).mark;
}

// Explicit site roots (including manifest-backed fixtures) use the same strict
// artifact validation as inventory; the canonical hash algorithm above is unchanged.
export function readBuiltPages(dir = siteDir) {
  return readPageArtifacts(dir).pages.sort((a, b) => a.route.localeCompare(b.route));
}
