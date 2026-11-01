# TK-006 - An under-the-hood page renders build-history rows from Supabase, returns and corrections in order

**Task ID:** TK-006
**Spec ID:** S-003
**Slice:** An under-the-hood page renders build-history rows from Supabase, returns and corrections in order
**Status:** blocked
**Blockers:** TK-001, S-006
**Destination:** spec-acceptance: Under the hood from rows
**Planned verification:** render tests on fixtures and a live read with the publishable key

## Assignment

**Target branch:** `dev`. Read this Task and the parent Spec (`../../SPEC.md`) from `origin/main`; branch from `origin/dev`, open a PR into `dev` and merge it once current and checked. Never merge `dev` -> `main`; only the owner does. Orchestrator A's lane: no Supabase service key, no web browsing; check the protected `dev` deployment through the Vercel connector ([ADR-003B](../../../../../../docs/adr/003B-the-dev-site-is-visible-only-to-the-owner-claude-and-codex.md)). Document site commands in `site/README.md`.

Read `AGENTS.md`, DDR-000O, and S-006's build-history table and import (`supabase/migrations/` and `src/` on `origin/main`).

Deliver the under-the-hood page: it reads S-006's build-history rows with the publishable key only and renders Specs, Tasks, PRs and commits in time order, returns and corrections included, each linking its source. With no rows it says so and names the next expected event. No history text is written by hand; test rows never render.

Out of scope: writing rows (S-006).

Hand back to S-003 with `close`.

## Acceptance

- [ ] Against a fixture with a return and a correction, both render in order with their source links (test).
- [ ] A test fails when any history sentence on the page does not come from a row.
- [ ] A live read on the `dev` deployment shows the rows Supabase holds.
- [ ] Build and tests pass.
