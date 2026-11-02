# TK-000U - Pinned history readback retains Wiki-routed historical Spec events

**Task ID:** TK-000U
**Spec ID:** S-006
**Slice:** Pinned history readback retains Wiki-routed historical Spec events
**Status:** done
**Blockers:** none
**Destination:** spec-acceptance: Build history from real records
**Planned verification:** Red-first relocated-history collector/readcheck fixture; original eight rows rederived from declared immutable Wiki source; tampered/missing/unsupported/future/orphan source cases; focused/full/fresh checks and independent source review.
**Claimed by:** codex-history-consumer
**Current claimant:** codex-history-consumer
**Proof:** Source9f3a6ca reconciles main17293a0; local and fresh590 passed4 skipped; focused85 passed; direct independent source review d50 PASS; all8 retained facts rederived exactly. Final CI/current-owner binding then postmerge live proof remain required.

## Assignment

The owner resumed S-006 writer work and S-002 delivery. Main6e30c87 history verification found8 extra retained real events after owner-authorized PR #85 moved history out of S-003/S-007 into their Wiki. Primary read-only proof verifies all eight subjects/summaries/times/URLs against original ancestor blobs and the declared97bfcaa archive. Preserve that failed check and source evidence. Owner decision is settled: history belongs in the Wiki, not restored Spec tables.

One writer codex-history-consumer uses an isolated managed worktree, base `a4d58dd6622477c0edab9bc2c61e03967b9c31dd`, branch `feature/s006-wiki-history-source`. Repair only the S-006 history consumer, relevant tests/docs and this Spec/Task/projection. Derive/validate explicitly Wiki-routed immutable historical Spec events through local Git, preserving source identity/fields/URLs and pinned ancestry. No arbitrary all-history allowlist, unsupported external fetch, blanket extra suppression, row deletion or schema/website/scorer change. No workbench/tools or S-002 owner edits. No credential/key copy or DB mutation from this worktree before merge.

Check/open PR into main, but WAIT for parent: S-002 PR #89 must merge first. Then update branch onto current main and recheck required gates. Independent noncontributor review of immutable source is required. Actual post-merge import/readcheck uses approved local writer interfaces after source/DB coordination. Native owner QA/formal Spec acceptance remains pending.

## Acceptance

- [x] Current destination Specs and declared immutable Wiki history together derive the8 retained events with exact original source/fields, without duplicate events or new evidence claims.
- [x] Missing/tampered/unprovable rows still fail readcheck; unsupported, conflicting, future or orphan routes cannot authorize events; route processing performs no external fetch.
- [x] Focused/full/fresh checks and independent review pass; previous failed history proof is retained and live after-merge verification is reported truthfully.

## Check and QA

Source candidate `d50b1673db868842016428bb804f48a763738689` (base `a4d58dd6622477c0edab9bc2c61e03967b9c31dd`):

- RED: relocated fixture derived0 retained events; expected8. Its existing DB rows were extras. GREEN: `pytest -q tests/test_build_history_wiki_sources.py tests/test_build_history.py`85passed, including exact six-plus-two recovery, missing/tampered/unprovable-row failures and source-route refusal cases.
- Local `uv run pytest -q`:540passed/4skipped111.73s. Clean fresh clone at exact source:540passed/4skipped106.12s. Render unchanged, doctor0blocking (same2informational findings), next/layout/diff pass in both. An initial room-check invocation used a nonexistent validator filename; the actual RUNBOOK command then passed. No source/test check was weakened.
- Local record reader independently compared all8 real retained facts with the saved original-blobs proof: subject, summary, UTC time, source URL and recorded_commit all exact. No database access.
- Actual eligible independent reviewer `s002_bootstrap_review` directly supplied scoped source PASS/no blockers at exact source: Standards0/Spec0 unresolved,85focusedpass11.09s in a clean detached clone, and independently rederived all8 real rows exactly once. Reviewer contributed no U source/records, used no credentials/DB/model calls or delegation. Implementor verified direct primary report and clean exact reviewer clone. This is a source review, not whole-Spec acceptance or a live DB observation.

Draft PR #91 targets main. CI/current-main integration remains pending; PR #89 must merge first and parent must release this merge. Actual post-merge history import/readcheck is pending; the earlier failed6e30c87 check remains actual evidence (missing0/extra8/mismatches0/unsourced0), not retroactively green. Owner Human QA and formal S-006 acceptance remain open. No table restoration, deletions, schema/scorer changes, secret/key copies, website changes or DB mutations occurred in this run.

### Current-main reconciliation

PR #89 merged at `17293a09d55806342442e57e6253984e20cdb7b8`; parent released U integration. Normal feature merge `9f3a6ca1fcb57ee15f6dcce7341d474abc00c419` reconciles that main with no conflicts and no change to reviewed history source/tests. At that exact reconciled source: local full590passed/4skipped110.87s; fresh clone full590passed/4skipped109.25s; both render/doctor/next/layout/diff checks pass, retaining the same2 informational doctor findings. Prior d50/415 CI passed; final closed-owner CI and exact record-only review binding remain required before checked merge. PR #91 is ready for review. Actual post-merge import/readcheck and durable Spec proof remain pending in this same authorized run; closed receipt will remain immutable. No live DB action or primary checkout change has occurred.

## Receipt

| Run | Branch | HEAD SHA | Upstream | Dirty | Tests | Docs touched | Remaining gap | Checksum |
|---|---|---|---|---|---|---|---|---|
| 1 | feature/s006-wiki-history-source | c59cc9b444109944d1fff9055698793e344f2afa | ahead 0 behind 0 | 0 | Source9f3a6ca reconciles main17293a0; local and fresh590 passed4 skipped; focused85 passed; direct independent source review d50 PASS; all8 retained facts rederived exactly. Final CI/current-owner binding then postmerge live proof remain required. | src/ams/build_history.py module contract; S006 TaskU and Spec; TASKBOARD | Postmerge history import/readcheck and durable Spec proof pending in same run; Build-history criterion remains unchecked. Owner HumanQA/formal Spec acceptance pending.; close attribution: {"agent":"codex-history-consumer","claimant":"codex-history-consumer","onBehalfOf":null} | 189e485a87720a4c6209170c116fcc41955ab54269ba7f539ded75641193cd0d |
