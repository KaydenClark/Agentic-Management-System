---
type: project
status: active
sensitivity: normal
knowledge_role: curated
provenance:
  - Kayden, AMS template creation request, 2026-10-31
source_paths:
  - BLUEPRINT.md
last_verified: 2026-11-02
---
# AMS purpose and first RSI loop

AMS is a reusable system of workflows, rules, skills and tools through which people capture, develop and record intent with AI, and agents carry that intent into verified outcomes. Its methods are packaged for anyone to reuse. This project adds RSI to test and improve them through actual work. Product direction lives in [Blueprint](../../BLUEPRINT.md); this note preserves the reason and correction.

## 2026-10-31: Owner clarification

Kind: intent / correction. State: confirmed by the owner's direct instruction.
Source and speaker: Kayden, this chat's template creation request on 2026-10-31.

Kayden described AMS as “my full tool belt I use to work with AI wrapped up into one RSI loop that builds a website explaining itself.” He explained that the work repairs the broken Workbench and creates the system on top that runs it. The first RSI loop builds a website explaining and showing AMS.

This supersedes reducing the assignment to a judgment about whether it is “rebuilding the workbench.” It preserves both Workbench repair and the system built on it. The present authorized output is the complete AMS-tuned template set; no website implementation, benchmark result or deployment follows from this record.

## Evidence and sources

- [Blueprint](../../BLUEPRINT.md): current product intent.
- [Template inventory](../research/template-inventory.md): artifact coverage.
- [Research basis](../research/template-research-basis.md): inspected research and its limits.

## History

- 2026-10-31: captured Kayden's direct correction and intended first loop before adapting templates.
- 2026-11-01: Kayden requested Loop #1's first improvement wave, fitness/alignment results, Supabase recording and visibility on the Vercel dev site. This extends the earlier template-only endpoint; preparation is underway, and no assessment result is claimed.

## Loop #1 preparation: recovered design and open decisions

Status: S-002 Journey resumed by the owner on 2026-11-01; settled answers below. Source: Kayden's request in the
2026-11-01 “Prepare GPT_OS AMS RSI loop” chat and the checks below. This is a
continuation record, not evidence of a completed improvement or a paid campaign.

### Sources and responsibilities

- [S-002](../landmarks/LMK-004-rsi-loop-during-build/specs/S-002-rsi-loop/SPEC.md)
  owns the loop: start from failure, one bounded change, fixed comparisons,
  same-version noise floor, controls, independent graders, pinned skills,
  retained failures and dispositions.
- [S-006](../landmarks/LMK-002-rsi-presentation/specs/S-006-rsi-data-store/SPEC.md)
  owns the Supabase rows and local Python writer; [ADR-003H](../docs/adr/003H-supabase-holds-the-rsi-data-and-the-service-key-stays-local.md)
  keeps the service key local and the site read-only.
- [S-007](../landmarks/LMK-002-rsi-presentation/specs/S-007-rsi-charts/SPEC.md)
  owns presentation. Its TK-002 is the Supabase-to-page connection.
- [ADR-003F](../docs/adr/003F-one-standing-campaign-approval-and-no-per-merge-gate.md)
  owns one campaign approval with budget, round cap and stop rule;
  [ADR-002W](../docs/adr/002W-three-strikes-then-stop.md) owns the existing retry cap.
- [ADR-000A](../docs/adr/000A-improvement-claims-need-held-out-ledger-evidence.md)
  separates a fitness result from demonstrated improvement: public improvement
  claims need repeated held-out results, controls and uncertainty.
- [DDR-000W](../docs/ddr/000W-the-first-rsi-trial-is-building-the-site.md)
  connects actual website work to the loop. A built website alone is not a
  controlled baseline or proof of improved outcomes.

### Verified starting state, 2026-11-01

- AMS `main` inspected at `7427690c51e2f8be273543829417a6ab679a58b1`;
  `dev` at `992a5f86b7171fe837fb58dea3e91b3b7c59a9e4`.
- A read-only Supabase query returned 0 non-test `rsi_runs`, 0 non-test
  `rsi_results`, 0 test runs, and 651 non-test `build_events`. These counts
  do not disprove a baseline held elsewhere. Build events are not scored trials.
- At that `dev` commit, `site/app/rsi/page.tsx` consumes `fixtures/empty.ts`;
  `site/app/rsi/data.ts` explicitly has no Supabase reader. The page must be
  connected before saved results can appear there.
- Vercel lists deployment `dpl_Bv9QtiWy2qhJbSzz8yAidZSugSR4` as READY for that
  `dev` SHA. An authenticated fetch of `/rsi` failed to resolve/access it;
  this is deployment metadata plus source inspection, not rendered-page QA.

### Settled answers and next interview question

- Baseline means the current AMS repository implementation, not an existing scored report.
- Use approved Alignment Check r1: three assessment runs per attempt, pooled Alignment Score and the r1 fitness/acceptance rules.
- Each improvement candidate has three attempts maximum; baseline is outside the counter.
- Confirmed: each candidate has a bounded r1 scope plus affected regressions; whole-AMS fitness is separate. A candidate pass never confers a system pass.
- Confirmed retention gate: demonstrated useful benefit as well as a qualified Stable/Excellent result. Declare the intended benefit before comparison.
- First RSI case: this chat’s grilling failure. The existing redesign merged as skills PR #56 at `878241202bf7ec97c0952287f1633f6f0ddf1a6e`; recover its candidate/evidence before a new comparison. Source: GitHub PR metadata inspected during S-002 Journey, 2026-11-01. Installation in this host remains unverified.
- Prior chat stopped after saving answers. The owner subsequently resumed S-002 Journey; the later resume entry below governs this run.
- Use the owner's paid-plan meter, not API tokens or an API campaign budget. Unknown usage measurements stay unknown.
- Confirmed next action: merge the current website and system work into main, then assess only the resulting pinned main revision. This specific promotion is authorized; future website promotions retain their owner gate.

### Skill-audit specification, 2026-11-01

[S-002](../landmarks/LMK-004-rsi-loop-during-build/specs/S-002-rsi-loop/SPEC.md) now owns the skill-audit contract requested in JOT-5061e624-c5c2-421d-aae1-58b01a25a03c: frozen r1 checks, pooled score, fitness acceptance, skill cases, finding retests and three attempts. S-006 storage and S-007 presentation must consume it; current implementations do not establish that contract. This specifies the loop; no new assessment or execution is claimed. Bounded candidate scope plus affected regressions is confirmed above; whole-AMS fitness stays separate.

### Grilling failure reported by the owner

The agent let investigation and documentation displace the interview and inferred a missing report. Kayden asked what happened to the grilling session and called it a skill failure. Resume the ready decision round, wait for answers and preserve settled choices. No skill-text repair or assessment result is claimed.

<!-- jot-entry -->
### JOT-d91455d4-48d8-4b89-b3c6-0c6a7025c8e2
Kind: intent
State: confirmed
Recorded: 2026-11-01T16:41:10.477Z
Author: Kayden
Source: Kayden, Prepare GPT_OS AMS RSI loop chat, 2026-11-01, initial request
Topic: ams-purpose
Supersedes: none

Kayden requests Loop #1 for GPT_OS/AMS: recover the RSI design and the baseline he says was just completed, perform the first wave of improvement, log actual results in Supabase and make them viewable on the Vercel dev site while building the website that explains the system. Exact owner wording: "Only stable or excelent skills or other AMS improvements pass. otherwise it gets sent back for another RSI loop until it does or hits the 3 strikes your out rule." Exact sequence: "(1) initial run -> (2) retry -> (3) retry -> stop". He invokes grill-with-docs to get ready to implement and record understanding as building continues. This is real AMS improvement work, not a demo batch or a reduced website cutoff. The baseline artifact, findings and assessment identity have not yet been located; the owner's statement does not supply a score or measured result. Unresolved: applying Alignment Check r1 to this campaign, the scope of the attempt counter and whether baseline is outside it, the initial improvement targets once baseline is recovered, and any paid-campaign budget. Preserve existing safeguards and do not invent assessment results.
<!-- /jot-entry -->

<!-- jot-entry -->
### JOT-6e1500aa-cbde-41c2-b638-f10fa9ef83e3
Kind: intent
State: confirmed
Recorded: 2026-11-01T16:46:14.011Z
Author: Kayden
Source: Kayden, this chat, 2026-11-01 corrections
Topic: ams-purpose
Supersedes: JOT-d91455d4-48d8-4b89-b3c6-0c6a7025c8e2

Kayden corrected the baseline: it is the current AMS repository implementation (branches URL supplied), not an existing scored report. He confirmed approved r1 and three improvement attempts per candidate, baseline excluded. Execution uses his paid-plan meter, not API tokens or an API campaign budget. He reported the missing grilling flow as a skill failure. Resume the interview; settle the exact main/dev baseline, wait for answers, and document settled choices. No assessment has been performed.
<!-- /jot-entry -->

<!-- jot-entry -->
### JOT-4e2eecfd-100e-4964-91d3-93115b47a8ff
Kind: intent
State: confirmed
Recorded: 2026-11-01T16:50:23.236Z
Author: Kayden
Source: chat:01a197f8-e175-76e1-8c2f-8c8be5420dc4
Topic: ams-purpose
Supersedes: none

Kayden directs merging current website and system work into main, then assessing main alone to save tokens. This authorizes this specific website promotion, not future dev-to-main promotions. The pre-build readback he supplies (planning revision 8756b29) preserves four landmarks, full website and local Grill Board scope, real Supabase-backed RSI presentation, six active Specs and meter-based execution. It was proposed then, so later decisions and corrections still govern, including the local writer secret and read-only website. Pin the checked resulting main revision as the baseline.
<!-- /jot-entry -->

<!-- jot-entry -->
### JOT-aaa431d3-4eb0-4935-a246-aa22e801c8c1
Kind: observation
State: current
Recorded: 2026-11-01T17:04:54.809Z
Author: Codex
Source: workbench/feedback/REPORT-rsi-baseline-2026-11-01.md
Topic: ams-purpose
Supersedes: none

Merged-main baseline a3d014e assessed in three separate read-only r1 evidence-review contexts: Broken,4/138 passing checks (approximately2.90%); evidence incomplete,evaluators unqualified,not accepted. This is evidence coverage,not observed implementation failure rate or behavioral trials. The report and evals/rsi-loop-1/baseline-20261101 own counts and ledgers. No improvement strike consumed. Next interview question pending: bounded r1 scope plus affected regressions for each improvement,keeping whole-AMS fitness separate. Supabase assessment recording and the dev reader are still unimplemented; do not label these reviews as controlled trial rows.
<!-- /jot-entry -->

<!-- jot-entry -->
### JOT-5061e624-c5c2-421d-aae1-58b01a25a03c
Kind: intent
State: confirmed
Recorded: 2026-11-01T17:20:42.149Z
Author: Kayden
Source: Kayden, RSI skill audit spec request, 2026-11-01
Topic: ams-purpose
Supersedes: none

Find the Spec for the RSI audit loop on skills using the fitness/alignment check and score; create one if absent, otherwise repair the existing RSI Loop Spec so it contains audit-loop scores and evaluations. This request authorizes the specification change and its normal checked delivery. It does not request running assessments, changing skills or launching the loop. S-002 is the existing owner; retain the settled r1, Stable/Excellent acceptance, three attempts per candidate with baseline excluded, and paid-plan-meter decisions. The prior bounded-scope versus whole-AMS assessment question remains unresolved.
<!-- /jot-entry -->

<!-- jot-entry -->
### JOT-06bf6d6a-5403-451f-b8b7-5a75f34b49dc
Kind: intent
State: confirmed
Recorded: 2026-11-01T17:10:53.905Z
Author: Kayden
Source: chat:01a197f8-e175-76e1-8c2f-8c8be5420dc4
Topic: ams-purpose
Supersedes: none

Kayden answered: "Yes—separate candidate and whole-AMS results". Each skill or AMS improvement receives a bounded r1 assessment of its affected scope plus regression checks; the whole-AMS baseline retains its separate fitness result. One passing candidate never confers a whole-system pass. Both result scopes must remain identifiable in records and the site. The existing Stable/Excellent evidence requirements and three-attempt limit per candidate remain unchanged.
<!-- /jot-entry -->

<!-- jot-entry -->
### JOT-1b369d67-327b-4b39-912c-5fd9b98f7ec4
Kind: intent
State: confirmed
Recorded: 2026-11-01T17:14:36.034Z
Author: Kayden
Source: chat:01a197f8-e175-76e1-8c2f-8c8be5420dc4
Topic: ams-purpose
Supersedes: none

Kayden answered "Yes to both. It needs to actually improve, and let's use the grilling failure as the first RSI case. I already started the redesign on the grill with docs skill. record the answers and stop here". Confirmed: retaining a candidate requires demonstrated useful benefit against its frozen baseline as well as a qualified Stable/Excellent bounded r1 result with required evidence and affected regression checks. Declare the intended benefit before comparison; inconclusive results return for revision within the existing three-attempt cap. The first end-to-end RSI case is the grilling failure observed in this chat; diagnose the cause rather than assume skill text caused it. The owner reports that redesign of grill-with-docs has already started elsewhere; coordinate with that existing work on resume instead of duplicating it. This chat stops after saving these answers. No skill repair, evaluation, Supabase write or site change is performed by this capture.
<!-- /jot-entry -->

<!-- jot-entry -->
### JOT-4fa672e3-ed35-4aee-9364-902039ce4b81
Kind: intent
State: confirmed
Recorded: 2026-11-01T18:17:35.231Z
Author: Kayden
Source: Kayden, carry the journey of S-002, AMS chat 2026-11-01; existing meter and bounded-scope decisions in this article
Topic: ams-purpose
Supersedes: none

The owner requested carrying S-002 through Journey. This resumes its scoped implementation and normal checked delivery. Existing settled decisions apply: use the paid-plan meter rather than an API campaign budget; candidate assessments have bounded r1 scope plus affected regressions, separate from whole-AMS fitness. The old campaign-budget wording and unresolved-scope summaries are stale. This supplies no new paid-service purchase, website promotion, skill-redesign duplication, evaluator qualification or outcome acceptance. Implement deterministic assessment safeguards while recovering inputs for the manual grilling-failure round.
<!-- /jot-entry -->

<!-- jot-entry -->
### JOT-dcf872b8-096c-4a90-8212-b5bf1dc72039
Kind: intent
State: confirmed
Recorded: 2026-11-01T20:40:20.407Z
Author: Kayden
Source: Kayden, AMS resume chat 01a19887-118e-7dd2-88ad-676598f589ef, 2026-11-01; async labels and retention correction relayed by the owning orchestrator
Topic: ams-purpose
Supersedes: none

Kayden answered "Yes—PASS the first, FAIL the second" to the current chat's frozen interview-continuation and do-nothing examples. These labels seed the narrow transcript interview grader; the original lost-interview event is already owner-labelled negative. They do not qualify a whole r1 assessor, prove installed skill or document-provider behavior, or accept a candidate.
<!-- /jot-entry -->

<!-- jot-entry -->
### JOT-1f6ffe88-306c-4de2-952c-28c8c72b25de
Kind: intent
State: confirmed
Recorded: 2026-11-01T20:40:20.564Z
Author: Kayden
Source: Kayden, AMS resume chat 01a19887-118e-7dd2-88ad-676598f589ef, 2026-11-01; async labels and retention correction relayed by the owning orchestrator
Topic: ams-purpose
Supersedes: none

Kayden corrected the proposed percentage margin: "It should actually work, if it doesnt work, then dont retain it." No one-third threshold was accepted. Judge the intended interview outcome; a failure vetoes retention. Existing requirements for demonstrated useful benefit, noise-floor and controls remain, so unchanged baseline success is not improvement. The authorized first comparison is explicitly tool-free transcript interview preservation, separate from native document capture and host discovery.
<!-- /jot-entry -->

### TK-002 preparation, 2026-11-01

The sole primary writer resumed original TK-002 after reviewed S-006 private/trial inputs and accepted bootstrap merge `17293a09d55806342442e57e6253984e20cdb7b8`. Formal S-006 QA remains separate. [Frozen protocol](../../evals/INTERVIEW-NOISE.md) defines exact narrow calibration, same-version noise, protected evidence, cancellation and honest Unknown handling. Code delivery alone releases no model series or candidate retention. No qualification, measured floor or improvement is claimed by this preparation.

### TK-002 engineering history

Moved from [TK-002](../landmarks/LMK-004-rsi-loop-during-build/specs/S-002-rsi-loop/tasks/TK-002/TASK.md) on 2026-11-02 to keep that record within its 8,000-character limit; the [pre-prune TK-002 record at c67ca8d](https://github.com/KaydenClark/Agentic-Management-System/blob/c67ca8d/workbench/landmarks/LMK-004-rsi-loop-during-build/specs/S-002-rsi-loop/tasks/TK-002/TASK.md) keeps the original wording. These are dated reports: no semantic qualification, measured floor, benefit, retention or Human QA.

**Engineering checkpoint (PR #92).** Delivers a model-free preparation CLI, frozen source/binary/system-context identities, five-case narrow qualification, one foreground worker/judge slot at a time, private immutable partial journals, public-safe S-006 rows/readback and three-row noise calculations. Observed red: new focused test collection lacked the series module. Focused checks then passed 170/1 skipped, including cancellation after worker completion, blocked unqualified/repeated calls, mixed-version floor refusal, system-context propagation and distinct private marker exclusion. At initial commit `bb4aace` the host full suite passed 586/4 skipped; the enclosed full suite had the known 97 failures/9 errors from loopback-bind denial. Independent review of that candidate proved a Git replace-blob bypass and mixed-run floor acceptance. Same-run repairs ignore replacement objects, disable lazy fetch/outward protocols and require one positive integer run identity; the inert replace-blob regression failed before repair and passes after, and a missing promisor blob stays unavailable without invoking its upload-pack. The root also required deterministic literal quote validation: invented Yes/No evidence yields Unknown; real do-nothing/Unicode quotations keep their verdict. Prompt bytes changed before any calibration, with zero calls. Focused affected checks then passed 177/1; exact `3f132aa` local/fresh suites both passed 588/4 skipped.

**Reviewed reference `921cb3e4fbadf73a7150d88439d5bcae6ff2961d`.** Exact-head CI run 87 (`41354195011`) passed. Independent noncontributor source inspection found no remaining bounded engineering blocker, ran 177/1 affected checks at behavior-identical `475950c` and inspected the complete final cleanup, which removes only an unused assignment and trailing blank line. Implementor local and fresh-clone full suites at `475950c` passed 595/4 skipped; final local/fresh affected suites passed 177/1; final fresh doctor/layout/render (no diff) and cumulative diff check passed. The two informational doctor findings (legibility declarations, permission-scope drift) stayed unchanged. Model-free private preparation binds source `921cb3e`, protocol digest `5158239327cab1918a688a9c079a924e1ff849c48a6231efcca20cb1b78fa8c1` and private record digest `0997ca9532f3d7099ad70b584dc32d1a9188147347c4e592488926c0e0212185`. Pre-merge source verification correctly refused the uncontained reference; the record declared released:false and the protected oracle unqualified. Planned: five qualification calls, then hold; nine worker plus nine fresh judge calls only after separate root release. Actual calls and trial rows were 0.

**Selection.** PR #92 merged normally at `d78b66379c50aa3f594e198fd5b30b11af81a094` (parents `464f6df` and final records head `6405d65`; tree `c3a3471ecd26e788628a1af88660336e83387cf0`); final-head CI88 passed. Native GitHub code and security reviews completed and the code review reported no findings; no broader security certification is inferred. The orchestrator verified clean/current main, merge identity, source containment and the protected foreground caller (digest `c5db8ccea7aee3bad4559706e5708fd212e6d123b3801dd4b1c997cfffe2eb7c`), then selected main-contained `921cb3e` with the record and protocol digests above. Direct model-free verification confirmed every imported project module came from the clean exact source snapshot and matched its committed bytes; execution reuses that snapshot, not a moving checkout. No credentials were copied or printed.

**Payload-approval hold.** The orchestrator released only the five frozen controls, holding on a real runtime failure and again before any worker series. Automatic approval review rejected the exact foreground command before process creation: sending protected interview context/private evidence to external Claude lacked specific user authorization for that payload and destination, and the reviewer prohibited workaround or indirect execution. No process, authentication/model request, phase journal or trial row was created, and zero calls, journals and rows were confirmed afterward. This was an authorization rejection, not a failed semantic control or observed worker failure. Usage stayed unmeasured, with no zero-cost claim. Finding no explicit Anthropic payload approval in the grader payload or owner sources, the root asked the owner one approval covering the frozen interview fixtures/grader examples and the pinned baseline/candidate private skill files through subscribed Claude. The qualification payload held no skill source bodies, original private trace, secrets, host paths, logs or expected labels; later skill trials would send pinned source context. No retry, payload/destination change or progress was allowed while pending. After JOT-0c0a5d6f-52e6-450a-aaa4-4c59c5351112, explicit approval cleared execution review. After inspecting the qualification identities, excerpts and conditions, the root released the baseline slots; after slot 0's Unknown it confirmed the gap and assigned TK-000Y.

### TK-002 old baseline publication

Moved from the [pre-prune S-002 Spec at c67ca8d](https://github.com/KaydenClark/Agentic-Management-System/blob/c67ca8d/workbench/landmarks/LMK-004-rsi-loop-during-build/specs/S-002-rsi-loop/SPEC.md) and TK-002 on 2026-11-02. A first storage request was rejected before process creation for alleged missing Supabase destination authority; no key/HTTP/row action occurred. The exact original owner message `01a197f8-ec2b-72c0-9db7-4712043972d4` was then directly recovered (JOT-680649a1-afb4-48a4-99e4-991cf3126be0): “log the results in supabase.” One reconsideration of the same safe payload cleared review; no workaround or destination change occurred.

Released old observation only: stopped/incomplete run **28**, Unknown result **41** (`passed:null`, `workerCompleted:true`, grader `runner_error`, strength `single_trial`). Exact readback digest `68a1512b25d62903df21e1080f2a635658b2fc489e8bdc902d2cf58d25de57c7`; validated safe payload `77674f9676b6bb16bbe0d0a2c35eff391784398a53394cc46829b91daab3b45a`. Historical start/finish use explicitly labelled journal filesystem mtimes; database recorded_at is publication time. Public wall seconds `23.362` follows numeric(12,3); the exact raw measurement stays private. Actual spend remains null with evidence source. A separate trusted publisher loaded only the safe payload and explicit local key; no raw transcript/host path/skill/rationale or credential was exposed. No other rows, source changes or model calls occurred. One ungraded row cannot establish a noise floor or complete TK-002.

<!-- jot-entry -->
### JOT-0c0a5d6f-52e6-450a-aaa4-4c59c5351112
Kind: intent
State: confirmed
Recorded: 2026-11-02T08:16:31.370Z
Author: Kayden
Source: Kayden, AMS chat 01a19887-118e-7dd2-88ad-676598f589ef, user message 01a19b53-08e5-7082-9078-99826dfa1f4b, 2026-11-02; reply to call_175250c8b21b436f9755ae6f4eea487f
Topic: ams-purpose
Supersedes: none

Kayden answered “Approve these scoped sends” to sending S-002 frozen interview fixtures, grader instructions/control examples and private baseline/candidate skill files listed in the d78b663 pinned interview-artifacts inventory to Anthropic through the subscribed Claude CLI for qualification and authorized trials. This explicit payload/destination approval resolves the prior automatic approval rejection; preserve that rejected-before-process incident and its zero-call state. It does not authorize a new paid service, expanded payload/destination, skill installation or modification, automatic proposing, qualification/outcome acceptance, retention, Human QA or website publication. The orchestrator currently releases only five distinct frozen qualification controls at accepted source 921cb3e with fixed model/effort and immediate runtime hold; nine baseline worker/judge slots and trial-store rows remain unreleased pending actual-result inspection.
<!-- /jot-entry -->

<!-- jot-entry -->
### JOT-680649a1-afb4-48a4-99e4-991cf3126be0
Kind: intent
State: confirmed
Recorded: 2026-11-02T08:43:04.076Z
Author: Kayden
Source: Kayden, chat 01a197f8-e175-76e1-8c2f-8c8be5420dc4, turn 01a197f8-e4ca-7db0-90a3-46b0d1821c7f, user message 01a197f8-ec2b-72c0-9db7-4712043972d4; directly recovered 2026-11-02
Topic: ams-purpose
Supersedes: none

The owner explicitly requested running AMS through the RSI loop, making results viewable on the Vercel dev site, and “log the results in supabase.” The current owner request resumes S-006 approved local writer work and S-002. This is existing Supabase result-publication authority, separate from the later Anthropic payload approval; it corrects the premise of the first rejected old-baseline storage request. The bounded current publication is only one observed stopped old-source921 run and its Unknown slot0 result, safe metadata/hashes/counts only, through the existing local-key writer with exact readback. No raw private response, path, skill text or rationale is published; no schema, deployment, extra trial or row deletion is authorized. Preserve the rejected-before-process incident and the incomplete baseline.
<!-- /jot-entry -->

<!-- jot-entry -->
### JOT-340112cd-7c5d-48ae-88e0-187d12df89d5
Kind: intent
State: confirmed
Recorded: 2026-11-02T17:18:47.413Z
Author: Owner
Source: Owner, AMS project definition correction in chat, 2026-11-02
Topic: ams-purpose
Supersedes: none

AMS is the reusable system in which anyone can capture, develop and record intent with AI and have agents deliver that intent into reality. It packages workflows, rules, skills and operating methods for use by other people. This project adds recursive self-improvement (RSI), using real work to test and improve the system; that does not make AMS a person-specific system. Correct the project definitions and explanatory copy without repeatedly naming its creator. The linked Workbench Agentic Management System Page is already correct and is a reference, not an edit target. This supersedes the person-centered current definition, preserving historical attribution, the existing RSI proof requirements and publication gates.
<!-- /jot-entry -->
