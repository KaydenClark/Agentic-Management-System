// Budgeted generated tables. Source rows remain whole, ordered and unchanged;
// pages are sibling projections, so their existing relative links still work.
import fs from 'node:fs';
import path from 'node:path';
import { assertSafeReadPath, assertSafeWritePath, writeSafeFile } from './workbench-paths.mjs';
import { loadBudgets, budgetFor, characterCount } from './artifact-budgets.mjs';

const characters = characterCount;
const marker = file => `<!-- workbench-generated-page: ${path.posix.basename(file)} -->`;
const escaped = value => value.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');

export function artifactCharacterLimit(root, file) {
  const policyPath = path.join(root, 'workbench/artifact-budgets.json');
  assertSafeReadPath(root, policyPath);
  if (!fs.existsSync(policyPath)) return null; // Older installed rooms have no policy.
  return budgetFor(loadBudgets(root), file).maxCharacters;
}

export function paginateGeneratedTable(file, table, { prefix = '', suffix = '', maxCharacters = null } = {}) {
  if (path.posix.isAbsolute(file) || file.includes('\\') || path.posix.normalize(file) !== file || file.split('/').includes('..')) throw new Error('Generated view must use a relative path inside the project');
  const original = prefix + table + suffix;
  if (maxCharacters !== null && (!Number.isSafeInteger(maxCharacters) || maxCharacters <= 0)) throw new Error('Invalid generated-view character budget');
  if (maxCharacters === null || characters(original) <= maxCharacters) return new Map([[file, original]]);
  const lines = table.trimEnd().split(/\r?\n/);
  if (lines.length < 2 || !/^\s*\|/.test(lines[0]) || !/^\s*\|(?:\s*:?-+:?\s*\|)+\s*$/.test(lines[1]) || lines.slice(2).some(line => !/^\s*\|/.test(line))) throw new Error('Pagination requires one Markdown table with whole rows');
  const header = lines.slice(0, 2).join('\n');
  const rows = lines.slice(2);
  const basename = path.posix.basename(file);
  const stem = basename.replace(/\.md$/i, '');
  const pageName = index => index === 0 ? basename : `${stem}.page-${String(index).padStart(3, '0')}.md`;
  const relativeName = index => path.posix.join(path.posix.dirname(file), pageName(index));
  const render = (group, index, next) => {
    const intro = index === 0 ? prefix : `${marker(file)}\n# ${stem} (continued)\n\n[First page](${basename}) · [Previous page](${pageName(index - 1)})\n\n`;
    return (intro + header + '\n' + group.join('\n') + (next ? `\n\n[Next page](${pageName(index + 1)})\n` : '') + (index === 0 ? suffix : '\n')).replace(/\n+$/, '\n');
  };
  const groups = [];
  let group = [];
  for (const row of rows) {
    if (characters(render([...group, row], groups.length, true)) > maxCharacters) {
      if (!group.length) throw new Error(`${file}: a generated row or page frame exceeds its character budget; condense the source row without losing meaning`);
      groups.push(group);
      group = [];
      if (characters(render([row], groups.length, true)) > maxCharacters) throw new Error(`${file}: a generated row exceeds its character budget; no row was truncated`);
    }
    group.push(row);
  }
  if (group.length || !groups.length) groups.push(group);
  const result = new Map(groups.map((group, index) => [relativeName(index), render(group, index, index < groups.length - 1)]));
  if ([...result.values()].some(source => characters(source) > maxCharacters)) throw new Error(`${file}: generated page frame exceeds its character budget`);
  return result;
}

function pagePaths(root, primary) {
  const folder = path.join(root, path.posix.dirname(primary));
  if (path.resolve(folder) !== path.resolve(root)) assertSafeReadPath(root, folder);
  if (!fs.existsSync(folder)) return [];
  const stem = path.posix.basename(primary).replace(/\.md$/i, '');
  const pattern = new RegExp(`^${escaped(stem)}\\.page-\\d{3,}\\.md$`);
  return fs.readdirSync(folder).filter(name => pattern.test(name)).map(name => path.posix.join(path.posix.dirname(primary), name));
}

export function generatedPageIssues(root, pages) {
  const primary = pages.keys().next().value;
  const issues = [];
  for (const [relative, expected] of pages) {
    try {
      const file = path.join(root, relative);
      assertSafeReadPath(root, file);
      if (!fs.existsSync(file) || fs.readFileSync(file, 'utf8').replace(/\r\n?/g, '\n') !== expected.replace(/\r\n?/g, '\n')) issues.push(`${relative} generated projection is stale`);
    } catch (error) { issues.push(`${relative}: ${error.message}`); }
  }
  for (const relative of pagePaths(root, primary)) if (!pages.has(relative)) issues.push(`${relative} generated continuation is obsolete`);
  return issues;
}

export function writeGeneratedPages(root, pages) {
  const primary = pages.keys().next().value;
  if (!primary) throw new Error('A generated view needs its primary page');
  const existing = pagePaths(root, primary);
  const candidates = [...new Set([...pages.keys(), ...existing])];
  // Preflight every path and ownership marker before touching the primary.
  for (const relative of candidates) {
    const file = path.join(root, relative);
    assertSafeWritePath(root, file);
    if (relative !== primary && fs.existsSync(file) && !fs.readFileSync(file, 'utf8').startsWith(marker(primary) + '\n')) throw new Error(`${relative}: generated-page ownership collision; existing file is not owned by this view`);
  }
  // Publish the entrypoint last: a failed continuation write must never expose
  // a new primary whose linked page has not been written yet. A retry is safe.
  for (const [relative, source] of pages) if (relative !== primary) writeSafeFile(root, path.join(root, relative), source);
  writeSafeFile(root, path.join(root, primary), pages.get(primary));
  for (const relative of existing) if (!pages.has(relative)) fs.unlinkSync(path.join(root, relative));
  return [...pages.keys()];
}
