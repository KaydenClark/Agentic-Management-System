# S-000D - Source-backed memory recovery

**Spec ID:** S-000D
**Status:** planned
**Priority:** 1
**Owner:** Kayden; codex-wiki-memory orchestrator
**Stance:** Builder
**Updated:** 2026-11-05
**Catalog description:** Recover, check and consolidate bounded Wiki understanding across sessions with traceable sources.
**Blockers:** none
**Confirmation:** [JOT-72534303-7521-4d2c-98d2-96b1bcb3825a](../../../../wiki/context-wiki-maintenance.md#jot-72534303-7521-4d2c-98d2-96b1bcb3825a)
**Execution approval:** [JOT-72534303-7521-4d2c-98d2-96b1bcb3825a](../../../../wiki/context-wiki-maintenance.md#jot-72534303-7521-4d2c-98d2-96b1bcb3825a)
**Next gate:** Prepare bounded Tasks, then activate and delegate implementation under existing approval.

## Outcome and authority

Fresh agents recover understanding, exact owner corrections, reasons, constraints, questions and live-owner pointers without starting from zero. [LMK-000A](../../LANDMARK.md) owns this critical AMS memory capability. The [owner correction](../../../../wiki/context-wiki-maintenance.md#jot-b3247909-9721-4842-a83f-61adc5da2e13) excludes RSI classification. Approval covers all five recommendations, Map, Plan and delegated implementation; confirmation, QA and acceptance remain distinct.

## Current evidence and problem

Base `adde5f4da1d8a8b78d9bcbc6bd490c18f8a3b37a`: MEMORY routes maintained prose; native Jot search covers entries only. Page freshness lacks claim/source binding; consolidation is manual; no memory CLI/evaluation runner exists. S-000C's repair and pending owner QA remain intact.

## Acceptance Criteria

- [ ] **R1 Retrieval:** Navigation-first bounded keyword retrieval covers maintained article sections, native Jots/correction context and source references. Each hit preserves page/title, heading/subject, kind/state, source identity and limits. Compare optional embeddings/reranking only against the keyword baseline when justified; no external service required. Prose-only recall must work; detached excerpts fail.
- [ ] **R2 Freshness:** Important claims bind to observed source revision or digest, observation date and superseding correction. A source edit reports affected explanations as possibly stale; missing/unavailable/unbound sources remain explicit. Changed bytes never prove falsity, refresh verification dates or authorize rewrite/confirmation. Retain historical bindings and distinguish restored bytes.
- [ ] **R3 Consolidation:** A supported operation finds the existing topic owner, separates additions/evidence/corrections/contradictions and identifies affected summaries/incoming links. An explicit revision-checked apply updates authorized explanation/routes and captures through native Jot where needed, retaining original source, historical entries and exact confirmation bytes. Repeated observations support only attributed, bounded lessons. Silent inference-to-confirmation, duplicate owners and stale writes fail.
- [ ] **R4 Context:** Short/standard/deep responses serve historical events/lifecycle, maintained understanding, procedures and live-owner pointers. Return explanation, constraints, unresolved questions and deeper evidence links, with stale/conflicting/unavailable claims visible. These are memory functions, never governance planes; live state is linked rather than copied. Procedure/history requests produce different focused context.
- [ ] **R5 Functional evaluation:** A small pinned real AMS set covers current understanding, historical recall, cross-page reasoning, corrections and unknown abstention. Record retrieval/source correctness, independently judged answer correctness, stale repetition, context size and actual owner correction effort or explicit unmeasured values. Compare the same cases at baseline/candidate; development and untouched held-out status is explicit. Introduce a labeled synthetic correction in an isolated public fixture and have a fresh agent recover the revised understanding without repeating the old claim. Retrieval scores alone cannot establish answer correctness or human effort.
- [ ] **R6 Preservation and delivery:** Privacy/path adversarial cases and immutable source/confirmation checks pass; all five requirements are mapped to Tasks, independently reviewed and delivered through the checked non-site route. Native green alone, implementor self-review or fabricated Human QA fails.

## Public contract and decisions

Use a project-owned Python CLI, `ams-memory`, with `query`, `check`, `consolidate` and `evaluate`; JSON and concise readable output share results. Additive `src/ams`, tests, pyproject entrypoint, eval fixtures and Wiki/procedure changes suffice. No edits to receipted workbench/tools or shared skills. Implementors use journey and TDD at public CLI seams.

Interface comparison: extending managed Jot couples AMS behavior to package adoption; hosted vector/graph services add synchronization and service burden. Choose the project-local CLI using existing owners/native Jot: reversible and testable, accepting adapter maintenance and explicit semantic review. Optional ranking changes need useful local evidence.

Git Markdown claim bindings carry stable IDs, explanation anchors, source identities, observed revision/digest/date and supersession; a page may bind several claims/sources. Use a compact machine-readable block compatible with Wiki validation. Never infer claim plane from page type. Preserve exactly 6 Projection, 5 Intent, 4 Enduring Context, 3 Grounding, 2 Canon, 1 Actuality and both traversal directions. Memory functions are independent of these roles.

The [scoped read/apply contract](../../../../wiki/context-wiki-maintenance.md#planned-memory-interface) defines navigation, bounds, privacy, explicit source access and whole-plan revision checks. These are required invariants, not current implementation claims.

## Dependencies, scope and documentation

No external blocker. Use existing Python 3.14, markdown-it-py and pytest; prefer standard library. Update maintenance procedure, topic, routes, synthesis and necessary architecture/run instructions. Native tools/history own lifecycle evidence; S-000C is no execution dependency.

Excluded: paid services, DB migrations, deployment, catalog changes/install, unrelated upgrades, autonomous confirmation and broad corpus rewrite. Missing evidence limits claims, never requirements. Research links in the topic inspire design; they prove no AMS result.

## Verification Procedure

Test public CLI recall, correction context, change/restore, whole-plan refusal, consolidation readback, bounds, unknowns and privacy/path failures. Baseline is pinned MEMORY navigation plus native Jot, with identical question/budget/source scope; missing CLI is no score. Compare actual baseline/candidate answers, then fresh-agent correction and session-continuity checks. Run render/doctor/Wiki/layout/hygiene, pytest and independent Review on a fresh assembled candidate. Separate pre-existing findings and unperformed owner QA.

## Completion Result

Pending; preparation records no working behavior, measured improvement or owner acceptance.

## Supersession

- Supersedes: none
- Superseded by: none
