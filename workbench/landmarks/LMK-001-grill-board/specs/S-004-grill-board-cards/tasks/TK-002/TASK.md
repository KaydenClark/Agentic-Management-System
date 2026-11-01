# TK-002 - Confirming a card's answer writes it into the owning record, and a changed target is refused

**Task ID:** TK-002
**Spec ID:** S-004
**Slice:** Confirming a card's answer writes it into the owning record, and a changed target is refused
**Status:** done
**Blockers:** TK-001
**Destination:** spec-acceptance: Answer lands in its owner; Conflict refusal
**Planned verification:** pytest against a fixture record in a temporary Git repository

## Assignment

**Target branch:** `main`. Branch from `origin/main`, open a PR into `main` and merge it once current and checked, per `AGENTS.md`.
**Claimed by:** Claude implementor (Orchestrator B)
**Current claimant:** Claude implementor (Orchestrator B)
**Proof:** pytest 151 passed; conflict and path mutations fail; live 409/200/403

Start from a clean clone. Read `AGENTS.md`, this Task, the parent Spec (`../../SPEC.md`), ADR-000B in `workbench/docs/adr/` (a confirmed answer goes straight to its owner) and the board code TK-001 landed under `grill-board/`.

Deliver: confirming an answer on a card writes it into the record the card names as its owner, in the same step, with no second confirmation. The write records the target's content hash when the card is read and refuses, writing nothing, when the target changed since. Nothing is deleted or renumbered.

Out of scope: ratings and flags (TK-003); writing to any record outside the room.

Hand back to S-004 with `close`.

## Acceptance

- [x] In a temporary Git repository, confirming a fixture card changes the owning fixture record and needs no second confirmation.
- [x] An answer that changes only board state fails the test.
- [x] Editing the target after the card is read makes the confirm refuse and leaves both files byte-identical.
- [x] `uv run pytest` passes.

## Receipt

| Run | Branch | HEAD SHA | Upstream | Dirty | Tests | Docs touched | Remaining gap | Checksum |
|---|---|---|---|---|---|---|---|---|
| 1 | feat/s004-tk002-answers | 662cfa14b78614ca798454ad50f6aca63da24f21 | ahead 0 behind 0 | 0 | pytest 151 passed; conflict and path mutations fail; live 409/200/403 | grill-board/README.md, card-example.md | Rating, flag (TK-003); owner QA; close attribution: {"agent":"Claude implementor (Orchestrator B)","claimant":"Claude implementor (Orchestrator B)","onBehalfOf":null} | ea53dafec905c1eb640b789517901f7ede5bf011441efc7ac5460dbaf5d78cb7 |
