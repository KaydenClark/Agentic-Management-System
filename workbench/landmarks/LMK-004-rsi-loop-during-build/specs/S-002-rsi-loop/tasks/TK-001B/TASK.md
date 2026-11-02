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

## Receipt

| Run | Branch | HEAD SHA | Upstream | Dirty | Tests | Docs touched | Remaining gap | Checksum |
|---|---|---|---|---|---|---|---|---|
| 1 | feature/s002-structured-judge | 179f8a1813d5378491c2e06f4c3f3df97d5c9bd1 | ahead 0 behind 0 | 0 | Source179f8a1 primary/fresh affected248 passed/1 skipped; exact local/fresh full786 passed/4 skipped (133.15s/133.01s); CI123 passed. Independent assembled-path review FAILED same private-evidence requirement: valid judge terminal then KeyboardInterrupt in finally close loses last_failure/privateDiagnostic and known terminal/usage. Proof SHA2561aaf62eb20c861438c0a635464c3bff88164dbffe9e584d3a287c7e6fb47e813. | TK-001B; S-002; TASKBOARD; held PR101 | STOP second private-evidence correction under three-strike rule.001A/001B retained; acceptance unmet, no further repair or merge. PR101 DRAFT/unmerged; source179 preserved unaccepted. Await fresh user authorization; corrective model/store calls0. Passing checks do not erase independent failure. | 07d29889e1fbf04cce0a4377b3ab7b2e07587d8243bd8ce38761b0830ada0663 |

## Stopped checkpoint — acceptance unmet

Independent assembled-path review proved the SAME private-evidence requirement still fails at `179f8a1813d5378491c2e06f4c3f3df97d5c9bd1`: an actual judge adapter consumes a valid success terminal with known usage, then transport.close raises KeyboardInterrupt from the adapter finally block. Its except cannot capture that cleanup exception; InterviewAdapter/Campaign retain one Unknown with null last_failure/privateDiagnostic and lose the known terminal/usage. The stream closes and no next query occurs. This is neither an unsafe accepted grade nor the completion naming question. Protected proof SHA256 `1aaf62eb20c861438c0a635464c3bff88164dbffe9e584d3a287c7e6fb47e813`.

Root invoked the explicit three-strike STOP. This second correction (001B) and first correction (001A) remain preserved with their source-specific history; Y/001A closures/PASS are not erased. Task001B remains incomplete with unchecked acceptance. No further source repair, callback workaround, model/store call or merge is authorized. PR101 is DRAFT/unmerged, source179 is unaccepted recovery, and a fresh user authorization is required before another corrective run. Primary/fresh full tests finished786/4 skipped and CI123 passed; those checks cannot erase the independent failure.

workerCompleted means normal worker-adapter return after full stream/protocol validation. A validated terminal followed by interruption retains available usage but does not establish that return; post-return context drift does establish return, while passed remains null. Existing successful integration cases establish those facts only within their tested boundaries; cleanup interruption remains unmet.

Smallest next proposal, NOT executed: bring cleanup exceptions into the producer evidence-capture boundary for both adapters, retain available partial/terminal facts before cleanup can interrupt, preserve the original interrupt and bounded owned-process cleanup, then test close-interruption through the actual adapter→Campaign→private-journal path. Keep invalid-context output quarantined, public metadata allowlisted and all semantic/tool/provider conditions unchanged. Confirm the analogous worker cleanup boundary rather than assuming it passes.
