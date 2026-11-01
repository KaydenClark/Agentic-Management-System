# TK-003 - A 1-5 rating and a "too taxing" flag are one click each, saved as committed records, and a flagged card cannot be re-asked unchanged

**Task ID:** TK-003
**Spec ID:** S-004
**Slice:** A 1-5 rating and a "too taxing" flag are one click each, saved as committed records, and a flagged card cannot be re-asked unchanged
**Status:** blocked
**Blockers:** TK-001
**Destination:** spec-acceptance: Rating and flag; Not a drafting surface
**Planned verification:** pytest over the saved files and a re-post attempt

## Assignment

**Target branch:** `main`. Branch from `origin/main`, open a PR into `main` and merge it once current and checked, per `AGENTS.md`.

Start from a clean clone. Read `AGENTS.md`, this Task, the parent Spec (`../../SPEC.md`), DDR-000J (too-taxing flag and rating) under `workbench/docs/ddr/` and the board code under `grill-board/`.

Deliver: a 1-5 rating and a "too taxing" flag on each card, one click each, plus an optional comment, saved as committed files (not ignored local files) that the RSI loop can read. A flagged card is held for rewrite: re-posting it with unchanged text is refused.

Out of scope: rewriting the question itself; loop analysis (S-002).

Hand back to S-004 with `close`.

## Acceptance

- [ ] One click saves a rating; one click saves the flag; both appear as tracked files, never under an ignored path.
- [ ] Re-posting a flagged card with the same text is refused; a changed text is accepted.
- [ ] The board offers no editor for pages or routine content.
- [ ] `uv run pytest` passes.
