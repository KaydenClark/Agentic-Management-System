---
type: project
status: partial
sensitivity: normal
knowledge_role: curated
provenance:
  - /jot capture; each claim names its source and date
source_paths: []
last_verified: 2026-11-01
---

# Owner answers to coherence findings

Captured context. Claim labels preserve intent and uncertainty; capture alone supplies neither Canon nor implementation proof. The date above checks this page's capture format, not every claim.

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
