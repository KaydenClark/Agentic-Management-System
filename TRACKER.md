# Intent tracker

Generated from DQC records. Execution state and proof remain in Landmarks, Specs and Tasks.

## DQC-000A — Grilling Board purpose and DQC lifecycle

Revision 10; confirmed. [Record](workbench/landmark-tracker/destination-questions/DQC-000A.json)

<pre>**Summary**

AMS has two connected lanes. TASKBOARD.md tracks execution through Landmarks, Specs and Tasks. TRACKER.md tracks intent and concepts through stable Destination Question Cards (DQCs), including how those concepts develop and move through execution. Execution records reference their originating DQCs by stable ID; DQCs can reference the corresponding Landmarks, Specs and Tasks.

DQCs are created when the interview starts: its main branches become initial DQCs. Each Grilling Board card is a view of its DQC, presenting a question laid out as a complete readback with a suggested answer that the owner can confirm or correct. Existing DQCs evolve as understanding changes; distinct new decisions receive new DQCs.

**The why**

Questions, reasons, confirmed concepts and resulting work must remain connected. The owner should be able to inspect and answer a complete proposal on the Board, while agents can recover what was actually confirmed and follow it through delivery without reconstructing scattered chats or maintaining competing copies.

**The intended result**

The exact confirmed readback is preserved on its DQC with its confirmation source and scope. Earlier wording, owner corrections, reasons and confirmed versions remain recoverable. Pending revisions retain their own status and do not inherit earlier confirmation.

Chat and Board actions reach the same DQC records. When the owner finishes a round, the agent reviews every changed DQC, including answers and question-quality feedback; updates the Wiki and owning documents with confirmed and approved understanding; and either proceeds to authorized preparation or presents the next interview frontier. Unanswered questions and dependencies carry forward.

DQCs remain traceable through preparation, implementation, verification and delivery, including deferral, supersession and reopening affected understanding after correction. Execution state and proof remain in their execution owners. Concept confirmation, execution authorization, Review, Human QA and publication remain distinct.

The tracker is available in AMS and included in reusable setup-workbench support. The Board remains local and Python-based, with complete question readbacks replacing the current card-context restriction that prevents them.

**What I will do**

After confirmation, preserve this exact readback as the authoritative intent, establish the supported AMS tracker and initial DQCs, and carry the requested tracker and DQC-backed Board lifecycle through the project’s Map, Plan and implementation workflow. Add reusable tracker support in the setup-workbench source in the shared skills catalog, preserving unrelated work and existing source decisions except where this confirmed concept supersedes them.

Verify stable references in both directions, exact readback/history preservation, consistent chat and Board updates, round continuation, conflict refusal and persistence, and tracker availability through setup-workbench. Publish checked AMS non-site work under the standing publication authority. Shared-skill candidates retain their required qualification and delivery gates; changing the installed personal catalog requires separate explicit installation authority. Stop at verified delivery and report any incomplete checks or owner-only acceptance gates; do not claim Human QA or deploy the public website.</pre>

Source: workbench/wiki/context-grilling-board\.md@aa2467c181989e5ff58d14687e39bea57083d7d3\#jot-af34e4a9-efdf-4688-91d9-0c2d2b0685ba; Kayden direct confirmation, 2026-11-03. Scope: After confirmation, preserve this exact readback as the authoritative intent, establish the supported AMS tracker and initial DQCs, and carry the requested tracker and DQC-backed Board lifecycle through the project’s Map, Plan and implementation workflow\. Add reusable tracker support in the setup-workbench source in the shared skills catalog, preserving unrelated work and existing source decisions except where this confirmed concept supersedes them\.&#10;&#10;Verify stable references in both directions, exact readback/history preservation, consistent chat and Board updates, round continuation, conflict refusal and persistence, and tracker availability through setup-workbench\. Publish checked AMS non-site work under the standing publication authority\. Shared-skill candidates retain their required qualification and delivery gates; changing the installed personal catalog requires separate explicit installation authority\. Stop at verified delivery and report any incomplete checks or owner-only acceptance gates; do not claim Human QA or deploy the public website\..

Round: ams-concept-20261103. Dependencies: none.

- [landmark:LMK-001](workbench/landmarks/LMK-001-grill-board/LANDMARK.md) (room): Connect sourced concept coverage with its actual maintained execution owner; no execution state is inferred\.
- [spec:S-004](workbench/landmarks/LMK-001-grill-board/specs/S-004-grill-board-cards/SPEC.md) (room): Connect sourced concept coverage with its actual maintained execution owner; no execution state is inferred\.
- [task:S-004/TK-002H](workbench/landmarks/LMK-001-grill-board/specs/S-004-grill-board-cards/tasks/TK-002H/TASK.md) (room): Connect sourced concept coverage with its actual maintained execution owner; no execution state is inferred\.
- [task:S-004/TK-002I](workbench/landmarks/LMK-001-grill-board/specs/S-004-grill-board-cards/tasks/TK-002I/TASK.md) (room): Connect sourced concept coverage with its actual maintained execution owner; no execution state is inferred\.
- [task:S-004/TK-002K](workbench/landmarks/LMK-001-grill-board/specs/S-004-grill-board-cards/tasks/TK-002K/TASK.md) (room): Later corrective Task repairs generated Markdown whitespace while preserving exact confirmed intent and owner history\.

Expected result: The exact confirmed DQC lifecycle is traceable through supported tracker setup and the local Python Board, with source/history and distinct owner gates\. — workbench/landmarks/LMK-001-grill-board/specs/S-004-grill-board-cards/SPEC\.md.

Recorded outcome (r10): Implemented and delivered through AMS PR161, main merge 3fea0317a9bf7a138de5d06ea6e86b592c151572; independent Standards/Spec PASS on fd65917; required CI839 passed/6 skipped plus10 browser checks\. Reusable setup source PR68/69/70 merged and consumed with authentic package8c3b46b0\. Owner Human QA and Spec acceptance remain unperformed; installed personal catalog unchanged\..
- propose at r7
- confirm at r8: Recording the actual prior owner confirmation and its exact displayed readback, not simulating a new owner action\. Source reply: Confirmed\. And I thought we just fixed that so that you could push things to the github\.

## DQC-000B — What belongs on the Grilling Board

Revision 4; pending. [Record](workbench/landmark-tracker/destination-questions/DQC-000B.json)

<pre>**Summary**

The Board presents owner questions through DQCs; ordinary drafts and routine content are outside its owner frontier.

**The why**

Owner attention belongs on actual choices and requested judgments.

**The intended result**

This branch covers the settled scope in DQC-000A. It is source-linked agent context and requests no new confirmation.

**What I will do**

Preserve the confirmed concept and link actual execution owners; introduce a distinct DQC only for a genuinely new decision.</pre>

Source: Derived source-linked branch context from DQC-000A; workbench/wiki/context-grilling-board\.md@aa2467c181989e5ff58d14687e39bea57083d7d3\#jot-af34e4a9-efdf-4688-91d9-0c2d2b0685ba; Kayden direct confirmation, 2026-11-03. Scope: Agent coverage context for the already confirmed DQC-000A; no new owner decision or authorization\..

Round: ams-concept-20261103. Dependencies: DQC-000A.

- [dqc:DQC-000A](workbench/landmark-tracker/destination-questions/DQC-000A.json) (tracker): Connect sourced concept coverage with its actual maintained execution owner; no execution state is inferred\.
- [spec:S-004](workbench/landmarks/LMK-001-grill-board/specs/S-004-grill-board-cards/SPEC.md) (room): Connect sourced concept coverage with its actual maintained execution owner; no execution state is inferred\.
- propose at r4

## DQC-000C — Question and answer flow

Revision 4; pending. [Record](workbench/landmark-tracker/destination-questions/DQC-000C.json)

<pre>**Summary**

Each Board card projects a stable DQC and its full proposed readback. Confirmations bind exactly displayed content; correction and quality feedback preserve owner words.

**The why**

Chat and Board actions must reach the same owning records.

**The intended result**

This branch covers the settled flow in DQC-000A, preserving pending revision and confirmation boundaries. It is agent context.

**What I will do**

Use the supported native lifecycle and retain source/history; request no reconfirmation of this derived summary.</pre>

Source: Derived source-linked branch context from DQC-000A; workbench/wiki/context-grilling-board\.md@aa2467c181989e5ff58d14687e39bea57083d7d3\#jot-af34e4a9-efdf-4688-91d9-0c2d2b0685ba; Kayden direct confirmation, 2026-11-03. Scope: Agent coverage context for the already confirmed DQC-000A; no new owner decision or authorization\..

Round: ams-concept-20261103. Dependencies: DQC-000A.

- [dqc:DQC-000A](workbench/landmark-tracker/destination-questions/DQC-000A.json) (tracker): Connect sourced concept coverage with its actual maintained execution owner; no execution state is inferred\.
- [spec:S-004](workbench/landmarks/LMK-001-grill-board/specs/S-004-grill-board-cards/SPEC.md) (room): Connect sourced concept coverage with its actual maintained execution owner; no execution state is inferred\.
- propose at r4

## DQC-000D — Keeping intent current

Revision 4; pending. [Record](workbench/landmark-tracker/destination-questions/DQC-000D.json)

<pre>**Summary**

After a round, agents review every changed DQC, answer and quality event; reconcile actual confirmed and authorized knowledge, then record authorized preparation or the next frontier.

**The why**

Unanswered questions, dependencies and prior confirmed versions must remain recoverable.

**The intended result**

This branch covers currentness and continuation already settled in DQC-000A; execution proof stays in its owners. It requests no new owner answer.

**What I will do**

Preserve context/history and expose genuine new decisions separately, without inventing Human QA or acceptance.</pre>

Source: Derived source-linked branch context from DQC-000A; workbench/wiki/context-grilling-board\.md@aa2467c181989e5ff58d14687e39bea57083d7d3\#jot-af34e4a9-efdf-4688-91d9-0c2d2b0685ba; Kayden direct confirmation, 2026-11-03. Scope: Agent coverage context for the already confirmed DQC-000A; no new owner decision or authorization\..

Round: ams-concept-20261103. Dependencies: DQC-000A.

- [dqc:DQC-000A](workbench/landmark-tracker/destination-questions/DQC-000A.json) (tracker): Connect sourced concept coverage with its actual maintained execution owner; no execution state is inferred\.
- [spec:S-004](workbench/landmarks/LMK-001-grill-board/specs/S-004-grill-board-cards/SPEC.md) (room): Connect sourced concept coverage with its actual maintained execution owner; no execution state is inferred\.
- propose at r4

## DQC-000E — Finish the Workbench Dashboard in AMS

Revision 3; pending. [Record](workbench/landmark-tracker/destination-questions/DQC-000E.json)

<pre>## Summary

Finish the AMS Workbench Dashboard. The current Python Grilling Board becomes one section of it. I add three more sections, Destination Tracker, Taskboard and Wiki, by pulling the working code from LLM_Workbench's Dashboard into AMS. Everything looks like the Grilling Board Redesign artifact. Drafts to approve is left out.

## The why

You have asked for this Dashboard from the start, and a working one already exists in LLM_Workbench, so rebuilding it from scratch wastes time. You approve things on GitHub, so a Drafts section only adds backlog. AMS does not share code with other projects; the skills do. So the Dashboard is built here first and turned into skills later.

## The intended result

- `uv run ams-board` opens one local Dashboard on your machine, never on Vercel.
- The top bar has search and a light/dark switch. The tabs are Destination Tracker, Taskboard, Grilling Board and Wiki.
- Tracker, Taskboard and Wiki show AMS's own records and only display them.
- The Grilling Board keeps working as it does now.
- Every part looks like the Redesign artifact, and its controls, such as search and filters, really work.
- Nothing in AMS links back to or updates LLM_Workbench.

## What I will do

1. Copy the LLM_Workbench page code for the three sections into AMS and have the Python Board supply the data they need.
2. Style the whole Dashboard from the Redesign artifact. Where it does not draw a section, use its colors and parts.
3. Test it and show it to you in the browser.
4. Do the work on the S-004 branch and open a draft PR.

Then stop. Not included: Drafts to approve, turning the Dashboard into skills (the next job), the public website, and your Human QA.</pre>

Source: workbench/wiki/context-grilling-board\.md@75862efddf475ce3e4f57c25f4002bf625642c53\#jot-97b271e2-af5c-4901-a9ae-4f87fa65f759. Scope: Add Destination Tracker, Taskboard and Wiki sections and the Dashboard frame to the AMS Python Board in the Redesign look; S-004 branch and draft PR; stop before skills, Drafts, website and Human QA.

Round: dashboard-round-1. Dependencies: none.

- propose at r2
