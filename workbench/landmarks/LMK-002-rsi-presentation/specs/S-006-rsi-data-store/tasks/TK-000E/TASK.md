# TK-000E - Review FAIL at c87bf4e corrected: readcheck fails on extra rows, history current, recorded_fact limited to build history, repeatable secret scan

**Task ID:** TK-000E
**Spec ID:** S-006
**Slice:** Review FAIL at c87bf4e corrected: readcheck fails on extra rows, history current, recorded_fact limited to build history, repeatable secret scan
**Status:** in-progress
**Blockers:** TK-005
**Destination:** spec-acceptance: Build history from real records; Real sources only; No secrets in Git
**Planned verification:** pytest with red-first tests for each finding; live ams-history import and readcheck (missing 0, extra 0), ams-rsi and ams-sources livecheck, get_advisors

## Assignment

**Target branch:** `main`. Branch from `origin/main`, open a PR into `main` and merge it once current and checked, per `AGENTS.md`.
**Claimed by:** orchestrator-b-tk000e-implementor
**Current claimant:** orchestrator-b-tk000e-implementor

Orchestrator B's lane only. Read `AGENTS.md`, this Task, the parent Spec (`../../SPEC.md`) and the writers under `src/ams/`.

The independent review of the assembled Spec at main `c87bf4ec86206bd5f734af7b828c81c3d3356a00` returned FAIL. Correct its findings:

- **H1.** `ams-history readcheck` exits 0 with rows in `extra`, so a hand-typed row passes. It must fail on any extra row.
- **M1.** Build history is stale (63 missing). Re-import from the shared checkout; readcheck missing 0, extra 0; the Spec says import runs on demand; the close procedure names the re-import.
- **M2.** `recorded_fact` is accepted on `rsi_runs` and `rsi_results`. Refuse it there in the writers and, by a new migration, in the database.
- **M3.** No repeatable hygiene check. A pytest scans every tracked file for real secret shapes, allows the bare prefix, and fails on a planted fake.
- **L2.** Decide and record whether a completed result may carry `score` without `passed`.
- **L1.** Evidence and receipt rows are keyed by table index; record it as a known limit unless a stable key is small.

Out of scope: ticking acceptance boxes or completing S-006; a fresh independent review decides that.

Hand back to S-006 with `close`.

## Acceptance

- [ ] A readcheck over rows plus one fabricated row exits 1 and names it.
- [ ] Live `ams-history readcheck` after import: missing 0, extra 0.
- [ ] The writer and the database refuse `recorded_fact` on `rsi_runs` and `rsi_results`.
- [ ] A pytest scans tracked files for real secret shapes and fails on a planted fake.
- [ ] L1 and L2 are recorded in the Spec.
- [ ] `uv run pytest` passes.
