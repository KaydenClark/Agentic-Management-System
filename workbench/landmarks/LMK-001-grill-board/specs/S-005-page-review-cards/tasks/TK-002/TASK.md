# TK-002 - Confirming a page card records an approval bound to its hash, committed in Git and written to Supabase for the site to read

**Task ID:** TK-002
**Spec ID:** S-005
**Slice:** Confirming a page card records an approval bound to its hash, committed in Git and written to Supabase for the site to read
**Status:** blocked
**Blockers:** TK-001
**Destination:** spec-acceptance: Approval bound to content
**Planned verification:** pytest with a fixture card and record; Supabase readcheck with the publishable key

## Assignment

**Target branch:** `main`. Branch from `origin/main`, open a PR into `main` and merge it once current and checked, per `AGENTS.md`. Nothing in `site/` changes.

Start from a clean clone. Read `AGENTS.md`, this Task, the parent Spec (`../../SPEC.md`, its approval-storage decision), `grill-board/README.md`, DDR-000O, DDR-000X, ADR-002U, ADR-003C, ADR-003H, the TK-001 generator and hash contract, `src/ams/writer.py` and `tests/test_writer.py`, and `supabase/migrations/`. Run Supabase commands only in orchestrator B's main checkout, where the service key lives; never print it.

Owner intent, relayed 2026-11-01: an approval is bound to the page content hash, and an edit after approval restores the draft mark.

Deliver:

1. **Confirm guard.** Under the board's lock, Confirm on a page card refuses, writing nothing, when the card is stale or its `Content hash` differs from the index entry for its page at the checked commit.
2. **Committed approval.** Confirm keeps the S-004 write: below `## Approvals` in `grill-board/page-approvals.md` it inserts the owner-answer line whose text names the path and `sha256:` hash. Add a parser that reads every approval line at a commit as (path, hash, date, card, commit).
3. **Supabase row.** A migration adds `page_approvals` (path, content_hash, approved_at, card, record_commit, source_url; primary key path and content_hash), readable by the publishable key and writable by no client role, matching the read-only baseline. `uv run ams-writer record-approvals` inserts each committed approval missing from the table; an identical row is a no-op and a differing one is refused (ADR-002U). `uv run ams-writer approvals-readcheck` reads with the publishable key and confirms every write is denied.
4. **Status.** `uv run ams-pages status` prints each listed page as `approved` only when a row names its path and its current index hash, else `draft`.

Coordinate with orchestrator A: S-003 TK-004 reads `page_approvals` with the publishable key and the TK-001 hash vectors, instead of the committed file its Task names. Do not edit S-003 or `site/`.

Out of scope: the voice record (TK-003); the coverage check (TK-000F); the site's draft mark (S-003 TK-004).

Hand back to S-005 with `close`.

## Acceptance

- [ ] In a temporary Git repository, confirming a fixture page card writes one approval line naming its path and hash, in one commit, with no second confirmation.
- [ ] Must fail: confirming a stale card, or a card whose hash differs from the index, writes nothing and leaves both files byte-identical.
- [ ] Approve a fixture page, change one character in its `<main>`, regenerate: `status` shows `draft`. Must fail: `approved` on changed content.
- [ ] `record-approvals` against a fake HTTP seam inserts once, is a no-op on rerun and refuses a differing row.
- [ ] Live: the migration is applied; `approvals-readcheck` reads the table with the publishable key and every write is denied.
- [ ] `uv run pytest` passes; render and doctor show no blocking finding.
