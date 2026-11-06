# TK-000K - A coverage check fails when a listed page has no card for its current hash or a card's hash is stale

**Task ID:** TK-000K
**Spec ID:** S-005
**Slice:** A coverage check fails when a listed page has no card for its current hash or a card's hash is stale
**Status:** in-progress
**Blockers:** TK-001
**Destination:** spec-acceptance: Every page covered
**Planned verification:** pytest with a fixture page missing a card and a stale index entry

## Assignment

**Target branch:** `main`. Branch from `origin/main`, open a PR into `main` and merge it once current and checked, per `AGENTS.md`. Nothing in `site/` changes.
**Claimed by:** codex-s005-coverage
**Current claimant:** codex-s005-coverage

Start from a clean clone. Read `AGENTS.md`, this Task, the parent Spec (`../../SPEC.md`), `grill-board/README.md` and the TK-001 generator, index and hash contract.

Owner intent, relayed 2026-11-01: the build stops when the full site is on the protected `dev` deployment with a card for every page. This check is that stop point's proof.

Deliver `uv run ams-pages check`, read-only. It reads the page list at `origin/dev` and the index and cards at HEAD, and exits non-zero, naming each failure, when:

- a listed path has no index entry or no card for its index hash;
- an index entry's landed commit differs from the page list's, so its hash was not recomputed;
- a page has more than one card that is neither stale nor answered;
- a page card names a hash other than its page's index hash and carries no `## Stale` section.

`--recompute` also rebuilds through the TK-001 seam and fails when a served hash differs from the index. On success it prints pages and cards counted. Add the command to the Spec's verification procedure and `RUNBOOK.md`.

Out of scope: writing cards (TK-001); approvals (TK-002); CI wiring, which needs the site build.

Hand back to S-005 with `close`.

## Acceptance

- [x] In a temporary Git repository after a fixture `generate`, `check` exits 0 and reports equal page and card counts.
- [x] Must fail: adding a page to the fixture page list without regenerating makes `check` exit non-zero and name the page.
- [x] Must fail: changing a page's landed commit, or its served `<main>` under `--recompute`, without regenerating makes `check` exit non-zero.
- [x] A second open card for one page makes `check` exit non-zero.
- [ ] Live: after TK-001's live run, `check` against `origin/dev` exits 0.
- [x] `uv run pytest` passes; render and doctor show no blocking finding.

Workspace baseline sha256:248e6840a3518a52d70b5d05c3ba1bf24eee78abd235135447528e2b64a5cf58

## Verified implementation and remaining live gate

Read-only coverage freezes committed review/source inputs and shares the cleanup/protected seam. Manifest paths have no collector fallback. Unit, provenance, held-card, damaged-card, voice-reference and input-drift controls pass; both corrective reviews0. Source97d8 full1079/4 skips and sourcebae full1088/4 skips use actual approved Docker/browser. Exactbae CI1075/9 skips plus11 browser succeeds. [Coverage proof](../../../../../../feedback/REPORT-s005-coverage-servitor-2026-11-06.md) retains earlier failures and genuine956-file/75-original baseline.

The private frozen0fa checkpoint validates50 protected pages,50 current cards/37 stale history, voice0, no-op regeneration, both coverage CLI modes including recomputation/cleanup, and50 selected-card HTTP readbacks with no owner actions/writes and owned server cleanup. It is historical: independently fetched dev is nowcb14e01353216e173b6ab3c998b73193f10ff1ba; PR200 integration/affected acceptance still owns assembly. Current-dev/final capture remains before this Task closes; no stale queue is published as ready.

## Receipt

| Run | Branch | HEAD SHA | Upstream | Dirty | Tests | Docs touched | Remaining gap | Checksum |
|---|---|---|---|---|---|---|---|---|
| 1 | Feature/S-005-page-review-cards | 089c065275679a4e5988a775b003d5385fbc397b | ahead 13 behind 0 | 10 | Uncommitted checker:199focused/2Docker skips;27coverage cases. Expected reds: missing checker/CLI, wrong-owner and unsafe queue/input drift controls; corrected greens. Current source data remains old47. | Coverage command/manifest path/RUNBOOK/Board guide. Native baseline248e and75 ignored originals preserved. | Fresh full with image, independent Review, exact CI, actual current-dev check. Final assembled capture/E/ownerQA/main permission remain; no site changes or owner actions. | acdcbcb6493f6a8a125cd9dc5a464f5117be9240e20481c576d4dca58571823f |
| 2 | Feature/S-005-page-review-cards | 6c468919f821e7b89d2a7008632233650be9f6c8 | ahead 17 behind 0 | 4 | 97d8:136scoped with actual Docker/SIGINT;both correctiveReviews0. Initial0baf full1076/4skips;correctedfreshfull running. Prior201pass/3fixturefail retained281-283. | Coverage report,RUNBOOK,Board guide,manifest,Wiki;FAIL269-285 preserved. | Corrected full/exactCI/current-dev live;consumption,assembledQA,main permission and release remain. No site changes or owner actions. | d70f2a7481d8fca83271b92f1a34ceb52bcd77bf7a1ac51813157846ff9f2646 |
| 3 | Feature/S-005-page-review-cards | bae5871f1d45175971d9e3785ab3ef34c0477f81 | ahead 21 behind 0 | 5 | Historical0fa:50protected responses/49static hashes/actualRSI;50cards/37stale/voice0/no-op;plain and real CLI recompute50/50,cleanup;50HTTP/no writes,server stopped. bae full1088/4skip;CI1075/9+11browser. | Checkpoint proof and private pins/artifacts retained. CurrentGitdevcb14 verified;only live Task criterion remains unchecked. | PR200 current-dev integration/acceptance and final assembled READY capture/current check. Task stays inprogress;ownerQA/main permission/release separate. | e4e6df6891867a8b15e698848da952344165b97ce9742bade615cfd85b42f463 |
