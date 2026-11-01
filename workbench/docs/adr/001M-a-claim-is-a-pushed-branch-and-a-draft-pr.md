---
date: 2026-11-01
canonicalized_in:
  - AGENTS.md
  - RUNBOOK.md
---

# A claim is a pushed branch and a draft PR

Claiming a Task means pushing its branch with the Task marked in progress and opening a draft pull request naming the Task and agent. GitHub Issues are not used for claims.

This is a hypothesis. The owner confirmed it as a working rule, and the RSI loop tests whether it holds. Confirmed if in parallel-agent runs, duplicate pickups fall below runs without claims, with no extra blocked runs. Refuted if duplicates do not occur without it, or claim pushes block work.

Considered and rejected: GitHub Issues as the required claim record. The owner set this aside: it adds a tool he does not use and makes GitHub availability a precondition for all work.

Consequences: Selection treats a Task as taken when an open PR or remote branch shows it in progress.

Provenance: Owner decision review, 2026-11-01. Owner answer, 2026-11-01 (round 2).
