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

[Scoring](tasks/TK-000M/TASK.md); [baseline](../../../../feedback/REPORT-rsi-baseline-2026-11-01.md): Broken 4/138, incomplete/unqualified; no trial, strike or skill result.

Exact-identity repair: S-006/TK-000S.

TK-000V repairs blocked prompt writes; [bootstrap](../../../../../evals/TRIALS.md) proves no trial, qualification or benefit. [TK-002](tasks/TK-002/TASK.md) owns noise state and exact identities under the [narrow protocol](../../../../../evals/INTERVIEW-NOISE.md): narrow qualification is accepted; baseline slot 0 stayed Unknown; later slots wait on TK-000Y's judge correction. Only old run28/result41 is [published](tasks/TK-002/TASK.md#old-incomplete-baseline-publication). Noise and benefit remain unproven.

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

## Append-Only Evidence And Execution Log

| Date | Task | Event | Verification | Docs | Remaining gap |
|---|---|---|---|---|---|
| 2026-11-01 | none | Mapped as planned | render, doctor | this Spec | Every criterion; campaign approval |
| 2026-11-01 | none | Owner requested Loop #1 preparation and the first improvement wave, with fitness/alignment results, Stable/Excellent-only acceptance and a three-attempt stop. Captured source and interview frontier in the linked RSI context. | Read-only Supabase counts; dev source and READY deployment metadata inspected | Current Verified State; existing RSI context | Exact baseline pins; remaining design answers; Supabase-to-site reader and actual trials |

| 2026-11-01 | baseline | Main a3d014e, attempt 0 | 4/138, Broken; incomplete/unqualified | Linked baseline report | Candidate scope; behavioral proof; storage/dev reader |

### Interview correction, 2026-11-01

Kayden reported lost grilling as a failure; the linked context preserves the interview correction.
| 2026-11-01 | TK-000M | Task closed | 36 focused; 427 suite/4 skip; QA/reviews in Task | RUNBOOK; evals; Wiki | S-006 and real trials remain; close attribution: {"agent":"codex-s002","claimant":"codex-s002","onBehalfOf":null} |
| 2026-11-01 | TK-000N | Task closed | 40 focused; fresh 431/4 skip; CI #32 pass | evals | S-006/trials; close attribution: {"agent":"codex-s002","claimant":"codex-s002","onBehalfOf":null} |
| 2026-11-01 | TK-000O | Task closed | 42 focused; CI #38 pass | evals | S-006/trials; close attribution: {"agent":"codex-s002","claimant":"codex-s002","onBehalfOf":null} |
| 2026-11-01 | TK-000T | Task closed | 45 focused; fresh 562/4 skip; CI70; actual adapter smoke | evals, Runbook, Wiki | Oracle calibration, noise, controls, benefit; close attribution: {"agent":"s002-bootstrap","claimant":"s002-bootstrap","onBehalfOf":null} |
| 2026-11-01 | TK-000V | Task closed | 50 focused; fresh 567/4 skip; actual inert adapter | evals/TRIALS.md | Oracle/noise/controls/benefit; close attribution: {"agent":"s002-transport","claimant":"s002-transport","onBehalfOf":null} |

## Review and Human QA

Independent review per retained change; owner judges automation.

## Completion Result

Pending.
