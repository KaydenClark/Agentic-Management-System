# S-002 - RSI loop with safeguards

**Spec ID:** S-002
**Status:** active
**Priority:** 1
**Owner:** Kayden; orchestrator B (local)
**Stance:** Builder
**Updated:** 2026-11-02
**Catalog description:** Skill/AMS audit loop.
**Blockers:** none
**Confirmation:** [JOT-1871d72c-c1cf-4602-887c-3c996f26e086](../../../../wiki/context-active-spec-approvals.md)
**Execution approval:** [JOT-1871d72c-c1cf-4602-887c-3c996f26e086](../../../../wiki/context-active-spec-approvals.md)
**Latest event:** TK-001B second private-evidence correction failed independent cleanup-interruption review; repair STOPPED.
**Next gate:** Report001A/001B failures and await fresh user authorization; PR101 DRAFT/unmerged. No further repair, model/store calls or merge.

## Intent and authority

[Owner decisions](../../../../wiki/context-ams-purpose.md) govern resumed Journey: fixed r1/acceptance, attempts, meter and bounded versus whole scope.

## Current Verified State

[Scoring](tasks/TK-000M/TASK.md); [baseline](../../../../feedback/REPORT-rsi-baseline-2026-11-01.md): Broken 4/138, incomplete/unqualified; no trial, strike or skill result.

Exact-identity repair: S-006/TK-000S.

[Bootstrap](../../../../../evals/TRIALS.md) proves no trial, qualification or benefit. TK-000V repairs blocked prompt writes; TK-002 owns noise. Its reviewed engineering reference `921cb3e` (PR #92; CI87; 177 affected checks) freezes the [narrow protocol](../../../../../evals/INTERVIEW-NOISE.md). PR #92 merged at `d78b663`; the orchestrator selected main-contained source `921cb3e` after direct model-free import/protocol verification. The released qualification command was rejected by automatic approval review before process creation. The owner explicitly approved scoped Anthropic/subscribed-Claude sends on 2026-11-02. The first five-control qualification phase then executed once and all expected outcomes matched; the root inspected private evidence digest `f6938f3...` and accepted only that narrow qualification. The first baseline worker process completed, but its judge returned fenced JSON and the strict parser retained Unknown (`3a2637ba...`); task success is unestablished. Further model slots are held. The root released only publication of the old incomplete observation, now run28/result41 with exact readback below. Noise and benefit remain unproven. [TK-002](tasks/TK-002/TASK.md) owns the exact hold and preserved identities.

[TK-000Y](tasks/TK-000Y/TASK.md) completed only the bounded structured-output/neutral-context engineering correction at independently reviewed source `c3e1fd9`; private model-free recorde9c08d/protocol720869 binds unchanged semantic inputs and prior actual labels. Current/fresh/independent affected231/1skip and predecessor ed5 full local/fresh761/4skip are source-bound in its receipt; CI117 passed runtime-identical head489. PR101 checked delivery remains separate from root source selection and actual restricted-CLI compatibility/new qualification. Corrective model queries and additional store writes remain zero; old source921 evidence is unchanged.

PR101 remained held after later automated review proved halted private diagnostic metadata could be lost. [TK-001A](tasks/TK-001A/TASK.md) completed the native fresh correction for that narrow retention gap, verified by affected239/1skip, exactb9 CI120 and independent delta PASS; Y’s closed receipt and scoped PASS remain historical. No actual corrective query or extra database write occurred.

Later PR101 review proved actual adapter interruption and post-return drift still lost evidence; [TK-001B](tasks/TK-001B/TASK.md) owns the fresh second private-retention correction with actual-adapter integration tests and an explicit stop-on-repeated-failure rule. Earlier Y/001A source-specific receipts remain unchanged.

TK-001B stopped at source179 after independent review proved valid-terminal evidence is lost when finally-close is interrupted (proof1aaf62e...). Passing786/4skip full local/fresh suites and CI123 do not satisfy the failed requirement. Acceptance remains unmet; [the stopped checkpoint](tasks/TK-001B/TASK.md) records both correction attempts and the unexecuted next proposal. No new source was selected or actual corrective query/storage action released.

## Desired Behavior

Failure -> earliest gap/owner -> one repository change -> baseline/retest -> disposition/later use.

### Audit scores

Canonical: `audit-workbench` r1 checks/scenarios/qualification, version 1,
hash `96636d4a5e70cacbb0b94fd079340f02ed0f09b121b6498c1c70eebeb13b0578`.
Freeze rubric, scope/inventory/exclusions, IDs/classes, baseline/candidate/skill
pins, loaded artifacts, host/tools and evaluator model/prompt/qualification;
no changes/extra points.

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

`evals/` pins case/failure, prompt/fixtures/reset, permissions, end state,
grader/model/host/loaded skill. Cover invocation/near misses, valid/adverse input,
prerequisites/discovery/resume/authority. Map r1 IDs; no extra points.
Qualify good/bad/do-nothing cases; protect inputs/logs. Deterministic checks first;
semantic judges need separate context, exact model, owner-labelled cases, no worker
reasoning. Requalify model/prompt/rubric changes; manual trials until qualified.

Findings: ID/check/class, run/candidate/evidence, uncertain cause, owner/retest.
Close only on three-run repaired-revision original/affected-regression passes
(or justified regression exclusion). Merge/omission/score cannot close; retain recurrence/new failures.

## Decisions And Contracts

- Retain only qualified Stable/Excellent with demonstrated useful benefit
  predeclared before comparison. First case: grilling failure; coordinate existing redesign.
- Failure-led rounds; review ineffective prior fixes on recurrence. One change/version.
- Fixed provider/model/effort. Accepted-version runner/graders/scoring, never
  candidate-owned. Grader changes start a new series judged by its predecessor.
- Same-version noise floor first. Fixed-task AMS/no-AMS/plain-instruction arms,
  three trials each; predeclared effect/margin, paired per-task intervals.
  Inside-margin is inconclusive; audit delta proves no benefit.
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

S-006 retains assessment/attempt/run identities, metadata, ledgers, counts/levels, acceptance/evidence/qualification and finding/retest/behavior links. S-007 safe presentation is pending.

Keep real build/skill seeds strength-labelled; private sources yield summaries/commits only. Require storage and qualified comparisons.

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
| 2026-11-02 | TK-000Y | Task closed | Engineering source c3e1fd9: primary/fresh/independent 231 passed/1 skipped; predecessor ed5 local/fresh full761 passed/4 skipped; current room/layout/render/diff checks; direct scoped independent source/binding PASS; CI117 passed exact489 runtime-identical head; model-free recorde9c08d/protocol720869 releasedfalse. | evals/INTERVIEW-NOISE.md; TK-000Y; S-002; TASKBOARD | Only bounded serialization/neutral-context engineering is complete. Actual restricted CLI compatibility and changed-source qualification are unverified/unreleased; TK-002 and floor remain incomplete. Old run28/result41 and original campaign evidence preserved; corrective model/store calls0. Current final-record CI and checked PR101 main delivery pending.; close attribution: {"agent":"s002-structured-judge","claimant":"s002-structured-judge","onBehalfOf":null} |
| 2026-11-02 | TK-001A | Task closed | Sourceb9 primary/fresh/independent239 passed/1 skipped; eight causal private journal/stop/privacy cases; current room/layout/render/diff checks; exactb9 CI120 passed; code review no findings/security completed; scoped independent delta PASS; unreleased record18e47/protocol48c882. | TK-001A; S-002; TASKBOARD; INTERVIEW-NOISE context | Bounded private halt-retention correction complete only. Actual structured-output compatibility/new qualification remain unverified/unreleased; TK-002 and floor incomplete, original stoppedrun28/result41 unchanged. Final records CI/reviews and checked PR101 main delivery pending. Corrective model/store calls0.; close attribution: {"agent":"s002-halt-evidence","claimant":"s002-halt-evidence","onBehalfOf":null} |

## Old incomplete baseline publication

A first storage request was also rejected before process creation for alleged missing Supabase destination authority; no key/HTTP/row action occurred. The exact original owner message `01a197f8-ec2b-72c0-9db7-4712043972d4` was then directly recovered: “log the results in supabase.” One reconsideration of the same safe payload cleared review; no workaround or destination change occurred.

Released old observation only: stopped/incomplete run **28**, Unknown result **41** (`passed:null`, `workerCompleted:true`, grader `runner_error`, strength `single_trial`). Exact readback digest `68a1512b25d62903df21e1080f2a635658b2fc489e8bdc902d2cf58d25de57c7`; validated safe payload `77674f9676b6bb16bbe0d0a2c35eff391784398a53394cc46829b91daab3b45a`. Historical start/finish use explicitly labelled journal filesystem mtimes; database recorded_at is publication time. Public wall seconds `23.362` follows numeric(12,3); the exact raw measurement stays private. Actual spend remains null with evidence source. A separate trusted publisher loaded only the safe payload and explicit local key; no raw transcript/host path/skill/rationale or credential was exposed. No other rows, source changes or model calls occurred. One ungraded row cannot establish a noise floor or complete TK-002.

## Review and Human QA

Independent review per retained change; owner judges automation.

## Completion Result

Pending.
