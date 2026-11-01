# TK-003 - The writer records RSI result and run rows with full provenance, refusing a missing skills commit and a stale update

**Task ID:** TK-003
**Spec ID:** S-006
**Slice:** The writer records RSI result and run rows with full provenance, refusing a missing skills commit and a stale update
**Status:** done
**Blockers:** TK-002
**Destination:** spec-acceptance: Schema and provenance; Conflict refusal
**Planned verification:** live tests for the missing-field and conflict refusals

## Assignment

**Target branch:** `main`. Branch from `origin/main`, open a PR into `main` and merge it once current and checked, per `AGENTS.md`.
**Claimed by:** claude-s006-tk003
**Current claimant:** claude-s006-tk003
**Proof:** PR #29 merged as 74b446e: migration 20261101134221_rsi_rows (rsi_runs, rsi_results) applied to hqvtnpvwwppbeurponnn, security advisors no lints; uv run pytest 212 passed, 2 skipped (rsi_rows tests red first: import error; Codex P2 findings 4435897333 and 4435926325 each fixed test-first, replied and resolved; final head 6aea2dc reviewed with no unresolved finding); live from main checkout: uv run ams-rsi livecheck exit 0, writer and database each refused a missing skills_commit (code 23502, column skills_commit) and a stale update (http 409, PT409), row unchanged: yes, site key saw 0 of 1 test runs and 0 of 1 test results, client insert/update/delete refused (401) on both tables, cleanup remaining 0; AMS_LIVE=1 test_live_livecheck passed; SQL count rsi_runs 0, rsi_results 0; hygiene grep found no key in the diff; render no diff, doctor no blocking finding

Orchestrator B's lane only. Read `AGENTS.md`, this Task, the parent Spec (`../../SPEC.md`), ADR-000A, ADR-002J and DDR-000T, and the writer under `src/`.

Deliver: a migration for RSI result and run tables carrying every field the Spec's Desired Behavior names (task, split, arm, runtime, controls and skills commits, provider, model, effort, pass, cost, tokens, completed state, source), non-null where required; the writer's insert for them; and a stale-update refusal: an update against a row changed since it was read is refused.

Out of scope: seeding (TK-005 and S-002).

Hand back to S-006 with `close`.

## Acceptance

- [x] Inserting a result row with no skills commit fails at the database.
- [x] A complete row inserts and the publishable key reads it; client writes fail on both new tables. *Scope as assigned by orchestrator B:* complete rows were inserted only as `is_test` rows (no real trial has run, so a non-test row would be fabricated); the publishable key's select succeeded and showed 0 of them, as the policy requires. A visible non-test row read waits for S-002's first real row.
- [x] An update against a row changed since it was read is refused and the row is unchanged.
- [x] `uv run pytest` passes.

## Receipt

| Run | Branch | HEAD SHA | Upstream | Dirty | Tests | Docs touched | Remaining gap | Checksum |
|---|---|---|---|---|---|---|---|---|
| 1 | feat/s006-tk003-close | 4f0f73e7d949a21eadaf19d9ccf512ed44f267fb | ahead 0 behind 0 | 0 | PR #29 merged as 74b446e: migration 20261101134221_rsi_rows (rsi_runs, rsi_results) applied to hqvtnpvwwppbeurponnn, security advisors no lints; uv run pytest 212 passed, 2 skipped (rsi_rows tests red first: import error; Codex P2 findings 4435897333 and 4435926325 each fixed test-first, replied and resolved; final head 6aea2dc reviewed with no unresolved finding); live from main checkout: uv run ams-rsi livecheck exit 0, writer and database each refused a missing skills_commit (code 23502, column skills_commit) and a stale update (http 409, PT409), row unchanged: yes, site key saw 0 of 1 test runs and 0 of 1 test results, client insert/update/delete refused (401) on both tables, cleanup remaining 0; AMS_LIVE=1 test_live_livecheck passed; SQL count rsi_runs 0, rsi_results 0; hygiene grep found no key in the diff; render no diff, doctor no blocking finding | RUNBOOK names uv run ams-rsi livecheck; ARCHITECTURE names ams-rsi and the rsi_* migration; both at 2,999 chars; module docstring in src/ams/rsi_rows.py documents the Store API and livecheck | No non-test RSI row exists (none may be fabricated), so a site-key read of a visible RSI row is proven by grant, policy and a 200 select, not by a live visible row; first real rows come from S-002. Legacy-JWT path still proven only with fakes; close attribution: {"agent":"claude-s006-tk003","claimant":"claude-s006-tk003","onBehalfOf":null} | 88cacbcb91b954daf560a5694429edfde0972df89753189de7e519985bce587a |
