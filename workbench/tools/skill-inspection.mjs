// Read-only skills-lane inspection (S-00V). The core skills ship inside the
// room at the manifest-declared skills lane. Since S-006I TK-00BQ (ADR-001M)
// that lane is `.agents/skills` itself and `.claude/skills` is one relative
// link to it; a room on the retired `workbench/skills` lane keeps two links. Doctor
// reads the room and personal discovery roots without writing. Discovery is filesystem evidence, never proof that a configured
// application can invoke a skill.
import crypto from 'node:crypto';
import { inspectPersonalSkills } from './personal-skills.mjs';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import { finding } from './diagnostics.mjs';
import { LEGACY_SKILLS_LANE, isSkillsLane } from './workbench-paths.mjs';

// One hash over a skill directory's ordinary files, in stable order. The
// managed marker a personal-catalog install writes beside the files is
// excluded so the hash describes the skill, not its installation.
export function skillContentHash(directory) {
  const hash = crypto.createHash('sha256');
  function walk(current, relative = '') {
    for (const name of fs.readdirSync(current).sort((a, b) => a.localeCompare(b))) {
      if (name === '.workbench-skill.json') continue;
      const target = path.join(current, name), child = path.posix.join(relative, name);
      const stat = fs.lstatSync(target);
      if (stat.isDirectory()) walk(target, child);
      else if (stat.isFile() && stat.nlink === 1) hash.update(`${child}\0`).update(fs.readFileSync(target)).update('\0');
      else throw new Error('Core content must contain ordinary unshared files and directories');
    }
  }
  walk(directory);
  return hash.digest('hex');
}

// The earliest room release the personal-catalog installer's marker may
// claim compatibility from; the lane itself carries a receipt, not markers.
export const CORE_COMPATIBILITY_MINIMUM = 'v3.1.4';

function lstatOrNull(target) {
  try { return fs.lstatSync(target); } catch (error) {
    // A missing entry or a non-directory ancestor cannot name this path.
    if (['ENOENT', 'ENOTDIR'].includes(error.code)) return null;
    throw error;
  }
}

function realpathOrNull(target) {
  try { return fs.realpathSync(target); } catch { return null; }
}

// Git records a symlink with mode 120000. Only then does a plain file holding
// the link target mean the checkout wrote it as text; an untracked or regular
// tracked file keeps the ordinary install remedy.
function indexedAsSymlink(root, relative) {
  const result = spawnSync('git', ['-C', root, 'ls-files', '-s', '--', relative], { encoding: 'utf8' });
  return result.status === 0 && result.stdout.startsWith('120000 ');
}

// The declared discovery roots are the only ones a Codex or Claude host reads
// at the project root; a policy naming anything else is not one this room's
// tools can reason about.
const SUPPORTED_DISCOVERY = ['.agents/skills', '.claude/skills'];

export function inspectSkills(manifest, project, { home = os.homedir() } = {}) {
  if (manifest?.schemaVersion !== 2) return [];
  if (manifest.skillPolicy?.normalSetup === 'personal-catalog') return inspectPersonalSkills(manifest, project, { home });
  const required = manifest.skillPolicy?.required, discovery = manifest.skillPolicy?.discovery;
  if (!Array.isArray(required) || !Array.isArray(discovery) ||
      required.some(name => typeof name !== 'string' || !/^[a-z][a-z0-9-]*$/.test(name)) ||
      discovery.some(root => !SUPPORTED_DISCOVERY.includes(root))) {
    return [finding('invalid-skill-policy', 'Core inspection requires safe declared skill names and supported discovery roots.')];
  }
  const root = path.resolve(project);
  const findings = [];
  const shadow = lstatOrNull(path.join(root, 'skills'));
  if (shadow) findings.push(finding('project-local-skills', 'a root skills/ directory shadows the skills lane; move its contents into the lane or remove it', { path: 'skills' }));
  const laneRelative = manifest.lanes?.skills;
  if (!isSkillsLane(laneRelative)) {
    findings.push(finding('skill-lane-missing', 'the manifest declares no .agents/skills lane; run workbench-layout.mjs migrate --project PATH once', { lane: laneRelative ?? null }));
    return findings;
  }
  if (laneRelative === LEGACY_SKILLS_LANE) findings.push(finding('skill-lane-legacy', `${LEGACY_SKILLS_LANE} is the retired skills lane; run workbench-layout.mjs migrate --project PATH to move it to .agents/skills`, { lane: laneRelative }));
  findings.push(...inspectRoomCopies(root));
  const lane = path.join(root, laneRelative);
  const laneEntry = lstatOrNull(lane);
  if (!laneEntry) {
    findings.push(finding('skill-lane-missing', `${laneRelative} is absent; run workbench-skills.mjs install from the release checkout`, { lane: laneRelative }));
    return findings;
  }
  if (laneEntry.isSymbolicLink() || !laneEntry.isDirectory()) {
    findings.push(finding('skill-lane-unreadable', `${laneRelative} must be an ordinary directory`, { lane: laneRelative }));
    return findings;
  }
  // Each adapter is judged once: a discovery root that is absent, or that
  // resolves outside the lane, is reported by root rather than per skill.
  const adapters = {};
  for (const discoveryRoot of discovery) {
    const adapter = path.join(root, discoveryRoot);
    const entry = lstatOrNull(adapter);
    if (!entry) {
      findings.push(finding('skill-adapter-missing', `${discoveryRoot} is absent, so that host cannot discover ${laneRelative}; run workbench-skills.mjs install from the release checkout`, { root: discoveryRoot }));
      adapters[discoveryRoot] = null;
      continue;
    }
    const resolved = realpathOrNull(adapter);
    if (!resolved || !fs.statSync(resolved).isDirectory()) {
      // S-005U: with core.symlinks=false Git checks the adapter symlink out as
      // a plain file holding its link target; name that cause and the restore.
      let checkedOutAsText = false;
      try { checkedOutAsText = entry.isFile() && entry.size < 256 && fs.readFileSync(adapter, 'utf8').trim() === path.relative(path.dirname(adapter), lane).split(path.sep).join('/') && indexedAsSymlink(root, discoveryRoot); }
      catch { /* an unreadable adapter keeps the ordinary finding */ }
      const message = checkedOutAsText
        ? `${discoveryRoot} is a plain file holding its link target, so Git checked the symlink out as text because core.symlinks is false on this host; enable symlinks (on Windows, Developer Mode or an elevated shell), run \`git config core.symlinks true\`, then restore it with \`git checkout -- ${discoveryRoot}\``
        : `${discoveryRoot} does not resolve to a directory`;
      findings.push(finding('skill-adapter-broken', message, { root: discoveryRoot }));
      adapters[discoveryRoot] = null;
      continue;
    }
    adapters[discoveryRoot] = resolved;
  }
  findings.push(...inspectDiscoveryScopes(lane, home));
  const laneReal = fs.realpathSync(lane);
  // A lane holding none of the required skills is one condition (it was
  // never installed), not one finding per skill.
  if (required.every((skill) => {
    try { return !lstatOrNull(path.join(lane, skill, 'SKILL.md')); }
    catch { return false; } // The per-skill path check below reports unsafe ancestry.
  })) {
    findings.push(finding('skill-lane-missing', `${laneRelative} holds none of the ${required.length} required core skills; run workbench-skills.mjs install --project PATH from the release checkout`, { lane: laneRelative }));
    return findings;
  }
  for (const skill of required) {
    const skillDir = path.join(lane, skill);
    const skillEntry = lstatOrNull(skillDir);
    let skillFile;
    try { skillFile = lstatOrNull(path.join(skillDir, 'SKILL.md')); }
    catch (error) {
      findings.push(finding('skill-lane-unreadable', `Cannot inspect ${skillDir}: ${error.message}`, { skill, lane: laneRelative }));
      continue;
    }
    if (!skillEntry || !skillFile) {
      findings.push(finding('skill-lane-missing', `${laneRelative}/${skill}/SKILL.md is missing; run workbench-skills.mjs update --project PATH --explicit-update from the release checkout`, { skill, lane: laneRelative }));
      continue;
    }
    if (skillEntry.isSymbolicLink() || !skillEntry.isDirectory() || !skillFile.isFile() || skillFile.isSymbolicLink() || skillFile.nlink !== 1) {
      findings.push(finding('skill-lane-unreadable', `${laneRelative}/${skill} must be an ordinary directory holding an ordinary, unshared SKILL.md`, { skill, lane: laneRelative }));
      continue;
    }
    for (const discoveryRoot of discovery) {
      if (adapters[discoveryRoot] === null) continue;
      const resolved = realpathOrNull(path.join(root, discoveryRoot, skill, 'SKILL.md'));
      if (resolved !== path.join(laneReal, skill, 'SKILL.md')) {
        findings.push(finding('skill-adapter-broken', `${discoveryRoot}/${skill} does not resolve into ${laneRelative}/${skill}`, { skill, root: discoveryRoot }));
      }
    }
    const extra = lstatOrNull(path.join(root, '.codex', 'skills', skill));
    if (extra) findings.push(finding('skill-duplicate-discovery', `.codex/skills/${skill} adds a second Codex discovery entry; preserve and reconcile it explicitly.`, { skill, root: '.codex/skills' }));
  }
  const pointers = resolveSkillPointers(manifest, root);
  for (const item of [...pointers.pointed, ...pointers.unpointed]) {
    if (item.contentError) findings.push(finding('skill-lane-unreadable', `${item.path} cannot be hashed: ${item.contentError}`, { skill: item.skill, lane: laneRelative }));
  }
  for (const pointer of pointers.dangling) {
    findings.push(finding('skill-pointer-dangling', `AGENTS.md Skill Map entry "${pointer.operation}" names ${pointer.pointer}, but ${laneRelative}/${pointer.skill}/SKILL.md is missing; restore the skill in the lane or re-point the entry`, { skill: pointer.skill, operation: pointer.operation, pointer: pointer.pointer }));
  }
  return findings;
}

// S-006I TK-00BQ (ADR-001M): every room directory a host or the retired lane
// layout can hold skills in. A declared skill name whose copies resolve to
// more than one real directory is a duplicate some host can see; the declared
// links resolve to one directory and so never count twice. `.codex/skills` keeps its own
// deprecated-discovery finding.
const ROOM_SKILL_ROOTS = ['.agents/skills', '.claude/skills', LEGACY_SKILLS_LANE, '.gemini/skills', '.github/skills'];
// Codex lists .agents/skills recursively, and the retired lane is reached
// through that root, so both are walked to the depth personal roots use.
const RECURSIVE_ROOM_ROOTS = ['.agents/skills', LEGACY_SKILLS_LANE];

function declaredSkillName(file) {
  const text = fs.readFileSync(file, 'utf8').replace(/^\uFEFF/, '');
  const header = text.match(/^---\r?\n([\s\S]*?)\r?\n---(?:\r?\n|$)/)?.[1];
  const value = header?.match(/^name:[ \t]*(?:"([a-zA-Z0-9-]+)"|'([a-zA-Z0-9-]+)'|([a-zA-Z0-9-]+))[ \t]*(?:#.*)?$/m);
  return value ? value[1] ?? value[2] ?? value[3] : path.basename(path.dirname(file));
}

function inspectRoomCopies(root) {
  const copies = new Map();
  for (const relative of ROOM_SKILL_ROOTS) {
    const maxDepth = RECURSIVE_ROOM_ROOTS.includes(relative) ? 6 : 1;
    const visited = new Set();
    (function scan(directory, display, depth) {
      let real;
      try { real = fs.realpathSync(directory); if (!fs.statSync(real).isDirectory()) return; }
      catch { return; } // A broken adapter keeps its own finding.
      if (visited.has(real)) return;
      visited.add(real);
      if (depth > 0) {
        const file = path.join(directory, 'SKILL.md');
        let name = null;
        try { if (lstatOrNull(file)) name = declaredSkillName(file); } catch { name = null; }
        if (name) {
          if (!copies.has(name)) copies.set(name, new Map());
          if (!copies.get(name).has(real)) copies.get(name).set(real, display);
        }
      }
      if (depth >= maxDepth) return;
      let entries;
      try { entries = fs.readdirSync(directory, { withFileTypes: true }); } catch { return; }
      for (const entry of entries) {
        if (entry.name.startsWith('.') || !(entry.isDirectory() || entry.isSymbolicLink())) continue;
        scan(path.join(directory, entry.name), `${display}/${entry.name}`, depth + 1);
      }
    })(path.join(root, relative), relative, 0);
  }
  return [...copies].filter(([, places]) => places.size > 1).sort(([a], [b]) => a.localeCompare(b))
    .map(([skill, places]) => finding('room-skill-duplicate', `${skill} has ${places.size} copies in the room (${[...places.values()].join(', ')}); keep the .agents/skills copy and remove the others so no host sees the name twice`, { skill, paths: [...places.values()] }));
}

// Personal roots are discovery inputs, never installation destinations for room names.
const PERSONAL_ROOTS = [
  ['.agents/skills', ['Claude Code via linked .claude root when present', 'Codex: both copies can be listed; a plain name is ambiguous', 'Gemini CLI: launch directory and trust affect selection', 'Copilot: precedence varies by host']],
  ['.claude/skills', ['Claude Code: personal copy wins', 'Copilot VS Code: workspace-first discovery']],
  ['.codex/skills', ['Codex: both copies can be listed; a plain name is ambiguous']],
  ['.gemini/skills', ['Gemini CLI: launch directory and trust affect selection']],
  ['.copilot/skills', ['Copilot: precedence varies by host']],
];

function inspectDiscoveryScopes(lane, home) {
  const findings = [];
  function skillName(file) {
    const text = fs.readFileSync(file, 'utf8').replace(/^\uFEFF/, '');
    const header = text.match(/^---\r?\n([\s\S]*?)\r?\n---(?:\r?\n|$)/)?.[1];
    const value = header?.match(/^name:[ \t]*(?:"([a-zA-Z0-9-]+)"|'([a-zA-Z0-9-]+)'|([a-zA-Z0-9-]+))[ \t]*(?:#.*)?$/m);
    return value ? value[1] ?? value[2] ?? value[3] : path.basename(path.dirname(file));
  }
  const names = new Set();
  for (const entry of fs.readdirSync(lane, { withFileTypes: true })) {
    if (!entry.isDirectory() && !entry.isSymbolicLink()) continue;
    const directory = path.join(lane, entry.name);
    try {
      if (!fs.statSync(directory).isDirectory()) throw new Error('skill directory link does not target a directory');
      const file = path.join(directory, 'SKILL.md');
      if (lstatOrNull(file)) names.add(skillName(file));
    } catch (error) {
      findings.push(finding('skill-lane-unreadable', `Cannot inspect ${directory}: ${error.message}`, { lane, skill: entry.name }));
    }
  }
  for (const [relative, hosts] of PERSONAL_ROOTS) {
    const root = path.join(home, relative);
    try {
      if (!lstatOrNull(root)) continue;
      const visited = new Set();
      const recursive = ['.agents/skills', '.codex/skills'].includes(relative);
      function scan(directory, depth = 0) {
        const canonical = fs.realpathSync(directory);
        if (visited.has(canonical)) return;
        visited.add(canonical);
        if (!fs.statSync(directory).isDirectory()) throw new Error('discovery root is not a readable directory');
        if (depth > 0) {
          const file = path.join(directory, 'SKILL.md');
          if (lstatOrNull(file)) {
            const skill = skillName(file);
            if (names.has(skill)) findings.push(finding('personal-skill-shadow', `${skill} occurs in ${lane} and ${directory}; ${hosts.join('; ')}. Keep the personal skill active and use its source explicitly. Reconcile the project duplicate within scope; moving, hiding or disabling the personal skill is not conflict repair.`, { skill, root, path: file, preferredSource: file, resolved: realpathOrNull(file), hosts }));
          }
        }
        if (depth >= (recursive ? 6 : 1)) return;
        for (const entry of fs.readdirSync(directory, { withFileTypes: true })) {
          if (entry.name.startsWith('.')) continue;
          const target = path.join(directory, entry.name);
          if (entry.isDirectory() || (entry.isSymbolicLink() && fs.statSync(target).isDirectory())) scan(target, depth + 1);
        }
      }
      scan(root);
    } catch (error) {
      findings.push(finding('personal-skill-inspection-unavailable', `Cannot inspect ${root}: ${error.message}`, { root }));
    }
  }
  // Hosts follow skill directory links. Inspect their reachable content, but
  // stop and report a cycle rather than accepting an uninspected shape.
  function walk(directory, depth = 0, ancestors = new Set()) {
    const canonical = fs.realpathSync(directory);
    if (ancestors.has(canonical)) {
      findings.push(finding('skill-lane-unreadable', `${directory} forms a directory-link cycle; reconcile it before relying on discovery.`, { path: directory }));
      return;
    }
    const next = new Set([...ancestors, canonical]);
    for (const entry of fs.readdirSync(directory, { withFileTypes: true })) {
      const file = path.join(directory, entry.name);
      if (entry.name === 'SKILL.md') {
        if (entry.isSymbolicLink()) findings.push(finding('skill-file-link', `${file} is a linked SKILL.md; use an ordinary file.`, { path: file }));
        if (depth > 1) findings.push(finding('nested-skill-file', `${file} becomes an extra skill in recursive discovery; rename the reference file.`, { path: file }));
      }
      if (!entry.name.startsWith('.') && (entry.isDirectory() || (entry.isSymbolicLink() && fs.statSync(file).isDirectory()))) walk(file, depth + 1, next);
    }
  }
  try { walk(lane); }
  catch (error) { findings.push(finding('skill-lane-unreadable', `Cannot inspect lane shape: ${error.message}`, { lane })); }
  for (let directory = lane; ; directory = path.dirname(directory)) {
    for (const prefix of ['.codex-plugin', '.claude-plugin', '.cursor-plugin']) {
      const file = path.join(directory, prefix, 'plugin.json');
      try {
        if (lstatOrNull(file)) findings.push(finding('lane-plugin-manifest', `${file} can namespace the lane skills; keep the lane outside plugin ancestry.`, { path: file }));
      } catch (error) {
        findings.push(finding('skill-lane-unreadable', `Cannot inspect plugin ancestry ${file}: ${error.message}`, { path: file }));
      }
    }
    if (path.dirname(directory) === directory) break;
  }
  return findings;
}

// S-004C TK-005E (ADR-000W), moved by S-005K TK-009T (DDR-001C): authority
// flows through the pointer, and the one place a pointer declares which skill
// binds is the `### Skill Map` section of the room's AGENTS.md. Each bullet is
// one operation family: the text before its first colon names the family, and
// every skill it names after the colon, as a code-span name (`save`) or a link
// into the lane, binds for that family; an indented line continues the bullet
// above it. Every other ordinary lane skill, including one the room
// added or one only a Runbook or another file names, is `teaching`; an
// entry naming a skill the lane lacks is `dangling`. Only the map and the lane
// copy are read: a discovery root, a provider home or any other installed copy
// never decides what binds, and the reported hash is the lane copy's. Never
// writes.
const MAP_HEADING = /^#{2,3}\s+Skill Map\s*$/;
const SKILL_NAME = /^[a-z][a-z0-9-]*$/;

function mapEntries(text) {
  const lines = text.split('\n');
  const start = lines.findIndex((line) => MAP_HEADING.test(line));
  if (start === -1) return null;
  const entries = [];
  for (const line of lines.slice(start + 1)) {
    if (/^#{1,6}\s/.test(line)) break;
    const bullet = line.match(/^[-*]\s+(.*)$/);
    if (bullet) {
      const colon = bullet[1].indexOf(':');
      const operation = (colon === -1 ? bullet[1] : bullet[1].slice(0, colon)).replace(/[*_`]/g, '').trim();
      entries.push({ operation, pointer: bullet[1] });
    } else if (/^\s+\S/.test(line) && entries.length) {
      entries[entries.length - 1].pointer += ` ${line.trim()}`;
    } else if (line.trim()) {
      if (entries.length) break;
    }
  }
  return entries;
}

function laneSkillName(target, laneRelative) {
  if (!target || /^[a-z][a-z0-9+.-]*:/i.test(target)) return null;
  let decoded;
  try { decoded = decodeURIComponent(target.split('#')[0]); } catch { return null; }
  if (!decoded) return null;
  const normalized = path.posix.normalize(decoded).replace(/^\.\//, '');
  if (!normalized.startsWith(`${laneRelative}/`)) return null;
  const name = normalized.slice(laneRelative.length + 1).split('/')[0];
  return SKILL_NAME.test(name) ? { name, pointer: normalized } : null;
}

function ordinarySkill(lane, name) {
  try {
    const directory = lstatOrNull(path.join(lane, name));
    if (!directory?.isDirectory() || directory.isSymbolicLink()) return false;
    const file = lstatOrNull(path.join(lane, name, 'SKILL.md'));
    return Boolean(file?.isFile() && !file.isSymbolicLink());
  } catch { return false; }
}

export function resolveSkillPointers(manifest, project) {
  const root = path.resolve(project);
  const laneRelative = manifest?.lanes?.skills;
  const empty = { index: null, lane: laneRelative ?? null, pointed: [], unpointed: [], dangling: [] };
  if (!isSkillsLane(laneRelative)) return empty;
  const lane = path.join(root, laneRelative);
  const laneEntry = lstatOrNull(lane);
  const laneSkills = laneEntry?.isDirectory() && !laneEntry.isSymbolicLink()
    ? fs.readdirSync(lane).filter((name) => SKILL_NAME.test(name) && ordinarySkill(lane, name)).sort((a, b) => a.localeCompare(b))
    : [];
  const describeSkill = (skill, authority) => {
    const description = { skill, authority, path: `${laneRelative}/${skill}/SKILL.md` };
    try { return { ...description, contentHash: skillContentHash(path.join(lane, skill)) }; }
    catch (error) { return { ...description, contentHash: null, contentError: error.message }; }
  };
  const agents = lstatOrNull(path.join(root, 'AGENTS.md'));
  const rows = agents?.isFile() && !agents.isSymbolicLink() ? mapEntries(fs.readFileSync(path.join(root, 'AGENTS.md'), 'utf8')) : null;
  if (rows === null) return { ...empty, unpointed: laneSkills.map((skill) => describeSkill(skill, 'teaching')) };
  const operations = new Map();
  const dangling = [];
  const LINK = /\[[^\]]*\]\(\s*<?([^)\s>]+)>?(?:\s+"[^"]*")?\s*\)/g;
  for (const row of rows) {
    const unlinked = row.pointer.replace(LINK, '');
    const named = [...unlinked.slice(unlinked.indexOf(':') + 1).matchAll(/`([^`]+)`/g)]
      .filter((match) => SKILL_NAME.test(match[1])).map((match) => ({ name: match[1], pointer: `${laneRelative}/${match[1]}/SKILL.md` }));
    const linked = [...row.pointer.matchAll(LINK)].map((match) => laneSkillName(match[1], laneRelative)).filter(Boolean);
    for (const target of [...linked, ...named]) {
      if (laneSkills.includes(target.name)) {
        if (!operations.has(target.name)) operations.set(target.name, []);
        if (!operations.get(target.name).includes(row.operation)) operations.get(target.name).push(row.operation);
      } else {
        dangling.push({ skill: target.name, operation: row.operation, pointer: target.pointer });
      }
    }
  }
  return {
    index: 'AGENTS.md#skill-map',
    lane: laneRelative,
    pointed: laneSkills.filter((skill) => operations.has(skill)).map((skill) => ({ ...describeSkill(skill, 'binding'), operations: operations.get(skill) })),
    unpointed: laneSkills.filter((skill) => !operations.has(skill)).map((skill) => describeSkill(skill, 'teaching')),
    dangling
  };
}
