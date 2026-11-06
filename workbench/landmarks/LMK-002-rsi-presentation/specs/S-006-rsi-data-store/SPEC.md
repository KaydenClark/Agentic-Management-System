# S-006 - RSI data store

**Spec ID:** S-006
**Status:** active
**Priority:** 1
**Owner:** Kayden; orchestrator B (local, holds the Supabase keys)
**Stance:** Builder
**Updated:** 2026-11-06
**Catalog description:** Supabase schema and local Python writer for RSI results, build history, cost and tokens; the site reads under RLS.
**Blockers:** none
**Confirmation:** [JOT-a85076a7-25a3-45bd-bd33-220c62d87882](../../../../wiki/context-active-spec-approvals.md)
**Execution approval:** [JOT-a85076a7-25a3-45bd-bd33-220c62d87882](../../../../wiki/context-active-spec-approvals.md)
**Next gate:** Close TK-002N with verification and documentation proof.

## Intent and authority

The [Stage A owner intent](../../../../wiki/context-feedback-improvement-loop-plan.md#jot-55876e5d-6957-4a4e-917b-8ba7245adee2) authorized preparation only. On 2026-11-05 the owner explicitly launched TK-002N/TK-002O implementation, starting with an isolated test namespace, and confirmed the execution readback. This releases only their implementation hold; O still requires verified N. Model campaigns, installation, stopped campaigns and production promotion retain their separate gates.

The owner decided that Python pushes RSI results to Supabase as they arrive and the site reads from it; everything the site shows, build history included, lives there. Token counts go with the RSI data. The service key stays in the gitignored local environment; the site receives only its publishable key.

## Outcome

One Supabase project holds every row the site presents; a local Python writer fills it; the site reads with the publishable key, never writes.

## Why It Matters

Sourced rows make charts auditable; private writes protect credentials.

## Current Verified State

Schema/provenance, writer/readback, conflict refusal, sources and key handling are met ([TK-000B](tasks/TK-000B/TASK.md#proof), [live limits](tasks/TK-000L/TASK.md#resumed-local-verification-2026-11-01)). Private assessments and explicit unknown metrics are met (TK-000Q/R/S and TK-000P).

Build history is incomplete: the approved pinned import at 771bd1e passed, but later coverage is unverified. Further import requires fresh approval and cannot rewrite S-008 creation provenance with --refresh-changed. TK-000W remains stopped/unaccepted; whole-Spec binding and actual Human QA are open. See [history](../../../../wiki/history/S-006.md).

## Desired Behavior

- Existing RSI result/run tables retain task, split, control arm, runtime/controls/skills commits, provider/model/effort, completion, grade and source. Assessments remain separate from behavioral trials.
- Presentation data is read-only to clients; private assessments and operational state are not publicly readable. Only the authorized worker writes lifecycle records; candidate agents receive no database credentials.
- Supabase owns worker-written, commit-pinned cases, runs, candidates, comparisons and dispositions. Git fixtures/contracts are referenced artifacts, not competing live statuses. Markdown owns failure intake; ingestion references stable ID, source revision and corrections, without duplicate occurrences.
- Link failures, case versions, experiment contracts, candidate parents, jobs, results, decisions and adoption/use receipts. Extend existing identities rather than creating a second ledger. Table/queue technology is left to implementation.
- Persist job authorization, claim, attempt, stage, next action and stop/block reason. Atomic claims and version conflicts prevent duplicate ownership; interrupted or uncertain writes reconcile before replay. S-000B owns execution semantics.
- Keep raw transcripts local/private. Store only safe derived fields and evidence identities. Git-committed exports preserve safe records, schema and completeness checkpoints; restore preserves attempts/corrections and refuses stale conflicts. Exports are recovery copies, not writable authorities; exclude secrets, host paths and private raw packets.
- Distinguish measured usage, subscription-meter availability and optional API-equivalent estimates; unknown is never zero or an invented bill. Free-plan outages/capacity failures remain visible; retain pending local evidence without claiming publication. No paid upgrade or cloud upload of raw evidence is implied.
- Build history comes from real Spec/Task/PR/commit events, including returns and corrections. Seeds carry source and strength; synthetic/test rows never reach the site.

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

[TK-002N/O contract](../../../../wiki/guidebooks/rsi-worker-contract.md); N released for isolated lineage implementation, O waits for verified N.

| Task | Slice | Status | Blockers | Proof |
|---|---|---|---|---|

## Acceptance Criteria

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
