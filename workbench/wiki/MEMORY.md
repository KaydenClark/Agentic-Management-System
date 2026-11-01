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
- [Runbook operation loop](../../RUNBOOK.md#preserve-knowledge-as-it-happens) - when to read and update existing articles.

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
| [AGENTS.md](../../AGENTS.md) | Authority, scope, safety, and the work loop |
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

## Routing

| Question | Read first |
|---|---|
| What is AMS and why is the first loop a website? | [AMS purpose](context-ams-purpose.md) — owner clarification, scope and rationale. |
| What should the website explain, and why was S-003 rewritten? | [Website presentation](context-website-presentation.md) — owner corrections, presentation intent and source-linked implementation history. |
| How was the Workbench adopted, and what moved where? | [Workbench adoption](context-workbench-adoption.md) — package identity, Port/Fold/Keep/Retire map, checks and open gaps. |
| Which Specs are active, and who approved them? | [Active Spec approvals](context-active-spec-approvals.md) — the owner's confirmed Jot entries each active Spec cites for Confirmation and Execution approval. |
| Who approves merges, where does the Supabase service key live, and may C use the shared connectors? | [Owner answers to coherence findings](context-owner-answers-coherence.md) — owner corrections of 2026-11-01: agents merge non-site work, the key stays local, C never calls the connectors. |
| Which research informed the templates? | [Research basis](../research/template-research-basis.md) — inspected sources, design implications and limits. |
| Where does AMS CI run? | [Shared CI](context-shared-ci.md) — owner requirement, workflow routing and VM operation. |

Add a row only when a durable note exists to route to. Grow flat notes beside
this router and inside the declared collections; only `archive/` may nest.
Every page this router links carries a one-line summary beside its link.

## Up-Link

Standalone room; no deployment wiki.
