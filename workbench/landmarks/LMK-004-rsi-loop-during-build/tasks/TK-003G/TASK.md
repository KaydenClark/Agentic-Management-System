# TK-003G - RSI Charts distinguish actual audits from empty and unavailable reads

**Task ID:** TK-003G
**Landmark ID:** LMK-004
**Slice:** RSI Charts distinguish actual audits from empty and unavailable reads
**Status:** ready
**Blockers:** none
**Destination:** spec-acceptance: Actual audits
**Planned verification:** Observable behavior and controls below; exact-candidate Check and QA.

## Assignment

[Servitor launch and case](../../../../wiki/guidebooks/rsi-loop-continuation.md#servitor-launch--2026-11-07). DQC-000I/L/N/O/P/Q supply the mapped behavior. Preserve established stops and source/privacy gates.

## Acceptance

- [ ] Implement the S-007 reader and view on /rsi from dev 325ea7d9. Use the TK-003F public audit projection. Show actual completed audit count including failed runs, separate scores, Critical status, provider/model and traceable versioned row identity. Preserve historical presentation. Test rows, ordinary skill uses, repair attempts and unexecuted slots must not inflate the count. Verify populated, empty, stale and unavailable states through the actual page or component and report exact build/browser limits. Deliver to dev.
