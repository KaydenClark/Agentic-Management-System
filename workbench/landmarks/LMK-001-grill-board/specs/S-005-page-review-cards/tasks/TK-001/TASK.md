# TK-001 - A generator writes one review card per page in the dev page list, bound to the built page's content hash, and marks a card stale when the hash changes

**Task ID:** TK-001
**Spec ID:** S-005
**Slice:** A generator writes one review card per page in the dev page list, bound to the built page's content hash, and marks a card stale when the hash changes
**Status:** in-progress
**Blockers:** none
**Destination:** spec-acceptance: Every page covered
**Planned verification:** pytest against a fixture page list and built pages in a temporary Git repository; live run against origin/dev

## Assignment

**Target branch:** `main`. Branch from `origin/main`, open a PR into `main` and merge it once current and checked, per `AGENTS.md`. Nothing in `site/` changes; the site is only read.
**Claimed by:** codex-s005-pages
**Current claimant:** codex-s005-pages

Start from a clean clone. Read `AGENTS.md`, this Task, the parent Spec (`../../SPEC.md`, its Decisions), `grill-board/README.md`, `grill-board/card-example.md`, DDR-000X, ADR-002U and the board code in `src/ams/grill_board/` (`cards.py`, `answers.py`: `repository_lock`, `_write_and_commit`). Read the page list with `git fetch origin dev && git show origin/dev:site/page-list.json`; orchestrator A is its only writer and `path` is stable.

Owner intent, relayed by orchestrator B on 2026-11-01: every website page gets a Grill Board review card so the owner can approve or criticize the whole site there.

Deliver `uv run ams-pages generate` (a new script in `pyproject.toml`):

1. **Read one current candidate.** Pin the current website review/deployment candidate and reconcile its complete built public-route inventory with `site/page-list.json`, including every skills article. Hash the served HTML from that one frozen build, including its current shared shell. `landed.commit` remains provenance; it must never select historical content for a current approval. A route present in only the list or only the build refuses without writing. The build/HTML seam is injectable for safe synthetic fixtures; actual current-build and protected-deployment evidence remain required.

2. **Hash.** Content hash = `sha256:` + SHA-256 hex of the canonical content of `<main id="main">`: drop `script` and `style` and any subtree carrying `data-review-mark` or `data-review-exclude`; join text nodes and `href`, `src` and `alt` values in document order; collapse whitespace to single spaces and trim; encode UTF-8. The footer's commit SHA is outside `<main>`, so a rebuild alone never changes a hash. Commit the contract in `grill-board/README.md` and test vectors (HTML plus expected hash) under `tests/fixtures/grill_board/pages/`, so S-003 TK-004 can match them.
3. **Cards.** One card per page and hash, `grill-board/cards/page-SLUG-HASH12.md` (`/` is `home`). Header: `Topic: Website pages`; Priority and Value with one-line reasons (DDR-000K); `Page`, `Title`, `Content hash`, `Landed` (branch, commit, PR), `Spec`, `Task`; `Recommendation: Approve page PATH (TITLE) at content hash HASH.`; `Owner record: grill-board/page-approvals.md`; `Write after: ## Approvals`. Context names the sources and the page's path on the protected `dev` deployment. Create `grill-board/page-approvals.md` with that anchor if absent, so Confirm works through the S-004 path.
4. **Index.** `grill-board/pages/index.json` holds, per listed path, the title, landed commit, hash and current card name.
5. **Stale.** When a page's hash changes, write the new card and append `## Stale` (`**Superseded by:** NAME`, `**Stale since:**` in UTC) to the previous card. Never edit or remove an existing section; answered history stays byte-for-byte. The board lists stale cards outside the queue and refuses to answer them.
6. **Idempotent.** A rerun with no change writes nothing and makes no commit. A change is one commit of cards, index and approvals record through the board's lock and compare-and-swap, subject `Grill Board: page cards for N pages`.

Out of scope: approval readback and stale-confirm refusal hardening (TK-002); the voice record (TK-003); the coverage check (TK-000K); any `site/` change. If a page needs a `data-review-exclude` region (live data on `/rsi`), ask orchestrator A; do not edit `site/`.

Hand back to S-005 with `close`.

## Acceptance

- [ ] In a temporary Git repository with a fixture page list of two pages and injected HTML, `generate` writes exactly one card per page, each naming the hash the test vectors predict, plus the index and approvals record, in one commit.
- [ ] A second run with the same input writes nothing and makes no commit.
- [ ] Changing one character inside a fixture page's `<main>` writes a new card for the new hash and appends `## Stale` to the old one; changing only the footer SHA changes no hash.
- [ ] Must fail: a run that rewrites any existing section of an answered card, or a page with no card after a run, fails the test.
- [ ] The board lists a stale card outside the queue and refuses an answer to it, writing nothing.
- [ ] Live: against one identified current built candidate, the complete route set (including the skills index and every article) has cards shown under "Website pages"; missing page-list/built coverage refuses.
- [ ] `uv run pytest` passes; render and doctor show no blocking finding.

## Starting preservation

Workspace baseline sha256:81dd8dfc83cf2aaa52dcbc6b763823137fe82ede9d053bb84a22225d4f2feb2d

The original claim-state bytes are committed before this inventory. Raw local inventory stays outside the checkout; local retention is not claimed as remote recovery.

## Stopped implementation checkpoint

Current source is incomplete and unaccepted. The initial missing-module red was expected. Existing Board tests passed 115/115 before product changes, with approved loopback sockets; the first sandbox baseline failed at socket binding (97 failed/18 passed), an environment limitation rather than a product finding.

Two later verification failures triggered the RUNBOOK stop:

1. Generator creation initially failed because the existing compare-and-swap index writer did not pass `git update-index --add` for newly created files. That defect was corrected before the next run.
2. The next `tests/test_pages.py -xq` run passed generation/idempotency but failed the stale answered-card diagnostic assertion: expected `stale`, received `already answered` from the existing earlier answer check. Refusal still occurs; the stale-specific requirement and regression evidence remain unresolved. No further product correction or test retry followed.

Implemented seam at the stopped source: `ams.pages.generate(root, inventory, built_html_by_route, candidate=SHA)` compares the exact list/build route sets, hashes the current injected HTML, generates cards/index/approval anchor through the Board lock/CAS, appends stale history, and makes identical reruns a no-op. `landed.commit` is retained separately. CLI accepts `--inventory FILE --built-html FILE --candidate SHA`; these are explicit frozen build artifacts, not proof of an actual build. Automatic pinned-build collection, live current-candidate coverage, remaining new tests, post-change Board regression tests and required full checks are unperformed.

Required scoped continuation: inspect the stopped diagnostic failure and source before correction, preserve both failed runs, finish the real current-build collector/integration, then run the unchanged behavioral and regression gates. A new Task name does not erase this stop. No approval, criticism consumption, Human QA, Supabase path or delivery is claimed.
