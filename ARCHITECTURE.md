# AMS Architecture

AMS carries intent into outcomes with AI and improves its methods through RSI. [Blueprint](BLUEPRINT.md) owns destination; [AGENTS](AGENTS.md) owns authority.

## Codemap

`src/`, `tests/`: package and checks; `supabase/`: storage; `site/`: public presentation using a read-only presentation key; `grill-board/`: local review; `evals/`: RSI. [Manifest](workbench/manifest.json): Workbench lanes. `.agents/`: hook and skill extensions.

## Ownership and routes

| Need | Owner or route |
|---|---|
| Scope | Owner request, AGENTS, assigned Spec/Task |
| Destination | Blueprint; [purpose](workbench/wiki/context-ams-purpose.md) explains |
| Requirements and proof | Spec; Task owns execution and receipt; Landmark owns direction |
| Decisions | `workbench/docs/adr/`, `workbench/docs/ddr/`; use `adr.mjs list` |
| Language and knowledge | [Glossary](GLOSSARY.md); [Wiki](workbench/wiki/MEMORY.md) via jot |
| Work view | [Taskboard](TASKBOARD.md), rendered from records |
| Methods and operation | [SKILLS](workbench/docs/SKILLS.md), [Runbook](RUNBOOK.md) |
| Configuration | Manifest and tool receipt |
| Feedback and evaluation | `workbench/feedback/`, `evals/`; [RSI operations](workbench/docs/SKILLS.md#rsi-operations) |

Records do not prove behavior. Review and Human QA name actual work; website evidence distinguishes planned, observed and repeated behavior. Skills retain their own lifecycle.
