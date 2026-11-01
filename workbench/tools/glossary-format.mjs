// The pinned glossary format, parsed whole, and the identity of the room's
// vocabulary controls. A dependency-free module so the Wiki validator, glossary
// promotion, the Lexicon retirement check and adoption share one parser and one
// answer to "is this path the canonical room-root control"; a malformed
// glossary throws an Error naming the violated rule.
import fs from 'node:fs';
import path from 'node:path';

// PR431 round 4 (comments 4312687900, 4312687917, 4312687933): four review
// rounds each found a new edge where one consumer's own textual check admitted
// a glossary, architecture or Lexicon control that was not the room's file:
// a symlink, a shared hard link, a same-named file reached by `../` from a
// nested article. Every consumer now asks here. A room file is canonical when
// it is an ordinary regular file (lstat, never followed), shared with no other
// name (nlink 1) and really at `<roomRoot>/<relative>` (realpath of both). The
// result is reported, never thrown: `exists` separates an absent file from a
// present one that is refused, and `reason` is the text a finding names.
export function canonicalRoomFile(roomRoot, relative) {
  const root = path.resolve(roomRoot);
  const file = path.join(root, relative);
  const refuse = (exists, reason) => ({ canonical: false, exists, reason, path: file });
  let entry;
  try { entry = fs.lstatSync(file); } catch (error) {
    return refuse(false, error.code === 'ENOENT' || error.code === 'ENOTDIR' ? 'absent' : `unreadable (${error.code})`);
  }
  if (entry.isSymbolicLink()) return refuse(true, 'a symbolic link');
  if (!entry.isFile()) return refuse(true, 'not a regular file');
  if (entry.nlink !== 1) return refuse(true, `shared by ${entry.nlink} hard links`);
  let real, realRoot;
  try { real = fs.realpathSync(file); realRoot = fs.realpathSync(root); } catch (error) { return refuse(true, `unresolvable (${error.code})`); }
  if (real !== path.join(realRoot, relative)) return refuse(true, `not at the room root (${real})`);
  return { canonical: true, exists: true, reason: null, path: file };
}

// A Markdown link from `sourceFile` reaches the room-root control `name` only
// when its target, resolved from the source file's own directory, is exactly
// `<roomRoot>/<name>`. The `../` count is never read on its own: the same
// `../../<name>` reaches the root from `workbench/wiki/article.md` and
// `workbench/<name>` from `workbench/wiki/nested/article.md`. A fragment
// is dropped, and an absolute, scheme or empty target is never a room route.
// Whether that control is itself canonical is `canonicalRoomFile`'s answer.
export function linkResolvesToRootControl(roomRoot, sourceFile, target, name) {
  if (typeof target !== 'string') return false;
  let value = target.trim().replace(/^<(.*)>$/, '$1').split('#')[0];
  if (!value || path.isAbsolute(value) || /^[a-z][a-z0-9+.-]*:/i.test(value)) return false;
  try { value = decodeURIComponent(value); } catch { /* a literal percent stays literal */ }
  return path.resolve(path.dirname(path.resolve(sourceFile)), value) === path.join(path.resolve(roomRoot), name);
}

// A grouped vocabulary article explains several terms under `## Term`
// sections without declaring one `glossary_term`: the `vocabulary-*.md` pages
// the Template installs directly at the Wiki lane root. The retirement report
// reads a term's heading section only there (PR431 comment 4315959826), and
// the Wiki validator requires the same pages to link the room-root glossary
// (comment 4315959839). Both paths are room-relative with `/` separators.
export function isGroupedVocabularyArticle(file, wikiLane) {
  return path.posix.dirname(file) === wikiLane && /^vocabulary-[a-z0-9]+(?:-[a-z0-9]+)*\.md$/.test(path.posix.basename(file));
}

const requireFormat = (condition, message) => { if (!condition) throw new Error(message); };
const sentenceCount = (text) => (text.match(/[.!?][)\]"'`*]*(?=\s|$)/g) ?? []).length || 1;

export function parseGlossary(content, label) {
  const lines = content.replace(/\r\n/g, '\n').replace(/\n+$/, '').split('\n');
  let index = 0;
  const next = () => lines[index] ?? '';
  const skipBlank = () => { while (index < lines.length && next().trim() === '') index += 1; };
  const heading = next().match(/^# (\S.*)$/);
  requireFormat(heading, `${label}: opens with a context heading`);
  index += 1;
  skipBlank();
  // A generated Template carries its release stamp before the description.
  while (next().startsWith('> ')) { index += 1; skipBlank(); }
  const description = [];
  while (index < lines.length && next().trim() !== '' && !next().startsWith('#')) description.push(lines[index++]);
  requireFormat(description.length, `${label}: has a context description under the heading`);
  requireFormat(sentenceCount(description.join(' ')) <= 2, `${label}: the context description is one or two sentences`);
  skipBlank();
  requireFormat(next() === '## Language', `${label}: the context description is followed by the Language section`);
  index += 1;
  const entries = [];
  let group = null;
  let groupStarted = false;
  while (index < lines.length) {
    skipBlank();
    if (index >= lines.length) break;
    const line = next();
    const groupHeading = line.match(/^### (\S.*)$/);
    if (groupHeading) { group = groupHeading[1]; groupStarted = false; index += 1; continue; }
    requireFormat(!/^#{1,2} /.test(line), `${label}: no section other than Language (${line})`);
    const term = line.match(/^\*\*([^*].*?)\*\*:$/);
    if (!term) {
      // One short note may open a grouping before its first entry. A heading
      // of any level is never that note (PR431 comment 4312850574).
      requireFormat(group && !groupStarted && !line.startsWith('_Avoid_') && !line.startsWith('**') && !line.startsWith('#') && sentenceCount(line) <= 2 && (lines[index + 1] ?? '').trim() === '',
        `${label}: unexpected line in Language: ${line}`);
      groupStarted = true;
      index += 1;
      continue;
    }
    groupStarted = true;
    index += 1;
    const definition = next();
    requireFormat(definition.trim() && !/^(\*\*|_Avoid_|#)/.test(definition), `${label}: ${term[1]} has a definition line under its term`);
    requireFormat(sentenceCount(definition) <= 2, `${label}: ${term[1]} is defined in at most two sentences`);
    index += 1;
    const avoid = [];
    while (index < lines.length && next().trim() !== '') {
      const alias = next().match(/^_Avoid_: ([^,\s][^,]*(?:, [^,\s][^,]*)*)$/);
      requireFormat(alias, `${label}: ${term[1]} is followed only by well-formed _Avoid_ lines, found: ${next()}`);
      avoid.push(...alias[1].split(', '));
      index += 1;
    }
    entries.push({ term: term[1], definition, avoid, group });
  }
  const seen = new Map();
  for (const entry of entries) {
    const key = entry.term.toLowerCase();
    requireFormat(!seen.has(key), `${label}: ${entry.term} is defined once`);
    seen.set(key, entry);
  }
  return { context: heading[1], description: description.join(' '), entries, entry: (name) => seen.get(name.toLowerCase()) };
}
