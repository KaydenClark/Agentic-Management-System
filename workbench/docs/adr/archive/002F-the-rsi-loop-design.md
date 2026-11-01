---
date: 2026-11-01
canonicalized_in:
  - evals
  - supabase
superseded_by: 003G-the-rsi-loop-design-with-one-owner-gate.md
---

# The RSI loop design

The RSI loop uses fixed tasks, code graders, a ledger, adaptive and regression sets, and held-out release numbers. The model is held fixed within a comparison, and the exact model ID is pinned. Two owner gates remain: the campaign approval and the merge. There is no automated proposer yet. The safeguards in the related CDRs apply to every round.

Considered and rejected: an automated proposer before the grader is trusted, which risks proxy-only wins and gamed evaluators.

Consequences: The first real ledger row is the loop's first milestone.

Provenance: Owner decision review, 2026-11-01. Modeled on the agentic-evolution paper that improved a fixed-model procedure.
