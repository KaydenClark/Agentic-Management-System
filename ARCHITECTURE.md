# AMS - Architecture

**Last reviewed:** 2026-11-03
**Status:** partial

## Bird's-Eye View

AMS carries intent into outcomes with AI and uses RSI to improve its methods. [Blueprint](BLUEPRINT.md) owns the destination; AGENTS owns authority.

## Codemap

| Path | What lives there |
|---|---|
| `src/`, `tests/` | Package `ams`, pytest (uv); keycheck; hygiene; writer/history/rsi source rules; assessment-store keeps raw r1 packets private; site key only reads presentation rows |
| `supabase/` | Migrations: read-only baseline, `build_events`, `rsi_*` |
| `site/` | Public website; planned Vercel hosting, Supabase data |
| `grill-board/` | Owner's [cards](grill-board/README.md), theme, QA; local `ams-board` only |
| `evals/` | RSI eval tasks, results, comparisons |
| `.agents/` | Commit hook and skill extensions (`.claude/skills` links here) |
| Root files | Eight controls plus concept projection TRACKER.md |
| `workbench/` | [Manifest](workbench/manifest.json) lanes: specs, landmarks, ADR/DDR, wiki, feedback, sessions, tools, research |

## Ownership

| Truth | Owner |
|---|---|
| Authority | Owner request -> [AGENTS](AGENTS.md); a Spec narrows |
| Destination | [Blueprint](BLUEPRINT.md) |
| Requirements, evidence | Spec `SPEC.md`; Task `TASK.md` owns execution state and proof |
| Direction above Specs | `workbench/landmarks/LMK-*/LANDMARK.md` |
| Decisions | `workbench/docs/adr/`, `workbench/docs/ddr/` (`adr.mjs`) |
| Language | [Glossary](GLOSSARY.md); Wiki explains |
| Knowledge | [Wiki MEMORY](workbench/wiki/MEMORY.md) via `jot` |
| Execution view | [Taskboard](TASKBOARD.md), from Landmarks, Specs and Tasks |
| Concept view | TRACKER.md, from stable DQCs; Board reads the same owners |
| Procedures | [Runbook](RUNBOOK.md) -> named skill and tool |
| Configuration | Manifest and `workbench/tools/` receipt |
| Feedback | `workbench/feedback/` |
| Evaluation | [RSI](workbench/docs/SKILLS.md#rsi-operations), `evals/` |
| Orientation | [README](README.md) |

## Routes

| Need | Read |
|---|---|
| Scope | [AGENTS](AGENTS.md) and the owner request |
| Purpose | [Blueprint](BLUEPRINT.md), [AMS purpose](workbench/wiki/context-ams-purpose.md) |
| Assigned work | `spec-workbench.mjs show S-###` |
| Decision rationale | `adr.mjs list` -> record -> its owners |
| Methods, layout | [SKILLS](workbench/docs/SKILLS.md), [structure](workbench/docs/WORKBENCH_STRUCTURE.md) |
| Operations, recovery | [Runbook](RUNBOOK.md) |

## Invariants And Boundaries

- DQCs and execution owners link stable IDs in both directions; projections never set execution state or acceptance.
- A manifest declares, a receipt records, a template shapes and code behaves; none proves another.
- Review and Human QA are recorded only when performed on identified content.
- Website claims separate planned, observed and repeated behavior; publish only safe evidence.
- Personal skills keep their own lifecycle; a host adapter changes only discovery.
