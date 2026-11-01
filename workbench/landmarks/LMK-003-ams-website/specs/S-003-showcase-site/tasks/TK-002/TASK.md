# TK-002 - Start here and How it works pages, with plain-language openers and forward and back reading order

**Task ID:** TK-002
**Spec ID:** S-003
**Slice:** Start here and How it works pages, with plain-language openers and forward and back reading order
**Status:** done
**Blockers:** TK-001
**Destination:** spec-acceptance: Pages exist; Reading order
**Planned verification:** inventory and link tests on the built output

## Assignment

**Target branch:** `dev`. Read this Task and the parent Spec (`../../SPEC.md`) from `origin/main`; branch from `origin/dev`, open a PR into `dev` and merge it once current and checked. Never merge `dev` -> `main`; only the owner does. Orchestrator A's lane: no Supabase service key, no web browsing; check the protected `dev` deployment through the Vercel connector ([ADR-003B](../../../../../../docs/adr/003B-the-dev-site-is-visible-only-to-the-owner-claude-and-codex.md)). Document site commands in `site/README.md`.
**Claimed by:** orchestrator-A-dispatcher-S003
**Current claimant:** orchestrator-A-dispatcher-S003
**Proof:** PR #23 (0418ac7) merged into demo batch site/demo-batch-20261102 for one dev merge; /start and /how-it-works with plain-language openers; red 37/49 at 9f0e8fa then green 49/49 at 542f241; inventory and link tests with planted faults (placeholder, missing opener, undefined term, unsourced or non-verbatim quote, dead end); owner quote verified verbatim against workbench/wiki/context-ams-purpose.md; tour-375 20/20; Codex code and security clean at 0418ac7; batch npm test 59/59

Read `AGENTS.md`, `site/PAGE-TEMPLATE.md` on `origin/main`, `GLOSSARY.md`, and the shell on `origin/dev`.

Deliver the first tour pages: Start here (what the AMS is and refuses to do) and How it works (records, lifecycle, and one real Spec and Task linked to their files on GitHub), each opening with a plain-language summary using no undefined term, then going deeper. Every page links forward and back in one reading order. Add a page inventory test and a link test over the built output.

Out of scope: the remaining tour pages (TK-003).

Hand back to S-003 with `close`.

## Acceptance

- [ ] Both pages exist in the built output with a plain-language opener; the inventory test fails on a placeholder page.
- [ ] The link test fails on a page with no forward or back link.
- [ ] Each owner quote links its dated source; a paraphrase is not shown as a quote.
- [ ] Build and tests pass.

## Receipt

| Run | Branch | HEAD SHA | Upstream | Dirty | Tests | Docs touched | Remaining gap | Checksum |
|---|---|---|---|---|---|---|---|---|
| 1 | site/demo-batch-20261102 | 060692ee9d956108a6c3df8c720ef0b18ad4955d | ahead 0 behind 0 | 0 | PR #23 (0418ac7) merged into demo batch site/demo-batch-20261102 for one dev merge; /start and /how-it-works with plain-language openers; red 37/49 at 9f0e8fa then green 49/49 at 542f241; inventory and link tests with planted faults (placeholder, missing opener, undefined term, unsourced or non-verbatim quote, dead end); owner quote verified verbatim against workbench/wiki/context-ams-purpose.md; tour-375 20/20; Codex code and security clean at 0418ac7; batch npm test 59/59 | site/README.md Tour pages; site/page-list.json entries /start and /how-it-works | Task links point at blob/dev and break when ADR-000T deletes Task files at Spec close; owner approval of page content pending (draft mark is TK-004); dev deployment content to be verified on the owner's machine; close attribution: {"agent":"orchestrator-A","claimant":"orchestrator-A-dispatcher-S003","onBehalfOf":"orchestrator-A-dispatcher-S003"} | 8319121b51b091f8e8fd2abfa1bedab0f42550343fa205e39dc5a90d81c0f9e7 |
