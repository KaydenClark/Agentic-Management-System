# S-002 - RSI evaluation and qualification

**Spec ID:** S-002
**Status:** active
**Priority:** 1
**Owner:** Kayden; orchestrator B (local)
**Stance:** Builder
**Updated:** 2026-11-07
**Catalog description:** RSI case contracts, qualification and regression evidence.
**Blockers:** none
**Confirmation:** [JOT-1871d72c-c1cf-4602-887c-3c996f26e086](../../../../wiki/context-active-spec-approvals.md)
**Execution approval:** [JOT-1871d72c-c1cf-4602-887c-3c996f26e086](../../../../wiki/context-active-spec-approvals.md)
**Next gate:** TK-000Y bounded structured-output correction; no further model calls or additional trial-store rows are released.

## Intent and authority

[Current destination](../../../../wiki/context-feedback-improvement-loop-plan.md#jot-7862917b-48cb-41bc-8f21-0ddfc611cdac): optional Servitor loop, Map only. Prior attempts, meter rules, frozen comparisons and holds remain; no trials released.

## Current Verified State

Historical r1 scoring is met ([TK-000M](tasks/TK-000M/TASK.md#receipt)); new skill severity/separate scores and cycle acceptance remain open. [Baseline](../../../../feedback/REPORT-rsi-baseline-2026-11-01.md): Broken 4/138, unqualified, no strike; S-006/TK-000S owns identity. TK-002’s baseline is Unknown; later slots wait for TK-000Y. Only stopped run28/result41 is published, not benefit. [History](../../../../wiki/history/S-002.md) retains evidence.

## Desired Behavior

LMK-004: failure → cause → repair → comparison → disposition → later use. S-000B executes, S-006 stores, S-013 detects, S-011 delivers.

Evaluate skills/bundles without inferring component gains. Diagnose method, instruction, tool, environment, context, ownership, coordination, proof or model causes; preserve unknowns and route defects to their Specs. Pin outcomes/baseline/loaded version/tools/end state. Separate development/selection from fresh confirmation; studied cases retire to development. Controls retain authority/safety instructions.

Record routing/invocation per host, eligible successes/failures, interventions and recurrence; unknown denominators stay unknown. Require native filesystem/Git proof. Transcripts, screening, brevity or audit gains alone prove no benefit. Preserve historical/prior-pass/cross-skill regressions.

### Audit scores

Shared questions/whole-Workbench rubric: audit-workbench r1 v1, hash `96636d4a5e70cacbb0b94fd079340f02ed0f09b121b6498c1c70eebeb13b0578`. Freeze rubric/scope/IDs, source pins, loaded artifacts, host/tools and evaluator/model/prompt/qualification. Whole-Workbench Alignment retains its own r1 rules; [assessments](../../../../../evals/ASSESSMENTS.md) describe current code.

Three skill audits report separate Quality and Regression scores: each pools `100 × Yes / applicable` within its class. Shared Alignment questions supply Quality; skill-specific tests cover regressions and connected workflows. Critical results remain separate, not double-counted in either percentage. No applicable checks means unavailable, not 100%; preserve per-run counts, evidence and justified N/A. Missing, unknown, refused or interrupted evidence remains No in its class and denominator; no rounding or invented proof.

Worst failure across all three runs sets the skill grade: Excellent = none; Stable = Quality only; Functional = Regression without Critical; Broken = any Critical. Skipping an explicitly requested skill is a Critical failed requested use even if never loaded. Incomplete audits cannot qualify or establish Excellent. Grade, acceptance, Human QA, distribution and benefit remain distinct; bounded results cannot certify whole-Workbench Alignment. Current code uses the older passing-run-count grade: new skill scoring must preserve historical packets and whole-Workbench semantics.

### Evals and retests

Git cases pin fixtures/permissions/end state/grader/model/host/skill/r1 IDs. Cover invocation, near misses, adverse input, prerequisites, discovery, resume and authority. Qualify judges with good/bad/do-nothing controls; protect evidence and use manual trials until qualified. Close findings only after three repaired-revision original/regression retests; retain recurrence/new failures.

## Decisions And Contracts

- Retain qualified Stable/Excellent only with predeclared useful benefit and no regression. First proof: real AMS website work on Servitor; Plan selects the case and coordinates existing work. Earlier grilling fixtures/attempts stay frozen.
- Failure-led rounds review ineffective fixes on recurrence; one change/version.
- Codex/Claude subscription meters; Mid/Small default, High with reason. Freeze provider/model/effort within comparisons and retain old pins. Accepted-version runner/graders/scoring stay candidate-independent; grader changes start a new series judged by the predecessor.
- Same-version noise floor precedes paired AMS/no-AMS/plain-instruction trials with per-task intervals. Audit delta is not benefit. Public lift requires more than two fresh held-out tasks, controls, baseline/interval; studied cases retire to development.
- No skipped sandbox permissions. Automatic proposing waits for trusted grading, recorded capacity and owner-judged manual round.
- Baseline consumes no attempt; initial → retry → retry → stop/report unless accepted. Repair/rename resets nothing; retain failures/harm.
- Rows retain task/arm, version/skills pin, model/provider/effort, completion, cost/token availability and source. Unknown subscription usage is not zero.

## Non-Goals

Weights; running loops during mapping; presentation (S-007).

## Dependencies And Blockers

S-000B executes; S-006 stores evidence; S-007 presents safe results. Only missing inputs block consumers.

## Vertical Implementation Slices

[TK-002Q case contract](../../../../wiki/guidebooks/rsi-case-contract.md).

## Acceptance Criteria

- [ ] **Severity:** three clean audits = Excellent; Quality-only No = Stable; Regression without Critical = Functional; any Critical = Broken. A third-run failure cannot disappear behind two clean runs.
- [ ] **Distinct scores:** synthetic pooled Quality 19/20, Regression 12/12 and one Critical failure display 95%, 100%, failed Critical and Broken. Never publish this example as live evidence. Empty denominators are unavailable; fewer than three audits cannot qualify.
- [ ] **Connected task:** draft and related skills complete a real website task in a separate Servitor session with verified loaded identity/end state. Isolated text success with workflow damage fails.
- [ ] **Scope:** new skill results neither overwrite historical r1 packets nor certify whole-Workbench Alignment.
- [ ] **Cycle:** failure → diagnosis → repair → qualified comparison → disposition → authorized adoption → later use. Missing pins/retests, stale loading or source merge alone fail.
- [x] **Historical r1 scoring:** tested pooled 8/10 + 1/2 + 1/2 = 10/14, empty/no-score and Critical/Regression/missing-proof/level rules.
- [ ] **Evals:** reject self-grading, do-nothing passes, static-only benefit, skipped permissions and below-noise gains.
- [ ] **Stops/recovery:** exclude baseline; reject fourth attempts, renamed/reset counters, omitted findings, unrun-check passes or restarted stopped work.
- [ ] **Readback:** S-006/S-007 preserve assessment/trial distinctions, failures and privacy; false storage claims fail.
- [ ] **Retention/recurrence:** qualified Stable/Excellent, useful benefit and no regression; original-pass/regression-fail cannot qualify. Bundle gains certify no component. Detect recurrence without owner prompting and distinguish accepted source, installation and actual loading.

## Documentation Impact

LMK-004/Wiki route owners; S-012 owns the general CLI.

## Testing Seams

CLI/runner/writer/readback: missing proof, recurrence, original-pass/regression-fail. Checks: RUNBOOK; [proof](tasks/TK-000M/TASK.md).

## Review and Human QA

Independent review per retained change; owner judges automation.

## Completion Result

Pending.
