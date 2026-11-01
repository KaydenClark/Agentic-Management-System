---
date: 2026-11-01
canonicalized_in:
  - evals
  - workbench/tools
---

# A repeated failure first checks the earlier fix

A failure seen twice may mean the earlier fix did not work, so that is checked first. A failure that recurs after a fix that held becomes a code check, not another prose rule. A new check starts non-blocking and blocks only once it has proven stable.

Considered and rejected: turning every repeat into a new check without asking whether the first fix failed.

Consequences: The improvement procedure checks the earlier fix before adding a check.

Provenance: Owner decision review, 2026-11-01, with the owner's correction.
