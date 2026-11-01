# TK-000A - The board reproduces the artifact's layout, formatting and colors in dark and light

**Task ID:** TK-000A
**Spec ID:** S-004
**Slice:** The board reproduces the artifact's layout, formatting and colors in dark and light
**Status:** blocked
**Blockers:** TK-004
**Destination:** spec-acceptance: Looks like the artifact
**Planned verification:** pytest comparing served CSS tokens with grill-board/theme/tokens.json and checking for third-party resources; Playwright screenshots of the artifact and the board, dark and light, at desktop width and 375px

## Assignment

**Target branch:** `main`. Branch from `origin/main`, open a PR into `main` and merge it once current and checked, per `AGENTS.md`.

Start from a clean clone. Read `AGENTS.md`, this Task, the parent Spec (`../../SPEC.md`), the theme decision record it cites, DDR-000K, DDR-000L, DDR-000M and DDR-000P, and the board code under `src/ams/grill_board/`.

The owner, relayed on 2026-11-01: the board should "basically look exactly like the artifact. The colors, the formatting, the layout. Just make the artifact, but for real." The artifact ("Grilling Board Redesign", version 1793538932-43c3) is the design guide; small calls are the implementor's.

Deliver: the server-rendered board restyled to the artifact's "topics first" layout, typography, spacing and colors, in dark and light with the system preference and a toggle. Token values come from `grill-board/theme/tokens.json` (TK-004). Fonts are self-hosted; the page loads nothing from another host. Controls for answering, rating and the too-taxing flag appear where the artifact puts them, inert until TK-002 and TK-003 wire them. Real card data only.

Blocked on TK-004 because the restyle uses its color list. Out of scope: answering, ratings and flags (TK-002, TK-003); the public site (S-003).

Hand back to S-004 with `close`.

## Acceptance

- [ ] Every CSS custom-property value the board serves equals `grill-board/theme/tokens.json`, in dark and light; a test fails on any drift.
- [ ] Side-by-side screenshots (artifact vs built board, dark and light) are committed under `grill-board/qa/`; the board is rendered from a generic fixture.
- [ ] The page loads no third-party resources; a test fails on any external URL.
- [ ] The board works at desktop width and holds at 375px with no horizontal scroll.
- [ ] `uv run pytest` passes.
