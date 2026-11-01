#!/usr/bin/env node
// Small, source-labelled capture inside the existing Wiki. The Markdown claim
// text is stored once; its labels never supply authority or implementation proof.
import fs from 'node:fs';
import { readRecordText, writeRecordText, isRecordPartPath } from './record-parts.mjs';
import path from 'node:path';
import crypto from 'node:crypto';
import { spawnSync } from 'node:child_process';
import { assertSafeReadPath, assertSafeWritePath, findRoot, isMainModule, lanePath, laneRelative, liveRecordPath, writeSafeFile } from './workbench-paths.mjs';
import { parseFrontmatter } from './adr.mjs';
import { scanPrivacy } from './privacy.mjs';
import { checkStructure, listNotes, readNote, resolveNote } from './notepads.mjs';

export const JOT_KINDS = Object.freeze(['intent', 'observation', 'inference', 'proposal', 'question', 'verification']);
export const JOT_STATES = Object.freeze(['current', 'confirmed', 'unresolved', 'experimental']);
const START = '<!-- jot-entry -->';
const END = '<!-- /jot-entry -->';
const SLUG = /^[a-z0-9]+(?:-[a-z0-9]+)*$/;
const digest = (value) => crypto.createHash('sha256').update(value).digest('hex');
const own = (value, key) => Object.prototype.hasOwnProperty.call(value, key);
function fail(code, message) { const error = new Error(message); error.code = code; throw error; }
function result(action) { try { return action(); } catch (error) { return { status: 'blocked', error: { code: error.code ?? 'invalid-invocation', message: error.message } }; } }
function line(value, name, maximum = 500) {
  if (typeof value !== 'string' || !value.trim() || value.length > maximum || /[\r\n]/.test(value) || value.includes('<!--')) fail('invalid-entry', `${name} must be a nonempty single line of at most ${maximum} characters`);
  return value.trim();
}
function privacy(value) { if (scanPrivacy(value).length) fail('secret-like-content', 'Secret-like or excluded personal material was refused; the matched value is not echoed'); }
function git(root, args) {
  const run = spawnSync('git', ['-C', root, ...args], { encoding: 'utf8' });
  if (run.error) fail('git-unavailable', 'Git is required to verify private access boundaries');
  return run;
}
function ignored(root, relative) {
  const checked = git(root, ['check-ignore', '--quiet', '--no-index', '--', relative]);
  if (![0, 1].includes(checked.status)) fail('git-unavailable', 'Git is required to verify ignored provenance');
  return checked.status === 0;
}
function privateBoundary(root, relative) {
  const tracked = git(root, ['ls-files', '--error-unmatch', '--', relative]);
  if (tracked.status === 0) fail('private-tracked', 'Private capture refuses a tracked destination');
  if (tracked.status !== 1) fail('git-unavailable', 'Private capture requires a readable Git index');
  if (!ignored(root, relative)) fail('private-not-ignored', 'Private Wiki capture must be ignored before writing; use the supplied Wiki ignore rule');
}
function location(root, options, writing = false) {
  if (fs.lstatSync(path.resolve(root)).isSymbolicLink()) fail('unsafe-path', 'The selected project root must be an ordinary directory, not a symlink');
  const wiki = lanePath(root, 'wiki');
  const visibility = options.visibility ?? 'shared';
  if (!['shared', 'private'].includes(visibility)) fail('invalid-entry', 'visibility must be shared or private');
  const topic = options.topic;
  if (topic !== undefined && !SLUG.test(topic)) fail('invalid-entry', 'topic must be a lowercase hyphenated slug');
  const relative = options.page ?? (topic ? `${laneRelative(root, 'wiki')}/${visibility === 'private' ? '.jot-private-' : 'context-'}${topic}.md` : null);
  if (!relative || path.isAbsolute(relative) || relative.includes('\\') || relative.split('/').includes('..')) fail('unsafe-path', 'Choose a repository-relative Wiki Markdown page or a topic slug');
  const absolute = path.resolve(root, relative);
  const within = path.relative(wiki, absolute);
  if (!within || within.startsWith('..') || path.isAbsolute(within) || !within.endsWith('.md')) fail('unsafe-path', 'A jot belongs to a Markdown page inside the declared Wiki');
  if (['MEMORY.md', 'SCHEMA.md', 'AGENTS.md'].includes(within) || within.split('/').includes('archive') || within.split('/').includes('skills-draft')) fail('unsafe-path', 'Capture uses an active topic owner, not a router, contract or historical collection');
  const privateFile = /^\.jot-private-[a-z0-9]+(?:-[a-z0-9]+)*\.md$/.test(within);
  if (within.split('/').some(part => part.startsWith('.')) && !privateFile) fail('unsafe-path', 'Only the named private Wiki capture pattern is supported');
  if (privateFile && visibility !== 'private' && !options['include-private']) fail('private-access', 'Private Wiki capture requires explicit local access');
  if (writing && visibility === 'private' && !privateFile) fail('private-access', 'Private captures use ignored .jot-private-<topic>.md Wiki pages');
  if (writing && visibility === 'shared' && privateFile) fail('private-access', 'A private Wiki page cannot become shared through capture');
  assertSafeReadPath(root, absolute);
  if (writing) assertSafeWritePath(root, absolute);
  const localIgnored = ignored(root, relative);
  const privateAccess = visibility === 'private' || options['include-private'] === true;
  if (localIgnored && (writing && visibility === 'shared' || !writing && !privateAccess)) fail('private-access', 'Ignored Wiki context remains local; shared capture is refused and reading requires explicit private access');
  if (writing && privateFile) privateBoundary(root, relative);
  return { absolute, relative, privateFile, localIgnored, privateAccess, topic: topic ?? path.basename(within, '.md').replace(/^(?:context-|\.jot-private-)/, ''), visibility: !writing && (privateFile || localIgnored) ? 'private' : visibility };
}
function sourceReference(root, reference, visibility) {
  const source = line(reference, 'source');
  privacy(source);
  if (/^https?:\/\//.test(source)) {
    const url = new URL(source);
    if (url.username || url.password) fail('private-source', 'Credential-bearing source URLs are refused');
    return source;
  }
  if (/^[A-Za-z][A-Za-z0-9_-]*:[A-Za-z0-9_-]+$/.test(source)) {
    if (visibility === 'shared' && /^(private|restricted|local):/i.test(source)) fail('private-source', 'A local/private source cannot enter shared capture');
    return source;
  }
  if (source.includes(':')) fail('unsafe-path', 'Opaque source references use a named namespace and a path-free identifier');
  const file = source.split('#')[0];
  if (path.isAbsolute(file) || /^[A-Za-z]:/.test(file) || file.includes('\\') || file.split('/').includes('..')) fail('unsafe-path', 'Source paths must be repository-relative');
  assertSafeReadPath(root, path.resolve(root, file));
  if (visibility === 'shared') {
    if (liveRecordPath(root, file) || ignored(root, file) || /(?:^|\/)\.jot-private-/.test(file)) fail('private-source', 'Ignored or private provenance cannot enter shared capture');
    if (fs.existsSync(path.resolve(root, file)) && file.endsWith('.md')) {
      const { data } = parseFrontmatter(fs.readFileSync(path.resolve(root, file), 'utf8'));
      if (data?.sensitivity && data.sensitivity !== 'normal') fail('private-source', 'Private or restricted Wiki provenance cannot enter shared capture');
    }
  }
  return source;
}
function parseEntries(text) {
  // Only native entries are parsed here; a preserved historical JSON string
  // can itself mention the delimiters without becoming a new entry.
  text = text.replace(/<!-- jot-legacy-source (\{[^\n]+\}) -->\n```json\n([\s\S]*?)\n```\n<!-- \/jot-legacy-source -->/g, '').replace(/\r\n?/g, '\n');
  const entries = [];
  const pattern = /<!-- jot-entry -->\n### ([A-Za-z0-9_-]+)\nKind: ([^\n]+)\nState: ([^\n]+)\nRecorded: ([^\n]+)\nAuthor: ([^\n]+)\nSource: ([^\n]+)\nTopic: ([^\n]+)\nSupersedes: ([^\n]+)\n\n([\s\S]*?)\n<!-- \/jot-entry -->/g;
  for (const match of text.matchAll(pattern)) {
    const [, id, kind, state, at, author, source, topic, previous, content] = match;
    if (!JOT_KINDS.includes(kind) || !JOT_STATES.includes(state) || entries.some(entry => entry.id === id) || !Number.isFinite(Date.parse(at))) fail('invalid-page', 'The Wiki page contains invalid or duplicate jot metadata');
    const supersedes = previous === 'none' ? null : previous;
    entries.push({ id, kind, state, at, author, source, topic, supersedes, content });
  }
  if (text.split(START).length - 1 !== entries.length || text.split(END).length - 1 !== entries.length) fail('invalid-page', 'The Wiki page contains a malformed jot boundary');
  return entries;
}
// S-006J TK-008R: the lifecycle authority check reads the same native entries
// and applies this reader's ignored-page rule: an ignored page is local
// context. Outside a Git work tree no ignore rule can apply.
export function parseJotEntries(text) { return parseEntries(text); }
export function ignoredJotPage(root, relative) {
  const inside = spawnSync('git', ['-C', root, 'rev-parse', '--is-inside-work-tree'], { encoding: 'utf8' });
  if (inside.error) fail('git-unavailable', 'Git is required to verify ignored provenance');
  if (inside.status !== 0) return false;
  return ignored(root, relative);
}
function legacySnapshot(text) {
  const match = text.match(/<!-- jot-legacy-source (\{[^\n]+\}) -->\n```json\n([\s\S]*?)\n```\n<!-- \/jot-legacy-source -->/);
  if (!match) return null;
  const metadata = JSON.parse(match[1]);
  if (digest(match[2]) !== metadata.sha256) fail('invalid-page', 'The preserved legacy snapshot hash does not match');
  const note = JSON.parse(match[2]);
  const checked = checkStructure(note);
  if (checked.missing.length || checked.invalid.length) fail('invalid-page', 'The preserved legacy snapshot is not a supported note');
  return { metadata, note };
}
function load(root, target) {
  if (!fs.existsSync(target.absolute)) return { text: '', revision: null, entries: [] };
  const text = readRecordText(target.absolute, root);
  const { data } = parseFrontmatter(text);
  if (!data || !data.sensitivity || !data.knowledge_role) fail('invalid-page', 'Capture requires an existing Wiki page with handling metadata');
  if (data.sensitivity !== 'normal' && !target.privateFile && !(data.sensitivity === 'private' && target.localIgnored && target.privateAccess)) fail('private-access', 'Private/restricted existing pages remain outside shared capture');
  if (target.privateFile && data.sensitivity !== 'private') fail('private-access', 'A private capture page must retain private sensitivity');
  const native = parseEntries(text);
  const entries = [];
  const snapshot = legacySnapshot(text);
  if (snapshot) {
    if (!target.privateFile) fail('private-access', 'A legacy snapshot must remain in private Wiki capture');
    const prefix = `LEGACY-${digest(target.relative).slice(0, 16)}-`;
    for (const entry of snapshot.note.entries) entries.push({ id: `${prefix}${entry.id}`, kind: entry.kind, state: snapshot.note.status, at: entry.at ?? snapshot.note.created_at, author: 'Preserved legacy source', source: `${snapshot.metadata.note}#${entry.id}`, topic: entry.topic ?? target.topic, supersedes: entry.corrects ? `${prefix}${entry.corrects}` : null, content: entry.content, classification: 'historical-legacy', original_id: entry.id, legacy_kind: entry.kind, state_scope: 'legacy-note' });
  }
  for (const entry of native) {
    if (entry.supersedes && !entries.some(previous => previous.id === entry.supersedes)) fail('invalid-page', 'A correction must follow the entry it supersedes');
    if (entries.some(previous => previous.id === entry.id)) fail('invalid-page', 'The page contains duplicate entry identity');
    entries.push(entry);
  }
  return { text, revision: digest(text), entries, snapshot, data };
}
function entryText(entry) {
  return `${START}\n### ${entry.id}\nKind: ${entry.kind}\nState: ${entry.state}\nRecorded: ${entry.at}\nAuthor: ${entry.author}\nSource: ${entry.source}\nTopic: ${entry.topic}\nSupersedes: ${entry.supersedes ?? 'none'}\n\n${entry.content}\n${END}\n`;
}
function newPage(target, title) {
  privacy(title);
  return `---\ntype: project\nstatus: partial\nsensitivity: ${target.privateFile ? 'private' : 'normal'}\nknowledge_role: curated\nprovenance:\n  - /jot capture; each claim names its source and date\nsource_paths: []\nlast_verified: ${new Date().toISOString().slice(0, 10)}\n---\n\n# ${title}\n\nCaptured context. Claim labels preserve intent and uncertainty; capture alone supplies neither Canon nor implementation proof. The date above checks this page's capture format, not every claim.\n`;
}
function publish(root, target, before, after) {
  const lock = path.join(path.dirname(target.absolute), `.jot-write-${digest(target.relative).slice(0, 16)}`);
  const occupied = () => {
    try {
      assertSafeReadPath(root, lock);
      const entry = fs.lstatSync(lock);
      if (!entry.isDirectory()) fail('unsafe-path', 'The capture publication lock is not an ordinary directory');
      return true;
    } catch (error) {
      if (error.code === 'ENOENT') return false;
      if (!error.code) fail('unsafe-path', 'The capture publication lock has an unsafe linked path');
      throw error;
    }
  };
  if (occupied()) fail('concurrent-write', 'Another capture holds this page; retry after it completes, or inspect an abandoned lock');
  assertSafeWritePath(root, path.join(lock, 'content'));
  fs.mkdirSync(path.dirname(lock), { recursive: true });
  try { fs.mkdirSync(lock); } catch (error) { if (error.code === 'EEXIST' && occupied()) fail('concurrent-write', 'Another capture holds this page; retry after it completes, or inspect an abandoned lock'); throw error; }
  const ownership = fs.lstatSync(lock);
  try {
    const current = fs.existsSync(target.absolute) ? readRecordText(target.absolute, root) : '';
    if (current !== before) fail('stale-revision', 'The page changed during capture; read its revision and retry');
    if (target.privateFile) privateBoundary(root, target.relative);
    writeRecordText(target.absolute, after, { root, writePrimary: (file, content) => writeSafeFile(root, file, content, { exclusive: !before, stagingDir: lock }) });
  } finally {
    // Do not remove a directory another writer substituted at the same path.
    try {
      const current = fs.lstatSync(lock);
      if (current.isDirectory() && current.dev === ownership.dev && current.ino === ownership.ino) fs.rmSync(lock, { recursive: true, force: true });
    } catch (error) { if (error.code !== 'ENOENT') throw error; }
  }
}
export function addJot(root, options = {}) {
  return result(() => {
    const target = location(root, options, true);
    const loaded = load(root, target);
    if (loaded.revision !== null && options.revision !== loaded.revision) fail('stale-revision', 'Read the current page revision before appending');
    if (loaded.revision === null && options.revision) fail('stale-revision', 'The requested page no longer exists');
    if (!loaded.text && path.dirname(target.absolute) !== lanePath(root, 'wiki')) fail('unsafe-path', 'New capture pages stay flat beside the Wiki router');
    const previous = options.supersedes ? loaded.entries.find(entry => entry.id === options.supersedes) : null;
    if (options.supersedes && (!previous || loaded.entries.some(entry => entry.supersedes === previous.id))) fail('invalid-entry', 'Correct an existing current entry, retaining the earlier correction chain');
    const kind = options.kind ?? previous?.kind;
    const state = options.state ?? 'unresolved';
    if (!JOT_KINDS.includes(kind) || !JOT_STATES.includes(state)) fail('invalid-entry', 'Choose a supported claim kind and state');
    const author = line(options.author, 'author', 120);
    const content = typeof options.content === 'string' ? options.content.trim() : '';
    if (!content || content.length > 12000 || content.includes('<!-- jot-') || content.includes('<!-- /jot-')) fail('invalid-entry', 'Capture requires a small nonempty claim without reserved jot boundaries');
    const source = sourceReference(root, options.source, target.visibility);
    privacy(`${author}\n${content}`);
    const entry = { id: `JOT-${crypto.randomUUID()}`, kind, state, at: new Date().toISOString(), author, source, topic: options.topic ?? previous?.topic ?? target.topic, supersedes: previous?.id ?? null, content };
    let ownerText = loaded.text || newPage(target, line(options.title ?? target.topic, 'title', 120));
    if (loaded.data?.type === 'design-concept') {
      const operation = line(options.operation, 'operation', 240);
      privacy(operation);
      if (!loaded.data.authorized_by || !/^## History\s*$/m.test(ownerText)) fail('unsupported-owner', 'A Design Concept capture requires its existing authorized_by and History conventions');
      const history = `- ${entry.at.slice(0, 10)}: /jot in ${operation}; ${author} captured ${entry.id}, sourced from ${source}.\n`;
      const section = /^## History[^\n]*\n/gm.exec(ownerText);
      const next = ownerText.slice(section.index + section[0].length).search(/^## /m);
      const end = next < 0 ? ownerText.length : section.index + section[0].length + next;
      ownerText = `${ownerText.slice(0, end).trimEnd()}\n${history}\n${ownerText.slice(end)}`;
    }
    const text = `${ownerText}\n${entryText(entry)}`;
    publish(root, target, loaded.text, text);
    return { status: 'added', page: target.relative, visibility: target.visibility, revision: digest(text), entry };
  });
}
export function correctJot(root, options = {}) {
  if (!options.supersedes) return { status: 'blocked', error: { code: 'invalid-entry', message: 'A correction names the entry it supersedes' } };
  return addJot(root, options);
}
function bound(entries, options, extra = {}) {
  const limit = Number(options.limit ?? 8);
  const maximum = Number(options['max-chars'] ?? 6000);
  if (!Number.isSafeInteger(limit) || limit < 1 || limit > 100 || !Number.isSafeInteger(maximum) || maximum < 1 || maximum > 48000) fail('invalid-entry', 'limit is 1..100 and max-chars is 1..48000');
  const key = (entry, id = entry.id) => `${entry.page ?? ''}#${id}`;
  const byId = new Map(entries.map(entry => [key(entry), entry]));
  const newer = new Map(entries.filter(entry => entry.supersedes).map(entry => [key(entry, entry.supersedes), entry.id]));
  const queryMatch = (entry) => !options.query || `${entry.topic} ${entry.content} ${entry.kind} ${entry.state}`.toLowerCase().includes(options.query.toLowerCase());
  const relevant = (entry) => {
    let current = entry;
    const seen = new Set();
    while (current && !seen.has(key(current))) {
      if (queryMatch(current)) return true;
      seen.add(key(current)); current = byId.get(key(current, current.supersedes));
    }
    return false;
  };
  const matches = entries.filter(entry => (options.id ? entry.id === options.id : !newer.has(key(entry))) && (!options.topic || entry.topic === options.topic) && relevant(entry));
  const selected = matches.slice(-limit).reverse();
  const history = new Map();
  let historyTotal = 0;
  for (const entry of selected) {
    let id = entry.supersedes;
    const seen = new Set();
    while (id && byId.has(key(entry, id)) && !seen.has(id)) {
      seen.add(id); historyTotal++;
      const previous = byId.get(key(entry, id));
      if (history.size < limit && !selected.some(item => key(item) === key(entry, id))) history.set(key(entry, id), previous);
      id = previous.supersedes;
    }
  }
  let budget = maximum;
  let truncated = 0;
  const trim = (entry) => {
    const content = entry.content.slice(0, budget);
    budget -= content.length;
    truncated += entry.content.length - content.length;
    return { ...entry, ...(newer.has(key(entry)) ? { state: 'superseded', recorded_state: entry.state, superseded_by: newer.get(key(entry)) } : {}), content, content_truncated: content.length < entry.content.length };
  };
  const selectedEntries = selected.map(trim);
  const correctionContext = [...history.values()].map(trim);
  return { status: 'read', ...extra, entries: selectedEntries, correction_context: correctionContext, total_matches: matches.length, omitted: Math.max(0, matches.length - selected.length), history_omitted: Math.max(0, historyTotal - history.size), truncated_chars: truncated, ...(truncated || historyTotal > history.size ? { continuation: 'Read the named entry with --id and a larger bound for omitted claim text or correction history.' } : {}) };
}
export function readJots(root, options = {}) {
  return result(() => {
    const target = location(root, options);
    const loaded = load(root, target);
    const output = bound(loaded.entries, options, { page: target.relative, visibility: target.visibility, revision: loaded.revision, ...(loaded.snapshot ? { legacy_source: loaded.snapshot.metadata, legacy_status: loaded.snapshot.note.status } : {}) });
    if (loaded.snapshot) {
      const serialized = JSON.stringify(loaded.snapshot.note.current);
      const used = [...output.entries, ...output.correction_context].reduce((total, entry) => total + entry.content.length, 0);
      const remaining = Math.max(0, Number(options['max-chars'] ?? 6000) - used);
      output.legacy_current_view = { serialized: serialized.slice(0, remaining), truncated_chars: Math.max(0, serialized.length - remaining), continuation: `jot.mjs legacy-read --note ${loaded.snapshot.metadata.note} --view current` };
    }
    return output;
  });
}
export function searchJots(root, options = {}) {
  return result(() => {
    const entries = [];
    const wiki = lanePath(root, 'wiki');
    const privateAccess = options['include-private'] === true || options.visibility === 'private';
    // Read handling metadata only, stopping at the closing frontmatter line.
    // Excluded private/restricted topic bodies never enter shared discovery.
    function handling(absolute) {
      assertSafeReadPath(root, absolute);
      const descriptor = fs.openSync(absolute, 'r');
      const bytes = [];
      const byte = Buffer.alloc(1);
      let lines = 0;
      let current = [];
      try {
        while (bytes.length < 16384 && fs.readSync(descriptor, byte, 0, 1, null)) {
          bytes.push(byte[0]); current.push(byte[0]);
          if (byte[0] !== 10) continue;
          const text = Buffer.from(current).toString('utf8').trimEnd();
          current = []; lines++;
          if (lines === 1 && text !== '---') return null;
          if (lines > 1 && text === '---') return parseFrontmatter(Buffer.from(bytes).toString('utf8')).data;
        }
        return null;
      } finally { fs.closeSync(descriptor); }
    }
    function walk(directory) {
      assertSafeReadPath(root, directory);
      for (const file of fs.readdirSync(directory, { withFileTypes: true })) {
        if (file.isSymbolicLink() || ['archive', 'skills-draft'].includes(file.name)) continue;
        const privateFile = file.name.startsWith('.jot-private-') && file.name.endsWith('.md');
        if (file.name.startsWith('.') && !(privateFile && privateAccess)) continue;
        const absolute = path.join(directory, file.name);
        const relative = path.relative(root, absolute).split(path.sep).join('/');
        const localIgnored = ignored(root, relative);
        if (localIgnored && !privateAccess) continue;
        if (file.isDirectory()) { walk(absolute); continue; }
        if (isRecordPartPath(absolute)) continue;
        if (!file.isFile() || !file.name.endsWith('.md') || ['MEMORY.md', 'SCHEMA.md', 'AGENTS.md'].includes(file.name)) continue;
        const metadata = handling(absolute);
        if (metadata?.sensitivity === 'restricted' || metadata?.sensitivity === 'private' && !(privateAccess && (privateFile || localIgnored))) continue;
        const text = readRecordText(absolute, root);
        if (!text.includes(START) && !text.includes('<!-- jot-legacy-source ')) continue;
        const target = location(root, { page: relative, visibility: privateFile || localIgnored ? 'private' : 'shared', 'include-private': privateAccess });
        const loaded = load(root, target);
        for (const entry of loaded.entries) entries.push({ ...entry, page: relative, visibility: target.visibility });
      }
    }
    walk(wiki);
    entries.sort((left, right) => left.at.localeCompare(right.at) || left.id.localeCompare(right.id));
    return bound(entries, options);
  });
}
export function listLegacyNotes(root, options = {}) {
  return result(() => {
    const listed = listNotes(root, options);
    if (listed.status === 'blocked') return listed;
    return { ...listed, notes: listed.notes.map(note => {
      const resolved = resolveNote(root, note.note, note.collection);
      return { ...note, sha256: digest(fs.readFileSync(resolved.absolute)), visibility: 'private-local', migration: 'original retained; private Wiki only' };
    }) };
  });
}
export function readLegacyNote(root, options = {}) { return readNote(root, options); }
export function importLegacyNote(root, options = {}) {
  return result(() => {
    if (options.visibility && options.visibility !== 'private') fail('private-migration', 'Legacy records can only be imported into ignored private Wiki; shared exposure needs separate specific approval');
    const resolved = resolveNote(root, options.note, options.collection);
    const original = fs.readFileSync(resolved.absolute);
    const bytes = original.toString('utf8');
    if (!Buffer.from(bytes, 'utf8').equals(original)) fail('unsupported-encoding', 'Legacy import requires lossless UTF-8; the original bytes were preserved and no destination was written');
    const note = JSON.parse(bytes);
    const checked = checkStructure(note);
    if (checked.missing.length || checked.invalid.length) fail('invalid-note', 'Only supported legacy records can be imported');
    privacy(bytes);
    const target = location(root, { ...options, visibility: 'private' }, true);
    if (fs.existsSync(target.absolute)) fail('destination-exists', 'An import creates a separate private Wiki page; the existing page and original are preserved');
    const metadata = { note: resolved.relative, sha256: digest(original), imported_at: new Date().toISOString(), schema_version: note.schema_version };
    const text = `${newPage(target, line(options.title ?? target.topic, 'title', 120))}\n## Preserved Legacy Source\n\nHistorical source snapshot. Original kind, status, revisions, current context and correction links are retained below and in retrieval. These are legacy classifications, not new claim confirmations. A legacy decision label alone does not prove owner intent, implementation or Canon. The original file remains unchanged.\n\n<!-- jot-legacy-source ${JSON.stringify(metadata)} -->\n\`\`\`json\n${bytes}\n\`\`\`\n<!-- /jot-legacy-source -->\n`;
    publish(root, target, '', text);
    return { status: 'imported', page: target.relative, revision: digest(text), source: resolved.relative, source_sha256: metadata.sha256, original_preserved: true, reversible: 'Original remains the source; stop using the import to revert.' };
  });
}
const COMMANDS = { add: addJot, correct: correctJot, read: readJots, search: searchJots, 'legacy-list': listLegacyNotes, 'legacy-read': readLegacyNote, 'import-legacy': importLegacyNote };
const VALUES = new Set(['path', 'page', 'topic', 'visibility', 'kind', 'state', 'source', 'author', 'content', 'title', 'revision', 'supersedes', 'operation', 'limit', 'max-chars', 'query', 'id', 'note', 'collection', 'view']);
function parseArgs(argv) {
  const command = argv.shift();
  if (!own(COMMANDS, command)) fail('invalid-invocation', 'Usage: jot.mjs add|correct|read|search|legacy-list|legacy-read|import-legacy [options]');
  const options = {};
  while (argv.length) {
    const flag = argv.shift();
    if (!flag.startsWith('--')) fail('invalid-invocation', 'Options use --name value');
    const key = flag.slice(2);
    if (own(options, key)) fail('invalid-invocation', `Duplicate option --${key}`);
    if (key === 'include-private') options[key] = true;
    else {
      if (!VALUES.has(key) || !argv.length || argv[0].startsWith('--')) fail('invalid-invocation', `Unknown option or missing value: --${key}`);
      options[key] = argv.shift();
    }
  }
  return { command, options };
}
if (isMainModule(import.meta.url)) {
  const output = result(() => { const { command, options } = parseArgs(process.argv.slice(2)); return COMMANDS[command](findRoot(options.path ?? process.cwd()), options); });
  process.stdout.write(`${JSON.stringify(output)}\n`);
  if (output.status === 'blocked') process.exitCode = 1;
}
