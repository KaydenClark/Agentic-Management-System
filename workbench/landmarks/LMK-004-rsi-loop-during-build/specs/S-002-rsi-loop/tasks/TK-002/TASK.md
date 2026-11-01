# TK-002 - A noise-floor run of the current version against itself on a fixed task set records per-task flip rate and spread

**Task ID:** TK-002
**Spec ID:** S-002
**Slice:** A noise-floor run of the current version against itself on a fixed task set records per-task flip rate and spread
**Status:** in-progress
**Blockers:** none
**Destination:** spec-acceptance: Noise floor first; Sandboxed; Graders independent
**Planned verification:** rows from repeated same-version runs and the recorded floor

## Assignment

**Target branch:** `main`. Branch from `origin/main`, open a PR into `main` and merge it once current and checked, per `AGENTS.md`. Orchestrator B's local lane only: it holds the writer's key and the skills repository checkout.
**Claimed by:** s002-noise-floor
**Current claimant:** s002-noise-floor

Uses the owner's existing paid-plan meter, not an API campaign budget (JOT-6e1500aa-cbde-41c2-b638-f10fa9ef83e3 in the linked AMS-purpose Wiki). The owner resumed S-002 Journey on 2026-11-01; the former campaign-budget blocker is superseded. Required S-006 private assessment and trial-row inputs are delivered through PRs #80/#81/#83/#86 at `6e30c87`; formal S-006 owner QA remains separate. The orchestrator released this input gate at accepted bootstrap merge `17293a09d55806342442e57e6253984e20cdb7b8`. Read `AGENTS.md`, this Task, the parent Spec, ADR-002G, ADR-002I, ADR-002L and ADR-002J under `workbench/docs/adr/`, and `evals/EVAL-TASK-TEMPLATE.md`.

Deliver step zero of the loop: a small fixed task set under `evals/` (dev split, at least three tasks, each with a grader taken from the accepted version), a runner that executes a pinned version in a sandbox without skipped permission checks, and repeated same-version runs whose rows (with arm, version, skills pin, provider, model, effort, cost, tokens and completed state) are written through S-006. Compute and record the per-task flip rate and spread as the noise floor.

Hand back to S-002 with `close`, including measured subscription usage, or unknown when unavailable.

## Acceptance

- [ ] At least three same-version runs per task exist as rows with full fields.
- [ ] The floor (flip rate and spread per task) is recorded and cited by row IDs.
- [ ] Trial logs show no skipped permission checks; the grader commit equals the accepted version's.

## Resumed bounded run

The orchestrator assigned `feature/s002-rsi-loop` as the sole primary writer. Preserve r1 and the three-run Spec rule; the older two-run Task wording is reconciled above. First deliver a checked runner, frozen five-case narrow-oracle qualification protocol and deterministic error/identity guards. Actual calibration and the nine same-version worker/nine fresh judge calls stay held until the orchestrator selects the reviewed merged reference. No candidate comparisons or skill modifications occur in this Task.
