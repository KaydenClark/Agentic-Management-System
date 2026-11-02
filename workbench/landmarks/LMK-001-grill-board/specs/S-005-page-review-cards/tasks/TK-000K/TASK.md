# TK-000K - A coverage check fails when a listed page has no card for its current hash or a card's hash is stale

**Task ID:** TK-000K
**Spec ID:** S-005
**Slice:** A coverage check fails when a listed page has no card for its current hash or a card's hash is stale
**Status:** blocked
**Blockers:** TK-001
**Destination:** spec-acceptance: Every page covered
**Planned verification:** pytest with a fixture page missing a card and a stale index entry

## Assignment

**Target branch:** `main`. Branch from `origin/main`, open a PR into `main` and merge it once current and checked, per `AGENTS.md`. Nothing in `site/` changes.

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
