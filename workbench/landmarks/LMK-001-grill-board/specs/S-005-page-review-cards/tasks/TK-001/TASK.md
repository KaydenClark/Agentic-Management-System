# TK-001 - A generator writes one review card per page in the dev page list, bound to the built page's content hash, and marks a card stale when the hash changes

**Task ID:** TK-001
**Spec ID:** S-005
**Slice:** A generator writes one review card per page in the dev page list, bound to the built page's content hash, and marks a card stale when the hash changes
**Status:** ready
**Blockers:** none
**Destination:** spec-acceptance: Every page covered
**Planned verification:** pytest against a fixture page list and built pages in a temporary Git repository; live run against origin/dev

## Assignment

**Target branch:** `main`. Branch from `origin/main`, open a PR into `main` and merge it once current and checked, per `AGENTS.md`. Nothing in `site/` changes; the site is only read.

Start from a clean clone. Read `AGENTS.md`, this Task, the parent Spec (`../../SPEC.md`, its Decisions), `grill-board/README.md`, `grill-board/card-example.md`, DDR-000X, ADR-002U and the board code in `src/ams/grill_board/` (`cards.py`, `answers.py`: `repository_lock`, `_write_and_commit`). Read the page list with `git fetch origin dev && git show origin/dev:site/page-list.json`; orchestrator A is its only writer and `path` is stable.

Owner intent, relayed by orchestrator B on 2026-11-01: every website page gets a Grill Board review card so the owner can approve or criticize the whole site there. The owner demos at 8:00 the next morning; this slice comes first.

Deliver `uv run ams-pages generate` (a new script in `pyproject.toml`):

1. **Read** the page list at `origin/dev`. For each distinct `landed.commit`, export that tree with `git archive` into a temporary directory, run `npm ci` and `npm run build` in `site/`, start `next start` on 127.0.0.1 and fetch each listed path. The build step is an injectable seam so tests pass fixture HTML.
2. **Hash.** Content hash = `sha256:` + SHA-256 hex of the canonical content of `<main id="main">`: drop `script` and `style` and any subtree carrying `data-review-mark` or `data-review-exclude`; join text nodes and `href`, `src` and `alt` values in document order; collapse whitespace to single spaces and trim; encode UTF-8. The footer's commit SHA is outside `<main>`, so a rebuild alone never changes a hash. Commit the contract in `grill-board/README.md` and test vectors (HTML plus expected hash) under `tests/fixtures/grill_board/pages/`, so S-003 TK-004 can match them.
3. **Cards.** One card per page and hash, `grill-board/cards/page-SLUG-HASH12.md` (`/` is `home`). Header: `Topic: Website pages`; Priority and Value with one-line reasons (DDR-000K); `Page`, `Title`, `Content hash`, `Landed` (branch, commit, PR), `Spec`, `Task`; `Recommendation: Approve page PATH (TITLE) at content hash HASH.`; `Owner record: grill-board/page-approvals.md`; `Write after: ## Approvals`. Context names the sources and the page's path on the protected `dev` deployment. Create `grill-board/page-approvals.md` with that anchor if absent, so Confirm works through the S-004 path.
4. **Index.** `grill-board/pages/index.json` holds, per listed path, the title, landed commit, hash and current card name.
5. **Stale.** When a page's hash changes, write the new card and append `## Stale` (`**Superseded by:** NAME`, `**Stale since:**` in UTC) to the previous card. Never edit or remove an existing section; answered history stays byte-for-byte. The board lists stale cards outside the queue and refuses to answer them.
6. **Idempotent.** A rerun with no change writes nothing and makes no commit. A change is one commit of cards, index and approvals record through the board's lock and compare-and-swap, subject `Grill Board: page cards for N pages`.

Out of scope: approval rows in Supabase and stale-confirm refusal hardening (TK-002); the voice record (TK-003); the coverage check (TK-000F); any `site/` change. If a page needs a `data-review-exclude` region (live data on `/rsi`), ask orchestrator A; do not edit `site/`.

Hand back to S-005 with `close`.

## Acceptance

- [ ] In a temporary Git repository with a fixture page list of two pages and injected HTML, `generate` writes exactly one card per page, each naming the hash the test vectors predict, plus the index and approvals record, in one commit.
- [ ] A second run with the same input writes nothing and makes no commit.
- [ ] Changing one character inside a fixture page's `<main>` writes a new card for the new hash and appends `## Stale` to the old one; changing only the footer SHA changes no hash.
- [ ] Must fail: a run that rewrites any existing section of an answered card, or a page with no card after a run, fails the test.
- [ ] The board lists a stale card outside the queue and refuses an answer to it, writing nothing.
- [ ] Live: against `origin/dev`, `generate` writes a card for `/` and `/rsi`, and `uv run ams-board` shows both under "Website pages".
- [ ] `uv run pytest` passes; render and doctor show no blocking finding.
