# TK-001 - A reader opens the `dev` deployment and gets the shell: navigation, light/dark with toggle, the deployed SHA linked to GitHub, and a server-rendered home page

**Task ID:** TK-001
**Spec ID:** S-003
**Slice:** A reader opens the `dev` deployment and gets the shell: navigation, light/dark with toggle, the deployed SHA linked to GitHub, and a server-rendered home page
**Status:** done
**Blockers:** none
**Destination:** spec-acceptance: SHA on every page; Responsive and accessible
**Planned verification:** site build and tests plus the `dev` deployment checked at 375 px

## Assignment

**Target branch:** `dev`. Read this Task and the parent Spec (`../../SPEC.md`) from `origin/main`; branch from `origin/dev`, open a PR into `dev` and merge it once current and checked. Never merge `dev` -> `main`; only the owner does. Orchestrator A's lane: no Supabase service key, no web browsing; check the protected `dev` deployment through the Vercel connector ([ADR-003B](../../../../../../docs/adr/003B-the-dev-site-is-visible-only-to-the-owner-claude-and-codex.md)). Document site commands in `site/README.md`.
**Claimed by:** orchestrator-A-dispatcher-S003
**Current claimant:** orchestrator-A-dispatcher-S003
**Proof:** PR #13 merged into dev as c529821; npm ci && npm run build && npm test 14/14 pass from a fresh clone (red 10/14 at 90559c8 first); check:browser 15/15 at 375px both themes, toggle overrides system and persists, self-hosted fonts, no off-site requests, home text without JS; Vercel dev deployment dpl_71NzXZ7rd77HgFsxAbgA1oVu7qsd READY at c529821; Codex code and security review no findings at 1fd680b

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

## Receipt

| Run | Branch | HEAD SHA | Upstream | Dirty | Tests | Docs touched | Remaining gap | Checksum |
|---|---|---|---|---|---|---|---|---|
| 1 | claude/sleepy-hamilton-5pyjrw | c529821de4f8f9b8db916dfc9988e365ab06c134 | ahead 7 behind 0 | 0 | PR #13 merged into dev as c529821; npm ci && npm run build && npm test 14/14 pass from a fresh clone (red 10/14 at 90559c8 first); check:browser 15/15 at 375px both themes, toggle overrides system and persists, self-hosted fonts, no off-site requests, home text without JS; Vercel dev deployment dpl_71NzXZ7rd77HgFsxAbgA1oVu7qsd READY at c529821; Codex code and security review no findings at 1fd680b | site/README.md documents npm ci, build, test, check:browser; tokens.css header cites the owner design canvas Color system v2.2 | Deployed footer SHA and home text not fetched from the dev deployment: the Vercel connector's web_fetch refuses this project (owner to extend connector access); contrast, keyboard and automated a11y pass belong to TK-005; tokens unverified against B's theme CDR until TK-007; close attribution: {"agent":"orchestrator-A","claimant":"orchestrator-A-dispatcher-S003","onBehalfOf":"orchestrator-A-dispatcher-S003"} | 08c5aca617f2429ee90aef4dd24b2650e348797aaa50e9575b0c21d742ff7039 |
