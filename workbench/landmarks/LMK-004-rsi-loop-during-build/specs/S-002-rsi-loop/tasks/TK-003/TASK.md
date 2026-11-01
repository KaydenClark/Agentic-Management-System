# TK-003 - No-AMS and plain-instruction control arms run on the same tasks, with paired per-task statistics and intervals

**Task ID:** TK-003
**Spec ID:** S-002
**Slice:** No-AMS and plain-instruction control arms run on the same tasks, with paired per-task statistics and intervals
**Status:** blocked
**Blockers:** TK-002
**Destination:** spec-acceptance: Controls run
**Planned verification:** control rows and a paired comparison against the floor

## Assignment

**Target branch:** `main`. Branch from `origin/main`, open a PR into `main` and merge it once current and checked, per `AGENTS.md`. Orchestrator B's local lane only: it holds the writer's key and the skills repository checkout.

Read `AGENTS.md`, this Task, the parent Spec, ADR-002I under `workbench/docs/adr/` and the TK-002 task set, runner and floor.

Deliver the control arms: run a no-AMS arm and a plain-instruction arm on the same tasks, same provider, model and effort as the AMS arm, writing rows through S-006; then a paired per-task comparison with intervals, read against the noise floor. A difference inside the floor is reported as noise.

Hand back to S-002 with `close`, including spend.

## Acceptance

- [ ] Each task has AMS, no-AMS and plain-instruction rows from one comparison.
- [ ] The comparison reports paired per-task differences with intervals, and labels any lift smaller than the floor as noise.
