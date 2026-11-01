# TK-005 - Seed and test rows: a row without source and strength label is refused and test rows never reach the publishable key

**Task ID:** TK-005
**Spec ID:** S-006
**Slice:** Seed and test rows: a row without source and strength label is refused and test rows never reach the publishable key
**Status:** in-progress
**Blockers:** TK-003
**Destination:** spec-acceptance: Real sources only
**Planned verification:** live tests for the refusal and the hidden test row

## Assignment

**Target branch:** `main`. Branch from `origin/main`, open a PR into `main` and merge it once current and checked, per `AGENTS.md`.
**Claimed by:** orchestrator-b-tk005-implementor
**Current claimant:** orchestrator-b-tk005-implementor

Orchestrator B's lane only. Read `AGENTS.md`, this Task, the parent Spec (`../../SPEC.md`), DDR-000T and DDR-000W, and the writer under `src/`.

Deliver the writer rules S-002's seeding depends on: a row is refused unless it names its source and a strength label from a closed list (anecdote, single trial, repeated trials, held-out with interval); a row may be marked as a test row, and the site's read policy never returns test rows.

Out of scope: choosing or writing seed rows (S-002 TK-001).

Hand back to S-006 with `close`.

## Acceptance

- [ ] A row with no source, or a strength label outside the list, is refused.
- [ ] A marked test row is readable with the service key and invisible to the publishable key.
- [ ] `uv run pytest` passes.
