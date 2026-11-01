# Agentic Management System

> Generated from LLM Workbench v3.2.2.

AMS brings Kayden's agents, workflows, intent capture, skills and AI tools into one RSI loop, using and repairing the Workbench beneath it.

The first loop builds a website that explains and demonstrates AMS. This repository holds the Workbench controls, lifecycle tools and artifact templates; application behavior, deployment and measured improvements remain to be implemented and verified. See [Blueprint](BLUEPRINT.md) for the destination.

## How This Project Is Run

Start with Git status -> [AGENTS](AGENTS.md) -> [RUNBOOK](RUNBOOK.md#get-oriented) -> [ARCHITECTURE](ARCHITECTURE.md#routes) -> [GLOSSARY](GLOSSARY.md) -> relevant [Wiki context](workbench/wiki/MEMORY.md), then begin the requested work. Load other owners only when the operation needs them:

- [`AGENTS.md`](AGENTS.md) - how agents behave here: authority, scope, checks and delivery.
- [`BLUEPRINT.md`](BLUEPRINT.md) - what the product is, who it serves, its promised outcomes and non-goals.
- [`GLOSSARY.md`](GLOSSARY.md) - accepted project-wide terms.
- [`ARCHITECTURE.md`](ARCHITECTURE.md) - which artifact owns each kind of truth, routes and invariants.
- [`TASKBOARD.md`](TASKBOARD.md) - generated view of active Specs: slice, owner, blocker, latest event and next gate.
- `workbench/specs/S-###-slug/SPEC.md` (or inside a landmark under `workbench/landmarks/`) - capability truth, acceptance and append-only evidence; its `tasks/TK-###/TASK.md` records own Task state and proof.
- [`RUNBOOK.md`](RUNBOOK.md) - the operating manual and verification commands.
- [`workbench/wiki/MEMORY.md`](workbench/wiki/MEMORY.md) - the room brain: durable, human-editable project knowledge routed to the live controls; it never duplicates Task state.
- [`workbench/feedback/WORKBENCH_FEEDBACK.md`](workbench/feedback/WORKBENCH_FEEDBACK.md) - Workbench Feedback: where the work structure or instructions cause friction.

## Getting Started

There is no application to install or run yet. The Workbench room checks need Node.js 20+ and Git:

```bash
git clone https://github.com/KaydenClark/Agentic-Management-System.git
cd Agentic-Management-System
node workbench/tools/spec-workbench.mjs doctor
node workbench/tools/spec-workbench.mjs next --json
```

`doctor` reports no blocking finding on a healthy room. Setup, environment variables and run commands will be recorded here from the actual implementation once `site/` or `src/` exists. Never commit real `.env` files, tokens, local databases, logs or private data.

## Working With Agents

The controls are plain Markdown for Codex, Claude or any agent that reads repository instructions. `CLAUDE.md` contains exactly `@AGENTS.md`; other agents start at `AGENTS.md`. Methods come from the owner's personal skill catalog, mapped in [SKILLS](workbench/docs/SKILLS.md); `.claude/skills` links to the project extension lane `.agents/skills/`.

The ordinary route is AGENTS -> Runbook -> Architecture -> assigned Spec and Task record. Every completed Task leaves proof in its record and the Spec's evidence log; review and Human QA use the receipts linked from the [Runbook](RUNBOOK.md#workflows).

## Project Status

See [`TASKBOARD.md`](TASKBOARD.md) for active work and [Wiki MEMORY](workbench/wiki/MEMORY.md) for durable knowledge.

## License

No license has been selected; `LICENSE` stays empty until the owner chooses one.

## Project Folders

| Path | Intended contents |
|---|---|
| `src/` | AMS runtime software |
| `tests/` | Software correctness tests |
| `supabase/` | Supabase migrations; `pyproject.toml` pins the Python runtime |
| `site/` | Public showcase website; planned Vercel hosting and Supabase backend |
| `grill-board/` | Separate locally hosted development question-and-answer tool |
| `evals/` | RSI trials, graders and measured results |
| `.agents/` | Commit hook and project-owned skill extensions; the personal catalog stays independent |
| `workbench/` | Manifest-declared lanes (specs, landmarks, docs, wiki, feedback, sessions, tools) and research templates |

`.local/` and `.worktrees/` are reserved ignored paths. See the [template inventory](workbench/research/template-inventory.md) for artifact templates and their sources.
