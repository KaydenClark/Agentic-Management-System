# TK-001 - A committed report gives the commits and days `dev` is ahead of and behind `main` at a named time

**Task ID:** TK-001
**Spec ID:** S-013
**Slice:** A committed report gives the commits and days `dev` is ahead of and behind `main` at a named time
**Status:** done
**Blockers:** none
**Destination:** spec-acceptance: Drift measured; No secrets
**Planned verification:** script test on a fixture repository plus one real report

## Assignment

**Target branch:** `main`. Branch from `origin/main`, open a PR into `main` and merge it once current and checked, per `AGENTS.md`. Orchestrator C's cloud lane: read through Git and GitHub only, hold no Supabase or Vercel secret, write no product code. Reports go to `workbench/feedback/coherence/`.
**Claimed by:** orchestrator-C
**Current claimant:** orchestrator-C
**Proof:** node --test workbench/tools/coherence-drift.test.mjs: 4 pass at 6848b75; clean-clone run with only git; report workbench/feedback/coherence/DRIFT-2026-11-01.md (main 0a7d04e, dev b06d7db, 3 ahead, 0 behind)

Read `AGENTS.md`, this Task, the parent Spec (`../../SPEC.md`), ADR-002T and ADR-000H under `workbench/docs/adr/`.

Deliver a read-only check (Python on the pinned version, or Node beside the room tools) that fetches `origin` and reports, at a named UTC time and pair of SHAs, the commits and days `dev` is ahead of `main` and behind it, plus a configurable threshold result. Commit one real report. The check starts non-blocking. Write the test first against a fixture Git repository with known drift.

Out of scope: raising the Grill Board item (TK-005); merging anything.

Hand back to S-013 with `close`.

## Acceptance

- [ ] The fixture test reports the known ahead and behind counts and days.
- [ ] One real report for this repository is committed, naming the time and both SHAs.
- [ ] The check needs no secret; it runs from a clean clone with only `git`.

## Receipt

| Run | Branch | HEAD SHA | Upstream | Dirty | Tests | Docs touched | Remaining gap | Checksum |
|---|---|---|---|---|---|---|---|---|
| 1 | claude/vigilant-wright-r50huh | 6848b751fb3196e2071508068698a3f97c07bf8d | ahead 0 behind 0 | 0 | node --test workbench/tools/coherence-drift.test.mjs: 4 pass at 6848b75; clean-clone run with only git; report workbench/feedback/coherence/DRIFT-2026-11-01.md (main 0a7d04e, dev b06d7db, 3 ahead, 0 behind) | workbench/feedback/coherence/DRIFT-2026-11-01.md; RUNBOOK not updated (at 2,996 of 3,000 chars, finding COH-005) | Grill Board item on breach (TK-005); thresholds 20 commits / 7 days are C's default pending owner choice; close attribution: {"agent":"orchestrator-C","claimant":"orchestrator-C","onBehalfOf":null} | 7943969fd191abd19ece89e39d89c00c08b0c45b857182ec4eb0bc52931883e2 |
