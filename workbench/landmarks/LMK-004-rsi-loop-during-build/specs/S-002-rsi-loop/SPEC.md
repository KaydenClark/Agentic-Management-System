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
**Latest event:** TK-000O claimed by codex-s002.
**Next gate:** Close TK-000O with verification and documentation proof.

## Intent and authority

[Owner decisions/resume](../../../../wiki/context-ams-purpose.md): JOT-4fa672e3 resumes Journey. r1; Stable/Excellent; three attempts excluding baseline; subscription meter; bounded candidate/regressions separate from whole AMS.

## Outcome

Pinned baselines, scores, evals, retests and dispositions.

## Why It Matters

Build, then loop until meter/stop. Static scores prove no benefit.

## Current Verified State

[Local CLI proof](tasks/TK-000M/TASK.md); runner/trials/storage incomplete. [Main a3d014e baseline](../../../../feedback/REPORT-rsi-baseline-2026-11-01.md): Broken, 4/138, incomplete/unqualified; reviews, no strike/skill result.

## Desired Behavior

Failure -> earliest gap/owner -> one change in its repository -> baseline/retest -> disposition/later use.

### Audit scores

Canonical method: `audit-workbench` r1 checks/scenarios/qualification, version 1,
hash `96636d4a5e70cacbb0b94fd079340f02ed0f09b121b6498c1c70eebeb13b0578`.
Freeze rubric, scope/inventory/exclusions, IDs/classes, baseline/candidate/skills
commits, loaded artifacts, host/tools, evaluator model/prompt/qualification.
No extra points or rubric changes.

Three runs/attempt: class, Yes/No/justified N/A, typed revision-bound
evidence/qualification. Missing/Unknown/refused/interrupted stays No in its class
and denominator. Label static/unqualified proof. Pool exact counts:
`100 × Yes / applicable`; no weights/partial credit/rounding; empty means no percentage.

Run pass: all Critical/Regression Yes; Regression needs baseline pass proof.
3/2/1/0 passing runs = Excellent/Stable/Functional/Broken; Critical No overrides
Broken. Acceptance additionally requires complete qualified proof and no open
Critical/Regression or unmapped historical finding. No QA/distribution/benefit
implied. Whole fitness covers ten areas; bounded results cannot certify AMS.

### Skill evals and retests

`evals/` pins case/failure, prompt/fixtures/reset, permissions, end state and
grader/model/host/loaded skill. Cover invocation/near misses, valid/adverse input,
prerequisites/discovery/resume/authority. Map r1 IDs without extra points.
Qualify good/bad/do-nothing cases; protect inputs/logs. Deterministic checks first;
semantic judges need separate context, exact model, owner-labelled cases, no worker
reasoning. Requalify model/prompt/rubric changes; manual trials until qualified.

Findings retain ID/check/class, run/candidate/evidence, uncertain cause, owner/retest.
Close only on three-run repaired-revision original/affected-regression passes
(or justified regression exclusion). Merge/omission/score cannot close; retain recurrence/new failures.

## Decisions And Contracts

- Retain only qualified Stable/Excellent with demonstrated useful benefit
  predeclared before comparison. First case: grilling failure; coordinate existing redesign.
- Rounds start from failures, never retro ideas. On recurrence check ineffective
  prior fixes. One change/version.
- Fixed provider/model/effort. Accepted-version runner/graders/scoring, never
  candidate-owned. Grader changes start a new series judged by its predecessor.
- Same-version noise floor first. Fixed-task AMS/no-AMS/plain-instruction arms,
  three trials each; predeclared effect/margin, paired per-task intervals.
  Inside-margin is inconclusive; audit delta proves no benefit.
- Public lift needs >2 fresh held-out tasks, controls, baseline/interval.
  Studied cases retire to dev; scores are not lift.
- Sandbox, no skipped permissions. No automatic proposer before trusted grader,
  measured trial cost and owner-judged manual round.
- Baseline 0: no strike. Candidate initial -> retry -> retry -> stop/report unless
  accepted. Repair/rename never resets; retain failures/harm.
- Trial rows: task/arm, version/skills pin, provider/model/effort, completion,
  cost/tokens availability, source. Subscription meter; unknown is not zero.

## Non-Goals

Model weights; loop execution during mapping; presentation (S-007).

## Dependencies And Blockers

S-006 must retain assessment/attempt/run IDs, frozen metadata, check ledgers, counts/levels, acceptance/evidence/qualification, findings/retests and behavioral links. S-007 presents scores/evals/failures/provenance. Integration missing; reviews are not trials.

Real build-history/skills seeds, strength labels; private summary/commit only. Storage/qualified comparisons required.

## Vertical Implementation Slices

TK-000M/N: local CLI/recovery only. Trial Tasks retain real inputs. B local; checked PRs to main.

| Task | Slice | Status | Blockers | Proof |
|---|---|---|---|---|

## Acceptance Criteria

- [ ] **Cycle:** skill failure -> change -> three-run score -> retest/disposition/later use. Reject missing pin/retest.
- [ ] **Scoring:** `8/10 + 1/2 + 1/2 = 10/14`; empty set has no score. Test all levels, Quality-only No, Critical/Regression/missing proof. Reject Broken acceptance or bounded-as-whole claims.
- [ ] **Evals:** enforce comparison contracts; reject do-nothing passes, self-grading, anecdotal/static benefit, skipped permissions/below-floor lift.
- [ ] **Stops:** omitted findings stay open; regressions visible; baseline excluded. Reject fourth attempt/reset.
- [ ] **Readback:** S-006/S-007 retain assessment/trial distinctions, failures/evidence links. Reject false storage claims or test/private-data publication.

## RSI and website connection

See dependencies.

## Testing Seams

CLI/runner/writer/readback fixtures: missing proof, recurrence, original-pass/regression-fail.

## Verification Procedure

RUNBOOK; [Task proof](tasks/TK-000M/TASK.md).

## Documentation Impact

RUNBOOK, S-006/S-007, Wiki/Tasks.

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

## Review and Human QA

Independent review per retained change; owner judges manual-round automation.

## Completion Result

Pending.

## Remaining Limitations Or Follow-Up Specs

- Qualify the manual loop before using it in force.

## Supersession

- Supersedes: none
- Superseded by: none
