# TK-007 - Recorded Grill Board tokens and a check that every value equals one

**Task ID:** TK-007
**Spec ID:** S-003
**Slice:** Recorded Grill Board tokens and a check that every value equals one
**Status:** in-progress
**Blockers:** none
**Destination:** spec-acceptance: Theme tokens
**Planned verification:** token comparison script failing on a stray color

## Assignment

**Target branch:** `dev`. Read this Task and the parent Spec (`../../SPEC.md`) from `origin/main`; branch from `origin/dev`, open a PR into `dev` and merge it once current and checked. Never merge `dev` -> `main`; only the owner does. Orchestrator A's lane: no Supabase service key, no web browsing; check the protected `dev` deployment through the Vercel connector ([ADR-003B](../../../../../../docs/adr/003B-the-dev-site-is-visible-only-to-the-owner-claude-and-codex.md)). Document site commands in `site/README.md`.
**Claimed by:** orchestrator-A
**Current claimant:** orchestrator-A

Blocked until the owner resolves `grill-board-theme-tokens` in S-003: the old Grill Board's values are not in this public repository. Read `AGENTS.md`, DDR-000M and the token file on `origin/dev`.

Deliver: a theme decision record listing every token with its source and meaning, the token file set to those values, and a comparison script in the site's checks that fails when any color, type or spacing value differs from the record.

Hand back to S-003 with `close`.

## Acceptance

- [ ] The decision record lists every token and cites the owner's answer.
- [ ] The comparison script fails on a planted stray color and passes on the build.
