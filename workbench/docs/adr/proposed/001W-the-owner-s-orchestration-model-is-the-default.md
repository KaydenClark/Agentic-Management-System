---
date: 2026-11-01
canonicalized_in:
  - AGENTS.md
  - RUNBOOK.md
---

# The owner's orchestration model is the default

This build runs the owner's orchestration model. The orchestrator decides how many Dispatchers to run, and each Dispatcher decides how many implementors. Usually one Dispatcher holds one Spec. Parallel writers use their own worktrees, with one writer per shared file. A single-agent run of the same Spec is a later loop comparison, not the default.

Considered and rejected: one agent by default. Multi-agent scaling research found large losses on sequential tasks at many times the tokens, so the comparison stays on the loop's list.

Consequences: The loop later compares a single agent with this model on the same Spec.

Provenance: Owner decision review, 2026-11-01, with the owner's correction.
