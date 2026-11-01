---
date: 2026-11-01
supersedes:
canonicalized_in:
  - AGENTS.md
  - RUNBOOK.md
---

# Confirmation, approval and the two delivery paths

Confirmation settles meaning; approval permits a named scope, and the owner may give both in one message. Work that is not deployed goes feature -> `main`, and agents merge it. Anything deployed to Vercel goes feature -> `dev` -> `main`, and only the owner approves `dev` -> `main`. Agents never ask again for what an approval already covers.

Considered and rejected: a permanent development trunk with `main` as an owner-approved branch for all work; that model let the trunk drift far ahead of `main`.

Consequences: There is no `integration` branch. The owner's only merge gate is `dev` -> `main` for the site.

Provenance: Owner decision review, 2026-11-01, with the owner's correction. Owner answer, 2026-11-01 (round 1).
