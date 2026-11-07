# S-002 - RSI evaluation and qualification

**Spec ID:** S-002
**Status:** active
**Priority:** 1
**Owner:** Kayden; orchestrator B (local)
**Stance:** Builder
**Updated:** 2026-11-07
**Catalog description:** Case contracts, comparisons, Fitness/Alignment qualification and regression evidence for LMK-004.
**Blockers:** none
**Confirmation:** [JOT-1871d72c-c1cf-4602-887c-3c996f26e086](../../../../wiki/context-active-spec-approvals.md)
**Execution approval:** [JOT-1871d72c-c1cf-4602-887c-3c996f26e086](../../../../wiki/context-active-spec-approvals.md)
**Next gate:** TK-000Y bounded structured-output correction; no further model calls or additional trial-store rows are released.

## Intent and authority

[Current RSI destination](../../../../wiki/context-feedback-improvement-loop-plan.md#jot-7862917b-48cb-41bc-8f21-0ddfc611cdac) maps the Servitor proof and optional participation. This updates requirements only: no Task activation, model trial, database write or installation occurs through Map. Existing receipts, frozen comparisons and stopped attempts retain their scope.


[Owner intent](../../../../wiki/context-feedback-improvement-loop-plan.md#jot-55876e5d-6957-4a4e-917b-8ba7245adee2) authorizes preparation; implementation and trials remain held.

[Owner decisions](../../../../wiki/context-ams-purpose.md) govern resumed Journey: fixed r1/acceptance, attempts, meter and bounded versus whole scope.

## Current Verified State

Historical r1 scoring is met ([TK-000M](tasks/TK-000M/TASK.md#receipt)); the new skill severity/separate-score contract is not implemented; cycle, evaluations, stops and readback remain open. The [baseline](../../../../feedback/REPORT-rsi-baseline-2026-11-01.md) is Broken 4/138, unqualified and not a strike; S-006/TK-000S owns identity. TK-002 owns narrow qualification and Unknown baseline; later slots wait on TK-000Y. Only stopped run28/result41 is published; bootstrap is not benefit. See [history](../../../../wiki/history/S-002.md).

## Desired Behavior

Failure -> earliest gap/owner -> one repository change -> baseline/retest -> disposition/later use.

### Evaluation within the RSI Landmark

LMK-004 owns the loop; S-000B executes, S-006 persists, S-013 detects recurrence and S-011 delivers shared-source changes. This Spec owns case contracts, comparisons, qualification and benefit decisions.

Evaluate individual skills or declared bundles; bundle gains do not certify each component. Diagnose skill, instruction, tool, environment, context, ownership, coordination, proof or model limitations; unknown remains unknown. Route product defects to their Specs.

Cases link original outcomes, baseline, actual loaded versions, tools and end states to r1. Separate optimizer training/selection from fresh confirmation; studied cases become development cases. Target-skill-withheld controls retain mandatory authority and safety instructions. Record natural routing and explicit invocation per host, actual loading and verified end state. Measure owner review effort and recurrence per eligible use; unknown denominators stay unknown. Objective and qualified semantic checks supply evidence, not new scores. Transcripts cannot certify Git/filesystem behavior; cheap screening cannot replace qualification.

Preserve historical provenance, development/held-out boundaries, prior-pass and cross-skill regressions. Count eligible successes, failures, owner interventions and later recurrence. Document size or audit gains alone are not useful benefit.

### Audit scores

Shared question source and whole-Workbench rubric: `audit-workbench` r1 version 1, hash `96636d4a5e70cacbb0b94fd079340f02ed0f09b121b6498c1c70eebeb13b0578`. Freeze rubric, scope, IDs, pins, loaded artifacts, host/tools and evaluator/model/prompt/qualification; no extra points.

Whole-Workbench Alignment retains r1 pooled `100 × Yes / applicable`, eligibility and its own levels; [assessments](../../../../../evals/ASSESSMENTS.md) describe the existing implementation. New skill audits use shared Alignment questions for applicable Quality checks and skill-specific regression tests, including connected workflows. Freeze their inventories and versions before comparison.

Across three skill audit runs, report Quality Score and Regression Score separately: each pools `100 × Yes / applicable` within its own class. Show Critical results separately; they do not lower either percentage by being counted in another class. No applicable checks means unavailable, not 100%. Preserve per-run counts and evidence, justified N/A and missing/unknown rules.

The most serious failure across all three runs determines the skill grade: Excellent = no failures; Stable = Quality failures only; Functional = Regression failure with no Critical failure; Broken = any Critical failure. Skipping an explicitly requested skill is a Critical failed requested use even if it never loaded. An incomplete audit set cannot establish qualification or Excellent. A grade is not release acceptance. The repository scorer currently uses the older passing-run-count grade; implementing this new skill contract must leave historical assessments and whole-Workbench scoring intact. Missing/Unknown/refused/interrupted stays No in class and denominator; label static/unqualified proof; no rounding or empty percentage. Acceptance is not QA, distribution or benefit; bounded results cannot certify ten-area AMS.

### Skill evals and retests

`evals/` pins case, fixtures, permissions, end state, grader/model/host/skill. Cover invocation, near misses, adverse input, prerequisites, discovery, resume and authority. Map r1 IDs; qualify judges and good/bad/do-nothing cases; protect inputs/logs and use manual trials until qualified. Findings close only by r1 three-run repaired-revision retest, not merge, omission or score; retain recurrence and new failures.

## Decisions And Contracts

- Retain only qualified Stable/Excellent with demonstrated useful benefit
  predeclared before comparison. First proof: one real AMS website task on Servitor; Plan selects the exact failure/case and coordinates existing website work. Earlier grilling fixtures and attempt histories remain frozen.
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

[TK-002Q case contract](../../../../wiki/guidebooks/rsi-case-contract.md).

## Acceptance Criteria

- [ ] **Skill severity:** three clean runs yield Excellent; one Quality No yields Stable; one Regression No without Critical yields Functional; any Critical No yields Broken. Two otherwise clean runs cannot hide the third-run failure.
- [ ] **Distinct scores:** pooled Quality 19/20 and Regression 12/12 with a Critical failure display 95%, 100%, failed Critical and Broken. The values are a synthetic acceptance example, never production results. Empty class denominators are unavailable; fewer than three audits cannot qualify.
- [ ] **Connected task:** draft plus related skills complete a real website task in a separate Servitor session with observed loading. Passing isolated text checks while breaking a related skill or the task outcome fails.
- [ ] **Scope separation:** skill Quality/Regression/Critical/grade results cannot overwrite historical r1 packets or certify whole-Workbench Alignment.


- [ ] **Cycle:** one failure reaches diagnosis, bounded repair, qualified comparison, disposition, authorized adoption and later-use evidence. Missing pins/retests fail.
- [x] **Historical r1 scoring:** pooled 8/10 + 1/2 + 1/2 = 10/14; empty has no score. Critical/Regression/missing-proof and level rules are tested.
- [ ] **Evals:** frozen contracts reject self-grading, do-nothing passes, static-only benefit, skipped permissions and below-noise gains.
- [ ] **Stops:** baseline excluded; fourth attempt, renamed/reset counter or omitted finding fails.
- [ ] **Readback:** S-006/S-007 preserve assessment/trial distinctions, failures and private-data boundaries; false storage claims fail.
- [ ] **Native evidence:** fresh real-tool execution proves required end state and loaded skill identity; a transcript alone fails Git/filesystem claims.
- [ ] **Worker evidence:** S-000B receipts preserve attempts; interruption cannot qualify an unrun check or restart stopped work.
- [ ] **Retention:** existing Fitness/Alignment checks establish Stable/Excellent, useful benefit and no regression. Original-case pass with regression fails; bundle gains cannot certify each skill.
- [ ] **Later use:** distinguish merge, authorized install, loading and outcomes. Recurrence is detected without owner prompting; stale loaded copies cannot count as repaired versions.

## Documentation Impact

LMK-004 owns the loop; Wiki routes capabilities. S-012 owns the lifecycle CLI; only missing inputs block consumers.

## Testing Seams

CLI/runner/writer/readback: missing proof, recurrence, original-pass/regression-fail. Checks: RUNBOOK; [proof](tasks/TK-000M/TASK.md).

## Review and Human QA

Independent review per retained change; owner judges automation.

## Completion Result

Pending.

## Feedback-loop planning boundary

Implementation and trials remain held; earlier approvals, attempts and stopped experiments retain scope. The [Wiki](../../../../wiki/context-feedback-improvement-loop-plan.md#current-mapped-destination) owns sourced continuation.
