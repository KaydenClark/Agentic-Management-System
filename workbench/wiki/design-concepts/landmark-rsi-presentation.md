---
type: design-concept
status: active
sensitivity: normal
knowledge_role: curated
provenance:
  - S-000C maintained Wiki repair, 2026-11-04
source_paths:
  - workbench/landmarks/LMK-002-rsi-presentation
  - workbench/landmark-tracker/destination-questions
parent: none
authorized_by: S-000C Wiki repair under JOT-a66709e3
last_verified: 2026-11-04
---

# Presentation of the RSI

## What the Landmark is

The website presents what RSI actually measured, including empty, failed, unchanged and regressed results. Traceable evidence matters more than a populated chart: a build event is not a scored trial, and a qualified candidate is not proof of benefit everywhere.

## Current accepted answers

No DQCs are assigned to this Landmark in the inspected tracker. There are no card-confirmed answers to synthesize. Its [Landmark direction](../../landmarks/LMK-002-rsi-presentation/LANDMARK.md) and [charts-start-blank decision](../../docs/ddr/000T-charts-start-blank-and-data-is-never-fabricated.md) establish the existing design: local Python writes canonical rows; the site reads presentation data under read-only access and invents no values. These are sourced design contracts, not newly confirmed interview answers.

## Open and unresolved

Inference: storage, lineage and chart behavior must be checked together before treating a displayed result as evidence. Their separate Specs own those checks and present delivery limits. This article neither reads live Supabase nor certifies the protected deployment. [The RSI explanation](../context-feedback-improvement-loop-plan.md) preserves Stage B/campaign holds; presentation readiness cannot release a campaign or imply broad benefit.

## Where the work lives

[LMK-002 — Presentation of the RSI](../../landmarks/LMK-002-rsi-presentation/LANDMARK.md) owns this direction. [S-006 — RSI data store](../../landmarks/LMK-002-rsi-presentation/specs/S-006-rsi-data-store/SPEC.md) owns persistence and [S-007 — RSI chart pages](../../landmarks/LMK-002-rsi-presentation/specs/S-007-rsi-charts/SPEC.md) owns presentation. Their participation in the [RSI Loop](landmark-rsi-loop.md) crosses Landmark placement without creating duplicate ownership. [AMS purpose](../context-ams-purpose.md) explains the website's evidence role.

## Evidence and Sources

- [Landmark source at intake revision](https://github.com/KaydenClark/Agentic-Management-System/blob/da4f0ca809c6759e9c17ce798c52753dab123a65/workbench/landmarks/LMK-002-rsi-presentation/LANDMARK.md) fixes this synthesis's inspected context; the live Landmark link above owns later changes.
- [Tracker question sources at intake revision](https://github.com/KaydenClark/Agentic-Management-System/tree/da4f0ca809c6759e9c17ce798c52753dab123a65/workbench/landmark-tracker/destination-questions) bound card coverage. Only the Grill Board currently has assigned cards; absence supplies no new confirmation.
- [Landmark history](../history/LMK-002.md) retains lifecycle judgments, approvals and corrections; this explanation copies no execution queue.

## History

- 2026-11-04: Created by S-000C authorized Wiki repair from existing Landmark/card sources; distinguishes current confirmed meaning, unresolved claims and implementation evidence. Updated alongside related topic explanations and MEMORY routes.
