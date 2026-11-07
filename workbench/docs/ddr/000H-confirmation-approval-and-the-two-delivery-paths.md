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

## Amendment, 2026-11-06: bounded delivery branches

The [confirmed repair scope](../../wiki/context-workbench-adoption.md#jot-bc41fc6e-de68-4769-b8e6-0419470558c5) separates continuing work ownership from branch lifetime. A short-lived branch carries a bounded related change; Tasks may belong to Specs or Landmarks, and project maintenance uses its existing owner. Ready records/non-site changes reach checked main; website code/content reaches checked dev, retaining owner-only website promotion. After verified integration, reconcile evidence and clean up the delivered branch even while its parent remains open. Temporary assembly branches serve concrete dependencies. Preserve unfinished work and historical decisions. [RUNBOOK](../../../RUNBOOK.md#delivery-and-recovery) owns the procedure; optional delivery targets supply structural verification, never authority.
