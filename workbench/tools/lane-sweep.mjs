#!/usr/bin/env node
// Lane Sweep: a read-only report that counts the live local branches,
// remote-tracking branches, worktrees and open PRs, classifies each against
// its owning Spec and reports lane drift. It is a report, not a store and not
// a gate: it writes no file, and it deletes, merges, pushes, fetches, checks
// out and rewrites nothing. Every Git call is read-only plumbing run with
// optional locks off, so even `git status` does not refresh an index.
// Remote-tracking refs are read as last fetched.
import fs from 'node:fs';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import crypto from 'node:crypto';
import { declaredGit, findRoot, isMainModule, lanePath, laneRelative } from './workbench-paths.mjs';
import { loadRetiredSpecs, loadSpecs, resolveIntegrationContainmentRef } from './spec-workbench.mjs';
import { parseFrontmatter } from './adr.mjs';
import { visibleIdKey } from './visible-ids.mjs';

export const LANE_SWEEP_DRIFT_KINDS = Object.freeze({
  'planned-spec-has-candidate': 'Spec says planned, but a candidate exists',
  'merged-into-assembly-not-integration': 'Merged into an assembly branch, not into integration',
  'idle-merged-worktree': 'Idle merged worktree, safe to delete with git branch -d'
});
// A worktree in one of these states is mid-operation and never idle.
const IN_PROGRESS = Object.freeze(['MERGE_HEAD', 'REBASE_HEAD', 'rebase-merge', 'rebase-apply', 'CHERRY_PICK_HEAD', 'REVERT_HEAD', 'BISECT_LOG']);
export const GH_PR_FIELDS = Object.freeze(['number', 'title', 'headRefName', 'baseRefName', 'isDraft', 'url']);
const READ_ENV = { ...process.env, GIT_OPTIONAL_LOCKS: '0' };
// A Spec or Task identifier in a branch name or PR title: case-insensitive,
// any width (`S-01T`, `s-005q`, `TK-00AA`), bounded by non-alphanumerics and
// carrying at least one digit, so an ordinary word such as `s-bad` is not one.
const ID_PATTERN = /(?<![A-Za-z0-9])(S|TK)-(?=[A-Za-z0-9]*[0-9])([A-Za-z0-9]+)(?![A-Za-z0-9])/gi;

function fail(code, message) { const error = new Error(message); error.code = code; throw error; }
function git(root, args) {
  const run = spawnSync('git', ['-C', root, ...args], { encoding: 'utf8', env: READ_ENV, maxBuffer: 64 * 1024 * 1024 });
  if (run.error) fail('git-unavailable', `git could not run: ${run.error.message}`);
  return run;
}
function lines(text) { return (text ?? '').split('\n').map((line) => line.trim()).filter(Boolean); }

// Every Spec (active and retired) and every Task it carries, indexed by the
// collision key so every spelling of one identity (`S-901`, `s-0901`)
// resolves to the stored record.
function ownerIndex(root) {
  const specs = [...loadSpecs(root, { allowDuplicates: true }), ...loadRetiredSpecs(root)];
  const bySpec = new Map(), byTask = new Map();
  const add = (map, key, value) => { if (!key) return; if (!map.has(key)) map.set(key, []); if (!map.get(key).includes(value)) map.get(key).push(value); };
  for (const spec of specs) {
    const owner = { id: spec.id, path: spec.relativePath, status: spec.status ?? null };
    add(bySpec, visibleIdKey(spec.id), owner);
    if (spec.formerId) add(bySpec, visibleIdKey(spec.formerId), owner);
    for (const task of [...(spec.rows ?? []), ...(spec.records ?? []), ...(spec.retiredRecords ?? [])]) {
      add(byTask, visibleIdKey(task.id), owner);
      if (task.formerId) add(byTask, visibleIdKey(task.formerId), owner);
    }
  }
  return { bySpec, byTask };
}

function idsIn(texts) {
  const found = [];
  for (const text of texts) for (const match of String(text ?? '').matchAll(ID_PATTERN)) {
    const id = `${match[1].toUpperCase()}-${match[2]}`;
    if (!found.some((seen) => visibleIdKey(seen) === visibleIdKey(id))) found.push(id);
  }
  return found;
}

function classify(index, lanes, { branches, texts }) {
  const names = branches.filter(Boolean);
  if (names.includes(lanes.integration)) return { classification: 'integration-lane', ids: [], owners: [], unknownIds: [], ambiguousIds: [] };
  if (names.includes(lanes.default)) return { classification: 'default-lane', ids: [], owners: [], unknownIds: [], ambiguousIds: [] };
  const ids = idsIn([...names, ...texts]);
  const owners = [], unknownIds = [], ambiguousIds = [];
  const own = (owner) => { if (!owners.some((seen) => seen.id === owner.id && seen.path === owner.path)) owners.push(owner); };
  for (const id of ids) {
    const key = visibleIdKey(id);
    const matches = (id.startsWith('S-') ? index.bySpec : index.byTask).get(key) ?? [];
    // A legacy numeric Task label recurs across Specs; it names no single
    // owner, so it is reported rather than resolved to one of them.
    if (id.startsWith('TK-') && matches.length > 1) ambiguousIds.push(id);
    else if (matches.length === 0) unknownIds.push(id);
    else matches.forEach(own);
  }
  const classification = owners.length ? 'owned' : ambiguousIds.length ? 'ambiguous-id' : unknownIds.length ? 'unknown-id' : 'unowned';
  return { classification, ids, owners, unknownIds, ambiguousIds };
}

function containment(root, integration, sha) {
  if (!integration.sha || !sha) return null;
  const run = git(root, ['merge-base', '--is-ancestor', sha, integration.sha]);
  return run.status === 0 ? true : run.status === 1 ? false : null;
}

function readRefs(root) {
  const run = git(root, ['for-each-ref', '--format=%(refname)%09%(objectname)%09%(symref)%09%(upstream)', 'refs/heads', 'refs/remotes']);
  if (run.status !== 0) fail('git-unavailable', `git for-each-ref failed: ${run.stderr.trim()}`);
  const local = [], remote = [];
  for (const line of lines(run.stdout)) {
    const [ref, sha, symref, upstream] = line.split('\t');
    if (ref.startsWith('refs/heads/')) local.push({ ref, name: ref.slice('refs/heads/'.length), branch: ref.slice('refs/heads/'.length), sha, upstream: upstream || null });
    else {
      // `refs/remotes/<remote>/HEAD` is a remote's own pointer, never a branch.
      const name = ref.slice('refs/remotes/'.length);
      if (symref || name.endsWith('/HEAD')) continue;
      remote.push({ ref, name, branch: name.slice(name.indexOf('/') + 1), sha });
    }
  }
  return { local, remote };
}

function readWorktrees(root, refs) {
  const run = git(root, ['worktree', 'list', '--porcelain']);
  if (run.status !== 0) fail('git-unavailable', `git worktree list failed: ${run.stderr.trim()}`);
  const worktrees = [];
  let current = null;
  for (const line of run.stdout.split('\n')) {
    if (line.startsWith('worktree ')) { current = { path: line.slice('worktree '.length), sha: null, branch: null, detached: false, bare: false, prunable: false, locked: false }; worktrees.push(current); }
    else if (!current) continue;
    else if (line.startsWith('HEAD ')) current.sha = line.slice(5);
    else if (line.startsWith('branch ')) current.branch = line.slice(7).replace(/^refs\/heads\//, '');
    else if (line === 'detached') current.detached = true;
    else if (line === 'bare') current.bare = true;
    else if (line.startsWith('prunable')) current.prunable = true;
    else if (line.startsWith('locked')) current.locked = true;
  }
  // `git worktree list` always prints the main worktree first.
  worktrees.forEach((worktree, position) => { worktree.main = position === 0; });
  for (const worktree of worktrees) {
    try { worktree.path = fs.realpathSync(worktree.path); } catch { /* A prunable worktree's directory is gone; keep Git's path. */ }
    // A detached worktree is classified through the branches whose tip is its
    // HEAD commit, if any.
    worktree.branchesAtHead = worktree.branch ? [worktree.branch] : [...refs.local, ...refs.remote].filter((ref) => ref.sha === worktree.sha).map((ref) => ref.name);
  }
  return worktrees;
}

// The Wiki jot target of each Spec: every active Wiki page whose frontmatter
// `source_paths` cites the Spec's SPEC.md or its folder, else the jot topic
// named by the Spec folder. Pages are read for metadata only.
function wikiCitations(root) {
  let wiki;
  try { wiki = lanePath(root, 'wiki'); } catch { return []; }
  const pages = [];
  const walk = (directory) => {
    let entries;
    try { entries = fs.readdirSync(directory, { withFileTypes: true }); } catch { return; }
    for (const entry of entries.sort((a, b) => a.name.localeCompare(b.name))) {
      // Jot refuses routers, contracts, historical collections and dot files.
      if (entry.name.startsWith('.') || entry.isSymbolicLink() || ['archive', 'skills-draft'].includes(entry.name)) continue;
      const absolute = path.join(directory, entry.name);
      if (entry.isDirectory()) { walk(absolute); continue; }
      if (!entry.isFile() || !entry.name.endsWith('.md') || ['MEMORY.md', 'SCHEMA.md', 'AGENTS.md'].includes(entry.name)) continue;
      let data;
      try { ({ data } = parseFrontmatter(fs.readFileSync(absolute, 'utf8'))); } catch { continue; }
      // A shared jot needs an existing page with normal handling metadata.
      if (!data || data.sensitivity !== 'normal' || !data.knowledge_role) continue;
      const cited = (Array.isArray(data.source_paths) ? data.source_paths : [data.source_paths]).filter((entry) => typeof entry === 'string' && entry).map((entry) => entry.replace(/\/+$/, ''));
      if (cited.length) pages.push({ page: path.relative(root, absolute).split(path.sep).join('/'), absolute, cited, designConcept: data.type === 'design-concept' });
    }
  };
  walk(wiki);
  return pages;
}

function quote(value) { return `'${String(value).replace(/'/g, `'\\''`)}'`; }
function revisionOf(absolute) {
  try { return crypto.createHash('sha256').update(fs.readFileSync(absolute, 'utf8')).digest('hex'); } catch { return null; }
}

function jotRoute(root, citations, spec, content) {
  if (!spec) return { route: 'none', reason: 'No owning Spec; no jot target. Name the owner first, then jot on its Spec\'s Wiki page.', topic: null, content, targets: [] };
  const tool = `node ${laneRelative(root, 'tools')}/jot.mjs`;
  const folder = path.posix.dirname(spec.path);
  const topic = path.posix.basename(folder).toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '') || 'lane-sweep';
  const common = `--kind observation --state current --source ${quote(spec.path)} --author AGENT --content ${quote(content)}`;
  const pages = citations.filter((page) => page.cited.some((cited) => cited === spec.path || cited === folder || cited.startsWith(`${folder}/`)));
  if (pages.length) return {
    route: 'page', topic, content,
    targets: pages.map((page) => {
      const revision = revisionOf(page.absolute);
      return { page: page.page, visibility: 'shared', exists: true, revision,
        read: `${tool} read --page ${quote(page.page)}`,
        add: `${tool} add --page ${quote(page.page)} --visibility shared --revision ${revision} ${page.designConcept ? `--operation ${quote('Lane Sweep')} ` : ''}${common}` };
    })
  };
  // No page cites the Spec: use the shared project-topic capture default.
  const page = `${laneRelative(root, 'wiki')}/context-${topic}.md`;
  const absolute = path.resolve(root, page);
  const revision = fs.existsSync(absolute) ? revisionOf(absolute) : null;
  return {
    route: 'topic', topic, content,
    targets: [{ page, visibility: 'shared', exists: revision !== null, revision,
      read: `${tool} read --topic ${topic}`,
      add: `${tool} add --topic ${topic} ${revision ? `--revision ${revision} ` : ''}${common}` }]
  };
}

// Every ref that holds a tip, other than the lanes themselves, the branch's
// own local/remote-tracking twin and refs at the very same commit. One
// `for-each-ref --contains` walk per distinct uncontained tip, cached.
function containingBranches(root, cache, lanes, item) {
  if (!cache.has(item.sha)) {
    const run = git(root, ['for-each-ref', '--contains', item.sha, '--format=%(refname)%09%(objectname)%09%(symref)', 'refs/heads', 'refs/remotes']);
    cache.set(item.sha, run.status === 0 ? lines(run.stdout).map((line) => line.split('\t')) : null);
  }
  const found = cache.get(item.sha);
  if (!found) return null;
  const names = [];
  for (const [ref, sha, symref] of found) {
    if (symref || sha === item.sha) continue;
    const local = ref.startsWith('refs/heads/');
    const name = local ? ref.slice('refs/heads/'.length) : ref.slice('refs/remotes/'.length);
    if (!local && name.endsWith('/HEAD')) continue;
    const branch = local ? name : name.slice(name.indexOf('/') + 1);
    if ([lanes.integration, lanes.default, item.branch].includes(branch)) continue;
    names.push(name);
  }
  return names;
}

// A linked worktree is idle when it has no staged, unstaged or untracked
// change, is not locked and is not mid-merge, rebase, cherry-pick, revert or
// bisect. Ignored entries are counted: `git worktree remove` deletes them.
function worktreeState(worktree) {
  const status = git(worktree.path, ['status', '--porcelain', '--ignored', '--untracked-files=normal']);
  if (status.status !== 0) return { idle: false, reason: 'git status failed' };
  const entries = status.stdout.split('\n').filter(Boolean);
  const changes = entries.filter((entry) => !entry.startsWith('!! '));
  if (changes.length) return { idle: false, reason: `${changes.length} uncommitted or untracked change(s)` };
  const dir = git(worktree.path, ['rev-parse', '--absolute-git-dir']);
  if (dir.status !== 0) return { idle: false, reason: 'git directory unreadable' };
  const busy = IN_PROGRESS.filter((name) => fs.existsSync(path.join(dir.stdout.trim(), name)));
  if (busy.length) return { idle: false, reason: `operation in progress (${busy.join(', ')})` };
  return { idle: true, ignoredEntries: entries.length - changes.length };
}

// The default open-PR source: one `gh pr list` read. Missing, failing or
// unauthenticated `gh` is a limitation, never a crash.
export function readOpenPrs(root, { gh = 'gh' } = {}) {
  const run = spawnSync(gh, ['pr', 'list', '--state', 'open', '--json', [...GH_PR_FIELDS, 'headRefOid'].join(','), '--limit', '500'], { cwd: root, encoding: 'utf8', env: { ...READ_ENV, GH_PROMPT_DISABLED: '1', GH_NO_UPDATE_NOTIFIER: '1' }, maxBuffer: 64 * 1024 * 1024 });
  if (run.error) return { status: 'unavailable', source: 'gh', reason: run.error.code === 'ENOENT' ? `gh not found (${run.error.code})` : `gh could not run: ${run.error.message}`, prs: null };
  if (run.status !== 0) return { status: 'unavailable', source: 'gh', reason: `gh pr list failed (exit ${run.status}): ${(run.stderr || run.stdout).trim().split('\n')[0] || 'no message'}`, prs: null };
  try { return { status: 'available', source: 'gh', reason: null, prs: validatePrs(JSON.parse(run.stdout)) }; }
  catch (error) { return { status: 'unavailable', source: 'gh', reason: `gh output was not a PR list: ${error.message}`, prs: null }; }
}

export function validatePrs(value) {
  if (!Array.isArray(value)) fail('invalid-prs', 'the open-PR list must be a JSON array');
  return value.map((pr, position) => {
    if (!pr || typeof pr !== 'object' || !Number.isInteger(pr.number) || typeof pr.headRefName !== 'string') fail('invalid-prs', `open PR entry ${position} needs an integer number and a headRefName`);
    return { number: pr.number, title: typeof pr.title === 'string' ? pr.title : '', headRefName: pr.headRefName, baseRefName: pr.baseRefName ?? null, isDraft: pr.isDraft ?? null, url: pr.url ?? null, headRefOid: pr.headRefOid ?? null };
  });
}

function resolveCommit(root, ref) {
  const run = git(root, ['rev-parse', '--verify', '--quiet', `${ref}^{commit}`]);
  return run.status === 0 ? run.stdout.trim() || null : null;
}

// `options.prs`: an injected PR array (tests, `--prs FILE`); otherwise
// `readOpenPrs` runs `options.gh` (default `gh`).
export function sweepLanes(project, options = {}) {
  const start = path.resolve(project ?? process.cwd());
  if (!fs.existsSync(start)) fail('not-a-workbench', `${start} does not exist`);
  const root = findRoot(start);
  if (!fs.existsSync(path.join(root, 'workbench', 'manifest.json'))) fail('not-a-workbench', `${start} is not a Workbench repository: no workbench/manifest.json`);
  const top = git(root, ['rev-parse', '--show-toplevel']);
  if (top.status !== 0) fail('not-a-workbench', `${root} is not a Workbench repository inside a Git work tree`);
  let declared;
  try { declared = declaredGit(root); } catch (error) { fail('not-a-workbench', `${root} is not a valid Workbench repository: ${error.message}`); }
  let index;
  try { index = ownerIndex(root); } catch (error) { fail('not-a-workbench', `${root} Spec records could not be read: ${error.message}`); }
  const limitations = ['Remote-tracking refs are read as last fetched; nothing is fetched or pruned, so a branch deleted on the remote still counts until a fetch with prune.'];
  const integration = resolveIntegrationContainmentRef(root);
  const lanes = { integration: declared?.integrationBranch ?? null, default: declared?.defaultBranch ?? null };
  if (!integration.ref) limitations.push('No git.integrationBranch is declared in workbench/manifest.json; integration containment is unknown and no candidate is reported.');
  else if (!integration.sha) limitations.push(`Integration ref ${integration.ref} does not resolve; integration containment is unknown and no candidate is reported.`);

  const refs = readRefs(root);
  const worktrees = readWorktrees(root, refs);
  let prSource;
  if (options.prs !== undefined) {
    try { prSource = { status: 'available', source: 'injected', reason: null, prs: validatePrs(options.prs) }; }
    catch (error) { fail('invalid-prs', error.message); }
  } else prSource = readOpenPrs(root, { gh: options.gh });
  if (prSource.status !== 'available') limitations.push(`Open PRs unavailable: ${prSource.reason}. Branches and worktrees are still reported.`);

  const items = [];
  const push = (base, classifyWith) => {
    const result = classify(index, lanes, classifyWith);
    items.push({ ...base, ...result, containedInIntegration: containment(root, integration, base.sha) });
  };
  for (const ref of refs.local) push({ type: 'local-branch', name: ref.name, ref: ref.ref, branch: ref.branch, sha: ref.sha }, { branches: [ref.branch], texts: [] });
  for (const ref of refs.remote) push({ type: 'remote-tracking-branch', name: ref.name, ref: ref.ref, branch: ref.branch, sha: ref.sha }, { branches: [ref.branch, ref.name], texts: [] });
  for (const worktree of worktrees) push({ type: 'worktree', name: worktree.path, path: worktree.path, branch: worktree.branch, sha: worktree.sha, detached: worktree.detached, bare: worktree.bare, prunable: worktree.prunable, locked: worktree.locked, branchesAtHead: worktree.branchesAtHead },
    { branches: worktree.branchesAtHead.map((name) => refs.remote.find((ref) => ref.name === name)?.branch ?? name), texts: worktree.branch ? [] : worktree.branchesAtHead });
  for (const pr of prSource.prs ?? []) {
    const sha = (pr.headRefOid && resolveCommit(root, pr.headRefOid)) || resolveCommit(root, `refs/remotes/origin/${pr.headRefName}`) || resolveCommit(root, `refs/heads/${pr.headRefName}`);
    push({ type: 'open-pr', name: `#${pr.number}`, number: pr.number, title: pr.title, branch: pr.headRefName, baseBranch: pr.baseRefName, isDraft: pr.isDraft, url: pr.url, sha }, { branches: [pr.headRefName], texts: [pr.title] });
  }

  // Every finding names its owning Spec (or none) and that Spec's Wiki jot
  // target; an item with several owners yields one finding per owner.
  const revision = resolveCommit(root, 'HEAD');
  const citations = wikiCitations(root);
  const findings = [];
  const report = (kind, item, owners, extra = {}) => {
    const lane = `${LABELS[item.type]} ${item.type === 'open-pr' ? `${item.name} (${item.branch})` : item.type === 'worktree' ? `on ${item.branch}` : item.name}`;
    for (const owner of owners.length ? owners : [null]) {
      const spec = owner ? { id: owner.id, path: owner.path, status: owner.status } : null;
      const content = `Lane Sweep at ${revision ? revision.slice(0, 12) : 'no commit'}: ${LANE_SWEEP_DRIFT_KINDS[kind]} - ${lane} at ${item.sha ? item.sha.slice(0, 12) : 'unknown commit'}${extra.containedIn ? `, contained in ${extra.containedIn.join(', ')}` : ''}.`;
      findings.push({ kind, message: LANE_SWEEP_DRIFT_KINDS[kind], spec,
        item: { type: item.type, name: item.name, ...(item.path ? { path: item.path } : {}), branch: item.branch, sha: item.sha, containedInIntegration: item.containedInIntegration, classification: item.classification, ...(item.url ? { url: item.url } : {}) },
        ...extra, jot: jotRoute(root, citations, spec, content) });
    }
  };
  const ownersOf = (item) => item.classification === 'owned' ? item.owners : [];
  if (integration.sha) {
    // Drift kind 1. A branch is a candidate when its tip is proven outside
    // integration; an open PR is one unless its head is proven contained,
    // since an open PR is unmerged by definition. Worktrees are reported
    // through their branches.
    for (const item of items) {
      if (item.classification !== 'owned' || item.type === 'worktree') continue;
      const candidate = item.type === 'open-pr' ? item.containedInIntegration !== true : item.containedInIntegration === false;
      const planned = item.owners.filter((owner) => owner.status === 'planned');
      if (candidate && planned.length) report('planned-spec-has-candidate', item, planned);
    }
    // Drift kind 2. A branch tip outside integration that another branch
    // holds: merged (or stacked) into an assembly lane, not into integration.
    const contains = new Map();
    for (const item of items) {
      if (!['local-branch', 'remote-tracking-branch'].includes(item.type) || item.containedInIntegration !== false || ['integration-lane', 'default-lane'].includes(item.classification)) continue;
      const containedIn = containingBranches(root, contains, lanes, item);
      if (containedIn?.length) report('merged-into-assembly-not-integration', item, ownersOf(item), { containedIn });
    }
    // Drift kind 3. A linked worktree on a branch integration contains, idle.
    for (const item of items) {
      if (item.type !== 'worktree' || item.containedInIntegration !== true || ['integration-lane', 'default-lane'].includes(item.classification)) continue;
      const worktree = worktrees.find((entry) => entry.path === item.path);
      if (!worktree || worktree.main || !worktree.branch || worktree.bare || worktree.prunable || worktree.locked) continue;
      const state = worktreeState(worktree);
      if (!state.idle) continue;
      const local = refs.local.find((ref) => ref.branch === worktree.branch);
      const upstreamSha = local?.upstream ? resolveCommit(root, local.upstream) : null;
      const upstreamHolds = upstreamSha ? git(root, ['merge-base', '--is-ancestor', worktree.sha, upstreamSha]).status === 0 : false;
      const commands = [`git worktree remove ${quote(worktree.path)}`,
        ...(upstreamHolds ? [] : [`git branch --set-upstream-to=${integration.ref} ${quote(worktree.branch)}`]),
        `git branch -d ${quote(worktree.branch)}`];
      const warnings = state.ignoredEntries ? [`git worktree remove deletes ${state.ignoredEntries} ignored entr${state.ignoredEntries === 1 ? 'y' : 'ies'} in this worktree without asking; check them first.`] : [];
      report('idle-merged-worktree', item, ownersOf(item), { cleanup: { safe: true, runBy: 'a person or agent by hand; Lane Sweep runs none of these', commands, ignoredEntries: state.ignoredEntries, warnings, note: 'git branch -d deletes only a branch merged into its upstream, or into HEAD when it has none, so the integration upstream is set first when the current one does not hold it.' } });
    }
  }

  const dirty = git(root, ['status', '--porcelain']);
  if (!citations.length) limitations.push('No Wiki page cites a Spec in its source_paths; every routed finding falls back to its Spec folder jot topic.');
  return {
    schemaVersion: 1, operation: 'lane-sweep', root,
    readOnly: 'Writes no file; deletes, merges, pushes, fetches, checks out and rewrites nothing.',
    specRecords: { revision, integrationRef: integration.ref, integrationSha: integration.sha, matchesIntegration: revision && integration.sha ? revision === integration.sha : null, dirty: dirty.status === 0 ? Boolean(dirty.stdout.trim()) : null },
    lanes: { integrationBranch: lanes.integration, defaultBranch: lanes.default, integrationSource: integration.source },
    counts: { localBranches: refs.local.length, remoteTrackingBranches: refs.remote.length, worktrees: worktrees.length, openPrs: prSource.prs ? prSource.prs.length : null },
    prs: { status: prSource.status, source: prSource.source, reason: prSource.reason },
    summary: Object.fromEntries(['integration-lane', 'default-lane', 'owned', 'ambiguous-id', 'unknown-id', 'unowned'].map((name) => [name, items.filter((item) => item.classification === name).length])),
    items, findings, limitations
  };
}

const LABELS = { 'local-branch': 'local branch', 'remote-tracking-branch': 'remote-tracking branch', worktree: 'worktree', 'open-pr': 'open PR' };
function contained(value) { return value === true ? 'in integration' : value === false ? 'not in integration' : 'containment unknown'; }
export function formatLaneSweep(report) {
  const out = [];
  const { specRecords: records, counts } = report;
  out.push('lane-sweep: read-only report; writes, deletes, merges, pushes and rewrites nothing');
  out.push('Jot commands run from the room root; replace AGENT with your agent name and read the page first if it changed since this report.');
  out.push(`Spec records read at ${records.revision ?? 'no commit'}${records.dirty ? ' (working tree dirty)' : ''}; integration ${records.integrationRef ?? 'undeclared'} at ${records.integrationSha ?? 'unresolved'}; ${records.matchesIntegration === true ? 'equal' : records.matchesIntegration === false ? 'not equal' : 'not comparable'}`);
  out.push(`Live counts: local branches ${counts.localBranches}, remote-tracking branches ${counts.remoteTrackingBranches}, worktrees ${counts.worktrees}, open PRs ${counts.openPrs ?? 'unavailable'}`);
  out.push(`Classified: ${Object.entries(report.summary).map(([name, count]) => `${name} ${count}`).join(', ')}`);
  out.push('', `Drift (${report.findings.length}):`);
  if (!report.findings.length) out.push('  none');
  for (const finding of report.findings) {
    const owner = finding.spec ? `${finding.spec.id} (${finding.spec.path}, status ${finding.spec.status})` : 'no owning Spec';
    const lane = `${LABELS[finding.item.type]} ${finding.item.name}${finding.item.type === 'open-pr' || finding.item.type === 'worktree' ? ` (${finding.item.branch})` : ''}`;
    out.push(`  ${finding.message}: ${owner} - ${lane}, ${contained(finding.item.containedInIntegration)}${finding.containedIn ? `, contained in ${finding.containedIn.join(', ')}` : ''}`);
    if (finding.cleanup) {
      out.push(`    cleanup (run by hand, never by Lane Sweep): ${finding.cleanup.commands.join(' && ')}`);
      for (const warning of finding.cleanup.warnings) out.push(`    warning: ${warning}`);
    }
    if (finding.jot.route === 'none') out.push('    route: no owning Spec; no jot target');
    else for (const target of finding.jot.targets) out.push(`    jot: ${target.add}`);
  }
  out.push('', 'Lanes:');
  for (const item of report.items) {
    const owner = item.owners.length ? item.owners.map((entry) => `${entry.id} [${entry.status}]`).join(', ') : '';
    const extra = [...item.unknownIds.map((id) => `${id} matches no Spec record`), ...item.ambiguousIds.map((id) => `${id} matches several Specs`)];
    const label = item.type === 'worktree' ? `${item.name} (${item.branch ?? `detached at ${item.sha?.slice(0, 12)}`})` : item.type === 'open-pr' ? `${item.name} ${item.branch}` : item.name;
    out.push(`  ${LABELS[item.type]} ${label}: ${item.classification}${owner ? ` ${owner}` : ''}${extra.length ? ` (${extra.join('; ')})` : ''}; ${contained(item.containedInIntegration)}`);
  }
  out.push('', 'Limitations:', ...report.limitations.map((line) => `  - ${line}`));
  return out.join('\n');
}

export function parseLaneSweepArgs(argv) {
  const options = { json: false, root: process.cwd(), prsFile: null };
  for (let i = 0; i < argv.length; i++) {
    const arg = argv[i];
    if (arg === '--json') options.json = true;
    else if (arg === '--root' || arg === '--prs') {
      const value = argv[++i];
      if (!value || value.startsWith('--')) fail('invalid-invocation', `${arg} needs a value`);
      if (arg === '--root') options.root = value; else options.prsFile = value;
    } else if (arg === '--help' || arg === '-h') options.help = true;
    else fail('invalid-invocation', `Unknown argument: ${arg}`);
  }
  return options;
}

const USAGE = 'Usage: lane-sweep.mjs [--root PATH] [--json] [--prs FILE]\n  Read-only: classifies every branch, worktree and open PR against its owning Spec and reports lane drift.\n  --prs FILE reads the open PRs from a JSON array (the shape of gh pr list --json number,title,headRefName,baseRefName,isDraft,url) instead of running gh.';

if (isMainModule(import.meta.url)) {
  try {
    const options = parseLaneSweepArgs(process.argv.slice(2));
    if (options.help) console.log(USAGE);
    else {
      let prs;
      if (options.prsFile) {
        try { prs = JSON.parse(fs.readFileSync(path.resolve(options.prsFile), 'utf8')); }
        catch (error) { fail('invalid-prs', `--prs ${options.prsFile} could not be read as JSON: ${error.message}`); }
      }
      const report = sweepLanes(options.root, prs === undefined ? {} : { prs });
      console.log(options.json ? JSON.stringify(report, null, 2) : formatLaneSweep(report));
      process.exitCode = 0;
    }
  } catch (error) {
    console.error(`lane-sweep: ${error.message}`);
    if (error.code === 'invalid-invocation') console.error(USAGE);
    process.exitCode = 2;
  }
}
