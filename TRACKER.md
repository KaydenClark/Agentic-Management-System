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

## DQC-000E — RSI: Coverage

Revision 6; confirmed. [Record](workbench/landmark-tracker/destination-questions/DQC-000E.json)

<pre>**Question:** Should shared skill reporting work from any project and environment, independently of whether GPT_OS is present?

**Recommended answer:** Yes. Provide one reusable reporting tool that participating skills can call from their current environment. GPT_OS may install or configure it, but neither the project nor the reporting tool must run inside GPT_OS. The repair worker runs separately on Servitor.

**Why:** Your skills operate across independent projects, machines and cloud environments. Tying reporting to one checkout would leave gaps and constrain how you work.

**Intended impact:** You continue working in the project you choose. Its skill failures reach the same shared history and repair queue without relocating the project or requiring a full GPT_OS installation.</pre>

Source: Kayden AMS alignment chat, 2026-11-06; exact displayed readbacks and owner corrections\.. Scope: Concept alignment only; no implementation, installation, database writes, campaign launch or deployment\..

Round: rsi-cross-project-20261106. Dependencies: none.

- propose at r2
- confirm at r3: Yes, Because of this we need to be very smart about how we do this\. Can we create something that we can have in GPT\_OS \(that is on both Mac and PC, and can be created as an environment for the cloud\) that would allow us to send info back to supabase? Do we need to send info back or can supabase collect it from github as long as the projects as pushing back to Kaydenclark/skills?
- propose at r4
- propose at r5
- confirm at r6: Yes, that's what I mean\. It should work from any project on my Mac, PC, or in the cloud without requiring GPT\_OS\. Let's move to question 2\.

## DQC-000F — RSI: Run boundaries

Revision 3; needs-rewrite. [Record](workbench/landmark-tracker/destination-questions/DQC-000F.json)

<pre>**Question:** What counts as one skill use, and when is it finished?

**Recommended answer:** One requested operation is one use, with linked child skill uses. Preserve its identity across pauses and resumed chats. Record completion, cancellation, interruption and reopening separately.

**Why:** I chose these boundaries without asking. Counting chats or file reads as uses would distort outcomes and recurrence.

**Intended impact:** Determines run counts, attribution, completion triggers and recovery behavior.</pre>

Source: Kayden AMS chat, 2026-11-06: align-concept request for cross-project RSI; first-pass question tree and Question / Recommended answer / Why / Intended impact readbacks\.. Scope: Meaning-only first-pass alignment\. Recommendations are pending, not owner-confirmed\. No implementation, trials, installation, database writes or merge-rule changes\..

Round: rsi-cross-project-20261106. Dependencies: DQC-000E.

- propose at r2
- correct at r3: When me, you \(codex\), or claude uses one of the workbench skills that we are doing RSI on\. we should log the failures and run the RSI loop on it\. The benefits of an RSI loop is that its recorded and can be started as soon as its logged in the system as needing to be fixed\.

## DQC-000G — RSI: Success and failure

Revision 3; needs-rewrite. [Record](workbench/landmark-tracker/destination-questions/DQC-000G.json)

<pre>**Question:** Who decides whether real work succeeded, and what failures must be captured?

**Recommended answer:** Use the requested outcome, observable checks and your corrections. Capture problems during work and discoveries afterward; allow success with recorded friction. Keep unknown outcomes explicit and diagnose cause before blaming a skill.

**Why:** A final agent message or a failed command alone cannot judge the whole job. Automatic capture cannot detect every semantic failure.

**Intended impact:** Makes real owner-requested work first-class evidence without inventing success or assigning every problem to a skill.</pre>

Source: Kayden AMS chat, 2026-11-06: align-concept request for cross-project RSI; first-pass question tree and Question / Recommended answer / Why / Intended impact readbacks\.. Scope: Meaning-only first-pass alignment\. Recommendations are pending, not owner-confirmed\. No implementation, trials, installation, database writes or merge-rule changes\..

Round: rsi-cross-project-20261106. Dependencies: DQC-000F.

- propose at r2
- correct at r3: I do when I use the skills\. I tell you when things fail, you record the failures\. That is what I want us to be able to look at\. How do we maintain a per skill failure log that we can use for regression testing\. When a skill fails at something it is supposed to do, it needs to be logged somewhere\. Is that is Kaydenclark/skills? Is that is GPT\_OS? It should not be in the project where we were doing the updates \(unless that project is GPT\_OS because that is our orchestrator project and can be used like that\)

## DQC-000H — RSI: Evidence and privacy

Revision 3; needs-rewrite. [Record](workbench/landmark-tracker/destination-questions/DQC-000H.json)

<pre>**Question:** What may leave each project, what stays private, and what may the public website show?

**Recommended answer:** Share version identities, safe outcome/failure summaries and evidence references. Keep raw transcripts and private project material at their authorized source. Separate private shared records from public-safe presentation; decide retention and remote access for repair evidence explicitly.

**Why:** I assumed local-only raw evidence and public-safe summaries. That affects whether another machine can reproduce and repair a finding.

**Intended impact:** Sets the data boundary, retention expectations and the evidence available to remote repairs.</pre>

Source: Kayden AMS chat, 2026-11-06: align-concept request for cross-project RSI; first-pass question tree and Question / Recommended answer / Why / Intended impact readbacks\.. Scope: Meaning-only first-pass alignment\. Recommendations are pending, not owner-confirmed\. No implementation, trials, installation, database writes or merge-rule changes\..

Round: rsi-cross-project-20261106. Dependencies: DQC-000E, DQC-000G.

- propose at r2
- correct at r3: For the website, I just want the results We should log the fitness level, alignment score, model tier, and provider used for each run\. So if we had 4 runs of the RSI loop to get the skills to a passing excellent state, I want to see that\. The website is supposed to show hundreds of tests, no single test result\. We are showing improvements over time, not run results\. How have skills X, Y, Z, A, B, C improved over the last 500 runs? Are we getting better at making skills? Is this a worth while effort? Are we having less errors over time when I run them? Are they doing what we designed them to do? Is the system working? That is what the tests are supposed to show\. None of that should be conflicting with privacy\. The Agentic Management system is open Source\. My skills repo is only private so we can keep private info on there, my skills themselves are not private, they are open source\. The website is to show them off\.

## DQC-000I — RSI: Recording authority

Revision 3; needs-rewrite. [Record](workbench/landmark-tracker/destination-questions/DQC-000I.json)

<pre>**Question:** Should Supabase own the shared lifecycle while project feedback logs retain local failure intake?

**Recommended answer:** Yes. Keep one linked lifecycle in Supabase; reference original project failure IDs and corrections. Queue evidence locally until receipt is verified, preserving original event times and preventing duplicates.

**Why:** This preserves the existing ownership model, but I assumed it also fits ordinary skill uses and projects before setup.

**Intended impact:** Prevents competing histories and silent evidence loss during outages or cloud teardown.</pre>

Source: Kayden AMS chat, 2026-11-06: align-concept request for cross-project RSI; first-pass question tree and Question / Recommended answer / Why / Intended impact readbacks\.. Scope: Meaning-only first-pass alignment\. Recommendations are pending, not owner-confirmed\. No implementation, trials, installation, database writes or merge-rule changes\..

Round: rsi-cross-project-20261106. Dependencies: DQC-000F, DQC-000H.

- propose at r2
- correct at r3: I am not sure if supabase should own the lifecycle of Kaydenclark/skills\. I need you to be the expert and find out the best system for me\.

## DQC-000J — RSI: Capture and transport

Revision 3; needs-rewrite. [Record](workbench/landmark-tracker/destination-questions/DQC-000J.json)

<pre>**Question:** Should we use a shared observer with host adapters and a restricted upload endpoint, or require logging inside each skill?

**Recommended answer:** Use a shared observer once per participating harness, integrated with setup-workbench for project identity. Prefer supported host events; add explicit lifecycle calls where observation is incomplete. Use restricted authenticated ingestion; leave the exact packaging and endpoint technology open until feasibility is checked.

**Why:** I selected an observer and Supabase Edge Function too early. The requirement is reliable capture with bounded access; the exact technology remains a proposal.

**Intended impact:** Avoids duplicating logging instructions across skills and makes unsupported capture paths visible.</pre>

Source: Kayden AMS chat, 2026-11-06: align-concept request for cross-project RSI; first-pass question tree and Question / Recommended answer / Why / Intended impact readbacks\.. Scope: Meaning-only first-pass alignment\. Recommendations are pending, not owner-confirmed\. No implementation, trials, installation, database writes or merge-rule changes\..

Round: rsi-cross-project-20261106. Dependencies: DQC-000E, DQC-000H, DQC-000I.

- propose at r2
- correct at r3: I think requiring loggin in each  skill would be easier, but again, I need you to be the expert, tell me what would actually be best\. What do I have set up? What does the research and our CDRs tell us to do?

## DQC-000K — RSI: Repair triggers and priority

Revision 3; confirmed. [Record](workbench/landmark-tracker/destination-questions/DQC-000K.json)

<pre>**Question:** When should findings become repair work, and may repairs run while your original task continues?

**Recommended answer:** Capture immediately; normally queue diagnosis after completion or interruption. Group related failures without erasing occurrences. Keep your active work moving; surface urgent blockers promptly. Do not silently repair an installed skill during its current use.

**Why:** I assumed automatic queuing after a use and background processing, without settling urgency, interruption or priority with you.

**Intended impact:** Controls when the loop acts and how it competes with useful project work.</pre>

Source: Kayden AMS chat, 2026-11-06: align-concept request for cross-project RSI; first-pass question tree and Question / Recommended answer / Why / Intended impact readbacks\.. Scope: Meaning-only first-pass alignment\. Recommendations are pending, not owner-confirmed\. No implementation, trials, installation, database writes or merge-rule changes\..

Round: rsi-cross-project-20261106. Dependencies: DQC-000G, DQC-000I.

- propose at r2
- confirm at r3: I like your recommended answer\. Capture into Kaydenclark/skills or supabase, then then fix when we are done, or at a designated time\.

## DQC-000L — RSI: Worker location and resources

Revision 3; needs-rewrite. [Record](workbench/landmark-tracker/destination-questions/DQC-000L.json)

<pre>**Question:** Where should repair and evaluation run, and what resource use can continue without asking?

**Recommended answer:** Start with the existing local Python-worker direction and subscription harnesses, using the established model/attempt limits. Make offline or unavailable workers visible. Choose the actual machine, scheduling, concurrency and any cloud execution explicitly; add no paid service by inference.

**Why:** A hosted database does not execute repairs. I assumed a local worker without establishing which host is reliably available.

**Intended impact:** Determines availability, compute authority, scheduling and practical throughput.</pre>

Source: Kayden AMS chat, 2026-11-06: align-concept request for cross-project RSI; first-pass question tree and Question / Recommended answer / Why / Intended impact readbacks\.. Scope: Meaning-only first-pass alignment\. Recommendations are pending, not owner-confirmed\. No implementation, trials, installation, database writes or merge-rule changes\..

Round: rsi-cross-project-20261106. Dependencies: DQC-000H, DQC-000J, DQC-000K.

- propose at r2
- correct at r3: On Servitor, using the AMS Website project to prove things work\. It should be tested on real work\.

## DQC-000M — RSI: Repair scope and pruning

Revision 3; needs-rewrite. [Record](workbench/landmark-tracker/destination-questions/DQC-000M.json)

<pre>**Question:** What may a repair change, and what does pruning a skill mean?

**Recommended answer:** Diagnose the owning cause first. Simplify or remove instructions only when evidence supports it, preserving requirements and provenance. Allow shared-skill and produced-Workbench repairs within their assigned scope; route unrelated product defects and third-party changes to their owners.

**Why:** I assumed the smallest repair was preferred, but pruning must not become automatic shortening or uncontrolled changes to every project.

**Intended impact:** Defines repair boundaries and protects useful behavior while reducing avoidable complexity.</pre>

Source: Kayden AMS chat, 2026-11-06: align-concept request for cross-project RSI; first-pass question tree and Question / Recommended answer / Why / Intended impact readbacks\.. Scope: Meaning-only first-pass alignment\. Recommendations are pending, not owner-confirmed\. No implementation, trials, installation, database writes or merge-rule changes\..

Round: rsi-cross-project-20261106. Dependencies: DQC-000G, DQC-000K.

- propose at r2
- correct at r3: "What does a pruning skill mean" is a scary question\. Its our pruning skill\. The one I had us create to replace the duplicated process in author skill and writing for agents\. This is how we create skills\. We use '/author-skill, add it everything we need to make it work, prune it using the '/prune skill we made, and then run it through the regression audit\. each run gets an alignment score on the rubric, and the whole skill gets a fitness level grade between broken and excellent and an alignment score based on those 3 runs\. We log the result for the RSI loop, its failures, etc\. And then run it again where we author skill, prune and run it through the regression audit until we get a stable or excellent skill that passes the alignment score, and doesn't fail any more of the failures we have recorded \(regressed\)

## DQC-000N — RSI: Fitness, Alignment and regression

Revision 3; needs-rewrite. [Record](workbench/landmark-tracker/destination-questions/DQC-000N.json)

<pre>**Question:** How should real uses, regression cases and grading combine to qualify a repaired skill?

**Recommended answer:** Record real work as observed-use evidence, preserve its findings as development/regression cases, and use independent evaluators with the existing r1 rules. Require accepted Stable/Excellent assessment, useful benefit and no disqualifying regression; state the evaluated scope and hosts.

**Why:** Real work shows value directly. Controlled comparisons and regression checks protect that value; one real run cannot stand in for unperformed grading runs.

**Intended impact:** Defines qualification without devaluing real work, hiding failures or claiming untested cross-host fitness.</pre>

Source: Kayden AMS chat, 2026-11-06: align-concept request for cross-project RSI; first-pass question tree and Question / Recommended answer / Why / Intended impact readbacks\.. Scope: Meaning-only first-pass alignment\. Recommendations are pending, not owner-confirmed\. No implementation, trials, installation, database writes or merge-rule changes\..

Round: rsi-cross-project-20261106. Dependencies: DQC-000G, DQC-000M.

- propose at r2
- correct at r3: Audits against failures to be able to complete new work without recreating the failure\.

## DQC-000O — RSI: Conditional merge authority

Revision 3; confirmed. [Record](workbench/landmark-tracker/destination-questions/DQC-000O.json)

<pre>**Question:** Should qualifying skill repairs merge automatically under your stated Stable/Excellent approval, and what must the gate verify?

**Recommended answer:** Yes. Encode your conditional approval for the exact assessed candidate, linked stored evidence, accepted qualification, benefit/regression requirements and repository checks. Preserve existing stopped work and attempt limits. Do not add another routine permission request; changed candidates need matching evidence.

**Why:** You explicitly described conditional merge approval. I proposed GitHub enforcement, but its exact scope and evidence requirements need alignment.

**Intended impact:** Turns the approval into an enforceable delivery rule rather than a reminder or a self-reported grade.</pre>

Source: Kayden AMS chat, 2026-11-06: align-concept request for cross-project RSI; first-pass question tree and Question / Recommended answer / Why / Intended impact readbacks\.. Scope: Meaning-only first-pass alignment\. Recommendations are pending, not owner-confirmed\. No implementation, trials, installation, database writes or merge-rule changes\..

Round: rsi-cross-project-20261106. Dependencies: DQC-000I, DQC-000N.

- propose at r2
- confirm at r3: Yes, they are authorize to merge\. the orchestrator merges them\. Or who ever is fixing the skill\. its part of completing it\. merging it into main and cleaning up the branch you left behind\.

## DQC-000P — RSI: Sharing accepted versions

Revision 3; needs-rewrite. [Record](workbench/landmark-tracker/destination-questions/DQC-000P.json)

<pre>**Question:** After merge, should participating machines update automatically, on startup, or only when you request it?

**Recommended answer:** Offer an explicit enrollment policy for checked updates between uses, with pinned versions for active work, preservation of local edits and a rollback path. Record installed and actually loaded versions. Choose the update timing and enrollment scope with you.

**Why:** I assumed a distribution policy without your direction. Merging shared source does not make a repaired version available in every environment.

**Intended impact:** Determines how improvements reach your work and how later use can establish whether the repair held.</pre>

Source: Kayden AMS chat, 2026-11-06: align-concept request for cross-project RSI; first-pass question tree and Question / Recommended answer / Why / Intended impact readbacks\.. Scope: Meaning-only first-pass alignment\. Recommendations are pending, not owner-confirmed\. No implementation, trials, installation, database writes or merge-rule changes\..

Round: rsi-cross-project-20261106. Dependencies: DQC-000E, DQC-000O.

- propose at r2
- correct at r3: We should either have something automated, or that I can run that just updates the skills\.

## DQC-000Q — RSI: Website and completion proof

Revision 3; needs-rewrite. [Record](workbench/landmark-tracker/destination-questions/DQC-000Q.json)

<pre>**Question:** What must the website show, and what evidence makes this shared loop complete?

**Recommended answer:** Show each skill and the Workbench it produces, real uses, failures, repair history, rejected attempts, grades, version adoption and later recurrence from canonical safe records. Show freshness and coverage. Prove one complete real-work loop, then verify the promised Mac, PC and cloud paths before claiming that coverage.

**Why:** I assumed a setup-workbench pilot and specific views. You established the website as the evidence surface for AMS; its exact presentation and completion standard remain choices.

**Intended impact:** Defines visible accountability and prevents a working demo or successful upload from being reported as a complete RSI loop.</pre>

Source: Kayden AMS chat, 2026-11-06: align-concept request for cross-project RSI; first-pass question tree and Question / Recommended answer / Why / Intended impact readbacks\.. Scope: Meaning-only first-pass alignment\. Recommendations are pending, not owner-confirmed\. No implementation, trials, installation, database writes or merge-rule changes\..

Round: rsi-cross-project-20261106. Dependencies: DQC-000I, DQC-000N, DQC-000P.

- propose at r2
- correct at r3: It should show the run history, how has each improvement run gone? Does a stable version have less failures? I honestly dont know what to show here\. Its probably part of why this RSI Loop is not set up\.
