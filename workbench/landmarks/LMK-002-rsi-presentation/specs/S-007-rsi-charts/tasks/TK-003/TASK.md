# TK-003 - A headline appears only from held-out rows with interval and baseline, and a zero-crossing interval reads as no difference detected

**Task ID:** TK-003
**Spec ID:** S-007
**Slice:** A headline appears only from held-out rows with interval and baseline, and a zero-crossing interval reads as no difference detected
**Status:** blocked
**Blockers:** TK-002
**Destination:** spec-acceptance: Held-out headlines
**Planned verification:** headline render tests on dev-only, held-out and zero-crossing fixtures

## Assignment

**Target branch:** `dev`. Read this Task and the parent Spec (`../../SPEC.md`) from `origin/main`; branch from `origin/dev`, open a PR into `dev` and merge it once current and checked. Never merge `dev` -> `main`; only the owner does. Orchestrator A's lane: no Supabase service key, no web browsing; check the protected `dev` deployment through the Vercel connector ([ADR-003B](../../../../../../docs/adr/003B-the-dev-site-is-visible-only-to-the-owner-claude-and-codex.md)). Document site commands in `site/README.md`.

Read `AGENTS.md`, ADR-000A, ADR-002I under `workbench/docs/adr/` and the chart page on `origin/dev`.

Deliver headline rules: a headline appears only from held-out rows, stated with its interval and its baseline. An interval that includes zero reads as "no difference detected at this size". Dev-task rows never make a headline. Use the interval the loop recorded; never recompute it in the browser.

Hand back to S-007 with `close`.

## Acceptance

- [ ] A dev-only fixture renders no headline.
- [ ] A held-out fixture renders the headline with interval and baseline.
- [ ] A zero-crossing fixture renders the no-difference wording, never "improved".
- [ ] Build and tests pass.
