# TK-003E - A participating chat records use and recovers pending skill evidence

**Task ID:** TK-003E
**Landmark ID:** LMK-004
**Slice:** A participating chat records use and recovers pending skill evidence
**Status:** ready
**Blockers:** none
**Destination:** spec-acceptance: Observer and scheduling
**Planned verification:** Observable behavior and controls below; exact-candidate Check and QA.

## Assignment

[Servitor launch and case](../../../../wiki/guidebooks/rsi-loop-continuation.md#servitor-launch--2026-11-07). DQC-000I/L/N/O/P/Q supply the mapped behavior. Preserve established stops and source/privacy gates.

## Acceptance

- [ ] Implement optional per-Workbench Python observer and versioned S-002 skill scoring. Persist independent request, load, use, failure and explicit work-status events per chat before transport. Recover the same IDs after interruption. Classify an evidenced skipped explicit request as Critical and preserve unknown observation. Expose three audit-run identities, separate Quality/Regression counts, Critical and severity grade. Keep historical r1 semantics. Demonstrate the public Python entry point with restart, duplicate delivery, incomplete audit, and finished vs blocked controls. Coordinate with TK-003F. No live setup or calls in this Task.
