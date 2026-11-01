# S-005 - Page review cards

**Spec ID:** S-005
**Status:** planned
**Priority:** 2
**Owner:** Kayden; orchestrator B (local)
**Stance:** Builder
**Updated:** 2026-11-01
**Catalog description:** A Grill Board review card for every website page, where the owner approves or criticizes the site and the criticism becomes the voice and taste record.
**Blockers:** S-004
**Latest event:** Mapped from the owner's confirmed decisions of 2026-11-01.
**Next gate:** Task planning after S-004's card flow exists.

## Intent and authority

The owner decided that approvals happen in chat until the Grill Board exists, and then the owner approves and gives feedback on the whole website through it. The owner's voice is not prose the owner types: it is the owner's intent carried through unchanged, plus taste learned from recorded ratings and criticism.

## Outcome

Every page of the website has a review card on the local board. The owner approves a page or says what is wrong with it. Approved pages lose their draft mark; criticism accumulates into a record agents follow when drafting.

## Why It Matters

Without a durable approval tied to exact content, the site cannot honestly show which pages the owner stands behind. Without recorded criticism, agents repeat the same misses.

## Current Verified State

- No board and no site pages exist yet. The site's draft-mark rule lives in S-003.

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

## Non-Goals

- Drafting pages on the board.
- Approving `dev` -> `main`; that is the owner's merge, outside the board.

## Dependencies And Blockers

- S-004 (cards and answers); S-003 (page list and draft marks).

## Vertical Implementation Slices

| Task | Slice | Status | Blockers | Proof |
|---|---|---|---|---|
| TK-001 | Generate one review card per site page from the page list, with the page's content hash | ready | none | pending |
| TK-002 | Approval writes a hash-bound record the site reads to drop the draft mark | ready | TK-001 | pending |
| TK-003 | Criticism and ratings appended to the voice and taste record | ready | TK-001 | pending |

### TK-001 - Card per page

**Stance:** Builder

Proves the coverage criterion.

### TK-002 - Hash-bound approval

**Stance:** Builder

Proves the approval and draft-mark criteria.

### TK-003 - Voice record

**Stance:** Builder

Proves the voice record criterion.

## Acceptance Criteria

- [ ] **Every page covered.** Each page in the site's page list has exactly one open or answered review card. *Check:* compare the page list with the cards. *Must fail:* a new page with no card.
- [ ] **Approval bound to content.** An approval names the content hash; editing the page restores its draft mark. *Check:* approve a fixture page, edit it, rebuild. *Must fail:* an approved mark on changed content.
- [ ] **Criticism becomes the voice record.** Each criticism is appended, with its page, hash and date, to the committed voice and taste record. *Must fail:* criticism that exists only in board state.
- [ ] **Agents cite it.** A page draft's review names the voice record version it was checked against. *Must fail:* a review with no voice record reference.

## RSI and website connection

Page ratings are loop inputs (S-002). The site shows draft or approved status per page from these records (S-003).

## Testing Seams

- Fixture site page list and fixture records in a temporary Git repository; the S-003 draft-mark test.

## Verification Procedure

```bash
node workbench/tools/spec-workbench.mjs show S-005
# Python test command named at Task planning
```

## Documentation Impact

- The voice and taste record gets a home and a pointer from the site's contributing notes.

## Append-Only Evidence And Execution Log

| Date | Task | Event | Verification | Docs | Remaining gap |
|---|---|---|---|---|---|
| 2026-11-01 | none | Mapped as planned | render, doctor | this Spec | Every criterion |

## Review and Human QA

The owner's page approvals are themselves Human QA receipts for each page.

## Completion Result

Pending.

## Remaining Limitations Or Follow-Up Specs

- none

## Supersession

- Supersedes: the earlier site draft's owner-written voice guide.
- Superseded by: none
