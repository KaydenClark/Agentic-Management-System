---
date: 2026-11-01
canonicalized_in:
  - AGENTS.md
---

# Built, deployed and passing claims name their commit

Every "built", "deployed" or "passing" claim names its commit and what it checked. A deployment claim checks the deployed site.

Considered and rejected: claims without a commit, or a deploy claim taken from a build log.

Consequences: Reports carry the commit and the check.

Provenance: Owner decision review, 2026-11-01.
