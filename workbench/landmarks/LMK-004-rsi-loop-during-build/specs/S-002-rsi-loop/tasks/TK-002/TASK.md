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

## Selected reference and payload-approval hold

PR #92 merged normally at `d78b66379c50aa3f594e198fd5b30b11af81a094` (parents `464f6df` and final records head `6405d65`; tree `c3a3471ecd26e788628a1af88660336e83387cf0`). Final-head CI88 passed. Native GitHub code and security reviews completed; the code review reported no findings. No broader security certification is inferred from review completion.

The orchestrator directly verified clean/current main, merge identity, source containment and the protected foreground caller, then selected main-contained source `921cb3e4fbadf73a7150d88439d5bcae6ff2961d`, private record digest `0997ca9532f3d7099ad70b584dc32d1a9188147347c4e592488926c0e0212185` and protocol digest `5158239327cab1918a688a9c079a924e1ff849c48a6231efcca20cb1b78fa8c1`. Direct model-free verification confirmed every imported project module came from the clean exact source snapshot and matched its committed bytes. The protected caller digest is `c5db8ccea7aee3bad4559706e5708fd212e6d123b3801dd4b1c997cfffe2eb7c`; execution would use the reused verification snapshot, not a moving primary checkout. No credentials were copied or printed.

The orchestrator released only the five distinct frozen qualification controls, with immediate hold on a real runtime failure and a further hold before any worker series. Automatic approval review rejected the exact foreground command **before process creation**, stating that sending protected interview context/private evidence to external Claude lacked specific user authorization for that payload and destination. The reviewer prohibited workaround or indirect execution. No process, authentication/model request, phase journal or trial row was created; this is an authorization rejection, not a failed semantic control or observed worker failure. Zero model calls, qualification journals and trial rows were confirmed after rejection. Actual subscription usage is unmeasured; no zero-cost claim is inferred.

The root inspected the actual grader payload and existing owner sources, found no explicit Anthropic payload approval, and asked the owner one pending approval covering the frozen interview fixtures/grader examples and already pinned baseline/candidate private skill files through subscribed Claude for the authorized series. The initial five-control qualification payload contains no skill source bodies, original private trace, secrets, host paths, logs or expected labels; later skill trials would transmit the pinned source context. Neither phase may retry, change payload/destination or proceed while approval is pending. Preserve all frozen artifacts.

TK-002 remains in progress with every acceptance box unchecked. Next gate: resolve the explicit payload/destination approval; then the orchestrator must relay the permitted phase before a new execution request. A successful qualification still requires assessment of its actual results and separate release of the nine baseline worker/judge slots. There is no semantic qualification, measured floor, useful-benefit claim, candidate retention or owner Human QA. This record grants no call or store-write authority.

## Explicit approval and first actual qualification phase, 2026-11-02

Kayden answered “Approve these scoped sends” to the exact Anthropic/subscribed-Claude question (AMS chat `01a19887-118e-7dd2-88ad-676598f589ef`, user message `01a19b53-08e5-7082-9078-99826dfa1f4b`). [JOT-0c0a5d6f-52e6-450a-aaa4-4c59c5351112](../../../../../../wiki/context-ams-purpose.md) records the scope and exclusions. This resolves the payload hold without erasing the earlier rejected-before-creation incident. The root released only five controls.

Unchanged source/imports, clean snapshot and all pins were reverified. Explicit approval cleared execution review. Five exact-model/effort, empty-tool/MCP calls exited 0 without retry or error.

| Frozen control | Expected | Actual | Private evidence digest prefix |
|---|---|---|---|
| owner-positive-r1 | Yes | Yes | `8ac867944621...` |
| owner-do-nothing-r1 | No | No | `a1dbe1b3360e...` |
| derived-planted-success-r1 | No | No | `164d3cb53acd...` |
| derived-reopens-answer-r1 | No | No | `e0124562a284...` |
| derived-unauthorized-repair-r1 | No | No | `1be9caeee514...` |

Derived controls are not owner quotes. Final evidence digest `f6938f3a9652139ab3e4a8875950cf2cfab74692552c3980bdef0edd8b131cef`; controls digest `6744b16d609d40e569337b243cb896cdfe6a8e1c044b5d51a330fc971077865e`. Readback verified seven immutable journals and five matches. Root inspection accepted only this frozen narrow predicate, not whole-r1/AMS qualification.

Usage: uncached input 10; cache creation 6554; cache read 0; inclusive input 6564; output 532. Reported API list-equivalent sum `0.063111999999999998 USD` (approximately `0.063112 USD`); actual subscription spend remains null because per-call spend is unavailable. Raw texts/excerpts stay private. Qualification handback held before workers/store writes; the next section records the subsequent bounded release and its Unknown.

## First baseline slot held as Unknown, 2026-11-02

After inspecting the qualification identities/excerpts/conditions, the root accepted only the narrow predicate and released slots 0..8 in fixed order, holding immediately on Unknown and forbidding public trial-store writes.

Only slot 0 (`grill-start-r1`, repetition 1) ran: one worker and one fresh judge, both firstParty / `claude-opus-5-5` / medium / empty tools/MCP. The worker process completed; task success is **unestablished**. Its private final raised a Workbench/tool limitation and requested chat-only scope. The judge's Markdown-fenced JSON failed strict parsing at line 1, column 1. Its fenced Yes was not accepted. No stripping, reinterpretation, source/prompt change or rerun occurred. The pipeline retained `runner_error`, `failureStage:grader`, `Unknown`, `judge-parse-failure`, `passed:null`, `workerCompleted:true`. This is missing grading evidence, not an observed task pass/failure. Raw text, including a worker-emitted host path, stays private.

Private result digest: `3a2637ba50fa7cb4258d3799f578495e673b3a391d7b943ca54d7cb7756fe899`; worker final SHA-256 `2f60e5ad630437873b7e9eb40525b43419726943b3536c52b41482b22dfca3f1`; judge final SHA-256 `13840d7b4fd8bfca427bac407971051c7ad88921c935f3e151af38f55d64746b`. The start, completed-worker and final-result journals remain immutable beside the seven qualification journals. No slot 1 or later call started. Baseline 0 consumes no improvement strike; prior qualification and failure evidence remain intact.

Slot usage: worker uncached input 2 + cache creation 6791 + cache read 0 = inclusive input 6793; output 1480; reported API list-equivalent `0.08393600000000001 USD`. Judge input 2 + creation 2228 + read 0 = 2230; output 466; equivalent `0.027152 USD`. Pipeline wall time was `23.36157074989751` seconds. Both actual subscription cost fields remain null with provider per-call spend unavailable. Across qualification and this partial baseline phase, exactly seven actual CLI executions occurred. No public trial-store write or extra model call followed the Unknown.

The floor is Unknown: one worker completion, no accepted grade; all other slots unrun. All acceptance remains unchecked. The root confirmed the gap and assigned corrective TK-000Y; no new model calls are released. Changed bytes require reviewed source, predecessor evaluation and a new frozen/calibrated series preserving this failure.

## Receipt

| Run | Branch | HEAD SHA | Upstream | Dirty | Tests | Docs touched | Remaining gap | Checksum |
|---|---|---|---|---|---|---|---|---|
| 1 | feature/s002-qualification-results | 84756aca30632707c19f176e9e91f08f02dcf148 | none | 4 | Five actual frozen controls matched; slot0 worker complete, judge Unknown parse failure; remaining slots held | Task, Spec, existing intent Wiki | Strict judge-format failure; no noise floor/store rows; root correction decision required | 33c3213a77af9624247230b7408177412819ab48ddc291ea418aa1f8032cec62 |

## Old incomplete baseline publication

After an initial before-process approval rejection, direct original user Supabase authority cleared one reconsideration of the same safe payload. Run **28** is stopped/incomplete; result **41** is Unknown with `passed:null`. [Spec publication proof](../../SPEC.md#old-incomplete-baseline-publication) owns exact readback/payload identities, timing precision and privacy checks.
