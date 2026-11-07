# LMK-004 - RSI Loop

**Landmark ID:** LMK-004
**Status:** active
**Priority:** 2
**Owner:** Kayden
**Updated:** 2026-11-07
**Catalog description:** Measured skill improvement on website work, with qualification and later-use evidence.
**Blockers:** none
**Next gate:** Implement TK-003E/F/G, then prove the first Servitor case in TK-003H. Earlier campaign stops remain.

## Direction

The RSI Loop improves shared skills/Workbench methods from real failures and checks persistence. The [owner map](../../wiki/context-feedback-improvement-loop-plan.md#current-mapped-destination) assigns independently verifiable capabilities; website work supplies the first proof.

The [current owner instruction](../../wiki/context-feedback-improvement-loop-plan.md#jot-7862917b-48cb-41bc-8f21-0ddfc611cdac) requires one complete skill improvement on a real AMS website task on Servitor as the first proof. RSI is an optional addition to participating Workbenches; Workbench setup and shared skills remain usable without it.

A per-chat Python observer records requested, loaded and used skills and failures. Skipping an explicitly requested skill is Critical. The orchestrator schedules routine repair after current work and blocking repair in a separate chat, with one active repair per skill. Repair uses author-skill and prune-artifact and exercises the draft plus related skills in a separate website test session on Servitor. Eligible repairs pass qualification, merge and automatically update everyday skills. Later use proves the accepted version loaded and measures recurrence.

Supabase owns shared failure/improvement history; Git owns skills and regression tests. Existing Markdown failure intake remains a local capture/recovery surface until implemented transport reconciles stable occurrences into the shared history. Three skill audits report separate Quality/Regression scores, Critical result and worst-failure grade (S-002), while whole-Workbench Alignment stays separate. S-007 shows safe results and actual audit counts. These are required outcomes, not claims about the current runtime.

Use subscription-meter capacity with Mid/Small Codex or Claude workers, High when needed. Preserve initial attempt -> retry -> retry -> stop, baseline excluded, and prior frozen campaign conditions. This mapping purchases nothing, starts no trials and grants no installation/deployment authority.

Individual skills and declared coupled bundles can improve; bundle results do not prove each component improved. Historical failures and previously successful behavior form development/regression evidence; fresh work tests generalization. Recurrence and owner interventions are measured per eligible use. Preserve failed attempts, uncertainty and previous decisions.

S-006/S-007 remain cross-landmark storage/presentation owners in LMK-002. S-012’s lifecycle CLI is distinct from S-000B. S-000A/S-011 retain scope and stops.

## Why It Matters

A repair must fix the underlying problem, preserve the connected workflow and reach everyday use. Later evidence must show whether the problem returns.

Measure against no-AMS and plain-instruction controls and report either outcome; research and apparatus alone prove no benefit.

## What Success Looks Like

- [ ] Site-build trial and safeguards produce traceable Supabase rows and a failed-result improvement disposition (S-002).
- [ ] Repaired land skill passes the missed-event case through the skills source process (S-011).
- [ ] Python lifecycle CLI is compared with Node on identical tasks (S-012).
- [ ] Coherence reports up-to-Spec, skills pin/sync and dev/main distance; independent Spec review occurs (S-013).
- [ ] Distinct shared methods preserve workflow/credit and truthful prerequisites/composition, with verified outcomes and no AMS preparation bypass (S-000A).

[History](../../wiki/history/LMK-004.md) retains prior evidence.

## End-to-end acceptance

- [ ] **First proof on Servitor:** one real website failure reaches root-cause diagnosis, author-skill/prune-artifact repair, connected draft-session tests, three qualified audits, eligible merge, automatic everyday update and observed later use. A merged but never loaded repair fails.
- [ ] **Observer and scheduling:** a skipped requested skill creates a Critical failed-use record; routine work finishes before repair starts, a blocker uses a separate chat, and competing triggers never run two repairs for the same skill.
- [ ] **Optional participation:** a Workbench without RSI can use the skills without observer/reporting setup; no activity is silently collected from nonparticipants.
- [ ] **Audit contract:** Quality-only failure in one of three runs prevents Excellent; any Critical failure yields Broken. Actual completed audit count, missing evidence and qualification remain visible; whole-Workbench Alignment is separate.

- [ ] One reported failure reaches diagnosis, controlled repair, qualification, no-regression decision, authorized adoption and later-use evidence, traceable through Supabase and the public-safe view.
- [ ] Interrupt and redeliver work: continuation preserves claims, evidence and attempt limits without duplicate external effects or owner relaying each step.
- [ ] Reintroduce a failure: detection records recurrence before owner intervention. Existing successes remain tested; absent use denominators cannot imply a recurrence rate.
- [ ] Numeric presentation derives from canonical evidence and distinguishes operational activity, audit fitness, useful benefit and generalization. Research-inspired design alone cannot pass.

## Decision Records

[Current owner intent](../../wiki/context-feedback-improvement-loop-plan.md#jot-7862917b-48cb-41bc-8f21-0ddfc611cdac) governs the new destination; historical campaign decisions remain frozen. S-002 owns evaluation/control/attempt contracts, S-000B recovery, S-006 storage and S-011 delivery. See the [decision catalog](../../docs/adr/) and [first website trial](../../docs/ddr/000W-the-first-rsi-trial-is-building-the-site.md). The [prior decision index](https://github.com/KaydenClark/Agentic-Management-System/blob/5f0c1d783cdf04fdf9fd87c5c54caf61aaf132a8/workbench/landmarks/LMK-004-rsi-loop-during-build/LANDMARK.md#decision-records) preserves every earlier reference; this Map resets none.

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

- [S-000C - Maintained Wiki understanding](specs/S-000C-wiki-maintenance/SPEC.md)

## Direct Tasks

- [TK-002M - Finish the RSI loop design and prepare its executable Task graph](tasks/TK-002M/TASK.md) (Stage A preparation closed and delivered by PR169)

## Verification Procedure

Use linked Spec observer/harness, scorer, writer/readback and chart seams. Join chat/request IDs, case/candidate pins, three actual run IDs, merge/update/loaded versions and later uses. Mapping inspected records/scorer only, not Servitor or live Supabase. Existing code’s passing-run-count grade is an implementation gap.

`node workbench/tools/spec-workbench.mjs show LMK-004`, `show S-002` and `doctor` inspect records. Runtime proof comes from produced Supabase rows naming commit, skill pin and trial arm.

## Reached Result

Pending.

## Supersession

- Supersedes: none
- Superseded by: none
