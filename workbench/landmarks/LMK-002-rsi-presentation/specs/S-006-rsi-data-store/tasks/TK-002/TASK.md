# TK-002 - The writer records one real build event and the site's publishable key reads it back while every client write fails

**Task ID:** TK-002
**Spec ID:** S-006
**Slice:** The writer records one real build event and the site's publishable key reads it back while every client write fails
**Status:** done
**Blockers:** TK-001
**Destination:** spec-acceptance: Writer works end to end; No client writes
**Planned verification:** live insert and publishable-key read and write test

## Assignment

**Target branch:** `main`. Branch from `origin/main`, open a PR into `main` and merge it once current and checked, per `AGENTS.md`.
**Claimed by:** claude-s006-tk002
**Current claimant:** claude-s006-tk002
**Proof:** PR #18 merged as d279ae1: migration 20261101132456_build_events applied to hqvtnpvwwppbeurponnn, security advisors no finding; uv run pytest 108 passed, 1 skipped (writer tests red first: import error, then 9 failing inconclusive-probe tests after Codex P2 finding 4435825468, fixed and resolved); live from main checkout: ams-writer record-merge 884d021 printed inserted: id=1 kind=merge subject=PR #15 strength=recorded_fact is_test=False, rerun printed already recorded; ams-writer readcheck with the publishable key printed rows: 1, insert/update/delete refused (http status 401), row unchanged: yes, exit 0; AMS_LIVE=1 live test passed; hygiene grep found no key in the diff; render no diff, doctor no blocking finding

Orchestrator B's lane only. Read `AGENTS.md`, this Task, the parent Spec (`../../SPEC.md`), `supabase/migrations/` (the read-only baseline), DDR-000O under `workbench/docs/ddr/` and the TK-001 key module under `src/`.

Deliver one whole path: a migration adding the build-history table with a SELECT policy for the site and no client write path; applying it to the project with the Supabase CLI; the writer inserting one real build event (for example the merge commit that landed TK-001, named by SHA) with the service key; and a test that reads it back with `SUPABASE_PUBLISHABLE_KEY` while insert, update and delete with that key fail. If this session cannot apply migrations, stop and report rather than simulate.

Out of scope: RSI result tables (TK-003), the full history import (TK-004).

Hand back to S-006 with `close`.

## Acceptance

- [x] The migration applies cleanly and is committed under `supabase/migrations/`.
- [x] One real build event row exists in Supabase, naming its commit SHA as source.
- [x] The publishable key selects the row; its insert, update and delete each fail.
- [x] Nothing is written only to a local file; `uv run pytest` passes.

## Receipt

| Run | Branch | HEAD SHA | Upstream | Dirty | Tests | Docs touched | Remaining gap | Checksum |
|---|---|---|---|---|---|---|---|---|
| 1 | feat/s006-tk002-close | 03712888eeb2b952d4a8e4c9e8f76b529ddfae4c | ahead 0 behind 0 | 0 | PR #18 merged as d279ae1: migration 20261101132456_build_events applied to hqvtnpvwwppbeurponnn, security advisors no finding; uv run pytest 108 passed, 1 skipped (writer tests red first: import error, then 9 failing inconclusive-probe tests after Codex P2 finding 4435825468, fixed and resolved); live from main checkout: ams-writer record-merge 884d021 printed inserted: id=1 kind=merge subject=PR #15 strength=recorded_fact is_test=False, rerun printed already recorded; ams-writer readcheck with the publishable key printed rows: 1, insert/update/delete refused (http status 401), row unchanged: yes, exit 0; AMS_LIVE=1 live test passed; hygiene grep found no key in the diff; render no diff, doctor no blocking finding | RUNBOOK names ams-writer record-merge/readcheck and AMS_LIVE=1; ARCHITECTURE names ams-writer and the build_events migration; both at or under 3,000 chars | Only build_events exists, with one row; the is_test filter is proven by policy text and stubs, not by a live test row. RSI result and run tables, stale-update refusal (TK-003) and the full build-history import (TK-004) remain; legacy-JWT path still proven only with fakes; close attribution: {"agent":"claude-s006-tk002","claimant":"claude-s006-tk002","onBehalfOf":null} | b3062433173b2586a9bf540191657fc3ad30fabc5dfcfa6eaebf63229ef8fbe3 |
