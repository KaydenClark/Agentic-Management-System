# TK-002 - Confirming a card's answer writes it into the owning record, and a changed target is refused

**Task ID:** TK-002
**Spec ID:** S-004
**Slice:** Confirming a card's answer writes it into the owning record, and a changed target is refused
**Status:** blocked
**Blockers:** TK-001
**Destination:** spec-acceptance: Answer lands in its owner; Conflict refusal
**Planned verification:** pytest against a fixture record in a temporary Git repository

## Assignment

**Target branch:** `main`. Branch from `origin/main`, open a PR into `main` and merge it once current and checked, per `AGENTS.md`.

Start from a clean clone. Read `AGENTS.md`, this Task, the parent Spec (`../../SPEC.md`), ADR-000B in `workbench/docs/adr/` (a confirmed answer goes straight to its owner) and the board code TK-001 landed under `grill-board/`.

Deliver: confirming an answer on a card writes it into the record the card names as its owner, in the same step, with no second confirmation. The write records the target's content hash when the card is read and refuses, writing nothing, when the target changed since. Nothing is deleted or renumbered.

Out of scope: ratings and flags (TK-003); writing to any record outside the room.

Hand back to S-004 with `close`.

## Acceptance

- [ ] In a temporary Git repository, confirming a fixture card changes the owning fixture record and needs no second confirmation.
- [ ] An answer that changes only board state fails the test.
- [ ] Editing the target after the card is read makes the confirm refuse and leaves both files byte-identical.
- [ ] `uv run pytest` passes.
