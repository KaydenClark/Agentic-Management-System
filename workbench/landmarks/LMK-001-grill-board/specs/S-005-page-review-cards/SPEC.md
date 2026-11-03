# S-005 - Page review cards

**Spec ID:** S-005
**Status:** planned
**Priority:** 2
**Owner:** Kayden; orchestrator B (local)
**Stance:** Builder
**Updated:** 2026-11-02
**Catalog description:** A Grill Board review card for every website page, where the owner approves or criticizes the site and the criticism becomes the voice and taste record.
**Blockers:** S-004
**Next gate:** Confirm scoped authority and required S-004 inputs, then activate. S-004 closure supplies no slot.

## Intent and authority

The owner decided that approvals happen in chat until the Grill Board exists, and then the owner approves and gives feedback on the whole website through it. The owner's voice is not prose the owner types: it is the owner's intent carried through unchanged, plus taste learned from recorded ratings and criticism.

## Outcome

Every page of the website has a review card on the local board. The owner approves a page or says what is wrong with it. Approvals stay owner-facing: the public site shows no draft, approval or review status ([DDR-001B](../../../../docs/ddr/001B-the-public-site-shows-no-review-status.md)). Criticism accumulates into a record agents follow when drafting. The build stops when the full site is on the protected `dev` deployment with a card for every page.

## Why It Matters

Without a durable approval tied to exact content, the owner and agents cannot tell which page content the owner has reviewed. Without recorded criticism, agents repeat the same misses.

## Current Verified State

- Not met: all four acceptance criteria; S-005 is planned and not activated.
- The S-004 board serves committed cards from `grill-board/cards/` with Priority and Value; Confirm writes into an owning record; ratings and too-taxing flags commit on the card; every write holds one repository flock and moves the branch by compare-and-swap ([README](../../../../../grill-board/README.md)).
- Orchestrator A, its only writer, keeps `site/page-list.json` on `dev`: path (stable), title, Spec, Task, `landed` {branch, commit, pr}, sources and status. It lists `/` and `/rsi`. Pages on `dev` still show draft marks (S-003 TK-004, PR #82), which DDR-001B withdraws; removing them is S-003 site work.

History: [S-005 history](../../../../wiki/history/S-005.md).

## Desired Behavior

- A review card exists for every page of the website, including new pages, created automatically from the site's page list.
- Approval records the page's content hash. Any later change to the page's content makes the approval stale on the board; nothing changes on the public site.
- Criticism is recorded against the page and hash, and the agent applies it to the page in a new candidate.
- Accumulated criticism and ratings form the voice and taste record: a committed file agents cite when drafting and reviewers check against.
- Ratings across pages are compared; the difference between high- and low-rated pages is studied and applied.

## Decisions And Contracts

- Approval is bound to a content hash, never to a page name or date alone.
- The voice record is built from the owner's recorded feedback; it is not owner-written prose.
- The public site shows no owner quotations and no review status ([DDR-001A](../../../../docs/ddr/001A-the-public-site-shows-no-owner-quotations.md), DDR-001B); criticism and approvals never surface there.
- **Approval storage: a Supabase row mirrored from a committed file.** Confirm writes the approval into `grill-board/page-approvals.md` (the committed record, DDR-000X); the Python writer copies it to a `page_approvals` row with the local service key, and the site reads the row with the publishable key. The site only presents and reads Supabase ([DDR-000O](../../../../docs/ddr/000O-the-public-site-only-presents-and-reads-supabase.md)) and does not read repository files at build time ([ADR-003H](../../../../docs/adr/003H-supabase-holds-the-rsi-data-and-the-service-key-stays-local.md)). A page is approved only while a row names its path and current content hash, so an edit makes the approval stale with nothing deleted. The site displays no approval; whether the row is still needed is open for TK-002.
- **Content hash** is SHA-256 over the canonical content of the served page's `<main id="main">`, excluding the footer and regions marked `data-review-exclude`. TK-001 commits the contract and test vectors.
- Page review cards target `main`; nothing here changes `site/`.

## Non-Goals

- Drafting pages on the board.
- Approving `dev` -> `main`; that is the owner's merge, outside the board.

## Dependencies And Blockers

- S-004 (cards and answers); S-003 (page list).

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

Page ratings are loop inputs (S-002). The public site shows no review status from these records (DDR-001B).

## Testing Seams

- Fixture page list and fixture served pages in a temporary Git repository, with the site build injected; the board's write path.

## Verification Procedure

```bash
node workbench/tools/spec-workbench.mjs show S-005
uv run pytest
uv run ams-pages check   # TK-000K: every listed page has a current card
```

## Documentation Impact

- `grill-board/README.md` gains page cards, the hash contract and the voice record.
- The voice and taste record lives at `grill-board/voice-and-taste.md`; orchestrator A adds the pointer from the site's contributing notes on `dev`.

## Review and Human QA

The owner's page approvals are themselves Human QA receipts for each page.

## Completion Result

Pending.

## Remaining Limitations Or Follow-Up Specs

- Comparing ratings across pages and applying the difference is left to the RSI loop (S-002), reading the voice record.
- S-003 TK-004 (draft marks) is withdrawn by DDR-001B and needs reconciling by orchestrator A.

## Supersession

- Supersedes: the earlier site draft's owner-written voice guide.
- Superseded by: none

## Feedback-loop planning boundary

Owner instruction, 2026-11-02: map and plan the feedback-to-improvement loop using existing Specs; stop before implementation. The new Task is preparation only and has an explicit execution hold. Earlier approvals, stopped experiments and failed evidence retain their original scope. See [cross-Spec plan](../../../../wiki/context-feedback-improvement-loop-plan.md).
