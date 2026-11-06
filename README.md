# Agentic Management System

> Generated from LLM Workbench v3.2.2.

AMS is a reusable system of workflows, rules, skills and tools through which people capture, develop and record intent with AI, and agents carry that intent into verified outcomes. [Blueprint](BLUEPRINT.md) describes the final product; [S-001](workbench/specs/S-001-ams/SPEC.md) assesses the current build against its bounded criteria.

This room builds the public website, runs the recursive self-improvement (RSI) loop and improves shared skills already used across projects. The website explains AMS and shows verified results from its own build and skill improvements, with room for evidence from other projects later. Its code lives in [`site/`](site/README.md). Projects needing setup or Workbench adjustments use `setup-workbench` in their own folder. Current implementation and proof live in the linked Spec and Task records.

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
