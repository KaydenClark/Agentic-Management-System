# TK-002 - The writer records one real build event and the site's publishable key reads it back while every client write fails

**Task ID:** TK-002
**Spec ID:** S-006
**Slice:** The writer records one real build event and the site's publishable key reads it back while every client write fails
**Status:** in-progress
**Blockers:** TK-001
**Destination:** spec-acceptance: Writer works end to end; No client writes
**Planned verification:** live insert and publishable-key read and write test

## Assignment

**Target branch:** `main`. Branch from `origin/main`, open a PR into `main` and merge it once current and checked, per `AGENTS.md`.
**Claimed by:** claude-s006-tk002
**Current claimant:** claude-s006-tk002

Orchestrator B's lane only. Read `AGENTS.md`, this Task, the parent Spec (`../../SPEC.md`), `supabase/migrations/` (the read-only baseline), DDR-000O under `workbench/docs/ddr/` and the TK-001 key module under `src/`.

Deliver one whole path: a migration adding the build-history table with a SELECT policy for the site and no client write path; applying it to the project with the Supabase CLI; the writer inserting one real build event (for example the merge commit that landed TK-001, named by SHA) with the service key; and a test that reads it back with `SUPABASE_PUBLISHABLE_KEY` while insert, update and delete with that key fail. If this session cannot apply migrations, stop and report rather than simulate.

Out of scope: RSI result tables (TK-003), the full history import (TK-004).

Hand back to S-006 with `close`.

## Acceptance

- [ ] The migration applies cleanly and is committed under `supabase/migrations/`.
- [ ] One real build event row exists in Supabase, naming its commit SHA as source.
- [ ] The publishable key selects the row; its insert, update and delete each fail.
- [ ] Nothing is written only to a local file; `uv run pytest` passes.
