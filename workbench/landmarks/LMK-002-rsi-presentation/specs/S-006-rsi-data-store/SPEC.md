# S-006 - RSI data store

**Spec ID:** S-006
**Status:** active
**Priority:** 1
**Owner:** Kayden; orchestrator B (local, holds the Supabase keys)
**Stance:** Builder
**Updated:** 2026-11-07
**Catalog description:** Supabase RSI/build/usage history, Python writer and RLS site reads.
**Blockers:** none
**Confirmation:** [JOT-a85076a7-25a3-45bd-bd33-220c62d87882](../../../../wiki/context-active-spec-approvals.md)
**Execution approval:** [JOT-a85076a7-25a3-45bd-bd33-220c62d87882](../../../../wiki/context-active-spec-approvals.md)
**Next gate:** Coverage, whole-Spec Review and owner QA remain open. TK-000W stays stopped.

## Intent and authority

[RSI Map source](../../../../wiki/context-feedback-improvement-loop-plan.md#jot-7862917b-48cb-41bc-8f21-0ddfc611cdac). Separate Nov. 5 launch authorized isolated N, then O. Prior stops remain.

Python writes RSI/build/usage data to Supabase; the site reads only. Service credentials stay gitignored/local; the site gets the publishable key.

## Outcome

One Supabase project supplies site rows. Python writes and the site reads.

## Why It Matters

Sourced rows make charts auditable; private writes protect keys.

## Current Verified State

[TK-000B proof](tasks/TK-000B/TASK.md#proof) covers schema, writer, conflicts, sources and keys within [live limits](tasks/TK-000L/TASK.md#resumed-local-verification-2026-11-01). TK-000Q/R/S/P cover private assessments and unknown metrics.

Import `771bd1e` passed. Later coverage needs fresh import approval. Preserve S-008 provenance and the TK-000W stop. See [history](../../../../wiki/history/S-006.md).

## Desired Behavior

- Supabase owns shared failure/improvement history and worker records. Git owns skills, tests, fixtures and contracts. Markdown is local intake/recovery. Transport preserves stable IDs, revisions and corrections.
- Link chat, request, loading, use and failure identities; distinguish recurrence occurrences, skill/candidate/parent pins, jobs, cases, contracts, decisions and adoption/later-use receipts. Skipped explicit requests remain failed requested uses. Replayed transport creates no duplicate occurrence; extend existing identities, not another ledger.
- Retain task/split/control arm, runtime/control/skill commits, provider/model/effort, completion, source, grade and three actual audit run identities/class counts/Critical results. Partial sets remain partial. Assessments and behavioral trials stay distinct; new grading cannot relabel historical r1 results or erase attempts.
- Persist authorization, claim, attempt, stage, next action and stop/block reason. Atomic ownership/version checks prevent duplicate jobs; reconcile interrupted/uncertain effects before replay. S-000B owns execution; table/queue choice remains implementation detail.
- Only trusted workers write. Presentation clients are read-only; candidates receive no credentials and cannot change graders. Private assessments/operations and raw transcripts remain private/local; public projections contain safe derived fields and evidence identities only.
- Safe Git exports retain schema/completeness checkpoints for recovery. Restore preserves IDs, attempts and corrections and refuses stale conflicts. Exports are not writable authorities; exclude secrets, host paths and raw/private packets.
- Separate measured usage, subscription capacity and optional API estimates. Keep unknowns and pending local evidence visible through outages. Paid upgrades and raw uploads require separate authority.
- Build events come from real Spec/Task/PR/commit history, including returns/corrections. Seeds carry source/strength; synthetic/test rows never reach the site.

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

[TK-002N/O contract](../../../../wiki/guidebooks/rsi-worker-contract.md). Isolated [lineage](tasks/TK-002N/TASK.md#proof) and [recovery](tasks/TK-002O/TASK.md#proof) passed at `3856614`. Production migration remains open.

## Acceptance Criteria

- [ ] **Shared history:** replay one event twice and retain one occurrence; a genuine later recurrence retains a second linked occurrence. Skipped requested use stays in failed-request counts. Git test/source pins and Supabase history resolve to the same candidate.
- [ ] **Versioned audits:** store partial and complete audit sets truthfully, preserve actual counts and class denominators, and retain historical r1 grade semantics. A new label silently rewriting old results fails.

- [x] **Schema/provenance:** required identities are enforced; a missing skills commit fails. [Proof][p].
- [x] **No client writes:** publishable-key mutations fail, safe SELECT works, raw assessment reads fail. [Proof][p].
- [x] **Writer end to end:** real build event is inserted and read back; local-only evidence fails. [Proof][p].
- [x] **Conflict refusal:** stale updates cannot silently overwrite. [Proof][p].
- [x] **Real sources:** seeds have source and strength, never fabricated values. [Proof][p].
- [x] **Key handling:** secret and legacy key loading/authentication reveal no key; legacy verified by fakes only. [Proof][p].
- [x] **No secrets in Git:** hygiene passes. [Proof][p].
- [x] **Private assessments:** immutable append/readback preserves assessment identity and attempts; tampering, exposure and silent overwrite fail.
- [ ] **Build history coverage:** real sourced events, returns and corrections are imported without duplicates; coverage after the pinned import remains unverified.
- [ ] **Lifecycle lineage:** readback traces failure to case/candidate/comparison/disposition/later use; orphan or unpinned records fail.
- [ ] **Recovery:** concurrent claims, duplicate intake and interrupted publication preserve one logical job and original attempts; uncertain writes cannot become new trials.
- [ ] **Safe export:** a complete checkpoint reconstructs safe records without changing identities; partial exports, stale conflicting restores and private-data exposure fail.
- [ ] **Worker boundary:** presentation access cannot mutate state, expose private operations or authorize candidate changes to graders.

[p]: tasks/TK-000B/TASK.md#proof

## RSI and website connection

S-002 writes its rows here; S-007 reads them.

## Testing Seams

- Branch database; writer insert interface; publishable-key queries.

## Verification Procedure

RUNBOOK checks and S-006 writer/history readback on the named candidate. Imports require the separately approved scope; Map writes no database rows.

## Documentation Impact

- RUNBOOK names the writer commands; ARCHITECTURE the data path.

## Review and Human QA

S-007 owns presentation Human QA; Spec completion needs actual owner QA, not engineering/source review.

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
