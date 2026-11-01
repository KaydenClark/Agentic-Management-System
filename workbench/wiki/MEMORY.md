---
type: memory
status: current
sensitivity: normal
knowledge_role: curated
provenance:
  - AMS template adaptation from owner instruction, 2026-10-31
source_paths:
  - workbench/wiki
last_verified: 2026-10-31
---

> AMS template adapted from LLM_Workbench `templates/wiki/MEMORY.project.md` at `227d7c2a3ca0`. This is a starting format, not evidence of installed software, approved AMS policy, or completed work.

# Agentic Management System Memory


The Wiki is this room's persistent knowledge base. For each operation, read
relevant existing articles and reconcile changed knowledge into those articles
before finishing; follow the definition and operation loop below.
This router links the articles and live owners; it never duplicates Task state.

Use the flat [note](NOTE-TEMPLATE.md), [guidebook](GUIDEBOOK-TEMPLATE.md), [comparison](COMPARISON-TEMPLATE.md), [design-concept](DESIGN-CONCEPT-TEMPLATE.md) and [feature](FEATURE-TEMPLATE.md) templates. Keep provenance, source paths, verification limits and correction history. No Wiki parser or runtime schema is installed.
- [Runbook operation loop](../../RUNBOOK.md#preserve-knowledge-as-it-happens) - when to read and update existing articles.

## Resolve claims against their owners

Use AGENTS for authority, Blueprint/assigned Spec for intended behavior, and dated source/runtime checks for actual behavior. Wiki explanations route to those owners. A newer requirement may expose an implementation gap; a newer verified implementation may expose stale documentation. Investigate unclear ordering rather than ranking whole files. Preserve the correction and evidence limits.

## Leaving The Wiki

| Go to | For |
|---|---|
| [AGENTS.md](../../AGENTS.md) | Authority, scope, safety, and the work loop |
| [BLUEPRINT.md](../../BLUEPRINT.md) | What the product is, who it serves, the outcomes it promises and what it is not |
| [GLOSSARY.md](../../GLOSSARY.md) | Shared terms and the Governance core |
| [ARCHITECTURE.md](../../ARCHITECTURE.md) | Which artifact owns each kind of truth, the routes to it, and design-concept routing |
| [TASKBOARD.md](../../TASKBOARD.md) | Current execution state |
| `workbench/specs/` | Stable capability records, acceptance, evidence, and proof |
| [RUNBOOK.md](../../RUNBOOK.md) | Exact operating and verification commands |

## Vocabulary

The root `GLOSSARY.md` defines the project's shared words. [Add explanatory article routes only when their content exists; upstream vocabulary articles are not copied into this scaffold.]

## Routing

| Question | Read first |
|---|---|
| What is AMS and why is the first loop a website? | [AMS purpose](context-ams-purpose.md) — owner clarification, scope and rationale. |
| Which research informed the templates? | [Research basis](../research/template-research-basis.md) — inspected sources, design implications and limits. |

Add a row only when a durable note exists to route to. A young room may have an
empty table; that is fine. Grow flat notes beside this router; create collections when actual content needs them.

Every page this router links carries a one-line summary beside its link, so a
reader can choose a page without opening it. In a list, write
a Markdown link to an existing article followed by a short description; in a table, give the
link's row a second cell that says what the page is for. [The AMS Wiki validation command remains unimplemented.]

## Up-Link

[Link the relevant GPT_OS context if needed; no cross-project management is implied.]
