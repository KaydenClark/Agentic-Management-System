# TK-002 - A noise-floor run of the current version against itself on a fixed task set records per-task flip rate and spread

**Task ID:** TK-002
**Spec ID:** S-002
**Slice:** A noise-floor run of the current version against itself on a fixed task set records per-task flip rate and spread
**Status:** blocked
**Blockers:** S-006, owner:rsi-campaign-approval
**Destination:** spec-acceptance: Noise floor first; Sandboxed; Graders independent
**Planned verification:** rows from repeated same-version runs and the recorded floor

## Assignment

**Target branch:** `main`. Branch from `origin/main`, open a PR into `main` and merge it once current and checked, per `AGENTS.md`. Orchestrator B's local lane only: it holds the writer's key and the skills repository checkout.

Blocked until the owner gives the standing campaign approval (`rsi-campaign-approval` in the Spec). Read `AGENTS.md`, this Task, the parent Spec, ADR-002G, ADR-002I, ADR-002L and ADR-002J under `workbench/docs/adr/`, and `evals/EVAL-TASK-TEMPLATE.md`.

Deliver step zero of the loop: a small fixed task set under `evals/` (dev split, at least three tasks, each with a grader taken from the accepted version), a runner that executes a pinned version in a sandbox without skipped permission checks, and repeated same-version runs whose rows (with arm, version, skills pin, provider, model, effort, cost, tokens and completed state) are written through S-006. Compute and record the per-task flip rate and spread as the noise floor.

Hand back to S-002 with `close`, including spend.

## Acceptance

- [ ] At least two same-version runs per task exist as rows with full fields.
- [ ] The floor (flip rate and spread per task) is recorded and cited by row IDs.
- [ ] Trial logs show no skipped permission checks; the grader commit equals the accepted version's.
