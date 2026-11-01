# TK-000E - Review FAIL at c87bf4e corrected: readcheck fails on extra rows, history current, recorded_fact limited to build history, repeatable secret scan

**Task ID:** TK-000E
**Spec ID:** S-006
**Slice:** Review FAIL at c87bf4e corrected: readcheck fails on extra rows, history current, recorded_fact limited to build history, repeatable secret scan
**Status:** done
**Blockers:** TK-005
**Destination:** spec-acceptance: Build history from real records; Real sources only; No secrets in Git
**Planned verification:** pytest with red-first tests for each finding; live ams-history import and readcheck (missing 0, extra 0), ams-rsi and ams-sources livecheck, get_advisors

## Assignment

**Target branch:** `main`. Branch from `origin/main`, open a PR into `main` and merge it once current and checked, per `AGENTS.md`.
**Claimed by:** orchestrator-b-tk000e-implementor
**Current claimant:** orchestrator-b-tk000e-implementor
**Proof:** PR #49 (a03d739): readcheck missing 0, extra 0; livechecks pass

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

- [x] A readcheck over rows plus one fabricated row exits 1 and names it.
- [x] Live `ams-history readcheck` after import: missing 0, extra 0.
- [x] The writer and the database refuse `recorded_fact` on `rsi_runs` and `rsi_results`.
- [x] A pytest scans tracked files for real secret shapes and fails on a planted fake.
- [x] L1 and L2 are recorded in the Spec.
- [x] `uv run pytest` passes.

## Proof notes

PR #49 merged as a03d739 (Codex: no findings). `uv run pytest`: 339 passed, 3 skipped; red first for H1, M2, L2.

- **H1:** `test_readcheck_fails_on_a_hand_typed_row_no_record_derives`.
- **M2:** `test_recorded_fact_is_for_build_history_only`, `test_the_rsi_writer_refuses_recorded_fact_before_sending`, `test_the_database_refuses_recorded_fact_on_rsi_tables`. Migration `20261101144510_rsi_strength_and_pass_rules` was applied with `apply_migration`; security advisors returned no lints.
- **L2:** `test_a_score_alone_does_not_grade_a_completed_trial`, `test_the_database_requires_passed_on_a_completed_trial`.
- **M3:** `tests/test_secret_scan.py` checks the tree and history. Commit 75d1fad's hand-written fake JWT, removed in f50a240, is named in `KNOWN_FAKE_COMMITS`.
- **M1:** live from the shared checkout at a03d739:
  - `ams-keycheck`: authenticated.
  - `ams-history import` inserted 142 rows (463 were already recorded).
  - `readcheck`: rows 605, missing 0, extra 0, unsourced 0.
  - `ams-rsi livecheck` and `ams-sources livecheck` exit 0, including the `recorded_fact` refusal on both RSI tables. Cleanup left 0 rows.
- **L1:** recorded in the Spec's limitations.

This Task's changes also deliver the content of orchestrator C's TK-000C (secret scan of tree and history) and TK-000D (no `recorded_fact` on the RSI tables). Those records stay open for their owner to reconcile.

## Receipt

| Run | Branch | HEAD SHA | Upstream | Dirty | Tests | Docs touched | Remaining gap | Checksum |
|---|---|---|---|---|---|---|---|---|
| 1 | feat/s006-tk000e-close | 979c29ad2e046308fbb63ffd231636188b29a380 | ahead 0 behind 0 | 0 | PR #49 (a03d739): readcheck missing 0, extra 0; livechecks pass | Spec, RUNBOOK | Fresh review; close attribution: {"agent":"orchestrator-b-tk000e-implementor","claimant":"orchestrator-b-tk000e-implementor","onBehalfOf":null} | 8ced6a3d260fb80f3268b0f37b7121bc06b31fc724e25200116aac3f16d8579a |
