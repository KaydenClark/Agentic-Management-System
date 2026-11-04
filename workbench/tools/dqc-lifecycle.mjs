// Shared terminal/Board lifecycle. Records own understanding; projections are derived.
import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import crypto from 'node:crypto';
import { spawnSync } from 'node:child_process';
import { declaredTracker, trackerDeclaration, assertSafeReadPath, assertSafeWritePath, writeSafeFile } from './workbench-paths.mjs';
import { scanPrivacy } from './privacy.mjs';

export const LIFECYCLE_SCHEMA = 'landmark-tracker/destination-question@3';
const text = value => typeof value === 'string' && value.trim().length > 0;
function canonical(value) { return JSON.stringify(value, (_key, item) => item && typeof item === 'object' && !Array.isArray(item) ? Object.fromEntries(Object.keys(item).sort().map(key => [key, item[key]])) : item); }
const hash = value => crypto.createHash('sha256').update(canonical(value)).digest('hex');
export const digestProposal = proposal => hash({readback:proposal.readback, why:proposal.why, scope:proposal.scope});
function refusal(code, message) { const error = new Error(message); error.code = code; throw error; }
function git(root, args, options = {}) {
  const result = spawnSync('git', args, { cwd: root, encoding: 'utf8', ...options });
  if (result.status !== 0) refusal('git-failed', result.stderr || result.stdout || `git ${args[0]} failed`);
  return result.stdout.trim();
}
function put(root, relative, body) { const file = path.join(root, relative); assertSafeWritePath(root, file); writeSafeFile(root, file, body); }
function json(value) { return `${JSON.stringify(value, null, 2)}\n`; }
export function lifecycleProblems(value) {
  if (!value || typeof value !== 'object' || Array.isArray(value)) return ['lifecycle must be an object'];
  if (!['pending', 'confirmed', 'needs-rewrite', 'deferred', 'superseded', 'reopened'].includes(value.state)) return ['invalid lifecycle state'];
  if (!Array.isArray(value.events) || !Array.isArray(value.confirmations)) return ['lifecycle events and confirmations must be arrays'];
  if (value.proposal !== null) {
    try { validateProposal(value.proposal); } catch (error) { return [error.message]; }
    if (value.digest !== digestProposal(value.proposal)) return ['proposal digest does not match'];
  }
  if (value.proposal === null && value.digest !== null) return ['missing proposal must have null digest'];
  const ids = new Set();
  for (const event of value.events) {
    if (!event || !text(event.eventId) || ids.has(event.eventId) || !text(event.type) || !Number.isInteger(event.revision) || !/^[0-9a-f]{64}$/.test(event.requestDigest ?? '') || !(event.note === null || typeof event.note === 'string')) return ['invalid or repeated lifecycle event'];
    ids.add(event.eventId);
  }
  for (const confirmation of value.confirmations) {
    if (confirmation?.legacy === true && text(confirmation.source) && confirmation.scope === null && confirmation.proposal === null && (confirmation.readback === null || typeof confirmation.readback === 'string') && text(confirmation.question) && confirmation.confirmation?.basis === confirmation.source) continue;
    if (!confirmation || !text(confirmation.source) || !text(confirmation.scope) || !confirmation.proposal || confirmation.readback !== confirmation.proposal.readback || confirmation.digest !== digestProposal(confirmation.proposal)) return ['invalid exact confirmation snapshot'];
  }
  if (value.state === 'confirmed' && (!value.proposal || value.confirmations.at(-1)?.digest !== value.digest)) return ['confirmed state needs a matching exact confirmation'];
  return [];
}
function validateProposal(proposal) {
  if (!proposal || !['readback', 'why', 'source', 'scope', 'round'].every(key => text(proposal[key]))) refusal('invalid-action', 'proposal needs exact readback, why, source, scope and round');
  for (const key of ['priority', 'value']) if (!proposal[key] || !Number.isInteger(proposal[key].value) || proposal[key].value < 1 || proposal[key].value > 4 || !text(proposal[key].reason)) refusal('invalid-action', `${key} needs value 1..4 and reason`);
  if (!Array.isArray(proposal.dependencies) || proposal.dependencies.some(item => !text(item))) refusal('invalid-action', 'proposal dependencies must be a text array');
  const keys = ['readback', 'why', 'source', 'scope', 'round', 'priority', 'value', 'dependencies', 'actionable'];
  if (proposal.actionable !== undefined && typeof proposal.actionable !== 'boolean') refusal('invalid-action', 'actionable must be boolean when supplied');
  if (Object.keys(proposal).some(key => !keys.includes(key))) refusal('invalid-action', 'proposal contains unsupported fields');
}
function lifecycle(record) { return record.lifecycle ?? { state: 'pending', proposal: null, digest: null, confirmations: record.confirmation ? [{legacy:true,readback:record.answer,question:record.question,source:record.confirmation.basis,scope:null,digest:null,proposal:null,revision:record.confirmation.revision,confirmation:structuredClone(record.confirmation)}] : [], events: [] }; }
function roundFile(declared) { return `${declared.root}/rounds.json`; }
export function readRounds(root) {
  const declared = declaredTracker(root);
  const file = path.join(root, roundFile(declared));
  assertSafeReadPath(root, file);
  if (!fs.existsSync(file)) return { schema: 'landmark-tracker/rounds@1', currentRound: null, rounds: [], events: [] };
  const entry = fs.lstatSync(file);
  if (!entry.isFile() || entry.nlink > 1) refusal('unsafe-path', 'Round record must be an ordinary unshared file');
  const data = JSON.parse(fs.readFileSync(file, 'utf8'));
  if (data.schema !== 'landmark-tracker/rounds@1' || !Array.isArray(data.rounds) || !Array.isArray(data.events)) refusal('invalid-record', 'invalid round record');
  return data;
}
export function addLifecycleViews(projection, root) {
  const declared = declaredTracker(root);
  for (const card of projection.questions) {
    const record = JSON.parse(fs.readFileSync(path.join(root, declared.collections['destination-questions'], `${card.id}.json`), 'utf8'));
    card.lifecycle = lifecycle(record);
  }
  const rounds = readRounds(root); projection.rounds = rounds.rounds; projection.currentRound = rounds.currentRound;
  return projection;
}
function htmlText(value) { return String(value).replaceAll('&', '&amp;').replaceAll('<', '&lt;').replaceAll('>', '&gt;'); }
function markdownText(value) { return htmlText(value).replace(/([\\`*_[\]{}()#+.!|])/g, '\\$1'); }
function questionFingerprint(value) { return value.normalize('NFKC').toLowerCase().replace(/[\p{P}\p{S}\p{Cf}\s]/gu, ''); }
export function renderTrackerMarkdown(projection, declared) {
  const lines = ['# Intent tracker', '', 'Generated from DQC records. Execution state and proof remain in Landmarks, Specs and Tasks.', ''];
  for (const card of projection.questions) {
    const life = card.lifecycle ?? {};
    lines.push(`## ${card.id} — ${markdownText(card.title)}`, '', `Revision ${card.revision}; ${life.state ?? 'legacy'}. [Record](${declared.collections['destination-questions']}/${card.id}.json)`, '');
    if (life.proposal) lines.push(`<pre>${htmlText(life.proposal.readback)}</pre>`, '', `Source: ${markdownText(life.proposal.source)}. Scope: ${markdownText(life.proposal.scope)}.`, '', `Round: ${markdownText(life.proposal.round)}. Dependencies: ${life.proposal.dependencies.map(markdownText).join(', ') || 'none'}.`, '');
    else lines.push(markdownText(card.question ?? card.origin.question), '');
    for (const related of card.related ?? []) lines.push(`- ${related.home ? `[${markdownText(related.key)}](${encodeURI(related.home).replaceAll('(', '%28').replaceAll(')', '%29')})` : markdownText(related.key)} (${markdownText(related.resolution)}): ${markdownText(related.reason)}`);
    if (card.expectedResult) lines.push('', `Expected result: ${markdownText(card.expectedResult.change)}${card.expectedResult.home ? ` — ${markdownText(card.expectedResult.home)}` : ''}.`);
    if (card.result) lines.push('', `Recorded outcome (r${card.result.revision}): ${markdownText(card.result.summary)}.`);
    if (card.uncertainty?.length) lines.push('', `Unresolved: ${card.uncertainty.map(markdownText).join('; ')}.`);
    for (const event of life.events ?? []) lines.push(`- ${markdownText(event.type)} at r${event.revision}: ${markdownText(event.note ?? '')}`);
    lines.push('');
  }
  for (const round of projection.rounds ?? []) lines.push(`## Round ${markdownText(round.id)}`, '', `Owner finished: ${round.finished ? 'yes' : 'no'}; reconciliation: ${round.receipt ? 'recorded' : 'pending'}. Changed DQCs: ${round.changed.map(item => item.id).join(', ') || 'none'}.`, '');
  return `${lines.join('\n')}\n`;
}
export function writeMarkdown(root, projection) {
  const declared = declaredTracker(root);
  if (declared.markdown) put(root, declared.markdown, renderTrackerMarkdown(projection, declared));
}

// All native mutators share this lock, including older capture/revise operations.
export function withTrackerLock(root, operation) {
  const gitDir = git(root, ['rev-parse', '--absolute-git-dir']);
  const lock = path.join(gitDir, 'workbench-tracker.lock');
  try { fs.mkdirSync(lock); } catch (error) { if (error.code === 'EEXIST') refusal('tracker-busy', 'Another native tracker writer holds the lock; retry after it finishes.'); throw error; }
  try { return operation(); } finally { fs.rmdirSync(lock); }
}
function records(root, declared) {
  return fs.readdirSync(path.join(root, declared.collections['destination-questions'])).filter(name => !name.startsWith('.') && name.endsWith('.json')).map(name => ({ relative: `${declared.collections['destination-questions']}/${name}`, record: JSON.parse(fs.readFileSync(path.join(root, declared.collections['destination-questions'], name), 'utf8')) }));
}
function operationEvents(root, declared) { return [...records(root, declared).flatMap(item => lifecycle(item.record).events), ...readRounds(root).events]; }
function sameRequest(event, request, id) { return event.requestDigest === hash({id:id ?? null,request}); }
function eventCommit(root, eventId, files) {
  const entries = git(root, ['log', '--format=%H%x00%B%x00', '--fixed-strings', `--grep=Workbench-event: ${eventId}`, '--', ...files]).split('\0');
  for (let index = 0; index + 1 < entries.length; index += 2) if (entries[index + 1].split('\n').includes(`Workbench-event: ${eventId}`)) return entries[index].trim();
  return '';
}
function ownedPaths(root, declared) {
  return [...records(root, declared).map(item => item.relative), declared.projection, ...(declared.markdown ? [declared.markdown] : []), roundFile(declared)];
}
// A separate index excludes unrelated staged work. Holding the real index lock
// prevents a competing index writer while its original bytes are preserved.
function commitTransaction(root, paths, eventId, expectedHead, operation) {
  const index = git(root, ['rev-parse', '--git-path', 'index']);
  const indexPath = path.resolve(root, index), indexLock = `${indexPath}.lock`;
  let descriptor;
  try { descriptor = fs.openSync(indexLock, 'wx'); } catch { refusal('index-busy', 'Git index is locked; no tracker files changed.'); }
  let before;
  try { before = new Map(paths.map(relative => { const file = path.join(root, relative); assertSafeWritePath(root, file); return [relative, fs.existsSync(file) ? fs.readFileSync(file) : null]; })); } catch (error) { fs.closeSync(descriptor); fs.unlinkSync(indexLock); throw error; }
  const temporary = fs.mkdtempSync(path.join(os.tmpdir(), 'dqc-index-'));
  const environment = { ...process.env, GIT_INDEX_FILE: path.join(temporary, 'commit-index') };
  const head = expectedHead;
  let committed = false;
  try {
    if (git(root, ['rev-parse', 'HEAD']) !== head) refusal('stale-head', 'HEAD changed before the transaction snapshot; refresh before acting.');
    if (git(root, ['status', '--porcelain', '--untracked-files=all', '--', ...paths])) refusal('dirty-tracker', 'Tracker records or projections have uncommitted changes; preserve and reconcile them before an action.');
    const result = operation();
    git(root, ['read-tree', head], { env: environment });
    git(root, ['add', '--', ...paths.filter(relative => fs.existsSync(path.join(root, relative)))], { env: environment });
    // Build the commit without moving HEAD, then compare-and-swap its exact
    // expected parent. Hooks inspect the same isolated index before publication.
    git(root, ['hook', 'run', '--ignore-missing', 'pre-commit'], { env: environment });
    const message = path.join(temporary, 'message');
    fs.writeFileSync(message, `Record DQC ${result.type}\n\nWorkbench-event: ${eventId}\n`);
    git(root, ['hook', 'run', '--ignore-missing', 'prepare-commit-msg', '--', message, 'message'], { env: environment });
    git(root, ['hook', 'run', '--ignore-missing', 'commit-msg', '--', message], { env: environment });
    git(root, ['diff', '--exit-code', '--', ...paths], { env: environment });
    const tree = git(root, ['write-tree'], { env: environment });
    const commit = git(root, ['commit-tree', tree, '-p', head, '-F', message], { env: environment });
    const publication = spawnSync('git', ['update-ref', '-m', `DQC event ${eventId}`, 'HEAD', commit, head], { cwd: root, encoding: 'utf8' });
    if (publication.status !== 0) refusal('stale-head', 'HEAD changed during the action; no DQC commit was published. Refresh before retrying.');
    committed = true;
    const changedFiles = git(root, ['diff-tree', '--no-commit-id', '--name-only', '-r', commit]).split('\n').filter(Boolean);
    // Rebase only the owned entries in the original index onto the new HEAD.
    const preserved = { ...process.env, GIT_INDEX_FILE: path.join(temporary, 'preserved-index') };
    if (fs.existsSync(indexPath)) fs.copyFileSync(indexPath, preserved.GIT_INDEX_FILE);
    else git(root, ['read-tree', head], { env: preserved });
    git(root, ['add', '--', ...changedFiles], { env: preserved });
    fs.writeFileSync(descriptor, fs.readFileSync(preserved.GIT_INDEX_FILE));
    fs.closeSync(descriptor); descriptor = null;
    fs.renameSync(indexLock, indexPath);
    return { status: 'committed', commit, changedFiles, ...result };
  } catch (error) {
    if (!committed) for (const [relative, bytes] of before) { const file = path.join(root, relative); if (bytes === null) { if (fs.existsSync(file)) fs.unlinkSync(file); } else fs.writeFileSync(file, bytes); }
    else { error.code = 'committed-index-failure'; error.message = `The DQC commit succeeded; index reconciliation failed. Preserve work and inspect HEAD. ${error.message}`; }
    throw error;
  } finally {
    if (descriptor !== null && descriptor !== undefined) fs.closeSync(descriptor);
    if (fs.existsSync(indexLock)) fs.unlinkSync(indexLock);
    fs.rmSync(temporary, { recursive: true, force: true });
  }
}

function verifyReceiptSource(root, source) {
  // Source verification checks existence at a pinned project revision, not the
  // semantic truth of the agent's claimed reconciliation.
  const separator = source.lastIndexOf('@');
  const relative = source.slice(0, separator), revision = source.slice(separator + 1);
  if (separator < 1 || !/^[0-9a-f]{40}$/.test(revision) || !relative.startsWith('workbench/') || !relative.endsWith('.md') || relative.split('/').some(part => part === '..' || part === '.')) refusal('invalid-receipt-source', 'Receipt sources must be existing workbench Markdown paths@full-project-commit');
  git(root, ['cat-file', '-e', `${revision}:${relative}`]);
}

export function applyAction(root, id, request, native) {
  if (!request || typeof request !== 'object' || Array.isArray(request)) refusal('invalid-action', 'Action input must be an object');
  if (!/^[A-Za-z0-9][A-Za-z0-9_-]{7,127}$/.test(request.eventId ?? '')) refusal('invalid-action', 'eventId must be a stable 8..128 character token');
  if (!/^[0-9a-f]{40}$/.test(request.expectHead ?? '')) refusal('invalid-action', 'expectHead must identify the displayed Git commit');
  if (scanPrivacy(JSON.stringify(request)).length) refusal('private-content', 'Action contains private material; use a safe source reference.');
  const declared = declaredTracker(root);
  if (!declared) refusal('tracker-undeclared', 'Enable the tracker through setup-workbench first');
  return withTrackerLock(root, () => {
    native.show(root);
    const previous = operationEvents(root, declared).find(event => event.eventId === request.eventId);
    if (previous) {
      if (!sameRequest(previous, request, id)) refusal('event-collision', 'eventId already names a different action');
      const commit = eventCommit(root, request.eventId, ownedPaths(root, declared));
      if (!commit) refusal('uncommitted-event', 'Retry event is not in committed history; preserve and reconcile records');
      return { status: 'replayed', commit, changedFiles: [], eventId: request.eventId };
    }
    if (git(root, ['rev-parse', 'HEAD']) !== request.expectHead) refusal('stale-head', 'The project changed after this view; refresh before acting.');
    const manifest = JSON.parse(fs.readFileSync(path.join(root, 'workbench/manifest.json'), 'utf8'));
    const inputs = [declared.root, 'workbench/manifest.json', manifest.lanes.specs, manifest.collections.landmarks, manifest.collections.adr, manifest.collections.grilling].filter(Boolean);
    if (git(root, ['status', '--porcelain', '--untracked-files=all', '--', ...inputs])) refusal('dirty-tracker-input', 'A tracker projection input has uncommitted changes; preserve and reconcile it before acting.');
    const inventory = records(root, declared);
    const target = inventory.find(item => item.record.id === id);
    const roundAction = ['finish-round', 'reconcile-round'].includes(request.type);
    if (!roundAction && !target) refusal('unknown-identity', `No DQC is named ${id}`);
    if (!roundAction && request.expectRevision !== target.record.revision) refusal('stale-revision', 'DQC revision changed; refresh before acting');
    if (!roundAction && request.type !== 'propose' && request.digest !== lifecycle(target.record).digest) refusal('stale-content', 'The displayed proposal digest differs; refresh before acting');
    const paths = ownedPaths(root, declared);
    return commitTransaction(root, paths, request.eventId, request.expectHead, () => {
      const event = { eventId: request.eventId, type: request.type, at: new Date().toISOString(), requestDigest: hash({id:id ?? null,request}), source: request.source ?? null, note: request.note ?? null };
      if (roundAction) {
        if (!text(request.round)) refusal('invalid-action', 'Round action needs round');
        const store = readRounds(root);
        let round = store.rounds.find(item => item.id === request.round);
        if (request.type === 'finish-round') {
          if (round?.finished) refusal('round-finished', 'This round is already finished');
          const reviewed = new Map();
          for (const prior of store.rounds) for (const card of prior.changed) reviewed.set(card.id, Math.max(reviewed.get(card.id) ?? 0, card.revision));
          const pending = inventory.filter(item => item.record.revision > (reviewed.get(item.record.id) ?? 0)).map(({record}) => ({id:record.id, revision:record.revision, state:lifecycle(record).state, unanswered:lifecycle(record).state !== 'confirmed', dependencies:lifecycle(record).proposal?.dependencies ?? [], events:lifecycle(record).events.filter(event => event.revision > (reviewed.get(record.id) ?? 0)), history:record.history.filter(entry => entry.revision > (reviewed.get(record.id) ?? 0))}));
          round = { id: request.round, finished: true, changed: pending, receipt: null, eventId: request.eventId };
          store.currentRound = `${request.round}-next`;
          store.rounds.push(round);
        } else {
          if (!round?.finished) refusal('round-open', 'Finish the round before reconciliation');
          const receipt = request.receipt;
          if (!receipt || !Array.isArray(receipt.sources) || !receipt.sources.length || receipt.sources.some(item => !text(item)) || !text(receipt.outcome) || !text(receipt.nextFrontier)) refusal('invalid-action', 'Reconciliation needs sources, outcome and nextFrontier');
          if (round.receipt) refusal('round-reconciled', 'This round already has a reconciliation receipt');
          for (const source of receipt.sources) verifyReceiptSource(root, source);
          round.receipt = receipt;
        }
        store.events.push({ ...event, round: request.round });
        put(root, roundFile(declared), json(store));
        rebuildFromCommittedInputs(root, declared, request.expectHead, native.rebuild);
        return { type: request.type, eventId: request.eventId, round };
      }
      const record = target.record;
      const life = lifecycle(record);
      if (request.type === 'propose') {
        validateProposal(request.proposal);
        if (readRounds(root).rounds.some(round => round.id === request.proposal.round && round.finished)) refusal('round-finished', 'Start a new round after the owner finishes this one');
        if (life.proposal && questionFingerprint(life.proposal.readback) === questionFingerprint(request.proposal.readback) && life.state === 'needs-rewrite') refusal('rewrite-required', 'Rewrite the flagged/corrected readback before asking again');
        if (canonical(life.proposal) === canonical(request.proposal)) refusal('unchanged-proposal', 'The proposed readback has not changed');
        const substanceChanged = life.digest !== digestProposal(request.proposal);
        life.proposal = request.proposal; life.digest = digestProposal(request.proposal);
        if (substanceChanged) { life.state = 'pending'; record.confirmation = null; }
      } else if (request.type === 'confirm') {
        if (!life.proposal || life.state !== 'pending' && life.state !== 'reopened') refusal('not-confirmable', 'Only a pending displayed readback can be confirmed');
        if (!text(request.source) || request.scope !== life.proposal.scope) refusal('invalid-action', 'Confirmation needs its actual source and the exact displayed scope');
        life.confirmations.push({ readback: life.proposal.readback, proposal: structuredClone(life.proposal), digest: life.digest, source: request.source, scope: request.scope, revision: record.revision + 1, eventId: request.eventId, at: event.at });
        life.state = 'confirmed'; record.confirmation = { basis: request.source, revision: record.revision + 1 }; record.answer = life.proposal.readback;
      } else if (request.type === 'correct') {
        if (!['rework-wording', 'change-the-why', 'change'].includes(request.kind) || !text(request.note)) refusal('invalid-action', 'Correction needs kind and exact owner note');
        event.kind = request.kind; life.state = 'needs-rewrite'; record.confirmation = null;
      } else if (request.type === 'rate') {
        if (!Number.isInteger(request.rating) || request.rating < 1 || request.rating > 5) refusal('invalid-action', 'Rating must be 1..5');
        event.rating = request.rating;
      } else if (request.type === 'flag') { life.state = 'needs-rewrite'; record.confirmation = null;
      } else if (['defer', 'supersede', 'reopen'].includes(request.type)) {
        if (!text(request.note)) refusal('invalid-action', 'Disposition needs its reason');
        if (request.type === 'supersede') { if (!inventory.some(item => item.record.id === request.replacement) || request.replacement === id) refusal('unknown-identity', 'Supersession needs a distinct existing replacement DQC'); event.replacement = request.replacement; }
        life.state = { defer: 'deferred', supersede: 'superseded', reopen: 'reopened' }[request.type]; record.confirmation = null;
      } else refusal('invalid-action', `Unsupported action ${request.type}`);
      record.schema = LIFECYCLE_SCHEMA;
      record.related ??= []; record.claims ??= [];
      record.revision += 1;
      event.revision = record.revision; event.round = readRounds(root).currentRound ?? life.proposal?.round ?? null;
      life.events.push(event); record.lifecycle = life;
      record.history.push({ revision: record.revision, at: event.at, reason: `DQC ${request.type}`, changes: [{ field: 'lifecycle', to: structuredClone(life) }] });
      const problems = native.validate(record);
      if (problems.length) refusal('invalid-record', problems.join('; '));
      put(root, target.relative, json(record));
      rebuildFromCommittedInputs(root, declared, request.expectHead, native.rebuild);
      return { type: request.type, eventId: request.eventId, id, revision: record.revision, digest: life.digest, state: life.state };
    });
  });
}

// Materialize a pinned committed view, never dirty records. Only room records
// needed for typed identity resolution are read; hooks and filters do not run.
function withCommittedRoom(root, head, operation) {
  const temporary = fs.mkdtempSync(path.join(os.tmpdir(), 'dqc-read-'));
  try {
    const manifest = JSON.parse(git(root, ['show', `${head}:workbench/manifest.json`]));
    const declared = trackerDeclaration(manifest);
    if (!declared) refusal('tracker-undeclared', 'Committed manifest declares no tracker');
    const prefixes = ['workbench/manifest.json', declared.root, manifest.lanes.specs, manifest.collections.landmarks, manifest.collections.adr, manifest.collections.grilling].filter(Boolean);
    const files = git(root, ['ls-tree', '-r', '--name-only', head, '--', ...prefixes]).split('\n').filter(Boolean);
    if (files.some(relative => /[\r\n]/.test(relative))) refusal('unsafe-path', 'Committed record paths contain a line separator');
    const batch = spawnSync('git', ['cat-file', '--batch'], {cwd:root, input:files.map(relative => `${head}:${relative}\n`).join(''), maxBuffer:32*1024*1024});
    if (batch.status !== 0) refusal('git-failed', String(batch.stderr));
    let offset = 0;
    for (const relative of files) {
      const end = batch.stdout.indexOf(10,offset);
      const header = batch.stdout.subarray(offset,end).toString('utf8');
      const match = /^[0-9a-f]+ blob ([0-9]+)$/.exec(header);
      if (!match) refusal('git-failed', `Cannot read committed blob ${relative}`);
      const size = Number(match[1]), content = batch.stdout.subarray(end+1,end+1+size); offset=end+size+2;
      const file = path.join(temporary, relative); fs.mkdirSync(path.dirname(file), { recursive: true }); fs.writeFileSync(file,content);
    }
    for (const relative of [declared.root, ...Object.values(declared.collections)]) fs.mkdirSync(path.join(temporary, relative), { recursive: true });
    return operation(temporary);
  } finally { fs.rmSync(temporary, { recursive: true, force: true }); }
}

export function committedView(root, id, show) {
  const head = git(root, ['rev-parse', 'HEAD']);
  return withCommittedRoom(root, head, temporary => ({ ...show(temporary, id), head }));
}
function rebuildFromCommittedInputs(root, declared, head, rebuild) {
  return withCommittedRoom(root, head, temporary => {
    // Only intended owning records overlay the pinned source snapshot. Dirty
    // execution/landmark inputs can never enter a committed projection.
    for (const relative of ownedPaths(root, declared).filter(relative => relative !== declared.projection && relative !== declared.markdown)) {
      const file = path.join(root, relative);
      if (fs.existsSync(file)) { const target = path.join(temporary, relative); fs.mkdirSync(path.dirname(target), {recursive:true}); fs.copyFileSync(file,target); }
    }
    rebuild(temporary);
    for (const relative of [declared.projection, declared.markdown].filter(Boolean)) put(root,relative,fs.readFileSync(path.join(temporary,relative)));
  });
}
