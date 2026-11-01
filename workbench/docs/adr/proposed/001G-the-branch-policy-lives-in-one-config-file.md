---
date: 2026-11-01
canonicalized_in:
  - workbench/manifest.json
---

# The branch policy lives in one config file

The branch policy is declared in one config file that tools read. It declares `main`, plus `dev` for anything deployed to Vercel. Every review, approval and deploy names its exact commit.

Considered and rejected: branch names hard-coded in tools.

Consequences: Tools read the branch names from the config.

Provenance: Owner decision review, 2026-11-01, with the owner's correction.
