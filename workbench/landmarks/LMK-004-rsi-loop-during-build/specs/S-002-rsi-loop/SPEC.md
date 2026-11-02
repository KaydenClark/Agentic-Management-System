# S-002 - RSI loop with safeguards

**Spec ID:** S-002
**Status:** active
**Priority:** 1
**Owner:** Kayden; orchestrator B (local)
**Stance:** Builder
**Updated:** 2026-11-01
**Catalog description:** Skill/AMS audit loop.
**Blockers:** none
**Confirmation:** [JOT-1871d72c-c1cf-4602-887c-3c996f26e086](../../../../wiki/context-active-spec-approvals.md)
**Execution approval:** [JOT-1871d72c-c1cf-4602-887c-3c996f26e086](../../../../wiki/context-active-spec-approvals.md)
**Latest event:** TK-002 narrow qualification accepted; first baseline slot held as Unknown on strict judge-format failure.
**Next gate:** TK-000Y bounded structured-output correction; no further model calls or additional trial-store rows are released.

## Intent and authority

[Owner decisions](../../../../wiki/context-ams-purpose.md) govern resumed Journey: fixed r1/acceptance, attempts, meter and bounded versus whole scope.

## Current Verified State

Met: **Scoring** ([TK-000M receipt](tasks/TK-000M/TASK.md#receipt)). Open: Cycle, Evals, Stops, Readback.

[Baseline](../../../../feedback/REPORT-rsi-baseline-2026-11-01.md): Broken 4/138, incomplete/unqualified; no trial, strike or skill result.

Exact-identity repair: S-006/TK-000S.

[Bootstrap](../../../../../evals/TRIALS.md) proves no trial, qualification or benefit. [TK-002](tasks/TK-002/TASK.md) owns noise state and exact identities under the [narrow protocol](../../../../../evals/INTERVIEW-NOISE.md): narrow qualification is accepted; baseline slot 0 is Unknown; later slots wait on TK-000Y's judge correction. Only old run28/result41 is [published](tasks/TK-002/TASK.md#old-incomplete-baseline-publication). Noise and benefit remain unproven.

History: [S-002 history](../../../../wiki/history/S-002.md).

## Desired Behavior

Failure -> earliest gap/owner -> one repository change -> baseline/retest -> disposition/later use.

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
- Fixed provider/model/effort. Accepted-version runner/graders/scoring, never
  candidate-owned. Grader changes start a new series judged by its predecessor.
- Same-version noise floor first, then r1 paired trials: fixed-task
  AMS/no-AMS/plain-instruction arms, paired per-task intervals. Audit delta proves no benefit.
- Public lift needs >2 fresh held-out tasks, controls, baseline/interval.
  Studied cases retire to dev; scores are not lift.
- Sandbox without skipped permissions. Automatic proposing waits for a trusted
  grader, measured cost and owner-judged manual round.
- Baseline 0: no strike. Candidate initial -> retry -> retry -> stop/report unless
  accepted. Repair/rename never resets; retain failures/harm.
- Trial rows: task/arm, version/skills pin, provider/model/effort, completion,
  cost/tokens availability, source. Subscription meter; unknown is not zero.

## Non-Goals

Weights; running loops during mapping; presentation (S-007).

## Dependencies And Blockers

S-006 retains assessment/attempt/run identities, metadata, ledgers, levels, acceptance/evidence/qualification and finding/retest/behavior links; S-007 safe presentation is pending. Strength-label real seeds; private sources yield summaries/commits only. Require storage and qualified comparisons.

## Vertical Implementation Slices

TK-000M/N/O: scoring; TK-000T/V: bootstrap; TK-001..004: trials. B local; checked PRs to main.

## Acceptance Criteria

- [ ] **Cycle:** failure -> change -> three-run score -> retest/disposition/later use; reject missing pin/retest.
- [x] **Scoring:** Pool `8/10 + 1/2 + 1/2 = 10/14`; empty: no score. Test all levels, Quality No, Critical/Regression/missing proof. Reject Broken acceptance and bounded-as-whole.
- [ ] **Evals:** enforce comparison contracts; reject do-nothing passes, self-grading, anecdotal/static benefit, skipped permissions/below-floor lift.
- [ ] **Stops:** omitted findings stay open; regressions visible; baseline excluded. Reject fourth attempt/reset.
- [ ] **Readback:** S-006/S-007 retain assessment/trial distinctions and failures/evidence. Reject false storage or test/private-data publication.

## Testing Seams

CLI/runner/writer/readback: missing proof, recurrence, original-pass/regression-fail. Checks: RUNBOOK; [proof](tasks/TK-000M/TASK.md).

## Review and Human QA

Independent review per retained change; owner judges automation.

## Completion Result

Pending.
