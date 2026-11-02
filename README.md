# Agentic Management System

> Generated from LLM Workbench v3.2.2.

AMS brings Kayden's agents, workflows, intent capture, skills and AI tools into one RSI loop, using and repairing the Workbench beneath it. [Blueprint](BLUEPRINT.md) describes the destination; [S-001](workbench/specs/S-001-ams/SPEC.md) is the yardstick for whether AMS is built.

The first loop builds a website that explains and demonstrates AMS; its code lives in [`site/`](site/README.md), with Vercel hosting planned. This repository also holds the Workbench controls, lifecycle tools and artifact templates. Application behavior, deployment and measured improvements remain to be implemented and verified.

## Get Oriented

Start with Git status, then [AGENTS](AGENTS.md), [RUNBOOK](RUNBOOK.md#get-oriented), [ARCHITECTURE](ARCHITECTURE.md#routes), [GLOSSARY](GLOSSARY.md) and the relevant [Wiki MEMORY](workbench/wiki/MEMORY.md). ARCHITECTURE says which artifact owns each kind of truth and what each folder holds; [TASKBOARD](TASKBOARD.md) shows active work.

## Run The Checks

The room checks need Node.js 20+ and Git:

```bash
git clone https://github.com/KaydenClark/Agentic-Management-System.git
cd Agentic-Management-System
node workbench/tools/spec-workbench.mjs doctor
node workbench/tools/spec-workbench.mjs next --json
```

Without the owner's personal skill catalog, `doctor` exits 1 with `personal-catalog-unavailable`; otherwise a healthy room reports no blocking finding. The [Runbook](RUNBOOK.md#test-and-build) lists the other room checks and the Python tests; [`site/README.md`](site/README.md) covers the site build. Never commit real `.env` files, tokens, local databases, logs or private data.

## Working With Agents

The controls are plain Markdown for Codex, Claude or any agent that reads repository instructions. `CLAUDE.md` contains exactly `@AGENTS.md`; other agents start at `AGENTS.md`. Methods come from the owner's personal skill catalog, mapped in [SKILLS](workbench/docs/SKILLS.md); `.claude/skills` links to the project extension lane `.agents/skills/`.

## License

No license has been selected; `LICENSE` stays empty until the owner chooses one.
