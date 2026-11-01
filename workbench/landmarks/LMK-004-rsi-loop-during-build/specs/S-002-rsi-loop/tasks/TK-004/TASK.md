# TK-004 - One full round runs from a failed row to a recorded disposition

**Task ID:** TK-004
**Spec ID:** S-002
**Slice:** One full round runs from a failed row to a recorded disposition
**Status:** blocked
**Blockers:** TK-003
**Destination:** spec-acceptance: Starts from failure; Stops
**Planned verification:** round record naming its failed row, rerun rows and disposition

## Assignment

**Target branch:** `main`. Branch from `origin/main`, open a PR into `main` and merge it once current and checked, per `AGENTS.md`. Orchestrator B's local lane only: it holds the writer's key and the skills repository checkout.

Read `AGENTS.md`, this Task, the parent Spec and the rows from TK-002 and TK-003.

Deliver one manual round: pick a failed row, name the earliest gap and its single owner, make one change through that owner's process (skills through the skills repository's own process), rerun the same tasks against the current version and the controls, and record the disposition (retain, revise or remove) with its rows. Stop after two failed fixes for one event and report.

Hand back to S-002 with `close`; the owner judges whether the round is worth automating.

## Acceptance

- [ ] The round record names the failed row it started from, the change, the rerun rows and the disposition.
- [ ] A round started from a retro idea, or a fourth attempt at one event, does not occur.
