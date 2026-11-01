# TK-005 - A drift threshold breach raises a Grill Board item

**Task ID:** TK-005
**Spec ID:** S-013
**Slice:** A drift threshold breach raises a Grill Board item
**Status:** blocked
**Blockers:** TK-001, S-004
**Destination:** spec-acceptance: Drift measured
**Planned verification:** fixture breach producing exactly one card

## Assignment

**Target branch:** `main`. Branch from `origin/main`, open a PR into `main` and merge it once current and checked, per `AGENTS.md`. Orchestrator C's cloud lane: read through Git and GitHub only, hold no Supabase or Vercel secret, write no product code. Reports go to `workbench/feedback/coherence/`.

Read `AGENTS.md`, this Task, the parent Spec, the TK-001 check, and S-004's card format under `grill-board/`.

Deliver: when the drift check's threshold is breached, it writes exactly one Grill Board card in S-004's format (Priority, Value, a reason for each), and no duplicate while the same breach persists.

Hand back to S-013 with `close`.

## Acceptance

- [ ] A fixture breach produces one card; a second run of the same breach produces none.
- [ ] No breach produces no card.
