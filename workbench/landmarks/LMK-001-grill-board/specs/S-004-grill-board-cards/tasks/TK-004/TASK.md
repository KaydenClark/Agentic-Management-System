# TK-004 - Every board color has one documented meaning in light and dark

**Task ID:** TK-004
**Spec ID:** S-004
**Slice:** Every board color has one documented meaning in light and dark
**Status:** done
**Blockers:** TK-001
**Destination:** spec-acceptance: Colors mean one thing
**Planned verification:** pytest comparing used colors with the documented list

## Assignment

**Target branch:** `main`. Branch from `origin/main`, open a PR into `main` and merge it once current and checked, per `AGENTS.md`.
**Claimed by:** claude-s004-theme
**Current claimant:** claude-s004-theme
**Proof:** Candidate 83747aab296fdd08a40182f3a84667150337e497: uv run pytest -> 65 passed (52 existing + 13 theme) on Python 3.14.5; grill-board/theme/tokens.json lists 16 tokens with one meaning each, dark and light; test_no_color_is_used_outside_the_token_list, test_no_color_carries_two_meanings_within_a_theme and test_every_token_has_exactly_one_meaning_and_no_meaning_two_tokens; mutation (a drifted --worth and a raw #123456 in board.css) fails two tests

Start from a clean clone. Read `AGENTS.md`, this Task, the parent Spec (`../../SPEC.md`), DDR-000M (colors are signals with one meaning each) under `workbench/docs/ddr/` and the board code under `grill-board/`.

Deliver: one documented list of board colors, each with exactly one meaning, used for both light and dark themes, and a test that every color the page uses is on the list and no meaning has two colors or a color two meanings. There is no fixed count of hues.

Out of scope: the public site's tokens (S-003).

Hand back to S-004 with `close`.

## Acceptance

- [x] The color list is documented with one meaning per color, in light and dark.
- [x] A test fails when the page uses a color not on the list, or one color for two meanings.
- [x] `uv run pytest` passes.

## Receipt

| Run | Branch | HEAD SHA | Upstream | Dirty | Tests | Docs touched | Remaining gap | Checksum |
|---|---|---|---|---|---|---|---|---|
| 1 | feat/s004-artifact-theme | d6eb9cfa13dba4d6eecc2713276494ac517fa0c7 | ahead 0 behind 0 | 0 | Candidate 83747aab296fdd08a40182f3a84667150337e497: uv run pytest -> 65 passed (52 existing + 13 theme) on Python 3.14.5; grill-board/theme/tokens.json lists 16 tokens with one meaning each, dark and light; test_no_color_is_used_outside_the_token_list, test_no_color_carries_two_meanings_within_a_theme and test_every_token_has_exactly_one_meaning_and_no_meaning_two_tokens; mutation (a drifted --worth and a raw #123456 in board.css) fails two tests | DDR-000Y (token table with meanings), grill-board/README.md (theme section) | Signal hues are drawn only where the board has real states (To answer, refusals, why and recommendation boxes); returned and agent lanes appear once TK-002 and TK-003 add their states; owner Human QA not performed; close attribution: {"agent":"claude-s004-theme","claimant":"claude-s004-theme","onBehalfOf":null} | 652c413e76bfbc8f26cd952a1bd922240cd66da28a67a8312ac80ba6971685c2 |
