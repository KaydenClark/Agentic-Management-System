# TK-000V - A caller delivers a large private prompt or receives a bounded transport refusal

**Task ID:** TK-000V
**Spec ID:** S-002
**Slice:** Bounded JSONL writes and concurrent runtime output drainage
**Status:** in-progress
**Blockers:** none
**Destination:** spec-acceptance: Evals; Readback
**Planned verification:** Inert full-pipe/partial-write/deadline regressions; runtime callers; required room checks; full fresh suite; checked PR #89 into main
**Claimed by:** s002-transport
**Current claimant:** s002-transport

## Assignment

The orchestrator assigned this corrective run after the late PR #89 transport finding, reserving TK-000V while S-006 separately owns TK-000U. Continue on `feature/s002-trial-preflight`, the existing unmerged PR. Preserve closed TK-000T and its historical receipt/review; this correction changes the transport candidate and requires affected review again. One writer owns the transport, tests, Task, S-002 owner and generated board. No model/authentication request, database fact, installed configuration change, S-006 edit or semantic qualification is authorized in this run.

Primary inert proof at source `2dae16cd989bbcd363a7c4eb12e1e30b08872d9d`: a child writes 262144 stderr bytes before reading stdin. Sending a 131072-byte synthetic prompt printed its start marker but failed to complete within the two-second outer deadline. The supervisor killed its own process group; no model/authentication call occurred. The blocking write/flush precedes the execution deadline and prevents stderr drainage. Existing short-prompt smoke and 45 focused tests did not exercise this failure.

Make initialize, control and execution writes nonblocking, drain stdout/stderr while writing, and start each bounded phase deadline before its send. Retain exact complete JSONL once across partial writes, actionable private refusal diagnostics and bounded process-group cleanup. Do not extend timeouts, introduce unbounded background writes or leak threads. Raw skill/prompt bytes remain private. The existing fixed model/tool checks, subscription-cost unknown, protected oracle and unreleased controlled series remain unchanged.

## Acceptance

- [ ] A realistic large synthetic private-context prompt arrives exactly once and complete despite partial pipe writes and simultaneous stderr/stdout output.
- [ ] A child that never reads stdin cannot stall past the send phase's deadline; control and execution share their deadline across write and response.
- [ ] Failure preserves an actionable private cause without recording prompt/stdout, and cleans the owned process group with no writer thread.
- [ ] Focused regressions and callers, required checks, fresh full suite and affected peer review bind the corrected immutable source before checked delivery.

## Continuing work

TK-000T remains historical bootstrap proof at its recorded revisions. TK-002 still owns qualified same-version noise; oracle calibration, controls, useful benefit and whole-Spec acceptance remain pending. A transport regression pass is not a provider/model trial or semantic qualification.
