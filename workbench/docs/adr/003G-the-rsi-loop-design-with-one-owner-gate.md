---
date: 2026-11-01
canonicalized_in:
  - evals
  - supabase
supersedes:
  - 002F-the-rsi-loop-design.md
---

# The RSI loop design with one owner gate

The RSI loop uses fixed tasks, code graders, a ledger, adaptive and regression sets, and held-out release numbers. The model is held fixed within a comparison, and the exact model ID is pinned. One owner gate remains: the campaign approval (ADR-003F); merges follow DDR-000H. There is no automated proposer yet. The safeguards in the related CDRs apply to every round.

Considered and rejected: an automated proposer before the grader is trusted, which risks proxy-only wins and gamed evaluators.

Consequences: The first real ledger row is the loop's first milestone.

Provenance: Owner decision review, 2026-11-01 (ADR-002F). Modeled on the agentic-evolution paper that improved a fixed-model procedure. Owner correction, 2026-11-01: `workbench/wiki/context-owner-answers-coherence.md` (JOT-eadaca6e-98eb-4872-bfbc-fdaf9c3a4b06).
