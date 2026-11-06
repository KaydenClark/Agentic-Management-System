# S-000B - Resumable RSI worker

**Spec ID:** S-000B
**Status:** active
**Priority:** 1
**Owner:** Kayden
**Stance:** Builder
**Updated:** 2026-11-06
**Catalog description:** Local Python execution and recovery for authorized RSI campaigns, with durable Supabase state.
**Blockers:** none for mapping
**Confirmation:** [JOT-d04bb644-433f-4c2a-9817-a147e0e1f0f2](../../../../wiki/guidebooks/rsi-worker-contract.md#jot-d04bb644-433f-4c2a-9817-a147e0e1f0f2)
**Execution approval:** [JOT-d04bb644-433f-4c2a-9817-a147e0e1f0f2](../../../../wiki/guidebooks/rsi-worker-contract.md#jot-d04bb644-433f-4c2a-9817-a147e0e1f0f2)
**Next gate:** TK-002P implements and checks the pre-model adapter/cleanup; actual calls retain the frozen case/grader/label/conditions/capacity gates.

## Intent and authority

[Owner intent](../../../../wiki/context-feedback-improvement-loop-plan.md#current-mapped-destination) places the RSI Loop at LMK-004 and permits capability separation. Supabase Free stores durable state; Python executes outside it. The owner uses subscription meters, not API-dollar budgets. The later scoped owner launch above releases TK-002P implementation, preserving the Stage A contracts and actual-call prerequisites. No stopped campaign is restarted.

## Outcome

An authorized campaign continues through eligible work without the owner launching every step. A fresh worker resumes durable state after interruption without duplicate effects, lost evidence or reset attempts.

## Why It Matters

A database of results alone does not execute the loop. Session-bound coordination leaves the owner relaying work and cannot reliably recover crashes or ambiguous external writes.

## Current Verified State

Worker criteria remain unverified. Existing trial_campaign.run_one executes one released slot; the narrow trial_runtime adapter is tool-free. These are reusable seams, not proof of real-tool execution or autonomous recovery. The coordinator released S-006 recovery artifact `3856614eeb8ec2e158db003025a7a75ee29bfc2f` after its isolated SQL/PostgREST checks, independent Standards/Spec rechecks and [full CI](https://github.com/KaydenClark/Agentic-Management-System/actions/runs/42207150002). This supplies the named dependency, not whole-S006 acceptance, production storage, worker proof or a model-call release.

## Desired Behavior

- Start locally in Python using supported Codex/Claude harnesses and isolated workspaces, with actual tools needed by each case. Host availability is visible; Supabase availability does not imply a running worker. Always-on hosting and paid upgrades are not authorized.
- Consume S-006 durable jobs referencing existing Spec/Task scope, frozen S-002 contracts, exact sources and campaign authorization. Reuse existing records rather than create a second project tracker.
- Record actual provider/model/effort, host and loaded skill identities. Use Mid/Small by default, High when needed with reason recorded. Freeze conditions within comparisons; preserve older campaign pins. Author and deciding evaluator are independent; accepted-version graders cannot be edited by the candidate.
- Continue eligible stages within campaign authority; stop at required approval, meter unavailability/exhaustion, explicit stop or attempt exhaustion. Never silently purchase API capacity or switch models to continue. Unknown meter state is explicit and does not justify an unlimited run.
- Preserve initial attempt -> retry -> retry -> stop, baseline excluded. Rename, repair, restart and re-delivery cannot reset counters. Transport recovery is distinct from another model execution; uncertain completion is reconciled before retry, and every actual attempt remains visible.
- Atomic claims, bounded ownership and progress receipts prevent simultaneous writers. After interruption, determine whether work completed, failed or has an unknown outcome; recover evidence or block for resolution before replaying effects. Duplicate notifications cannot create duplicate jobs, commits or result rows.
- Operational recovery, candidate revision and adoption monitoring have separate states. A grader failure is not a measured skill failure or pass. A merge is not installation or actual host loading. Installation follows separately scoped authority.
- Keep credentials in trusted execution/writer boundaries; candidate agents cannot access private graders, database secrets or unrestricted publication. Preserve sandbox rules and unrelated work. Short scheduling/queue mechanisms are optional implementation choices, not mandates for new services.

## Decisions And Contracts

S-002 owns qualification and useful-benefit decisions, S-006 authoritative data, S-011 source delivery, S-013 detection, and S-007 public views. The local Board surfaces consequential owner decisions. S-012 remains the general Python lifecycle CLI; this Spec does not replace it.

## Non-Goals

New scoring rules, model training, automatic personal installation, cross-project rollout, production deployment, resuming stopped campaigns or purchasing inference/hosting.

## Dependencies And Blockers

Real execution needs supported harness authentication, appropriate local tools, writable isolated state, an authorized campaign, S-002 contracts and S-006 persistence. Missing inputs block only their consumer. Website completion is not a prerequisite to independent worker verification.

## Vertical Implementation Slices

TK-002P consumes the [worker contract](../../../../wiki/guidebooks/rsi-worker-contract.md), exact verified S-006 recovery API and frozen Stage A fixture. Pre-model implementation is released; calls require the independently frozen and verified conditions in those owners. TK-002Q execution is not a prerequisite.

## Acceptance Criteria

- [ ] **Real execution:** a case needing Git/filesystem tools reaches its verified end state with actual loaded skill identity. A text-only success claim fails.
- [ ] **Continuation:** one campaign advances eligible stages without repeated initiation; a fresh process recovers the same identities. A chat-only handoff fails.
- [ ] **Idempotence:** duplicate delivery and competing claims cause one logical effect. Crash after external success but before receipt must reconcile; blind replay fails.
- [ ] **Limits:** injected exhaustion, unknown meter, explicit stops and third failed attempt stop correctly. Fourth attempts, silent provider/model fallback or paid API calls fail.
- [ ] **Evidence:** successful, failed and interrupted work persists with stage, exact source and actual execution identity. Worker success with unknown grading cannot become a pass.
- [ ] **Authority:** qualified merge eligibility follows existing gates; installation still requires its own authority. Candidate access to secrets/graders or stopped-campaign restart fails.
- [ ] **Availability:** sleeping host/database outage yields truthful blocked/pending state and recoverable evidence, not completed execution or publication.

## Testing Seams

Harness adapter, job claim/receipt, source identity, state reconciliation and S-006 writer/readback. Exercise duplicate trigger, process termination, uncertain write, unavailable meter and a planted regression under the intended host conditions. Native checks and isolated fresh-candidate verification precede delivery; model trials require their campaign authority.

## Documentation Impact

RUNBOOK will name supported worker operations when implemented; Wiki explains ownership and recovery, and S-006/S-007 consume truthful worker state.

## Review and Human QA

Independent review covers the exact candidate; actual owner judgment evaluates unattended operation. Neither this map nor static checks supply those receipts.

## Completion Result

Pending.
