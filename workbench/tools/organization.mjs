// Selected-file organization for the optional research and release homes.
// The manifest remains fixed; these operations never relocate its stores or Git.
import crypto from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import { planReferenceRewrite, splitEvidenceSection } from './adr.mjs';
import { COLLECTIONS, LANES, assertSafeReadPath, assertSafeWritePath, collectionRelative, laneRelative, markdownLinkTargets, readManifest, writeSafeFile } from './workbench-paths.mjs';

const digest = value => crypto.createHash('sha256').update(value).digest('hex');
const jsonHash = value => digest(JSON.stringify(value));
const adapterNames = new Set(['.agents/skills', '.claude/skills']);
const fail = (code, message, extra = {}) => ({ status: 'blocked', error: { code, message, ...extra } });
const issue = (code, message) => { throw Object.assign(new Error(message), { code }); };
const stat = target => { try { return fs.lstatSync(target); } catch (error) { if (error.code === 'ENOENT') return null; throw error; } };
const same = (a, b) => JSON.stringify(a) === JSON.stringify(b);
function guarded(operation) {
  try { return operation(); } catch (error) { return fail(error.code ?? 'organization-refused', error.message); }
}
function git(root, args, allowed = [0]) {
  if (['GIT_DIR', 'GIT_WORK_TREE', 'GIT_INDEX_FILE'].some(name => process.env[name])) issue('git-override', 'Clear Git repository/index overrides before organization.');
  const result = spawnSync('git', ['--no-optional-locks', ...(args[0] === 'check-ignore' ? [] : ['--literal-pathspecs']), '-C', root, ...args], { encoding: 'utf8', env: { ...process.env, GIT_OPTIONAL_LOCKS: '0' }, maxBuffer: 64 * 1024 * 1024 });
  if (result.error || !allowed.includes(result.status)) issue('git-unavailable', `Git could not establish organization state: ${result.error?.message ?? result.stderr.trim()}`);
  return result;
}
function relative(value) {
  if (typeof value !== 'string' || !value || path.posix.normalize(value) !== value || value.startsWith('/') || value.startsWith('../') || value === '..' || /[\\\x00-\x1f\x7f]/.test(value) || /^[a-z]:/i.test(value)) issue('unsafe-path', 'Organization paths must be normalized paths inside the room.');
  if (value.split('/').some(part => ['.git', '.worktrees', 'research papers'].includes(part.toLowerCase()))) issue('protected-path', 'Git workspaces and protected reference material are inventory-only, never selected files.');
  return value;
}
function exactCase(root, value) {
  let current = root;
  for (const part of value.split('/')) {
    const entry = stat(current);
    if (!entry) return;
    if (!entry.isDirectory() || entry.isSymbolicLink()) issue('unsafe-path', 'A selected ancestor is not an ordinary directory.');
    const matches = fs.readdirSync(current).filter(name => name.toLowerCase() === part.toLowerCase());
    if (matches.length > 1 || (matches.length === 1 && matches[0] !== part)) issue('case-collision', `The spelling of ${value} conflicts with an existing path.`);
    current = path.join(current, part);
  }
}
function admitted(root, value, { adapter = false, write = false } = {}) {
  relative(value);
  exactCase(root, value);
  const absolute = path.join(root, value);
  if (adapter && adapterNames.has(value) && stat(absolute)?.isSymbolicLink()) {
    assertSafeReadPath(root, path.dirname(absolute));
    const target = fs.readlinkSync(absolute);
    if (value !== '.claude/skills' || target !== '../.agents/skills' || fs.realpathSync(absolute) !== fs.realpathSync(path.join(root, laneRelative(root, 'skills')))) issue('unsafe-adapter', `${value} does not resolve to the room skills lane through the selected relative link.`);
    return absolute;
  }
  (write ? assertSafeWritePath : assertSafeReadPath)(root, absolute);
  for (let ancestor = path.dirname(absolute); ancestor !== root; ancestor = path.dirname(ancestor)) {
    if (stat(path.join(ancestor, '.git'))) issue('nested-repository', 'A selected path belongs to a nested Git repository; retain it through its owner.');
  }
  return absolute;
}
function state(root, value, { optional = false } = {}) {
  const absolute = admitted(root, value, { adapter: true });
  const entry = stat(absolute);
  if (!entry) { if (optional) return null; issue('missing-source', `${value} is absent; reconcile the map before planning.`); }
  if (entry.isSymbolicLink() && adapterNames.has(value)) {
    const target = fs.readlinkSync(absolute);
    return { type: 'adapter', sha256: digest(target), target };
  }
  // S-006I TK-00BQ: .agents/skills is the skills lane itself, a discovery root
  // retained in place like the .claude/skills link to it.
  if (adapterNames.has(value) && value === laneRelative(root, 'skills') && entry.isDirectory()) {
    return { type: 'adapter', sha256: digest(`lane:${value}`), target: value };
  }
  if (!entry.isFile()) issue('unsupported-source', 'Select individual ordinary files; directories, worktrees and special files remain with their owner.');
  if (entry.mode & 0o7000) issue('unsupported-mode', 'A selected file has special permission bits; retain and reconcile it before migration.');
  return { type: 'file', sha256: digest(fs.readFileSync(absolute)), mode: entry.mode & 0o777 };
}
function snapshot(root) {
  if (fs.realpathSync(git(root, ['rev-parse', '--show-toplevel']).stdout.trim()) !== root) issue('not-room-root', 'Run organization at the Git room root.');
  const index = git(root, ['rev-parse', '--path-format=absolute', '--git-path', 'index']).stdout.trim();
  const entry = stat(index);
  if (entry && (!entry.isFile() || entry.isSymbolicLink() || entry.nlink > 1)) issue('unsafe-index', 'The Git index must be an ordinary, unshared file.');
  return {
    head: git(root, ['rev-parse', '--verify', 'HEAD']).stdout.trim(),
    gitDir: git(root, ['rev-parse', '--absolute-git-dir']).stdout.trim(),
    commonDir: git(root, ['rev-parse', '--path-format=absolute', '--git-common-dir']).stdout.trim(),
    indexSha256: entry ? digest(fs.readFileSync(index)) : null,
    refs: git(root, ['for-each-ref', '--format=%(refname) %(objectname)', 'refs/heads', 'refs/stash']).stdout,
    worktrees: git(root, ['worktree', 'list', '--porcelain']).stdout
  };
}
function recordPath(root, file) {
  const absolute = path.resolve(file);
  for (let ancestor = path.dirname(absolute); ; ancestor = path.dirname(ancestor)) {
    try { if (fs.realpathSync(ancestor) === root) return path.join(root, path.relative(ancestor, absolute)); } catch { /* Admission below reports the unavailable path. */ }
    if (path.dirname(ancestor) === ancestor) break;
  }
  return absolute;
}
function readJson(root, file) {
  const absolute = recordPath(root, file);
  assertSafeReadPath(root, absolute);
  const entry = stat(absolute);
  if (!entry?.isFile() || entry.isSymbolicLink() || entry.nlink > 1) issue('unsafe-record', 'The selected map, plan or receipt must be an ordinary, unshared file inside the room.');
  return JSON.parse(fs.readFileSync(absolute, 'utf8'));
}
function mapEntries(root, map) {
  if (!map || map.schemaVersion !== 1 || typeof map.owner !== 'string' || !map.owner.trim() || !Array.isArray(map.entries) || !map.entries.length || Object.keys(map).some(key => !['schemaVersion', 'owner', 'entries'].includes(key))) issue('invalid-map', 'Use schemaVersion 1, a named owner and a nonempty entries array.');
  const sourceNames = new Set(), destinations = new Set();
  const docs = laneRelative(root, 'docs');
  const optionalHome = value => [`${docs}/research/`, `${docs}/releases/`].some(prefix => value.startsWith(prefix));
  return map.entries.map(item => {
    if (!item || Object.keys(item).some(key => !['source', 'destination', 'action', 'owner', 'privacy', 'reason'].includes(key)) || !['move', 'retain'].includes(item.action) || !['shared', 'private'].includes(item.privacy) || ![item.owner, item.reason].every(value => typeof value === 'string' && value.trim())) issue('invalid-map', 'Each entry needs source, action, owner, privacy and reason; a move also needs destination.');
    const source = relative(item.source);
    const destination = item.action === 'move' ? relative(item.destination) : source;
    if (item.action === 'retain' && item.destination !== undefined && item.destination !== source) issue('invalid-map', 'A retain entry cannot change location.');
    const sourceKey = source.toLowerCase(), targetKey = destination.toLowerCase();
    if (sourceNames.has(sourceKey) || destinations.has(targetKey)) issue('duplicate-path', 'Every selected source and destination must occur exactly once, including case aliases.');
    sourceNames.add(sourceKey); destinations.add(targetKey);
    if (item.action === 'move' && (source === destination || item.privacy !== 'shared' || !optionalHome(destination) || !(/^(research|releases)\//.test(source) || optionalHome(source)))) issue('out-of-scope-move', 'Only shared research or release files may move into their optional docs homes. Application files, skills, stores, output and private context are retained.');
    admitted(root, source, { adapter: true });
    if (item.action === 'move') admitted(root, destination, { write: true });
    return { source, destination, action: item.action, owner: item.owner, privacy: item.privacy, reason: item.reason };
  }).sort((a, b) => a.source.localeCompare(b.source));
}
function ignored(root, value) { return git(root, ['check-ignore', '--quiet', '--no-index', '--', value], [0, 1]).status === 0; }
function room(root) {
  root = fs.realpathSync(path.resolve(root));
  assertSafeReadPath(root, path.join(root, 'workbench/manifest.json'));
  const manifest = readManifest(root);
  if (!manifest || manifest.schemaVersion !== 2 || !manifest.workbenchId || Object.keys(manifest.lanes ?? {}).length !== Object.keys(LANES).length || Object.entries(LANES).some(([name, value]) => manifest.lanes?.[name] !== value) || manifest.collections?.recovery !== COLLECTIONS.recovery) issue('invalid-room', 'Organization needs the fixed schema 2 seven-lane room and its existing identity/recovery collection; it is not a lane relocation engine.');
  return root;
}
function planned(root, map) {
  root = room(root);
  const definitions = mapEntries(root, map);
  const locations = new Map(definitions.map(item => [path.join(root, item.source), path.join(root, item.destination)]));
  const totals = { referencesRewritten: {}, historicalReferencesLeft: {} };
  const entries = definitions.map(item => {
    const before = state(root, item.source);
    if (item.action === 'move' && stat(path.join(root, item.destination))) issue('destination-collision', `${item.destination} already exists; organization never overwrites it.`);
    if (before.type === 'adapter' && item.action !== 'retain') issue('unsafe-adapter', 'Discovery adapters are retained at their existing locations.');
    const gitState = git(root, ['ls-files', '--error-unmatch', '--', item.source], [0, 1]).status === 0 ? 'tracked' : ignored(root, item.source) ? 'ignored' : 'untracked';
    if (gitState === 'ignored' && item.privacy !== 'private') issue('privacy-conflict', 'Ignored material must be explicitly private and retained; private-to-shared transfer is outside organization.');
    let bytes = before.type === 'file' ? fs.readFileSync(path.join(root, item.source)) : null;
    let historicalSha256 = null;
    if (bytes && item.privacy === 'shared' && item.source.endsWith('.md')) {
      const content = new TextDecoder('utf-8', { fatal: true }).decode(bytes);
      historicalSha256 = digest(splitEvidenceSection(content).evidence);
      // Rebase outgoing links to unmoved files as well as moved destinations.
      for (const link of markdownLinkTargets(content)) {
        const target = path.resolve(path.dirname(path.join(root, item.source)), link);
        if (target.startsWith(root + path.sep) && stat(target) && !locations.has(target)) locations.set(target, target);
      }
      const rewritten = planReferenceRewrite(root, path.join(root, item.destination), content, path.dirname(path.join(root, item.source)), path.dirname(path.join(root, item.destination)), locations, totals);
      if (rewritten !== null) bytes = Buffer.from(rewritten);
    }
    const after = before.type === 'file' ? { ...before, sha256: digest(bytes) } : before;
    if (item.action === 'move' || !same(before, after)) admitted(root, item.source, { write: true });
    return { ...item, gitState, before, after, historicalSha256 };
  });
  // A destination cannot consume another selected source, even on a filesystem
  // that would happen to permit the resulting rename order.
  const selected = new Set(entries.map(item => item.source.toLowerCase()));
  if (entries.some(item => item.action === 'move' && selected.has(item.destination.toLowerCase()))) issue('destination-collision', 'A move destination is another selected source.');
  const body = { schemaVersion: 1, owner: map.owner, root, manifestSha256: digest(fs.readFileSync(path.join(root, 'workbench/manifest.json'))), snapshot: snapshot(root), entries, createdDirectories: createdDirectories(root, { entries }), ...totals };
  return { ...body, digest: jsonHash(body) };
}
function validPlan(root, plan) {
  root = room(root);
  if (!plan || plan.schemaVersion !== 1 || plan.root !== root || !plan.snapshot || !Array.isArray(plan.entries)) issue('invalid-plan', 'Use a plan from this exact room.');
  const { digest: expected, ...body } = plan;
  if (!/^[a-f0-9]{64}$/.test(expected ?? '') || jsonHash(body) !== expected) issue('invalid-plan', 'The plan digest does not match its recorded content.');
  mapEntries(root, { schemaVersion: 1, owner: plan.owner, entries: plan.entries.map(({ source, destination, action, owner, privacy, reason }) => ({ source, destination, action, owner, privacy, reason })) });
  return root;
}
function states(plan, which) {
  const result = new Map();
  for (const item of plan.entries) {
    result.set(item.source, which === 'before' ? item.before : item.action === 'move' ? null : item.after);
    if (item.action === 'move') result.set(item.destination, which === 'after' ? item.after : null);
  }
  return result;
}
function checkStates(root, expected) {
  for (const [relative, wanted] of expected) if (!same(state(root, relative, { optional: true }), wanted)) issue('changed-source', `${relative} differs from the recorded state; preserve and reconcile it first.`);
}
function sameRoom(root, plan) {
  if (digest(fs.readFileSync(path.join(root, 'workbench/manifest.json'))) !== plan.manifestSha256 || !same(snapshot(root), plan.snapshot)) issue('changed-room', 'The manifest, index, refs or Git worktree topology changed after planning. Regenerate the map proof.');
}
function receiptRelative(root, plan) { return `${collectionRelative(root, 'recovery')}/organization/${plan.digest}.json`; }
function saveReceipt(root, relative, receipt) {
  const target = path.join(root, relative);
  admitted(root, relative, { write: true });
  if (!ignored(root, relative)) issue('recovery-not-private', 'The existing recovery collection must be ignored before any operation.');
  // Start private before writing any bytes; writeSafeFile uses a public mode.
  fs.mkdirSync(path.dirname(target), { recursive: true, mode: 0o700 });
  const temporary = fs.mkdtempSync(path.join(path.dirname(target), '.receipt-'));
  try {
    fs.writeFileSync(path.join(temporary, 'data'), JSON.stringify(receipt) + '\n', { mode: 0o600, flag: 'wx' });
    fs.renameSync(path.join(temporary, 'data'), target);
  } finally { fs.rmdirSync(temporary); }
}
function expectedBytes(root, plan) {
  const locations = new Map(plan.entries.map(item => [path.join(root, item.source), path.join(root, item.destination)]));
  const result = new Map();
  for (const item of plan.entries) {
    if (item.before.type !== 'file') continue;
    const bytes = fs.readFileSync(path.join(root, item.source));
    let after = bytes;
    if (item.privacy === 'shared' && item.source.endsWith('.md')) {
      const content = new TextDecoder('utf-8', { fatal: true }).decode(bytes);
      for (const link of markdownLinkTargets(content)) {
        const target = path.resolve(path.dirname(path.join(root, item.source)), link);
        if (target.startsWith(root + path.sep) && stat(target) && !locations.has(target)) locations.set(target, target);
      }
      const rewritten = planReferenceRewrite(root, path.join(root, item.destination), content, path.dirname(path.join(root, item.source)), path.dirname(path.join(root, item.destination)), locations, { referencesRewritten: {}, historicalReferencesLeft: {} });
      if (rewritten !== null) after = Buffer.from(rewritten);
    }
    if (digest(bytes) !== item.before.sha256 || digest(after) !== item.after.sha256) issue('changed-source', 'Selected contents or expected link transformations no longer match the plan.');
    result.set(item.source, { before: bytes.toString('base64'), after: after.toString('base64') });
  }
  return result;
}
function createdDirectories(root, plan) {
  const missing = new Set();
  for (const item of plan.entries.filter(item => item.action === 'move')) {
    for (let directory = path.dirname(item.destination); directory !== '.'; directory = path.dirname(directory)) if (!stat(path.join(root, directory))) missing.add(directory);
  }
  return [...missing].sort((a, b) => a.split('/').length - b.split('/').length || a.localeCompare(b));
}
function readReceipt(root, relative, plan) {
  if (relative !== receiptRelative(root, plan)) issue('invalid-receipt', 'Use the exact organization receipt in the room recovery collection.');
  const receipt = readJson(root, path.join(root, relative));
  if (!same(receipt.plan, plan) || !['applying', 'applied', 'rolled-back', 'incomplete'].includes(receipt.state) || !Array.isArray(receipt.backups) || !Array.isArray(receipt.createdDirectories)) issue('invalid-receipt', 'The recovery receipt does not match this plan.');
  const files = plan.entries.filter(item => item.before.type === 'file');
  if (receipt.backups.length !== files.length) issue('invalid-receipt', 'The backup inventory is incomplete.');
  for (const item of files) {
    const backup = receipt.backups.filter(value => value.source === item.source);
    if (backup.length !== 1 || !['before', 'after'].every(which => typeof backup[0][which] === 'string' && Buffer.from(backup[0][which], 'base64').toString('base64') === backup[0][which] && digest(Buffer.from(backup[0][which], 'base64')) === item[which].sha256)) issue('invalid-receipt', 'Backup bytes do not match their recorded hashes.');
  }
  const expectedDirectories = new Set(createdDirectoriesFromPlan(plan));
  if (!same(receipt.createdDirectories, plan.createdDirectories) || receipt.createdDirectories.some(directory => !expectedDirectories.has(directory))) issue('invalid-receipt', 'The recovery directory inventory differs from the frozen plan.');
  return receipt;
}
function createdDirectoriesFromPlan(plan) {
  const directories = new Set();
  for (const item of plan.entries.filter(item => item.action === 'move')) for (let directory = path.dirname(item.destination); directory !== '.'; directory = path.dirname(directory)) directories.add(relative(directory));
  return [...directories];
}
function restore(root, receipt) {
  const plan = receipt.plan;
  sameRoom(root, plan);
  const before = states(plan, 'before'), after = states(plan, 'after');
  // Interrupted moves can contain both copies, or only the old copy. Any third
  // state belongs to new work and blocks recovery before a restoration writes.
  for (const [relative, wanted] of before) {
    const current = state(root, relative, { optional: true });
    if (!same(current, wanted) && !same(current, after.get(relative))) issue('rollback-conflict', `${relative} changed outside the migration; preserve it before recovery.`);
  }
  for (const item of plan.entries) if (item.before.type === 'file') {
    const backup = receipt.backups.find(value => value.source === item.source);
    if (!same(state(root, item.source, { optional: true }), item.before)) {
      writeSafeFile(root, admitted(root, item.source, { write: true }), Buffer.from(backup.before, 'base64'));
      fs.chmodSync(path.join(root, item.source), item.before.mode);
    }
  }
  for (const item of plan.entries.filter(item => item.action === 'move')) {
    const target = admitted(root, item.destination, { write: true });
    if (stat(target)) fs.unlinkSync(target);
  }
  for (const directory of [...receipt.createdDirectories].sort((a, b) => b.split('/').length - a.split('/').length || b.localeCompare(a))) {
    const target = path.join(root, relative(directory));
    assertSafeReadPath(root, target);
    if (stat(target)) fs.rmdirSync(target);
  }
  checkStates(root, before);
  sameRoom(root, plan);
}
export function planOrganization(project, mapFile) {
  return guarded(() => {
    const root = room(project);
    return { status: 'planned', plan: planned(root, readJson(root, mapFile)), limitations: ['Selected files only; the caller establishes that its selection is complete.', 'Worktree registrations are inventoried in place; native host behavior and semantic reconciliation need separate proof.'] };
  });
}
function applyUnlocked(project, planFile, options = {}) {
  return guarded(() => {
    const root = room(project), plan = readJson(root, planFile);
    validPlan(root, plan);
    const relative = receiptRelative(root, plan);
    if (stat(path.join(root, relative))) {
      const old = readReceipt(root, relative, plan);
      if (old.state === 'applied') { sameRoom(root, plan); checkStates(root, states(plan, 'after')); return { status: 'current', digest: plan.digest, receipt: relative }; }
      if (old.state !== 'rolled-back') return fail('recovery-required', 'An interrupted migration needs its recorded rollback before reapplication.', { receipt: relative });
    }
    sameRoom(root, plan);
    checkStates(root, states(plan, 'before'));
    const map = { schemaVersion: 1, owner: plan.owner, entries: plan.entries.map(({ source, destination, action, owner, privacy, reason }) => ({ source, destination, action, owner, privacy, reason })) };
    if (!same(planned(root, map), plan)) issue('changed-source', 'The planned inventory or transformations changed; plan again before writing.');
    const contents = expectedBytes(root, plan);
    const receipt = { schemaVersion: 1, state: 'applying', plan, backups: [...contents].map(([source, bytes]) => ({ source, ...bytes })), createdDirectories: plan.createdDirectories };
    saveReceipt(root, relative, receipt);
    let writes = 0;
    try {
      for (const item of plan.entries) {
        if (item.before.type !== 'file' || (item.action === 'retain' && same(item.before, item.after))) continue;
        const target = admitted(root, item.destination, { write: true });
        writeSafeFile(root, target, Buffer.from(contents.get(item.source).after, 'base64'), { exclusive: item.action === 'move' });
        fs.chmodSync(target, item.after.mode);
        options.afterWrite?.(++writes);
        if (item.action === 'move') fs.unlinkSync(admitted(root, item.source, { write: true }));
      }
      checkStates(root, states(plan, 'after'));
      sameRoom(root, plan);
      receipt.state = 'applied';
      saveReceipt(root, relative, receipt);
      return { status: 'organized', digest: plan.digest, receipt: relative, selected: plan.entries.length, moved: plan.entries.filter(item => item.action === 'move').length, referencesRewritten: plan.referencesRewritten, historicalReferencesLeft: plan.historicalReferencesLeft, historicalSourceCommit: plan.snapshot.head };
    } catch (error) {
      try { restore(root, receipt); receipt.state = 'rolled-back'; saveReceipt(root, relative, receipt); return fail('organization-interrupted', 'The operation failed and its original file/index/topology state was restored.', { receipt: relative, restored: true, cause: error.code ?? 'write-failed' }); }
      catch (recovery) { receipt.state = 'incomplete'; saveReceipt(root, relative, receipt); return fail('rollback-incomplete', 'Recovery found a conflict; keep the receipt and all originals for explicit reconciliation.', { receipt: relative, restored: false, cause: recovery.code ?? 'recovery-failed' }); }
    }
  });
}
function rollbackUnlocked(project, receiptFile) {
  return guarded(() => {
    const root = room(project), absolute = recordPath(root, receiptFile);
    const loaded = readJson(root, absolute);
    const plan = loaded.plan;
    validPlan(root, plan);
    const relative = path.relative(root, absolute).split(path.sep).join('/');
    const receipt = readReceipt(root, relative, plan);
    if (receipt.state === 'rolled-back') { sameRoom(root, plan); checkStates(root, states(plan, 'before')); return { status: 'current', digest: plan.digest, receipt: relative }; }
    restore(root, receipt);
    receipt.state = 'rolled-back';
    saveReceipt(root, relative, receipt);
    return { status: 'rolled-back', digest: plan.digest, receipt: relative, restored: plan.entries.length };
  });
}

// Share the existing layout identity lock so direct API calls and the CLI
// serialize with native layout/identity changes. An orphan lock is retained.
function withOrganizationLock(project, operation) {
  const root = room(project), lock = path.join(root, 'workbench/.identity.lock');
  assertSafeWritePath(root, lock);
  let descriptor;
  try {
    try { descriptor = fs.openSync(lock, 'wx', 0o600); }
    catch (error) { if (error.code === 'EEXIST') issue('organization-busy', 'A layout operation owns .identity.lock; preserve the lock until its owner or recovery procedure releases it.'); throw error; }
    fs.writeFileSync(descriptor, JSON.stringify({ operation: 'organization', pid: process.pid }) + '\n');
    return operation(root);
  } finally { if (descriptor !== undefined) { fs.closeSync(descriptor); fs.unlinkSync(lock); } }
}
export function applyOrganization(project, planFile, options = {}) {
  return guarded(() => withOrganizationLock(project, root => applyUnlocked(root, planFile, options)));
}
export function rollbackOrganization(project, receiptFile) {
  return guarded(() => withOrganizationLock(project, root => rollbackUnlocked(root, receiptFile)));
}
