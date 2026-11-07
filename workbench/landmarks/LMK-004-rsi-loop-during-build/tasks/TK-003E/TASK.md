# TK-003E - A participating chat records use and recovers pending skill evidence

**Task ID:** TK-003E
**Landmark ID:** LMK-004
**Slice:** A participating chat records use and recovers pending skill evidence
**Status:** in-progress
**Blockers:** none
**Destination:** spec-acceptance: Observer and scheduling
**Planned verification:** Observable behavior and controls below; exact-candidate Check and QA.
**Claimed by:** codex-rsi-python
**Current claimant:** codex-rsi-python

## Assignment

[Servitor launch and case](../../../../wiki/guidebooks/rsi-loop-continuation.md#servitor-launch--2026-11-07). DQC-000I/L/N/O/P/Q supply the mapped behavior. Preserve established stops and source/privacy gates.

## Acceptance

- [ ] Implement optional per-Workbench Python observer and versioned S-002 skill scoring. Persist independent request, load, use, failure and explicit work-status events per chat before transport. Recover the same IDs after interruption. Classify an evidenced skipped explicit request as Critical and preserve unknown observation. Expose three audit-run identities, separate Quality/Regression counts, Critical and severity grade. Keep historical r1 semantics. Demonstrate the public Python entry point with restart, duplicate delivery, incomplete audit, and finished vs blocked controls. Coordinate with TK-003F. No live setup or calls in this Task.

## Workspace baseline

Workspace baseline sha256:6162e0bf0fbb0a6cfdad3317dbc3762a1a891dd521000c559329d5a1df054a49

## Receipt

| Run | Branch | HEAD SHA | Upstream | Dirty | Tests | Docs touched | Remaining gap | Checksum |
|---|---|---|---|---|---|---|---|---|
| 1 | Feature/servitor-rsi-observer | 5abfb686ef30bda2157235b45bd62d7f2c958a0a | none | 0 | Fresh ede79bbc offline pytest passed 881 with 6 skipped. Exact rubric correction Red then Green, 81 focused passed at this HEAD. Layout, doctor, local next, hygiene and diff passed. Assembled Python to isolated PostgREST to built RSI Charts smoke passed with synthetic evidence before the rubric-only correction. | workbench/rsi-observer/README.md records opt-in events, recovery, audit and trusted transport. | Local candidate awaiting assembled verification and authorized delivery. Real Servitor hook use, hosted Supabase and repair proof remain open. | 127a86c4305bb91f4d24deeb184331c8b3984f6133718df264d760c960f32105 |
| 2 | Feature/servitor-rsi-observer | e13a3899aa7e0dcdfb8f4079851f7f084b6b1a89 | none | 0 | Independent review corrections exercised at the Python CLI. Red reproduced lost Critical on an interrupted run and qualification of Functional and Broken. Green passed 84 focused cases, including historical r1, in the assigned and fresh checkouts. Layout, hygiene and whitespace passed. | Observer README distinguishes counted completions, interrupted denominators, evaluator eligibility and skill qualification. | Assembled candidate recheck and authorized dev delivery remain pending. Real Servitor and hosted repair proof remain open. | 001aa7ad93e417ca423adbabf6f757b1d0f2deaf7db4e9a6f43a4432b3dd4457 |
| 3 | Feature/servitor-rsi-observer | 9a3d8e59a123acddf87326408d67f11ed4f719a6 | none | 0 | Standards boundary Red reproduced enqueue of a 65-character provider. Green rejects before creating state and accepts the SQL 64-character boundary. 85 focused observer and historical r1 tests passed on this product head. Hygiene and whitespace passed. | Source comments specify the audit contract and evidence rules, observer status and durable replay. | Assembled recheck and authorized dev delivery remain pending. Real Servitor and hosted repair proof remain open. | b86d26fb5b2635efc87cb9e74fbd37874377d37d3e608bcc4c7cf78455d30da2 |
