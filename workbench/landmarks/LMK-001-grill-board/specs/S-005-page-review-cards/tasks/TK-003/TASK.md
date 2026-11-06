# TK-003 - Preserve private page feedback and commit its safe voice record version

**Task ID:** TK-003
**Spec ID:** S-005
**Slice:** Preserve original page feedback privately; bind safe committed voice entries and later page cards to its version.
**Status:** in-progress
**Blockers:** TK-001
**Destination:** spec-acceptance: Criticism becomes the voice record; Agents cite it
**Planned verification:** synthetic private-note canaries never enter Git; safe version/card writes are atomic, stale writes refuse, and originals remain recoverable

## Assignment

**Claimed by:** codex-s005-feedback
**Current claimant:** codex-s005-feedback
Target `main` on the existing Spec branch; no `site/` edits. Read AGENTS, the parent Spec, Board guide, DDR-000J/000X and ADR-002U. The confirmed launch and Nov6 expanded approval carry this scope forward. The parent privacy contract supersedes earlier public-verbatim instructions, retained in S-005 history.

Deliver:

1. Preserve exact originals in secure ignored local storage with stable event ID and page/hash/date/card/kind. Never commit original words, actual private locations or raw evidence. The safe voice record has a Version counter and append-only Entries with page/hash/date/card/kind/version, separate interpretation and disposition. Leave unknown interpretation pending; label synthetic originals synthetic.
2. Under Board lock/CAS, return/rate/flag privately captures before committing only safe card/voice/version writes. Check render-time voice SHA. Stale/conflicting public bytes or missing private capture refuse without partial Git writes. Keep copyable words and the exact retry identity. Reconcile crashes/retries without duplicate events, commits or versions; retain unrelated work. Refuse unsafe receipt types promptly and release the lock, including substitution races. Confirm adds no voice entry and its note stays private; non-page behavior stays. Retain the page-note guard until this complete path qualifies.
3. New cards name the applicable voice path/version. Append one Voice record section to legacy open cards; never edit existing sections or answered history.

Hand off the safe record path/version to orchestrator A for its contributing pointer and drafts; A owns site changes. S-002 owns rating comparisons. TK-001E owns later consumption and applying criticism; storage alone proves none. Hand back through native close after actual verification.

## Acceptance

- [ ] In a disposable fixture, a return, rating/comment and flag preserve the exact synthetic original privately and atomically commit only safe card/voice references with page/hash/date/kind/version, incrementing the version.
- [ ] Must fail: a unique synthetic private-note canary in any Git blob, card, approval, voice record, public log or exported evidence. Original and safe interpretation remain separate and traceable; originals survive interruption/retry without duplicate effects.
- [ ] Must fail: criticism on a page card whose commit leaves the voice record unchanged fails the test.
- [ ] Editing the voice record after render makes the write refuse; card and record stay byte-identical.
- [ ] Must fail: an open page card that names no voice record version fails the test.
- [ ] `uv run pytest` passes; render and doctor show no blocking finding.

Local65 close is historical after FAIL258/260. Native Review continues this Task/original claimant. Both bounded FIFO controls first timed out, then corrected130 focused HTTP/browser/page cases pass. Fresh checks, corrective Review/current CI remain. Prior receipts and originals stay; no actual owner notes, final QA or main delivery.

Workspace baseline sha256:77b8702e5c168d8ea307b5c62fcffeb0f5ab555e304d05be9de27cbba50ffcb9

## Receipt

| Run | Branch | HEAD SHA | Upstream | Dirty | Tests | Docs touched | Remaining gap | Checksum |
|---|---|---|---|---|---|---|---|---|
| 1 | Feature/S-005-page-review-cards | 6d06b13a501d6e558d9cd047382ce9c4fada39ac | ahead 0 behind 0 | 13 | Uncommitted TK003:36 focused pass; actual browser retry1 pass. Earlier142pass/1fail stale refusal and28pass/1fail invalid fixture verdict retained; browser encoding miss retained. Seven interruption cuts pass; raw canaries absent in all Git objects. | Board private-feedback guide; source dependency report; central FAIL237-244. | Full/fresh checks, independent Review, publication/CI and native close remain. No owner notes, final assembled capture, consumption or HumanQA; main merge remains unapproved. | 238bb69a990386fb09e2c7b96d04396cc3a2759d970611a82c733d54c000581a |
| 2 | Feature/S-005-page-review-cards | d2c9d211a44bb4e6b98b9fdc6eac05733a13f5c6 | ahead 5 behind 0 | 4 | Fresh642:1047pass/4skip,128focused incl actual browser/HTTP; independent corrective45x2,0 findings. Exact d2 CI1034pass/9skip plus10browser/all14steps succeeded. Added existing retry browser test to explicit CI list; new-head CI remains. | Private feedback guide/configuration; FAIL246/248 corrected. FAIL254-256 retains reviewer/publication harness limits. TK000K own expected-red work is outside this passed source. | New-head browser CI and native close. Coverage/consumption/final assembled dev capture/ownerQA/main permission remain; no actual owner notes or workspace release. | bcb5d3e466acba3dfd7578eabf3a06a91dd502ca835255f7d3cd8c27eca81bbc |
| 3 | Feature/S-005-page-review-cards | dc2cc96151cd2788750e8a1e556245b8b8cb755f | ahead 0 behind 0 | 0 | 642:1047/4skip;CI422486:1034/9+11browser;128focused;Reviews0. | Board guide/manifest/FAIL246+248. | Coverage/consumption/final dev/ownerQA/main permission; originals retained.; close attribution: {"agent":"codex-servitor-pr174","claimant":"codex-s005-feedback","onBehalfOf":"codex-s005-feedback"} | 138d451c7f8edbd55de1008f4466302da626f6b8e08c3adcf0c00199abafac9f |

## Continuation

| Run | Date | Answers | Adjusted handoff |
|---|---|---|---|
| 1 | 2026-11-06 | evidence row 25 (fail verdict at 65ab2cf13ea74985473c1b4f2708c61ee450eabf on 2026-11-06) | FAIL258 and260 OA-S005-20261106-FIFO-dc2cc96. Private FIFO read blocks before type validation and can retain the Board lock. Require bounded recoverable refusal and lock-release regression. Preserve prior receipts and local close as history. |
