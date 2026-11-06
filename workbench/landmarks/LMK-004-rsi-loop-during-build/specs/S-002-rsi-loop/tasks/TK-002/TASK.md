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

Uses the owner's paid-plan meter, not an API campaign budget (JOT-6e1500aa-cbde-41c2-b638-f10fa9ef83e3, linked AMS-purpose Wiki); the 2026-11-01 Journey resume superseded the budget blocker. S-006 private assessment/trial-row inputs (PRs #80/#81/#83/#86 at `6e30c87`; owner QA separate) were released at bootstrap merge `17293a09d55806342442e57e6253984e20cdb7b8`. Read `AGENTS.md`, this Task, the parent Spec, ADR-002G/002I/002L/002J under `workbench/docs/adr/` and `evals/EVAL-TASK-TEMPLATE.md`.

Deliver step zero of the loop: a small fixed task set under `evals/` (dev split, at least three tasks, each with a grader taken from the accepted version), a runner that executes a pinned version in a sandbox without skipped permission checks, and repeated same-version runs whose rows (with arm, version, skills pin, provider, model, effort, cost, tokens and completed state) are written through S-006. Compute and record the per-task flip rate and spread as the noise floor.

Hand back to S-002 with `close`, including measured subscription usage, or unknown when unavailable.

## Acceptance

- [ ] At least three same-version runs per task exist as rows with full fields.
- [ ] The floor (flip rate and spread per task) is recorded and cited by row IDs.
- [ ] Trial logs show no skipped permission checks; the grader commit equals the accepted version's.

## Resumed bounded run

Sole primary writer: `feature/s002-rsi-loop`. Preserve r1 and the Spec's three-run rule (older two-run wording reconciled). Deliver the checked runner, frozen five-case narrow-oracle protocol and deterministic error/identity guards before any call; no candidate comparison or skill modification occurs here.

## Engineering reference and payload hold

PR #92 (merged `d78b66379c50aa3f594e198fd5b30b11af81a094`) delivered the model-free runner and [frozen protocol](../../../../../../../evals/INTERVIEW-NOISE.md). The orchestrator selected reviewed main-contained source `921cb3e4fbadf73a7150d88439d5bcae6ff2961d` (CI run 87), protocol digest `5158239327cab1918a688a9c079a924e1ff849c48a6231efcca20cb1b78fa8c1` and private record digest `0997ca9532f3d7099ad70b584dc32d1a9188147347c4e592488926c0e0212185`. Automatic approval review then rejected the five-control command **before process creation** for lacking payload/destination authorization; nothing ran. The [engineering history](../../../../../../wiki/context-ams-purpose.md#tk-002-engineering-history) keeps checks, review repairs, selection proof and rejection detail.

## Explicit approval and first actual qualification phase, 2026-11-02

Kayden answered “Approve these scoped sends” (chat `01a19887-118e-7dd2-88ad-676598f589ef`, message `01a19b53-08e5-7082-9078-99826dfa1f4b`); [JOT-0c0a5d6f-52e6-450a-aaa4-4c59c5351112](../../../../../../wiki/context-ams-purpose.md) records scope and exclusions; the rejection stays recorded. With source, imports, snapshot and pins reverified, the root released only five controls: exact-model/effort, empty-tool/MCP calls that exited 0 without retry or error.

| Frozen control | Expected | Actual | Private evidence digest prefix |
|---|---|---|---|
| owner-positive-r1 | Yes | Yes | `8ac867944621...` |
| owner-do-nothing-r1 | No | No | `a1dbe1b3360e...` |
| derived-planted-success-r1 | No | No | `164d3cb53acd...` |
| derived-reopens-answer-r1 | No | No | `e0124562a284...` |
| derived-unauthorized-repair-r1 | No | No | `1be9caeee514...` |

Derived controls are not owner quotes. Evidence digest `f6938f3a9652139ab3e4a8875950cf2cfab74692552c3980bdef0edd8b131cef`; controls digest `6744b16d609d40e569337b243cb896cdfe6a8e1c044b5d51a330fc971077865e`; readback verified seven immutable journals and five matches. The root accepted only this narrow predicate, not whole-r1/AMS qualification. Usage: input 10 + creation 6554 + read 0 = 6564, output 532; API list-equivalent `0.063111999999999998 USD`; subscription spend null (unavailable). Raw texts stay private.

## First baseline slot held as Unknown, 2026-11-02

The root released slots 0..8 in fixed order, holding on Unknown, without public store writes. Only slot 0 (`grill-start-r1`, repetition 1) ran: a worker and fresh judge, both firstParty / `claude-opus-5-5` / medium / empty tools/MCP. The worker completed, its private final raising a Workbench/tool limitation and requesting chat-only scope; task success is **unestablished**. The judge's Markdown-fenced JSON failed strict parsing at line 1, column 1. Its fenced Yes was not accepted; nothing was stripped, reinterpreted, changed or rerun. Retained `runner_error`, `failureStage:grader`, `Unknown`, `judge-parse-failure`, `passed:null`, `workerCompleted:true`: missing grading evidence, not an observed pass/failure. Raw text, including a worker-emitted host path, stays private.

Result digest `3a2637ba50fa7cb4258d3799f578495e673b3a391d7b943ca54d7cb7756fe899`; worker final SHA-256 `2f60e5ad630437873b7e9eb40525b43419726943b3536c52b41482b22dfca3f1`; judge final SHA-256 `13840d7b4fd8bfca427bac407971051c7ad88921c935f3e151af38f55d64746b`. Start, completed-worker and final-result journals stay immutable beside the seven qualification journals. Worker input 2 + 6791 + 0 = 6793, output 1480, `0.08393600000000001 USD` equivalent; judge 2 + 2228 + 0 = 2230, output 466, `0.027152 USD`; wall `23.36157074989751` s; subscription costs null. Seven CLI executions in all; no slot 1+, store write or extra call followed. Baseline 0 consumes no strike.

The floor is Unknown and acceptance unchecked; no benefit, retention or Human QA is claimed. The root assigned corrective TK-000Y and released no calls. Changed bytes require reviewed source, predecessor evaluation and a new frozen/calibrated series preserving this failure. This record grants no call or store-write authority.

## Receipt

| Run | Branch | HEAD SHA | Upstream | Dirty | Tests | Docs touched | Remaining gap | Checksum |
|---|---|---|---|---|---|---|---|---|
| 1 | feature/s002-qualification-results | 84756aca30632707c19f176e9e91f08f02dcf148 | none | 4 | Five actual frozen controls matched; slot0 worker complete, judge Unknown parse failure; remaining slots held | Task, Spec, existing intent Wiki | Strict judge-format failure; no noise floor/store rows; root correction decision required | 33c3213a77af9624247230b7408177412819ab48ddc291ea418aa1f8032cec62 |

## Old incomplete baseline publication

Under [JOT-680649a1-afb4-48a4-99e4-991cf3126be0](../../../../../../wiki/context-ams-purpose.md), only stopped/incomplete run **28** and Unknown result **41** were published (readback digest `68a1512b25d62903df21e1080f2a635658b2fc489e8bdc902d2cf58d25de57c7`). Its [publication proof](../../../../../../wiki/context-ams-purpose.md#tk-002-old-baseline-publication) keeps authority, payload, timing and privacy facts.
