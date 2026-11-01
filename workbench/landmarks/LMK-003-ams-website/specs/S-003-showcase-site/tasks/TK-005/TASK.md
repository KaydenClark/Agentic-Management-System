# TK-005 - Hygiene, accessibility, 375 px and no-third-party checks run on the built output

**Task ID:** TK-005
**Spec ID:** S-003
**Slice:** Hygiene, accessibility, 375 px and no-third-party checks run on the built output
**Status:** blocked
**Blockers:** TK-001
**Destination:** spec-acceptance: Public hygiene; No third parties; Responsive and accessible
**Planned verification:** check scripts failing on planted faults

## Assignment

**Target branch:** `dev`. Read this Task and the parent Spec (`../../SPEC.md`) from `origin/main`; branch from `origin/dev`, open a PR into `dev` and merge it once current and checked. Never merge `dev` -> `main`; only the owner does. Orchestrator A's lane: no Supabase service key, no web browsing; check the protected `dev` deployment through the Vercel connector ([ADR-003B](../../../../../../docs/adr/003B-the-dev-site-is-visible-only-to-the-owner-claude-and-codex.md)). Document site commands in `site/README.md`.

Read `AGENTS.md` and the site on `origin/dev`.

Deliver checks over the built output, wired into the site's test command: hygiene (no host path, key or private record ID), accessibility (an automated pass for WCAG AA contrast, keyboard navigation and reduced motion), 375 px layout in both themes, and network requests limited to the site, Supabase and GitHub links. Each check must fail on a planted fault before it passes.

Out of scope: fixing content the checks flag beyond this Task's own pages; report them.

Hand back to S-003 with `close`.

## Acceptance

- [ ] Planting a host path, a fake key, an external font and a low-contrast color each makes its check fail.
- [ ] All checks pass on the current build and run from the documented command.
- [ ] Screenshots of the `dev` deployment at 375 px and desktop in both themes are linked in the hand-back.
