# S-000B - Resumable RSI worker

**Spec ID:** S-000B
**Status:** planned
**Priority:** 1
**Owner:** Kayden
**Stance:** Builder
**Updated:** 2026-11-07
**Catalog description:** Python campaign execution/recovery with durable Supabase state.
**Blockers:** none for mapping
**Confirmation:** Current destination supplied by the owner’s 2026-11-07 Map request; linked source retains prior confirmed decisions.
**Execution approval:** none for implementation; Map/Plan preparation only.
**Next gate:** Plan reconciles prepared TK-002P and Stage A contracts with the Servitor observer/repair destination; implementation requires a later scoped launch.

## Intent and authority

[RSI Map source](../../../../wiki/context-feedback-improvement-loop-plan.md#jot-7862917b-48cb-41bc-8f21-0ddfc611cdac); no execution release or reset of prior stops.

[Owner intent](../../../../wiki/context-feedback-improvement-loop-plan.md#current-mapped-destination) places the RSI Loop at LMK-004 and permits capability separation. Supabase Free stores durable state; Python executes outside it. The owner uses subscription meters, not API-dollar budgets. This Spec maps the worker; TK-002P is prepared and held. No stopped campaign is restarted.

## Outcome

Authorized campaigns continue without repeated owner initiation; fresh workers resume without duplicate effects, lost evidence or reset attempts.

## Why It Matters

Durable execution removes owner relaying and recovers crashes/uncertain writes; stored results alone do not execute a loop.

## Current Verified State

All criteria remain unverified. trial_campaign.run_one executes one released slot; trial_runtime is tool-free. Neither proves real-tool execution or autonomous recovery.

## Desired Behavior

- Run locally in Python on Servitor with supported Codex/Claude harnesses, isolated workspaces and actual case tools. Expose host availability; a database is not a worker. No always-on hosting or paid upgrade is authorized.
- A per-chat event-driven observer distinguishes skill request, loading, use and failure, with chat/event and observed version identities. Unknown/interrupted observation cannot become success. S-013 classifies/detects; S-006 stores shared history.
- Routine repair starts after current work finishes; blocking repair uses a separate chat. At most one repair is active per skill across participating chats. Duplicate triggers join its history; completion, ownership and attempts survive interruption.
- Test draft and related skills in a separate real AMS website session on Servitor. Preserve loaded identities and task end state; do not replace everyday skills before eligible merge.
- Workbench setup and skill use remain independent of optional RSI. No silent enrollment, observation or credential/Supabase requirement for nonparticipants.
- Consume S-006 durable jobs linked to existing Spec/Task scope, frozen S-002 contracts, sources and campaign authority. No second tracker. Record actual provider/model/effort, host and loaded versions; Mid/Small default, High with reason, conditions frozen within comparisons. Preserve older pins; author and deciding evaluator are independent, with candidate-inaccessible accepted-version graders.
- Continue only within campaign authority; stop at approvals, unavailable/exhausted meters, explicit stops or exhausted attempts. Unknown capacity is not unlimited. No silent paid calls or model/provider substitution. Baseline excluded: initial → retry → retry → stop. Rename, repair, restart or redelivery resets nothing.
- Separate transport recovery from model attempts. Reconcile uncertain completion before replay; retain every actual attempt. Atomic bounded claims/progress receipts prevent concurrent writers, duplicate jobs, commits or result rows. Recover evidence or block when an interrupted effect is unknown.
- Recovery, candidate revision and adoption monitoring have distinct states. Grader failure is neither measured skill failure nor pass. Under S-011, eligible merged repairs automatically update everyday Servitor skills, with source/install/later-loading evidence; Map installs nothing. Other scopes need their own authority.
- Keep credentials inside trusted execution/writer boundaries; candidates cannot access private graders, secrets or unrestricted publication. Preserve sandbox rules and unrelated work. Scheduling implementation need not introduce a service.

## Decisions And Contracts

S-002 owns qualification and useful-benefit decisions, S-006 authoritative data, S-011 source delivery, S-013 detection, and S-007 public views. The local Board surfaces consequential owner decisions. S-012 remains the general Python lifecycle CLI; this Spec does not replace it.

## Non-Goals

Defining scoring rules (S-002), model training, installation before eligible merge, deployment beyond the Servitor proof, production promotion, resuming stopped campaigns or purchasing inference/hosting.

## Dependencies And Blockers

Execution needs authenticated supported harnesses/tools, isolated writable state, campaign authority, S-002 contracts and S-006 persistence. Missing inputs block only consumers; website completion is not required for independent worker checks.

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

Independent review names the candidate; owner judgment evaluates unattended operation. Map/static checks supply neither.

## Completion Result

Pending.
