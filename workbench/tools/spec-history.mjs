// A Spec or Landmark describes a destination; how it got there is history,
// and history lives in the Wiki. Each Spec or Landmark ID owns one history
// page, `<history collection>/<ID>.md` (by default `<wiki lane>/history`),
// keyed by ID alone so it never moves when the record's directory moves or
// retires. Every native lifecycle row - Task closes, review verdicts, owner
// approvals, landings, corrections, moves and retirements - is appended there,
// never into SPEC.md or LANDMARK.md.
//
// The page keeps the `## Append-Only Evidence And Execution Log` heading and
// row shape the records used to carry, so every row parser reads it
// unchanged. A record that still carries a legacy in-body log (an unmigrated
// room) is read first and the page second, so old rooms keep working; writers
// only ever append to the page.
import fs from 'node:fs';
import path from 'node:path';
import { assertSafeWritePath, isSafeRelative, laneRelative, readManifest } from './workbench-paths.mjs';
import { readRecordText, writeRecordText } from './record-parts.mjs';

export const HISTORY_SECTION = 'Append-Only Evidence And Execution Log';
export const HISTORY_HEADING = `## ${HISTORY_SECTION}`;
export const HISTORY_TABLE = '| Date | Task | Event | Verification | Docs | Remaining gap |\n|---|---|---|---|---|---|';
const DATA_ROW = /^\|\s*\d{4}-\d{2}-\d{2}\s*\|/;

// The manifest's `history` collection when declared, else `<wiki lane>/history`.
export function historyRelative(root) {
  const declared = readManifest(root)?.collections?.history;
  if (declared !== undefined) {
    if (!isSafeRelative(declared)) {
      const failure = new Error(`manifest collection history is unsafe: ${declared}`);
      failure.code = 'invalid-collection';
      throw failure;
    }
    return declared;
  }
  return `${laneRelative(root, 'wiki')}/history`;
}

export function historyPagePath(root, id) {
  return path.join(path.resolve(root), historyRelative(root), `${id}.md`);
}

export function historyPageRelative(root, id) {
  return `${historyRelative(root)}/${id}.md`;
}

// The body of the log section in `content`, or '' when it has none.
function sectionBody(content, heading = HISTORY_SECTION) {
  const marker = new RegExp(`^## ${heading.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}[ \\t]*$`, 'm');
  const match = marker.exec(String(content ?? ''));
  if (!match) return '';
  const bodyStart = match.index + match[0].length;
  const end = content.indexOf('\n## ', bodyStart);
  return content.slice(bodyStart, end < 0 ? content.length : end);
}

export function hasLegacyHistory(content) {
  return new RegExp(`^${HISTORY_HEADING}[ \\t]*$`, 'm').test(String(content ?? ''));
}

function tableHeader(body) {
  const lines = body.split('\n').map((line) => line.trim()).filter(Boolean);
  const index = lines.findIndex((line) => line.startsWith('|') && !DATA_ROW.test(line));
  if (index < 0 || !/^\|[\s:|-]+\|$/.test(lines[index + 1] ?? '')) return null;
  return `${lines[index]}\n${lines[index + 1]}`;
}

function rowsOf(body) {
  return body.split('\n').map((line) => line.trim()).filter((line) => DATA_ROW.test(line));
}

// Every ID a record has answered to, oldest first: a widened record keeps its
// validated Former ID, whose page (if any) is read before the current one.
function historyIds(record) {
  return [...new Set([record.formerId, record.id].filter(Boolean))];
}

function readPage(root, id) {
  const filePath = historyPagePath(root, id);
  if (!fs.existsSync(filePath)) return { filePath, content: null };
  return { filePath, content: readRecordText(filePath, root) };
}

// The record's complete history as one log section: its legacy in-body rows
// first, then each history page's rows. Every existing row parser reads this
// exactly as it read the record's own section. `record.historyOverride`, when
// set, is a proposed history (a row planned but not yet written) and wins.
export function historyText(record, root = record.root) {
  if (typeof record.historyOverride === 'string') return record.historyOverride;
  const legacy = sectionBody(record.content);
  const pages = historyIds(record).map((id) => readPage(root, id)).filter((page) => page.content !== null).map((page) => sectionBody(page.content));
  const header = tableHeader(legacy) ?? pages.map(tableHeader).find(Boolean) ?? HISTORY_TABLE;
  const rows = [legacy, ...pages].flatMap(rowsOf);
  return `${HISTORY_HEADING}\n\n${header}\n${rows.map((row) => `${row}\n`).join('')}`;
}

export function historyRows(record, root = record.root) {
  return rowsOf(sectionBody(historyText(record, root)));
}

// The history as a proposed record would see it after `rows` are appended.
export function proposedHistory(record, rows, root = record.root) {
  const current = historyText(record, root);
  return `${current}${[].concat(rows).map((row) => `${row}\n`).join('')}`;
}

function newPage(root, record, filePath, date) {
  const recordRelative = path.relative(path.resolve(root), record.filePath).split(path.sep).join('/');
  const link = path.relative(path.dirname(filePath), record.filePath).split(path.sep).join('/');
  return [
    '---',
    'type: history',
    'status: active',
    'sensitivity: normal',
    'knowledge_role: derived',
    'provenance:',
    '  - native Workbench lifecycle tools',
    'source_paths:',
    `  - ${recordRelative}`,
    `last_verified: ${date}`,
    '---',
    '',
    `# ${record.id} history`,
    '',
    `How [${record.id}](${link}) reached its current state. The ${record.kind === 'landmark' ? 'Landmark' : 'Spec'} holds only its destination; this page holds closes, verdicts, approvals and corrections.`,
    '',
    HISTORY_HEADING,
    '',
    tableHeader(sectionBody(record.content)) ?? HISTORY_TABLE,
    ''
  ].join('\n');
}

// Insert rows at the end of the page's log table, keeping every existing byte.
function appendRows(content, rows) {
  const marker = new RegExp(`^${HISTORY_HEADING}[ \\t]*$`, 'm');
  const match = marker.exec(content);
  if (!match) throw new Error('history page has no evidence log');
  const next = content.indexOf('\n## ', match.index + match[0].length);
  const end = next < 0 ? content.length : next;
  const trailing = content.slice(0, end).match(/(?:\n[ \t\r]*)+$/)?.[0] ?? '';
  const insertion = end - trailing.length;
  return `${content.slice(0, insertion)}${rows.map((row) => `\n${row}`).join('')}${content.slice(insertion)}`;
}

// Plan appending `rows` to the record's history page without writing. The
// page is created with its Wiki frontmatter on the first write. `base`, when
// given, is already-planned page content to append to instead of the file.
export function planHistoryAppend(record, rows, root = record.root, base = undefined) {
  const list = [].concat(rows);
  for (const row of list) {
    if (typeof row !== 'string' || /[\r\n]/.test(row) || !DATA_ROW.test(row)) throw new Error(`invalid history row: ${row}`);
  }
  const filePath = historyPagePath(root, record.id);
  assertSafeWritePath(root, filePath);
  const existing = fs.existsSync(filePath) ? readRecordText(filePath, root) : null;
  const date = list[0]?.match(/^\|\s*(\d{4}-\d{2}-\d{2})/)?.[1] ?? new Date().toISOString().slice(0, 10);
  const start = base ?? existing ?? newPage(root, record, filePath, date);
  return { filePath, originalContent: existing ?? undefined, newFile: existing === null, content: appendRows(start, list) };
}

export function appendHistory(record, rows, root = record.root) {
  const plan = planHistoryAppend(record, rows, root);
  fs.mkdirSync(path.dirname(plan.filePath), { recursive: true });
  writeRecordText(plan.filePath, plan.content.endsWith('\n') ? plan.content : `${plan.content}\n`, { root });
  return plan.filePath;
}

// The record content with its legacy log section (heading and body) and
// `Latest event` field removed: what a destination-only record holds. The
// whitespace before the removed section is normalized to one blank line, so a
// record migrated by hand and one normalized here compare equal.
export function withoutLegacyHistory(content) {
  const text = String(content ?? '');
  const match = new RegExp(`^${HISTORY_HEADING}[ \\t]*$`, 'm').exec(text);
  let result = text;
  if (match) {
    const next = text.indexOf('\n## ', match.index + match[0].length);
    const before = text.slice(0, match.index).replace(/\s+$/, '');
    result = next < 0 ? `${before}\n` : `${before}\n\n${text.slice(next + 1)}`;
  }
  return result.replace(/^\*\*Latest event:\*\*.*(?:\r?\n|$)/m, '');
}
