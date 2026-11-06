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

## Verification and hand-back

The Proof field and Receipt hold the source verification and its remaining gaps. How the run went (the red/green collector tests, the held a555 candidate and its corrected guard, the frozen expected-row comparison, independent review and the implementor judgment) is kept verbatim in [S-006 history](../../../../../../wiki/history/S-006.md#task-birth-provenance-run-tk-000z-moved-from-the-task).

## Receipt

| Run | Branch | HEAD SHA | Upstream | Dirty | Tests | Docs touched | Remaining gap | Checksum |
|---|---|---|---|---|---|---|---|---|
| 1 | feature/s006-task-birth-provenance | db9f23a5e2ca10488edd71df91e4c43bcc907bab | ahead 0 behind 0 | 0 | Source3a25cac: local/fresh764 passed,4 skipped; independent215 history and49 affected; strict1232-to1234 full replay,61 source classifications; exact3S008+8archives/R; Task metadata applying-fake undo/CAS/current readback; real GET exact200-one/mismatch200-zero; source CI41435710340 pass | build_history module contract; S006 Spec/TK000Z; history regression tests; scoped independent source review and frozen comparison | Final owner-record CI and checked PR104 merge; real history import requires explicit approval and has not run; current canonical DB repair/readback and global live readcheck unrun; stopped W, whole-S006 binding and actual owner HumanQA remain open; close attribution: {"agent":"codex-task-provenance","claimant":"codex-task-provenance","onBehalfOf":null} | 952983c237f6185838d20f26253d9eb24620ae09322dac1d2f67605f91ef74bc |

## Later expressly approved live batch

The source-run Receipt above is unchanged. The owner subsequently approved exactly main771/devfe. The [actual pinned import proof](approved-history-import-771bd1e.md) records 131 inserts, 41 conditional Task refreshes, direct-current 74 Task projections and pinned global zero-gap readback, with all original rows/facts and audit preserved. Later c67/proof history remains unimported; this supplies no whole-S006 acceptance, owner QA or W closure.
