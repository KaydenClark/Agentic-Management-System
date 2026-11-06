# TK-000V - A caller delivers a large private prompt or receives a bounded transport refusal

**Task ID:** TK-000V
**Spec ID:** S-002
**Slice:** Bounded JSONL writes and concurrent runtime output drainage
**Status:** done
**Blockers:** none
**Destination:** spec-acceptance: Evals; Readback
**Planned verification:** Inert full-pipe/partial-write/deadline regressions; runtime callers; required room checks; full fresh suite; checked PR #89 into main
**Claimed by:** s002-transport
**Current claimant:** s002-transport
**Proof:** 50 focused; fresh 567/4 skip; actual inert adapter

## Assignment

The orchestrator assigned this corrective run after the late PR #89 transport finding, reserving TK-000V while S-006 separately owns TK-000U. Continue on `feature/s002-trial-preflight`, the existing unmerged PR. Preserve closed TK-000T and its historical receipt/review; this correction changes the transport candidate and requires affected review again. One writer owns the transport, tests, Task, S-002 owner and generated board. No model/authentication request, database fact, installed configuration change, S-006 edit or semantic qualification is authorized in this run.

Primary inert proof at source `2dae16cd989bbcd363a7c4eb12e1e30b08872d9d`: a child writes 262144 stderr bytes before reading stdin. Sending a 131072-byte synthetic prompt printed its start marker but failed to complete within the two-second outer deadline. The supervisor killed its own process group; no model/authentication call occurred. The blocking write/flush precedes the execution deadline and prevents stderr drainage. Existing short-prompt smoke and 45 focused tests did not exercise this failure.

Make initialize, control and execution writes nonblocking, drain stdout/stderr while writing, and start each bounded phase deadline before its send. Retain exact complete JSONL once across partial writes, actionable private refusal diagnostics and bounded process-group cleanup. Do not extend timeouts, introduce unbounded background writes or leak threads. Raw skill/prompt bytes remain private. The existing fixed model/tool checks, subscription-cost unknown, protected oracle and unreleased controlled series remain unchanged.

## Acceptance

- [x] A realistic large synthetic private-context prompt arrives exactly once and complete despite partial pipe writes and simultaneous stderr/stdout output.
- [x] A child that never reads stdin cannot stall past the send phase's deadline; control and execution share their deadline across write and response.
- [x] Failure preserves an actionable private cause without recording prompt/stdout, and cleans the owned process group with no writer thread.
- [x] Focused regressions and callers, required checks, fresh full suite and affected peer review bind the corrected immutable source before checked delivery.

## Continuing work

TK-000T remains historical bootstrap proof at its recorded revisions. TK-002 still owns qualified same-version noise; oracle calibration, controls, useful benefit and whole-Spec acceptance remain pending. A transport regression pass is not a provider/model trial or semantic qualification.

## Check and corrective evidence

The four initial regressions failed under the outer watchdog before the repair; the successful-large-prompt case directly reproduces the original deadlock. After correction, five new cases and the existing callers pass together: 50 focused tests. They cover a 131072-byte prompt with 64 simultaneous stdout frames and a stderr flood, exact complete JSONL hash with no duplicate bytes, nonreading initialize/MCP/execution peers, bounded private refusal/cleanup and the combined write/reply deadline. No provider/authentication request occurred; the inert harness replaces those endpoints before constructing the transport.

The implementation uses nonblocking descriptor writes and a shared selector to drain both output pipes during partial writes. Each phase computes its absolute deadline before serializing/sending its request; receive consumes the same deadline. Existing 15-second control and 55-second execution budgets are preserved. At corrected source `5467b5e3715fd229d260b064c2250d36c54b4068`, both primary and fresh full suites passed: 567 passed, 4 skipped. A separate noncontributor context independently passed all 50 focused tests and found no unresolved affected-transport issue. Render exposed a stale generated claim projection; the owner records were correct, and the board was regenerated before final publication. Doctor, layout, next and diff checks passed. Final closure records still require their exact-head CI before merge.

## QA and runtime observation

Inert QA demonstrates exact complete single delivery under simultaneous stdout/stderr floods and partial pipe writes; nonreading peers refuse with retained private stderr/stage and an exited owned process. The combined-deadline test refuses rather than restarting its budget after sending. The outer regression watchdog can clean both owned process groups even against the original blocked implementation.

The orchestrator additionally authorized exactly one inert actual adapter call at source `5467b5e`: `PREFLIGHT_OK`, exact `claude-opus-5-5`, medium effort, empty tools/MCP. All four loaded source hashes matched the authorized commit before the call. Usage: input 2, output 13, cache read 1545, cache creation 798. API list-equivalent cost: 0.006961 USD; actual subscription spend unknown. The safe local execution-fact digest `44d1843eecc48fe529c19ae3604f67fbcfe8e462f46fe83307c78616390fd548` matched readback. No private skill input, database fact, semantic qualification or controlled trial was involved. TK-000T's earlier source/smoke/review remain historical; they are not substituted for this corrective evidence.

CI run 75 (`41351943803`) passed all 567 tests with 4 skips, then failed the record-currentness gate on the same stale TASKBOARD claim row seen locally. Its job log directly shows the ready/in-progress row diff. The regenerated board is included in this correction; final-head CI must confirm that repair. No test failure is hidden or waived.

## Receipt

| Run | Branch | HEAD SHA | Upstream | Dirty | Tests | Docs touched | Remaining gap | Checksum |
|---|---|---|---|---|---|---|---|---|
| 1 | feature/s002-trial-preflight | ce0a585b52522cb9f3f9d9daeabd3142fe24a6d9 | ahead 0 behind 0 | 0 | 50 focused; fresh 567/4 skip; actual inert adapter | evals/TRIALS.md | Oracle/noise/controls/benefit; close attribution: {"agent":"s002-transport","claimant":"s002-transport","onBehalfOf":null} | 450ae1c87581a9c82a53b5c03bf147da88aa2e8b4be72afb032eda35a1243fd3 |
