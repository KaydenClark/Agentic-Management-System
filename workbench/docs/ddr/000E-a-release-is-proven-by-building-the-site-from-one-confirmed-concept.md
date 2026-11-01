---
date: 2026-11-01
supersedes:
canonicalized_in:
  - BLUEPRINT.md
  - evals
---

# A release is proven by building the site from one confirmed concept

An AMS release is proven when, from one confirmed site concept, the AMS builds the site to its Spec acceptance with no re-alignment after confirmation, and the owner's only act is Approve.

This is a hypothesis. The owner confirmed it as a working rule, and the RSI loop tests whether it holds. Confirmed if k of n recorded runs reach Approve with no re-alignment, with owner interventions and blockers logged in the ledger. Refuted if runs repeatedly need re-alignment or owner rescue.

Considered and rejected: proving releases through a template repository or a scripted demo project.

Consequences: Release runs log interventions and blockers as ledger rows.

Provenance: Owner decision review, 2026-11-01.
