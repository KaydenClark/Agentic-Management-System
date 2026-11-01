---
date: 2026-11-01
canonicalized_in:
  - evals
  - supabase
---

# Every ledger row records cost and run state

Every ledger row records cost, tokens, turns, wall time and whether the run completed. Each trial is capped. Cost per pass is reported beside the pass rate, never alone.

Considered and rejected: grading runner or auth errors as task failures.

Consequences: Failed runs are rows with an execution state, not graded results.

Provenance: Owner decision review, 2026-11-01.
