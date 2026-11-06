# TK-003 - Preserve private page feedback and commit its safe voice record version

**Task ID:** TK-003
**Spec ID:** S-005
**Slice:** Preserve original page feedback privately; bind safe committed voice entries and later page cards to its version.
**Status:** in-progress
**Blockers:** TK-001
**Destination:** spec-acceptance: Criticism becomes the voice record; Agents cite it
**Planned verification:** synthetic private-note canaries never enter Git; safe version/card writes are atomic, stale writes refuse, and originals remain recoverable

## Assignment

**Target branch:** `main`. Branch from `origin/main`, open a PR into `main` and merge it once current and checked, per `AGENTS.md`. Nothing in `site/` changes.
**Claimed by:** codex-s005-feedback
**Current claimant:** codex-s005-feedback

Start from a clean clone. Read `AGENTS.md`, this Task, the parent Spec (`../../SPEC.md`), `grill-board/README.md` (answers, rating and flag), DDR-000J, DDR-000X, ADR-002U, the TK-001 generator and `src/ams/grill_board/answers.py`.

Owner intent, relayed 2026-11-01: criticism becomes the voice and taste record that feeds the loop. The owner's voice is not prose the owner writes; it is the owner's recorded feedback. The parent Spec's later privacy contract governs: original criticism stays private, separate from interpretation; only safe voice/version/disposition records may enter public Git. The owner's expanded implementation approval of 2026-11-06 does not waive that privacy rule. Earlier verbatim-public instructions are superseded, with their correction retained in S-005 history.

Deliver:

1. **Private originals and safe record.** Preserve exact original notes in ignored private local storage, with page/hash/date/card/kind and a stable identity; never commit raw private words, private paths or raw evidence. `grill-board/voice-and-taste.md` retains a `**Version:**` counter and append-only `## Entries` containing safe page/hash/date/card/kind/version references and a safe interpretation/disposition, explicitly distinct from the original. Do not automatically quote or copy private originals into cards, approvals, the voice record, logs or public evidence. Keep unavailable interpretation visibly pending rather than inventing it. Synthetic test originals remain labeled synthetic.
2. **One checked operation.** A page return, rating or flag preserves its original privately and commits only the safe card section, voice entry and version increment through Board lock/CAS. Check the voice record's render-time SHA like the owning record. Missing private capture or stale/conflicting public bytes refuse without a partial Git write; preserve copyable owner words and recover any private pending outcome without duplicating an event. Confirm adds no voice entry; a Confirm note must also remain private. Non-page cards retain their existing behavior. Keep the current page-note refusal guard until this complete private path is verified; never remove it merely to make a feedback test pass.
3. **Version stamp.** The generator writes `**Voice record:** grill-board/voice-and-taste.md version N` on each new page card; an open page card made before this Task gets an appended `## Voice record` section. Existing sections are never edited.

Tell orchestrator A the record's path, so A adds the pointer from the site's contributing notes on `dev` and cites the version when drafting. Do not edit `site/`.

Out of scope: comparing ratings across pages (S-002 loop); applying criticism to a page (orchestrator A, in a new candidate); approval rows (TK-002); publishing private originals. TK-001E consumes the applicable version/original under its own authorization; a stored version alone proves no later use.

Hand back to S-005 with `close`.

## Acceptance

- [ ] In a disposable fixture, a return, rating/comment and flag preserve the exact synthetic original privately and atomically commit only safe card/voice references with page/hash/date/kind/version, incrementing the version.
- [ ] Must fail: a unique synthetic private-note canary in any Git blob, card, approval, voice record, public log or exported evidence. Original and safe interpretation remain separate and traceable; originals survive interruption/retry without duplicate effects.
- [ ] Must fail: criticism on a page card whose commit leaves the voice record unchanged fails the test.
- [ ] Editing the voice record after render makes the write refuse; card and record stay byte-identical.
- [ ] Must fail: an open page card that names no voice record version fails the test.
- [ ] `uv run pytest` passes; render and doctor show no blocking finding.

TK-002 is natively closed at published6d06b13 with exact-head CI success. This Task now implements private capture, safe version/card commits and durable event replay in the existing baselined continuation. Synthetic boundary/interruption checks pass36 cases; the actual browser retry passes after correcting its form-encoding expectation. Full/fresh checks and independent Review remain before delivery or close; no actual owner notes were submitted.

Workspace baseline sha256:77b8702e5c168d8ea307b5c62fcffeb0f5ab555e304d05be9de27cbba50ffcb9

## Receipt

| Run | Branch | HEAD SHA | Upstream | Dirty | Tests | Docs touched | Remaining gap | Checksum |
|---|---|---|---|---|---|---|---|---|
| 1 | Feature/S-005-page-review-cards | 6d06b13a501d6e558d9cd047382ce9c4fada39ac | ahead 0 behind 0 | 13 | Uncommitted TK003:36 focused pass; actual browser retry1 pass. Earlier142pass/1fail stale refusal and28pass/1fail invalid fixture verdict retained; browser encoding miss retained. Seven interruption cuts pass; raw canaries absent in all Git objects. | Board private-feedback guide; source dependency report; central FAIL237-244. | Full/fresh checks, independent Review, publication/CI and native close remain. No owner notes, final assembled capture, consumption or HumanQA; main merge remains unapproved. | 238bb69a990386fb09e2c7b96d04396cc3a2759d970611a82c733d54c000581a |
