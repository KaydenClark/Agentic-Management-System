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
**Latest event:** TK-000M claimed by codex-s002.
**Next gate:** Close TK-000M with verification and documentation proof.

## Intent and authority

[Owner answers](../../../../wiki/context-ams-purpose.md): r1, Stable/Excellent, three attempts excluding baseline, paid-plan meter. The earlier JOT-5061e624-c5c2-421d-aae1-58b01a25a03c requested only Spec repair. [Owner resume](../../../../wiki/context-ams-purpose.md#jot-4fa672e3-ed35-4aee-9364-902039ce4b81) now requests S-002 Journey; retain the subscription meter and bounded-candidate/whole-AMS distinction.

## Outcome

Skill/AMS changes have pinned baselines, fitness/alignment scores, behavioral evals, retests and dispositions.

## Why It Matters

Build first, then loop until meter/stop. Static scores prove no benefit.

## Current Verified State

Runner/evals/storage reader incomplete. [Main a3d014e baseline](../../../../feedback/REPORT-rsi-baseline-2026-11-01.md): Broken, 4/138, incomplete/unqualified; reviews, no strike/skill result.

## Desired Behavior

Failed audit -> earliest gap/owner -> one hypothesis/change -> baseline comparison/retests -> retain, revise (variant) or remove -> record/later use. Owners repair through their repositories.

### Audit scores

Use `audit-workbench` Alignment Check r1, check version 1, hash `96636d4a5e70cacbb0b94fd079340f02ed0f09b121b6498c1c70eebeb13b0578`; its checks/scenarios/qualification remain canonical. Freeze rubric, scope/inventory/exclusions, IDs/classes, baseline/candidate/skills commits, loaded artifacts, host/tools and evaluator model/prompt/qualification. No extra points/rubric changes.

Three runs per attempt. Each check keeps Yes/No/justified N/A, class, typed revision-bound evidence/qualification. Missing proof, Unknown, refusal/interruption stay No in original class/denominator. Justify N/A; label static/unqualified proof.

Score = `100 × pooled Yes / pooled applicable`; keep exact counts/ratio, no weights/partial credit/rounding default. Empty set has no percentage. Run pass requires all Critical/Regression checks; Regression needs baseline pass proof. 3/2/1/0 passing runs = Excellent/Stable/Functional/Broken; any Critical failure overrides to Broken.

Separate level/score, acceptance, evidence and qualification. Pass only Stable/Excellent with complete proof, no open Critical/Regression or unmapped historical finding. No QA/distribution/benefit implied. Whole fitness covers ten areas; bounded scores cannot certify AMS. Candidate and whole-AMS scores remain separate, per the owner answers in the Wiki.

### Skill evals and retests

Use `evals/` templates: versioned case/failure, prompt/fixtures/reset, permissions, end state, grader/model/host/loaded skill pin. Cover invocation/near misses, valid/adverse input, prerequisites/discovery/resume/authority. Map r1 IDs; extra criteria add no points.

Qualify with good/bad/do-nothing cases; protect inputs/logs. Prefer deterministic checks; semantic judges: separate context, exact model, owner-labelled cases, no worker reasoning. Requalify model/prompt/rubric changes; manual trials until runner qualified.

Findings: ID/check/class, run/candidate/evidence, uncertain cause, owner/retest. Close only on repaired-revision original/affected-regression passes in three runs (or justified regression exclusion). Merge/omission/score cannot close; keep new failures/recurrence.

## Decisions And Contracts

- Retain only qualified Stable/Excellent candidates with demonstrated useful benefit declared before comparison. First case: the grilling failure; coordinate with the owner-reported redesign already underway.

- Failed results start rounds, never retro ideas; check earlier ineffective fixes on recurrence. One change/version.
- Fixed provider/model/effort; accepted-version runner/graders/scoring, never candidate. Grader changes start new series, judged by predecessor.
- Same-version noise floor first; fixed-task AMS/no-AMS/plain-instruction arms, three trials each; predeclared effect/margin, per-task paired intervals. Inside-margin is inconclusive; audit delta proves no benefit.
- Public lift requires >2 fresh held-out tasks, controls, baseline/interval. Studied cases retire to dev; audit scores are not lift.
- Sandbox without skipped permissions. No automated proposer before trusted grader, measured trial cost and owner-judged manual round.
- Baseline 0 consumes no strike. Candidate: initial -> retry -> retry -> stop/report unless accepted. Repair/rename never resets; retain failures/harm.
- Trial rows: task/arm, version/skills pin, provider/model/effort, completion, cost/tokens availability, source. Paid-plan meter; unknown is not zero.

## Non-Goals

Model weights; loop execution during mapping; presentation (S-007).

## Dependencies And Blockers

S-006 must retain assessment/attempt/run IDs, frozen metadata, check ledgers, counts/levels, acceptance/evidence/qualification, findings/retests and behavioral-row links; S-007 shows scores/evals/failures with provenance. Integration gaps remain; reviews are not trials.

Seeds: real build-history/skills sources, strength-labelled; private skills summary/commit pointer only. TK-002 uses the existing subscription meter; no API campaign budget. Actual storage input and qualified comparison prerequisites remain.

## Vertical Implementation Slices

Existing trial Tasks retain their storage/comparison dependencies. TK-000M independently delivers local assessment intake, scoring, retest and stop safeguards through the CLI; it supplies no trial or storage acceptance. B local, checked PRs to main; evals/runner/writer/queries.

| Task | Slice | Status | Blockers | Proof |
|---|---|---|---|---|

## Acceptance Criteria

- [ ] **Cycle:** skill failure -> change -> three-run score -> retest/disposition/later use. Reject missing pin/retest.
- [ ] **Scoring:** `8/10 + 1/2 + 1/2 = 10/14`; empty set has no score. Test all levels, Quality-only No, Critical/Regression/missing proof. Reject Broken acceptance or bounded-as-whole claims.
- [ ] **Evals:** enforce comparison contracts; reject do-nothing passes, self-grading, anecdotal/static benefit, skipped permissions/below-floor lift.
- [ ] **Stops:** omitted findings stay open; regressions visible; baseline excluded. Reject fourth attempt/reset.
- [ ] **Readback:** S-006/S-007 retain assessment/trial distinctions, failures/evidence links. Reject false storage claims or test/private-data publication.

## RSI and website connection

S-006 stores; S-007 presents.

## Testing Seams

Scoring/finding fixtures; runner known outcomes; writer/readback/render. Include missing proof, recurrence and original-pass/regression-fail.

## Verification Procedure

`node workbench/tools/spec-workbench.mjs show S-002`; planning names runner/tests.

## Documentation Impact

RUNBOOK; S-006/S-007; Wiki/Tasks.

## Append-Only Evidence And Execution Log

| Date | Task | Event | Verification | Docs | Remaining gap |
|---|---|---|---|---|---|
| 2026-11-01 | none | Mapped as planned | render, doctor | this Spec | Every criterion; campaign approval |
| 2026-11-01 | none | Owner requested Loop #1 preparation and the first improvement wave, with fitness/alignment results, Stable/Excellent-only acceptance and a three-attempt stop. Captured source and interview frontier in the linked RSI context. | Read-only Supabase counts; dev source and READY deployment metadata inspected | Current Verified State; existing RSI context | Exact baseline pins; remaining design answers; Supabase-to-site reader and actual trials |

| 2026-11-01 | baseline | Main a3d014e, attempt 0 | 4/138, Broken; incomplete/unqualified | Linked baseline report | Candidate scope; behavioral proof; storage/dev reader |

### Interview correction, 2026-11-01

Kayden reported the lost grilling flow as a failure. Resume the ready decision round and wait; the linked context preserves his corrections.

## Review and Human QA

Each retained change gets independent review; the owner judges whether a manual round is worth automating.

## Completion Result

Pending.

## Remaining Limitations Or Follow-Up Specs

- The retro improvement loop needs its own improvement before it is used in force.

## Supersession

- Supersedes: none
- Superseded by: none
