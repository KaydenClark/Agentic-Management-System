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

- [ ] In a temporary Git repository after a fixture `generate`, `check` exits 0 and reports equal page and card counts.
- [ ] Must fail: adding a page to the fixture page list without regenerating makes `check` exit non-zero and name the page.
- [ ] Must fail: changing a page's landed commit, or its served `<main>` under `--recompute`, without regenerating makes `check` exit non-zero.
- [ ] A second open card for one page makes `check` exit non-zero.
- [ ] Live: after TK-001's live run, `check` against `origin/dev` exits 0.
- [ ] `uv run pytest` passes; render and doctor show no blocking finding.

Workspace baseline sha256:248e6840a3518a52d70b5d05c3ba1bf24eee78abd235135447528e2b64a5cf58

## Current implementation

The existing read-only checker/CLI is under verification. Normal check freezes the fetched source inventory and reads one committed review snapshot; recompute shares the existing collector, cleanup and protected overlay. Manifest-declared inventory paths follow the single reader. Explicit injected inputs stay fixture evidence.

Retain approved historical/verified/pending provenance: pending has landed:null and must bind the frozen candidate/integration-pending state. No landing is invented. Coverage also refuses damaged extra page questions and missing/future voice references on open cards, while keeping stale/answered history.

Uncommitted coverage/collector/capture/page/approval/feedback/browser checks pass199 with2 Docker skips (no image configured for that focused run). The27-case coverage matrix includes input drift, damaged extra page cards and missing/future voice references. Fresh full with the approved image, independent Review, current CI and actual current-dev live coverage remain before close. Final assembled QA/consumption/owner judgments and main permission remain separate. No site edit or actual owner feedback.

## Receipt

| Run | Branch | HEAD SHA | Upstream | Dirty | Tests | Docs touched | Remaining gap | Checksum |
|---|---|---|---|---|---|---|---|---|
| 1 | Feature/S-005-page-review-cards | 089c065275679a4e5988a775b003d5385fbc397b | ahead 13 behind 0 | 10 | Uncommitted checker:199focused/2Docker skips;27coverage cases. Expected reds: missing checker/CLI, wrong-owner and unsafe queue/input drift controls; corrected greens. Current source data remains old47. | Coverage command/manifest path/RUNBOOK/Board guide. Native baseline248e and75 ignored originals preserved. | Fresh full with image, independent Review, exact CI, actual current-dev check. Final assembled capture/E/ownerQA/main permission remain; no site changes or owner actions. | acdcbcb6493f6a8a125cd9dc5a464f5117be9240e20481c576d4dca58571823f |
