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
| [S-002](workbench/landmarks/LMK-004-rsi-loop-during-build/specs/S-002-rsi-loop/SPEC.md) | TK-001: First-trial rows are seeded from real sources only, this build's history and the skills repository's before/after notes, each labeled at the strength it supports (blocked) | Kayden; orchestrator B (local) | S-006 | Activated 2026-11-01 under the owner's six-active-Spec approval; four Tasks planned, seeding first. | S-006 rows for TK-001; the owner's standing campaign approval before TK-002. |
| [S-003](workbench/landmarks/LMK-003-ams-website/specs/S-003-showcase-site/SPEC.md) | TK-001: A reader opens the `dev` deployment and gets the shell: navigation, light/dark with toggle, the deployed SHA linked to GitHub, and a server-rendered home page (ready) | Kayden; orchestrator A (Website, cloud) | none | Activated 2026-11-01 under the owner's six-active-Spec approval; seven Tasks planned on `dev`, under-the-hood criterion restored. | Claim TK-001 in orchestrator A's lane. |
| [S-004](workbench/landmarks/LMK-001-grill-board/specs/S-004-grill-board-cards/SPEC.md) | TK-003: A 1-5 rating and a "too taxing" flag are one click each, saved as committed records, and a flagged card cannot be re-asked unchanged (ready) | Kayden; orchestrator B (local) | TK-001 | TK-002 closed with proof. | Complete TK-003. |
| [S-006](workbench/landmarks/LMK-002-rsi-presentation/specs/S-006-rsi-data-store/SPEC.md) | TK-004: Build-history rows are imported from this build's real Spec, Task, PR and commit records, returns and corrections included (in-progress) | Kayden; orchestrator B (local, holds the Supabase keys) | TK-002 | TK-004 claimed by claude-s006-tk004. | Close TK-004 with verification and documentation proof. |
| [S-007](workbench/landmarks/LMK-002-rsi-presentation/specs/S-007-rsi-charts/SPEC.md) | TK-001: The chart page is live on `dev` with every series place and the honest "no trials yet" state (ready) | Kayden; orchestrator A (Website, cloud) | none | Activated 2026-11-01 under the owner's six-active-Spec approval; three Tasks planned on `dev`. | Claim TK-001 in orchestrator A's lane. |
| [S-013](workbench/landmarks/LMK-004-rsi-loop-during-build/specs/S-013-coherence-checks/SPEC.md) | TK-004: A Spec review names its exact commit and comes from a context that did not build the Spec (ready) | Kayden; orchestrator C (Coherence, cloud, no secrets) | TK-002 | TK-002 closed with proof. | Complete TK-003. |
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
