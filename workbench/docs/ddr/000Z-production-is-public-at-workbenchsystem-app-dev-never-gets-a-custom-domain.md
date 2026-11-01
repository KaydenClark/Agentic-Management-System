---
date: 2026-11-01
canonicalized_in:
  - site/vercel.json
---

# Production is public at workbenchsystem.app; dev never gets a custom domain

The AMS website's production deployment (`main`) is public at `workbenchsystem.app`, a domain the owner bought through Vercel with DNS on Vercel. `dev` and every other deployment stay behind Vercel Authentication: deployment protection is set to all-except-custom-domains, so only a custom domain skips login, and `dev` is never given one. The Vercel team moved to the Pro plan, so the daily deployment cap no longer blocks work; the main-and-dev-only deploy rule (ADR-003I) stays as hygiene.

Considered and rejected: the free `*.vercel.app` production URL as the public address (superseded by the owner's purchase); a custom domain for `dev` (it would make the protected staging site public).

Consequences: the owner attaches the domain to the project's production environment in the Vercel dashboard (the connector cannot write). Production changes only when the owner merges `dev` -> `main`. An agent must never assign a custom domain to `dev` or a preview.

Provenance: Owner decisions, 2026-11-01, relayed by the coordinating session. Checked by Orchestrator B through the Vercel API the same day: `workbenchsystem.app` is registered to the team, on Vercel nameservers, verified, and not yet attached to the project. The plan tier is not visible through the API.
