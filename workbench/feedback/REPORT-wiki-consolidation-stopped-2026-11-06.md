# Wiki consolidation: stopped candidate and bounded restart

## State and evidence boundary

Stopped HEAD: `03c17ab90b78fd7d5e1c0dd13777cb6cdc49276e`; code/receipt candidate: `f1621c89020ae2b1bef37f3dcc294cd15e2e8762`; review base: `36cf26eafa9da2dba4ae1f0b56959af31c14ad11`. [S-000D](../landmarks/LMK-000A-wiki-memory/specs/S-000D-memory-retrieval/SPEC.md) retains all five accepted improvements under the independent Wiki memory Landmark.

TK-002U is now natively done locally at36cf26e, with sourcef924010,26focused passes and6real sources unchanged. [Its earlier stopped report](REPORT-wiki-memory-stopped-2026-11-05.md), failures, authorization and receipts remain preserved. The owner's exact prior answer, “Authorize bounded continuation,” is [JOT-4a2097ca](../wiki/context-wiki-maintenance.md#jot-4a2097ca-5bd6-456f-83c9-3bdbe7a79a29). That released the prior bounded run; it did not waive later Runbook stops or authorize public export.

[TK-002V](../landmarks/LMK-000A-wiki-memory/specs/S-000D-memory-retrieval/tasks/TK-002V/TASK.md) remains open with Receipt1 intact. Explicit-owner planning/apply/native correction reached green;15earlier consolidation cases passed before later additions, and unresolved-evidence append had a targeted pass. FAIL-127's explicit-owner loading failure was repaired. FAIL-128 was the second unexpected verification failure; the worker stopped immediately. No final aggregate/core26 rerun, native checks, operating-doc adoption or acceptance followed. TK-002W must remain blocked on its actual consolidation artifact, not released by this receipt.

Root used diagnosing-bugs read-only against the recorded owner-omitted fixture: the synthesis scores violet/orchard/purpose3 while the topic scores violet/orchard2 because Purpose is a section heading excluded from scoring; selection then fails incoming-link sufficiency. This is a source/recorded-input diagnosis, not a newly executed test result.

## Supplemental static review

Source: direct root-thread handbacks, captured2026-11-06. Fresh independent contexts `consolidation_standards` and `wiki_spec_review`, both High / OpenAI gpt-6.1-sol / Codex, inspected the pinned candidate/base above. No reviewer edits, tests, public actions, native verdict or Human QA occurred. These are findings on an incomplete candidate, not assembled Spec PASS. Defect actor: High / OpenAI gpt-6.1-sol / Codex implementor `codex-wiki-consolidation`.

**FAIL-129 — Selected source identity can change before the final check notices.** Both reviewers: [memory_consolidation.py](../../src/ams/memory_consolidation.py), lines175–182, protects an anchored source sharing a target page only by requiring its old text as a substring of proposed text. Appending within the source heading subtree or inserting an earlier duplicate heading retains that substring while changing the selected source/digest. Apply writes at290; source checks at287–289 and305–307 may detect the preventable mutation only after it occurs. Disposable native preflight also does not compare source fingerprints after capture; a native append can extend a final-heading source. Requirement: validate exact source selection identity/digests against both proposed prose and post-native state before any live write. Anchored source and target may legitimately share a page; do not impose a blanket ban. Static proof only; no current real-source mutation or exploit was observed.

**FAIL-130 — Corrected native source is parsed without its predecessor context.** Spec reviewer: [memory_consolidation.py](../../src/ams/memory_consolidation.py), lines110–112, passes the one selected native block from `_source_bytes` to `_entries`; [memory.py](../../src/ams/memory.py), lines180–192, requires all Supersedes predecessors. A valid corrected entry therefore fails invalid-jot when its predecessor is outside that block. Evaluate the selected source using the full owning-page correction context while matching the actual selected bytes. Historical confirmed intent must not become current authority merely because its old block says confirmed. The existing fixture used an uncorrected source; no new real case was executed. This is existing R3 lineage scope.

## Proposed corrective run: TK-002V only

Await the owner's new bounded restart answer. Preserve both failures and the unchanged stop rule. One serialized High-tier writer uses journey/TDD, one public behavior at a time: intentional red → minimal repair → green, then the next behavior.

1. Repair omitted-owner discovery using heading/navigation context and sufficient-owner eligibility before final selection; demonstrate both explicit and discovered existing owners without defaulting to new pages.
2. Repair FAIL-129 with exact proposed and post-native selected-source preflight before live writes. Include same-page anchored sources, heading extension/duplicate-heading selection and native append; refused plans must leave every live target/source unchanged.
3. Repair FAIL-130 with full correction-chain context and exact selected-source identity. Include corrected sources and superseded confirmed intent; preserve original sources, entries and exact readbacks.
4. Finish existing adversarial/schema/privacy/negative cases, appropriate consolidation aggregate plus core26 regressions, CLI QA, operating docs and preservation checks. Retain the incomplete workspace inventory/REBASE_HEAD limitation; no metadata cleanup or fabricated full closeout.
5. Commit a local handoff with actual results, source/receipt preservation and gaps. Root inspects it before closure or any TK-002W release. The restart question also concerns later W continuation, but this proposed implementor run stops at the V handoff; W retains its existing scope/dependency and independent evaluation requirements.

## Pending decisions

- **New bounded continuation:** the async question for TK-002V restart and subsequent TK-002W is unanswered. No source repair, tests, native closure or downstream implementation while STOP remains active. Prior continuation approval is not a waiver.
- **Public export/checked main delivery:** the separate question remains unanswered after FAIL-114/115. No push, alternate connector export, PR or merge. A local restart answer alone would not release publication.

This records-only continuation captures knowledge and a proposed restart. It changes no source, tests, evaluation artifacts, managed runtime, receipts or execution status; it proves no answer correctness, owner-effort benefit, acceptance or Human QA.
