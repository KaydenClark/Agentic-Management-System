# TK-001 - First-trial rows are seeded from real sources only, this build's history and the skills repository's before/after notes, each labeled at the strength it supports

**Task ID:** TK-001
**Spec ID:** S-002
**Slice:** First-trial rows are seeded from real sources only, this build's history and the skills repository's before/after notes, each labeled at the strength it supports
**Status:** blocked
**Blockers:** S-006
**Destination:** spec-acceptance: Real, labeled seeds; Full rows
**Planned verification:** rows queried with source, skills pin and strength label; no outcome claim

## Assignment

**Target branch:** `main`. Branch from `origin/main`, open a PR into `main` and merge it once current and checked, per `AGENTS.md`. Orchestrator B's local lane only: it holds the writer's key and the skills repository checkout.

Read `AGENTS.md`, this Task, the parent Spec (`../../SPEC.md`), DDR-000W and DDR-000T under `workbench/docs/ddr/`, ADR-000A under `workbench/docs/adr/`, and the S-006 writer under `src/`.

Deliver the first-trial seed through the S-006 writer, from real sources only:
1. **This build.** One trial row for the build so far, derived from S-006's build-history rows (Specs, Tasks, PRs, returns and corrections), with the runtime, controls and skills commits, and cost and tokens where recorded (unknown stays unknown, never estimated). Strength: single trial, no control.
2. **Skills fixes.** One row per before/after note the owner's skills repository records for a recent skill fix, naming the skills commit and a short summary in your own words, never its private text. Strength: anecdote, unless the note records repeated runs.

Record what you found and skipped in the hand-back. Make no outcome claim.

Out of scope: running new trials (TK-002, TK-003).

Hand back to S-002 with `close`.

## Acceptance

- [ ] Every seed row names its source (build-history row ID or skills commit SHA), skills pin and strength label; a query for rows missing any returns none.
- [ ] No row copies text from the private skills repository; the hand-back lists each source used.
- [ ] No seed row is labeled stronger than single trial unless its source records repeated runs.
