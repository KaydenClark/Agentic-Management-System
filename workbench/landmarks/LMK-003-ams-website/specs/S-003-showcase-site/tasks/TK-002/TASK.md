# TK-002 - Start here and How it works pages, with plain-language openers and forward and back reading order

**Task ID:** TK-002
**Spec ID:** S-003
**Slice:** Start here and How it works pages, with plain-language openers and forward and back reading order
**Status:** in-progress
**Blockers:** TK-001
**Destination:** spec-acceptance: Pages exist; Reading order
**Planned verification:** inventory and link tests on the built output

## Assignment

**Target branch:** `dev`. Read this Task and the parent Spec (`../../SPEC.md`) from `origin/main`; branch from `origin/dev`, open a PR into `dev` and merge it once current and checked. Never merge `dev` -> `main`; only the owner does. Orchestrator A's lane: no Supabase service key, no web browsing; check the protected `dev` deployment through the Vercel connector ([ADR-003B](../../../../../../docs/adr/003B-the-dev-site-is-visible-only-to-the-owner-claude-and-codex.md)). Document site commands in `site/README.md`.
**Claimed by:** orchestrator-A-dispatcher-S003
**Current claimant:** orchestrator-A-dispatcher-S003

Read `AGENTS.md`, `site/PAGE-TEMPLATE.md` on `origin/main`, `GLOSSARY.md`, and the shell on `origin/dev`.

Deliver the first tour pages: Start here (what the AMS is and refuses to do) and How it works (records, lifecycle, and one real Spec and Task linked to their files on GitHub), each opening with a plain-language summary using no undefined term, then going deeper. Every page links forward and back in one reading order. Add a page inventory test and a link test over the built output.

Out of scope: the remaining tour pages (TK-003).

Hand back to S-003 with `close`.

## Acceptance

- [ ] Both pages exist in the built output with a plain-language opener; the inventory test fails on a placeholder page.
- [ ] The link test fails on a page with no forward or back link.
- [ ] Each owner quote links its dated source; a paraphrase is not shown as a quote.
- [ ] Build and tests pass.
