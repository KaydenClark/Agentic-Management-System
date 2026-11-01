import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { finding } from './diagnostics.mjs';

export const personalCoreSkills = ['setup-workbench', 'map', 'plan', 'orchestrate', 'journey', 'jot', 'domain-modeling', 'grilling', 'code-review', 'pr', 'carry', 'reconcile', 'improve-workbench', 'evaluate-workbench', 'audit-workbench', 'author-skill'];
export const personalSkillPolicy = { required: personalCoreSkills, discovery: ['.agents/skills', '.claude/skills'], normalSetup: 'personal-catalog', updates: 'explicit-only' };
// Project roots a host reads besides the lane: Claude Code's adapter, Codex's
// deprecated root, Gemini CLI's and Copilot's. A trusted host can select a
// project copy there over the personal source, so each is inspected; a root
// resolving to the lane, like the prepared `.claude/skills` link, is the lane
// and counts once.
const projectDiscoveryRoots = ['.claude/skills', '.codex/skills', '.gemini/skills', '.github/skills'];

// `adapter: false` skips the project adapter check for a caller that has not
// prepared it yet (adoption preflight); every catalog and shadow check runs.
export function inspectPersonalSkills(manifest, project, { home = os.homedir(), adapter = true } = {}) {
  const findings = [];
  const lane = path.join(project, manifest.lanes.skills);
  if (adapter) try {
    for (const relative of ['.agents', '.agents/skills', '.claude']) {
      const directory = path.join(project, relative);
      if (fs.lstatSync(directory).isSymbolicLink() || !fs.statSync(directory).isDirectory()) throw new Error(`unsafe project directory: ${relative}`);
    }
    if (fs.lstatSync(lane).isSymbolicLink() || !fs.statSync(lane).isDirectory()) throw new Error('not an ordinary directory');
    if (fs.realpathSync(path.join(project, '.claude/skills')) !== fs.realpathSync(lane)) throw new Error('Claude adapter does not resolve into the project skills lane');
  } catch (error) { findings.push(finding('skill-adapter-broken', `Project skill discovery: ${error.message}`)); }
  // Both roots may resolve to one catalog. A cloud session can provide its
  // own catalog root; this reads it and never installs or changes user skills.
  const roots = process.env.WORKBENCH_SKILLS_ROOT ? [process.env.WORKBENCH_SKILLS_ROOT]
    : [...new Set([path.join(home, '.agents/skills'), path.join(home, '.claude/skills')])];
  const catalogNames = new Set();
  for (const root of roots) {
    try {
      for (const name of fs.readdirSync(root).filter(name => !name.startsWith('.'))) {
        if (fs.existsSync(path.join(root, name, 'SKILL.md'))) catalogNames.add(name);
      }
    } catch (error) {
      if (!['ENOENT', 'ENOTDIR'].includes(error.code)) findings.push(finding('personal-catalog-unavailable', `Cannot inspect catalog ${root}: ${error.message}`));
    }
  }
  for (const name of manifest.skillPolicy.required) {
    const available = new Set();
    for (const root of roots) {
      try {
        const file = path.join(root, name, 'SKILL.md');
        const body = fs.readFileSync(file, 'utf8');
        if (!new RegExp(`^name:\\s*["']?${name}["']?\\s*$`, 'm').test(body)) throw new Error('name mismatch');
        available.add(fs.realpathSync(file));
      } catch (error) {
        if (!['ENOENT', 'ENOTDIR'].includes(error.code)) findings.push(finding('skill-lane-unreadable', `${name} in ${root}: ${error.message}`, { skill: name }));
      }
    }
    if (available.size !== 1) findings.push(finding('skill-lane-missing', `${name}: expected one personal source, found ${available.size}; make the catalog available to this host without copying it into the project.`, { skill: name }));
  }
  const projectRoots = [[lane, null]];
  const seenRoots = new Set();
  try { seenRoots.add(fs.realpathSync(lane)); } catch { /* The adapter finding above names it. */ }
  for (const relative of projectDiscoveryRoots) {
    let real;
    try { real = fs.realpathSync(path.join(project, relative)); } catch { continue; }
    if (seenRoots.has(real)) continue;
    seenRoots.add(real);
    projectRoots.push([path.join(project, relative), relative]);
  }
  for (const name of catalogNames) {
    for (const [directory, relative] of projectRoots) {
      if (fs.existsSync(path.join(directory, name, 'SKILL.md'))) findings.push(finding('personal-catalog-unavailable', `${name} has a project copy${relative ? ` in ${relative}` : ''}; preserve the personal source and reconcile the project duplicate.`, { skill: name, ...(relative ? { root: relative } : {}) }));
    }
  }
  if (findings.length) findings.push(finding('personal-catalog-unavailable', 'Personal-catalog setup is incomplete; repair the stated discovery or ownership gap before selection or claims.'));
  return findings;
}
