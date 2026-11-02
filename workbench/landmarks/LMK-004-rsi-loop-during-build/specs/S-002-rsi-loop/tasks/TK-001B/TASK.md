# TK-001B - Actual interrupted or context-invalid executions retain their available private evidence without becoming grades

**Task ID:** TK-001B
**Spec ID:** S-002
**Slice:** Actual interrupted or context-invalid executions retain their available private evidence without becoming grades
**Status:** in-progress
**Blockers:** none
**Destination:** spec-acceptance: Evals; Readback
**Planned verification:** Actual worker/judge adapters with inert transports through Campaign; cancellation/post-return drift/private readback/stop/privacy; affected/current CI and assembled-path peer review; no actual calls
**Claimed by:** s002-interruption-evidence
**Current claimant:** s002-interruption-evidence

## Assignment

Root authorized this fresh bounded run on 2026-11-02 after final PR101 review proved two remaining private evidence losses. Actual judge interruption bypasses Exception capture; post-return context drift discards completed execution/usage. Primary inert reproductions confirmed both. Native next-id proposes TK-001B. Preserve closed Y/001A, their source-bound scoped PASS/receipts, old source/artifact histories and actual stopped baseline. Same held PR101/feature lane.

This is the SECOND corrective run for private-evidence retention. If it still fails that same requirement, stop/report both correction attempts under the three-strike rule instead of iterating again. Fix producer → Campaign → phase journal coherently: capture real KeyboardInterrupt partial metadata in judge and worker adapters without swallowing interruption; retain returned execution/role when post-query context validation fails. Worker process completion and known available usage stay truthful; passed remains null and context-invalid judge output stays quarantined/unaccepted. No semantic/prompt/parser/tool/permission change, row mutation, model call, schema change or broad logging framework.

Causal integration tests must use actual adapters with inert transports, not callbacks prepopulating last_failure. Cover partial interruption, returned execution/context drift, exact protected readback, no next query, truthful completion/measurement availability and planted public marker exclusions. Peer review the assembled failure path proportionately. Publish immutable source/freeze and appropriate checks before checked main engineering delivery; actual compatibility/new qualification remain separately unreleased, TK-002 incomplete.

## Acceptance

- [ ] Actual worker/judge interruption captures available partial/terminal facts, rethrows cancellation and closes the owned transport.
- [ ] Context-invalid returned executions/roles survive private journal readback, worker completion/known usage remain truthful and no invalid grade or next query is accepted.
- [ ] Private markers stay outside public rows/metric reasons; causal affected/current checks and assembled-path peer review pass, with actual calls still held.

## Progress

Nine actual-adapter/Campaign integration cases reproduced the missing private evidence before implementation. The coherent producer/campaign/journal correction now passes all nine: qualification/worker/grader crossed with partial interruption, interruption after a validated terminal, and post-return context drift. Exact private facts, role/return state, known usage/process completion, Unknown/quarantined judge outputs, owned stream closure, no replay/next query and fake-store public marker privacy are checked. Primary affected248 passed/1 skipped. Two initial no-next-slot assertions expected missing-prior-result, but drift is refused earlier by context validation; only that expected exception was corrected, with no source change or extra query. No post-fix private-evidence assertion failed. Existing worker diagnostic-file content assertions remain, adapted to the explicit private envelope. Independent assembled-path review, immutable source/freeze/current checks and delivery are next; no actual calls/store writes.
