---
date: 2026-11-01
canonicalized_in:
  - RUNBOOK.md
---

# Check a host before relying on it

Before relying on a host, run a short check (Python runs, skills load, paths write, Git works) and record each result. A missing capability blocks only the work that needs it.

Considered and rejected: assuming a host is capable, or halting all work for one missing capability.

Consequences: The Runbook carries the host check.

Provenance: Owner decision review, 2026-11-01.
