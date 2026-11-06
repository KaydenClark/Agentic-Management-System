<!-- workbench-generated-page: TASKBOARD.md -->
# TASKBOARD (continued)

[First page](TASKBOARD.md) · [Previous page](TASKBOARD.page-001.md)

| Spec | Current slice | Owner | Blocker | Latest meaningful event | Next gate |
|---|---|---|---|---|---|
| [S-013](workbench/landmarks/LMK-004-rsi-loop-during-build/specs/S-013-coherence-checks/SPEC.md) | TK-003: A skills report lists RSI rows with no skills commit or one behind the current skills `main` (blocked) | Kayden; orchestrator C (Coherence, cloud, no secrets) | S-006 | TK-001D: Task closed (2026-11-06) | Complete TK-003. |
| [S-008](workbench/landmarks/LMK-003-ams-website/specs/S-008-skills-wiki/SPEC.md) | Acceptance / owner gate | Kayden; orchestrator A (Website, cloud) | none | TK-0033: Task closed (2026-11-06) | Independent review and dev containment of TK-0033; owner page approvals and Human QA on protected `dev`; only the owner merges `dev` -> `main`. Refocus fidelity remains unchecked. |
| [S-009](workbench/landmarks/LMK-003-ams-website/specs/S-009-demo-grill-board/SPEC.md) | TK-001: Demo page with labeled sample cards in the real card shape, deployed to `dev` (ready) | Kayden; orchestrator A (Website, cloud) | S-003 | TK-0030: Task closed (2026-11-06) | Reconcile legacy TK-001/TK-002 evidence and remaining Spec acceptance. |
| [S-010](workbench/landmarks/LMK-003-ams-website/specs/S-010-governance-flow-charts/SPEC.md) | TK-003A: Accept exactly two independently audited RSI authority revisions while rejecting unknown or meaning-changing source drift (blocked) | Kayden; orchestrator A (Website, cloud) | S-003 site shell content exists at checked dev commit `259b7a905639cc6ab621220b160fc813c5bc43f1`; whole-Spec completion remains separate. | review: Review verdict: pass at 501470c326d4cc8d0721b4fc600c553efdb2f5c3 [bb805778de9e] #1 (2026-11-06) | Inspect TK-003A source-transition plan before claim; final S-005 page cards and owner Human QA remain open. Only the owner promotes dev to main. |
