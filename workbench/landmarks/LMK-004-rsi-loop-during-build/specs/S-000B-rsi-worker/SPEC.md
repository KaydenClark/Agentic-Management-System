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

<!-- workbench-record-section max=7000 -->
- [Part 1](SPEC.md.part-desired-behavior-001.96f6135312720946cc99b2d433275769d94ba69116a9fdc44b3d7619f1e90ae6.md)
<!-- /workbench-record-section -->

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
