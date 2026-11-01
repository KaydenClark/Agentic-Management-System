---
date: 2026-11-01
canonicalized_in:
  - site/vercel.json
---

# Only main, dev and site branches deploy to Vercel

Vercel builds only `main` (production), `dev` (the protected staging site) and branches named `site/<slug>` (site previews). Every other branch creates no deployment. This is free-tier protection: on 2026-11-01 pushes from non-site branches used up the Hobby plan's 100 deployments a day, which blocked `dev` and site previews.

Considered and rejected: upgrading to a paid plan (any paid-plan request stops for the owner); relying only on the `ignoreCommand` skip (cancelled builds still count as deployments).

Consequences: `site/vercel.json` sets `git.deploymentEnabled` with `"*"` and `"**"` false and `main`, `dev` and `site/**` true. Site work branches must be named `site/<slug>` to get a preview. Non-site PRs into `main` show no Vercel check.

Provenance: Orchestrators A and B with the coordinating session, 2026-11-01, after Vercel refused deployments with `api-deployments-free-per-day`.
