# TK-004 - Every board color has one documented meaning in light and dark

**Task ID:** TK-004
**Spec ID:** S-004
**Slice:** Every board color has one documented meaning in light and dark
**Status:** in-progress
**Blockers:** TK-001
**Destination:** spec-acceptance: Colors mean one thing
**Planned verification:** pytest comparing used colors with the documented list

## Assignment

**Target branch:** `main`. Branch from `origin/main`, open a PR into `main` and merge it once current and checked, per `AGENTS.md`.
**Claimed by:** claude-s004-theme
**Current claimant:** claude-s004-theme

Start from a clean clone. Read `AGENTS.md`, this Task, the parent Spec (`../../SPEC.md`), DDR-000M (colors are signals with one meaning each) under `workbench/docs/ddr/` and the board code under `grill-board/`.

Deliver: one documented list of board colors, each with exactly one meaning, used for both light and dark themes, and a test that every color the page uses is on the list and no meaning has two colors or a color two meanings. There is no fixed count of hues.

Out of scope: the public site's tokens (S-003).

Hand back to S-004 with `close`.

## Acceptance

- [ ] The color list is documented with one meaning per color, in light and dark.
- [ ] A test fails when the page uses a color not on the list, or one color for two meanings.
- [ ] `uv run pytest` passes.
