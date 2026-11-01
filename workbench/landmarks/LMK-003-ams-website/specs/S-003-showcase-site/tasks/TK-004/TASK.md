# TK-004 - A page shows a draft mark until an approval bound to its content hash exists

**Task ID:** TK-004
**Spec ID:** S-003
**Slice:** A page shows a draft mark until an approval bound to its content hash exists
**Status:** in-progress
**Blockers:** TK-001
**Destination:** spec-acceptance: Draft marks
**Planned verification:** draft-mark tests editing approved content

## Assignment

**Target branch:** `dev`. Read this Task and the parent Spec (`../../SPEC.md`) from `origin/main`; branch from `origin/dev`, open a PR into `dev` and merge it once current and checked. Never merge `dev` -> `main`; only the owner does. Orchestrator A's lane: no Supabase service key, no web browsing; check the protected `dev` deployment through the Vercel connector ([ADR-003B](../../../../../../docs/adr/003B-the-dev-site-is-visible-only-to-the-owner-claude-and-codex.md)). Document site commands in `site/README.md`.
**Claimed by:** orchestrator-A-dispatcher-S003
**Current claimant:** orchestrator-A-dispatcher-S003

Read `AGENTS.md`, DDR-000X under `workbench/docs/ddr/` and the shell on `origin/dev`.

Deliver draft marks: each page shows a draft mark unless a committed approval record names that page and its current content hash. Approvals come only from the owner (in chat until S-005 exists); the agent records an approval only with its dated source and never creates one itself. Editing an approved page restores the mark.

Out of scope: the Grill Board review flow (S-005).

Hand back to S-003 with `close`.

## Acceptance

- [ ] A page with no approval record shows the draft mark.
- [ ] A fixture approval bound to the page's hash removes it; changing one character of the page restores it (test).
- [ ] Build and tests pass.
