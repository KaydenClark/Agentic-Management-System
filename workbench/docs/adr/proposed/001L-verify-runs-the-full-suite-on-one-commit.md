---
date: 2026-11-01
canonicalized_in:
  - RUNBOOK.md
---

# Verify runs the full suite on one commit

`verify <sha>` runs the full suite on that commit in a fresh worktree. A result without a commit is not proof.

Considered and rejected: results from a working tree with uncommitted changes.

Consequences: Verification output names its commit.

Provenance: Owner decision review, 2026-11-01.
