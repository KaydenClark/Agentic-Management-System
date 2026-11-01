---
type: project
status: active
sensitivity: normal
knowledge_role: curated
provenance:
  - Kayden, AMS template creation request, 2026-10-31
source_paths:
  - BLUEPRINT.md
last_verified: 2026-10-31
---
# AMS purpose and first RSI loop

AMS brings Kayden's agents, workflows, intent capture, skills and AI tools into one managed improvement loop. Product direction lives in [Blueprint](../../BLUEPRINT.md); this note preserves the reason and correction.

## 2026-10-31: Owner clarification

Kind: intent / correction. State: confirmed by the owner's direct instruction.
Source and speaker: Kayden, this chat's template creation request on 2026-10-31.

Kayden described AMS as “my full tool belt I use to work with AI wrapped up into one RSI loop that builds a website explaining itself.” He explained that the work repairs the broken Workbench and creates the system on top that runs it. The first RSI loop builds a website explaining and showing AMS.

This supersedes reducing the assignment to a judgment about whether it is “rebuilding the workbench.” It preserves both Workbench repair and the system built on it. The present authorized output is the complete AMS-tuned template set; no website implementation, benchmark result or deployment follows from this record.

## Evidence and sources

- [Blueprint](../../BLUEPRINT.md): current product intent.
- [Template inventory](../research/template-inventory.md): artifact coverage.
- [Research basis](../research/template-research-basis.md): inspected research and its limits.

## History

- 2026-10-31: captured Kayden's direct correction and intended first loop before adapting templates.
- 2026-11-01: Kayden requested Loop #1's first improvement wave, fitness/alignment results, Supabase recording and visibility on the Vercel dev site. This extends the earlier template-only endpoint; preparation is underway, and no assessment result is claimed.

## Loop #1 preparation: recovered design and open decisions

Status: design interview in progress; settled answers below. Source: Kayden's request in the
2026-11-01 “Prepare GPT_OS AMS RSI loop” chat and the checks below. This is a
continuation record, not evidence of a completed improvement or a paid campaign.

### Sources and responsibilities

- [S-002](../landmarks/LMK-004-rsi-loop-during-build/specs/S-002-rsi-loop/SPEC.md)
  owns the loop: start from failure, one bounded change, fixed comparisons,
  same-version noise floor, controls, independent graders, pinned skills,
  retained failures and dispositions.
- [S-006](../landmarks/LMK-002-rsi-presentation/specs/S-006-rsi-data-store/SPEC.md)
  owns the Supabase rows and local Python writer; [ADR-003H](../docs/adr/003H-supabase-holds-the-rsi-data-and-the-service-key-stays-local.md)
  keeps the service key local and the site read-only.
- [S-007](../landmarks/LMK-002-rsi-presentation/specs/S-007-rsi-charts/SPEC.md)
  owns presentation. Its TK-002 is the Supabase-to-page connection.
- [ADR-003F](../docs/adr/003F-one-standing-campaign-approval-and-no-per-merge-gate.md)
  owns one campaign approval with budget, round cap and stop rule;
  [ADR-002W](../docs/adr/002W-three-strikes-then-stop.md) owns the existing retry cap.
- [ADR-000A](../docs/adr/000A-improvement-claims-need-held-out-ledger-evidence.md)
  separates a fitness result from demonstrated improvement: public improvement
  claims need repeated held-out results, controls and uncertainty.
- [DDR-000W](../docs/ddr/000W-the-first-rsi-trial-is-building-the-site.md)
  connects actual website work to the loop. A built website alone is not a
  controlled baseline or proof of improved outcomes.

### Verified starting state, 2026-11-01

- AMS `main` inspected at `7427690c51e2f8be273543829417a6ab679a58b1`;
  `dev` at `992a5f86b7171fe837fb58dea3e91b3b7c59a9e4`.
- A read-only Supabase query returned 0 non-test `rsi_runs`, 0 non-test
  `rsi_results`, 0 test runs, and 651 non-test `build_events`. These counts
  do not disprove a baseline held elsewhere. Build events are not scored trials.
- At that `dev` commit, `site/app/rsi/page.tsx` consumes `fixtures/empty.ts`;
  `site/app/rsi/data.ts` explicitly has no Supabase reader. The page must be
  connected before saved results can appear there.
- Vercel lists deployment `dpl_Bv9QtiWy2qhJbSzz8yAidZSugSR4` as READY for that
  `dev` SHA. An authenticated fetch of `/rsi` failed to resolve/access it;
  this is deployment metadata plus source inspection, not rendered-page QA.

### Settled answers and next interview question

- Baseline means the current AMS repository implementation, not an existing scored report.
- Use approved Alignment Check r1: three assessment runs per attempt, pooled Alignment Score and the r1 fitness/acceptance rules.
- Each improvement candidate has three attempts maximum; baseline is outside the counter.
- Use the owner's paid-plan meter, not API tokens or an API campaign budget. Unknown usage measurements stay unknown.
- Next question: pin main for system records and dev for the website, assessing both as separate baseline components without merging first? Recommended: yes.

### Grilling failure reported by the owner

The agent let investigation and documentation displace the interview and inferred a missing report. Kayden asked what happened to the grilling session and called it a skill failure. Resume the ready decision round, wait for answers and preserve settled choices. No skill-text repair or assessment result is claimed.

<!-- jot-entry -->
### JOT-d91455d4-48d8-4b89-b3c6-0c6a7025c8e2
Kind: intent
State: confirmed
Recorded: 2026-11-01T16:41:10.477Z
Author: Kayden
Source: Kayden, Prepare GPT_OS AMS RSI loop chat, 2026-11-01, initial request
Topic: ams-purpose
Supersedes: none

Kayden requests Loop #1 for GPT_OS/AMS: recover the RSI design and the baseline he says was just completed, perform the first wave of improvement, log actual results in Supabase and make them viewable on the Vercel dev site while building the website that explains the system. Exact owner wording: "Only stable or excelent skills or other AMS improvements pass. otherwise it gets sent back for another RSI loop until it does or hits the 3 strikes your out rule." Exact sequence: "(1) initial run -> (2) retry -> (3) retry -> stop". He invokes grill-with-docs to get ready to implement and record understanding as building continues. This is real AMS improvement work, not a demo batch or a reduced website cutoff. The baseline artifact, findings and assessment identity have not yet been located; the owner's statement does not supply a score or measured result. Unresolved: applying Alignment Check r1 to this campaign, the scope of the attempt counter and whether baseline is outside it, the initial improvement targets once baseline is recovered, and any paid-campaign budget. Preserve existing safeguards and do not invent assessment results.
<!-- /jot-entry -->

<!-- jot-entry -->
### JOT-6e1500aa-cbde-41c2-b638-f10fa9ef83e3
Kind: intent
State: confirmed
Recorded: 2026-11-01T16:46:14.011Z
Author: Kayden
Source: Kayden, this chat, 2026-11-01 corrections
Topic: ams-purpose
Supersedes: JOT-d91455d4-48d8-4b89-b3c6-0c6a7025c8e2

Kayden corrected the baseline: it is the current AMS repository implementation (branches URL supplied), not an existing scored report. He confirmed approved r1 and three improvement attempts per candidate, baseline excluded. Execution uses his paid-plan meter, not API tokens or an API campaign budget. He reported the missing grilling flow as a skill failure. Resume the interview; settle the exact main/dev baseline, wait for answers, and document settled choices. No assessment has been performed.
<!-- /jot-entry -->
