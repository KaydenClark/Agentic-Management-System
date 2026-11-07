# S-000B - Resumable RSI worker

**Spec ID:** S-000B
**Status:** planned
**Priority:** 1
**Owner:** Kayden
**Stance:** Builder
**Updated:** 2026-11-07
**Catalog description:** Local Python execution and recovery for authorized RSI campaigns, with durable Supabase state.
**Blockers:** none for mapping
**Confirmation:** Current destination supplied by the owner’s 2026-11-07 Map request; linked source retains prior confirmed decisions.
**Execution approval:** none for implementation; Map/Plan preparation only.
**Next gate:** Plan reconciles prepared TK-002P and Stage A contracts with the Servitor observer/repair destination; implementation requires a later scoped launch.

## Intent and authority

[Current RSI destination](../../../../wiki/context-feedback-improvement-loop-plan.md#jot-7862917b-48cb-41bc-8f21-0ddfc611cdac) maps the Servitor proof and optional participation. This updates requirements only: no Task activation, model trial, database write or installation occurs through Map. Existing receipts, frozen comparisons and stopped attempts retain their scope.


[Owner intent](../../../../wiki/context-feedback-improvement-loop-plan.md#current-mapped-destination) places the RSI Loop at LMK-004 and permits capability separation. Supabase Free stores durable state; Python executes outside it. The owner uses subscription meters, not API-dollar budgets. This Spec maps the worker; TK-002P is prepared and held. No stopped campaign is restarted.

## Outcome

An authorized campaign continues through eligible work without the owner launching every step. A fresh worker resumes durable state after interruption without duplicate effects, lost evidence or reset attempts.

## Why It Matters

A database of results alone does not execute the loop. Session-bound coordination leaves the owner relaying work and cannot reliably recover crashes or ambiguous external writes.

## Current Verified State

All criteria are unverified. Existing trial_campaign.run_one executes one released slot; the narrow trial_runtime adapter is tool-free. These are reusable seams, not proof of real-tool execution or autonomous recovery. No worker acceptance is claimed.

## Desired Behavior

- A per-chat Python observer records skill requests, loading, actual use and failures as distinct evidence, with chat/event identity and observed source version. It reacts to available session events; unavailable or interrupted observation is explicit, never invented success. S-013 owns detection/classification and S-006 durable shared history.
- The orchestrator starts routine repair after the current work finishes; blocking repair proceeds in a separate chat. One repair may be active per skill across participating chats; duplicate triggers join its history rather than create competing repairs. Completion and ownership must survive interruption.
- The first proof runs on Servitor. Draft and related skills run in a separate AMS website test session. Keep candidate loading isolated from everyday skills until qualified merge; preserve actual loaded identities and the website task end state.
- Workbench setup does not require RSI. Participation enables observer/repair behavior explicitly; no silent observation, credentials or Supabase account requirement for ordinary skill use.


- Start locally in Python using supported Codex/Claude harnesses and isolated workspaces, with actual tools needed by each case. Host availability is visible; Supabase availability does not imply a running worker. Always-on hosting and paid upgrades are not authorized.
- Consume S-006 durable jobs referencing existing Spec/Task scope, frozen S-002 contracts, exact sources and campaign authorization. Reuse existing records rather than create a second project tracker.
- Record actual provider/model/effort, host and loaded skill identities. Use Mid/Small by default, High when needed with reason recorded. Freeze conditions within comparisons; preserve older campaign pins. Author and deciding evaluator are independent; accepted-version graders cannot be edited by the candidate.
- Continue eligible stages within campaign authority; stop at required approval, meter unavailability/exhaustion, explicit stop or attempt exhaustion. Never silently purchase API capacity or switch models to continue. Unknown meter state is explicit and does not justify an unlimited run.
- Preserve initial attempt -> retry -> retry -> stop, baseline excluded. Rename, repair, restart and re-delivery cannot reset counters. Transport recovery is distinct from another model execution; uncertain completion is reconciled before retry, and every actual attempt remains visible.
- Atomic claims, bounded ownership and progress receipts prevent simultaneous writers. After interruption, determine whether work completed, failed or has an unknown outcome; recover evidence or block for resolution before replaying effects. Duplicate notifications cannot create duplicate jobs, commits or result rows.
- Operational recovery, candidate revision and adoption monitoring have separate states. A grader failure is not a measured skill failure or pass. A merge is not installation or actual host loading. For this mapped loop, eligible merged repairs automatically update everyday Servitor skills under S-011; Map itself performs no installation. Other installation scopes retain their own authority.
- Keep credentials in trusted execution/writer boundaries; candidate agents cannot access private graders, database secrets or unrestricted publication. Preserve sandbox rules and unrelated work. Short scheduling/queue mechanisms are optional implementation choices, not mandates for new services.

## Decisions And Contracts

S-002 owns qualification and useful-benefit decisions, S-006 authoritative data, S-011 source delivery, S-013 detection, and S-007 public views. The local Board surfaces consequential owner decisions. S-012 remains the general Python lifecycle CLI; this Spec does not replace it.

## Non-Goals

Defining scoring rules (S-002), model training, installation before eligible merge, deployment beyond the Servitor proof, production promotion, resuming stopped campaigns or purchasing inference/hosting.

## Dependencies And Blockers

Real execution needs supported harness authentication, appropriate local tools, writable isolated state, an authorized campaign, S-002 contracts and S-006 persistence. Missing inputs block only their consumer. Website completion is not a prerequisite to independent worker verification.

## Vertical Implementation Slices

TK-002P consumes the [worker contract](../../../../wiki/guidebooks/rsi-worker-contract.md) and frozen Stage A fixture; implementation stays held.

## Acceptance Criteria

- [ ] **Scheduling:** routine work completes before repair; a blocking failure receives a distinct repair chat. Two chats reporting the same skill cannot produce concurrent repairs. Crash/restart preserves the active claim and attempt history.
- [ ] **Observation and isolation:** requested-but-unused is retained for Critical classification, unavailable observation is visible, and draft test use cannot overwrite everyday skills before qualification/merge.
- [ ] **Optional setup:** a nonparticipating Workbench still uses shared skills without RSI collection or credentials.


- [ ] **Real execution:** a case needing Git/filesystem tools reaches its verified end state with actual loaded skill identity. A text-only success claim fails.
- [ ] **Continuation:** one campaign advances eligible stages without repeated initiation; a fresh process recovers the same identities. A chat-only handoff fails.
- [ ] **Idempotence:** duplicate delivery and competing claims cause one logical effect. Crash after external success but before receipt must reconcile; blind replay fails.
- [ ] **Limits:** injected exhaustion, unknown meter, explicit stops and third failed attempt stop correctly. Fourth attempts, silent provider/model fallback or paid API calls fail.
- [ ] **Evidence:** successful, failed and interrupted work persists with stage, exact source and actual execution identity. Worker success with unknown grading cannot become a pass.
- [ ] **Authority:** qualified merge eligibility follows existing gates; automatic everyday update follows qualified merge within the approved repair scope. Candidate access to secrets/graders or stopped-campaign restart fails.
- [ ] **Availability:** sleeping host/database outage yields truthful blocked/pending state and recoverable evidence, not completed execution or publication.

## Testing Seams

Harness adapter, job claim/receipt, source identity, state reconciliation and S-006 writer/readback. Exercise duplicate trigger, process termination, uncertain write, unavailable meter and a planted regression under the intended host conditions. Native checks and isolated fresh-candidate verification precede delivery; model trials require their campaign authority.

## Documentation Impact

RUNBOOK will name supported worker operations when implemented; Wiki explains ownership and recovery, and S-006/S-007 consume truthful worker state.

## Review and Human QA

Independent review covers the exact candidate; actual owner judgment evaluates unattended operation. Neither this map nor static checks supply those receipts.

## Completion Result

Pending.
