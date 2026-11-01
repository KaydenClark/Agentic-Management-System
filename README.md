# Agentic Management System

> AMS orientation adapted from LLM_Workbench `templates/README.md` at `227d7c2a3ca0`; setup fields remain unconfigured.

AMS brings Kayden's agents, workflows, intent capture, skills and AI tools into one RSI loop, using and repairing the Workbench beneath it.

The first loop builds a website that explains and demonstrates AMS. This repository currently provides the tailored controls and reusable artifact templates; application behavior, deployment and measured improvements remain to be implemented and verified. See [Blueprint](BLUEPRINT.md) for the destination.

## How This Project Is Run

This repository is governed by a small set of control documents. Start with
Git status -> [AGENTS](AGENTS.md) -> [RUNBOOK](RUNBOOK.md#get-oriented) ->
[ARCHITECTURE](ARCHITECTURE.md#routes) -> [GLOSSARY](GLOSSARY.md) -> relevant
[Wiki/context](workbench/wiki/MEMORY.md) -> begin the requested work.
Keep the initial prompt in mind when choosing context. Load the other
owners below when the operation needs them:

- [`AGENTS.md`](AGENTS.md) - how agents behave here: authority order, read/edit
  scope, the task-selection loop, documentation ownership, and proof rules.
- [`BLUEPRINT.md`](BLUEPRINT.md) - what the product is, who it serves, the outcomes it promises and what it is not.
- [`GLOSSARY.md`](GLOSSARY.md) - accepted project-wide terms and definitions;
  consult it when shared language could be ambiguous.
- [`ARCHITECTURE.md`](ARCHITECTURE.md) - which artifact owns each kind of
  truth, the routes to it and the invariants that must stay true.
- [`TASKBOARD.md`](TASKBOARD.md) - active spec projection: current slice, owner,
  blocker, latest event, and next gate.
- `workbench/specs/S-NNN/SPEC.md` - on-demand capability truth,
  acceptance, decisions, verification, append-only evidence, and completion.
- [`RUNBOOK.md`](RUNBOOK.md) - the short operating manual linking each workflow
  to its owning procedure and verification commands.
- [`workbench/wiki/MEMORY.md`](workbench/wiki/MEMORY.md) - the room brain:
  canonical, human-editable durable memory for this project. It routes to the
  live controls above, to flat memory notes, and to article collections when needed; it never duplicates live task state.

- [`workbench/feedback/WORKBENCH_FEEDBACK.md`](workbench/feedback/WORKBENCH_FEEDBACK.md) -
  Workbench Feedback: log where the AMS work structure or instructions cause friction, with observations and dispositions.

## Getting Started

```bash
[INSTALL COMMAND]      # e.g. npm install / pip install -e . / make setup
[RUN COMMAND]          # e.g. npm run dev / python -m app
[TEST COMMAND]         # e.g. npm test / pytest
```

[Fill in setup and environment details after implementation choices are made.]

### Prerequisites

Required tools:

- [tool and version]
- [tool and version]

Required accounts/services:

- [service]
- [service]

Required local files:

- `[path]` - [purpose / how to create safely]

### Environment Configuration

Create local config from the example:

```bash
[COPY_ENV_COMMAND]
```

Required variables:

| Variable | Purpose | Secret? | Example / Notes |
|---|---|---|---|
| `[ENV_VAR]` | [purpose] | [yes/no] | [placeholder only] |

Rules:

- Do not commit real `.env` files, tokens, local databases, logs, or private
  data.
- Keep secrets server-side or local-only.
- Prefer degraded states over fake data when an external source is unavailable.

### Install

```bash
[INSTALL_COMMAND]
```

Expected result:

- [what success looks like]

### Run Locally

```bash
[RUN_COMMAND]
```

Open:

- [local URL, CLI command, or service endpoint]

Expected result:

- [health response / visible UI / log line]

## Working With Agents

The control docs are intentionally plain Markdown so they work with Codex,
Claude, or any other agent that reads repository instructions - no framework or
preprocessing required.

For **Claude Code**, keep the one-line `CLAUDE.md` containing exactly
`@AGENTS.md` so the rules load automatically. Other agents should be pointed at `AGENTS.md` as their
entry point.

The ordinary route is AGENTS -> Runbook -> Architecture -> assigned Spec and
Task record, without reading every control. TASK.md owns Task state and proof;
its Spec owns acceptance and append-only evidence. Record the actual implementer, coordinator and reviewer where assigned. Review independence follows prior involvement; verify the applicable branch route before delivery.

Use the review and Human QA receipts linked in [Runbook](RUNBOOK.md#workflows). Branch and publication policy remain unconfigured.

Every completed task must leave proof in its final response and owning spec's
append-only evidence log. Milestone specs additionally require a short demo
artifact (screenshot, recording, preview URL, or one-command demo) so work is
accepted on product truth, not passing tests alone.

## Project Status

See [`TASKBOARD.md`](TASKBOARD.md) for the work-view template and [Wiki MEMORY](workbench/wiki/MEMORY.md) for durable knowledge. The reusable records are templates, not active Specs, Tasks or installed generators.

## License

[LICENSE - e.g. MIT. See `LICENSE`.]

## Project Folders

| Path | Intended contents |
|---|---|
| `src/` | AMS runtime software |
| `tests/` | Software correctness tests |
| `site/` | Public showcase website; planned Vercel hosting and Supabase backend |
| `grill-board/` | Separate locally hosted development question-and-answer tool |
| `evals/` | RSI trials, graders and measured results |
| `.agents/skills/` | Project-owned skills only; personal catalog remains independent |
| `.claude/skills` | Discovery symlink to ../.agents/skills |
| `workbench/` | Decisions, research, Wiki, Specs and Tasks, feedback, and ignored session context |

`.local/` and `.worktrees/` are reserved ignored paths, created when used.

## Template Sources And Coverage

See [template inventory](workbench/research/template-inventory.md) for source versions, layout adaptations, missing formats and deferred choices. LICENSE remains empty until a license is selected.
