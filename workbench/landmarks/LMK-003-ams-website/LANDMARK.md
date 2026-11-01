# LMK-003 - AMS website

**Landmark ID:** LMK-003
**Status:** planned
**Priority:** 1
**Owner:** Kayden
**Updated:** 2026-11-01
**Catalog description:** The public presentation website for the AMS, a Next.js app in `site/` on Vercel, built with the AMS as its first outside product.
**Blockers:** none
**Latest event:** Landmark mapped from the owner's confirmed decisions of 2026-11-01.
**Next gate:** Task planning for S-003; fill the Decision Records links once the decision records reach `main`.

## Direction

A public, blog-style site that explains what the AMS is, why it exists and how it works, and shows the real thing rather than describing it. Its pages are the orientation tour, the RSI charts (LMK-002), a demo Grill Board, the governance stack, the flow charts and a wiki of the owner's skills.

The site is a Next.js app in `site/`, deployed on Vercel at a free `*.vercel.app` address. It is presentation only: data it shows, such as RSI results and build history, comes from Supabase. Python owns the backends; there is no FastAPI and no development view on Vercel.

Site work goes feature -> `dev` -> `main`. `dev` is the protected staging deployment, visible only to the owner, Claude and Codex. Only the owner merges `dev` -> `main`, so production changes only after the owner has seen it. Website orchestrator A deploys only through Git pushes to `dev`.

## Why It Matters

The site is how the owner shows the AMS to friends, a manager or a CTO, and how the owner relearns the system. Because it is built with the AMS while the RSI loop measures that build, the site is its own evidence, as long as every claim on it links to something real.

## What Success Looks Like

- [ ] The site shell and orientation tour are on the protected `dev` deployment, in the old Grill Board's theme tokens, light and dark, usable at 375 px (S-003).
- [ ] Every page shows its deployed commit SHA, linked to GitHub, and carries a draft mark until the owner approves it (S-003).
- [ ] The skills wiki presents site-written summaries of the owner's skills (S-008).
- [ ] A demo Grill Board page shows sample cards with non-engineering questions (S-009).
- [ ] The governance stack and flow charts are drawn from, or tested against, the code they depict (S-010).
- [ ] The public hygiene check passes on every candidate: no host paths, secrets, private research or traces (S-003).
- [ ] Production on `main` changes only through an owner-approved `dev` -> `main` merge.

## Decision Records

The decision records for this landmark are being written in parallel and are not on `main` yet. They are named here by short title; links are filled at Task planning.

- Site stack: Next.js on Vercel, Python backends, Supabase; no FastAPI.
- Site branch model: feature -> `dev` -> `main`; only the owner approves `dev` -> `main`.
- No development view on Vercel; the Grill Board stays local.
- The public site only presents.
- Owner's voice: preserved intent plus taste learned from recorded feedback.
- Skills wiki: site-written summaries.
- Domain: free `*.vercel.app`.

## Child Specs

- [S-003 - Showcase site shell and orientation tour](specs/S-003-showcase-site/SPEC.md)
- [S-008 - Skills wiki](specs/S-008-skills-wiki/SPEC.md)
- [S-009 - Demo Grill Board page](specs/S-009-demo-grill-board/SPEC.md)
- [S-010 - Governance stack and flow charts](specs/S-010-governance-flow-charts/SPEC.md)

## Direct Tasks

- none

## Verification Procedure

```bash
node workbench/tools/spec-workbench.mjs show LMK-003
node workbench/tools/spec-workbench.mjs show S-003
node workbench/tools/spec-workbench.mjs doctor
```

Page checks run against the built output and the protected `dev` deployment at a named commit, not the source tree.

## Append-Only Evidence And Execution Log

| Date | Task | Event | Verification | Docs | Remaining gap |
|---|---|---|---|---|---|
| 2026-11-01 | none | Landmark mapped from confirmed owner decisions; S-003 ported and rewritten; S-008, S-009 and S-010 written as planned | render and doctor on the mapping branch | this record | Decision record links; Next app; Task planning |

## Reached Result

Pending.

## Supersession

- Supersedes: none
- Superseded by: none
