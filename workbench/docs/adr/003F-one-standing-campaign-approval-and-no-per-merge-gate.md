---
date: 2026-11-01
canonicalized_in:
  - evals
  - grill-board
supersedes:
  - 002O-one-standing-campaign-approval.md
---

# One standing campaign approval and no per-merge gate

The owner approves an RSI campaign once: budget, round cap and stop rule. He does not approve individual merges; agents merge non-site work into `main` themselves under DDR-000H, so every agent works from the current project. His only merge gate is the site's `dev` -> `main`.

Considered and rejected: a spend approval every round, which causes approval fatigue; an owner approval on every merge, which the owner refused ("Please Please Please do not make me approve every merge").

Consequences: The campaign approval is a Grill Board card with a committed answer. A ledger change rides its PR like any other change.

Provenance: Owner decision review, 2026-11-01 (ADR-002O). Owner correction, 2026-11-01: `workbench/wiki/context-owner-answers-coherence.md` (JOT-eadaca6e-98eb-4872-bfbc-fdaf9c3a4b06).
