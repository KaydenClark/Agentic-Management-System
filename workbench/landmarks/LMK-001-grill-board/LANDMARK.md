# LMK-001 - Grill Board

**Landmark ID:** LMK-001
**Status:** planned
**Priority:** 1
**Owner:** Kayden
**Updated:** 2026-11-01
**Catalog description:** The owner's local attention queue, where agents post items that need an answer and confirmed answers land straight in their owning records.
**Blockers:** none
**Latest event:** Landmark mapped from the owner's confirmed decisions of 2026-11-01.
**Next gate:** Task planning for S-004; fill the Decision Records links once the decision records reach `main`.

## Direction

The Grill Board is where the owner's attention goes. Agents post only what needs the owner: an owner gate, an open choice, a page approval or the text of a decision. The owner answers, rates and comments there, and the agent writes each confirmed answer straight into the record that owns it. Nothing is re-asked and no bookkeeping step sits in between.

It runs locally on the owner's machine with a Python server. It is never hosted on Vercel and is never a drafting surface: pages and routine content are written elsewhere, and only items that need an answer go on the board.

Once the board exists it replaces chat as the place where the owner approves and criticizes the whole website, page by page. The recorded criticism and ratings become the owner's voice and taste record, which agents follow and the RSI loop reads.

## Why It Matters

Owner attention is the scarcest input in the system. Without one queue, questions scatter across chats, answers are lost or re-asked, and agents guess at taste. The owner already sorts what needs attention by Priority and Value, so the board keeps both on every card. Approval in chat leaves no durable, hash-bound record that the site can show as approved.

## What Success Looks Like

- [ ] The board runs locally from a Python server on the owner's machine, and no Vercel deployment serves it.
- [ ] Every card shows Priority and Value with a one-line reason each, a 1-5 rating and a one-click "too taxing" flag (S-004).
- [ ] A confirmed answer is written into its owning record in the same step, with no second confirmation (S-004).
- [ ] Flags, ratings and comments are committed records; a write that would overwrite a newer change is refused (S-004).
- [ ] Every page of the website has a review card, and an approval is bound to the page's content hash (S-005).
- [ ] Recorded criticism is kept as the voice and taste record that agents cite when drafting (S-005).

## Decision Records

The decision records for this landmark are being written in parallel and are not on `main` yet. They are named here by short title; links are filled at Task planning.

- The Grill Board is the owner's attention queue, never a drafting surface.
- A confirmed Grill Board answer is written straight into its owning record.
- Priority and Value stay on every card (owner choice).
- Every owner question has a "too taxing" flag and a 1-5 rating.
- Colors are signals, each with one stated meaning.
- Writes to shared stores refuse on conflict.
- Approvals happen in chat until the Grill Board exists, then through it.

## Child Specs

- [S-004 - Grill Board cards and answers](specs/S-004-grill-board-cards/SPEC.md)
- [S-005 - Page review cards](specs/S-005-page-review-cards/SPEC.md)

## Direct Tasks

- none

## Verification Procedure

```bash
node workbench/tools/spec-workbench.mjs show LMK-001
node workbench/tools/spec-workbench.mjs show S-004
node workbench/tools/spec-workbench.mjs show S-005
node workbench/tools/spec-workbench.mjs doctor
```

Each reached check is confirmed against what has landed on `main`, by running the child Spec's verification and reading its evidence log.

## Append-Only Evidence And Execution Log

| Date | Task | Event | Verification | Docs | Remaining gap |
|---|---|---|---|---|---|
| 2026-11-01 | none | Landmark mapped from confirmed owner decisions; child Specs S-004 and S-005 written as planned | render and doctor on the mapping branch | this record | Decision record links; Task planning |

## Reached Result

Pending.

## Supersession

- Supersedes: none
- Superseded by: none
