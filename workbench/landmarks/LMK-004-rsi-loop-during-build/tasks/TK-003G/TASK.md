# TK-003G - RSI Charts distinguish actual audits from empty and unavailable reads

**Task ID:** TK-003G
**Landmark ID:** LMK-004
**Slice:** RSI Charts distinguish actual audits from empty and unavailable reads
**Status:** in-progress
**Blockers:** none
**Destination:** spec-acceptance: Actual audits
**Planned verification:** Observable behavior and controls below; exact-candidate Check and QA.
**Claimed by:** codex-rsi-site
**Current claimant:** codex-rsi-site

## Assignment

[Servitor launch and case](../../../../wiki/guidebooks/rsi-loop-continuation.md#servitor-launch--2026-11-07). DQC-000I/L/N/O/P/Q supply the mapped behavior. Preserve established stops and source/privacy gates.

## Acceptance

- [ ] Implement the S-007 reader and view on /rsi from dev 325ea7d9. Use the TK-003F public audit projection. Show actual completed audit count including failed runs, separate scores, Critical status, provider/model and traceable versioned row identity. Preserve historical presentation. Test rows, ordinary skill uses, repair attempts and unexecuted slots must not inflate the count. Verify populated, empty, stale and unavailable states through the actual page or component and report exact build/browser limits. Deliver to dev.

Workspace baseline sha256:68e63f39c435cce63eabdff4c7fcb1d817514ea0cda3a9e16f7ec6c112d93f8b

## Receipt

| Run | Branch | HEAD SHA | Upstream | Dirty | Tests | Docs touched | Remaining gap | Checksum |
|---|---|---|---|---|---|---|---|---|
| 1 | Feature/servitor-rsi-charts | fe90a2f377ae8b2291a0ec01aa54724fed15e976 | none | 0 | Site candidate fe90a2f: standalone clone npm run build and npm test passed (351 tests); focused /rsi browser checks passed 56 checks at three widths and both themes on 52a1b4e. Full browser run stopped after an unrelated /start toy RSC prefetch check failed. Isolated gateway and Python synthetic fixtures rendered two public audits including a failed row and excluded private/test rows; sanitized section sha256 47078a02c173878d95b68cbb4ddd769ccfb5c20ba40f2aa3013844b395daa87d. The later all-N/A correction passed its focused test and full site suite. | No documentation files changed; view explains audit counts, unavailable scores and evidence limits. | Task remains in progress: real audit, hosted readback, independent review, delivery and owner Human QA unverified. No push, merge, deployment or live credentials. | 664f9651f7fb22411c72e1083dc5e1a130d7536da540191556bb599eb7c5debd |
| 2 | Feature/servitor-rsi-charts | 1fde818244ccb1ccab403ddc43d1ff3c42e7f5c8 | none | 0 | Candidate 459be8d standalone production build and 353 tests passed; comment-only 1fde818 focused audit tests passed 8/8 and diff check passed. Built page at 1fde818 against isolated Python and SQL synthetic grade gateway showed five public audits, Broken, pooled Quality 19/20, Regression 12/12, Critical missed, three row links, partial Unknown, failed row, read timestamp and exclusion of private/test rows; sanitized section sha256 78f718119cd0876d146be02dd4622cc9d8fbb87ba30e44fdfba8f792e6e4c916. | Audit UI separates grade from run outcome and benefit; no documentation files changed. | Synthetic isolated proof only; real audit, hosted readback, independent review, delivery and owner Human QA remain unverified. Full browser suite had prior unrelated /start prefetch failure; Task remains in progress. | 8f3c4faf7b3eb6e3e68a31079d220edd53bb9331794cf970b0f80f24a8d927f8 |
