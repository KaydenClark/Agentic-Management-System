# S-006 - RSI data store

**Spec ID:** S-006
**Status:** active
**Priority:** 1
**Owner:** Kayden; orchestrator B (local, holds the Supabase keys)
**Stance:** Builder
**Updated:** 2026-11-01
**Catalog description:** The Supabase schema and the local Python writer that push RSI results, build history, cost and tokens, read by the site under row-level security.
**Blockers:** none
**Confirmation:** [JOT-a85076a7-25a3-45bd-bd33-220c62d87882](../../../../wiki/context-active-spec-approvals.md)
**Execution approval:** [JOT-a85076a7-25a3-45bd-bd33-220c62d87882](../../../../wiki/context-active-spec-approvals.md)
**Latest event:** TK-004 closed with proof.
**Next gate:** Complete TK-005.

## Intent and authority

The owner decided that Python pushes RSI results to Supabase as they arrive and the site reads from it; everything the site shows, build history included, lives there. Token counts go with the RSI data. Secrets live only in Vercel and Supabase settings.

## Outcome

One Supabase project holds every row the site presents; a local Python writer keeps it current; the site reads with the publishable key and cannot write.

## Why It Matters

Charts are honest only if each number has a row with provenance; local writes and public reads keep credentials off the site.

## Current Verified State

- `supabase/migrations/`: read-only baseline; new public tables start with RLS on, no client write.
- `build_events` (`20261101132456`): 463 rows `ams-history` imported from Git, `gh` and the records, incl. ams-writer's PR #15 row; the site key reads them, its writes get 401.
- `rsi_runs`, `rsi_results` (`20261101134221`): empty, since no real trial has run. Each requires skills, runtime, controls and grader commits; a version trigger refuses stale updates (409). `ams-rsi livecheck` proves both refusals with hidden test rows, then deletes them.

## Desired Behavior

- Tables for RSI trial results, build history and run metadata. Each result row names: task, held-out or dev, trial arm (AMS, no-AMS or plain instructions), system version (runtime, controls and skills commits), provider, model, effort, pass, cost, tokens, completed state and source.
- Every table has a SELECT policy for the site and no client write path.
- A local Python writer with the service key inserts rows and refuses a write that conflicts with a newer row.
- Seed rows come only from real sources (the site build, later improvements, the skills repository's recorded fixes), each with a strength label (anecdote, single trial, repeated trials, held-out with interval).
- Test and synthetic rows are marked; the site never shows them.
- **Build history.** Rows for this build's Spec, Task, PR and commit events from the real records, returns and corrections included, showing how the AMS built itself.

## Decisions And Contracts

- The site only presents; it never writes.
- The service key never enters this repository or the site's environment. The writer reads `SUPABASE_SERVICE_ROLE_KEY` from its process environment, loaded from the gitignored env file, and accepts `sb_secret_` and legacy JWT keys.
- Never fabricate data. An empty table is a valid state.

## Non-Goals

- Chart pages (S-007).
- Running trials (S-002).

## Dependencies And Blockers

- Supabase project `hqvtnpvwwppbeurponnn` ([ADR-003C](../../../../docs/adr/003C-the-supabase-project-and-its-read-only-baseline.md)); Python 3.14.5 with uv ([ADR-003D](../../../../docs/adr/003D-python-3-14-5-pinned-with-uv.md)).

## Vertical Implementation Slices

Each Task is one fresh-session run in orchestrator B's lane (the only service-key holder), landed feature -> `main` by checked PR. TK-001 to TK-004 are done; TK-005 (seed and test rows) remains.

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

- Migrations on a local or branch database; the writer's insert interface; publishable-key queries.

## Verification Procedure

```bash
node workbench/tools/spec-workbench.mjs show S-006
# migration and Python test commands named at Task planning
```

## Documentation Impact

- RUNBOOK names the writer commands; ARCHITECTURE the data path.

## Append-Only Evidence And Execution Log

Condensed 2026-11-01 to one row per closed Task; the full proof lives in each TASK.md Receipt and in Git history.

| Date | Task | Event | Verification | Docs | Remaining gap |
|---|---|---|---|---|---|
| 2026-11-01 | none | Mapped as planned; baseline migration noted | render, doctor | this Spec | Every criterion |
| 2026-11-01 | TK-001 | Task closed | PR [#15](https://github.com/KaydenClark/Agentic-Management-System/pull/15) merged as 884d021; receipt [c1f4182](https://github.com/KaydenClark/Agentic-Management-System/commit/c1f4182): live `ams-keycheck` authenticated, no key printed | RUNBOOK, ARCHITECTURE | Legacy-JWT path proven only with fakes |
| 2026-11-01 | TK-002 | Task closed | PR [#18](https://github.com/KaydenClark/Agentic-Management-System/pull/18) merged as d279ae1; receipt [0371288](https://github.com/KaydenClark/Agentic-Management-System/commit/0371288): `build_events` applied; `ams-writer` wrote PR #15's row; site key reads, writes 401 | RUNBOOK, ARCHITECTURE | `is_test` filter proven by stubs |
| 2026-11-01 | TK-003 | Task closed | PR [#29](https://github.com/KaydenClark/Agentic-Management-System/pull/29) merged as 74b446e; receipt [4f0f73e](https://github.com/KaydenClark/Agentic-Management-System/commit/4f0f73e): `rsi_*` applied; `ams-rsi livecheck` refused a missing skills commit and a stale update | RUNBOOK, ARCHITECTURE | No real RSI row until S-002 |
| 2026-11-01 | TK-004 | Task closed | PRs [#31](https://github.com/KaydenClark/Agentic-Management-System/pull/31) (4d74e90) and [#37](https://github.com/KaydenClark/Agentic-Management-System/pull/37) (d26bb8c); receipt [ab2118c](https://github.com/KaydenClark/Agentic-Management-System/commit/ab2118c): `ams-history` imported 463 rows matching record counts; rerun added 0 | RUNBOOK, ARCHITECTURE | Dev-only records not imported; no scheduled re-import |

## Review and Human QA

Spec review only; presentation gets Human QA in S-007.

## Completion Result

Pending.

## Remaining Limitations Or Follow-Up Specs

- Supabase region is the nearest US default unless the owner chooses otherwise.

## Supersession

- Supersedes: the earlier draft's JSONL ledger files.
- Superseded by: none
