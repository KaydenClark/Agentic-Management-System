// The skills wiki's source check (S-008 Faithful / No private files): each
// article names a skill folder in a checkout of the private skills repository
// at the pinned commit, and no article copies a run of RUN or more
// consecutive words from any file in its skill's folder. Findings name the
// article, section, word offset and skill file, never the matched words, so a
// report cannot republish private text. Pure functions over paths; the CLI is
// tests/skills-source.check.mjs and the self-test tests/skills-source.test.mjs.
import { execFileSync } from 'node:child_process';
import { existsSync, mkdtempSync, readdirSync, readFileSync, realpathSync, rmSync, statSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join, relative } from 'node:path';
import { SKILLS_PIN, parseFrontMatter } from '../app/skills/content.mjs';
import { siteDir } from './helpers.mjs';
import { contentNames } from './skills-helpers.mjs';

export const RUN = 10;

// Lowercase words, apostrophes dropped, link targets and Markdown punctuation
// removed, so formatting cannot hide a copied run.
export function words(text) {
  return text
    .toLowerCase()
    .replace(/\]\([^)\s]*\)/g, ' ')
    .replace(/['’]/g, '')
    .split(/[^a-z0-9]+/)
    .filter(Boolean);
}

// An article's checked text: its summary and each ## section's body.
export function articleSections(src, file = 'article.md') {
  const { data, body } = parseFrontMatter(src, file);
  const out = [{ section: 'summary', text: data.summary ?? '' }];
  let cur = null;
  for (const line of body.split('\n')) {
    const h = line.match(/^##\s+(.*)$/);
    if (h) { cur = { section: h[1].trim(), text: '' }; out.push(cur); continue; }
    if (cur) cur.text += `${line}\n`;
  }
  return out;
}

// Every text file in a skill folder, recursively (binary files skipped).
export function skillFiles(dir) {
  const out = [];
  const walk = (d) => {
    for (const name of readdirSync(d).sort()) {
      const p = join(d, name);
      if (statSync(p).isDirectory()) { if (name !== '.git') walk(p); continue; }
      const buf = readFileSync(p);
      if (buf.includes(0)) continue;
      out.push({ file: relative(dir, p), text: buf.toString('utf8') });
    }
  };
  walk(dir);
  return out;
}

// Runs of `n` or more consecutive words an article shares with the skill's
// files: { section, offset (word index in the section), length, file }.
export function copiedRuns(articleSrc, files, { n = RUN, file = 'article.md' } = {}) {
  const grams = new Map();
  for (const f of files) {
    const w = words(f.text);
    for (let i = 0; i + n <= w.length; i++) {
      const key = w.slice(i, i + n).join(' ');
      if (!grams.has(key)) grams.set(key, f.file);
    }
  }
  const runs = [];
  for (const { section, text } of articleSections(articleSrc, file)) {
    const w = words(text);
    let run = null;
    for (let i = 0; i + n <= w.length; i++) {
      const hit = grams.get(w.slice(i, i + n).join(' '));
      if (hit && run && i === run.last + 1) { run.last = i; continue; }
      if (run) { runs.push(run); run = null; }
      if (hit) run = { section, offset: i, last: i, file: hit };
    }
    if (run) runs.push(run);
  }
  return runs.map(({ section, offset, last, file: f }) => ({ section, offset, length: last - offset + n, file: f }));
}

// The skill folder an article needs is missing (no <name>/SKILL.md).
export const folderMissing = (skillsDir, name) => !existsSync(join(skillsDir, name, 'SKILL.md'));

// The checkout's HEAD when `dir` is the top of a git checkout, else null.
export function checkoutHead(dir) {
  try {
    const top = execFileSync('git', ['-C', dir, 'rev-parse', '--show-toplevel'], { encoding: 'utf8', stdio: ['ignore', 'pipe', 'ignore'] }).trim();
    if (realpathSync(top) !== realpathSync(dir)) return null;
    return execFileSync('git', ['-C', dir, 'rev-parse', 'HEAD'], { encoding: 'utf8', stdio: ['ignore', 'pipe', 'ignore'] }).trim();
  } catch {
    return null;
  }
}

// Every finding for the articles in `contentDir` against `skillsDir`.
export function sourceFindings(contentDir, skillsDir, pin) {
  const findings = [];
  const head = checkoutHead(skillsDir);
  if (head === null) findings.push({ kind: 'note', message: 'skills folder is not a git checkout; its commit was not compared with the pin' });
  else if (head !== pin) findings.push({ kind: 'pin', message: `skills checkout is at ${head}, not the pin ${pin}` });
  const names = contentNames(contentDir);
  for (const name of names) {
    if (folderMissing(skillsDir, name)) { findings.push({ kind: 'folder', article: name, message: `${name}: no skill folder ${name}/SKILL.md at the skills checkout` }); continue; }
    const src = readFileSync(join(contentDir, `${name}.md`), 'utf8');
    for (const r of copiedRuns(src, skillFiles(join(skillsDir, name)), { file: `${name}.md` })) {
      findings.push({ kind: 'copy', article: name, ...r, message: `${name} / ${r.section}: words ${r.offset}-${r.offset + r.length - 1} (${r.length} words) match ${name}/${r.file}` });
    }
  }
  return { names, findings };
}

// Planted faults on the fixtures (tests/fixtures/skills against the fixture
// skill folders in tests/fixtures/skills-source): the copied run in map's
// article is reported without its words, reformatting does not hide a run,
// the clean fixtures pass, a missing folder and a wrong pin are reported.
// Empty when every check can fail.
export function selfTestProblems() {
  const problems = [];
  const content = join(siteDir, 'tests', 'fixtures', 'skills');
  const skills = join(siteDir, 'tests', 'fixtures', 'skills-source');
  const { names, findings } = sourceFindings(content, skills, SKILLS_PIN);
  const copies = findings.filter((f) => f.kind === 'copy');
  if (names.join(',') !== 'grilling,map,readback') problems.push(`fixture articles are ${names.join(', ')}`);
  if (!copies.some((f) => f.article === 'map' && f.section === 'What it does' && f.length >= RUN && f.file === 'SKILL.md')) problems.push('the planted copied run in map is not reported');
  if (copies.some((f) => f.article !== 'map')) problems.push('a clean fixture article is reported as copied');
  if (findings.some((f) => /planted sentence/i.test(f.message))) problems.push('a finding prints the matched words');
  if (findings.some((f) => f.kind === 'folder')) problems.push('a fixture skill folder is reported missing');
  if (!findings.some((f) => f.kind === 'note')) problems.push('a folder that is not a git checkout is not noted');
  if (!folderMissing(skills, 'teach')) problems.push('a missing skill folder is not reported');

  const src = ['---', 'summary: short', '---', '', '## What it does', '', 'Here **the planted** sentence of [twelve](/skills/map) plain *words* lives only in this folder, and so on.', ''].join('\n');
  if (!copiedRuns(src, skillFiles(join(skills, 'map'))).length) problems.push('Markdown formatting hides a copied run');
  const nine = ['---', 'summary: short', '---', '', '## What it does', '', 'Unrelated: the planted sentence of twelve plain words lives here.', ''].join('\n');
  if (copiedRuns(nine, skillFiles(join(skills, 'map'))).length) problems.push('a run of nine shared words is reported');

  const repo = mkdtempSync(join(tmpdir(), 'skills-pin-'));
  try {
    const git = (...a) => execFileSync('git', ['-C', repo, '-c', 'user.name=fixture', '-c', 'user.email=fixture@localhost', ...a], { stdio: 'ignore' });
    git('init', '-q');
    git('commit', '-q', '--allow-empty', '-m', 'fixture');
    const head = checkoutHead(repo);
    if (!/^[0-9a-f]{40}$/.test(head ?? '')) problems.push('a git checkout is not recognised');
    if (!sourceFindings(content, repo, SKILLS_PIN).findings.some((f) => f.kind === 'pin')) problems.push('a checkout at another commit than the pin is not reported');
    if (sourceFindings(content, repo, head).findings.some((f) => f.kind === 'pin')) problems.push('a checkout at the pin is reported');
  } catch (e) {
    problems.push(`the pin self-test could not run git (${e.message.split('\n')[0]})`);
  } finally {
    rmSync(repo, { recursive: true, force: true });
  }
  return problems;
}
