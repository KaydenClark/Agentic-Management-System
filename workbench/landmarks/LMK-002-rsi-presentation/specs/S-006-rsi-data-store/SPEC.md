# S-006 - RSI data store

**Spec ID:** S-006
**Status:** active
**Priority:** 1
**Owner:** Kayden; orchestrator B (local, holds the Supabase keys)
**Stance:** Builder
**Updated:** 2026-11-03
**Catalog description:** Supabase schema and local Python writer for RSI results, build history, cost and tokens; the site reads under RLS.
**Blockers:** none
**Confirmation:** [JOT-a85076a7-25a3-45bd-bd33-220c62d87882](../../../../wiki/context-active-spec-approvals.md)
**Execution approval:** [JOT-a85076a7-25a3-45bd-bd33-220c62d87882](../../../../wiki/context-active-spec-approvals.md)
**Next gate:** Coverage/W disposition, whole Review, actual owner QA.

## Intent and authority

The [mapped owner intent](../../../../wiki/context-feedback-improvement-loop-plan.md#current-mapped-destination) authorizes this destination revision only. Existing execution approvals remain scoped; this Map creates no Tasks, runs, installation or deployment authority.

The owner decided that Python pushes RSI results to Supabase as they arrive and the site reads from it; everything the site shows, build history included, lives there. Token counts go with the RSI data. The service key stays in the gitignored local environment; the site receives only its publishable key.

## Outcome

One Supabase project holds every row the site presents; a local Python writer fills it; the site reads with the publishable key, never writes.

## Why It Matters

Charts are honest only if each number has a sourced row; local writes keep credentials off the site.

## Current Verified State

- **Met** (proof [TK-000B](tasks/TK-000B/TASK.md#proof); live checks and limits [TK-000L](tasks/TK-000L/TASK.md#resumed-local-verification-2026-11-01)): schema and provenance, no client writes, writer end to end, conflict refusal, real sources only, key loads and authenticates, no secrets in Git.
- **Met:** private assessment persistence ([TK-000Q](tasks/TK-000Q/TASK.md), [TK-000R](tasks/TK-000R/TASK.md), [TK-000S](tasks/TK-000S/TASK.md)); explicit unknown trial metrics ([TK-000P](tasks/TK-000P/TASK.md)).
- **Not met:** build history from real records. The owner-approved pinned import at `771bd1e` and its canonical readback pass ([proof](tasks/TK-000Z/approved-history-import-771bd1e.md)); history recorded after that pin is not imported, and latest coverage is unverified. A further import needs fresh explicit approval and must not rewrite original S-008 creation provenance via `--refresh-changed`.
- **Open:** [TK-000W](tasks/TK-000W/TASK.md) is stopped and unaccepted; whole-Spec binding and owner Human QA are open. The Spec is not accepted.

History: [S-006 history](../../../../wiki/history/S-006.md).

## Desired Behavior

- Tables for RSI results, build history and run metadata. Each result names task, held-out or dev, arm (AMS, no-AMS or plain instructions), system version (runtime, controls and skills commits), provider, model, effort, pass, cost, tokens, completed state and source.
- Site presentation tables have a site SELECT policy and no client write path; raw assessment envelopes remain private.
- A local writer with the service key inserts rows and refuses a write conflicting with a newer row.
- Trial metrics preserve known values versus explicit unknowns with reasons/sources; unknown is never zero ([S-002 contract](../../../LMK-004-rsi-loop-during-build/specs/S-002-rsi-loop/SPEC.md), [consumer rules](../../../../../evals/TRIAL-ROWS.md)).
- Seed rows come only from real sources (site build, later improvements, the skills repository's fixes), each labelled anecdote, single trial, repeated trials or held-out with interval; `recorded_fact` is for build history only.
- Test and synthetic rows are marked; the site never shows them.
- **Build history.** Rows for this build's Spec, Task, PR and commit events from real records, returns and corrections included, showing how the AMS built itself.

- Private assessment envelopes retain S-002 frozen packets, attempt/run IDs, findings/retests and recomputable results, separately from behavioral trial rows.

### Lifecycle records and recovery

Failures remain canonical in WORKBENCH_FEEDBACK.md. Worker ingestion references stable failure ID, source revision and correction lineage; duplicate ingestion is idempotent. Supabase is canonical for cases, runs, candidates, comparisons and dispositions, written through the authorized Python worker with commit-pinned provenance. Existing Git fixtures/contracts remain versioned artifacts referenced by those records, not independent live statuses.

Extend existing run/result/assessment identities to connect failure occurrence, case version, experiment contract, candidate/parent, execution job, outcome, decision, source merge and installation/use receipts. Preserve the existing assessment versus behavioral-evidence distinction. No table layout or queue technology is mandated by this destination.

Durable job state identifies authorization, owner/claim, attempt, next eligible action, stop/block reason and recoverable execution stage. Atomic claims and conflict refusal prevent two workers owning the same job. Interruptions, duplicate notifications and database outages preserve uncertain outcomes for reconciliation; no automatic replay of an already completed external effect.

Raw transcripts remain local/private; only safe derived fields and evidence identities enter Supabase. Public-safe data is separate from private operational state. Safe Git-committed exports carry source revision, schema, record identities and a completeness checkpoint; export is a recovery snapshot, not another writer. Restore preserves corrections, attempts and provenance and refuses stale conflicting state. Export excludes secrets, host paths, raw traces and private assessment contents.

Free-plan capacity and availability are constraints: the worker exposes storage/read failures and preserves pending evidence locally without reporting publication success. No paid hosting, upgrade, inference purchase or raw-evidence cloud upload is implied. Subscription availability and usage are distinct from optional estimated API-equivalent metrics.

## Decisions And Contracts

- The site only presents; it never writes.
- The service key stays out of Git and the site; writers read `SUPABASE_SERVICE_ROLE_KEY` from the gitignored env file.
- Never fabricate data; an empty table is valid.
- A completed result needs `passed` ([ADR-002J](../../../../docs/adr/002J-every-ledger-row-records-cost-and-run-state.md)); `score` is optional.

## Non-Goals

- Chart pages (S-007).
- Running trials (S-002).

## Dependencies And Blockers

- Supabase project `hqvtnpvwwppbeurponnn` ([ADR-003C](../../../../docs/adr/003C-the-supabase-project-and-its-read-only-baseline.md)); Python 3.14.5 with uv ([ADR-003D](../../../../docs/adr/003D-python-3-14-5-pinned-with-uv.md)).

## Vertical Implementation Slices

One run per Task in B's lane, by checked PR. Native Task records own slices; duplicate table rows are not permitted.

| Task | Slice | Status | Blockers | Proof |
|---|---|---|---|---|

## Acceptance Criteria

- [x] **Schema and provenance.** Every result row has the fields named above, enforced as non-null where required. *Check:* insert a row missing its skills commit. *Must fail:* the insert succeeds. [Proof][p].
- [x] **No client writes.** With the publishable key, insert, update and delete fail on every table; presentation-table SELECT works and private assessment SELECT is refused. *Check:* a test using the publishable key. *Must fail:* any client write accepted. [Proof][p].
- [x] **Writer works end to end.** The writer inserts a real build event and the site's key reads it back. *Must fail:* a row written only to a local file. [Proof][p].
- [x] **Conflict refusal.** A writer update against a row changed since it was read is refused. *Must fail:* a silent overwrite. [Proof][p].
- [x] **Real sources only.** Each seed row names its source and strength label. *Must fail:* a row with no source, or a sample value presented as real. [Proof][p].
- [x] **Key loads and authenticates.** A check reports only whether `SUPABASE_SERVICE_ROLE_KEY` loaded and whether Supabase accepted it, for `sb_secret_` and legacy keys. *Must fail:* any output, log or file containing the value. [Proof][p]; legacy JWT by fakes only (see limits).
- [ ] **Build history from real records.** Supabase holds build-history rows from this build's real Spec, Task, PR and commit records, each naming its source (path, PR number or commit SHA); returns and corrections are rows. Re-importing adds no duplicates. *Must fail:* a hand-typed row or a row with no source. [Proof][p].
- [x] **No secrets in Git.** The hygiene check finds no service key in the repository. *Must fail:* a committed key. [Proof][p].

[p]: tasks/TK-000B/TASK.md#proof

- [x] **Private assessment persistence.** Private remote append/readback retains the canonical assessment history with idempotence and conflict refusal; clients cannot read raw packets or write. *Must fail:* tampered totals, reset attempts, exposed private evidence or a silent overwrite.

- [ ] **Lifecycle lineage:** a safe readback follows a failure through case, candidate, comparison, disposition and actual later use. An orphan result or unpinned candidate fails.
- [ ] **Recovery:** concurrent claims, repeated intake, interrupted publication and duplicate delivery preserve one logical job and original attempts. An uncertain successful write replayed as a new result fails.
- [ ] **Safe export:** an exported checkpoint reconstructs eligible safe records without changing identities or exposing private data; incomplete exports and conflicting restores fail visibly.
- [ ] **Authority boundary:** presentation clients cannot write or read private operational evidence. Worker-only mutation does not give candidate agents database credentials or permission to change graders.

## RSI and website connection

S-002 writes its rows here; S-007 reads them.

## Testing Seams

- Branch database; writer insert interface; publishable-key queries.

## Verification Procedure

```bash
node workbench/tools/spec-workbench.mjs show S-006
uv run pytest
# before close, in B's checkout after merge
uv run ams-history import --refresh-changed
uv run ams-history readcheck --ref SHA --dev-ref origin/dev
```

## Documentation Impact

- RUNBOOK names the writer commands; ARCHITECTURE the data path.

## Review and Human QA

Presentation Human QA belongs to S-007. Completion requires actual candidate owner Human QA; engineering or independent source review does not supply it.

## Completion Result

Pending.

## Remaining Limitations Or Follow-Up Specs

- Region: nearest US default unless the owner chooses.
- Rows key on table index: a condensed row is re-dated; `import --refresh-changed` updates it, logged, old values in `detail.refreshed`.
- Legacy JWT: fakes only; the project has only an `sb_secret_` key.
- Baseline migration version: repo `20261101000000`, DB `20261101123819`; not renamed.

## Supersession

- Supersedes: the earlier draft's JSONL ledger files.
- Superseded by: none
