---
date: 2026-11-01
canonicalized_in:
  - site/vercel.json
---

# Only main, dev and site branches deploy to Vercel

Vercel builds only `main` (production), `dev` (the protected staging site) and the site branches on an explicit allow list in `site/vercel.json` (site previews): `site/<slug>`, plus orchestrator A's existing `proto/**`, `feat/s003-*`, `feat/s007-*`, `feat/s009-*` and its records branch. Every other branch creates no deployment. This is free-tier protection: on 2026-11-01 pushes from non-site branches used up the Hobby plan's 100 deployments a day, which blocked `dev` and site previews.

Considered and rejected: upgrading to a paid plan (any paid-plan request stops for the owner); relying only on the `ignoreCommand` skip (cancelled builds still count as deployments).

Consequences: `site/vercel.json` sets `git.deploymentEnabled` with `"*"` and `"**"` false and only the allow-listed branches true. New site work uses `site/<slug>`; a new site Spec adds its own branch pattern to the same file. Non-site branches must stay off those patterns. Non-site PRs into `main` show no Vercel check.

Provenance: Orchestrators A and B with the coordinating session, 2026-11-01, after Vercel refused deployments with `api-deployments-free-per-day`.

Changed 2026-11-01: allow list widened to orchestrator A's existing site branches, by Spec number only so non-site `feat/` branches stay off.

Changed 2026-11-01: previews replaced by CI to protect the free quota. Only `main` and `dev` deploy; the GitHub Actions check `site builds` (`.github/workflows/site-build.yml`: npm ci, lint if present, test, build in `site/`) is the required check for site PRs into `dev` and `main`, in place of the Vercel preview. It skips cleanly where `site/package.json` is absent.
