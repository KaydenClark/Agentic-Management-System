---
date: 2026-11-01
canonicalized_in:
  - AGENTS.md
---

# A PR merges only after checks on the combined commit

A pull request merges only after it is brought up to date with its target branch and passes checks on that combined commit, one at a time. Site pull requests target `dev`; other pull requests target `main`.

Considered and rejected: merging on checks run against a stale base.

Consequences: Agents merge the target into the branch before merging.

Provenance: Owner decision review, 2026-11-01, with the owner's correction.
