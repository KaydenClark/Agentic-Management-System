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
| [S-001](workbench/specs/S-001-ams/SPEC.md) | TK-001: Run the "Are we there yet?" check at a named commit and record the answer in this Spec's log (ready) | Kayden | none | Owner set the cap to six active Landmarks; S-001 activated without waiting for another Spec to close. | Run TK-001 now; unfinished assessed capabilities are findings, not a start gate. |
| [S-002](workbench/landmarks/LMK-004-rsi-loop-during-build/specs/S-002-rsi-loop/SPEC.md) | TK-001: First-trial rows are seeded from real sources only, this build's history and the skills repository's before/after notes, each labeled at the strength it supports (blocked) | Kayden; orchestrator B (local) | S-006 | TK-000V closed with proof. | Complete TK-001. |
| [S-003](workbench/landmarks/LMK-003-ams-website/specs/S-003-showcase-site/SPEC.md) | TK-003: Why, Limits, Glossary, quickstart and About pages complete the tour, and the quickstart replays on a fresh clone (ready) | Kayden; orchestrator A (Website, cloud) | TK-002 | Destination clarified. | Reconcile assignments. |
| [S-004](workbench/landmarks/LMK-001-grill-board/specs/S-004-grill-board-cards/SPEC.md) | Acceptance / owner gate | Kayden; orchestrator B (local) | none | Review #2 passed at 4d49bfc (Orchestrator C). | Owner approval and Human QA, then complete; this supplies no Spec activation slot. |
| [S-006](workbench/landmarks/LMK-002-rsi-presentation/specs/S-006-rsi-data-store/SPEC.md) | Acceptance / owner gate | Kayden; orchestrator B (local, holds the Supabase keys) | none | TK-000S closed with proof. | Checked exact-identity PR delivery and actual native owner QA; independent Review PASS at e5a8c33. |
| [S-007](workbench/landmarks/LMK-002-rsi-presentation/specs/S-007-rsi-charts/SPEC.md) | TK-002: Rows from Supabase render per task and version, each number linked to its rows with its strength label and test rows hidden (blocked) | Kayden; orchestrator A (Website, cloud) | TK-001, S-006 | TK-001 closed with proof. | Complete TK-002. |
| [S-013](workbench/landmarks/LMK-004-rsi-loop-during-build/specs/S-013-coherence-checks/SPEC.md) | TK-004: A Spec review names its exact commit and comes from a context that did not build the Spec (ready) | Kayden; orchestrator C (Coherence, cloud, no secrets) | TK-002 | TK-002 closed with proof. | Complete TK-003. |
| [S-008](workbench/landmarks/LMK-003-ams-website/specs/S-008-skills-wiki/SPEC.md) | TK-001: `/skills` index and one complete article from the pinned commit, deployed to `dev` (in-progress) | Kayden; orchestrator A (Website, cloud) | none | TK-001 claimed by Orchestrator (Claude Opus 5.5). | Close TK-001 with verification and documentation proof. |
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
