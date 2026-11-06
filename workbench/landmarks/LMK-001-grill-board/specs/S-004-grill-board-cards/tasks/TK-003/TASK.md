# TK-003 - A 1-5 rating and a "too taxing" flag are one click each, saved as committed records, and a flagged card cannot be re-asked unchanged

**Task ID:** TK-003
**Spec ID:** S-004
**Slice:** A 1-5 rating and a "too taxing" flag are one click each, saved as committed records, and a flagged card cannot be re-asked unchanged
**Status:** done
**Blockers:** TK-001
**Destination:** spec-acceptance: Rating and flag; Not a drafting surface
**Planned verification:** pytest over the saved files and a re-post attempt

## Assignment

**Target branch:** `main`. Branch from `origin/main`, open a PR into `main` and merge it once current and checked, per `AGENTS.md`.
**Claimed by:** Claude implementor (Orchestrator B)
**Current claimant:** Claude implementor (Orchestrator B)
**Proof:** pytest 321 passed; 7 mutations fail; live rate/flag 200, re-ask refused

Start from a clean clone. Read `AGENTS.md`, this Task, the parent Spec (`../../SPEC.md`), DDR-000J (too-taxing flag and rating) under `workbench/docs/ddr/` and the board code under `grill-board/`.

Deliver: a 1-5 rating and a "too taxing" flag on each card, one click each, plus an optional comment, saved as committed files (not ignored local files) that the RSI loop can read. A flagged card is held for rewrite: re-posting it with unchanged text is refused.

Out of scope: rewriting the question itself; loop analysis (S-002).

Hand back to S-004 with `close`.

## Acceptance

- [x] One click saves a rating; one click saves the flag; both appear as tracked files, never under an ignored path.
- [x] Re-posting a flagged card with the same text is refused; a changed text is accepted.
- [x] The board offers no editor for pages or routine content.
- [x] `uv run pytest` passes.

## Receipt

| Run | Branch | HEAD SHA | Upstream | Dirty | Tests | Docs touched | Remaining gap | Checksum |
|---|---|---|---|---|---|---|---|---|
| 1 | feat/s004-tk003-rating-flag | b96f10e0c16262c6f78dec22460b0a962af19b39 | ahead 0 behind 0 | 0 | pytest 321 passed; 7 mutations fail; live rate/flag 200, re-ask refused | grill-board/README.md, DDR-000Y, tokens.json | Owner QA; qa/ shots not regenerated; close attribution: {"agent":"Claude implementor (Orchestrator B)","claimant":"Claude implementor (Orchestrator B)","onBehalfOf":null} | 21381b19e48ceb6e89b91f34654d6188077147a917f945877d014b1cbda42b84 |
