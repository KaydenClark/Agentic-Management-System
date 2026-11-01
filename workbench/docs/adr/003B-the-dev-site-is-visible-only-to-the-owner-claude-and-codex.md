---
date: 2026-11-01
canonicalized_in:
  - site
---

# The dev site is visible only to the owner, Claude and Codex

Dev and preview deployments are visible only to the owner, Claude and Codex. Vercel Authentication (Standard Protection) stays on. Claude reaches them through the Vercel connector. Codex uses a Vercel Protection Bypass for Automation secret that the owner keeps in Codex's own secret store, never in Git or chat. Production becomes public only after the owner merges `dev` -> `main`.

Considered and rejected: public previews, or a bypass secret stored in the repository.

Consequences: No access secret appears in Git or chat.

Provenance: Owner answer, 2026-11-01, given after the decision review.
