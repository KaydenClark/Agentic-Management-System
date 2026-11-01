---
date: 2026-11-01
canonicalized_in:
  - RUNBOOK.md
  - pyproject.toml
---

# The AMS runtime is a small Python CLI

The AMS is a small Python CLI where each command does one action and records stay plain readable files. A command exists only where it prevents a repeated agent mistake or does deterministic work. The current Node lifecycle tools run this build and serve as the baseline; the Python CLI is its own Spec, measured against them.

Considered and rejected: replacing the Node tools before the Python CLI is measured against them.

Consequences: The Python CLI Spec reports its results against the Node baseline.

Provenance: Owner decision review, 2026-11-01, with the owner's correction.
