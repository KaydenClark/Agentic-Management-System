# TK-000Z - Task creation facts survive migration and removal

**Task ID:** TK-000Z
**Spec ID:** S-006
**Slice:** Task creation facts survive migration and removal
**Status:** done
**Blockers:** none
**Destination:** spec-acceptance: Build history from real records
**Planned verification:** Full creation-row identity across table/native migration and removal; native-only/rename/pin/conflict tests; exact3 S008 plus8 archive facts; deterministic complete expected-row BEFORE/AFTER diff; independent pinned delta review; full/fresh/room/current CI and checked merge.
**Claimed by:** codex-task-provenance
**Current claimant:** codex-task-provenance
**Proof:** Source3a25cac: local/fresh764 passed,4 skipped; independent215 history and49 affected; strict1232-to1234 full replay,61 source classifications; exact3S008+8archives/R; Task metadata applying-fake undo/CAS/current readback; real GET exact200-one/mismatch200-zero; source CI41435710340 pass

## Assignment

The orchestrator assigned one fresh bounded correction under existing S-006 history-correctness authority after direct read-only diagnosis. Checked main771 readback has130 missing rows, one extra S008/TK003 and two changed S008 creation projections. All three stored originals match e0ca3a8 Spec lines56–58; ancestors of checked/current main/dev. Main native-file migration e8135ef and earlier removal16e3e7 changed the projection; dev still derives originals. This is a new event class, not another stopped W scanner attempt. Preserve W/X records, exact failed pins, receipts and the successful eight-fact CommonMark repair.

Sole writer codex-task-provenance uses retained managed worktree and fresh feature/s006-task-birth-provenance from checked main27c62fa. Only currently registered Specs and verified local ancestor/rename lineage may derive a Task birth. Creation fields come from the earliest provable graph source/blob, never mutable current slice text or DB rows; conflicting ambiguous births refuse. Native records retain current execution/receipt ownership. Removed creation facts remain historical without reactivation or restored source tables. Preserve no-replace/no-lazy-fetch/no-protocol/textconv guards. No unregistered path scan, handtyped S008 facts, S008 owner edits, broad refactor, schema changes, row deletion/ignore or model calls.

Produce a deterministic complete expected-row comparison on identical pinned source inputs, identifying every broader canonical-field correction for review. Focused/full/fresh/room/CI and independent exact delta review precede normal main merge. No live mutation is authorized now, including after permission arrives until correctness gates pass; do not refresh original provenance to fit a newer projection. Build-history/whole-S006 acceptance, stopped W lifecycle and owner HumanQA remain separate.

## Acceptance

- [x] Full immutable creation row identity survives legacy-to-native migration, changed current slices and intentional removal; current native receipts appear once without resurrecting removed assignments.
- [x] Native-only, rename, pinned and conflicting/invalid lineage cases are correct and fail closed; exact3 original S008 and8 archived facts derive once with original fields/sources.
- [x] Task-only canonical birth metadata refresh preserves annotations/audit, logs bounded undo, rejects full-detail concurrent changes and verifies direct current readback.
- [x] Complete deterministic BEFORE/AFTER expected-row diff is reviewed; focused/full/fresh/room/CI and independent pinned delta review pass before checked merge, while actual live/acceptance gates stay truthful.

## Provenance reconciliation boundary

Read-only graph inspection found two sibling native R definitions at `9a2813380cdeeaf3d1ff772f4d4d84c0f5b48add` and `ca447da043ad92ecfafc2ac370e7e717ff149fcc`. The first supplied native claim `5de39ea2ed605be304e5920ae281d00088d4c10b`; the historical failed-verdict scaffold supplied no pre-join claim or execution. Merge `5e17601863373b2f3e5608ef767bd1eea6c95510` preserves the claimed document and adds the existing explicit Native corrective provenance statement identifying both assignments as the same correction and naming the joined verdict source. R's unchanged native run1 receipt binds source `4220d1f0a01feca72d97aaa204add0d19989f6a1` and its original claimant; native receipt parsing validates its checksum.

The orchestrator inspected the primary proof and authorized a generic narrow reconciliation: unique native-claimed owner ancestry, no competing pre-join claim/execution, an explicit visible source resolution and unchanged claimed assignment/acceptance. Unsupported/ambiguous cases still refuse. Neither wall time, today's Slice, first-parent ordering alone nor a Task/commit allowlist selects the birth. Both original commits and failed verdict remain historical facts; closed R and its receipt are untouched. Literal code/comments cannot supply metadata or resolution authority.

## Check and implementor QA

Initial public collector tests observed seven causal failures and one positive pass; the first implementation made all eight pass. Native-owner/scaffold reconciliation was independently observed red before implementation, then all 24 focused birth cases passed. Source-only readback derived 206 Spec/Task records and 76 immutable births, reproducing the three original S008 rows from e0ca3a8 lines56–58 and all eight previously retained Wiki-routed facts exactly once. Later guard verification includes the original native record test and 29 birth cases, 30 passed. An intermediate local Git-error wrapper incorrectly made absent legacy receipt files fatal; the correction preserves optional receipt reads while required birth objects fail closed. The corresponding local failure evidence is retained; no source candidate containing that failure was published.

All history modules now pass: 195 tests in 80.05 seconds. Complete same-input expected-row comparison, full/fresh verification, independent immutable delta review and current CI are pending; doctor has no blockers and layout/diff checks pass. Actual live import remains held for both explicit permission and source correctness. This local engineering proof does not pass global readcheck, close W, confer whole-S006 acceptance or owner HumanQA.

### Corrected source boundary

Source `a5551032940ce2c4a727ff144276c7014eff8ecd` passed full and fresh checks (744 passed, four skipped) and source-only exact-three/eight verification. Independent scoped review then held that candidate: a ready/unclaimed scaffold with genuine nonempty Proof could still reconcile. The causal public-reader repro and the prior source proof remain retained. The same open run corrects that guard generically, including visible native fields in Task body paragraphs; code/comment examples supply no execution authority. The metadata seam was separately proved with an applying fake: metadata-only wrong status remained stale while the old writer/readcheck both returned success.

The approved Task-only correction compares the six birth-detail keys with presence, preserves unrelated stored metadata and prior audit, records bounded previous canonical metadata without recursive audit copies, and conditionally refreshes against the entire original stored detail plus core fields. Direct current Task response data must match, even though pinned readcheck deliberately accepts genuine historical states. A real anonymous GET protocol probe examined 68 existing Task rows: exact id/full-detail predicate returned HTTP200 and one matching row; a deliberate mismatch returned HTTP200 and no rows. Three GETs only, maximum encoded detail 832 bytes; no service key, dotenv or mutation. Complex escaping/type/race/undo cases use applying fakes.

The complete frozen comparison at a555 derives 1,220 versus 1,222 rows: two additions, no removals, and 59 Task-only changes. Every added/changed birth was verified against its exact original blob/line/time. Thirty-one restore original legacy declarations, O restores its original native Slice, K repairs an impossible old URL to its first matching-ID record, and 26 change only birth status metadata. F and K are first records of different Spec/Task identities; b7d explicitly renumbers the same coverage assignment. This does not claim two independent work executions, reactivate F, invent a Former ID field or add an alias allowlist. Strict offline replay uses 106 frozen public GitHub responses, 3,217 successful Git responses, 14 lifecycle responses and 13 genuine failed local-object reads; repeated complete rows are identical.

The branch integrates checked main c96a991. Corrected history tests passed 213; the subsequent native-body Proof audit passes 49 focused birth/metadata cases. Fresh corrected full-suite verification, final frozen-input comparison and independent new source review follow the immutable corrected pin. Live history mutation remains unapproved and held; prior missing/global-readcheck receipts, W's stopped state and actual owner QA remain open.

### Implementor QA and source submission

Corrected immutable source `3a25cacf797743ca8189739a46661ec4e3a76a09` is pushed in PR #104. Full local/fresh checks pass 764 tests with four skips; the fresh clone is clean and room checks have no blockers. Exact-source CI run41435710340 passes. Source/test/dependency/schema bytes are frozen after this pin. The native-body audit adds two cases beyond the preceding 213-history run; the corrected independent history run passes all 215, with 49 affected cases.

Actual eligible noncontributor `s002_bootstrap_review` supplied direct bounded engineering source-readiness PASS at that exact source, no blocking findings. The reviewer independently reran 215/49 tests, the original Proof refusal, real-source 208 records/76 births with exact three S008/eight archive facts and R ownership, and strict copied-map replay/classification. Final sealed corrected comparison is 1,232→1,234 rows, two additions/no removals/59 Task-only changes (33 core fields plus 26 status-only metadata); all 61 added/changed source rows are verified. Its 107 public GitHub, 3,264 Git and 14 lifecycle successful responses plus 13 genuine Git failures replay identically twice without fallback. The reviewer directly read both 764/4 logs and checked the fresh source clone. This supersedes only the scoped a555 finding/hold; earlier failures remain evidence.

Judgment: the bounded source outcome is met. Migration/removal and mutable current fields cannot rewrite identity births; unsupported competing execution refuses; current native receipts remain separate; applying fake refreshes preserve unknown/audit data, bounded undo, exact key presence and race refusal. Direct current representations are checked, not merely historical readcheck matches. Real anonymous GET verifies object-filter syntax only. No real import or current canonical database repair/readback ran. Normal final owner-record CI/checked merge follow; actual history-import approval, global live verification, stopped W and formal owner HumanQA remain open. This is no evaluator qualification, trial benefit or whole-S006 acceptance.

## Receipt

| Run | Branch | HEAD SHA | Upstream | Dirty | Tests | Docs touched | Remaining gap | Checksum |
|---|---|---|---|---|---|---|---|---|
| 1 | feature/s006-task-birth-provenance | db9f23a5e2ca10488edd71df91e4c43bcc907bab | ahead 0 behind 0 | 0 | Source3a25cac: local/fresh764 passed,4 skipped; independent215 history and49 affected; strict1232-to1234 full replay,61 source classifications; exact3S008+8archives/R; Task metadata applying-fake undo/CAS/current readback; real GET exact200-one/mismatch200-zero; source CI41435710340 pass | build_history module contract; S006 Spec/TK000Z; history regression tests; scoped independent source review and frozen comparison | Final owner-record CI and checked PR104 merge; real history import requires explicit approval and has not run; current canonical DB repair/readback and global live readcheck unrun; stopped W, whole-S006 binding and actual owner HumanQA remain open; close attribution: {"agent":"codex-task-provenance","claimant":"codex-task-provenance","onBehalfOf":null} | 952983c237f6185838d20f26253d9eb24620ae09322dac1d2f67605f91ef74bc |

## Later expressly approved live batch

The source-run Receipt above is unchanged. The owner subsequently approved exactly main771/devfe. The [actual pinned import proof](approved-history-import-771bd1e.md) records 131 inserts, 41 conditional Task refreshes, direct-current 74 Task projections and pinned global zero-gap readback, with all original rows/facts and audit preserved. Later c67/proof history remains unimported; this supplies no whole-S006 acceptance, owner QA or W closure.
