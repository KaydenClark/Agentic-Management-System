# TK-002 - Rows from Supabase render per task and version, each number linked to its rows with its strength label and test rows hidden

**Task ID:** TK-002
**Spec ID:** S-007
**Slice:** Rows from Supabase render per task and version, each number linked to its rows with its strength label and test rows hidden
**Status:** blocked
**Blockers:** TK-001, S-006
**Destination:** spec-acceptance: Every number links; Provenance and series; Not only up; No test rows
**Planned verification:** link-coverage, model-change, regression and test-row render tests

## Assignment

**Target branch:** `dev`. Read this Task and the parent Spec (`../../SPEC.md`) from `origin/main`; branch from `origin/dev`, open a PR into `dev` and merge it once current and checked. Never merge `dev` -> `main`; only the owner does. Orchestrator A's lane: no Supabase service key, no web browsing; check the protected `dev` deployment through the Vercel connector ([ADR-003B](../../../../../../docs/adr/003B-the-dev-site-is-visible-only-to-the-owner-claude-and-codex.md)). Document site commands in `site/README.md`.

Read `AGENTS.md`, the S-006 Spec (`workbench/landmarks/LMK-002-rsi-presentation/specs/S-006-rsi-data-store/SPEC.md`) and its result and run tables under `supabase/migrations/` on `origin/main`, and the chart route on `origin/dev`.

Deliver: the page reads result rows with the publishable key and renders them per task and per version, with provider, model, effort and system version on each series. A model change starts a new series. Regressions, variants, removed versions and fired stop rules are marked. Every number links to the rows behind it and shows each row's strength label. Test rows never render. Render tests use labeled fixtures for each case.

Out of scope: headlines (TK-003); statistics computed differently from the loop's.

Hand back to S-007 with `close`.

## Acceptance

- [ ] A link-coverage test fails on any rendered number without a row link.
- [ ] A model-change fixture renders two series, never one line.
- [ ] A regression fixture shows the regression marked as such.
- [ ] A marked test row in the fixture never renders.
- [ ] Build and tests pass; the `dev` deployment reads live rows or shows the empty state.
