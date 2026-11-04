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

<!-- jot-entry -->
### JOT-aa694f42-e43c-4eb7-9aea-e3e63d57ba36
Kind: intent
State: current
Recorded: 2026-11-04T02:12:38.416Z
Author: Kayden
Source: Kayden, AMS align-concept lifecycle correction, 2026-11-03
Topic: grilling-board
Supersedes: none

## Owner correction: DQCs own the interview from its beginning

Source: Kayden, AMS align-concept chat, 2026-11-03 America/Denver. The following is the exact owner correction, not an agent paraphrase or confirmation of a new assembled readback:

> This describes a good part of it, but doesn't get the whole story.  The DQCs are supposed to be where all of the intent and questions are initially recorded, so like at the start of this align concept you would of created the 4 DQCs for the 4 main branches on the interview tree. and after we align on each concept, and you give me the readback to confirm, its the readback that is stored onto the DQC since that is the concept that I confirmed and aligned. and then as we adjusted the interview tree you edit the DQC, chaning the why and the answer, or creating new DQCs when a new decision needs to be made form a different question. Each card on the grilling board is a DQ Card. When I saw I am done with a grilling board round, then you should review all of the DQCs cards that got changed by me pushing buttons on the website, and then update the project's wiki and docs with any confirmed and approved concepts, start the prepare phase with a map and plan, or just update the DQCs with the next round for me after I tell you I am done so I can go right back to answering them.

This expands the incomplete lifecycle description in JOT-e26f9c60-59ef-4f8f-8fe4-80bab6b41029. Preserve the earlier source investigation and evidence limits; its summary is not the complete owner model.

## Current interpretation for the next readback

DQCs are the initial home for intent and questions, not merely records produced after an interview or linked to independent Board cards. For this interview the four main tree branches should have four initial DQCs. Each Grilling Board card is a view of its DQC. As the tree evolves, update the existing DQC's question, why and developing answer, retaining history; create another DQC when a distinct question introduces a new decision.

After alignment on a concept, present its readback for owner confirmation. The exact confirmed readback is stored on that DQC as the concept actually confirmed, with source, scope, confirmation and prior revisions preserved. Tentative answers, corrections and proposed readbacks must retain their own state; do not treat them as confirmation of a newly assembled concept.

The owner's statement that a Board round is finished triggers the agent's review of all DQCs changed through the website. Reconcile the confirmed and approved concepts into the project's Wiki and appropriate documents, proceed to Prepare through Map and Plan where covered by existing approval, or update DQCs for the next interview round so the owner can return to answering. Round completion is not merely an archival count of button clicks. Implementation still needs its applicable authorization. This interpretation awaits confirmation as an assembled readback.

## Verified AMS recording limitation

The supported command `node workbench/tools/landmark-tracker.mjs show --json` currently refuses with code `tracker-undeclared`: the room declares no Landmark Tracker root. No DQCs were created in this session. The Wiki capture is a recoverable holding record, not a substitute DQC system or proof that the intended lifecycle is available. Restoring the supported DQC capability is a Workbench setup operation; this correction capture does not silently change the manifest, create a hand-built tracker, repair the Board, or claim publication.

Publication approval asked earlier remains unanswered; this correction is not approval to push the branch or merge it.
<!-- /jot-entry -->

<!-- jot-entry -->
### JOT-a1064eef-0239-494e-9fa1-387a68d3529d
Kind: proposal
State: unresolved
Recorded: 2026-11-04T02:18:31.649Z
Author: Codex
Source: Kayden AMS align-concept chat, save request and pending readback, 2026-11-03
Topic: grilling-board
Supersedes: none

## Owner feedback and continuation, 2026-11-03

Kayden said: "This is sounding a lot better, we are almost there. Save this and why are we getting this error? You are the only session running righ tnow"

Save the latest four-section readback as pending, alongside the exact lifecycle correction in JOT-aa694f42-e43c-4eb7-9aea-e3e63d57ba36. This is positive alignment feedback and an explicit save request, not final confirmation of the assembled readback or permission to publish the branch. Next: continue from the DQC-first lifecycle and clarify any remaining meaning; do not restart settled questions.

## Pending readback preserved exactly

**Summary**

At the start of alignment, the main interview branches become DQCs—four initial DQCs for this session’s four branches. Each card on the Grilling Board **is a DQ Card**, displaying that record’s current question, why, developing answer and confirmation state.

As the interview tree changes, existing DQCs evolve with it. A distinct question requiring another decision creates a new DQC. Earlier wording, answers, corrections and reasons remain recoverable.

**The why**

The interview, board and recorded intent must remain connected throughout alignment. Otherwise, agents reconstruct understanding from scattered conversations, and the board becomes stale or disconnected from what was actually confirmed.

**The intended result**

After alignment on each concept, the agent presents a readback. **The exact readback you confirm is stored on its DQC as the confirmed concept.**

When you say a board round is finished, the agent reviews every DQC changed through your website actions and takes the appropriate continuation:

- Update the Wiki and owning documents with confirmed and approved concepts.
- Begin Prepare with Map and Plan where authorized.
- Update the DQCs with the next questions and proposals so you can immediately resume answering.

That round review carries understanding forward; it does not merely count completed answers.

**What I will do**

I’ve preserved your exact correction in the [existing capture](context-grilling-board.md), committed locally as `59bcbff`. This assembled readback remains pending your confirmation.

AMS currently refuses the supported DQC operation with `tracker-undeclared`. Consequently, the four initial DQCs do **not** exist yet; the Wiki capture preserves the correction while that capability is unavailable. Nothing has been published.

Preservation note: the original chat's machine-local Markdown link target was normalized to this Wiki page's relative path; visible readback text is unchanged.

## Error investigation

No index.lock or HEAD.lock exists in the inspected AMS checkout. The Git save hook runs because the branch has commits absent from remote-tracking refs, not because another session holds a lock. Its stop operation calls unpushed for the entire HEAD after HEAD changes from the session baseline, so its count also includes earlier unpushed commits on this branch. The other-worktree warning inventories dirty worktrees; it does not establish active sessions.

The actual push was rejected before Git ran by automatic approval review for insufficient explicit authorization to disclose the branch's documentation/project context to the public repository. The save hook's instruction to push does not override that review. No retry or workaround is authorized by this diagnosis.

The separate DQC error, tracker-undeclared, is a manifest/configuration gap, also unrelated to concurrent sessions. Existing data, pending confirmation and blocked publication remain preserved. No hook, security setting, manifest or Board code was changed by this capture.
<!-- /jot-entry -->

<!-- jot-entry -->
### JOT-d24d46bd-7ca5-44e0-854e-0411e4fbff30
Kind: intent
State: confirmed
Recorded: 2026-11-04T02:44:40.440Z
Author: Kayden
Source: Kayden direct AMS chat, standing public-publication authorization and merge instruction, 2026-11-03
Topic: grilling-board
Supersedes: none

## Standing public-publication authorization

Kayden explicitly adopted the following standing instruction in the AMS chat, 2026-11-03 America/Denver, then directed: "And then merge the PRs that have been getting flagged in this chat".

> For AMS, I authorize routine publication of project source, documentation, DQCs and Wiki records—including captured project questions, corrections, and pending or confirmed readbacks—to the public KaydenClark/Agentic-Management-System repository. Preserve each record’s confirmation state. Push feature branches and merge checked non-site PRs into main without asking again. Private answer stores, ignored files, credentials, private research and raw transcripts remain excluded. Website dev-to-main promotion remains mine.

This grants the stated publication and checked non-site merge scope. It does not confirm the pending Grilling Board concept readback, approve Human QA, activate implementation of the DQC lifecycle, or authorize website dev-to-main promotion. Earlier publication-hold entries remain historical; their missing explicit public-disclosure authorization is resolved by this owner statement. The requested current delivery includes this documentation branch and the eligible PRs actually raised in this chat, preserving each existing target and any failed checks or product-acceptance limits.
<!-- /jot-entry -->
