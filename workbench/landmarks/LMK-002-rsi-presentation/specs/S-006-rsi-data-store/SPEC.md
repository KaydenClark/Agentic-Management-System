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
**Latest event:** TK-000B closed with proof.
**Next gate:** Confirm acceptance criteria and completion result.

## Intent and authority

The owner decided that Python pushes RSI results to Supabase as they arrive and the site reads from it; everything the site shows, build history included, lives there. Token counts go with the RSI data. Secrets live only in Vercel and Supabase settings.

## Outcome

One Supabase project holds every row the site presents; a local Python writer fills it; the site reads with the publishable key, never writes.

## Why It Matters

Charts are honest only if each number has a sourced row; local writes and public reads keep credentials off the site.

## Current Verified State

- Each acceptance line links its proof at `a4470a4`. `rsi_*` stay empty until a real trial; `ams-history import` runs on demand, not on a schedule.

## Desired Behavior

- Tables for RSI results, build history and run metadata. Each result names task, held-out or dev, arm (AMS, no-AMS or plain instructions), system version (runtime, controls and skills commits), provider, model, effort, pass, cost, tokens, completed state and source.
- Each table has a site SELECT policy, no client write path.
- A local writer with the service key inserts rows, refusing a write that conflicts with a newer row.
- Seed rows come only from real sources (site build, later improvements, the skills repository's fixes), each labelled anecdote, single trial, repeated trials or held-out with interval; `recorded_fact` is for build history only.
- Test and synthetic rows are marked; the site never shows them.
- **Build history.** Rows for this build's Spec, Task, PR and commit events from real records, returns and corrections included, showing how the AMS built itself.

## Decisions And Contracts

- The site only presents; it never writes.
- The service key stays out of the repository and the site; the writer reads `SUPABASE_SERVICE_ROLE_KEY` from the gitignored env file.
- Never fabricate data; an empty table is valid.
- A completed result needs `passed` ([ADR-002J](../../../../docs/adr/002J-every-ledger-row-records-cost-and-run-state.md)); `score` is optional.

## Non-Goals

- Chart pages (S-007).
- Running trials (S-002).

## Dependencies And Blockers

- Supabase project `hqvtnpvwwppbeurponnn` ([ADR-003C](../../../../docs/adr/003C-the-supabase-project-and-its-read-only-baseline.md)); Python 3.14.5 with uv ([ADR-003D](../../../../docs/adr/003D-python-3-14-5-pinned-with-uv.md)).

## Vertical Implementation Slices

One run per Task in B's lane (sole key holder), by checked PR to `main`.

| Task | Slice | Status | Blockers | Proof |
|---|---|---|---|---|

## Acceptance Criteria

- [x] **Schema and provenance.** Every result row has the fields named above, enforced as non-null where required. *Check:* insert a row missing its skills commit. *Must fail:* the insert succeeds. [Proof](tasks/TK-000B/TASK.md#proof).
- [x] **No client writes.** With the publishable key, insert, update and delete fail on every table; select works. *Check:* a test using the publishable key. *Must fail:* any client write accepted. [Proof](tasks/TK-000B/TASK.md#proof).
- [x] **Writer works end to end.** The writer inserts a real build event and the site's key reads it back. *Must fail:* a row written only to a local file. [Proof](tasks/TK-000B/TASK.md#proof).
- [x] **Conflict refusal.** A writer update against a row changed since it was read is refused. *Must fail:* a silent overwrite. [Proof](tasks/TK-000B/TASK.md#proof).
- [x] **Real sources only.** Each seed row names its source and strength label. *Must fail:* a row with no source, or a sample value presented as real. [Proof](tasks/TK-000B/TASK.md#proof).
- [x] **Key loads and authenticates.** A check reports only whether `SUPABASE_SERVICE_ROLE_KEY` loaded and whether Supabase accepted it, for `sb_secret_` and legacy keys. *Must fail:* any output, log or file containing the value. [Proof](tasks/TK-000B/TASK.md#proof).
- [x] **Build history from real records.** Supabase holds build-history rows from this build's real Spec, Task, PR and commit records, each naming its source (path, PR number or commit SHA); returns and corrections are rows. Re-importing adds no duplicates. *Must fail:* a hand-typed row or a row with no source. [Proof](tasks/TK-000B/TASK.md#proof).
- [x] **No secrets in Git.** The hygiene check finds no service key in the repository. *Must fail:* a committed key. [Proof](tasks/TK-000B/TASK.md#proof).

## RSI and website connection

S-002 writes its rows here; S-007 reads them.

## Testing Seams

- Migrations on a branch database; the writer's insert interface; publishable-key queries.

## Verification Procedure

```bash
node workbench/tools/spec-workbench.mjs show S-006
uv run pytest
# before close, in B's checkout after merge
uv run ams-history import && uv run ams-history readcheck
```

## Documentation Impact

- RUNBOOK names the writer commands; ARCHITECTURE the data path.

## Append-Only Evidence And Execution Log

TASK.md Receipts hold full proof.

| Date | Task | Event | Verification | Docs | Remaining gap |
|---|---|---|---|---|---|
| 2026-11-01 | none | Mapped as planned; baseline migration noted | render, doctor | this Spec | Every criterion |
| 2026-11-01 | TK-001 | Task closed | PR #15 (884d021) | RUNBOOK, ARCHITECTURE | Legacy JWT: fakes only |
| 2026-11-01 | TK-002 | Task closed | PR #18 (d279ae1) | RUNBOOK, ARCHITECTURE | none |
| 2026-11-01 | TK-003 | Task closed | PR #29 (74b446e) | RUNBOOK, ARCHITECTURE | No RSI row until S-002 |
| 2026-11-01 | TK-004 | Task closed | PRs #31 (4d74e90), #37 (d26bb8c) | RUNBOOK, ARCHITECTURE | Dev-only records not imported |
| 2026-11-01 | TK-005 | Task closed | PR #42 (55c3856) | RUNBOOK, ARCHITECTURE, Spec | S-002 picks seed rows |
| 2026-11-01 | review | Review verdict: fail at c87bf4ec86206bd5f734af7b828c81c3d3356a00 [a2124994b4d9] #1 | new Tasks TK-000B, TK-000C, TK-000D | C, repo half | 3 |
| 2026-11-01 | TK-000E | B review FAIL c87bf4e: H1, M1-M3, L1, L2 | live half | Spec | TK-000E |
| 2026-11-01 | TK-000E | Task closed | PR #49 (a03d739): readcheck missing 0, extra 0; livechecks pass | Spec, RUNBOOK | Fresh review; close attribution: {"agent":"orchestrator-b-tk000e-implementor","claimant":"orchestrator-b-tk000e-implementor","onBehalfOf":null} |
| 2026-11-01 | TK-000C | Task closed | TK-000E, a4470a4: tests/test_secret_scan.py scans tree and history | Spec | none; close attribution: {"agent":"orch-b","claimant":"orch-b","onBehalfOf":null} |
| 2026-11-01 | TK-000D | Task closed | TK-000E, a4470a4: test_recorded_fact_is_for_build_history_only; DB check 20261101144510 | Spec | none; close attribution: {"agent":"orch-b","claimant":"orch-b","onBehalfOf":null} |
| 2026-11-01 | TK-000B | Task closed | 8 lines checked, proof in TK-000B at a4470a4 | Spec | Fresh review; close attribution: {"agent":"orch-b","claimant":"orch-b","onBehalfOf":null} |
| 2026-11-01 | review | Review verdict: pass at d6d4a6d65cc6287b667fe78ee5db937440972a5e [213a7241e512] #2 | none | Orchestrator C, Claude cloud session, separate from B's build lanes: repo-only half. Live-database half is B's local reviewer's. | none |

## Review and Human QA

Spec review only; presentation gets Human QA in S-007.

## Completion Result

Pending.

## Remaining Limitations Or Follow-Up Specs

- Region: nearest US default unless the owner chooses.
- Evidence and Receipt rows are keyed by index: edits are not re-imported; a removed row reads as extra.

## Supersession

- Supersedes: the earlier draft's JSONL ledger files.
- Superseded by: none
