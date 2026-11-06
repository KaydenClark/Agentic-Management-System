# TK-0031 - Recover the four RSI chart fixes on current dev

**Task ID:** TK-0031
**Spec ID:** S-007
**Slice:** Preserve the stopped record and verify the four existing fixes on current dev
**Status:** in-progress
**Blockers:** none
**Destination:** spec-acceptance: Comparable series, regressions, read states and traceability.
**Planned verification:** Preserve original TK-002L receipt rows byte-for-byte; satisfy record budgets; test timestamp, evidence and availability hash, grader isolation and run-only evidence; check actual bar contrast, responsive fixtures, build and required checks.
**Claimed by:** codex-rsi-recovery
**Current claimant:** codex-rsi-recovery

## Assignment

The owner authorized resuming PR165's bounded post-close budget stop and checking its existing chart fixes. Use the S-007 Spec branch into dev. Preserve TK-002L status, receipts, requirements and failed evidence; do not restart trials, call models, write production data or claim Human QA or improvement. Own S-007 records and RSI source/tests. Return exact candidate, checks and limits for independent review.

Merge provenance: PR165 head 1cbb969 merged dev 259b7a9. The canonical log writer verified the entire prior log was an exact prefix of dev's log; the merged log matches dev byte-for-byte, preserving all published rows.

## Acceptance

- [ ] TK-002L and S-007 fit their budgets without losing requirements, failures or changing native receipt rows.
- [ ] Candidate bars retain distinct fill and double borders in both themes.
- [ ] Freshness alone leaves the review hash stable; actual results and availability change it.
- [ ] Grader versions remain separate and visible; stopped or failed runs without result rows remain visible without fabricated results.
- [ ] Build, required checks and representative browser QA pass on the current-base candidate; evidence and limits are recorded.
