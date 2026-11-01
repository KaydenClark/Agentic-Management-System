---
date: 2026-11-01
canonicalized_in:
  - RUNBOOK.md
  - evals
---

# Runbook commands are the commands graders call

The Runbook's run, inspect and measure commands are exactly the ones graders call. A declared command nothing runs is a defect.

This is a hypothesis. The owner confirmed it as a working rule, and the RSI loop tests whether it holds. Confirmed if trial transcripts show agents using them and graders depending on them. Refuted if they are never invoked.

Considered and rejected: a declared command surface that nothing executes.

Consequences: Graders call only Runbook commands.

Provenance: Owner decision review, 2026-11-01.
