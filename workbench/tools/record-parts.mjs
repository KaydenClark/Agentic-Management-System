// Linked sections keep physical records bounded while retaining one logical
// record. Only marked links are includes; ordinary Markdown links stay links.
import fs from 'node:fs';
import path from 'node:path';
import { createHash } from 'node:crypto';
import { assertSafeReadPath, assertSafeWritePath } from './workbench-paths.mjs';
const START = '<!-- workbench-record-section';
const BODY_START = '<!-- workbench-record-body:start -->\n';
const BODY_END = '<!-- workbench-record-body:end -->';
const digest = text => createHash('sha256').update(text).digest('hex');
const count = text => [...text.replace(/\r\n?/g, '\n')].length;
const slug = text => text.trim().toLowerCase().replace(/<[^>]*>/g, '').replace(/&amp;/g, 'and').replace(/[^\p{L}\p{N}_\-\s]/gu, '').replace(/\s+/g, '-') || 'section';
function sections(text) {
  let fence = null, offset = 0;
  const headings = [];
  // Existing physical include blocks already identify their exact section;
  // logical source headings inside a fenced example are never boundaries.
  const physical = text.includes(START);
  for (const line of text.match(/[^\n]*\n|[^\n]+$/g) ?? []) {
    const delimiter = /^\s*(`{3,}|~{3,})/.exec(line)?.[1];
    if (!physical && delimiter) { if (!fence) fence = delimiter; else if (delimiter[0] === fence[0] && delimiter.length >= fence.length) fence = null; }
    if ((physical || !fence) && /^## [^\n]+\n$/.test(line)) headings.push({ name: line.slice(3).trim(), start: offset + line.length, heading: offset });
    offset += line.length;
  }
  return headings.map((heading, i) => ({ name: heading.name, start: heading.start, end: headings[i + 1]?.heading ?? text.length }));
}
function references(body, file) {
  if (!body.includes(START)) return null;
  body = body.replace(/\r\n?/g, '\n');
  const match = /^\s*<!-- workbench-record-section max=(\d+) -->\n([\s\S]*?)<!-- \/workbench-record-section -->\s*$/.exec(body);
  if (!match) throw new Error(`${file}: malformed linked record section`);
  const max = Number(match[1]);
  if (!Number.isSafeInteger(max) || max < 300 || max > 15000) throw new Error(`${file}: invalid linked page budget`);
  const allLines = match[2].trim().split('\n');
  const fields = allLines.filter(line => /^\*\*[^*]+:\*\*.*$/.test(line));
  const anchors = allLines.filter(line => /^<a id=/.test(line));
  for (const anchor of anchors) if (!/^<a id="[a-z0-9_-]+"><\/a> \[[^\]]+\]\([^)]+#[a-z0-9_-]+\)$/.test(anchor)) throw new Error(`${file}: malformed forwarding anchor`);
  const lines = allLines.filter(line => !fields.includes(line) && !anchors.includes(line));
  const names = lines.map((line, index) => {
    const link = /^- \[Part (\d+)\]\(([^)]+)\)$/.exec(line);
    if (!link || Number(link[1]) !== index + 1) throw new Error(`${file}: malformed or unordered record part link`);
    const name = link[2];
    if (path.basename(name) !== name || !name.startsWith(path.basename(file) + '.part-') || !/\.[0-9a-f]{64}\.md$/.test(name)) throw new Error(`${file}: invalid record part path ${name}`);
    return name;
  });
  if (!names.length || new Set(names).size !== names.length) throw new Error(`${file}: empty or duplicate record parts`);
  return { names, max, fields, anchors };
}
export function recordPartPaths(content, file) {
  return sections(content).flatMap(section => references(content.slice(section.start, section.end), file)?.names.map(name => path.join(path.dirname(file), name)) ?? []);
}
function filesystemReader(file, root, { allowHardlinks = false } = {}) {
  assertSafeReadPath(root ?? path.dirname(file), file);
  const stat = fs.lstatSync(file);
  if (!stat.isFile() || stat.isSymbolicLink() || (stat.nlink > 1 && !allowHardlinks)) throw new Error(`${file}: record part must be an ordinary file`);
  return fs.readFileSync(file, 'utf8');
}
function pageBody(page, file, max) {
  const marker = /<!-- workbench-record-body:start(?: context=(\d+))?(?: format=(2))? -->\r?\n/.exec(page);
  const begin = marker?.index ?? -1, end = page.indexOf(BODY_END);
  if (begin < 0 || end < begin || [...page.matchAll(/<!-- workbench-record-body:start/g)].length !== 1 || page.indexOf(BODY_END, end + BODY_END.length) >= 0 || page.slice(end + BODY_END.length).trim()) throw new Error(`${file}: malformed record part body`);
  if (count(page) > max) throw new Error(`${file}: record page exceeds ${max} characters`);
  const full = page.slice(begin + marker[0].length, end);
  const context = Number(marker[1] ?? 0);
  if (!Number.isSafeInteger(context) || context < 0 || context > [...full].length) throw new Error(`${file}: invalid continuation context`);
  let cursor = 0, consumed = 0;
  while (consumed < context && cursor < full.length) {
    if (full[cursor] === '\r' && full[cursor + 1] === '\n') cursor += 2;
    else cursor += full.codePointAt(cursor) > 0xffff ? 2 : 1;
    consumed++;
  }
  const body = full.slice(cursor);
  const expected = /\.([0-9a-f]{64})\.md$/.exec(file)?.[1];
  if (!expected || digest(marker[2] === '2' ? page : body) !== expected) throw new Error(`${file}: immutable record part hash mismatch (altered page)`);
  if (body.includes(START) || body.includes('<!-- workbench-record-body:start') || body.includes(BODY_END)) throw new Error(`${file}: nested record parts are not allowed`);
  return body;
}
export function expandRecordText(content, file, options = {}) {
  if (!content.includes(START)) return content;
  if (!file) throw new Error('Linked record content requires its source path');
  const read = options.readPart ?? (part => filesystemReader(part, options.root));
  const edits = sections(content).flatMap(section => {
    const refs = references(content.slice(section.start, section.end), file);
    if (!refs) return [];
    const body = refs.names.map(name => {
      const part = path.join(path.dirname(file), name);
      return pageBody(read(part), part, refs.max);
    }).join('');
    const fields = [...body.matchAll(/^\*\*[^*]+:\*\*.*$/gm)].map(match => match[0]);
    if (JSON.stringify(refs.fields) !== JSON.stringify(fields)) throw new Error(`${file}: linked record field projection differs from source`);
    for (const anchor of refs.anchors) {
      const [, id, title, target] = /^<a id="([^"]+)"><\/a> \[([^\]]+)\]\(([^)]+)\)$/.exec(anchor);
      const [name, fragment] = target.split('#');
      if (id !== slug(title) || fragment !== id || !refs.names.includes(name) || !body.split('\n').some(line => /^#{3,6} /.test(line) && line.replace(/^#{3,6} /, '') === title)) throw new Error(`${file}: forwarding anchor differs from source`);
      const part = path.join(path.dirname(file), name);
      if (!pageBody(read(part), part, refs.max).split('\n').some(line => /^#{3,6} /.test(line) && line.replace(/^#{3,6} /, '') === title)) throw new Error(`${file}: forwarding anchor points to wrong page`);
    }
    return [{ ...section, body }];
  });
  if (!edits.length || [...content.matchAll(/<!-- workbench-record-section/g)].length !== edits.length) throw new Error(`${file}: record part marker is outside a section`);
  for (const edit of edits.reverse()) content = content.slice(0, edit.start) + edit.body + content.slice(edit.end);
  return content;
}
export function readRecordSection(content, heading, file, root) {
  const section = sections(content).find(section => section.name === heading);
  if (!section) return '';
  return expandRecordText(`## ${heading}\n${content.slice(section.start, section.end)}`, file, { root }).slice(heading.length + 4);
}
// Read-only reference scans may inspect a hardlinked primary to decide whether
// it actually needs rewriting. Immutable detail pages always remain single-link
// files, and mutation callers still preflight the primary with write safety.
export function readRecordText(file, root, { allowPrimaryHardlinks = false } = {}) {
  return expandRecordText(filesystemReader(file, root, { allowHardlinks: allowPrimaryHardlinks }), file, { root });
}
// Preserve accessors when loaders add routing fields; spreading a lazy record
// would read every linked historical page before list/next needs its content.
export function withRecordProperties(record, extra) {
  return Object.defineProperties(extra, Object.getOwnPropertyDescriptors(record));
}
export function lazyRecordContent(record, raw, file, root) {
  let expanded;
  Object.defineProperty(record, 'content', { enumerable: true, configurable: true, get() { return expanded ??= expandRecordText(raw, file, { root }); } });
  return record;
}
function atomic(file, text) {
  const temporary = `${file}.tmp-${process.pid}`;
  try { fs.writeFileSync(temporary, text); fs.renameSync(temporary, file); }
  finally { fs.rmSync(temporary, { force: true }); }
}
function semanticBlocks(body) {
  const lines = body.match(/[^\n]*\n|[^\n]+$/g) ?? [];
  const blocks = [];
  let paragraph = '', fence = null, fenced = '', header = '';
  const flush = () => { if (paragraph) blocks.push({ text: paragraph, context: '' }); paragraph = ''; };
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    const delimiter = /^\s*(`{3,}|~{3,})/.exec(line)?.[1];
    if (fence) {
      fenced += line;
      if (delimiter && delimiter[0] === fence[0] && delimiter.length >= fence.length) { blocks.push({ text: fenced, context: '' }); fence = null; fenced = ''; }
      continue;
    }
    if (delimiter) { flush(); fence = delimiter; fenced = line; header = ''; continue; }
    if (/^\s*\|/.test(line)) {
      flush();
      if (/^\s*\|[ :|-]+\|\s*$/.test(lines[i + 1] ?? '')) { header = line + lines[++i]; blocks.push({ text: header, context: '' }); }
      else blocks.push({ text: line, context: header });
      continue;
    }
    header = '';
    if (/^\s*$/.test(line)) { paragraph += line; flush(); }
    else { if (/^#{3,6} /.test(line)) flush(); paragraph += line; }
  }
  flush();
  if (fenced) blocks.push({ text: fenced, context: '' });
  return blocks;
}
function planPages(file, heading, body, max) {
  if (body.includes(START) || body.includes('<!-- workbench-record-body:start') || body.includes(BODY_END)) throw new Error(`${file}: reserved record marker in source section`);
  const pages = [];
  const links = semanticBlocks(body).filter(block => !/^\s*(`{3,}|~{3,})/.test(block.text)).map(block => block.text).join('').replace(/`[^`]*`/g, '');
  const fragments = [...new Set([...links.matchAll(/\]\(#([a-z0-9_-]+)\)/g)].map(match => match[1]))];
  const routes = fragments.map(fragment => `<a id="${fragment}"></a> [Original section](${path.basename(file)}#${fragment})\n\n`).join('');
  const wrapper = (part, context) => `# ${heading} (part ${part})\n\n[Record](${path.basename(file)}#${slug(heading)})\n\n${routes}<!-- workbench-record-body:start context=${[...context.replace(/\r\n?/g, '\n')].length} format=2 -->\n`;
  let chunk = '', context = '';
  const flush = () => {
    if (!chunk) return;
    const ordinal = String(pages.length + 1).padStart(3, '0');
    const text = wrapper(pages.length + 1, context) + context + chunk + BODY_END + '\n';
    const name = `${path.basename(file)}.part-${slug(heading).slice(0, 40)}-${ordinal}.${digest(text)}.md`;
    pages.push({ file: path.join(path.dirname(file), name), text });
    chunk = ''; context = '';
  };
  for (const block of semanticBlocks(body)) {
    if (count(wrapper(pages.length + 1, context) + context + chunk + block.text + BODY_END + '\n') > max) flush();
    if (!chunk) context = block.context;
    if (count(wrapper(pages.length + 1, context) + context + block.text + BODY_END + '\n') > max) throw new Error(`${file}: one paragraph, table row or fenced block exceeds its ${max}-character page budget; condense it before splitting`);
    chunk += block.text;
  }
  flush();
  return pages;
}
export function planRecordWrite(file, content, options = {}) {
  const root = options.root ?? path.dirname(file);
  const originalFile = options.sourceFile ?? file;
  const original = options.sourceText ?? (fs.existsSync(file) ? filesystemReader(file, root) : '');
  // Validate every existing page before planning a mutation.
  expandRecordText(original, originalFile, { root });
  const selected = new Map(sections(original).flatMap(section => { const ref = references(original.slice(section.start, section.end), originalFile); return ref ? [[section.name, ref.max]] : []; }));
  for (const name of options.sections ?? []) selected.set(name, options.maxPageCharacters ?? 15000);
  content = expandRecordText(content, file, { root });
  const pages = [];
  const edits = [];
  const oldAnchors = sections(original).flatMap(section => references(original.slice(section.start, section.end), originalFile)?.anchors ?? []).map(anchor => /^<a id="[^"]+"><\/a> \[([^\]]+)\]/.exec(anchor)[1]);
  const forward = new Set([...(options.forwardAnchors ?? []), ...oldAnchors]);
  for (const section of sections(content)) {
    if (!selected.has(section.name)) continue;
    const max = options.maxPageCharacters ?? selected.get(section.name);
    const parts = planPages(file, section.name, content.slice(section.start, section.end), max);
    if (!parts.length) continue;
    pages.push(...parts);
    const fields = [...content.slice(section.start, section.end).matchAll(/^\*\*[^*]+:\*\*.*$/gm)].map(match => match[0]);
    let projection = fields.length ? fields.join('\n') + '\n' : '';
    for (const title of forward) {
      const part = parts.find(part => pageBody(part.text, part.file, max).split('\n').some(line => /^#{3,6} /.test(line) && line.replace(/^#{3,6} /, '') === title));
      if (part) projection += `<a id="${slug(title)}"></a> [${title}](${path.basename(part.file)}#${slug(title)})\n`;
    }
    edits.push({ ...section, body: `\n<!-- workbench-record-section max=${max} -->\n${projection}${parts.map((part, index) => `- [Part ${index + 1}](${path.basename(part.file)})`).join('\n')}\n<!-- /workbench-record-section -->\n\n` });
  }
  const logicalLength = content.length;
  for (const edit of edits.reverse()) content = content.slice(0, edit.start) + edit.body + content.slice(edit.end);
  if (edits.some(edit => edit.end === logicalLength)) content = content.replace(/\n{2,}$/, '\n');
  assertSafeWritePath(root, file);
  for (const page of pages) {
    assertSafeWritePath(root, page.file);
    if (fs.existsSync(page.file) && filesystemReader(page.file, root) !== page.text) throw new Error(`${page.file}: existing immutable page differs`);
  }
  return { file, content, original, pages, previousParts: recordPartPaths(original, originalFile), characters: count(content) };
}
export function writeRecordText(file, logical, options = {}) {
  const { content, original, pages, previousParts, characters } = planRecordWrite(file, logical, options);
  // Pages are immutable and complete before the only reference to them changes.
  // A stopped write can leave an unreferenced page, never a half-written record.
  if (options.dryRun) return { file, parts: pages.map(page => page.file), characters };
  for (const page of pages) if (!fs.existsSync(page.file)) atomic(page.file, page.text);
  (options.writePrimary ?? atomic)(file, content);
  const currentParts = new Set(pages.map(page => page.file));
  for (const previous of previousParts) if (!currentParts.has(previous)) fs.unlinkSync(previous);
  return { file, parts: pages.map(page => page.file), characters: count(content) };
}
export function paginateRecord(file, options = {}) {
  return writeRecordText(file, readRecordText(file, options.root), options);
}

export function isRecordPartPath(file) { return /\.md\.part-[^/]+\.[0-9a-f]{64}\.md$/.test(file); }
export function verifiedRecordPart(file, root) {
  if (!isRecordPartPath(file)) return false;
  const parent = file.slice(0, file.indexOf('.md.part-') + 3);
  const raw = filesystemReader(parent, root);
  if (!recordPartPaths(raw, parent).includes(path.resolve(file))) throw new Error(`${file}: unreferenced record part`);
  readRecordText(parent, root);
  return true;
}

export function recordSections(text) { return sections(text); }
