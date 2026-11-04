---
type: memory
status: active
sensitivity: normal
knowledge_role: canonical
provenance:
  - AMS template adaptation from owner instruction, 2026-10-31
  - Workbench Adoption with setup-workbench v3.2.2, 2026-11-01
source_paths:
  - workbench/wiki
last_verified: 2026-11-01
---

# Agentic Management System Memory

> Generated from LLM Workbench v3.2.2. This is the room brain: the
> canonical, human-editable memory router for this project, kept at
> `workbench/wiki/MEMORY.md`. Start here and follow the smallest relevant
> link instead of browsing folders or searching.

The Wiki is this room's persistent knowledge base. For each operation, read
relevant existing articles and reconcile changed knowledge into those articles
before finishing. This router links the articles and live owners; it never
duplicates Task state.

- [Wiki definition and maintenance rules](SCHEMA.md#purpose-and-ownership) - purpose, ownership, metadata and article maintenance.
- [Jot method](../docs/SKILLS.md) - when to read and update existing articles.

- [Canonical failure log](../feedback/WORKBENCH_FEEDBACK.md) — all failures, failed model tier/provider, activity, correct outcome and repair evidence.
- [Feedback-to-improvement loop plan](context-feedback-improvement-loop-plan.md) — detection, feedback consumption, visible learning and later-use proof; planning only.
- [Shared skills refocus](context-skills-refocus.md) — confirmed jobs, composition, prerequisites, attribution and the Prepare-only boundary; links the AMS preparation-bypass failure.

## Source Precedence

Use AGENTS for authority, Blueprint or the assigned Spec for intended behavior,
and dated source or runtime checks for actual behavior; maintained notes routed
here come next, then `archive/` and generated material. A newer requirement may
expose an implementation gap; a newer verified implementation may expose stale
documentation. Investigate unclear ordering, repair the stale note and keep the
correction. The Wiki routes to owners and authorizes nothing.

## Leaving The Wiki

| Go to | For |
|---|---|
| [AGENTS.md](../../AGENTS.md) | Authority, scope, safety and collaboration |
| [BLUEPRINT.md](../../BLUEPRINT.md) | What the product is, who it serves, the outcomes it promises and what it is not |
| [GLOSSARY.md](../../GLOSSARY.md) | Shared AMS terms and feedback dispositions |
| [ARCHITECTURE.md](../../ARCHITECTURE.md) | Which artifact owns each kind of truth and the routes to it |
| [TASKBOARD.md](../../TASKBOARD.md) | Current execution state, rendered from Spec and Task records |
| `workbench/specs/`, `workbench/landmarks/` | Stable capability and landmark records, acceptance, evidence, and proof |
| [RUNBOOK.md](../../RUNBOOK.md) | Exact operating and verification commands |
| [design-concepts/](design-concepts/README.md) | Articles explaining durable design models and each landmark's evolving synthesis |
| [features/](features/README.md) | Maintained capability knowledge, history and sources across contributing Specs |
| [guidebooks/](guidebooks/) | Ordered procedures that outgrew the Runbook |

## Vocabulary

The root `GLOSSARY.md` defines AMS's shared words. The Workbench ships these
explanatory articles for its own vocabulary; they explain, and do not replace,
an AMS glossary entry.

- [Destination and direction](vocabulary-destination-and-direction.md) - destinations, landmarks, question cards and the frontier of ready work
- [Workflow verbs](vocabulary-workflow-verbs.md) - the actions every workflow is built from
- [Workbench, room and artifacts](vocabulary-workbench-room-and-artifacts.md) - the Workbench, the project and the kinds of artifact agents meet
- [Specs and Tasks](vocabulary-specs-and-tasks.md) - units of planned work, their reviews and where their records go
- [Chats and roles](vocabulary-chats-and-roles.md) - working contexts agents run in and the scopes they are assigned
- [Feedback disposition](vocabulary-feedback-disposition.md) - the closed set of outcomes a feedback finding ends with
- [Workbench meanings of AI coding terms](vocabulary-workbench-meanings-of-ai-coding-terms.md) - AI coding words with a distinct Workbench meaning
- [Continuity terms](vocabulary-continuity-terms.md) - notepads, scoped handoffs and artifact identifiers
- [Stance terms](vocabulary-stance-terms.md) - the job each stance does inside an assigned role
- [Governance core](vocabulary-governance-core.md) - claim roles, authority, lanes, collections and decision records
- [Continuity and evidence boundaries](vocabulary-continuity-and-evidence-boundaries.md) - what transport, promotion and host checks do and do not establish
- [AI coding reference](ai-coding-reference.md) - general AI coding words restated in Workbench words

## History

One page per Spec and Landmark. The Spec holds the destination; its page holds how it got there.

- [LMK-001 history](history/LMK-001.md) - closes, verdicts, approvals and corrections for LMK-001 (Grill Board)
- [LMK-002 history](history/LMK-002.md) - closes, verdicts, approvals and corrections for LMK-002 (RSI presentation)
- [LMK-003 history](history/LMK-003.md) - closes, verdicts, approvals and corrections for LMK-003 (AMS website)
- [LMK-004 history](history/LMK-004.md) - closes, verdicts, approvals and corrections for LMK-004 (RSI loop during the build)
- [S-001 history](history/S-001.md) - closes, verdicts, approvals and corrections for S-001 (AMS)
- [S-002 history](history/S-002.md) - closes, verdicts, approvals and corrections for S-002 (RSI loop)
- [S-003 history](history/S-003.md) - closes, verdicts, approvals and corrections for S-003 (showcase site)
- [S-004 history](history/S-004.md) - closes, verdicts, approvals and corrections for S-004 (Grill Board cards)
- [S-005 history](history/S-005.md) - closes, verdicts, approvals and corrections for S-005 (page review cards)
- [S-006 history](history/S-006.md) - closes, verdicts, approvals and corrections for S-006 (RSI data store)
- [S-007 history](history/S-007.md) - closes, verdicts, approvals and corrections for S-007 (RSI charts)
- [S-008 history](history/S-008.md) - closes, verdicts, approvals and corrections for S-008 (skills wiki)
- [S-009 history](history/S-009.md) - closes, verdicts, approvals and corrections for S-009 (demo Grill Board)
- [S-010 history](history/S-010.md) - closes, verdicts, approvals and corrections for S-010 (governance flow charts)
- [S-011 history](history/S-011.md) - closes, verdicts, approvals and corrections for S-011 (land skill events)
- [S-012 history](history/S-012.md) - closes, verdicts, approvals and corrections for S-012 (Python lifecycle CLI)
- [S-013 history](history/S-013.md) - closes, verdicts, approvals and corrections for S-013 (coherence checks)

## Routing

| Question | Read first |
|---|---|
| What is the Grilling Board, and how do DQCs carry its questions and updates? | [Grilling Board and DQC-backed intent](context-grilling-board.md) — recovered LLM_Workbench definition, confirmed DQC relationship, implementation limits and AMS comparison. |
| What is AMS and why is the first loop a website? | [AMS purpose](context-ams-purpose.md) — owner clarification, scope and rationale. |
| What should the website explain, and where are skill improvements proved? | [Website presentation](context-website-presentation.md) — this build proves shared skill improvements and displays the RSI log; owner corrections and site history. |
| How was the Workbench adopted, and what moved where? | [Workbench adoption](context-workbench-adoption.md) — package identity, Port/Fold/Keep/Retire map, checks and open gaps. |
| Which Specs are active, and who approved them? | [Active Spec approvals](context-active-spec-approvals.md) — the owner's confirmed Jot entries each active Spec cites for Confirmation and Execution approval. |
| Who approves merges, where does the Supabase service key live, and may C use the shared connectors? | [Owner answers to coherence findings](context-owner-answers-coherence.md) — owner corrections of 2026-11-01: agents merge non-site work, the key stays local, C never calls the connectors. |
| Which research informed the templates? | [Research basis](../research/template-research-basis.md) — inspected sources, design implications and limits. |
| Where does AMS CI run? | [Shared CI](context-shared-ci.md) — owner requirement, workflow routing and VM operation. |
| Where does a Spec's history go? | [Spec history](context-spec-history.md) — owner ruling of 2026-11-02: no history on Specs; each Spec and Landmark's history lives on its page under [History](#history). |

Add a row only when a durable note exists to route to. Grow flat notes beside
this router and inside the declared collections; only `archive/` may nest.
Every page this router links carries a one-line summary beside its link.

## Up-Link

Standalone room; no deployment wiki.
