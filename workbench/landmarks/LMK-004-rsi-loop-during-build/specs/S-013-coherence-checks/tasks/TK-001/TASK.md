# TK-001 - A committed report gives the commits and days `dev` is ahead of and behind `main` at a named time

**Task ID:** TK-001
**Spec ID:** S-013
**Slice:** A committed report gives the commits and days `dev` is ahead of and behind `main` at a named time
**Status:** in-progress
**Blockers:** none
**Destination:** spec-acceptance: Drift measured; No secrets
**Planned verification:** script test on a fixture repository plus one real report

## Assignment

**Target branch:** `main`. Branch from `origin/main`, open a PR into `main` and merge it once current and checked, per `AGENTS.md`. Orchestrator C's cloud lane: read through Git and GitHub only, hold no Supabase or Vercel secret, write no product code. Reports go to `workbench/feedback/coherence/`.
**Claimed by:** orchestrator-C
**Current claimant:** orchestrator-C

Read `AGENTS.md`, this Task, the parent Spec (`../../SPEC.md`), ADR-002T and ADR-000H under `workbench/docs/adr/`.

Deliver a read-only check (Python on the pinned version, or Node beside the room tools) that fetches `origin` and reports, at a named UTC time and pair of SHAs, the commits and days `dev` is ahead of `main` and behind it, plus a configurable threshold result. Commit one real report. The check starts non-blocking. Write the test first against a fixture Git repository with known drift.

Out of scope: raising the Grill Board item (TK-005); merging anything.

Hand back to S-013 with `close`.

## Acceptance

- [ ] The fixture test reports the known ahead and behind counts and days.
- [ ] One real report for this repository is committed, naming the time and both SHAs.
- [ ] The check needs no secret; it runs from a clean clone with only `git`.
