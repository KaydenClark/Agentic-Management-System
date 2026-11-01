---
date: 2026-11-01
canonicalized_in:
  - AGENTS.md
---

# Three strikes, then stop

An event is tried at most three times: the run, a failed test, a second failed test. Then the agent stops and reports.

Considered and rejected: retrying until something passes.

Consequences: Reports after a stop name the failing check and both attempts.

Provenance: Owner decision review, 2026-11-01.
