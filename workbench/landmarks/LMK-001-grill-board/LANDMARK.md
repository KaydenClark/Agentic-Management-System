# LMK-001 - Grill Board

**Landmark ID:** LMK-001
**Status:** planned
**Priority:** 1
**Owner:** Kayden
**Updated:** 2026-11-03
**Catalog description:** The owner's local attention queue, where agents post items that need an answer and confirmed answers land straight in their owning records.
**Blockers:** none
**Next gate:** S-004 DQC tracker/setup and Python Board implementation; owner Human QA remains open.

## Direction

The Grill Board presents DQCs needing the owner: questions and concepts laid out as full readbacks with suggested answers to confirm or correct. DQCs own the interview from its first branches, evolve with its tree, and preserve exact confirmed readbacks, corrections, reasons and history. The [confirmed lifecycle](../../wiki/context-grilling-board.md#jot-af34e4a9-efdf-4688-91d9-0c2d2b0685ba) supplies current meaning.

It runs locally with a Python server, never Vercel. Complete DQC readbacks are visible on cards; routine page drafting remains elsewhere. TRACKER.md projects concepts; TASKBOARD.md projects execution through Landmarks, Specs and Tasks, with stable references in both directions. Ending a round triggers review of changed answers and feedback, then actual reconciliation, authorized preparation or another interview frontier.

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

The decision records under this landmark, one line each, linked to their record.

- [The Grill Board is local, with a Python server](../../docs/ddr/000P-the-grill-board-is-local-with-a-python-server.md)
- [One local page shows what waits on the owner](../../docs/ddr/000L-one-local-page-shows-what-waits-on-the-owner.md)
- [A confirmed Grill Board answer goes straight to its owner](../../docs/adr/000B-a-confirmed-grill-board-answer-goes-straight-to-its-owner.md)
- [The decision journey is tracked apart from delivery](../../docs/ddr/000I-the-decision-journey-is-tracked-apart-from-delivery.md)
- [Every card carries Priority and Value grades](../../docs/ddr/000K-every-card-carries-priority-and-value-grades.md)
- [Every owner question has a too-taxing flag and a rating](../../docs/ddr/000J-every-owner-question-has-a-too-taxing-flag-and-a-rating.md)
- [Colors on owner pages are signals with one meaning each](../../docs/ddr/000M-colors-on-owner-pages-are-signals-with-one-meaning-each.md)
- [Writes to shared stores refuse on conflict](../../docs/adr/002U-writes-to-shared-stores-refuse-on-conflict.md)
- [Approvals move to the Grill Board once it exists](../../docs/ddr/000X-approvals-move-to-the-grill-board-once-it-exists.md)

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

Each reached check is confirmed against what has landed on `main`, by running the child Spec's verification and reading its Current Verified State and the proof it links.

## Reached Result

Pending.

History: [LMK-001 history](../../wiki/history/LMK-001.md).

## Supersession

- Supersedes: none
- Superseded by: none
