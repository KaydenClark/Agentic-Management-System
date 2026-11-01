# TK-001 - A reader opens the `dev` deployment and gets the shell: navigation, light/dark with toggle, the deployed SHA linked to GitHub, and a server-rendered home page

**Task ID:** TK-001
**Spec ID:** S-003
**Slice:** A reader opens the `dev` deployment and gets the shell: navigation, light/dark with toggle, the deployed SHA linked to GitHub, and a server-rendered home page
**Status:** ready
**Blockers:** none
**Destination:** spec-acceptance: SHA on every page; Responsive and accessible
**Planned verification:** site build and tests plus the `dev` deployment checked at 375 px

## Assignment

**Target branch:** `dev`. Read this Task and the parent Spec (`../../SPEC.md`) from `origin/main`; branch from `origin/dev`, open a PR into `dev` and merge it once current and checked. Never merge `dev` -> `main`; only the owner does. Orchestrator A's lane: no Supabase service key, no web browsing; check the protected `dev` deployment through the Vercel connector ([ADR-003B](../../../../../../docs/adr/003B-the-dev-site-is-visible-only-to-the-owner-claude-and-codex.md)). Document site commands in `site/README.md`.

Read `AGENTS.md`, DDR-000O, DDR-000S and DDR-000M under `workbench/docs/ddr/`, and the scaffold in `site/` on `origin/dev`.

Deliver the shell every page uses, on the existing Next.js scaffold: navigation showing reading position; light and dark following the system with a manual toggle; every color, type and spacing value defined once in a single token file (provisional values until TK-007 records the Grill Board tokens); a footer on every page showing the deployed commit SHA (from Vercel's build environment) linked to its GitHub commit; and a server-rendered home page with a plain-language opener. No third-party fonts or scripts. Write the tests first.

Out of scope: tour content (TK-002, TK-003), draft marks (TK-004), the full quality suite (TK-005).

Hand back to S-003 with `close`: candidate commit on `dev`, deployment URL checked, test output, gaps.

## Acceptance

- [ ] `npm run build` and the site's test command pass in `site/` from a clean clone of `dev`.
- [ ] A test fails when a page's footer SHA differs from the build's commit; the deployed footer equals the `dev` deployment's commit and links to GitHub.
- [ ] The home page text is present in the server-rendered HTML.
- [ ] At 375 px there is no horizontal scroll, in both themes; the toggle overrides the system theme.
- [ ] No color, type or spacing literal exists outside the token file (test).
