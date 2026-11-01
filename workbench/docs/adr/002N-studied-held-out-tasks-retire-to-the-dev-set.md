---
date: 2026-11-01
canonicalized_in:
  - evals
---

# Studied held-out tasks retire to the dev set

After a release run, any held-out task whose failures are studied retires to the development set, and a fresh task replaces it.

Considered and rejected: reusing studied tasks as held-out, which leaks them into tuning.

Consequences: The held-out set is refreshed after each release run.

Provenance: Owner decision review, 2026-11-01.
