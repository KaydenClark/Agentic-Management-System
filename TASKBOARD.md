# Agentic Management System - Hot Taskboard

> Generated from LLM Workbench v3.2.2.

**Current focus:** Port the pre-repo S-001/S-003 Specs, decisions and landmarks into this room; first product loop: the website explaining and demonstrating AMS.
**Owner:** Kayden (executive owner); execution owner per assigned Spec
**Last updated:** 2026-11-01

Read this continuation view to locate relevant work, then follow its linked
Spec/Task owners for current scope, claimant, blockers, evidence and next action.
A stale or missing row grants no authority; use current owners and the manifest.
For work outside an assigned Spec, follow RUNBOOK and the relevant Wiki context.

Before handoff or exit, update those owners and knowledge, then run
`node workbench/tools/spec-workbench.mjs render` to refresh this projection.
Keep one writer per owner and serialize shared board regeneration. Never edit
generated rows as an independent queue. An empty board means no projected work.

## Active Specs

<!-- hot-specs:start -->
| Spec | Current slice | Owner | Blocker | Latest meaningful event | Next gate |
|---|---|---|---|---|---|
| [S-001](workbench/specs/S-001-ams/SPEC.md) | TK-002: Add a public hygiene and character-limit check over records, controls and the built site (ready) | Kayden | none | TK-001 closed with proof. | Complete TK-002. |
| [S-002](workbench/landmarks/LMK-004-rsi-loop-during-build/specs/S-002-rsi-loop/SPEC.md) | TK-002: A noise-floor run of the current version against itself on a fixed task set records per-task flip rate and spread (in-progress; runs 1, feature/s002-qualification-results @ 84756ac, dirty 4); TK-001B: Actual interrupted or context-invalid executions retain their available private evidence without becoming grades (in-progress; runs 1, feature/s002-structured-judge @ 179f8a1, dirty 0); TK-001C: One adapter lifetime boundary preserves body and cleanup evidence without swallowing cancellation (in-progress) | Kayden; orchestrator B (local) | none | TK-001C claimed by s002-lifecycle. | Close TK-001C with verification and documentation proof. |
| [S-003](workbench/landmarks/LMK-003-ams-website/specs/S-003-showcase-site/SPEC.md) | TK-003: Why, Limits, Glossary, quickstart and About pages complete the tour, and the quickstart replays on a fresh clone (ready) | Kayden; orchestrator A (Website, cloud) | TK-002 | Destination clarified. | Reconcile assignments. |
| [S-004](workbench/landmarks/LMK-001-grill-board/specs/S-004-grill-board-cards/SPEC.md) | Acceptance / owner gate | Kayden; orchestrator B (local) | none | Review #2 passed at 4d49bfc (Orchestrator C). | Owner approval and Human QA, then complete; this supplies no Spec activation slot. |
| [S-006](workbench/landmarks/LMK-002-rsi-presentation/specs/S-006-rsi-data-store/SPEC.md) | TK-000W: Historical source declarations exclude multiline inline code (in-progress; runs 1, feature/s006-wiki-history-source @ 5e02ead, dirty 2) | Kayden; orchestrator B (local, holds the Supabase keys) | none | TK-000Z closed with proof. | Complete TK-000W. |
| [S-007](workbench/landmarks/LMK-002-rsi-presentation/specs/S-007-rsi-charts/SPEC.md) | TK-002: Rows from Supabase render per task and version, each number linked to its rows with its strength label and test rows hidden (blocked) | Kayden; orchestrator A (Website, cloud) | TK-001, S-006 | TK-001 closed with proof. | Complete TK-002. |
| [S-013](workbench/landmarks/LMK-004-rsi-loop-during-build/specs/S-013-coherence-checks/SPEC.md) | TK-003: A skills report lists RSI rows with no skills commit or one behind the current skills `main` (blocked) | Kayden; orchestrator C (Coherence, cloud, no secrets) | S-006 | TK-004 closed with proof. | Complete TK-003. |
| [S-008](workbench/landmarks/LMK-003-ams-website/specs/S-008-skills-wiki/SPEC.md) | Acceptance / owner gate | Kayden; orchestrator A (Website, cloud) | none | TK-001 and TK-002 closed: `/skills` and 39 articles at skills commit `8782412` merged into `dev` at `19c06cc` (PR #93), 2026-11-01. | Owner page approvals and Human QA of the 40 draft-marked pages on protected `dev`; only the owner merges `dev` -> `main`; then `complete`. |
<!-- hot-specs:end -->

Completed specs disappear from this projection. Their requirements,
decisions, acceptance, proof, completion, and supersession remain in retained
Specs, listed on demand with `node workbench/tools/spec-workbench.mjs list --all`.
The board projects Task records and never approves or completes them.

## Owner Decisions

Only decisions blocking an active spec appear here. Put options,
recommendation, cost/impact, owner, and next gate in one concise row; move the
resolved result into the owning spec.

| Spec | Decision | Options | Recommendation | Cost / impact | Owner | Next gate |
|---|---|---|---|---|---|---|
