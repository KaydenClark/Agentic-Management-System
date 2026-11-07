# TK-003F - A trusted writer records an audit and returns safe evidence

**Task ID:** TK-003F
**Landmark ID:** LMK-004
**Slice:** A trusted writer records an audit and returns safe evidence
**Status:** in-progress
**Blockers:** none
**Destination:** spec-acceptance: Feedback connection
**Planned verification:** Observable behavior and controls below; exact-candidate Check and QA.
**Claimed by:** codex-rsi-store
**Current claimant:** codex-rsi-store

## Assignment

[Servitor launch and case](../../../../wiki/guidebooks/rsi-loop-continuation.md#servitor-launch--2026-11-07). DQC-000I/L/N/O/P/Q supply the mapped behavior. Preserve established stops and source/privacy gates.

## Acceptance

- [ ] Implement the S-006 write and read seam. Review PR175 at ce454a4a before choosing reusable lineage/recovery components. Keep one canonical shared history. One row per actual audit run with stable identity, pinned skill and contract, provider/model, result counts and completion. Identical replay leaves one row and changed payload with the same identity fails. Prove isolated PostgreSQL/Supabase trusted write, public-safe read, test row exclusion, private read denial and public write denial. Coordinate payload with TK-003E and TK-003G. No production migration in this Task.

## Starting inventory

Workspace baseline sha256:3ea3953be15aa1d891b492c02b651cfc914f2079426d020bf5671aa729209adf

## Receipt

| Run | Branch | HEAD SHA | Upstream | Dirty | Tests | Docs touched | Remaining gap | Checksum |
|---|---|---|---|---|---|---|---|---|
| 1 | Feature/servitor-rsi-store | 4811a8876139413fac1109a6c160369353a56c37 | none | 0 | 4811a887 exact fresh checkout: 865 pytest pass, 9 skip. Isolated PostgreSQL 17.6 and PostgREST 14.18: 3 tests pass. New all-N/A and evaluator-pin controls reproduced two failures on earlier SQL, then passed on correction. Trusted append, readback, replay, divergent and concurrent writes, exact public count, test/private exclusions and mutation denial proved. Hygiene 0, layout valid, render stable, doctor no blocking finding and local next passed. First full run was refused loopback sockets by the sandbox, then the scoped rerun passed. | SQL contract comments and this Task receipt. Agreed the wire contract with TK-003E and TK-003G. | Local isolated schema only. Coordinator smoke joined Python to chart on earlier SQL 15d425ca. Corrected 4811a887 has separate isolated REST proof. Supabase CLI exited via SIGKILL, so migration registration and advisors remain pending. Hosted proof, shared CI and publication remain held. Public data reports per-run verdicts. Assessment grade requires separate full-set evidence. | cd3275004adc3e816a13d54b8007768e9438421cad068e7c8e07f998ec1b84ef |
| 2 | Feature/servitor-rsi-store | 128c7c0d97317a510dd7d3a12c187b514a0e5955 | none | 0 | 128c7c0d exact grade delta. PostgreSQL 17.6 and PostgREST 14.18 fresh separate fixture: 14 pass. Old SQL reproduced missing grade for three-run Broken and two-run null. Window draft preserved grades but changed denied write to HTTP 500. Indexed set aggregate restored exact denial. Proved all grades, 19/20 Quality and 12/12 Regression with Critical miss, row-filter parity, and incomplete, private, interrupted, test and no-check controls. Fresh scoped pytest 142 pass and 16 skip. Hygiene 0, layout valid, render stable, doctor no blocking finding, local next and diff checks passed. | Extended SQL projection contract comments. Coordinated nullable assessment_grade with TK-003G. | Isolated local proof. Prior full pytest 865 pass and 9 skip applies to 4811a887. Current grade delta has focused exact verification. Grade remains distinct from qualification. Hosted migration registration, advisors, shared CI and publication remain pending. | f19a5f54516297a621d00cd2937d56463434ad550b3b89cc69494edeea5b402b |
