// The skills wiki's Markdown: exactly the restricted subset of the S-008
// article contract, parsed to a small block tree that app/skills/Markdown.tsx
// renders. Anything outside the subset throws a MarkdownError naming the file
// and line, so a build fails loudly instead of rendering it wrong.
//
// Blocks: `##` and `###` headings; paragraphs; `-` bullet and `1.` numbered
// lists (one level); GFM pipe tables with a header row; `>` blockquotes;
// fenced code blocks (```). Inline: `code`, **bold**, *italic* and
// [text](url) links. A backslash escapes Markdown punctuation.
// Refused: `#` and `####`+ headings, raw HTML and autolinks, images,
// footnotes, reference links, nested lists, `*`/`+` bullets, `1)` markers,
// `_`/`__` emphasis, strikethrough, thematic breaks, setext headings,
// indented code, `~~~` fences and character references.
// Plain JavaScript so the tests import it on any Node; types in markdown.d.mts.

export class MarkdownError extends Error {
  constructor(file, line, message) {
    super(`${file}:${line}: ${message}`);
    this.name = 'MarkdownError';
    this.file = file;
    this.line = line;
  }
}

const ESCAPABLE = new Set('\\`*_{}[]()#+-.!|>~<'.split(''));
const FENCE = /^```([A-Za-z0-9_+-]*)\s*$/;
const HEADING = /^(#+)(\s*)(.*)$/;
const BULLET = /^-\s+(.*)$/;
const NUMBERED = /^\d{1,3}\.\s+(.*)$/;
const TABLE_SEP = /^\|?\s*:?-+:?\s*(?:\|\s*:?-+:?\s*)*\|?\s*$/;

// Plain text of inline nodes (headings, slugs, test comparisons).
export function inlineText(nodes) {
  return nodes.map((n) => (n.type === 'text' || n.type === 'code' ? n.value : inlineText(n.children))).join('');
}

// A heading's id: lowercase words joined by hyphens, apostrophes dropped.
export function slug(text) {
  return text.toLowerCase().replace(/['’]/g, '').replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '') || 'section';
}

// Inline Markdown to nodes. `fail(message)` throws for the current line.
export function parseInline(src, fail, inLink = false) {
  const [nodes, end] = inlineUntil(src, 0, null, fail, inLink);
  if (end !== src.length) fail(`unexpected text at column ${end + 1}`);
  return nodes;
}

function inlineUntil(s, start, closer, fail, inLink) {
  const nodes = [];
  let text = '';
  let rawStart = start;
  let i = start;
  // Refusals are checked on the raw source of each text run, so an escaped
  // character (\_) is never mistaken for syntax.
  const flush = () => {
    if (text) {
      checkText(s.slice(rawStart, i), fail);
      nodes.push({ type: 'text', value: text });
    }
    text = '';
  };
  const mark = (next) => { i = next; rawStart = next; };
  while (i < s.length) {
    const c = s[i];
    if (c === '\\' && ESCAPABLE.has(s[i + 1])) { text += s[i + 1]; i += 2; continue; }
    if (closer === '**' && s.startsWith('**', i)) { flush(); return [nodes, i + 2]; }
    // *** after italic text inside bold closes the italic, then the bold.
    if (closer === '*' && s.startsWith('***', i)) { flush(); return [nodes, i + 1]; }
    if (closer === '*' && c === '*' && !s.startsWith('**', i)) { flush(); return [nodes, i + 1]; }
    if (closer === ']' && c === ']') { flush(); return [nodes, i + 1]; }
    if (c === '`') {
      const run = s.slice(i).match(/^`+/)[0];
      const close = s.indexOf(run, i + run.length);
      if (close < 0) fail('unclosed inline code (`)');
      let value = s.slice(i + run.length, close);
      if (value.length > 1 && value.startsWith(' ') && value.endsWith(' ')) value = value.slice(1, -1);
      if (!value.trim()) fail('empty inline code');
      flush();
      nodes.push({ type: 'code', value });
      mark(close + run.length);
      continue;
    }
    if (s.startsWith('***', i)) fail('*** emphasis is not supported; use **bold** or *italic*');
    if (s.startsWith('**', i)) {
      flush();
      const [children, end] = inlineUntil(s, i + 2, '**', fail, inLink);
      if (end < 0) fail('unclosed **bold**');
      if (!children.length) fail('empty **bold**');
      nodes.push({ type: 'strong', children });
      mark(end);
      continue;
    }
    if (c === '*') {
      // An asterisk between spaces is a literal (5 * 3); any other opens italic.
      if (/\s/.test(s[i + 1] ?? ' ') && (i === 0 || /\s/.test(s[i - 1]))) { text += c; i += 1; continue; }
      flush();
      const [children, end] = inlineUntil(s, i + 1, '*', fail, inLink);
      if (end < 0) fail('unclosed *italic*');
      if (!children.length) fail('empty *italic*');
      nodes.push({ type: 'em', children });
      mark(end);
      continue;
    }
    if (c === '!' && s[i + 1] === '[') fail('images are not supported');
    if (c === '[') {
      if (s[i + 1] === '^') fail('footnotes are not supported');
      if (inLink) fail('a link inside link text is not supported');
      flush();
      const [children, end] = inlineUntil(s, i + 1, ']', fail, true);
      if (end < 0) fail('unclosed [ (escape a literal bracket as \\[)');
      if (s[end] !== '(') fail('[text] must be followed by (url); reference links are not supported (escape a literal bracket as \\[)');
      const close = s.indexOf(')', end);
      if (close < 0) fail('unclosed link (url)');
      const href = s.slice(end + 1, close);
      if (!href || /\s/.test(href)) fail(`link url ${JSON.stringify(href)} is empty or has spaces (titles are not supported)`);
      if (!children.length) fail('empty link text');
      nodes.push({ type: 'link', href, children });
      mark(close + 1);
      continue;
    }
    if (c === '<' && /[A-Za-z/!?]/.test(s[i + 1] ?? '')) fail('raw HTML and <autolinks> are not supported');
    if (s.startsWith('~~', i)) fail('strikethrough is not supported');
    text += c;
    i += 1;
  }
  if (closer) return [nodes, -1];
  flush();
  return [nodes, i];
}

function checkText(text, fail) {
  if (/&(?:#\d+|#x[0-9a-f]+|[a-z][a-z0-9]*);/i.test(text)) fail('character references (&name;) are not supported; type the character');
  if (/(?:^|[^\w\\])__?[^_\s][^_]*?__?(?![\w])/.test(text)) fail('_underscore_ emphasis is not supported; use *italic* or **bold** (or escape \\_)');
}

// Split a table row on unescaped pipes outside inline code.
function cells(line, fail) {
  let s = line.trim();
  if (s.startsWith('|')) s = s.slice(1);
  if (s.endsWith('|') && !s.endsWith('\\|')) s = s.slice(0, -1);
  const out = [];
  let cur = '';
  let code = null;
  for (let i = 0; i < s.length; i++) {
    const c = s[i];
    if (c === '\\' && s[i + 1] === '|') { cur += '\\|'; i++; continue; }
    if (c === '`') {
      const run = s.slice(i).match(/^`+/)[0];
      if (code === null) code = run; else if (code === run) code = null;
      cur += run;
      i += run.length - 1;
      continue;
    }
    if (c === '|' && code === null) { out.push(cur.trim()); cur = ''; continue; }
    cur += c;
  }
  if (code !== null) fail('unclosed inline code in table row');
  out.push(cur.trim());
  return out;
}

// Markdown source to blocks. `file` names the source in errors.
export function parseMarkdown(src, file = 'markdown', firstLine = 1) {
  const lines = src.replace(/\r\n?/g, '\n').split('\n');
  const blocks = [];
  let i = 0;
  const lineNo = () => firstLine + i;
  const failAt = (n) => (message) => { throw new MarkdownError(file, n, message); };
  const fail = (message) => failAt(lineNo())(message);
  const inline = (text, n = lineNo()) => parseInline(text, failAt(n));

  // A line that starts a block other than a paragraph (or is refused).
  function blockStart(raw) {
    const line = raw.trimEnd();
    if (!line.trim()) return true;
    if (/^ {4,}|^\t/.test(raw)) return true;
    const t = line.trimStart();
    return HEADING.test(t) || t.startsWith('```') || t.startsWith('~~~') || t.startsWith('>') || t.startsWith('|') ||
      BULLET.test(t) || NUMBERED.test(t) || /^[*+]\s/.test(t) || /^\d+\)\s/.test(t) || /^</.test(t) ||
      /^(?:-{3,}|\*{3,}|_{3,}|={3,})\s*$/.test(t) || /^\[[^\]]+\]:/.test(t);
  }

  // Refusals that apply to any line that opens a block.
  function refuse(raw) {
    const t = raw.trim();
    if (/^ {4,}\S|^\t/.test(raw)) fail('indented code blocks and indented lines are not supported; use a ``` fence');
    if (t.startsWith('~~~')) fail('~~~ fences are not supported; use ```');
    if (/^(?:-{3,}|\*{3,}|_{3,})$/.test(t)) fail('thematic breaks (---) are not supported');
    if (/^={3,}$/.test(t)) fail('setext headings are not supported; use ## or ###');
    if (/^[*+]\s/.test(t)) fail('use - for bullet lists (* and + are not supported)');
    if (/^\d+\)\s/.test(t)) fail('numbered lists use 1. markers (1) is not supported)');
    if (/^</.test(t)) fail('raw HTML is not supported');
    if (/^\[\^[^\]]*\]:/.test(t)) fail('footnotes are not supported');
    if (/^\[[^\]]+\]:/.test(t)) fail('reference link definitions are not supported');
  }

  while (i < lines.length) {
    const raw = lines[i];
    const line = raw.trimEnd();
    if (!line.trim()) { i++; continue; }
    refuse(raw);
    const t = line.trimStart();

    const fence = t.match(FENCE);
    if (t.startsWith('```')) {
      if (!fence) fail('a ``` fence takes at most a language name');
      const start = lineNo();
      const body = [];
      i++;
      while (i < lines.length && lines[i].trim() !== '```') body.push(lines[i++]);
      if (i >= lines.length) failAt(start)('unclosed ``` fence');
      i++;
      if (!body.join('').trim()) failAt(start)('empty code block');
      blocks.push({ type: 'code', lang: fence[1] || null, text: body.join('\n') });
      continue;
    }

    const h = t.match(HEADING);
    if (h) {
      const level = h[1].length;
      if (level === 1) fail('# headings are not supported (the page title is the skill name); use ##');
      if (level > 3) fail(`${h[1]} headings are not supported; use ## or ###`);
      if (!h[2] && h[3]) fail(`${h[1]} must be followed by a space`);
      const text = h[3].replace(/\s+#+\s*$/, '').trim();
      if (!text) fail('empty heading');
      blocks.push({ type: 'heading', level, inline: inline(text), line: lineNo() });
      i++;
      continue;
    }

    if (t.startsWith('>')) {
      const start = lineNo();
      const paras = [];
      let cur = [];
      while (i < lines.length && lines[i].trimStart().startsWith('>')) {
        const inner = lines[i].trimStart().replace(/^>\s?/, '');
        if (inner.trimStart().startsWith('>')) fail('nested blockquotes are not supported');
        if (!inner.trim()) { if (cur.length) paras.push(cur); cur = []; i++; continue; }
        if (blockStart(inner)) fail('only paragraphs are supported inside a blockquote');
        cur.push(inner.trim());
        i++;
      }
      if (cur.length) paras.push(cur);
      if (!paras.length) failAt(start)('empty blockquote');
      blocks.push({ type: 'blockquote', paragraphs: paras.map((p) => inline(p.join(' '), start)) });
      continue;
    }

    if (t.startsWith('|')) {
      const start = lineNo();
      const header = cells(t, fail);
      i++;
      if (i >= lines.length || !TABLE_SEP.test(lines[i].trim())) failAt(start)('a table needs a header row and a | --- | separator row');
      const sep = cells(lines[i].trim(), fail);
      if (sep.length !== header.length) fail(`table separator has ${sep.length} columns, header has ${header.length}`);
      i++;
      const rows = [];
      while (i < lines.length && lines[i].trim().startsWith('|')) {
        const row = cells(lines[i].trim(), fail);
        if (row.length !== header.length) fail(`table row has ${row.length} cells, header has ${header.length}`);
        rows.push(row.map((c) => inline(c)));
        i++;
      }
      if (i < lines.length && lines[i].trim()) fail('a table must be followed by a blank line');
      if (!rows.length) failAt(start)('a table needs at least one body row');
      blocks.push({ type: 'table', header: header.map((c) => inline(c, start)), rows });
      continue;
    }

    const bullet = t.match(BULLET);
    const numbered = t.match(NUMBERED);
    if (bullet || numbered) {
      const ordered = !bullet;
      const marker = ordered ? NUMBERED : BULLET;
      const items = [];
      while (i < lines.length) {
        const l = lines[i];
        const lt = l.trim();
        if (!lt) break;
        const m = /^\S/.test(l) ? lt.match(marker) : null;
        if (m) { items.push({ text: [m[1].trim()], line: lineNo() }); i++; continue; }
        if (/^\s+(?:[-*+]|\d+[.)])\s/.test(l)) fail('nested lists are not supported');
        if (/^\S/.test(l) && blockStart(l)) {
          if ((ordered ? BULLET : NUMBERED).test(lt)) fail('a bullet list and a numbered list must be separated by a blank line');
          break;
        }
        if (/^\t/.test(l)) fail('tabs are not supported in lists');
        items[items.length - 1].text.push(lt); // continuation of the item
        i++;
      }
      blocks.push({ type: 'list', ordered, items: items.map((it) => inline(it.text.join(' '), it.line)) });
      continue;
    }

    // Paragraph: consecutive lines that open no other block.
    const start = lineNo();
    const para = [t.trim()];
    i++;
    while (i < lines.length && !blockStart(lines[i])) para.push(lines[i++].trim());
    if (i < lines.length && /^(?:-{3,}|={3,})\s*$/.test(lines[i].trim())) fail('setext headings and thematic breaks are not supported');
    blocks.push({ type: 'paragraph', inline: inline(para.join(' '), start) });
  }
  return blocks;
}
