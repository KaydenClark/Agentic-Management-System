# TK-002 - Confirming a page card records an owner-facing approval bound to its current hash in Git

**Task ID:** TK-002
**Spec ID:** S-005
**Slice:** Confirming a page card records an owner-facing approval bound to its current hash in Git
**Status:** in-progress
**Blockers:** TK-001
**Destination:** spec-acceptance: Approval bound to content
**Planned verification:** pytest with fixture cards, current hashes, stale approvals and append-only committed approval readback

## Assignment

**Target branch:** `main`. Branch from `origin/main`, open a PR into `main` and merge it once current and checked, per `AGENTS.md`. Nothing in `site/` changes.
**Claimed by:** codex-s005-approvals
**Current claimant:** codex-s005-approvals

Start from a clean clone. Read `AGENTS.md`, this Task, the parent Spec (`../../SPEC.md`, its approval-storage decision), `grill-board/README.md`, DDR-000O, DDR-000X, ADR-002U, ADR-003C, ADR-003H, the TK-001 generator and hash contract, `src/ams/writer.py` and `tests/test_writer.py`, and `supabase/migrations/`. Run Supabase commands only in orchestrator B's main checkout, where the service key lives; never print it.

Owner intent, relayed 2026-11-01: an approval is bound to the page content hash, and an edit after approval restores the draft mark.

Deliver:

1. **Confirm guard.** Under the board's lock, Confirm on a page card refuses, writing nothing, when the card is stale or its `Content hash` differs from the index entry for its page at the checked commit.
2. **Committed approval.** Confirm keeps the S-004 write: below `## Approvals` in `grill-board/page-approvals.md` it inserts the owner-answer line whose text names the path and `sha256:` hash. Add a parser that reads every approval line at a commit as (path, hash, date, card, commit).
3. **Committed readback.** `uv run ams-pages status` reads committed approval lines and the current index. It reports `approved` only for a matching path and current content hash, otherwise `draft`; these words are local Board/CLI state only. The public site reads neither this record nor a Supabase approval mirror.

The owner's 2026-11-05 correction confirms the presented committed-record-only recommendation. This supersedes the obsolete publicly readable Supabase approval-row path and withdrawn public draft mark; no migration or publishable-key approval query is implemented.

Out of scope: the voice record (TK-003); the coverage check (TK-000K); the site's draft mark (S-003 TK-004).

Hand back to S-005 with `close`.

## Acceptance

- [ ] In a temporary Git repository, confirming a fixture page card writes one approval line naming its path and hash, in one commit, with no second confirmation.
- [ ] Must fail: confirming a stale card, or a card whose hash differs from the index, writes nothing and leaves both files byte-identical.
- [ ] Approve a fixture page, change one character in its `<main>`, regenerate: `status` shows `draft`. Must fail: `approved` on changed content.
- [ ] Readback parses committed approval identity without overwriting prior entries; a changed current hash reports `draft` locally.
- [ ] No Supabase approval migration, publicly readable approval row, site approval query or public review status is introduced.
- [ ] `uv run pytest` passes; render and doctor show no blocking finding.

Preparation: published prerequisite TK-001 is done at800a67b. Exact PR174 main delivery is approval-blocked. This continuation remains local; it does not change that held PR head or claim delivery.

Workspace baseline sha256:64986c46643318243bc3bb1e5aba64064430cdfbe4b85768d01b02cd82a18e6f
