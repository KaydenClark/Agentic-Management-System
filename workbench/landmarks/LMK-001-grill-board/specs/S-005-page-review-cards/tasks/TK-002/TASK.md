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

## Receipt

| Run | Branch | HEAD SHA | Upstream | Dirty | Tests | Docs touched | Remaining gap | Checksum |
|---|---|---|---|---|---|---|---|---|
| 1 | Feature/S-005-page-review-cards | 3f021946ac96b18cb010f1d8730db2b0987901ae | ahead 4 behind 0 | 0 | Local continuation: expected index-drift red; guard green1; focused101 pass. Added compatibility cases:13 pass/1 failed, CRLF blob versus Git text newline normalization. Failure retained before correction. | Approval guard/readback and Board guide; original receipt chains unchanged. | Correct normalized line comparison, then focused/full checks and independent review. Local only; PR174 exact merge remains approval-blocked. No close or owner QA. | 8e6b6f77791886c62a1ea47f755466e1780578e058025e0d1fada720d6539d4d |
| 2 | Feature/S-005-page-review-cards | 3cb0da1313e449d8beab2657759342b7c84abe4e | ahead 5 behind 0 | 3 | 3cb0da1 full981 passed/6 skipped including Docker/SIGINT. Independent Spec review found CRLF conversion loses original approval commit; retained P2. Corrective working delta uses -w, four substantive-identity controls and shared recommendation formatter;107 focused pass. | Board guide, preserved failure receipt and original Task chains. | Corrective immutable source needs fresh full checks and renewed review. Local continuation only; held PR174 head800a unchanged, no publication/close/owner QA. | 7358b36809194212807963bd2978da0ff8d087fe58fce6c3e3a680259e3a0931 |
| 3 | Feature/S-005-page-review-cards | 6ad46e1922aa3990b8d92a45b612acfcd6f3c64c | ahead 10 behind 0 | 0 | Fresh b8e2236:984 passed/6 skipped/1 failed. test_poll_interruption_is_reraised_after_owned_cleanup raises EPERM from owned group send(0). Collector bytes equal800a; earlier full981/6 remains historical. Approval source reviews and107 focused pass; projection omission corrected11578ce. | Retained failed full log and independent findings; no original receipt overwritten. | Diagnose collector lifecycle before readiness; no permission waiver or merge retry. Task3 locally claimed/baselined but implementation paused. All continuation commits remain private. | 37a79b5b166630c511634508d2f61cf3072b472958fb87affc46e1c20c750a19 |
| 4 | Feature/S-005-page-review-cards | a5b4c57fcd313efad21894bce9583454b5b73e80 | ahead 11 behind 0 | 3 | Collector unchanged b8 diagnosis:90/100 pass,10 EPERM after successful TERM before leader reap. Deterministic race red retained. Corrected working runtime:100/100 original-fixture cases pass with sentinel safety; all17 collector tests pass including Docker/SIGINT and persistent-permission controls. | S005 group-observation report; original full failure and prior rows retained. | Fresh immutable full checks and renewed independent review remain. Private continuation only; no main merge retry, Task close or owner QA. Task3 implementation remains paused. | 27d6de3d2506dc978b8c24383858e4dfc4b8210bbfbc335e53a0f053b4420f71 |
| 5 | Feature/S-005-page-review-cards | 5ef89a66e619815a834119b45bccf0285679487f | ahead 12 behind 0 | 3 | 5ef fresh989/6skip;17 collector;100/100 original fixture. Runtime Review0; late central FAIL210-234 added, record review pending. | Failure log/report; original rows retained. | Exact CI/publication/native close and TK003 remain. No main retry or owner QA. | 1182474b6b4dde757ca6691979bae3af4e7d75e7ed74177bf6a885089952718e |
