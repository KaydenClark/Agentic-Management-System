# TK-000U - Pinned history readback retains Wiki-routed historical Spec events

**Task ID:** TK-000U
**Spec ID:** S-006
**Slice:** Pinned history readback retains Wiki-routed historical Spec events
**Status:** in-progress
**Blockers:** none
**Destination:** spec-acceptance: Build history from real records
**Planned verification:** Red-first relocated-history collector/readcheck fixture; original eight rows rederived from declared immutable Wiki source; tampered/missing/unsupported/future/orphan source cases; focused/full/fresh checks and independent source review.
**Claimed by:** codex-history-consumer
**Current claimant:** codex-history-consumer

## Assignment

The owner resumed S-006 writer work and S-002 delivery. Main6e30c87 history verification found8 extra retained real events after owner-authorized PR #85 moved history out of S-003/S-007 into their Wiki. Primary read-only proof verifies all eight subjects/summaries/times/URLs against original ancestor blobs and the declared97bfcaa archive. Preserve that failed check and source evidence. Owner decision is settled: history belongs in the Wiki, not restored Spec tables.

One writer codex-history-consumer uses an isolated managed worktree, base `a4d58dd6622477c0edab9bc2c61e03967b9c31dd`, branch `feature/s006-wiki-history-source`. Repair only the S-006 history consumer, relevant tests/docs and this Spec/Task/projection. Derive/validate explicitly Wiki-routed immutable historical Spec events through local Git, preserving source identity/fields/URLs and pinned ancestry. No arbitrary all-history allowlist, unsupported external fetch, blanket extra suppression, row deletion or schema/website/scorer change. No workbench/tools or S-002 owner edits. No credential/key copy or DB mutation from this worktree before merge.

Check/open PR into main, but WAIT for parent: S-002 PR #89 must merge first. Then update branch onto current main and recheck required gates. Independent noncontributor review of immutable source is required. Actual post-merge import/readcheck uses approved local writer interfaces after source/DB coordination. Native owner QA/formal Spec acceptance remains pending.

## Acceptance

- [ ] Current destination Specs and declared immutable Wiki history together derive the8 retained events with exact original source/fields, without duplicate events or new evidence claims.
- [ ] Missing/tampered/unprovable rows still fail readcheck; unsupported, conflicting, future or orphan routes cannot authorize events; route processing performs no external fetch.
- [ ] Focused/full/fresh checks and independent review pass; previous failed history proof is retained and live after-merge verification is reported truthfully.
