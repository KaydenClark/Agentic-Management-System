# AMS failure log

This is the single canonical Markdown log for **every AMS failure**: model/skill
execution, coordination, tooling, tests, environment, delivery and owner-reported
failures. Record failures here even when a Task, trial ledger or detailed report
also records evidence. Supporting artifacts link here; they are not alternative
failure intake locations. Expected TDD red controls are test evidence, not failed
candidate attempts; unexpected verification failures and failed retries belong here.

Source: Kayden's AMS chat, 2026-11-03: every failure belongs in the same Markdown
file, with the model tier, provider, what it was doing and the correct outcome,
so the evidence can guide skill repairs. This supersedes the harness-only scope.

## Recording rules

- Append a stable `FAIL-NNN` row when a failure is observed, before handback or
  dependent repair. No separate service or new incident report is required.
- Record the **failed actor**, not the reporting/reviewing agent: tier
  (`Frontier`, `High`, `Mid`, `Small`), provider (e.g. OpenAI/Anthropic), exact model
  and harness when known. Separate requested from actual configuration. Use
  `unknown` with the missing-evidence reason; `not-applicable` only when no model
  was involved. A Codex host alone does not prove the model or provider.
- Name the activity and skill/copy/revision when known, actual failure and impact,
  and an observable correct outcome derived from the request or contract. Link
  source, candidate/attempt, owner and disposition. Do not infer skill causation
  from an agent mistake, environmental refusal or missing evidence.
- Log each failed retry/recurrence as a new row linked to its earlier ID; keep
  original outcomes. Append corrections or repair evidence referencing the ID;
  never erase a failure or turn a later pass into a passed earlier attempt.
- Diagnosis, repair and baseline/candidate/later-use evidence link back to these
  IDs. A proposal, merge or static score alone cannot close a failure or prove
  improvement. Follow the existing RSI qualification and installation authority.
- Publish safe summaries only; keep secrets, raw private traces and host paths out.

Copy this row, filling every field (escape literal pipes inside cells):

| ID | Date | Tier | Provider | Model / harness | Activity / skill | Failure / impact | Correct outcome | Evidence / owner / disposition |
|---|---|---|---|---|---|---|---|---|
| FAIL-NNN | YYYY-MM-DD | unknown — reason | unknown — reason | unknown — reason | Task and skill revision, if known | Observed result | Observable expected result | Source; candidate/attempt; owning Spec/Task or unknown; pending/diagnostic/test/repaired/declined/accepted-open |

## Recorded failures

The first18 rows normalize the previous log in its original order, summarizing
its activity, observed result, impact and historical status. Original wording and
proposed remedies remain in this file at `8b09ae4` and the linked reports.
Historical statuses below are observations at capture, not fresh repair judgments.
Model metadata absent from the original evidence remains unknown. Multi-finding
historical summaries retain their source granularity; newly recorded attempts
must be separate. This migration does not claim an exhaustive audit of every
historical trial, coherence finding or private trace.

| ID | Date | Tier | Provider | Model / harness | Activity / skill | Failure / impact | Correct outcome | Evidence / owner / disposition |
|---|---|---|---|---|---|---|---|---|
| FAIL-001 | 2026-11-01 | unknown | unknown | unknown | setup-workbench Adopt / budgets | Adopted controls and package AGENTS exceed budget; fidelity divergences remain without doctor enforcement. | Adopt controls within budgets without losing required guidance; detect excess before delivery. | Original log at `8b09ae4`; historical status: open |
| FAIL-002 | 2026-11-01 | unknown | unknown | unknown | setup-workbench Adopt / migration preflight | Migration refused sessions-not-ignored; extra reconciliation needed because scaffold ignore hid lane files. | Preflight the actual ignore rules and migrate without an avoidable refusal. | Original log at `8b09ae4`; historical status: open |
| FAIL-003 | 2026-11-01 | unknown | unknown | unknown | Wiki validation / scaffold templates | Wiki templates failed validation with30 invalid-note errors and were retired to archive. | Keep templates outside validated articles or support their declared format. | Original log at `8b09ae4`; historical status: open |
| FAIL-004 | 2026-11-01 | unknown | unknown | unknown | Adopt / host settings | Host refused settings write as self-modification; permission-scope-drift remained. | Identify the host permission boundary before attempting the settings edit. | Original log at `8b09ae4`; historical status: open |
| FAIL-005 | 2026-11-01 | unknown | unknown | unknown | specs / TASK-TEMPLATE.md | T-NNN template disagreed with runtime tasks/TK-###; ported records would not be backed by tooling. | Use one Task naming convention supported by templates and runtime. | Original log at `8b09ae4`; historical status: open |
| FAIL-006 | 2026-11-01 | unknown | unknown | unknown | Adopt / branches | Manifest cannot declare a separate dev deployment branch; delivery policy needs another owner. | Declare and recover the separate deployment route consistently. | Original log at `8b09ae4`; historical status: open |
| FAIL-007 | 2026-11-01 | unknown | unknown | unknown | Coherence sweep (S-013) | First sweep found contradictions, bundled decisions, missing mappings, unenforced budgets and lifecycle/doctor disagreement (COH-001–018). | Controls and lifecycle checks agree; every owner item remains traceable. | [COHERENCE-2026-11-01](coherence/COHERENCE-2026-11-01.md); historical status: open |
| FAIL-008 | 2026-11-01 | unknown | unknown | unknown | Coordination / scope fidelity (whole build) | Coordinator reframed confirmed build as an8am demo; RSI scope removed and owner asked to redefine the build. | Build the confirmed orientation tour, skills Wiki and RSI scope; preserve owner intent. | [REPORT-demo-framing-failure-2026-11-01](REPORT-demo-framing-failure-2026-11-01.md); historical status: open |
| FAIL-009 | 2026-11-01 | unknown | unknown | unknown | Grilling / Loop #1 preparation | Investigation displaced grilling; agent inferred missing baseline, interrupting interview and requiring repeated owner direction. | Continue the ready grilling question using settled answers and the known baseline. | [Baseline F-005](REPORT-rsi-baseline-2026-11-01.md#findings); historical status: open |
| FAIL-010 | 2026-11-01 | unknown | unknown | unknown | RUNBOOK version control / land cleanup | At15:58Z origin held62 non-main/dev branches:41 main-contained,14 dev-only,7 unmerged; dev drift exceeded threshold. | Keep branches scoped to live work; clean only contained, authorized refs. | Original log at `8b09ae4`; historical status: open |
| FAIL-011 | 2026-11-01 | unknown | unknown | unknown | S-007 RSI chart pages / Alignment Check (audit-workbench r1) | Requested Workbench fitness scores were replaced with a private activity-count dashboard; valid assessment/display path absent. | Produce the requested pinned three-run Alignment assessments and show their qualified limits on RSI. | Original log at `8b09ae4`; historical status: open |
| FAIL-012 | 2026-11-01 | unknown | unknown | unknown | S-002 / branch naming | Agent used codex/s002-trial-preflight and called it a feature branch; owner corrected the misleading namespace. | Use the owner-requested feature namespace and describe the published branch accurately. | [F-001](REPORT-s002-branch-naming-failure-2026-11-01.md#findings); historical status: disposition-recorded |
| FAIL-013 | 2026-11-02 | unknown | unknown | unknown | Shared handoff and delivery procedures | Owner reported wrong handoff publication, recurring branch/cleanup failures and confusion over catalog installation scope. | Keep handoffs local/ignored and complete authorized publication and containment checks. | [S-011](../landmarks/LMK-004-rsi-loop-during-build/specs/S-011-land-skill-events/SPEC.md); [frozen comparison](../research/IMPROVEMENT-shared-skills-delivery-2026-11-02.md); historical status: open |
| FAIL-014 | 2026-11-02 | unknown | unknown | unknown / Codex on macOS | RUNBOOK pruning / goal fidelity | Four size attempts failed; implementor optimized3000 ceiling instead of900–1500 target/near900 goal; owner repeatedly intervened. | Meet the 900–1500-character target, aiming near900, while retaining required commands. | [Diagnostic report](REPORT-runbook-target-failure-2026-11-02.md); historical status: disposition-recorded |
| FAIL-015 | 2026-11-02 | Mid (actual Terra workers) | OpenAI | gpt-6.1-terra / controlled fixtures; other actors unknown | S-011 shared workflow repair, first candidate | Candidate24/33 vs baseline29/33 predicates; unpushed/dirty end states and incomplete/unqualified Broken audit failed merge gate. | Complete clean, fully published end states and satisfy the Stable/Excellent gate before merge/install. | [First-attempt readback](REPORT-shared-skills-attempt-1-2026-11-02.md); historical status: disposition-recorded |
| FAIL-016 | 2026-11-02 | Mid (actual Terra workers) | OpenAI | gpt-6.1-terra / controlled fixtures; other actors unknown | S-011 continuation / trust and capacity | V2b attempt2 Broken28/78: writable-program execution and Critical gaps; matched pruning2916/2907 missed target; capacity failure left partial draft. | Use trusted trial execution; preserve original bytes; complete independent pruning and retests. | [Continuation report](REPORT-shared-skills-attempt-1-2026-11-02.md#continuation-checkpoint-later-contexts-no-reset); historical status: disposition-recorded |
| FAIL-017 | 2026-11-02 | unknown | unknown | unknown | Shared-skill change / Workbench preparation | Assistant proposed catalog pilot/rollout without Map, bounded Tasks, Wiki reconciliation or Prepare stop despite reading routes. | Apply AMS Map/Plan, bounded Tasks, Wiki reconciliation and the requested Prepare stop. | [Preparation-bypass report](REPORT-skills-workbench-bypass-2026-11-02.md); historical status: open |
| FAIL-018 | 2026-11-03 | unknown | unknown | unknown / Codex on macOS | Grilling Board / carry and delivery | Assistant stopped authorized research/build and repeatedly required owner intervention to publish supplied design; Board unfinished. | Carry the authorized Board research and supplied design through verified delivery. | [Failure report](REPORT-grill-board-carry-delivery-failure-2026-11-03.md); historical status: open |
| FAIL-019 | 2026-11-01 | unknown | unknown | unknown | S-003 branch organization | Work scattered across per-Task/harness branches instead of one Spec feature branch. | Use the owner-requested Feature/S-003 branch, preserving active work. | [Branch report](REPORT-s003-feature-branch-naming-failure-2026-11-01.md); F-001; pending |
| FAIL-020 | 2026-11-02 | unknown | unknown | unknown / Codex on macOS | S-003 historical-example assertion | Verification selected contextual links outside the historical example; second full attempt failed. | Check the example section and its three immutable source identities; allow contextual links outside it. | [Live verification](REPORT-live-dev-verification-failure-2026-11-02.md); F-001; S-003; test at `1d2b70d` |
| FAIL-021 | 2026-11-02 | unknown | unknown | unknown / Codex on macOS | S-003 build/tests and copy contracts | Tests ran before build completion; build invoked in wrong directory; opener violated vocabulary contract. First full attempt failed. | Read contracts first; await build in site/; test current output and compliant copy. | [Live verification](REPORT-live-dev-verification-failure-2026-11-02.md); F-002; S-003; diagnostic |
| FAIL-022 | 2026-11-02 | unknown | unknown | unknown / Codex on macOS | Retry of FAIL-021 | Built-article tests ran before rebuilding the changed pin; two assertions read stale HTML. | Rebuild changed source before testing generated HTML. | [Retry evidence](REPORT-live-dev-verification-failure-2026-11-02.md#retry-evidence-and-recurrence); S-003; diagnostic; later206 passing tests do not erase recurrence |
| FAIL-023 | 2026-11-02 | not-applicable | not-applicable | not-applicable — source inspection | Budget failure diagnostic | Tool suggests splitting artifacts, contrary to the no-split policy. | Recommend coherent pruning within the policy. | [Target report](REPORT-runbook-target-failure-2026-11-02.md); F-002; setup-workbench; diagnostic |
| FAIL-024 | 2026-11-02 | Mid (workers) | OpenAI | gpt-6.1-terra / fixtures | Workflow v2 setup, related FAIL-016 | Doctor could not resolve personal catalog; paired setup failed. | Resolve the pinned support catalog before launching a valid comparison. | [Continuation](REPORT-shared-skills-attempt-1-2026-11-02.md#continuation-checkpoint-later-contexts-no-reset); S-011/TK-002; diagnostic; separate from corrected v2b |
| FAIL-025 | 2026-11-02 | Mid (workers) | OpenAI | gpt-6.1-terra / fixtures | v3.1 qualification, related FAIL-015 | Runbook2810 missed target; native original-bytes-unverified; round failed. | Meet stated output goals and verify original-byte preservation on the candidate. | [v3.1](REPORT-shared-skills-attempt-1-2026-11-02.md#premature-handback-and-v31-failure); S-011/TK-002; failed, unqualified |
| FAIL-026 | 2026-11-02 | Mid (workers) | OpenAI | gpt-6.1-terra / fixtures | Final v3.2 and focused checks, related FAIL-025 | Candidate Runbook2845/ship481; focused2802/503 also missed goals; three full rounds incomplete. | Meet output goals and complete required qualifying rounds before eligible skill merge/install. | [Final qualification](REPORT-shared-skills-attempt-1-2026-11-02.md#owner-ended-failed-qualification); candidate `fbf581fe`; S-011/TK-002; FAILED; owner stopped tests |
| FAIL-027 | 2026-11-03 | unknown | OpenAI | GPT-6 / Codex desktop; tier not exposed | Failure-log verification | uv could not open its default cache under sandbox permissions. | Run hygiene with a writable cache; no permission bypass. | This chat; `UV_CACHE_DIR=/tmp/ams-uv-cache` hygiene passed; environment failure, diagnostic |
| FAIL-028 | 2026-11-03 | unknown | OpenAI | GPT-6 / Codex desktop; tier not exposed | Failure-log delivery fetch | Broad fetch could not update case-conflicting remote refs. | Fetch required delivery refs without altering other branches. | This chat; targeted main/dev/current-branch fetch passed; diagnostic |
| FAIL-029 | 2026-11-03 | unknown | OpenAI | GPT-6 / Codex desktop; tier not exposed | Log normalization script | Invoked unavailable python executable; script did not run. | Use the available python3 interpreter. | This chat; rerun with python3 succeeded; local invocation corrected, no reliability claim |
