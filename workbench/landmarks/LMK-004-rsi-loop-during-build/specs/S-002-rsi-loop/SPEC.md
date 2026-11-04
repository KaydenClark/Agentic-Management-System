# S-002 - RSI evaluation and qualification

**Spec ID:** S-002
**Status:** active
**Priority:** 1
**Owner:** Kayden; orchestrator B (local)
**Stance:** Builder
**Updated:** 2026-11-03
**Catalog description:** Case contracts, comparisons, Fitness/Alignment qualification and regression evidence for LMK-004.
**Blockers:** none
**Confirmation:** [JOT-1871d72c-c1cf-4602-887c-3c996f26e086](../../../../wiki/context-active-spec-approvals.md)
**Execution approval:** [JOT-1871d72c-c1cf-4602-887c-3c996f26e086](../../../../wiki/context-active-spec-approvals.md)
**Next gate:** TK-000Y bounded structured-output correction; no further model calls or additional trial-store rows are released.

## Intent and authority

The [mapped owner intent](../../../../wiki/context-feedback-improvement-loop-plan.md#current-mapped-destination) authorizes Map only; execution holds remain. No new Tasks or trials.

[Owner decisions](../../../../wiki/context-ams-purpose.md) govern resumed Journey: fixed r1/acceptance, attempts, meter and bounded versus whole scope.

## Current Verified State

Scoring is met ([TK-000M](tasks/TK-000M/TASK.md#receipt)); cycle, evaluations, stops and readback remain open. The [baseline](../../../../feedback/REPORT-rsi-baseline-2026-11-01.md) is Broken 4/138, incomplete/unqualified, not a trial or strike. S-006/TK-000S owns exact identity. [TK-002](tasks/TK-002/TASK.md) owns the accepted narrow qualification and Unknown baseline slot; later slots wait on TK-000Y. Only stopped run28/result41 is published. Bootstrap is not benefit evidence. See [history](../../../../wiki/history/S-002.md).

## Desired Behavior

Failure -> earliest gap/owner -> one repository change -> baseline/retest -> disposition/later use.

### Evaluation within the RSI Landmark

LMK-004 owns the loop; S-000B executes, S-006 persists, S-013 detects recurrence and S-011 delivers shared-source changes. This Spec owns case contracts, comparisons, qualification and benefit decisions.

Evaluate individual skills or declared bundles; bundle gains do not certify each component. Diagnose skill, instruction, tool, environment, context, ownership, coordination, proof or model limitations; unknown remains unknown. Route product defects to their Specs.

Cases link original correct outcomes, baseline, loaded versions, tools and end states to r1 checks. Objective checks and qualified semantic judgments supply evidence, not new scores. Transcript-only tests cannot certify Git/filesystem behavior. Cheap screening never replaces full qualification.

Preserve historical provenance, development/held-out boundaries, prior-pass and cross-skill regressions. Count eligible successes, failures, owner interventions and later recurrence. Document size or audit gains alone are not useful benefit.

### Audit scores

Canonical: `audit-workbench` r1 checks/scenarios/qualification, version 1,
hash `96636d4a5e70cacbb0b94fd079340f02ed0f09b121b6498c1c70eebeb13b0578`.
Freeze rubric, scope/inventory/exclusions, IDs/classes, baseline/candidate/skill
pins, loaded artifacts, host/tools and evaluator model/prompt/qualification;
no changes/extra points.

r1 owns rows, pooled `100 × Yes / applicable`, run pass, levels (3/2/1/0 passing
of three runs = Excellent/Stable/Functional/Broken; Critical No overrides) and
eligibility; [assessments](../../../../../evals/ASSESSMENTS.md) implement them.
Missing/Unknown/refused/interrupted stays No in class and denominator; label
static/unqualified proof; no rounding; empty means no percentage. Acceptance
implies no QA/distribution/benefit; bounded results cannot certify ten-area AMS.

### Skill evals and retests

`evals/` pins case/failure, prompt/fixtures/reset, permissions, end state,
grader/model/host/loaded skill. Cover invocation/near misses, valid/adverse input,
prerequisites/discovery/resume/authority. Map r1 IDs; no extra points.
Qualify good/bad/do-nothing cases and judges per r1; protect inputs/logs; manual
trials until qualified. Findings close only by r1 three-run repaired-revision
retest; merge/omission/score cannot close; retain recurrence/new failures.

## Decisions And Contracts

- Retain only qualified Stable/Excellent with demonstrated useful benefit
  predeclared before comparison. First case: grilling failure; coordinate existing redesign.
- Failure-led rounds; review ineffective prior fixes on recurrence. One change/version.
- New campaigns use Mid/Small tiers by default, High when needed, on Codex or Claude subscription meters. Record the selection and reason; freeze provider/model/effort within a comparison. Existing campaign pins remain unchanged. Accepted-version runner/graders/scoring, never
  candidate-owned. Grader changes start a new series judged by its predecessor.
- Same-version noise floor first, then r1 paired trials: fixed-task
  AMS/no-AMS/plain-instruction arms, paired per-task intervals. Audit delta proves no benefit.
- Public lift needs >2 fresh held-out tasks, controls, baseline/interval.
  Studied cases retire to dev; scores are not lift.
- Sandbox without skipped permissions. Automatic proposing waits for a trusted
  grader, recorded subscription-meter availability and owner-judged manual round.
- Baseline 0: no strike. Candidate initial -> retry -> retry -> stop/report unless
  accepted. Repair/rename never resets; retain failures/harm.
- Trial rows: task/arm, version/skills pin, provider/model/effort, completion,
  cost/tokens availability, source. Subscription meter; unknown is not zero.

## Non-Goals

Weights; running loops during mapping; presentation (S-007).

## Dependencies And Blockers

S-000B executes; S-006 stores evidence; S-007 presents safe results. Only missing inputs block consumers.

## Vertical Implementation Slices

Existing Tasks retain their scope; Map creates none.

## Acceptance Criteria

- [ ] **Cycle:** one failure reaches diagnosis, bounded repair, qualified comparison, disposition, authorized adoption and later-use evidence. Missing pins/retests fail.
- [x] **Scoring:** pooled 8/10 + 1/2 + 1/2 = 10/14; empty has no score. Critical/Regression/missing-proof and level rules are tested.
- [ ] **Evals:** frozen contracts reject self-grading, do-nothing passes, static-only benefit, skipped permissions and below-noise gains.
- [ ] **Stops:** baseline excluded; fourth attempt, renamed/reset counter or omitted finding fails.
- [ ] **Readback:** S-006/S-007 preserve assessment/trial distinctions, failures and private-data boundaries; false storage claims fail.
- [ ] **Native evidence:** fresh real-tool execution proves required end state and loaded skill identity; a transcript alone fails Git/filesystem claims.
- [ ] **Worker evidence:** S-000B receipts preserve attempts; interruption cannot qualify an unrun check or restart stopped work.
- [ ] **Retention:** existing Fitness/Alignment checks establish Stable/Excellent, useful benefit and no regression. Original-case pass with regression fails; bundle gains cannot certify each skill.
- [ ] **Later use:** distinguish merge, authorized install, loading and outcomes. Recurrence is detected without owner prompting; stale loaded copies cannot count as repaired versions.

## Documentation Impact

LMK-004 owns the loop; Wiki explains intent. S-000B owns the worker, S-006 storage, S-007 visuals, S-013 detection and S-011 delivery. S-012 remains the lifecycle CLI. Plan reconciles Tasks later; only actual missing inputs block consumers.

## Testing Seams

CLI/runner/writer/readback: missing proof, recurrence, original-pass/regression-fail. Checks: RUNBOOK; [proof](tasks/TK-000M/TASK.md).

## Review and Human QA

Independent review per retained change; owner judges automation.

## Completion Result

Pending.

## Feedback-loop planning boundary

The mapped destination grants no implementation or new trial authority. Earlier approvals, explicit holds, attempts and stopped experiments retain scope. The [Wiki](../../../../wiki/context-feedback-improvement-loop-plan.md#current-mapped-destination) owns the sourced correction and continuation.

