---
date: 2026-11-01
canonicalized_in:
  - RUNBOOK.md
---

# Measure how far dev runs ahead of main

The AMS measures how far `dev` runs ahead of `main` and shows it, so the gap never grows unnoticed.

Considered and rejected: leaving drift unmeasured; an earlier trunk ran thousands of commits ahead of `main`.

Consequences: The Coherence orchestrator watches the drift.

Provenance: Owner decision review, 2026-11-01.
