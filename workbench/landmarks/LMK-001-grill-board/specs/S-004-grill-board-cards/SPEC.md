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
**Latest event:** TK-002 closed with proof.
**Next gate:** Complete TK-003.

## Intent and authority

The owner named "make the Grill Board cards" as an example Spec of LMK-001 and confirmed the card rules on 2026-11-01. Orchestrator B builds it locally; it holds the only Supabase keys and never deploys.

## Outcome

The owner opens one local page and sees every item waiting on them, sorted by the signals the owner already uses. Answering an item updates the record that owns it.

## Why It Matters

Priority and Value are how the owner decides what needs attention; without them the queue is noise. Questions that cost too much to answer waste the scarcest input, so the owner can flag them and force a rewrite.

## Current Verified State

- The board serves committed cards with Priority, Value and reasons on 127.0.0.1 in the artifact's layout and colors (TK-001, TK-004, TK-000A). Confirm writes the answer into the card's owning record in one commit and refuses a changed target (TK-002); rating and the flag are inert.

## Desired Behavior

- A Python server runs the board locally. It reads durable records and is never the record itself.
- Agents post only items that need an answer: owner gates, open choices, page approvals and decision texts. Routine content and drafting never go on the board.
- Each card shows Priority and Value, each with a one-line reason, a 1-5 rating and a one-click "too taxing" flag.
- A flagged card is rewritten before it is asked again.
- A confirmed answer is written straight into its owning record, with no bookkeeping step and no re-confirmation.
- Flags, ratings and comments are committed records the loop reads, never ignored local files.
- A write refuses when the target changed since it was read; nothing is deleted or renumbered.
- Colors are signals, each with one stated meaning; there is no fixed count of hues.
- The board looks like the owner's "Grilling Board Redesign" artifact in dark and light and loads nothing from other hosts.

## Decisions And Contracts

- The decision journey on the board is tracked apart from delivery (Specs and Tasks).
- The board is local only; Vercel never serves it.
- Card data lives in plain files in Git; the owner's answer is the source, the owning record the destination.
- The theme follows the artifact; tokens live in `grill-board/theme/tokens.json` ([DDR-000Y](../../../../docs/ddr/000Y-the-grill-board-theme-follows-the-grilling-board-redesign-artifact.md)).

## Non-Goals

- Page review cards (S-005) and the public demo (S-009).
- Accounts, a hosted board or a drafting editor.

## Dependencies And Blockers

- A pinned current Python version in the repository: Python 3.14.5 with uv ([ADR-003D](../../../../docs/adr/003D-python-3-14-5-pinned-with-uv.md)).

## Vertical Implementation Slices

Each Task is one fresh-session run, landed feature -> `main` through a checked PR. Stack: committed card and record files, a Python server on the pinned Python ([ADR-003D](../../../../docs/adr/003D-python-3-14-5-pinned-with-uv.md)), the local page, and pytest against a temporary Git repository.

| Task | Slice | Status | Blockers | Proof |
|---|---|---|---|---|

## Acceptance Criteria

- [ ] **Signals on every card.** Every card shows Priority and Value with a one-line reason each. *Check:* render a fixture card set. *Must fail:* a card with a grade and no reason.
- [ ] **Answer lands in its owner.** Confirming an answer changes the owning record and needs no second confirmation. *Check:* test against a fixture record. *Must fail:* an answer that only changes board state.
- [ ] **Conflict refusal.** A write against a record changed since it was read is refused and nothing is written. *Must fail:* a silent overwrite.
- [ ] **Rating and flag.** A 1-5 rating and a "too taxing" flag are each one click and saved as committed records. A flagged card cannot be re-asked unchanged. *Must fail:* a flagged card re-posted with the same text.
- [ ] **Not a drafting surface.** The board offers no editor for pages or routine content. *Must fail:* a page draft posted as a card.
- [ ] **Colors mean one thing.** Each color has one documented meaning used consistently. *Must fail:* one color used for two meanings.
- [ ] **Local only.** The board starts with one documented local command and no Vercel deployment serves it.
- [ ] **Looks like the artifact.** Layout, formatting and colors match the artifact, dark and light. *Check:* served tokens equal `grill-board/theme/tokens.json`; side-by-side screenshots in `grill-board/qa/`; no third-party request; 375px holds. *Must fail:* a drifted token or a third-party resource.

## RSI and website connection

Ratings and flags are loop inputs: a low-rated or flagged question is a failed result the loop may study (S-002). The public demo (S-009) shows the board's shape with sample cards.

## Testing Seams

- The Python server's HTTP interface against fixture records in a temporary Git repository.

## Verification Procedure

```bash
node workbench/tools/spec-workbench.mjs show S-004
# Python test command named at Task planning
```

## Documentation Impact

- RUNBOOK gains the command that starts the board.
- `grill-board/README.md` holds the board's format, theme and QA detail.

## Append-Only Evidence And Execution Log

Rows are condensed per Task; full proof is in each TASK.md Receipt and Git history.

| Date | Task | Event | Verification | Docs | Remaining gap |
|---|---|---|---|---|---|
| 2026-11-01 | none | Mapped as planned | render, doctor | this Spec | Every criterion |
| 2026-11-01 | TK-001 | Closed; candidate 1ba5df0, [PR #16](https://github.com/KaydenClark/Agentic-Management-System/pull/16) | pytest 12 passed; refusal mutation fails; 127.0.0.1 only | RUNBOOK, ARCHITECTURE, card-example.md | Answers, ratings, flags, colors |
| 2026-11-01 | TK-004 | Closed; candidate 83747aa, [PR #24](https://github.com/KaydenClark/Agentic-Management-System/pull/24) | pytest 65 passed; color tests; drift mutation fails | DDR-000Y, grill-board/README.md | Agent and returned states await TK-002/TK-003 |
| 2026-11-01 | TK-000A | Planned (blocked on TK-004; no fold), closed; candidate 63913a2, [PR #24](https://github.com/KaydenClark/Agentic-Management-System/pull/24) | pytest 121 passed; tokens equal tokens.json; no third-party URL; QA shots | DDR-000Y, grill-board/README.md | Controls inert until TK-002/TK-003 |
| 2026-11-01 | TK-002 | Task closed | pytest 151 passed; conflict and path mutations fail; live 409/200/403 | grill-board/README.md, card-example.md | Rating, flag (TK-003); owner QA; close attribution: {"agent":"Claude implementor (Orchestrator B)","claimant":"Claude implementor (Orchestrator B)","onBehalfOf":null} |

Owner Human QA has not been performed for any Task.

## Review and Human QA

Human QA is the owner using the board on real items.

## Completion Result

Pending.

## Remaining Limitations Or Follow-Up Specs

- S-005 adds page review cards on this board.

## Supersession

- Supersedes: none
- Superseded by: none
