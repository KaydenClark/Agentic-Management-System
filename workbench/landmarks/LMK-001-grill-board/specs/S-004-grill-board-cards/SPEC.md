# S-004 - Grill Board cards and answers

**Spec ID:** S-004
**Status:** active
**Priority:** 1
**Owner:** Kayden; orchestrator B (local)
**Stance:** Builder
**Updated:** 2026-11-01
**Catalog description:** Local Grill Board cards with Priority, Value, a rating and a "too taxing" flag, whose confirmed answers are written straight into their owning records.
**Blockers:** none
**Confirmation:** [JOT-6198374a-22d7-45f2-9f3b-3e960abe583e](../../../../wiki/context-active-spec-approvals.md)
**Execution approval:** [JOT-6198374a-22d7-45f2-9f3b-3e960abe583e](../../../../wiki/context-active-spec-approvals.md)
**Next gate:** Owner approval and Human QA, then complete; this supplies no Spec activation slot.

## Intent and authority

The owner named "make the Grill Board cards" as an LMK-001 Spec and confirmed the card rules on 2026-11-01. Orchestrator B builds locally, holds the only Supabase keys and never deploys.

## Outcome

One local page shows every item waiting on the owner, sorted by the owner's signals. Answering an item updates its owning record.

## Why It Matters

Priority and Value are how the owner decides what needs attention. Costly questions waste the scarcest input, so the owner can flag them for rewrite.

## Current Verified State

- Met: every acceptance criterion, each at its linked evidence (TK-001 to TK-000J).
- Review: passed at `4d49bfc` (Orchestrator C); proof in [S-004 history](../../../../wiki/history/S-004.md).
- Not met: owner approval and Human QA.

History: [S-004 history](../../../../wiki/history/S-004.md).

## Desired Behavior

- A local Python server reads durable records and is never the record.
- Agents post only items needing an answer (owner gates, open choices, page approvals, decision texts), never routine content or drafts.
- Each card shows Priority and Value with one-line reasons, a 1-5 rating and a one-click "too taxing" flag; a flagged card is rewritten before it is re-asked.
- A confirmed answer goes straight into its owning record, with no re-confirmation.
- Flags, ratings and comments are committed records the loop reads.
- A write refuses a target changed since it was read; nothing is deleted or renumbered.
- Each color is a signal with one stated meaning.
- It matches the owner's "Grilling Board Redesign" artifact, dark and light, loading nothing from other hosts.

## Decisions And Contracts

- Board decisions are tracked apart from delivery (Specs, Tasks).
- The board is local only; Vercel never serves it.
- Card Context is a note of at most 1,000 characters with no heading or `---` line; else it is refused as page content (TK-000I).
- Card data is plain files in Git; an answer lands in its owning record.
- An owning record is a `.md` file under `workbench/` `specs/`, `landmarks/`, `docs/adr/`, `docs/ddr/` or `wiki/`, or `grill-board/page-approvals.md`; any other path is refused (TK-000G).
- The theme follows the artifact; tokens live in `grill-board/theme/tokens.json` ([DDR-000Y](../../../../docs/ddr/000Y-the-grill-board-theme-follows-the-grilling-board-redesign-artifact.md)).

## Non-Goals

- Page review cards (S-005) and the public demo (S-009).
- Accounts, a hosted board or a drafting editor.

## Dependencies And Blockers

- Python 3.14.5 pinned with uv ([ADR-003D](../../../../docs/adr/003D-python-3-14-5-pinned-with-uv.md)).

## Vertical Implementation Slices

Each Task is one run landed on `main` by a checked PR.

| Task | Slice | Status | Blockers | Proof |
|---|---|---|---|---|

## Acceptance Criteria

- [x] **Signals on every card.** Every card shows Priority and Value with a one-line reason each. *Check:* render a fixture card set. *Must fail:* a card with a grade and no reason. *Evidence:* [board] (TK-001, PR #16).
- [x] **Answer lands in its owner.** Confirming an answer changes the owning record and needs no second confirmation. *Check:* test against a fixture record. *Must fail:* an answer that only changes board state. *Evidence:* [answers] (TK-000G, 3e557c0).
- [x] **Conflict refusal.** A write against a record changed since it was read is refused and nothing is written. *Must fail:* a silent overwrite. *Evidence:* [answers] (TK-002).
- [x] **Rating and flag.** A 1-5 rating and a "too taxing" flag are each one click and saved as committed records. A flagged card cannot be re-asked unchanged. *Must fail:* a flagged card re-posted with the same text. *Evidence:* [ratings] (TK-003; TK-000H, 0356d08).
- [x] **Not a drafting surface.** The board offers no editor for pages or routine content. *Must fail:* a page draft posted as a card. *Evidence:* [ratings] (TK-000I, a06d530).
- [x] **Colors mean one thing.** Each color has one documented meaning used consistently. *Must fail:* one color used for two meanings. *Evidence:* [theme] (TK-004, PR #24).
- [x] **Local only.** The board starts with one documented local command and no Vercel deployment serves it. *Evidence:* [board].
- [x] **Looks like the artifact.** Layout, formatting and colors match the artifact, dark and light. *Check:* served tokens equal `grill-board/theme/tokens.json`; side-by-side screenshots in `grill-board/qa/`; no third-party request; 375px holds. *Must fail:* a drifted token or a third-party resource. *Evidence:* [theme], [qa shots], [375px] (TK-000J, 00b0aa0).

[board]: ../../../../../tests/test_grill_board.py
[answers]: ../../../../../tests/test_grill_board_answers.py
[ratings]: ../../../../../tests/test_grill_board_ratings.py
[theme]: ../../../../../tests/test_grill_board_theme.py
[qa shots]: ../../../../../grill-board/qa/
[375px]: ../../../../../tests/test_grill_board_phone.py

## RSI and website connection

A low-rated or flagged question is a failed result the loop may study (S-002). The demo (S-009) shows the board with sample cards.

## Testing Seams

- The server's HTTP interface on fixture records in a temporary Git repository.

## Verification Procedure

```bash
node workbench/tools/spec-workbench.mjs show S-004
uv run pytest
uv run --with playwright pytest tests/test_grill_board_phone.py
```

## Documentation Impact

- RUNBOOK: the start command. `grill-board/README.md`: format, theme, QA.

## Review and Human QA

Human QA is the owner using the board on real items.

## Completion Result

Pending.

## Remaining Limitations Or Follow-Up Specs

- S-005 adds page review cards on this board.

## Supersession

- Supersedes: none
- Superseded by: none
