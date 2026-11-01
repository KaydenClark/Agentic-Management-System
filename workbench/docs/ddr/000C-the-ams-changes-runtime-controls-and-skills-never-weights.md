---
date: 2026-11-01
supersedes:
canonicalized_in:
  - BLUEPRINT.md
  - evals
---

# The AMS changes runtime, controls and skills, never weights

The AMS changes only runtime, controls and skills, never model weights. Its premise, that this environment beats none, is tested against a no-AMS control and a generic-instructions control on held-out tasks.

This is a hypothesis. The owner confirmed it as a working rule, and the RSI loop tests whether it holds. Confirmed if the AMS beats both controls on held-out tasks, with a paired interval that excludes zero, at a stated cost per pass. Refuted if no difference is detected or the cost per pass is higher. Either way the site reports the result.

Considered and rejected: asserting the premise as settled. SWE-Skills-Bench v2 found no significant effect for most skills it tested.

Consequences: Every release run includes both control arms.

Provenance: Owner decision review, 2026-11-01.
