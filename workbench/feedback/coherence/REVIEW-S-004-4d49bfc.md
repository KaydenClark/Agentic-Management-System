# Review receipt: S-004 re-review at `4d49bfc`

- **Spec:** [S-004 Grill Board cards](../../landmarks/LMK-001-grill-board/specs/S-004-grill-board-cards/SPEC.md)
- **Candidate:** `4d49bfc75efaa81fb3d0ccde07b773ef5af50b05` (`main` after PR #58).
- **Reviewer:** orchestrator C, a Claude cloud session. C did not build S-004.
- **Verdict:** **pass**, recorded with `spec-workbench.mjs verdict`. It replaces the fail at `dd52f70` ([receipt](REVIEW-S-004-dd52f70.md)).

## Method

- `uv run pytest`: 368 passed, 4 skipped.
- `uv run --with playwright pytest tests/test_grill_board_phone.py` (the 375px check, dark and light): 3 passed.
- C re-ran every earlier repro against a live `ams-board` in a throwaway clone.

## Earlier findings

| Finding at `dd52f70` | At `4d49bfc` (C reproduced each live) |
|---|---|
| TK-000G: Confirm wrote into any tracked file | Fixed. Confirm into `.github/workflows/site-build.yml` was refused (409), with 0 commits and the file unchanged. Confirm into an allowed `workbench/wiki/*.md` record still writes one commit containing both the card and the record. |
| TK-000H: punctuation or zero-width characters beat the re-ask guard | Fixed. All five re-ask variants were refused: `taxing ?`, `taxing?!`, no `?`, a zero-width space, and full-width `ＩＳ`. |
| TK-000I: a page draft was shown as a card | Fixed. A card with a page heading in its context is refused when cards load. |
| TK-000J: stale QA shots and no 375px test | Fixed. The `grill-board/qa/` shots (`00b0aa0`) post-date the last UI change (`3e557c0`). The 375px Playwright test passes. |
| TK-000F: no line linked evidence | Fixed. All 8 lines are checked and link test files and fix commits that exist at the candidate. |

## Notes

- **Layout fidelity is owner Human QA.** C checked the tokens, the screenshots and the 375px layout, but whether the board looks like the owner's artifact is for the owner to judge.
- Two color meanings are still compound, `--line-strong` and `--agent` (noted at `dd52f70`). This is not blocking.
- C's own `up_to_spec` checker does not resolve Markdown reference-style links such as `[board]: …`, so it reports 4 of these lines as unknown. The links resolve. This is a gap in C's checker (S-013), not in S-004.
- The verdict row brings the Spec over 8,000 characters, so it returns to B to prune (ADR-002V).
