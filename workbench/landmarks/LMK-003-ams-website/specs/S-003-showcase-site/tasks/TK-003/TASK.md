# TK-003 - Why, Limits, Glossary, quickstart and About pages complete the tour, and the quickstart replays on a fresh clone

**Task ID:** TK-003
**Spec ID:** S-003
**Slice:** Why, Limits, Glossary, quickstart and About pages complete the tour, and the quickstart replays on a fresh clone
**Status:** blocked
**Blockers:** TK-002
**Destination:** spec-acceptance: Pages exist; Quickstart replays; Owner words
**Planned verification:** inventory test and quickstart replay test

## Assignment

**Target branch:** `dev`. Read this Task and the parent Spec (`../../SPEC.md`) from `origin/main`; branch from `origin/dev`, open a PR into `dev` and merge it once current and checked. Never merge `dev` -> `main`; only the owner does. Orchestrator A's lane: no Supabase service key, no web browsing; check the protected `dev` deployment through the Vercel connector ([ADR-003B](../../../../../../docs/adr/003B-the-dev-site-is-visible-only-to-the-owner-claude-and-codex.md)). Document site commands in `site/README.md`.

Read `AGENTS.md`, `site/PAGE-TEMPLATE.md` on `origin/main`, `GLOSSARY.md`, `LICENSE` and the tour pages on `origin/dev`.

Deliver the rest of the tour: Why, Limits, Glossary (from `GLOSSARY.md`), a short quickstart and About with a resume summary, all in the reading order. Add a replay test that runs the quickstart's commands on a fresh clone and compares the shown output.

Out of scope: video walkthroughs (open owner choice).

Hand back to S-003 with `close`.

## Acceptance

- [ ] Every tour page the Spec names exists with a plain-language opener; the inventory test passes and fails on a removed page.
- [ ] The quickstart replay test gets the output the page shows.
- [ ] Every page links forward and back.
- [ ] Build and tests pass.

## Reconciled disposition — 2026-11-02

The owner corrections in context-website-presentation.md withdraw the separate quickstart, command replay and resume requirements. Source f148c7c is contained in dev76b9c564692a1e979cffbebbe30063b73588efb6; historical claimant remains on records/s003-tk003-tk004. Current orientation and visual-glossary work belongs to TK-001P and TK-001R under the new assignment. Do not execute the superseded brief. The native lifecycle has no withdrawn/incomplete-run closure; retain this blocked record and evidence rather than fabricate completion or steal its claim.
