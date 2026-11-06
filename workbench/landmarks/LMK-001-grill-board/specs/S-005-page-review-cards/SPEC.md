# S-005 - Page review cards

**Spec ID:** S-005
**Status:** active
**Priority:** 2
**Owner:** Kayden; orchestrator B (local)
**Stance:** Builder
**Updated:** 2026-11-06
**Confirmation:** [JOT-3f414c7a-684a-4625-b07a-11e7b73e83b2](../../../../wiki/context-active-spec-approvals.md)
**Execution approval:** [JOT-3f414c7a-684a-4625-b07a-11e7b73e83b2](../../../../wiki/context-active-spec-approvals.md)
**Catalog description:** Content-bound page reviews and versioned feedback consumed by later drafts.
**Blockers:** none
**Next gate:** Close TK-003 with verification and documentation proof.


## Intent and authority

The owner approves and criticizes the whole website through the local Grill Board. Voice means preserved intent and taste learned from ratings/criticism, not owner-written page prose. Linked confirmed intent supplies this scoped implementation launch; earlier preparation-only records remain history.

## Outcome

Every website page has a content-bound owner review card. Changed content makes approval stale locally. Criticism informs the next draft/review through a versioned record. Stop at a complete protected dev site with current page coverage; public pages show no review status or private criticism.

## Why It Matters

Exact content identity prevents stale approvals; consumed feedback prevents repeated misses.

## Current Verified State

No Spec acceptance is claimed. [TK-001](tasks/TK-001/TASK.md) owns evidence/failures. Source930d9c2 passes fresh967 tests/6 skips and separate89-test Standards/Spec reviews; shared CI965/8 skips plus10 browser passes. Exact protected47e3c88 supplies50 current cards,39 skill articles and visitor404;3 stale histories remain and rerun is a no-op. All50 selected cards pass owned HTTP readback with cleanup; no owner action occurred. Source/deployment/footer/document markers and manifest digest44b7a64e bind unchanged private HTML, including real populated RSI. S003's failure-table schema finding remains open. Original804 public files remain in history;4 private cache originals are copied, original nodeids not located, so workspace release is not claimed. Later devb699f10 includes navigation/governance changes: refresh the final queue after assembly. Private feedback, later Tasks and owner QA remain open.

History: [S-005](../../../../wiki/history/S-005.md).

## Desired Behavior

- Automatically cover every built public page, including new pages and all skill articles, from explicit current owner metadata.
- Bind approvals to content hashes; edits stale the local approval without changing the public site.
- Preserve original criticism separately from interpretation; next draft and review cite its version and apply it or give an explicit disposition.
- Accumulate criticism and ratings in the voice/taste record; agents cite it and reviewers check it. S-002 compares high/low ratings and applies useful differences.

## Decisions And Contracts

- Approval binds exact content, never page name/date alone. [DDR-001B](../../../../docs/ddr/001B-the-public-site-shows-no-review-status.md) excludes public review status; [DDR-001A](../../../../docs/ddr/001A-the-public-site-shows-no-owner-quotations.md) excludes owner quotations. Neither approval nor criticism surfaces on public pages.
- **Approval storage: committed owner record only.** Confirm writes path/hash to `grill-board/page-approvals.md` through Board lock/CAS. No Supabase approval mirror, publishable-key approval path or site consumption. This applies the confirmed recommendation; history retains the withdrawn proposal. Do not commit raw private criticism/evidence; synthetic fixtures stay labeled synthetic.
- Content hash: UTF-8 SHA-256 of canonical served `<main id="main">`, excluding footer and review-exclude/mark regions; retain the shared contract/test vectors. Current candidate supplies content; historical `landed.commit` is provenance only. Explicit historical, verified-containment and pending-candidate/null meanings must not fabricate authorship or integration.
- RSI hash exclusions cover freshness only: real changed results and availability remain bound. A different local data state cannot substitute for exact protected-deployment HTML; require a trusted immutable deployed artifact for that proof.
- Cards/records target checked `main`; S-003 owns site changes and source/served route metadata. Missing ownership refuses rather than invents Spec/Task/landing.

## Non-Goals

Drafting pages on the Board; owner-only dev-to-main promotion; public approval status.

## Dependencies And Blockers

Required S-004 card/answer operations exist; full S-004 acceptance is not an input. S-003 supplies complete built inventory and protected candidate. TK-001E retains its delivered same-Spec prerequisites; launch grants no campaign restart, attempt reset, installation, Human QA or promotion.

## Vertical Implementation Slices

| Task | Slice | Status | Blockers | Proof |
|---|---|---|---|---|

## Acceptance Criteria

- [ ] **Feedback loop connection:** Feedback is consumed: preserve original criticism separately from interpretation; a subsequent page draft and its review name the applicable feedback version and show application or a reasoned unresolved disposition. A stored rating with no downstream use must fail.

- [ ] **Every page covered.** Each page in the site's page list has exactly one open or answered review card. *Check:* compare the page list with the cards. *Must fail:* a new page with no card.
- [ ] **Approval bound to content.** An approval names the content hash; editing the page makes it stale on the board. *Check:* approve a fixture page, edit it, regenerate cards. *Must fail:* changed content shown approved on the board, or review status on the public site.
- [ ] **Criticism becomes the voice record.** Each criticism is appended, with its page, hash and date, to the committed voice and taste record. *Must fail:* criticism that exists only in board state.
- [ ] **Agents cite it.** A page draft's review names the voice record version it was checked against. *Must fail:* a review with no voice record reference.

## RSI and website connection

Ratings feed S-002. Activity/storage alone proves no downstream use or improvement.

## Testing And Verification

Disposable Git fixtures exercise built HTML injection, actual current-build collection, Board lock/CAS, content changes, immutable history, stale/refused writes, privacy and feedback consumption. Run required RUNBOOK checks and actual protected dev/card readback.

```bash
node workbench/tools/spec-workbench.mjs show S-005
uv run pytest
uv run ams-pages check   # TK-000K; unavailable until delivered
```

## Documentation Impact

Maintain `grill-board/README.md` with hash/card/feedback contracts. `grill-board/voice-and-taste.md` is the safe committed version record; private original criticism stays private. S-003 owns the contributing pointer and cites versions when drafting.

## Review and Human QA

Actual owner approvals supply content-bound page Human QA. Agent checks, storage, merge and deployment do not supply it.

## Completion Result

Pending. Required checks, exact-candidate Review, complete protected dev coverage and real owner judgments remain separate.

## Remaining Limitations Or Follow-Up Specs

S-002 owns rating comparisons. DDR-001B withdraws historical public draft marks; their prior Task evidence stays in history.

## Supersession

- Supersedes: earlier owner-written voice-guide approach and withdrawn public approval-row/draft-mark path.
- Superseded by: none

The confirmed 2026-11-05 launch supersedes only the historical preparation hold for this scope. Existing failures, stopped campaigns, independent Review/Human QA and owner-only promotion remain. [Cross-Spec plan](../../../../wiki/context-feedback-improvement-loop-plan.md) explains artifact releases, not a second task queue.
