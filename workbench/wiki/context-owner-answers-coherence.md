---
type: project
status: partial
sensitivity: normal
knowledge_role: curated
provenance:
  - /jot capture; each claim names its source and date
source_paths:
  - AGENTS.md
  - RUNBOOK.md
last_verified: 2026-11-02
---

# Owner answers to coherence findings

Captured context. Claim labels preserve intent and uncertainty; capture alone supplies neither Canon nor implementation proof. The date above checks this page's capture format, not every claim.

## Cleanup responsibilities, 2026-11-02

The [owner correction](#jot-fdaea0bd-5afa-4a88-ad43-dc8b41656c17) established cleanup, shared CI, delivery and recovery obligations. Following the [2026-11-03 document-ownership correction](context-workbench-adoption.md#jot-9abd9e46-08ae-4283-a950-a96e6095759f), [RUNBOOK](../../RUNBOOK.md#delivery-and-recovery) owns their procedures. [RUNBOOK Clean up](../../RUNBOOK.md#clean-up) owns the actions after Test And Build: inspect owned state, publish and verify the authorized target, remove contained temporary scaffolding, and leave clean owned checkouts with explicit retained items or blockers. Earlier merge authority and recovery protections remain.

<!-- jot-entry -->
### JOT-eadaca6e-98eb-4872-bfbc-fdaf9c3a4b06
Kind: intent
State: confirmed
Recorded: 2026-11-01T13:44:15.011Z
Author: Kayden
Source: Owner message to orchestrator C, 2026-11-01 (cloud session), answering COH-005, COH-006 and COH-016
Topic: owner-answers-coherence
Supersedes: none

COH-005 merges: The owner does not approve every merge. Agents merge non-site work into main themselves, so other agents always have the most current project. The owner approves only website merges from dev into main. ADR-002O and ADR-002F said otherwise and are wrong. Owner: 'Please Please Please do not make me approve every merge.'
<!-- /jot-entry -->

<!-- jot-entry -->
### JOT-33cf0369-9c98-44ed-a480-a93e63b49a81
Kind: intent
State: confirmed
Recorded: 2026-11-01T13:44:24.850Z
Author: Kayden
Source: Owner message to orchestrator C, 2026-11-01 (cloud session), answering COH-005, COH-006 and COH-016
Topic: owner-answers-coherence
Supersedes: none

COH-006 secret location: The owner delegated the call: store the Supabase service key where it belongs and fix the records. Resolution: the service role key lives only in the gitignored local env file in the owner's main checkout (ADR-003C), never in the repository or in Vercel; the public site only reads Supabase (DDR-000O), so Vercel settings hold only the project URL and publishable key.
<!-- /jot-entry -->

<!-- jot-entry -->
### JOT-dfb739bc-b5c5-47e2-8433-8efde3f6922d
Kind: intent
State: confirmed
Recorded: 2026-11-01T13:44:25.074Z
Author: Kayden
Source: Owner message to orchestrator C, 2026-11-01 (cloud session), answering COH-005, COH-006 and COH-016
Topic: owner-answers-coherence
Supersedes: none

COH-016 connectors: The owner does not want the Supabase and Vercel connectors detached, because the attachment is shared with the other orchestrators. Orchestrator C keeps them attached and never uses them; that is the working rule for S-013 No secrets.
<!-- /jot-entry -->

<!-- jot-entry -->
### JOT-7d650a76-bdc6-49e5-9f23-d1681b5ab1eb
Kind: intent
State: confirmed
Recorded: 2026-11-01T21:01:05.284Z
Author: Kayden
Source: Kayden, AMS resume chat 01a19887-118e-7dd2-88ad-676598f589ef, 2026-11-01; branch naming failure correction relayed by the owning orchestrator
Topic: owner-answers-coherence
Supersedes: none

Kayden corrected this run: "Report failure, you mislabled that branch. Codex/ is not a feature." Use feature/s002-trial-preflight for this work. The agent had used the harness default codex/ prefix and called it a feature branch. This entry records the current owner correction; it does not invent proof of a previously recorded prefix rule. Rename/push must preserve the exact commits and dirty work. Retain the old remote ref as recovery until main contains it; then clean up with containment checks.
<!-- /jot-entry -->

<!-- jot-entry -->
### JOT-fdaea0bd-5afa-4a88-ad43-dc8b41656c17
Kind: intent
State: confirmed
Recorded: 2026-11-02T17:30:51.085Z
Author: Owner
Source: Owner, AGENTS and RUNBOOK cleanup responsibilities in chat, 2026-11-02
Topic: owner-answers-coherence
Supersedes: none

The owner directs AGENTS.md to require cleanup and own shared CI, delivery and recovery rules. RUNBOOK.md owns where and how agents clean up, with a Clean up section after Test And Build. After verification, publish work to its authorized target, verify remote containment and leave no owned uncommitted or dirty work for the next agent on cold start. Preserve other writers and needed recovery material; any blocked publication or cleanup remains explicitly reported. This changes the operating documentation; it supplies no permission to publish unfinished site work to main or discard unrelated state.
<!-- /jot-entry -->

<!-- jot-entry -->
### JOT-3ac3966d-b26f-4212-894f-011e5e2410ad
Kind: intent
State: confirmed
Recorded: 2026-11-02T20:40:19.854Z
Author: Kayden
Source: Kayden, shared-skill repair instruction in AMS chat, 2026-11-02
Topic: owner-answers-coherence
Supersedes: none

Handoffs belong in the local ignored workbench/sessions lane and are never pushed to GitHub. The reusable skill source is KaydenClark/skills. Repair the skills responsible for handoff storage, branch ownership and cleanup; update this machine personal skills folder after the accepted repair so AMS can use it. Use Terra 6.1 for skill tests and RSI audits; merge skills only with Stable or Excellent results. Log failures, comparisons and disposition and show them in RSI graphs and charts on dev. This authorizes personal-catalog installation, not installation into other projects, dev-to-main promotion or fabricated qualification and benefit claims.
<!-- /jot-entry -->

<!-- jot-entry -->
### JOT-705f372a-89b7-4f9d-822c-77f7a7a0e689
Kind: intent
State: confirmed
Recorded: 2026-11-02T20:41:36.747Z
Author: Kayden
Source: Kayden, shared-skill repair instruction in AMS chat, 2026-11-02; routed to existing S-011 by assigned orchestrator
Topic: owner-answers-coherence
Supersedes: JOT-3ac3966d-b26f-4212-894f-011e5e2410ad

For S-011 shared-skill repair, Kayden confirms the destination and directs implementation: fix local handoff storage and the branch/cleanup failures, using source KaydenClark/skills. Handoffs stay in ignored workbench/sessions and never go to GitHub; Tasks are published. Test and audit with Terra 6.1, merge skills only with eligible Stable or Excellent results, then update this machine personal skills folder so subsequent AMS website work uses the repairs. Never install reusable methods in an AMS-specific skills folder. Log actual comparisons and disposition and display them in RSI charts on dev. This authorizes S-011 execution and personal-catalog installation, not cross-project rollout, dev-to-main promotion or fabricated qualification/benefit.
<!-- /jot-entry -->

<!-- jot-entry -->
### JOT-08cbbb7a-b88b-4ecc-962e-88d1578bce53
Kind: intent
State: confirmed
Recorded: 2026-11-02T20:54:13.949Z
Author: Kayden
Source: Kayden, RUNBOOK size and limits-versus-goal corrections in AMS chat, 2026-11-02
Topic: owner-answers-coherence
Supersedes: none

For S-011, Kayden rejects repeatedly shaving RUNBOOK toward its ceiling: the requested goal is a small operating entrypoint near900 characters, with a short cleanup line after verification. Characters, not words. The owner requires checking all existing rules before recording the correction. The actual policy already targets900–1500 Unicode codepoints with a3000 ceiling and forbids splitting/truncation; full-source counting normalizes line endings. Preserve the real command surface and use shared skill procedures rather than duplicating cleanup. Limits do not replace the requested goal. Log this execution failure and owner interventions separately from the frozen shared-skills comparison; do not change that series criteria or restart failed attempts.
<!-- /jot-entry -->

<!-- jot-entry -->
### JOT-8a72da2b-8f02-45c8-8df5-4ae2a339df45
Kind: proposal
State: unresolved
Recorded: 2026-11-02T20:54:43.528Z
Author: Kayden
Source: Kayden, possible prune-artifact skill in AMS chat, 2026-11-02; coordinating agent boundary suggestion remains proposed
Topic: owner-answers-coherence
Supersedes: none

Kayden proposes a single prune-artifact skill to do pruning for author-skill and writing-for-agents and reduce overlap. A suggested boundary leaves method development and behavior validation with author-skill, composition/prose quality with writing-for-agents, and meaning-preserving pruning against actual owner goals, target ranges and ceilings with prune-artifact. Author-skill would still delegate independent pruning and retest behavior. This is a proposal, not implementation or installation approval; keep it outside the current repair and use the observed RUNBOOK failure as a possible future trial.
<!-- /jot-entry -->

<!-- jot-entry -->
### JOT-1d568dd6-5ffd-43f5-a6e3-8f58568c92bf
Kind: intent
State: confirmed
Recorded: 2026-11-02T20:57:28.353Z
Author: Kayden
Source: Kayden, approval to add prune-artifact in AMS chat, 2026-11-02, after the proposed ownership breakdown
Topic: owner-answers-coherence
Supersedes: none

Kayden approves the proposed ownership breakdown and explicitly authorizes adding prune-artifact. This follows the earlier unresolved proposal: one shared pruning owner, author-skill retaining method development and behavior validation, and writing-for-agents retaining composition. The new skill is part of the shared skills source repair, with independent pruning/testing and the same eligible Stable or Excellent merge gate. Approval to implement is not evidence of an implemented, installed or accepted skill. Its new finite suite stays distinct from the original frozen workflow comparison.
<!-- /jot-entry -->

<!-- jot-entry -->
### JOT-d6f00913-7514-485e-9d55-fe69c6023838
Kind: intent
State: confirmed
Recorded: 2026-11-02T22:37:45.341Z
Author: Kayden
Source: Kayden, AMS continuation and three-example calibration corrections in chat, 2026-11-02; relayed by owning orchestrator
Topic: owner-answers-coherence
Supersedes: none

The owner requests a handoff to continue improving the skills, ending this campaign at a recoverable checkpoint. All three proposed examples still need actual tests. The owner identifies example 2 as losing the explicit owner-only dev-to-main approval gate and example 3 as losing the 900–1500 RUNBOOK target and near-900 goal in favor of the 3000 ceiling. These negative labels do not accept example 1, prove general skill behavior or impose a universal 900-character minimum. Preserve failed assessments and setup failures, source drafts and pending pruning; do not merge or install an unqualified candidate. Publish safe continuation records while handoff and raw evidence remain local and ignored.
<!-- /jot-entry -->

<!-- jot-entry -->
### JOT-fed30f75-6d6c-4cf6-9460-6c6bd22f69ed
Kind: intent
State: confirmed
Recorded: 2026-11-03T04:31:27.000Z
Author: Kayden
Source: Kayden, AMS chat 2026-11-02, orchestrate request naming skills PRs 59–66, then two model corrections
Topic: owner-answers-coherence
Supersedes: JOT-705f372a-89b7-4f9d-822c-77f7a7a0e689 (evaluator model only)

Kayden resumes S-011 as an RSI loop: improve the eight shared skills in PRs 59–66, fix their recorded failures (this project and GitHub) and prove the result on the AMS website. Each PR qualifies on its own; a PR may merge once fixed with an eligible Stable or Excellent passing review. Models follow the tier pairing in ADR-003K: the Mid tier runs the deciding trials and the Small tier gets a testing role chosen by the orchestrator. The prior owner-ended attempt and its failures stay preserved; this instruction is not a reset of attempt history.
<!-- /jot-entry -->

<!-- jot-entry -->
### JOT-e72ca481-c2b9-4940-86a0-141f6c261913
Kind: correction
State: confirmed
Recorded: 2026-11-03T04:33:31.000Z
Author: Kayden
Source: Kayden, AMS chat 2026-11-02, model correction during the resumed S-011 orchestration
Topic: owner-answers-coherence
Supersedes: JOT-fed30f75-6d6c-4cf6-9460-6c6bd22f69ed (model roles only)

Name model roles by tier, with each agent running a tier on its own harness's model: Frontier Fable/Astra, High Opus/Sol, Mid Sonnet/Terra, Small Haiku/Luna ([ADR-003K](../docs/adr/003K-model-tiers-pair-claude-and-codex-models.md)). This Claude-run orchestration uses Claude models: High implements, Mid runs the deciding trials, High and Small run the same held-out cases for a cross-model comparison, and Frontier judges and reviews. Claude and Codex share the system without one provider's model names standing in for the other's.
<!-- /jot-entry -->

<!-- jot-entry -->
### JOT-398538e8-c998-439c-9885-bb13b3388570
Kind: intent
State: confirmed
Recorded: 2026-11-03T05:29:29.000Z
Author: Kayden
Source: Kayden, AMS chat 2026-11-02, answering how ceiling-scoring skills qualify for merge
Topic: owner-answers-coherence
Supersedes: none

Kayden ruled that skills sent back because of failures the owner found are no longer excellent, and that those failures are the tests each fix must be proven against and brought to Stable or Excellent on. The qualifying tests for each skill are its owner-found failures, reproduced under their actual conditions; a baseline passing a test that does not reproduce the failure proves nothing. Each candidate must reach Stable or Excellent on those reproduction tests. The first held-out contract (SHA-256 197858fe…), on which the baseline already scored Excellent for seven skills, stays recorded as non-qualifying evidence.
<!-- /jot-entry -->

<!-- jot-entry -->
### JOT-c1566797-be06-4950-9dee-0d228d452c70
Kind: decision
State: confirmed
Recorded: 2026-11-03T16:00:39.000Z
Author: Kayden
Source: Kayden, AMS chat 2026-11-03, answering whether to merge journey (skills PR 60)
Topic: owner-answers-coherence
Supersedes: none

Kayden chose to merge journey (PR 60) although its recorded failures did not reproduce on the Claude Mid tier. The evidence is recorded as no regression (Excellent 30/30 in both arms) with a passing independent review, not as a proven fix.
<!-- /jot-entry -->

<!-- jot-entry -->
### JOT-0c8b00a9-901a-41c7-924e-1af73e48c7d6
Kind: decision
State: confirmed
Recorded: 2026-11-03T16:00:39.000Z
Author: Kayden
Source: Kayden, AMS chat 2026-11-03, choosing how S-011's RSI page change is branched
Topic: owner-answers-coherence
Supersedes: none

S-011's site change uses the same Spec branch, Feature/S-011-shared-skill-repair, with a pull request from it into dev, rather than a second S-011 branch. The orchestrator sequences it so records reach main before dev is merged into the branch, so the main pull request never carries unreleased dev work past the owner-only dev→main gate.
<!-- /jot-entry -->

<!-- jot-entry -->
### JOT-c093c149-fea8-41e0-a377-d2e263d699aa
Kind: intent
State: confirmed
Recorded: 2026-11-03T02:38:01.784Z
Author: Kayden
Source: Kayden, owner correction in AMS chat (Claude Code), 2026-11-02
Topic: owner-answers-coherence
Supersedes: none

Correction: run-scoped instructions never enter durable records. Limits that a chat gives one run (for example 'do not implement anything', 'preparation only', 'handoff only this run') stay in that run. Writing them into project instructions, Specs, Tasks, Wiki or skills makes the records stale and misleads later models, which obey them as standing rules. Durable records state lasting truth; authority for a run comes from the owner in that run.
<!-- /jot-entry -->

<!-- jot-entry -->
### JOT-b66f8d31-3731-4017-8502-dd54c9eba23e
Kind: intent
State: confirmed
Recorded: 2026-11-03T02:38:01.968Z
Author: Kayden
Source: Kayden, owner correction in AMS chat (Claude Code), 2026-11-02
Topic: owner-answers-coherence
Supersedes: none

Correction: CONTINUE.md (private GPT_OS branch claude/ams-s003-map-20261031) directly opposes how the Workbench works. It cannot be in the AMS environment, should never have been created, and should have been cleaned up when setup-workbench adopted AMS. Continuation goes only through Workbench records (Spec, Task, Wiki, jot) and local ignored session handoffs; the AGENTS.md pointer to CONTINUE.md is removed.
<!-- /jot-entry -->

<!-- jot-entry -->
### JOT-aba91085-29c1-4777-88a7-e8bc1da63060
Kind: intent
State: confirmed
Recorded: 2026-11-03T02:53:57.770Z
Author: Kayden
Source: Kayden, owner direction in AMS chat (Claude Code), 2026-11-02
Topic: owner-answers-coherence
Supersedes: none

AMS is the fixed, optimized and refined LLM_Workbench with RSI: the Workbench is the AMS and the AMS uses it. It accumulates what the owner has built with AI, knows and can prove; the website shows it off. The move from the Workbench Studio (LLM_Workbench, Audit_Workbench, Workbench_Template) trimmed only what research, evidence and proofs did not support or let be tested; it was not a redesign. No proper recovery phase ran: definitions and workflows were not captured here, so fixes already made in LLM_Workbench (for example, Specs carrying no history, AGENTS.md as every-turn universal obligations) were lost. Direction: anything from the Workbench that works and can be used is taken and made sure to be in AMS; do not redesign; do not reuse merely for ease. First step: find what really needs fixing and correcting so AMS is the working LLM_Workbench with RSI.
<!-- /jot-entry -->

<!-- jot-entry -->
### JOT-7f1423d9-1f8a-4b06-8334-de686807f172
Kind: intent
State: confirmed
Recorded: 2026-11-03T03:42:25.385Z
Author: Kayden
Source: Kayden, AMS recovery owner correction in chat, 2026-11-02
Topic: owner-answers-coherence
Supersedes: none

The owner authorized resuming after identifying another failure: the agent pursued the maximum instead of the established goal despite the earlier recorded issue. Preserve this as a recurrence and repair toward the smallest useful, faithful controls; passing a ceiling is not the goal or evidence of prevention.
<!-- /jot-entry -->
