# S-005 - Page review cards

**Spec ID:** S-005
**Status:** planned
**Priority:** 2
**Owner:** Kayden; orchestrator B (local)
**Stance:** Builder
**Updated:** 2026-11-01
**Catalog description:** A Grill Board review card for every website page, where the owner approves or criticizes the site and the criticism becomes the voice and taste record.
**Blockers:** S-004
**Latest event:** Four Tasks planned; the owner moved the cap to Landmarks, so no Spec slot is needed.
**Next gate:** Confirm scoped authority and required S-004 inputs, then activate. S-004 closure supplies no slot.

## Intent and authority

The owner decided that approvals happen in chat until the Grill Board exists, and then the owner approves and gives feedback on the whole website through it. The owner's voice is not prose the owner types: it is the owner's intent carried through unchanged, plus taste learned from recorded ratings and criticism.

## Outcome

Every page of the website has a review card on the local board. The owner approves a page or says what is wrong with it. Approved pages lose their draft mark; criticism accumulates into a record agents follow when drafting. The build stops when the full site is on the protected `dev` deployment with a card for every page.

## Why It Matters

Without a durable approval tied to exact content, the site cannot honestly show which pages the owner stands behind. Without recorded criticism, agents repeat the same misses.

## Current Verified State

- The S-004 board serves committed cards from `grill-board/cards/` with Priority and Value; Confirm writes into an owning record; ratings and too-taxing flags commit on the card; every write holds one repository flock and moves the branch by compare-and-swap ([README](../../../../../grill-board/README.md)).
- Orchestrator A, its only writer, keeps `site/page-list.json` on `dev`: path (stable), title, Spec, Task, `landed` {branch, commit, pr}, sources and status. It lists `/` and `/rsi`. No page shows a draft mark yet; that is S-003 TK-004.

## Desired Behavior

- A review card exists for every page of the website, including new pages, created automatically from the site's page list.
- Approval records the page's content hash. Any later change to the page's content clears the approval and restores its draft mark.
- Criticism is recorded against the page and hash, and the agent applies it to the page in a new candidate.
- Accumulated criticism and ratings form the voice and taste record: a committed file agents cite when drafting and reviewers check against.
- Ratings across pages are compared; the difference between high- and low-rated pages is studied and applied.

## Decisions And Contracts

- Approval is bound to a content hash, never to a page name or date alone.
- The voice record is built from the owner's recorded feedback; it is not owner-written prose.
- Owner words appear on the site verbatim only with their source.
- **Approval storage: a Supabase row mirrored from a committed file.** Confirm writes the approval into `grill-board/page-approvals.md` (the committed record, DDR-000X); the Python writer copies it to a `page_approvals` row with the local service key, and the site reads the row with the publishable key. Chosen because the site only presents and reads Supabase ([DDR-000O](../../../../docs/ddr/000O-the-public-site-only-presents-and-reads-supabase.md)) and reading repository files at build time was rejected ([ADR-003H](../../../../docs/adr/003H-supabase-holds-the-rsi-data-and-the-service-key-stays-local.md)). A page is approved only while a row names its path and current content hash, so an edit restores the draft mark (S-003) with nothing deleted.
- **Content hash** is SHA-256 over the canonical content of the served page's `<main id="main">`, excluding the footer, the review mark and regions marked `data-review-exclude`. TK-001 commits the contract and test vectors; S-003 TK-004 matches them.
- Page review cards target `main`; nothing here changes `site/`.

## Non-Goals

- Drafting pages on the board.
- Approving `dev` -> `main`; that is the owner's merge, outside the board.

## Dependencies And Blockers

- S-004 (cards and answers); S-003 (page list and draft marks).

## Vertical Implementation Slices

| Task | Slice | Status | Blockers | Proof |
|---|---|---|---|---|

## Acceptance Criteria

- [ ] **Every page covered.** Each page in the site's page list has exactly one open or answered review card. *Check:* compare the page list with the cards. *Must fail:* a new page with no card.
- [ ] **Approval bound to content.** An approval names the content hash; editing the page restores its draft mark. *Check:* approve a fixture page, edit it, rebuild. *Must fail:* an approved mark on changed content.
- [ ] **Criticism becomes the voice record.** Each criticism is appended, with its page, hash and date, to the committed voice and taste record. *Must fail:* criticism that exists only in board state.
- [ ] **Agents cite it.** A page draft's review names the voice record version it was checked against. *Must fail:* a review with no voice record reference.

## RSI and website connection

Page ratings are loop inputs (S-002). The site shows draft or approved status per page from these records (S-003).

## Testing Seams

- Fixture page list and fixture served pages in a temporary Git repository, with the site build injected; the board's write path; the S-003 draft-mark test.

## Verification Procedure

```bash
node workbench/tools/spec-workbench.mjs show S-005
uv run pytest
uv run ams-pages check   # TK-000K: every listed page has a current card
```

## Documentation Impact

- `grill-board/README.md` gains page cards, the hash contract and the voice record.
- The voice and taste record lives at `grill-board/voice-and-taste.md`; orchestrator A adds the pointer from the site's contributing notes on `dev`.

## Append-Only Evidence And Execution Log

| Date | Task | Event | Verification | Docs | Remaining gap |
|---|---|---|---|---|---|
| 2026-11-01 | none | Mapped as planned | render, doctor | this Spec | Every criterion |
| 2026-11-01 | none | Planned TK-001, TK-002, TK-003, TK-000K; approval storage chosen; not activated | render, doctor | this Spec, Task records | Every criterion |

## Review and Human QA

The owner's page approvals are themselves Human QA receipts for each page.

## Completion Result

Pending.

## Remaining Limitations Or Follow-Up Specs

- Comparing ratings across pages and applying the difference is left to the RSI loop (S-002), reading the voice record.
- S-003 TK-004 names a committed approval record; orchestrator A reads the `page_approvals` row instead.

## Supersession

- Supersedes: the earlier site draft's owner-written voice guide.
- Superseded by: none
