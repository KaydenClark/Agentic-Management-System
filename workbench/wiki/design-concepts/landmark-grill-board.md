---
type: design-concept
status: active
sensitivity: normal
knowledge_role: curated
provenance:
  - S-000C maintained Wiki repair, 2026-11-04
source_paths:
  - workbench/landmarks/LMK-001-grill-board
  - workbench/landmark-tracker/destination-questions
parent: none
authorized_by: S-000C Wiki repair under JOT-a66709e3
last_verified: 2026-11-04
---

# Grill Board

## What the Landmark is

The local Python Board makes owner attention actionable while preserving question identity, reasons and exact confirmed wording. It connects concept development to execution without owning execution state. The public demonstration is a separate website capability.

## Current accepted answers

[DQC-000A — Grilling Board purpose and DQC lifecycle](../../landmark-tracker/destination-questions/DQC-000A.json), revision10 with confirmation snapshot8, records the confirmed answer: cards present full readbacks; terminal and Board reach the same DQC; exact confirmations/corrections survive; changed answers and quality feedback are reconciled after rounds. TRACKER projects concepts and TASKBOARD projects execution, linked by stable IDs. See [the maintained capability explanation](../context-grilling-board.md) for flow, rationale and evidence.

## Open and unresolved

[DQC-000B — What belongs on the Grilling Board](../../landmark-tracker/destination-questions/DQC-000B.json), [DQC-000C — Question and answer flow](../../landmark-tracker/destination-questions/DQC-000C.json) and [DQC-000D — Keeping intent current](../../landmark-tracker/destination-questions/DQC-000D.json) are pending, non-actionable branch context derived from the confirmed parent, not separately confirmed answers. No new owner request is inferred from them. The later [redesign correction](../context-grilling-board.md#jot-c9dcebb6-4d50-4d6d-95d7-30d723d66d53) requires functional search/filter/batch controls; delivered DQC lifecycle does not establish that redesign. Owner Human QA and Spec acceptance remain their own gates.

Page review also requires explicit current route owners and trustworthy protected HTML. Content hashes and preserved metadata history do not fill missing inventory, capture private criticism or demonstrate its later use; [the maintained explanation](../context-grilling-board.md#established-behavior-and-remaining-gap) routes those distinct requirements to S-005 and its guide.

## Where the work lives

[LMK-001 — Grill Board](../../landmarks/LMK-001-grill-board/LANDMARK.md) owns direction. [S-004 — Grill Board cards and answers](../../landmarks/LMK-001-grill-board/specs/S-004-grill-board-cards/SPEC.md) owns implementation/proof; [S-005 — Page review cards](../../landmarks/LMK-001-grill-board/specs/S-005-page-review-cards/SPEC.md) owns content-bound page review. [The guide](../../../grill-board/README.md) owns operations, including the agent reconciliation required after Finish this round.

## Evidence and Sources

- [Landmark source at intake revision](https://github.com/KaydenClark/Agentic-Management-System/blob/da4f0ca809c6759e9c17ce798c52753dab123a65/workbench/landmarks/LMK-001-grill-board/LANDMARK.md) fixes this synthesis's inspected context; the live Landmark link above owns later changes.
- [Tracker question sources at intake revision](https://github.com/KaydenClark/Agentic-Management-System/tree/da4f0ca809c6759e9c17ce798c52753dab123a65/workbench/landmark-tracker/destination-questions) bound card coverage. Only the Grill Board currently has assigned cards; absence supplies no new confirmation.
- [Landmark history](../history/LMK-001.md) retains lifecycle judgments, approvals and corrections; this explanation copies no execution queue.

## History

- 2026-11-04: Created by S-000C authorized Wiki repair from existing Landmark/card sources; distinguishes current confirmed meaning, unresolved claims and implementation evidence. Updated alongside related topic explanations and MEMORY routes.
- 2026-11-06: PR174 management reconciled content identity, ownership history and private-feedback limits into the existing explanation; S-005 remains unaccepted.
