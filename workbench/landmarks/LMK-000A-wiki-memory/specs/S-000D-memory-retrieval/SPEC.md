# S-000D - Source-backed memory recovery

**Spec ID:** S-000D
**Status:** active
**Priority:** 1
**Owner:** Kayden; codex-wiki-memory orchestrator
**Stance:** Builder
**Updated:** 2026-11-06
**Catalog description:** Recover, check and consolidate bounded Wiki understanding across sessions with traceable sources.
**Blockers:** none
**Confirmation:** [JOT-36034de3-6b3b-4b50-8538-c1a3f54ac123](../../../../wiki/context-wiki-maintenance.md#jot-36034de3-6b3b-4b50-8538-c1a3f54ac123)
**Execution approval:** [JOT-36034de3-6b3b-4b50-8538-c1a3f54ac123](../../../../wiki/context-wiki-maintenance.md#jot-36034de3-6b3b-4b50-8538-c1a3f54ac123)
**Next gate:** Owner bounded-restart answer for TK-002V; [scope and separate export hold](../../../../feedback/REPORT-wiki-consolidation-stopped-2026-11-06.md).

## Outcome and authority

Fresh agents recover understanding, exact owner corrections, reasons, constraints, questions and live-owner routes without starting from zero. [LMK-000A](../../LANDMARK.md) owns this critical memory capability. [Owner correction](../../../../wiki/context-wiki-maintenance.md#jot-b3247909-9721-4842-a83f-61adc5da2e13) excludes RSI classification. Approval covers all five improvements, Map/Plan and delegated implementation, not QA or acceptance.

## Current evidence and problem

At base `adde5f4da1d8a8b78d9bcbc6bd490c18f8a3b37a`, MEMORY routed prose and native Jot searched entries; retrieval, claim freshness, consolidation and evaluation gaps motivated this Spec. S-000C evidence/owner QA remain intact.

## Acceptance Criteria

- [ ] **R1 Retrieval:** Navigation-first bounded keyword retrieval covers maintained article sections, native Jots/correction context and source references. Each hit preserves page/title, heading/subject, kind/state, source identity and limits. Compare optional embeddings/reranking only against the keyword baseline when justified; no external service required. Prose-only recall must work; detached excerpts fail.
- [ ] **R2 Freshness:** Important claims bind to observed source revision or digest, observation date and superseding correction. A source edit reports affected explanations as possibly stale; missing/unavailable/unbound sources remain explicit. Changed bytes never prove falsity, refresh verification dates or authorize rewrite/confirmation. Retain historical bindings and distinguish restored bytes.
- [ ] **R3 Consolidation:** A supported operation finds the existing topic owner, separates additions/evidence/corrections/contradictions and identifies affected summaries/incoming links. An explicit revision-checked apply updates authorized explanation/routes and captures through native Jot where needed, retaining original source, historical entries and exact confirmation bytes. Repeated observations support only attributed, bounded lessons. Silent inference-to-confirmation, duplicate owners and stale writes fail.
- [ ] **R4 Context:** Short/standard/deep responses serve historical events/lifecycle, maintained understanding, procedures and live-owner pointers. Return explanation, constraints, unresolved questions and deeper evidence links, with stale/conflicting/unavailable claims visible. These are memory functions, never governance planes; live state is linked rather than copied. Procedure/history requests produce different focused context.
- [ ] **R5 Functional evaluation:** A small pinned real AMS set covers current understanding, historical recall, cross-page reasoning, corrections and unknown abstention. Record retrieval/source correctness, independently judged answer correctness, stale repetition, context size and actual owner correction effort or explicit unmeasured values. Compare the same cases at baseline/candidate; development and untouched held-out status is explicit. Introduce a labeled synthetic correction in an isolated public fixture and have a fresh agent recover the revised understanding without repeating the old claim. Retrieval scores alone cannot establish answer correctness or human effort.
- [ ] **R6 Preservation and delivery:** Privacy/path adversarial cases and immutable source/confirmation checks pass; all five requirements are mapped to Tasks, independently reviewed and delivered through the checked non-site route. Native green alone, implementor self-review or fabricated Human QA fails.

## Public contract and decisions

Use project Python `ams-memory query|check|consolidate|evaluate`, readable/JSON results, additive src/ams/tests/entrypoint/evals and scoped docs. Managed tools/shared skills stay unchanged; use journey/TDD at public seams.

Project CLI plus native Jot avoids managed-package coupling and hosted graph/vector sync. It accepts adapter maintenance/semantic review; ranking changes need local evidence.

Git Markdown claim bindings carry stable IDs, explanation anchors, source identities, observed revision/digest/date and supersession; a page may bind several claims/sources. Use a compact machine-readable block compatible with Wiki validation. Never infer claim plane from page type. Preserve exactly 6 Projection, 5 Intent, 4 Enduring Context, 3 Grounding, 2 Canon, 1 Actuality and both traversal directions. Memory functions are independent of these roles.

The [scoped read/apply contract](../../../../wiki/context-wiki-maintenance.md#planned-memory-interface) defines navigation, bounds, privacy, explicit source access and whole-plan revision checks. These are required invariants, not current implementation claims.

## Dependencies, scope and documentation

No external blocker or S-000C dependency. Use Python3.14, markdown-it-py/pytest and standard library. Reconcile procedure/topic/routes/synthesis and operating docs; native history owns evidence.

Exclude paid services, DB migrations, deployment, catalog changes/install, unrelated upgrades, autonomous confirmation and broad rewrites. Evidence gaps limit claims, not requirements; research inspiration proves no AMS result.

## Verification Procedure

Exercise CLI recall/corrections, change/restore, consolidation preflight/readback, bounds, unknowns and privacy/path failures. Compare pinned MEMORY/native-Jot baseline and candidate with identical questions/budgets/sources; missing CLI is no score. Judge actual answers and fresh-agent correction/session continuity. Fresh assembled checks: render/doctor/Wiki/layout/hygiene, pytest and independent Review. Retain prior findings and unperformed owner QA.

## Task coverage and ready frontier

1. [TK-002U](tasks/TK-002U/TASK.md), locally closed: recall/freshness/baseline, R1/R2/R5/R6.
2. [TK-002V](tasks/TK-002V/TASK.md), stopped open after TK-002U local closure: consolidation, R3/R2/R6.
3. [TK-002W](tasks/TK-002W/TASK.md), blocked by TK-002V correction/readback: context/full evaluation, R4/R5 and integrated R1-R6.

Serialize shared writers. Tasks include Check/QA/repair/hand-back; root owns independent probes/Review/delivery. Stopped implementation grants no success claim.

## Completion Result

TK-002U local reader/check/evaluation candidate:26 focused passes,4/4 pre-anchor development checks,4claims/6sources; [retained report](../../../../feedback/REPORT-wiki-memory-stopped-2026-11-05.md) preserves failures/limits. Root accepted the final anchor repair and authorized local closure; it verifies done artifacts before the next Task. TK-002V then stopped at FAIL-128; [static findings and bounded restart](../../../../feedback/REPORT-wiki-consolidation-stopped-2026-11-06.md) remain open, and TK-002W stays blocked. New restart/public-export answers are separately pending; no assembled Review, answer/effort benefit or owner acceptance.

## Supersession

- Supersedes: none
- Superseded by: none
