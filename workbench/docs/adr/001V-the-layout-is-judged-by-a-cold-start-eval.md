---
date: 2026-11-01
canonicalized_in:
  - evals
---

# The layout is judged by a cold-start eval

The repository layout is judged by a fixed cold-start eval task with a planted correction, passed repeatedly with no owner help.

This is a hypothesis. The owner confirmed it as a working rule, and the RSI loop tests whether it holds. Confirmed if the task passes repeatedly (pass^k) with no owner help. Refuted if the agent revives a superseded meaning or needs the owner to re-explain.

Considered and rejected: judging layout by how it looks to a reviewer.

Consequences: Layout changes rerun the cold-start task.

Provenance: Owner decision review, 2026-11-01.
