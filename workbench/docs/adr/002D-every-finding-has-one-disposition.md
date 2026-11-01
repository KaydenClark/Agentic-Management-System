---
date: 2026-11-01
canonicalized_in:
  - workbench/feedback
---

# Every finding has one disposition

Every finding has a stable ID and exactly one disposition, which doctor checks. A behavior finding closes only when a linked eval rerun is recorded.

This is a hypothesis. The owner confirmed it as a working rule, and the RSI loop tests whether it holds. Confirmed if within three loop rounds, at least one behavior finding goes from finding to eval task to rerun row. Refuted if open findings keep growing without linked rows.

Considered and rejected: findings left open with no owner or revisit trigger.

Consequences: An open finding names its owner and revisit trigger.

Provenance: Owner decision review, 2026-11-01.
