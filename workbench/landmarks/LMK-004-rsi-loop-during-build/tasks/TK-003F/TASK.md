# TK-003F - A trusted writer records an audit and returns safe evidence

**Task ID:** TK-003F
**Landmark ID:** LMK-004
**Slice:** A trusted writer records an audit and returns safe evidence
**Status:** ready
**Blockers:** none
**Destination:** spec-acceptance: Feedback connection
**Planned verification:** Observable behavior and controls below; exact-candidate Check and QA.

## Assignment

[Servitor launch and case](../../../../wiki/guidebooks/rsi-loop-continuation.md#servitor-launch--2026-11-07). DQC-000I/L/N/O/P/Q supply the mapped behavior. Preserve established stops and source/privacy gates.

## Acceptance

- [ ] Implement the S-006 write and read seam. Review PR175 at ce454a4a before choosing reusable lineage/recovery components. Keep one canonical shared history. One row per actual audit run with stable identity, pinned skill and contract, provider/model, result counts and completion. Identical replay leaves one row and changed payload with the same identity fails. Prove isolated PostgreSQL/Supabase trusted write, public-safe read, test row exclusion, private read denial and public write denial. Coordinate payload with TK-003E and TK-003G. No production migration in this Task.
