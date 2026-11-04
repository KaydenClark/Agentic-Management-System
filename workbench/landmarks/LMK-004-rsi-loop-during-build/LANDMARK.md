# LMK-004 - RSI Loop

**Landmark ID:** LMK-004
**Status:** planned
**Priority:** 2
**Owner:** Kayden
**Updated:** 2026-11-01
**Catalog description:** The measured self-improvement loop, run on the website build and the work after it, with safeguards that keep its results honest.
**Blockers:** none
**Next gate:** Launch TK-002M to finish design and preparation; stopped campaigns and implementation holds remain scoped.

## Direction

The RSI Loop turns failures from real agent work into demonstrated improvements to shared skills and the Workbench, then checks whether those improvements persist. The website build is the first application; later work supplies further evidence. The [owner map](../../wiki/context-feedback-improvement-loop-plan.md#current-mapped-destination) establishes this as a Landmark composed of independently verifiable capabilities.

Failures enter one Markdown log. Diagnosis identifies the owning cause; cases and comparisons use the existing Fitness/Alignment checks. The external Python worker carries authorized execution and recovery, Supabase holds durable cases/runs/candidates/comparisons/dispositions, and presentation shows safe evidence. Qualified Stable/Excellent changes need useful benefit and no regression before merge; adoption and later observed loading remain distinct.

Use subscription-meter capacity with Mid/Small Codex or Claude workers, High when needed. Preserve initial attempt -> retry -> retry -> stop, baseline excluded, and prior frozen campaign conditions. This mapping purchases nothing, starts no trials and grants no installation/deployment authority.

Individual skills and declared coupled bundles can improve; bundle results do not prove each component improved. Historical failures and previously successful behavior form development/regression evidence; fresh work tests generalization. Recurrence and owner interventions are measured per eligible use. Preserve failed attempts, uncertainty and previous decisions.

Capability ownership crosses existing landmark placements: S-006 and S-007 remain in LMK-002 and supply storage and presentation. Their placement does not duplicate ownership. S-012's general lifecycle CLI is separate from S-000B's RSI worker. The existing S-000A catalog refocus and S-011 source repairs retain scope and stops.

## Why It Matters

Outside research does not settle whether shaping an agent's environment improves results, so the AMS has to measure it against a no-AMS control and a plain-instruction control, and report the answer either way. An earlier loop built its apparatus and never ran it; this one runs on real work from day one.

## What Success Looks Like

- [ ] The loop and its safeguards are specified and the first trial, the site build, has produced rows in Supabase (S-002).
- [ ] At least one improvement that started from a failed result has a recorded disposition (S-002).
- [ ] Agents using the land skill no longer miss a landing event, shown by a rerun of the failing case after a change made through the skills repository's own process (S-011).
- [ ] A Python lifecycle CLI exists and is compared with the current Node lifecycle tools on the same tasks (S-012).
- [ ] Coherence checks report up-to-Spec state, skills pin and sync, and `dev`-ahead-of-`main` distance, and independent Spec review happens (S-013).
- [ ] Shared skills teach distinct methods with verified reliability/capability outcomes, truthful composition/prerequisite labels and preserved workflows/credit; AMS no longer bypasses preparation for source changes (S-000A).

History: [LMK-004 history](../../wiki/history/LMK-004.md).

## End-to-end acceptance

- [ ] One reported failure reaches diagnosis, controlled repair, qualification, no-regression decision, authorized adoption and later-use evidence, traceable through Supabase and the public-safe view.
- [ ] Interrupt and redeliver work: continuation preserves claims, evidence and attempt limits without duplicate external effects or owner relaying each step.
- [ ] Reintroduce a failure: detection records recurrence before owner intervention. Existing successes remain tested; absent use denominators cannot imply a recurrence rate.
- [ ] Numeric presentation derives from canonical evidence and distinguishes operational activity, audit fitness, useful benefit and generalization. Research-inspired design alone cannot pass.

## Decision Records

The decision records under this landmark, one line each, linked to their record.

- [The RSI loop design](../../docs/adr/archive/002F-the-rsi-loop-design.md)
- [The first RSI trial is building the site](../../docs/ddr/000W-the-first-rsi-trial-is-building-the-site.md)
- [One improvement procedure, starting from failed results](../../docs/adr/002A-one-improvement-procedure-starting-from-failed-results.md)
- [A repeated failure first checks the earlier fix](../../docs/adr/002B-a-repeated-failure-first-checks-the-earlier-fix.md)
- [Measure the noise floor before trusting a change](../../docs/adr/002G-measure-the-noise-floor-before-trusting-a-change.md)
- [Every round runs two control arms](../../docs/adr/002H-every-round-runs-two-control-arms.md)
- [Comparisons use paired per-task statistics](../../docs/adr/002I-comparisons-use-paired-per-task-statistics.md)
- [Every ledger row records cost and run state](../../docs/adr/002J-every-ledger-row-records-cost-and-run-state.md)
- [Graders come from the accepted version](../../docs/adr/002K-graders-come-from-the-accepted-version.md)
- [Trials run in a sandbox](../../docs/adr/002L-trials-run-in-a-sandbox.md)
- [More than two held-out tasks before a public number](../../docs/adr/002M-more-than-two-held-out-tasks-before-a-public-number.md)
- [Studied held-out tasks retire to the dev set](../../docs/adr/002N-studied-held-out-tasks-retire-to-the-dev-set.md)
- [One standing campaign approval](../../docs/adr/archive/002O-one-standing-campaign-approval.md)
- [Each RSI run pins the skills commit](../../docs/adr/002R-each-rsi-run-pins-the-skills-commit.md)
- [Three strikes, then stop](../../docs/adr/002W-three-strikes-then-stop.md)
- [Measure how far dev runs ahead of main](../../docs/adr/002T-measure-how-far-dev-runs-ahead-of-main.md)
- [No session holds untrusted input, secrets and outward actions together](../../docs/adr/002P-no-session-holds-untrusted-input-secrets-and-outward-actions-together.md)
- [Three orchestrators split the work by risk](../../docs/adr/002Z-three-orchestrators-split-the-work-by-risk.md)
- [The AMS runtime is a small Python CLI](../../docs/adr/000X-the-ams-runtime-is-a-small-python-cli.md)

## Capability owners

- [S-000B - Resumable RSI worker](specs/S-000B-rsi-worker/SPEC.md)
- [S-006 - Durable RSI data](../LMK-002-rsi-presentation/specs/S-006-rsi-data-store/SPEC.md) (cross-landmark dependency)
- [S-007 - RSI evidence presentation](../LMK-002-rsi-presentation/specs/S-007-rsi-charts/SPEC.md) (cross-landmark dependency)

## Child Specs

- [S-002 - RSI loop with safeguards](specs/S-002-rsi-loop/SPEC.md)
- [S-000A - Behavior-specific shared skills and reliable AMS preparation](specs/S-000A-skills-refocus/SPEC.md)
- [S-011 - Land skill catches every event](specs/S-011-land-skill-events/SPEC.md)
- [S-012 - Python lifecycle CLI](specs/S-012-python-lifecycle-cli/SPEC.md)
- [S-013 - Coherence checks](specs/S-013-coherence-checks/SPEC.md)

## Direct Tasks

- [TK-002M - Finish the RSI loop design and prepare its executable Task graph](tasks/TK-002M/TASK.md) (held until the design launch)

## Verification Procedure

```bash
node workbench/tools/spec-workbench.mjs show LMK-004
node workbench/tools/spec-workbench.mjs show S-002
node workbench/tools/spec-workbench.mjs doctor
```

Loop results are confirmed from the Supabase rows they produced, each naming its commit, skills pin and trial arm.

## Reached Result

Pending.

## Supersession

- Supersedes: none
- Superseded by: none
