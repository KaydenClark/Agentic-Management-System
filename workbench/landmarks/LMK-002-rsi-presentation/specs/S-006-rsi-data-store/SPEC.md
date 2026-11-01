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
**Latest event:** TK-000E claimed by orchestrator-b-tk000e-implementor.
**Next gate:** Close TK-000E with verification and documentation proof.

## Intent and authority

The owner decided that Python pushes RSI results to Supabase as they arrive and the site reads from it; everything the site shows, build history included, lives there. Token counts go with the RSI data. Secrets live only in Vercel and Supabase settings.

## Outcome

One Supabase project holds every row the site presents; a local Python writer fills it; the site reads with the publishable key, never writes.

## Why It Matters

Charts are honest only if each number has a sourced row; local writes and public reads keep credentials off the site.

## Current Verified State

- Every public table has RLS on; the site key reads, its writes get 401.
- `build_events`: `ams-history import` derives rows from Git, `gh` and records on demand, not on a schedule; `readcheck` fails on any missing or extra row.
- `rsi_runs`, `rsi_results`: empty until a real trial; need the four commits and a trial strength; completed needs `passed`; stale updates 409 (`ams-rsi livecheck`).
- Writers and DB refuse rows without source or listed strength; test rows hidden (`ams-sources livecheck`). `tests/test_secret_scan.py` scans tracked files for keys.

## Desired Behavior

- Tables for RSI results, build history and run metadata. Each result names task, held-out or dev, arm (AMS, no-AMS or plain instructions), system version (runtime, controls and skills commits), provider, model, effort, pass, cost, tokens, completed state and source.
- Every table has a site SELECT policy and no client write path.
- A local writer with the service key inserts rows and refuses a write conflicting with a newer row.
- Seed rows come only from real sources (site build, later improvements, the skills repository's recorded fixes), each labelled anecdote, single trial, repeated trials or held-out with interval. `recorded_fact` is for build history only.
- Test and synthetic rows are marked; the site never shows them.
- **Build history.** Rows for this build's Spec, Task, PR and commit events from real records, returns and corrections included, showing how the AMS built itself.

## Decisions And Contracts

- The site only presents; it never writes.
- The service key never enters this repository or the site's environment; the writer reads `SUPABASE_SERVICE_ROLE_KEY` from the gitignored env file and accepts `sb_secret_` and legacy JWT keys.
- Never fabricate data. An empty table is a valid state.
- A completed result needs `passed` for pass rates ([ADR-002J](../../../../docs/adr/002J-every-ledger-row-records-cost-and-run-state.md)); `score` is optional.

## Non-Goals

- Chart pages (S-007).
- Running trials (S-002).

## Dependencies And Blockers

- Supabase project `hqvtnpvwwppbeurponnn` ([ADR-003C](../../../../docs/adr/003C-the-supabase-project-and-its-read-only-baseline.md)); Python 3.14.5 with uv ([ADR-003D](../../../../docs/adr/003D-python-3-14-5-pinned-with-uv.md)).

## Vertical Implementation Slices

One fresh run per Task in orchestrator B's lane (sole key holder), landed by checked PR to `main`. TK-001 to TK-005 done; TK-000E fixes review FAIL c87bf4e.

| Task | Slice | Status | Blockers | Proof |
|---|---|---|---|---|

## Acceptance Criteria

- [ ] **Schema and provenance.** Every result row has the fields named above, enforced as non-null where required. *Check:* insert a row missing its skills commit. *Must fail:* the insert succeeds.
- [ ] **No client writes.** With the publishable key, insert, update and delete fail on every table; select works. *Check:* a test using the publishable key. *Must fail:* any client write accepted.
- [ ] **Writer works end to end.** The writer inserts a real build event and the site's key reads it back. *Must fail:* a row written only to a local file.
- [ ] **Conflict refusal.** A writer update against a row changed since it was read is refused. *Must fail:* a silent overwrite.
- [ ] **Real sources only.** Each seed row names its source and strength label. *Must fail:* a row with no source, or a sample value presented as real.
- [ ] **Key loads and authenticates.** A check reports only whether `SUPABASE_SERVICE_ROLE_KEY` loaded and whether Supabase accepted it, for `sb_secret_` and legacy keys. *Must fail:* any output, log or file containing the value.
- [ ] **Build history from real records.** Supabase holds build-history rows from this build's real Spec, Task, PR and commit records, each naming its source (path, PR number or commit SHA); returns and corrections are rows. Re-importing adds no duplicates. *Must fail:* a hand-typed row or a row with no source.
- [ ] **No secrets in Git.** The hygiene check finds no service key in the repository. *Must fail:* a committed key.

## RSI and website connection

S-002 writes its rows here; S-007 reads them.

## Testing Seams

- Migrations on a branch database; the writer's insert interface; publishable-key queries.

## Verification Procedure

```bash
node workbench/tools/spec-workbench.mjs show S-006
uv run pytest
```

Before close, after merge, in orchestrator B's checkout: `uv run ams-history import`, then `readcheck` (missing 0, extra 0).

## Documentation Impact

- RUNBOOK names the writer commands; ARCHITECTURE the data path.

## Append-Only Evidence And Execution Log

One row per closed Task; each TASK.md Receipt holds the full proof.

| Date | Task | Event | Verification | Docs | Remaining gap |
|---|---|---|---|---|---|
| 2026-11-01 | none | Mapped as planned; baseline migration noted | render, doctor | this Spec | Every criterion |
| 2026-11-01 | TK-001 | Task closed | PR #15 (884d021): live `ams-keycheck` authenticated, no key printed | RUNBOOK, ARCHITECTURE | Legacy-JWT path proven only with fakes |
| 2026-11-01 | TK-002 | Task closed | PR #18 (d279ae1): `build_events` applied; `ams-writer` wrote PR #15's row; site key reads, writes 401 | RUNBOOK, ARCHITECTURE | `is_test` filter proven by stubs |
| 2026-11-01 | TK-003 | Task closed | PR #29 (74b446e): `rsi_*` applied; `ams-rsi livecheck` refused a missing skills commit and a stale update | RUNBOOK, ARCHITECTURE | No real RSI row until S-002 |
| 2026-11-01 | TK-004 | Task closed | PRs #31 (4d74e90), #37 (d26bb8c): `ams-history` imported 463 rows matching record counts; rerun added 0 | RUNBOOK, ARCHITECTURE | Dev-only records not imported; no scheduled re-import |
| 2026-11-01 | TK-005 | Task closed | PR #42 (55c3856): live `ams-sources livecheck`: writer and DB refused no source, blank ref, bad strength on all 3 tables; site key saw 0 test rows | RUNBOOK, ARCHITECTURE, Spec | S-002 picks seed rows |
| 2026-11-01 | TK-000E | Review FAIL at c87bf4e: H1, M1-M3, L1, L2 | Spec review | this Spec | TK-000E |

## Review and Human QA

Spec review only; presentation gets Human QA in S-007.

## Completion Result

Pending.

## Remaining Limitations Or Follow-Up Specs

- Supabase region: nearest US default unless the owner chooses.
- Evidence and Receipt rows are keyed by index: an edited row keeps its imported text; a removed one reads as extra.

## Supersession

- Supersedes: the earlier draft's JSONL ledger files.
- Superseded by: none
