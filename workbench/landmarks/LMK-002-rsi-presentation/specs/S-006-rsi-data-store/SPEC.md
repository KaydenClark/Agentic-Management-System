# S-006 - RSI data store

**Spec ID:** S-006
**Status:** active
**Priority:** 1
**Owner:** Kayden; orchestrator B (local, holds the Supabase keys)
**Stance:** Builder
**Updated:** 2026-11-01
**Catalog description:** Supabase schema and local Python writer for RSI results, build history, cost and tokens; the site reads under RLS.
**Blockers:** none
**Confirmation:** [JOT-a85076a7-25a3-45bd-bd33-220c62d87882](../../../../wiki/context-active-spec-approvals.md)
**Execution approval:** [JOT-a85076a7-25a3-45bd-bd33-220c62d87882](../../../../wiki/context-active-spec-approvals.md)
**Latest event:** TK-000R claimed by codex-assessment-writer.
**Next gate:** Close TK-000R with verification and documentation proof.

## Intent and authority

The owner decided that Python pushes RSI results to Supabase as they arrive and the site reads from it; everything the site shows, build history included, lives there. Token counts go with the RSI data. The service key stays in the gitignored local environment; the site receives only its publishable key (owner coherence correction).

## Outcome

One Supabase project holds every row the site presents; a local Python writer fills it; the site reads with the publishable key, never writes.

## Why It Matters

Charts are honest only if each number has a sourced row; local writes keep credentials off the site.

## Current Verified State

- Verified candidate: `5aa2621ec03a1d419615374ec31e4c3db12069b6`, dev `c0f6c67687f432cd75b55e7d4fdad460ea2f77db`; 943 history rows, missing/extra/content mismatches/unsourced all 0. [TK-000L](tasks/TK-000L/TASK.md#resumed-local-verification-2026-11-01) owns live proof and limits. No real trial or assessment storage completion claimed.
- TK-000P adds explicit unknown metrics with reasons/sources and preserves known zero; remote migration `20261101192328` and live tagged roundtrip pass. See [trial consumer contract](../../../../../evals/TRIAL-ROWS.md). TK-000R corrects the failed TK-000Q numeric roundtrip: source `d98a770`, additive migration `20261101195609`, exact TEXT artifacts/hash and JSONB projection checks. Full local/fresh495 passed/4 skipped,62 focused, source CI53 pass; tagged numeric/retry/client-denial probes cleanup0. Earlier FAIL remains recorded; checked delivery/whole Review/owner QA remain separate.

## Desired Behavior

- Tables for RSI results, build history and run metadata. Each result names task, held-out or dev, arm (AMS, no-AMS or plain instructions), system version (runtime, controls and skills commits), provider, model, effort, pass, cost, tokens, completed state and source.
- Site presentation tables have a site SELECT policy and no client write path; raw assessment envelopes remain private.
- A local writer with the service key inserts rows and refuses a write conflicting with a newer row.
- Trial metrics preserve known values versus explicit unknowns with reasons/sources; unknown is never zero ([S-002 contract](../../../LMK-004-rsi-loop-during-build/specs/S-002-rsi-loop/SPEC.md), [consumer rules](../../../../../evals/TRIAL-ROWS.md)).
- Seed rows come only from real sources (site build, later improvements, the skills repository's fixes), each labelled anecdote, single trial, repeated trials or held-out with interval; `recorded_fact` is for build history only.
- Test and synthetic rows are marked; the site never shows them.
- **Build history.** Rows for this build's Spec, Task, PR and commit events from real records, returns and corrections included, showing how the AMS built itself.

- Private assessment envelopes retain S-002 frozen packets, attempt/run IDs, findings/retests and recomputable results, separately from behavioral trial rows.

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

One run per Task in B's lane, by checked PR. Tasks are records under `tasks/` (the tool refuses table rows beside them): TK-001 to TK-005, TK-000B to TK-000E done; TK-000L closed with live verification. Native Task records own slices; duplicate table rows are not permitted.

| Task | Slice | Status | Blockers | Proof |
|---|---|---|---|---|

## Acceptance Criteria

- [x] **Schema and provenance.** Every result row has the fields named above, enforced as non-null where required. *Check:* insert a row missing its skills commit. *Must fail:* the insert succeeds. [Proof][p].
- [x] **No client writes.** With the publishable key, insert, update and delete fail on every table; presentation-table SELECT works and private assessment SELECT is refused. *Check:* a test using the publishable key. *Must fail:* any client write accepted. [Proof][p].
- [x] **Writer works end to end.** The writer inserts a real build event and the site's key reads it back. *Must fail:* a row written only to a local file. [Proof][p].
- [x] **Conflict refusal.** A writer update against a row changed since it was read is refused. *Must fail:* a silent overwrite. [Proof][p].
- [x] **Real sources only.** Each seed row names its source and strength label. *Must fail:* a row with no source, or a sample value presented as real. [Proof][p].
- [x] **Key loads and authenticates.** A check reports only whether `SUPABASE_SERVICE_ROLE_KEY` loaded and whether Supabase accepted it, for `sb_secret_` and legacy keys. *Must fail:* any output, log or file containing the value. [Proof][p]; legacy JWT by fakes only (see limits).
- [x] **Build history from real records.** Supabase holds build-history rows from this build's real Spec, Task, PR and commit records, each naming its source (path, PR number or commit SHA); returns and corrections are rows. Re-importing adds no duplicates. *Must fail:* a hand-typed row or a row with no source. [Proof][p].
- [x] **No secrets in Git.** The hygiene check finds no service key in the repository. *Must fail:* a committed key. [Proof][p].

[p]: tasks/TK-000B/TASK.md#proof

- [x] **Private assessment persistence.** Private remote append/readback retains the canonical assessment history with idempotence and conflict refusal; clients cannot read raw packets or write. *Must fail:* tampered totals, reset attempts, exposed private evidence or a silent overwrite.

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

## Append-Only Evidence And Execution Log

TASK.md Receipts hold full proof.

| Date | Task | Event | Verification | Docs | Remaining gap |
|---|---|---|---|---|---|
| 2026-11-01 | none | Mapped as planned; baseline migration noted | render, doctor | this Spec | Every criterion |
| 2026-11-01 | TK-001 | Task closed | PR #15 (884d021) | RUNBOOK, ARCH | Legacy JWT: fakes only |
| 2026-11-01 | TK-002 | Task closed | PR #18 (d279ae1) | RUNBOOK, ARCH | none |
| 2026-11-01 | TK-003 | Task closed | PR #29 (74b446e) | RUNBOOK, ARCH | No RSI row until S-002 |
| 2026-11-01 | TK-004 | Task closed | PRs #31 (4d74e90), #37 (d26bb8c) | RUNBOOK, ARCH | Dev-only records not imported |
| 2026-11-01 | TK-005 | Task closed | PR #42 (55c3856) | RUNBOOK, ARCHITECTURE, Spec | S-002 picks seed rows |
| 2026-11-01 | review | Review verdict: fail at c87bf4ec86206bd5f734af7b828c81c3d3356a00 [a2124994b4d9] #1 | new Tasks TK-000B, TK-000C, TK-000D | C, repo half | 3 |
| 2026-11-01 | TK-000E | B review FAIL c87bf4e: H1, M1-M3, L1, L2 | live half | Spec | TK-000E |
| 2026-11-01 | TK-000E | Task closed | PR #49 (a03d739): readcheck missing 0, extra 0; livechecks pass | Spec, RUNBOOK | Fresh review |
| 2026-11-01 | TK-000C | Task closed | TK-000E, a4470a4: tests/test_secret_scan.py scans tree and history | Spec | none |
| 2026-11-01 | TK-000D | Task closed | TK-000E, a4470a4: test_recorded_fact_is_for_build_history_only; DB check 20261101144510 | Spec | none |
| 2026-11-01 | TK-000B | Task closed | 8 lines checked, proof in TK-000B at a4470a4 | Spec | Fresh review |
| 2026-11-01 | review | Review verdict: pass at d6d4a6d65cc6287b667fe78ee5db937440972a5e [213a7241e512] #2 | none | C, repo half | none |
| 2026-11-01 | TK-000L | B review FAIL d6d4a6d: N1-N6, legacy key | live half | Spec | TK-000L |
| 2026-11-01 | TK-000L | Task closed | 5aa2621/dev c0f6c67: history 943 rows; missing/extra/mismatch/unsourced 0; live summary edit detected/restored; key/writer/RSI/source checks pass; pytest 433 passed,4 skipped; layout valid; doctor no blocking finding | S-006 SPEC and TK-000L pinned live verification | Fresh independent assembled Review; S-002 assessment persistence and unknown metrics compatibility; close attribution: {"agent":"codex-local-writer","claimant":"orch-b","onBehalfOf":"orch-b"} |
| 2026-11-01 | TK-000P | Task closed | 475 passed,4 skipped; focused99/1; migration20261101192328; live null and zero roundtrip; DB bad availability23514; client writes401/test hiding; cleanup0; advisors empty | TRIAL-ROWS; template; rsi_rows; S-006 SPEC/TK-000P | Fresh assembled Review; private assessment storage; real qualified S-002 trials; close attribution: {"agent":"codex-local-writer","claimant":"codex-local-writer","onBehalfOf":null} |
| 2026-11-01 | TK-000Q | Task closed | 56 focused; fresh source489 passed,4 skipped; private migration20261101193603; live duplicate200/conflict409/concurrent200-409/client401/update403/cleanup0; source CI45 pass | ASSESSMENTS; RUNBOOK; ARCHITECTURE; S-006 SPEC/TK-000Q | Final CI/checked merge; fresh assembled Review; native owner QA; safe S007 presentation and real S002 trials; close attribution: {"agent":"codex-assessment-writer","claimant":"codex-assessment-writer","onBehalfOf":null} |
| 2026-11-01 | review | Review verdict: fail at 977ac08fed4a269182b67d6ada990042e2ceee88 [cfc6d944ca57] #3 | new Task: P1 JSONB numeric normalization changes valid packet digest after append and blocks immutable namespace readback. Preserve exact canonical text and verify projection before rereview. | s006_review, independent Codex context | 1 |

## Review and Human QA

Spec review only; presentation gets Human QA in S-007.

## Completion Result

Implementation delivered: schema/local writers, real build history, explicit
unknown trial metrics and private assessment append/replay. TK-000L/P/Q/R retain
candidate-specific live checks and test evidence. Private packets remain
inaccessible to site clients; no trial result or evaluator qualification is
inferred. Checked PR delivery, independent assembled Review and the native
owner-QA completion gate remain distinct and pending; the Spec is not accepted.

## Remaining Limitations Or Follow-Up Specs

- Region: nearest US default unless the owner chooses.
- Rows key on table index: a condensed row is re-dated; `import --refresh-changed` updates it, logged, old values in `detail.refreshed`.
- Legacy JWT: fakes only; the project has only an `sb_secret_` key.
- Baseline migration version: repo `20261101000000`, DB `20261101123819`; not renamed.

## Supersession

- Supersedes: the earlier draft's JSONL ledger files.
- Superseded by: none
