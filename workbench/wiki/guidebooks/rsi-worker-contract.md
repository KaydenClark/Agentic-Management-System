---
type: guidebook
status: active
sensitivity: normal
knowledge_role: curated
provenance:
  - TK-002M Stage A source inspection, 2026-11-04
source_paths:
  - src/ams/trial_runtime.py
  - src/ams/trial_campaign.py
  - src/ams/assessment_store.py
  - evals/ASSESSMENTS.md
last_verified: 2026-11-04
---

# RSI worker, recovery and checkpoint contracts

[S-000B](../../landmarks/LMK-004-rsi-loop-during-build/specs/S-000B-rsi-worker/SPEC.md) owns execution; [S-006](../../landmarks/LMK-002-rsi-presentation/specs/S-006-rsi-data-store/SPEC.md) owns durable truth. Worker/RPC/schema availability remains unproven. Stage A used no database, credential or model call.

## Implemented pre-model interfaces

The availability sentence above records Stage A on November 4. The later scoped launch and [TK-002P](../../landmarks/LMK-004-rsi-loop-during-build/specs/S-000B-rsi-worker/tasks/TK-002P/TASK.md) retain current bounded proof and failed checks. `ams.native_worker` now provides:

- `run_owned`: bounded byte IO, owned POSIX-group cleanup and interruption propagation. A denied disappearance probe remains unknown; only observed disappearance permits success.
- `NativeRpc` and `CodexHost`: one dedicated native server, strict bounded stdio and cancellation of its connection-scoped standalone commands before closing the server. Actual tool sessions can have separate process groups. Malformed completion retains ownership/unknown outcome; cancellation attempts cover all tracked commands, retaining failures and the original exception. Receipt2 records the independent cleanup Review FAIL; those repairs passed independent recheck. Receipt4 records a separate private-file FIFO failure; its correction passed independent bounded recheck. Refreshed exact-source no-model permissions, cancellation/controller SIGINT and synthetic crash/fresh-process recovery also pass. Real skill/model-turn proof remains held. Model-turn cleanup still needs its own proof.
- `PrivateEvidence`: exclusive, fsynced private execution artifacts outside the case tree; safe reconciliation returns identities/digests. Missing evidence remains unavailable. Reads open nonblocking and validate the descriptor before reading, so an owner-only FIFO cannot wait for a writer. Capture supplies no semantic grade.
- `run_slot`: consume an existing S-006 job using an independently retained job digest and matching executor input digest. Claims/fences/slots remain in S-006. Existing consumed slots reconcile without another invocation; this function never creates/renames campaigns or namespaces and always leaves assessment unknown. The caller supplies the qualified release and fresh gates.

Run `uv run pytest -q tests/test_native_worker.py tests/test_native_worker_live.py`. Actual isolated-store checks require an operator-supplied `AMS_LINEAGE_TEST_CONFIG` pointing to a private loopback configuration; otherwise those checks skip. They allocate distinct synthetic no-model controller identities, leaving the frozen grilling case and original attempt chain untouched. Preserve their rows and private failure evidence.

Native host checks additionally need independently pinned binary, permissions and runtime/source closure. The observed bounded profile keeps root/tmp/network denied and grants read access only to the case plus its pinned runtime; conflicting workspace-root denial and the cache-writing Apple interpreter shim failed and remain recorded. Use the host's supported profile/cancellation interfaces. Private operator replay scripts/captures remain with the Task evidence. Raw packets, paths, credentials and skill text never enter this guide or public projections. A read-only account/capacity snapshot and skill discovery establish neither actual model execution nor loaded skill use. The frozen real invocation retains its grader/labels/conditions/capacity gates.

## Accepted software continuation

The coordinator accepted bounded TK-002P thread/turn software continuation under the existing owner launch. Private plan SHA-256 `cf481230b48195dd5d1b3de5a2ab4ec56d64fd7742d6ba7beabc88d1dcd02cc1` binds the inspected proposal; it is not a call release. Preserve the original claim/baseline, guarded receipts, reviewed standalone/FIFO primitives and accepted O385 API.

Add a supported, bounded thread/turn executor with explicit pinned skill mapping, correlated events, held approval/user-input requests and incomplete captures. External release/readiness, source/fixture and effective connector/tool containment checks must pass before entering `run_slot` or consuming an intent; recheck critical gates immediately before `turn/start`. A purported normal completion requires a final response. Failed/interrupted/awaiting-input captures stay incomplete with assessment unknown; persistence does not establish semantic success. Unknown tool-tree cleanup cannot establish closed-success or a safe retry.

The software slice uses inert peers/processes and distinct synthetic isolated-store identities only. Actual host canaries need later coordinator release; no model, skill or grader call, frozen-case slot, install, source-skill change, held evaluator import, production write or main merge is included. Keep exact installed804 runtime sources and ed0 bytes, required hooks, private raw packets and safe store fields. Missing runtime-model/load/descendant evidence remains unknown. Native configuration and acknowledgments do not fill it. Draft193 and P remain open until their actual acceptance conditions hold.

## Component deadline failure

FAIL-215 records independent Review FAIL at immutable `cf85db03df69897d367cb59aacdcb1268534c273`: an inert peer delayed each reply by0.15s; execution/cancellation budgets were each0.3s, yet11 requests returned complete/cleanup-confirmed after1.779s. The source restarted preparation/revalidation budgets per RPC and reset unsubscribe time. The retained private reproducer/log are the RED evidence; no native model or skill call occurred.

The accepted minimal correction uses one monotonic total preparation/execution deadline and one separate aggregate cleanup deadline, with remaining time applied to each RPC, interrupt, unsubscribe and owned host close. Targeted red/green and final immutable retest evidence will be appended here. Prior failures, assessment runs, counters and no-model proof scopes remain intact; this is no trial reset or full P acceptance.

## Component MessagePhase failure

FAIL-217 records source/schema mismatch at `cf85db03df69897d367cb59aacdcb1268534c273`: parser and inert peer used unsupported `final`. Exact Codex0.159.3 generated MessagePhase is `commentary` or `final_answer`; null/missing is unknown. The offline experimental v2 schema is pinned by SHA-256 `e77b7d1436a78f431a74b2cb263a862e92ae40d70411bc63835b47ab2168827c`. No real host call was needed to establish the defect.

The schema-backed positive `final_answer` and negative unsupported `final` controls were RED before the minimal parser/peer correction, then GREEN together with the unknown-phase negative. Current coherent source/review evidence will be appended after the in-scope history and deadline changes freeze. Native loading, runtime identity, cleanup and semantic qualification remain separate unknowns.

## Component history input-binding failure

FAIL-219 records independent Review FAIL at `63200b1adc728685a9751c33e455cf5293db8184`: the history helper accepted one frozen userMessage plus an unapproved second userMessage through a presence/OR test. It returned observed while keeping the store unchanged, execution disallowed and assessment unknown. This remains a source binding defect. Required STOP/report retained both failed component candidates, cf85 and632; the two full632 suites (each967 passed/214 skipped) do not clear either independent failure.

The coordinator released one bounded same-Task recovery. `9cca984bccbab6a8ceef4219942199c23d78e376` changes exactly3 source lines to collect the complete ordered normalized input sequence and require its exact frozen singleton. Only documented empty text_elements normalization remains. Primitive/O/Task bytes and deadline/MessagePhase fixes stay unchanged.

The original independent reproducer remains byte-identical (SHA-256 `f51accd41df56cb9be8fab909da928cc1dbe74af17cee90e585667b80b2a6f1c`): observed/two inputs before, untrusted/no retry/store unchanged after. Exact-single, extra-before/after/after-final/across-page, duplicate, different, reordered, split and missing controls gave5 expected REDs/5 existing passes before the correction and all GREEN after. The targeted history set passes19; independent delta review and one corrected-candidate full/fresh check remain pending. No real call or qualification is implied.

## Checked software checkpoint

Product `9cca984bccbab6a8ceef4219942199c23d78e376` (native_turn module SHA-256 `c73d22386e94ae31c1b312b0287408dacf2edef2680d8e3e721cbd16a803b4d8`) passed independent bounded delta review: the unchanged extra-input reproducer returns untrusted, execution disallowed, assessment unknown and store unchanged; the reviewer's10 sequence controls pass. Earlier independent deadline/MessagePhase fixes retain their checked scope. The cf85/632 FAILs and FAIL-215/217/219 remain recorded.

Author history checks pass19. Exactly one corrected fresh-candidate full check at metadata `596f7976d29e122759aaacd4c51b1baf09812d57` (identical product) exits0 with977 passed/214 skipped; fresh render/doctor/next/layout/ADR/hygiene/whitespace/Taskboard checks pass and the checkout is clean. The separate prior author/fresh967 suites remain632 evidence; neither is relabeled as corrected-source qualification. Primitive/O bytes and guarded Task receipts stay unchanged.

This is checked pre-model software progress only. Actual native worker preflight/skill use/model-turn cleanup/runtime identity, exact approved labels/qualified grader/frozen conditions/current capacity and real-case result remain held. P stays open; protected O/PR175 publication and main merge remain separate.

A separately authorized one-shot read-only account/subscription check at2026-11-06T17:21:55Z verified unchanged binary/schema/runtime/config-source pins before launch, then stopped with PermissionError after attempting initialize. Effective containment was not established, so no account/meter request ran; authentication, subscription capacity and owned-process cleanup remain unknown. A supported read-only exact-binary process inventory found no candidates; without a retained owned PID that is not complete cleanup proof. No retry, thread, turn, command, tool, skill, model, grader or store write followed. Sanitized evidence stays private. A private-helper SyntaxError caught before execution and a default-context process-inventory EPERM remain separate harness/environment diagnostics, not model attempts. No capacity, reservation, semantic qualification or call authority follows.

## Verified source seams and gaps

At main `cfc0bc4c7f2cd167cea2972016edee076b479b73`, `trial_campaign.Campaign.run_one` journals before one released slot, refuses an attempted slot and requires its predecessor. It is not a durable multiworker scheduler. `trial_runtime.ClaudeAdapter` explicitly requires empty tools/MCP and rejects native tool use. Private source packs prove no native discovery/installation. Do not change its stopped protocol.

`assessment_store.py` and its exact-artifact migration preserve immutable canonical TEXT plus identity projection and predecessor digest, expected-head append, matching-prefix resume and divergent-prefix refusal. Existing scorer/store tests cover typed JSON identity, skipped/reset/fourth attempt rejection and duplicate artifacts. They do not implement the new lineage/job/export interfaces. `rsi_rows` has AMS/no-AMS/plain-instruction arms and run/result provenance; extend existing identities rather than create a competing tracker. Readback proves no qualification or benefit.

## Host invocation and evidence

Non-secret local help on 2026-11-04: Codex CLI `0.159.3` supports `exec --json --model MODEL -c model_reasoning_effort=EFFORT --sandbox workspace-write --cd FIXTURE --output-last-message FINAL PROMPT`; stdin `-` avoids shell-interpolated prompts. The effort key needs release-preflight validation. Claude Code `2.1.310` supports `--print --output-format stream-json --verbose --model MODEL --effort EFFORT --tools Read,Bash --allowedTools RULES --permission-mode dontAsk --permission-prompts none --strict-mcp-config --mcp-config EMPTY_JSON PROMPT`. Use the owned fixture cwd. These are unexecuted command shapes; verify tool rules and sandbox before release. Tool permission refusal stops the case, never triggers bypass flags.

Do not use permission/sandbox bypass, Claude `--bare` API-auth route, fallback models, provider switching or dollar caps. Existing subscription authentication remains within the trusted harness; do not forward provider API overrides or database credentials to the case process. Native user/project discovery must remain enabled when claimed, with all loaded instructions pinned. CLI version alone proves neither authentication, subscription availability, native skill/tool execution nor loaded identity. Failed local PATH-alias creation during help is a host limitation, not a model trial.

Before an authorized real-tool call, the worker owner proves sandbox/connector boundaries using synthetic canaries, validates an exact model/effort against actual runtime events, verifies binary and source hashes, and records an affirmative recent subscription-capacity observation with source/time/scope. No meter endpoint was verified in Stage A. Unknown/exhausted meter blocks new calls; resumption requires updated evidence, not another model or paid capacity. Unknown subscription cost/tokens stay null with reason/source, distinct from optional API-equivalent estimates. Mid/Small is default; High requires recorded need before freezing. Aliases prove no actual model identity.

Loading requires native discovery/load evidence, source/package/installed byte identities and independent observed use/end state. Separate declared/observed paths; public exports redact host paths and private originals stay local. Missing path/version observation remains Unknown; model self-report or a declared command argument cannot fill it. Each host adapter needs its own native proof; absence of one does not block an authorized other.

## Durable identity and release manifest

S-006/TK-002N supplies one linked graph: original failure occurrence + source revision/correction, immutable case version/digest, candidate revision/parent, frozen comparison, run/result, disposition, adoption receipt and eligible later use. Markdown owns intake; Supabase retains safe derived fields/pointers. A failure family and recurrence occurrence are different identities. Missing origin/qualification stays missing.

Before TK-002P or TK-002Q real execution, freeze campaign ID + explicit approval scope, existing Task/Spec IDs, baseline/current/candidate and skill closure identities, case/fixture + inventory/exclusions, grader/labels/qualification identities, host/binary/tools/permissions/model/effort, arms/order/repetitions/limits, usage availability and expected artifact release hashes. Bind each call to a unique execution slot. A new label/repair/campaign name does not reset the underlying failure/candidate attempt chain. Baseline is 0; candidate versions are 1–3. Worker and grader calls are separately journaled; a grader failure is neither a measured worker No nor permission to replay its worker.

## Claim, effect and recovery semantics

TK-002O implements atomic compare-and-swap claim with job ID, expected state version, claimant, bounded lease and fencing token. Allowed transitions distinguish ready, running, effect-uncertain, awaiting-evidence, completed, failed, blocked and stopped; they are operational states, not r1 verdicts. Expired lease transfers no permission to repeat an effect. Each side effect uses a stable effect key and intent receipt before execution, then observed remote/object identity and readback receipt after it. Duplicate intake/matching repeat return the same job/artifact; changed same-key payload refuses.

On crash after success but before receipt, a fresh worker queries the authoritative effect by its key and verifies payload/hash: matching success records recovered receipt; demonstrably absent permits only the still-authorized pending action; unavailable or conflicting outcome becomes effect-uncertain/blocked. Never infer absence from a timeout. Stale fences cannot append/publish. Reserve a model slot before spawning; unknown completion consumes no new slot and cannot be rerun blindly. Retain every actual candidate attempt and partial evidence. Failed candidate three stops; baseline/transport reconciliation never erases history. Stop/approval/meter state is checked again before each new call/effect.

## Safe export and restore

TK-002O exports allowlisted safe lineage/job/receipt projections with schema/reader revision, export ID, namespace, exact record IDs, per-record canonical byte digest, predecessor/head, completeness boundary/counts and manifest digest. Raw assessment packets/transcripts, prompts/labels/private locators/host paths/secrets never enter Git. A redacted checkpoint restores only its declared safe projection and operational identities; unavailable private evidence remains missing and cannot be recreated or qualify a result. Complete means complete for that declared projection, not a full private evidence backup.

Restore validates hashes, graph closure/counts, schema/reader, sources, namespace and expected head before writing. Empty compatible destination may reconstruct identical safe identities; matching destination is a no-op; strict matching-prefix append requires expected-head fencing and full validation. Partial, unsupported, stale-divergent, changed same-ID bytes, absent parents and private fields refuse atomically, with no overwrite, renumber or attempt reset. Outage leaves local evidence pending, unpublished. Reconcile against Supabase before replay; Git export is recovery only, never a parallel writable authority.

<!-- jot-entry -->
### JOT-d04bb644-433f-4c2a-9817-a147e0e1f0f2
Kind: intent
State: confirmed
Recorded: 2026-11-06T11:18:06.741Z
Author: Kayden (captured by Codex S000B writer)
Source: Kayden, current AMS twelve-outcome execution request item5 and two-confirmation correction
Topic: rsi-worker-contract
Supersedes: none

Exact owner item5 in the current twelve-outcome /Orchestrate and /carry request:

"Implement and prove the native worker—S-000B/TK-002P.
Use the frozen grilling-native-resume-v1 development case; I verified its recorded SHA-256. Implement a real-tool adapter under the existing host’s supported permissions. Prove process cleanup—including interruption—before trusting its lifecycle. Keep the stopped PR #101 campaign stopped.
Pass condition: a real native invocation loads the identified skill, uses the permitted tools, preserves unrelated files, and resumes in a fresh process without repeating a consumed execution slot.
The installed CLIs are present. Their versions alone do not prove authentication, subscription capacity, or model/skill loading."

This records the existing confirmed S-000B/TK-002P implementation launch, not another confirmation request or delivery judgment. Preserve r1, its three assessment runs, initial candidate -> retry -> retry -> stop with baseline excluded, existing stops and all prior evidence. Neither a new Task nor campaign name resets exhausted attempts. Candidate agents receive no credentials, protected grader material or publication authority. Keep unrelated work and active Wiki/Board writers untouched.

Implementation consumes the exact verified S-006 job/recovery artifact after its named checks; whole-Spec completion and TK-002Q execution are not prerequisites. Before model calls, independently freeze the exact host/model, sources, qualified protected grader, applicable owner-approved semantic labels, case/controls/repetitions, useful-effect margin, uncertainty method and available subscription capacity. Unknown/exhausted capacity, required approval and explicit stop remain stopping boundaries. No paid fallback, personal installation, stopped-PR101 repair/restart or production promotion is granted here. Actual Human QA and owner-controlled dev-to-main promotion remain separate.
<!-- /jot-entry -->
