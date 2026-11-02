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

The [owner correction](#jot-fdaea0bd-5afa-4a88-ad43-dc8b41656c17) assigns the cleanup obligation, shared CI, delivery and recovery rules to [AGENTS](../../AGENTS.md#delivery-and-recovery). [RUNBOOK Clean up](../../RUNBOOK.md#clean-up) owns the actions after Test And Build: inspect owned state, publish and verify the authorized target, remove contained temporary scaffolding, and leave clean owned checkouts with explicit retained items or blockers. Earlier merge authority and recovery protections remain.

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
