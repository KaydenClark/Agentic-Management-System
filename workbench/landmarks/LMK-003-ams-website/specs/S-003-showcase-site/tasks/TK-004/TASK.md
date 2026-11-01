# TK-004 - A page shows a draft mark until an approval bound to its content hash exists

**Task ID:** TK-004
**Spec ID:** S-003
**Slice:** A page shows a draft mark until an approval bound to its content hash exists
**Status:** done
**Blockers:** TK-001
**Destination:** spec-acceptance: Draft marks
**Planned verification:** draft-mark tests editing approved content

## Assignment

**Target branch:** `dev`. Read this Task and the parent Spec (`../../SPEC.md`) from `origin/main`; branch from `origin/dev`, open a PR into `dev` and merge it once current and checked. Never merge `dev` -> `main`; only the owner does. Orchestrator A's lane: no Supabase service key, no web browsing; check the protected `dev` deployment through the Vercel connector ([ADR-003B](../../../../../../docs/adr/003B-the-dev-site-is-visible-only-to-the-owner-claude-and-codex.md)). Document site commands in `site/README.md`.
**Claimed by:** claude-impl-s003-tk004
**Current claimant:** claude-impl-s003-tk004
**Proof:** PR #82 (07ba43c) merged into dev as 8ba15e0; site builds CI pass; red 70/71 at 2084e5f (draft-marks tests unloadable) then green npm ci && npm run build && npm test 79/79, rerun by orchestrator at 8ba15e0; check:browser 264/264 (axe A/AA, both themes, 375/1280, no-JS text); check:draft-marks 4 real builds: no approvals marks every page, fixture approval at / hash removes it, wrong-hash approval keeps it, one-character edit restores it; site/approvals.json ships empty

Read `AGENTS.md`, DDR-000X under `workbench/docs/ddr/` and the shell on `origin/dev`.

Deliver draft marks: each page shows a draft mark unless a committed approval record names that page and its current content hash. Approvals come only from the owner (in chat until S-005 exists); the agent records an approval only with its dated source and never creates one itself. Editing an approved page restores the mark.

Out of scope: the Grill Board review flow (S-005).

Hand back to S-003 with `close`.

## Acceptance

- [ ] A page with no approval record shows the draft mark.
- [ ] A fixture approval bound to the page's hash removes it; changing one character of the page restores it (test).
- [ ] Build and tests pass.

## Receipt

| Run | Branch | HEAD SHA | Upstream | Dirty | Tests | Docs touched | Remaining gap | Checksum |
|---|---|---|---|---|---|---|---|---|
| 1 | records/s003-tk003-tk004 | 5118ca02294d41709776282fadf59f654de2288f | ahead 0 behind 0 | 0 | PR #82 (07ba43c) merged into dev as 8ba15e0; site builds CI pass; red 70/71 at 2084e5f (draft-marks tests unloadable) then green npm ci && npm run build && npm test 79/79, rerun by orchestrator at 8ba15e0; check:browser 264/264 (axe A/AA, both themes, 375/1280, no-JS text); check:draft-marks 4 real builds: no approvals marks every page, fixture approval at / hash removes it, wrong-hash approval keeps it, one-character edit restores it; site/approvals.json ships empty | site/README.md Draft marks section; npm run page-hashes; npm run check:draft-marks | Hash contract (sha256 of canonical <main>, data-review-exclude and data-review-mark dropped) not yet reconciled with S-005 TK-001 vectors; check:draft-marks runs locally, not in CI; check:browser used a Playwright install outside the repo via NODE_PATH; /_not-found can never be approved; live regions must carry data-review-exclude; draft mark uses the owner hue, meaning not owner-confirmed; dev deployment not inspected; close attribution: {"agent":"claude-orch-s003","claimant":"claude-impl-s003-tk004","onBehalfOf":"claude-impl-s003-tk004"} | 48f6f562394f8ced4e7d7b8bd2f8da16a1b1812ba84f4d13e8be8ae676a3e937 |
