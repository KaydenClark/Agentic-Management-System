<!-- workbench-generated-page: TASKBOARD.md -->
# TASKBOARD (continued)

[First page](TASKBOARD.md) · [Previous page](TASKBOARD.md)

| Spec | Current slice | Owner | Blocker | Latest meaningful event | Next gate |
|---|---|---|---|---|---|
| [S-004](workbench/landmarks/LMK-001-grill-board/specs/S-004-grill-board-cards/SPEC.md) | Acceptance / owner gate | Kayden; orchestrator B (local) | none | Review #2 passed at 4d49bfc (Orchestrator C). | Owner approval and Human QA, then complete; this supplies no Spec activation slot. |
| [S-006](workbench/landmarks/LMK-002-rsi-presentation/specs/S-006-rsi-data-store/SPEC.md) | TK-000W: Historical source declarations exclude multiline inline code (in-progress; runs 1, feature/s006-wiki-history-source @ 5e02ead, dirty 2) | Kayden; orchestrator B (local keys) | none | Approved pinned import/readback passed. | Coverage/W disposition, whole Review, actual owner QA. |
| [S-007](workbench/landmarks/LMK-002-rsi-presentation/specs/S-007-rsi-charts/SPEC.md) | TK-002: Rows from Supabase render per task and version, each number linked to its rows with its strength label and test rows hidden (blocked) | Kayden; orchestrator A (Website, cloud) | TK-001, S-006 | TK-001 closed with proof. | Complete TK-002. |
| [S-013](workbench/landmarks/LMK-004-rsi-loop-during-build/specs/S-013-coherence-checks/SPEC.md) | TK-003: A skills report lists RSI rows with no skills commit or one behind the current skills `main` (blocked) | Kayden; orchestrator C (Coherence, cloud, no secrets) | S-006 | TK-004 closed with proof. | Complete TK-003. |
| [S-008](workbench/landmarks/LMK-003-ams-website/specs/S-008-skills-wiki/SPEC.md) | Acceptance / owner gate | Kayden; orchestrator A (Website, cloud) | none | TK-001 and TK-002 closed: `/skills` and 39 articles at skills commit `8782412` merged into `dev` at `19c06cc` (PR #93), 2026-11-01. | Owner page approvals and Human QA of the 40 draft-marked pages on protected `dev`; only the owner merges `dev` -> `main`; then `complete`. |
