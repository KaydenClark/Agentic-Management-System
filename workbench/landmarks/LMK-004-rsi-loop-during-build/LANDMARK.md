# LMK-004 - Running the RSI loop while the website is built

**Landmark ID:** LMK-004
**Status:** planned
**Priority:** 2
**Owner:** Kayden
**Updated:** 2026-11-01
**Catalog description:** The measured self-improvement loop, run on the website build and the work after it, with safeguards that keep its results honest.
**Blockers:** none
**Latest event:** Landmark mapped from the owner's confirmed decisions of 2026-11-01.
**Next gate:** Task planning for S-002; fill the Decision Records links once the decision records reach `main`.

## Direction

The whole website build is the loop's first trial; after it, the loop repeats. For now an improvement starts only from a failed result. Each round changes one owner (a runtime, control or skill), reruns the same tasks and ends in recorded rows plus a disposition: retain, revise or remove.

The loop carries its safeguards from the start: a noise-floor run, control arms, paired statistics, graders from the accepted version, sandboxed trials and enough held-out tasks before any public number. Three strikes, then stop. The loop runs until the owner's token meter is spent or a stop rule fires.

Coherence is part of the loop. Orchestrator C, which holds no secrets, checks that the project stays up to Spec, that skills are pinned and in sync, and how far `dev` runs ahead of `main`.

## Why It Matters

Outside research does not settle whether shaping an agent's environment improves results, so the AMS has to measure it against a no-AMS control and a plain-instruction control, and report the answer either way. An earlier loop built its apparatus and never ran it; this one runs on real work from day one.

## What Success Looks Like

- [ ] The loop and its safeguards are specified and the first trial, the site build, has produced rows in Supabase (S-002).
- [ ] At least one improvement that started from a failed result has a recorded disposition (S-002).
- [ ] Agents using the land skill no longer miss a landing event, shown by a rerun of the failing case after a change made through the skills repository's own process (S-011).
- [ ] A Python lifecycle CLI exists and is compared with the current Node lifecycle tools on the same tasks (S-012).
- [ ] Coherence checks report up-to-Spec state, skills pin and sync, and `dev`-ahead-of-`main` distance, and independent Spec review happens (S-013).

## Decision Records

The decision records for this landmark are being written in parallel and are not on `main` yet. They are named here by short title; links are filled at Task planning.

- RSI loop design and its safeguards.
- One improvement procedure, starting only from failed results for now.
- A failure seen twice: first check that the earlier fix worked.
- Skills pinned per run.
- Measure how far `dev` runs ahead of `main`.
- Three strikes, then stop.
- Session security: three orchestrators, no session holds untrusted input, credentials and outward actions together.
- The Python CLI is its own Spec, measured against the Node lifecycle tools.

## Child Specs

- [S-002 - RSI loop with safeguards](specs/S-002-rsi-loop/SPEC.md)
- [S-011 - Land skill catches every event](specs/S-011-land-skill-events/SPEC.md)
- [S-012 - Python lifecycle CLI](specs/S-012-python-lifecycle-cli/SPEC.md)
- [S-013 - Coherence checks](specs/S-013-coherence-checks/SPEC.md)

## Direct Tasks

- none

## Verification Procedure

```bash
node workbench/tools/spec-workbench.mjs show LMK-004
node workbench/tools/spec-workbench.mjs show S-002
node workbench/tools/spec-workbench.mjs doctor
```

Loop results are confirmed from the Supabase rows they produced, each naming its commit, skills pin and trial arm.

## Append-Only Evidence And Execution Log

| Date | Task | Event | Verification | Docs | Remaining gap |
|---|---|---|---|---|---|
| 2026-11-01 | none | Landmark mapped from confirmed owner decisions and the earlier loop proposal; child Specs S-002, S-011, S-012 and S-013 written as planned | render and doctor on the mapping branch | this record | Decision record links; Task planning; standing campaign approval |

## Reached Result

Pending.

## Supersession

- Supersedes: none
- Superseded by: none
