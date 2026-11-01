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

## Engineering checkpoint

PR #92 delivers a model-free preparation CLI, frozen source/binary/system-context identities, five-case narrow qualification, one foreground worker/judge slot at a time, private immutable partial journals, public-safe S-006 rows/readback and three-row noise calculations. No actual calibration or worker trial has run; all Task acceptance remains unchecked. The root must review and select a merged exact reference before releasing qualification, then inspect qualification before separately releasing the nine worker/judge slots.

Observed red: new focused test collection lacked the series module. Latest focused checks: 170 passed, 1 skipped, including cancellation after worker completion, blocked unqualified/repeated calls, mixed-version floor refusal, system-context propagation and distinct private marker exclusion. At initial engineering commit `bb4aace`, host full suite passed 586/4 skipped; enclosed full suite had the known 97 failures/9 errors from loopback-bind denial. Final delta moves/strengthens outcomes validation; its exact-candidate full/fresh checks are pending. No model call, database trial row, semantic qualification, measured floor, candidate improvement or owner Human QA is claimed.

Independent source review of the initial engineering candidate proved a Git replace-blob bypass and mixed-run floor acceptance. Same-run repairs ignore replacement objects, disable lazy fetch/outward protocols and require one positive integer run identity. Actual inert replace-blob regression failed before repair and passes afterward; a missing promisor blob stays unavailable without invoking its upload-pack. The root additionally required deterministic literal quote validation: invented Yes/No evidence now yields Unknown; real do-nothing/Unicode quotations preserve the semantic verdict. Prompt bytes change before any calibration, with zero calls to date. Focused affected checks: 177 passed, 1 skipped. Historical exact `3f132aa` local/fresh suites both passed 588/4 skipped; these source corrections require their own final check/pin.

## Reviewed engineering reference

Runtime/caller reference `921cb3e4fbadf73a7150d88439d5bcae6ff2961d`, PR #92: exact-head CI run 87 (`41354195011`) passed. Independent noncontributor source inspection reported no remaining bounded engineering blocker at that exact reference; it independently ran 177 affected checks with 1 skip at behavior-identical `475950c` and inspected the complete final cleanup. Implementor local and fresh-clone full suites at `475950c` both passed 595/4 skipped; final `921cb3e` removes only an unused assignment and trailing blank line. Both final local/fresh affected suites passed 177/1 skipped; final fresh doctor/layout/render (no diff) and cumulative diff check passed. The two existing doctor informational findings (legibility declarations and permission-scope drift) remain visible and unchanged.

Model-free private preparation binds source `921cb3e`, protocol digest `5158239327cab1918a688a9c079a924e1ff849c48a6231efcca20cb1b78fa8c1`, and complete private record digest `0997ca9532f3d7099ad70b584dc32d1a9188147347c4e592488926c0e0212185`. Pre-merge source verification correctly refuses this uncontained reference. The record still declares released:false and the protected oracle remains unqualified. Planned calls: five qualification calls, then hold; nine worker plus nine fresh judge calls only after separate root release. Actual calls 0, actual trial rows 0, measured floor absent. This engineering delivery neither completes TK-002 nor qualifies the oracle, certifies AMS, demonstrates benefit or records Human QA.
