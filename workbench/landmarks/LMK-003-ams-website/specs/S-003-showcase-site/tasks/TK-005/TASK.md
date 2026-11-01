# TK-005 - Hygiene, accessibility, 375 px and no-third-party checks run on the built output

**Task ID:** TK-005
**Spec ID:** S-003
**Slice:** Hygiene, accessibility, 375 px and no-third-party checks run on the built output
**Status:** done
**Blockers:** TK-001
**Destination:** spec-acceptance: Public hygiene; No third parties; Responsive and accessible
**Planned verification:** check scripts failing on planted faults

## Assignment

**Target branch:** `dev`. Read this Task and the parent Spec (`../../SPEC.md`) from `origin/main`; branch from `origin/dev`, open a PR into `dev` and merge it once current and checked. Never merge `dev` -> `main`; only the owner does. Orchestrator A's lane: no Supabase service key, no web browsing; check the protected `dev` deployment through the Vercel connector ([ADR-003B](../../../../../../docs/adr/003B-the-dev-site-is-visible-only-to-the-owner-claude-and-codex.md)). Document site commands in `site/README.md`.
**Claimed by:** orchestrator-A-dispatcher-S003-qa
**Current claimant:** orchestrator-A-dispatcher-S003-qa
**Proof:** PR #25 (0970944) merged into demo batch site/demo-batch-20261102 for one dev merge; npm test hygiene scan of every served file (host paths, keys, JWTs, private IDs, session links, external loads in every resource attribute); check:browser over every route at 375 and 1280 px in both themes: axe WCAG A/AA incl. contrast, Tab reach with visible focus change, reduced motion, 375 px no scroll, requests only to site/Supabase/GitHub, with nine planted-fault self-tests; host path, fake key, external font and low contrast each failed before passing; Codex findings (focus visibility, multi-attribute scan) fixed red/green; Codex clean at 0970944; batch npm test 59/59, check:browser 149/149

Read `AGENTS.md` and the site on `origin/dev`.

Deliver checks over the built output, wired into the site's test command: hygiene (no host path, key or private record ID), accessibility (an automated pass for WCAG AA contrast, keyboard navigation and reduced motion), 375 px layout in both themes, and network requests limited to the site, Supabase and GitHub links. Each check must fail on a planted fault before it passes.

Out of scope: fixing content the checks flag beyond this Task's own pages; report them.

Hand back to S-003 with `close`.

## Acceptance

- [ ] Planting a host path, a fake key, an external font and a low-contrast color each makes its check fail.
- [ ] All checks pass on the current build and run from the documented command.
- [ ] Screenshots of the `dev` deployment at 375 px and desktop in both themes are linked in the hand-back.

## Receipt

| Run | Branch | HEAD SHA | Upstream | Dirty | Tests | Docs touched | Remaining gap | Checksum |
|---|---|---|---|---|---|---|---|---|
| 1 | site/demo-batch-20261102 | 7dfb1459f0c434a0d7df246790717a53e7b058e5 | ahead 0 behind 0 | 0 | PR #25 (0970944) merged into demo batch site/demo-batch-20261102 for one dev merge; npm test hygiene scan of every served file (host paths, keys, JWTs, private IDs, session links, external loads in every resource attribute); check:browser over every route at 375 and 1280 px in both themes: axe WCAG A/AA incl. contrast, Tab reach with visible focus change, reduced motion, 375 px no scroll, requests only to site/Supabase/GitHub, with nine planted-fault self-tests; host path, fake key, external font and low contrast each failed before passing; Codex findings (focus visibility, multi-attribute scan) fixed red/green; Codex clean at 0970944; batch npm test 59/59, check:browser 149/149 | site/README.md documents npm test and npm run check:browser | Focus check requires a visible change but does not measure indicator contrast; screenshots are from local next start, not the dev deployment; reduced-motion check fails any transition over 0.01s, so pages must disable motion under prefers-reduced-motion; close attribution: {"agent":"orchestrator-A","claimant":"orchestrator-A-dispatcher-S003-qa","onBehalfOf":"orchestrator-A-dispatcher-S003-qa"} | 79cf3a49aa3320fe75ddb0dd8c1c9eab18b6fc3663c25d9fb4a1446bbcfca7d8 |
