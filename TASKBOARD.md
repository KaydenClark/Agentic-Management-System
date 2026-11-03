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
| [S-001](workbench/specs/S-001-ams/SPEC.md) | Acceptance / owner gate | Kayden | none | TK-003: Task closed (2026-11-02) | Confirm acceptance criteria and completion result. |
| [S-002](workbench/landmarks/LMK-004-rsi-loop-during-build/specs/S-002-rsi-loop/SPEC.md) | TK-002: A noise-floor run of the current version against itself on a fixed task set records per-task flip rate and spread (in-progress; runs 1, feature/s002-qualification-results @ 84756ac, dirty 4) | Kayden; orchestrator B (local) | none | TK-000V: Task closed (2026-11-01) | TK-000Y bounded structured-output correction; no further model calls or additional trial-store rows are released. |
| [S-003](workbench/landmarks/LMK-003-ams-website/specs/S-003-showcase-site/SPEC.md) | TK-001P: Visitors understand a coherent orientation without overlapping pages (in-progress); TK-001S: Visitors can comfortably read text across the website (in-progress; runs 1, codex/s003-website-completion @ 9f81ba1, dirty 3) | Kayden; orchestrator A (Website, cloud) | none | TK-002A: Readability corrective run delivered to dev (2026-11-02) | Close TK-001P with verification and documentation proof. |

[Next page](TASKBOARD.page-001.md)

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
