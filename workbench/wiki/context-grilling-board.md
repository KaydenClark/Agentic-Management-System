---
type: project
status: partial
sensitivity: normal
knowledge_role: curated
provenance:
  - /jot capture; each claim names its source and date
source_paths: []
last_verified: 2026-11-04
---

# Grilling Board and DQC-backed intent

Captured context. Claim labels preserve intent and uncertainty; capture alone supplies neither Canon nor implementation proof. The date above checks this page's capture format, not every claim.

<!-- jot-entry -->
### JOT-e26f9c60-59ef-4f8f-8fe4-80bab6b41029
Kind: observation
State: current
Recorded: 2026-11-04T01:54:58.535Z
Author: Codex
Source: Kayden AMS align-concept chat, 2026-11-03; LLM_Workbench DQC-007B at 9d5e1f25b0d5870589ae1c5752f27f42acb796ef
Topic: grilling-board
Supersedes: none

## Purpose and source status

Recovered on 2026-11-03 America/Denver for Kayden's align-concept session about the existing Grilling Board. This is source-backed knowledge capture and a pending alignment synthesis, not a new confirmed readback, implementation instruction, board answer, Human QA, or acceptance. The four investigation branches are purpose, what belongs there, question/answer flow, and keeping the board current. Kayden additionally requested: "Make sure you find out and capture how DQCs are supposed to be used to carry the info on the board and keep it updated."

Reference: LLM_Workbench integration source at 9d5e1f25b0d5870589ae1c5752f27f42acb796ef. The live GitHub integration DQC-007B and tools/grill-board.mjs were fetched through the GitHub connector and exactly matched that pinned source. The local producer checkout is behind its tracking ref and dirty; it was preserved and not used as the current implementation baseline.

## What the board is and what belongs there

The Grilling Board presents the owner's current questions and reviews, with enough context to answer without a treasure hunt. LLM_Workbench's larger Workbench Dashboard includes Destination Tracker, Taskboard, Grilling Board, Drafts to approve, and Wiki; those sections read their existing owners rather than becoming a new authoritative tracker. Do not infer that every Dashboard feature is already an AMS requirement.

Items include owner gates, open decisions, unsettled Destination Question Cards (DQCs), decision-record text and page/text reviews. Questions have stable identities, topic context, current understanding, an explicitly labeled agent proposal, reasons, consequences, sources, and exact proposed text where wording is being approved. Existing answers must be recovered before asking again; an unanswered Board item does not establish that the underlying choice was never answered.

Questions are grouped by topic. Priority and Value are separate signals with source-backed reasons; neither combines into a score. Questions support a 1-5 quality rating and a separate Too taxing signal. Comments, ratings, and notes do not create confirmation or implementation authority.

## Confirmed DQC-backed model: the information owner

The governing recovered intent is [DQC-007B: How should DQC-backed grilling preserve confirmed intent across chat, website buttons and Wiki?](https://github.com/KaydenClark/LLM_Workbench/blob/9d5e1f25b0d5870589ae1c5752f27f42acb796ef/workbench/landmark-tracker/destination-questions/DQC-007B.json). Its answer retains the full confirmed readback, its original response digest, source lineage, and the exact owner confirmation: "Yes, confirmed. Capture this in the DQCs and wiki. This is going to be the first thing we test through the audit workbench." Link to that retained source rather than replace it with this summary.

A DQC carries the evolving question/concept and its intent history. Every grilling question is backed by a named DQC and revision. Its displayed question, current confirmed concept, proposed change, reasons and history come from that record. Board card identity is not a substitute for DQC identity.

Synthesis may evolve. Each confirmed version stays recoverable word for word. Preserve previous value, replacement, exact owner correction, stated reason, source and confirmation scope. If no reason was supplied, record "reason not supplied"; do not supply an inferred owner reason. Individual answers and pending corrections do not silently confirm a newly assembled readback. A pending revision cannot inherit an older version's confirmation.

The original grilling sources remain. DQCs synthesize related conceptual questions with their lineage; not every conversational prompt requires its own DQC. A DQC can exist without a Landmark. Specs organize confirmed intent into requirements and acceptance while linking back to exact source wording; Landmarks organize broader scope when useful. None substitutes for retained intent history.

## Board, terminal and round update flow

Both chat/terminal activity and Board actions must reach the same DQC through the same validated owning operations.

- Confirm records the exact displayed proposal against its displayed DQC revision.
- Rework wording, Change the why, and Change record the owner's exact words with the correct status. A correction needing agent interpretation remains pending while the revised synthesis is prepared for confirmation.
- Every grilling round updates the affected DQCs and the Wiki, whether the interview happens in chat or on the website. Jot may aid capture; it is not a mandatory intermediary or substitute for the DQC.
- The Wiki explains the resulting understanding and links to the exact DQC revisions used. The Board rereads those updated records. A terminal change and a website change must be visible through the same reader, without separately rewriting a second copy of the question.
- Preserve stable identity, prior confirmed versions, corrections, reasons, unresolved work and source lineage across reloads and restarts.
- Retry must not duplicate a change. Stale browser/agent writes and competing revisions must refuse rather than silently overwrite current data.

Answer state, confirmation, application, publication, implementation and Human QA remain distinct. The producer's current statuses include Pending, Re-answer, Answered and Applied. Its apply operation records where an agent already carried the actual answer; that receipt alone does not perform the owning-record update. Decision publication requires its scoped authorization; ending a round or confirming wording does not automatically dispatch implementation.

## Actual producer implementation and limits

At the pinned source, tools/grill-board.mjs mergeBoard reads independent items.json plus owner answers. Its decision operation records Board answer snapshots, while applyAnswer records application bookkeeping. tools/dashboard-workflow.mjs endRound records confirmed Board identities/revisions, with no DQC or Wiki write. This is the disconnected mechanism identified by the earlier diagnosis retained in DQC-007B; it is not evidence that the confirmed DQC-backed design has been delivered.

The existing page polls every 15 seconds and offers reload when items change, preserving in-progress owner typing. This is freshness detection for Board items, not a DQC-backed reader. The reusable project component also requires agents to add/revise items through supported tools; it does not discover every pending owner question automatically.

Fresh isolated tests of the exact pinned source: tools/test-grill-board.mjs passed 25/25 with loopback access. The first sandboxed run passed 21 and could not run 4 HTTP cases because listen was denied; the permitted retry passed all 25. These are component checks, not proof of DQC/Wiki synchronization, rendered owner usability, or AMS acceptance.

## AMS comparison and unresolved verification

The inspected AMS checkout serves committed Markdown cards. Its existing S-004 acceptance evidence does not establish DQC-backed questions or round-to-Wiki updates. The separate in-progress Python queue candidate uses explicit owner-request blocks, stable keys and versioned wording in committed owning records; that work must be preserved and assessed on its own candidate. This inspection found no DQC connection in that candidate's Board module. It has not been exercised against the full recovered DQC contract in this session.

AMS also excludes full drafts from card Context while the producer supports complete proposed wording and linked drafts. Resolve this difference against AMS's established source decisions before treating it as a repair instruction. Preserve Python and the owner's requirement for current items without a manual update request.

Observable proof needed to establish the DQC connection: a real DQC-backed question displays the named revision; Board action and equivalent terminal action update the same record/history; prior confirmed words and reasons remain exact; the completed round's Wiki links read back correctly; the Board shows the resulting current/pending state; stale/repeated writes and restart preserve data. These are recovered verification criteria, not a new implementation plan.

Next alignment step: present the recovered model for owner correction/confirmation, then identify actual AMS divergences against that confirmed meaning. This session has no repair, migration, installation, live owner-answer write, Spec completion, or deployment authority.

## Supporting sources

- [Producer Board README](https://github.com/KaydenClark/LLM_Workbench/blob/9d5e1f25b0d5870589ae1c5752f27f42acb796ef/workbench/grill-board/README.md) and its linked answer-controls, question-feedback, ownership, P/V, owner-use and batch-processing pages.
- [Confirmed grilling context](https://github.com/KaydenClark/LLM_Workbench/blob/9d5e1f25b0d5870589ae1c5752f27f42acb796ef/workbench/wiki/context-workbench-grilling.md), including JOT-43f8ec8b, JOT-f260b50a and JOT-d364d2cd.
- [Reusable project Board](https://github.com/KaydenClark/LLM_Workbench/blob/9d5e1f25b0d5870589ae1c5752f27f42acb796ef/workbench/docs/project-grill-board.md).
- [AMS Board](../../grill-board/README.md), [Grill Board Landmark](../landmarks/LMK-001-grill-board/LANDMARK.md), and [S-004](../landmarks/LMK-001-grill-board/specs/S-004-grill-board-cards/SPEC.md).
<!-- /jot-entry -->
