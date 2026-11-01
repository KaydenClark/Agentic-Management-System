---
date: 2026-11-01
canonicalized_in:
  - evals
---

# Measure the noise floor before trusting a change

Before any change is trusted, the current version is run against itself through the whole task set. Per-task flip rate and spread are recorded, and any difference inside the noise floor is treated as noise.

Considered and rejected: comparing a candidate with one prior run.

Consequences: The noise-floor run is step zero of the loop.

Provenance: Owner decision review, 2026-11-01.
