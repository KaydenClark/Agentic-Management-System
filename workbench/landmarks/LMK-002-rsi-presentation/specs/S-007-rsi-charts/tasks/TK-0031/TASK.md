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

Workspace baseline sha256:7a1c61ba565d56e09c7be07037d60c7c39306f09d1b941d2b2256c14c93d31ee

## Acceptance

- [x] TK-002L and S-007 fit their budgets without losing requirements, failures or changing native receipt rows.
- [x] Candidate bars retain distinct fill and double borders in both themes.
- [x] Freshness alone leaves the review hash stable; actual results and availability change it.
- [x] Grader versions remain separate and visible; stopped or failed runs without result rows remain visible without fabricated results.
- [x] Build, required checks and representative browser QA pass on the current-base candidate; evidence and limits are recorded.

## Receipt

| Run | Branch | HEAD SHA | Upstream | Dirty | Tests | Docs touched | Remaining gap | Checksum |
|---|---|---|---|---|---|---|---|---|
| 1 | Feature/S-007-rsi-chart-pages | b8ee5fcfc16d31d3c800e73e67ed4af93c6297a0 | ahead 131 behind 0 | 0 | Focused chart tests 4/4, build and 267 site tests passed. Root and site hygiene 0 after offline dependency install; layout valid. Initial uv --no-sync hygiene could not spawn from empty environment. Sandboxed Chrome browser check exited SIGABRT with cleanup EPERM before assertions; second unexpected verification failure, stopped. | TK-002L condensed; original receipt rows unchanged. | Browser QA, full Python, fresh-candidate checks, CI, review and dev containment remain. | da20302f37cc263d8fd06144caf333381e88ae2c5d17b33502bc434f0db2d654 |

## Assembled verification

Source aa5f811 merges dev63870b5; the S-003 writer preserved all Jot blocks from both parents. Fresh build and 279 site tests pass; Chrome contrast and planted solid-fill negative pass in light, dark and system-dark; run-only fixtures pass at 375/1280 in both themes. Root and built-site hygiene 0; 37 hygiene tests, Wiki/ADR/layout/render and candidate whitespace pass. Earlier source15ce44c: full Python 841 passed, 5 skipped; subsequent dev merge changes site, records and Wiki, not Python runtime/tests. Exact-head shared CI and independent review remain. No live-store readback, Human QA or measured benefit claimed.

Root independently reviewed source and receipt preservation, verified exact d17d03d site and Python shared CI, and passed the trusted immutable-main gate. PR165 merged to dev as 6cdb647d2d415a8400d1d26cad2614b492c03926; fresh dev e10216e contains d17d03d. This completes only TK-0031, not S-007, live lineage or Human QA. Workspace closeout accounting remains incomplete; retain the clone and evidence.
