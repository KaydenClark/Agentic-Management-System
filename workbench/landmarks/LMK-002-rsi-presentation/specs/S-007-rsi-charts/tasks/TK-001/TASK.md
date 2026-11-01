# TK-001 - The chart page is live on `dev` with every series place and the honest "no trials yet" state

**Task ID:** TK-001
**Spec ID:** S-007
**Slice:** The chart page is live on `dev` with every series place and the honest "no trials yet" state
**Status:** done
**Blockers:** none
**Destination:** spec-acceptance: Honest empty state
**Planned verification:** render test on an empty fixture plus the `dev` deployment

## Assignment

**Target branch:** `dev`. Read this Task and the parent Spec (`../../SPEC.md`) from `origin/main`; branch from `origin/dev`, open a PR into `dev` and merge it once current and checked. Never merge `dev` -> `main`; only the owner does. Orchestrator A's lane: no Supabase service key, no web browsing; check the protected `dev` deployment through the Vercel connector ([ADR-003B](../../../../../../docs/adr/003B-the-dev-site-is-visible-only-to-the-owner-claude-and-codex.md)). Document site commands in `site/README.md`.
**Claimed by:** orchestrator-A-dispatcher-S007
**Current claimant:** orchestrator-A-dispatcher-S007
**Proof:** PR #14 merged into dev as fceec12; red: 6/6 rsi tests failed at 66f04e1 with no route; green: npm test 33/33 at bb2b3a4 after merging dev; 11 planted faults (dropped place, merged sections, missing empty message/explanation/next event, digit in a place or intro, drawn SVG, hidden/display:none/aria-hidden) each fail their check; Playwright at 375px light and dark: scrollWidth 375, zero off-site requests; Vercel preview READY at bb2b3a4; Codex code and security review no findings

Read `AGENTS.md`, DDR-000T and DDR-000O under `workbench/docs/ddr/`, ADR-000A under `workbench/docs/adr/`, and `site/` on `origin/dev`.

Deliver the chart route in `site/`: one place for each planned series (per task and per version, dev and held-out visibly separate). With no rows each place says that no trials are recorded yet, explains task, trial and version in plain words, and names the next expected event. No sample chart and no number. Use S-003's shell and tokens if they are on `dev`; never edit the shell. Write the render test first against an empty fixture.

Out of scope: reading Supabase (TK-002), headlines (TK-003).

Hand back to S-007 with `close`.

## Acceptance

- [ ] With an empty fixture the page builds and shows every series place and the explanation (test).
- [ ] A test fails if the empty page contains a digit inside a chart place or hides a section.
- [ ] The page is reachable on the `dev` deployment.

## Receipt

| Run | Branch | HEAD SHA | Upstream | Dirty | Tests | Docs touched | Remaining gap | Checksum |
|---|---|---|---|---|---|---|---|---|
| 1 | claude/sleepy-hamilton-5pyjrw | aae1a7219b630cbe78a1f392fcd62c092327730e | ahead 0 behind 0 | 0 | PR #14 merged into dev as fceec12; red: 6/6 rsi tests failed at 66f04e1 with no route; green: npm test 33/33 at bb2b3a4 after merging dev; 11 planted faults (dropped place, merged sections, missing empty message/explanation/next event, digit in a place or intro, drawn SVG, hidden/display:none/aria-hidden) each fail their check; Playwright at 375px light and dark: scrollWidth 375, zero off-site requests; Vercel preview READY at bb2b3a4; Codex code and security review no findings | site/README.md section RSI charts (/rsi); site/page-list.json entry /rsi | Page not fetched on the dev deployment: the Vercel connector's web_fetch refuses this project (owner to extend connector access); hidden-content test cannot see hiding from global or shell CSS classes; live Supabase reads are TK-002; close attribution: {"agent":"orchestrator-A","claimant":"orchestrator-A-dispatcher-S007","onBehalfOf":"orchestrator-A-dispatcher-S007"} | 393aafbd6408979389491c0fd35e39c684e1a742fca6f982f2fa5932af37fb1c |
