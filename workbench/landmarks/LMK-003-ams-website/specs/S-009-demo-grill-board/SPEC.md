# S-009 - Demo Grill Board page

**Spec ID:** S-009
**Status:** planned
**Priority:** 3
**Owner:** Kayden; orchestrator A (Website, cloud)
**Stance:** Builder
**Updated:** 2026-11-01
**Catalog description:** A public demo of the Grill Board with sample cards asking non-engineering questions, showing what a non-developer might use it for.
**Blockers:** S-003
**Latest event:** Mapped from the owner's confirmed decisions of 2026-11-01.
**Next gate:** Task planning after the site shell (S-003) exists.

## Intent and authority

The owner asked for a demo Grill Board on the site with sample cards and example non-engineering questions. The real board stays local (LMK-001); this page is a demonstration only.

## Outcome

A visitor sees how the board works: cards with Priority and Value, a reason for each, a rating and a "too taxing" flag, and how an answer would flow into a record, using everyday questions rather than engineering ones.

## Why It Matters

The board is the part of the AMS a non-developer is most likely to use. Showing it with familiar questions makes the idea concrete without exposing the owner's real queue.

## Current Verified State

- No demo page exists. The real board's card rules are specified in S-004.

## Desired Behavior

- A page with a small set of sample cards, each clearly labeled as a sample.
- Questions come from non-engineering situations (for example planning an event or choosing a supplier).
- Each card shows the same parts as a real card: Priority and Value with reasons, a 1-5 rating and a "too taxing" flag.
- Interacting with a card is local to the visitor's browser and stores or sends nothing.
- A short explanation shows where a confirmed answer would go in the real system.

## Decisions And Contracts

- The demo uses the real board's card shape and signal colors, so it cannot drift from S-004.
- The demo never reads or writes the owner's real board or any record.

## Non-Goals

- A hosted, working Grill Board; the real one is local only.
- Collecting visitor answers.

## Dependencies And Blockers

- S-003 (site shell); S-004 for the card shape.

## Vertical Implementation Slices

| Task | Slice | Status | Blockers | Proof |
|---|---|---|---|---|
| TK-001 | Demo page with labeled sample cards in the real card shape, deployed to `dev` | ready | none | pending |
| TK-002 | Local-only interaction for rating, flag and answer, with the "where it goes" explanation | ready | TK-001 | pending |

### TK-001 - Sample cards

**Stance:** Builder

Proves the card-shape and sample-label criteria.

### TK-002 - Local interaction

**Stance:** Builder

Proves the no-network criterion.

## Acceptance Criteria

- [ ] **Labeled samples.** Every card is marked as a sample. *Must fail:* a card that could be read as the owner's real item.
- [ ] **Non-engineering questions.** No sample asks about code, branches or tooling. *Check:* content review. *Must fail:* a question about a pull request.
- [ ] **Same shape as the real board.** Cards show Priority, Value, reasons, rating and flag in the signal colors of S-004. *Must fail:* a card missing a reason.
- [ ] **Nothing sent.** Interacting with cards makes no network request and sets no cookie. *Check:* network inspection. *Must fail:* any request on rating.

## RSI and website connection

The page explains the board whose ratings feed the loop (S-002); it produces no loop data itself.

## Testing Seams

- The built page in a browser with network inspection.

## Verification Procedure

```bash
node workbench/tools/spec-workbench.mjs show S-009
# site test command named at Task planning
```

## Documentation Impact

- The tour links the demo from the Grill Board explanation.

## Append-Only Evidence And Execution Log

| Date | Task | Event | Verification | Docs | Remaining gap |
|---|---|---|---|---|---|
| 2026-11-01 | none | Mapped as planned | render, doctor | this Spec | Every criterion |

## Review and Human QA

The owner reviews the page through its Grill Board card (S-005).

## Completion Result

Pending.

## Remaining Limitations Or Follow-Up Specs

- none

## Supersession

- Supersedes: none
- Superseded by: none
