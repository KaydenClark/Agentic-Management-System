# AMS - Architecture

> Generated from LLM Workbench v3.2.2.

**Last reviewed:** 2026-11-01
**Status:** partial

## Bird's-Eye View

AMS runs Kayden's agents, workflows, intent capture, skills and AI tools as one RSI loop on the Workbench it repairs. [Blueprint](BLUEPRINT.md) owns the destination; AGENTS owns authority.

## Codemap

| Path | What lives there |
|---|---|
| `src/`, `tests/` | Package `ams`, pytest suite (uv); `ams-keycheck` checks the Supabase key |
| `supabase/` | Supabase migrations (read-only baseline) |
| `site/` | Public website; planned Vercel hosting, Supabase backend |
| `grill-board/` | Owner's card queue (`cards/*.md`); local `ams-board` only |
| `evals/` | RSI eval tasks, results and comparisons |
| `.agents/` | Commit hook and project skill extensions; `.claude/skills` links here |
| Root files | The eight controls; jobs in [Ownership](#ownership) |
| `workbench/` | [Manifest](workbench/manifest.json) lanes: specs, landmarks, docs (ADR/DDR), wiki, feedback, sessions, tools; plus `research/` templates |

## Ownership

| Truth | Owner |
|---|---|
| Authority, boundaries | Owner request -> [AGENTS](AGENTS.md); an assigned Spec narrows |
| Destination | [Blueprint](BLUEPRINT.md) |
| Requirements, acceptance, evidence | Spec `SPEC.md`; Task `TASK.md` owns execution state and proof |
| Direction above Specs | `workbench/landmarks/LMK-*/LANDMARK.md` |
| Decisions | `workbench/docs/adr/`, `workbench/docs/ddr/` (`adr.mjs`) |
| Language | [Glossary](GLOSSARY.md); Wiki explains |
| Knowledge, working context | [Wiki MEMORY](workbench/wiki/MEMORY.md) via `jot` |
| Work view | [Taskboard](TASKBOARD.md), rendered from records |
| Procedures, checks | [Runbook](RUNBOOK.md) -> named skill and tool |
| Configuration | Manifest and `workbench/tools/` receipt |
| Feedback | `workbench/feedback/` |
| Evaluation | [RSI](RUNBOOK.md#rsi-during-website-work), `evals/` |
| Orientation | [README](README.md) |

## Routes

| Need | Read |
|---|---|
| Scope | [AGENTS](AGENTS.md) and the owner request |
| Purpose | [Blueprint](BLUEPRINT.md), [AMS purpose](workbench/wiki/context-ams-purpose.md) |
| Assigned work | `spec-workbench.mjs show S-###` |
| Decision rationale | `adr.mjs list` -> record -> its owners |
| Methods, layout | [SKILLS](workbench/docs/SKILLS.md), [structure](workbench/docs/WORKBENCH_STRUCTURE.md) |
| Artifact choice | [Template inventory](workbench/research/template-inventory.md) |
| Operations, recovery | [Runbook](RUNBOOK.md) |

## Invariants And Boundaries

- Each claim has one owner; consumers link it. Taskboard and Wiki never establish state or acceptance.
- A manifest declares, a receipt records, a template shapes and code behaves; none proves another.
- Review and Human QA are recorded only when performed on identified content.
- Website claims separate planned, observed and repeated behavior and publish only safe evidence.
- Personal skills keep their own lifecycle; a host adapter changes only discovery.
