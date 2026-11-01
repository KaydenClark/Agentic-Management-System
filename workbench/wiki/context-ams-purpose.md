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

Status: preparation; owner answers pending. Source: Kayden's request in the
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

### Interview frontier

1. Recover the completed baseline's report/chat/file/assessment ID and exact
   candidate, findings and rubric. Requested from Kayden; no replacement baseline
   or invented numeric score.
2. Proposed: reuse approved Alignment Check r1. Each assessment has three runs;
   Excellent means three passing runs, Stable two. Alignment Score pools passed
   and applicable checks across the runs. Complete evidence and no unresolved
   Critical/Regression findings remain necessary; a numeric score alone cannot
   pass a candidate. Applying that contract to this campaign awaits an answer.
3. Proposed: baseline is attempt 0; each improvement candidate has at most three
   assessed versions: initial improvement, retry, retry, then stop/report.
   Assessment runs do not consume separate improvement attempts. Counter scope
   and baseline treatment await an answer; renaming must not erase failures.
4. Proposed: prepare and check locally, then declare one budget before any paid
   evaluation campaign. No campaign spending limit is recorded yet.

After answers: select the earliest evidenced gap from the baseline, freeze the
candidate scope, task/check inventory, grader/model/host identities and useful
effect before the deciding comparison. Record each attempt and failure, evidence,
counts, level, score, qualification/acceptance state, disposition and stop reason
in Supabase through the existing writer. Extend the row contract only where the
current fields cannot carry those meanings. Connect and verify the dev results
page against read-back rows, including missing evidence and stopped candidates.
Keep local completion, merge, deployment, retention and demonstrated benefit
separate. Reusable skill changes retain their catalog's own delivery process.

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
