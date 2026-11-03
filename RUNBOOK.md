# AMS Runbook

## Get oriented

`git status --short --branch`; read [AGENTS](AGENTS.md), [architecture](ARCHITECTURE.md), [glossary](GLOSSARY.md), [Wiki](workbench/wiki/MEMORY.md), [Taskboard](TASKBOARD.md), assigned Spec/Task and [skill](workbench/docs/SKILLS.md).

## Workflows

Use `map` → `plan` → `journey`, or authorized `orchestrate`; retain evidence and failures. Handoffs stay local and ignored.

## Test And Build

```sh
uv run pytest
node workbench/tools/spec-workbench.mjs render
node workbench/tools/spec-workbench.mjs doctor
node workbench/tools/spec-workbench.mjs next --json
node workbench/tools/workbench-layout.mjs validate --project .
git diff --check
uv run ams-hygiene
```

Render: no diff; doctor: no global blockers. Repeat on a fresh checkout. Site: `npm run build`, `npm test`.
Root: `uv run ams-hygiene --site site`. Live tests: `AMS_LIVE=1`.

`uv run ams-board` (loopback). Other commands use `uv run`:

- `ams-keycheck`; `ams-writer record-merge|readcheck SHA`
- `ams-history import [--refresh-changed]|readcheck --ref SHA --dev-ref origin/dev`
- `ams-rsi livecheck`; `ams-sources livecheck`
- `ams-assess score|record|list`; `ams-assessment-store import|readcheck|livecheck`
- `ams-trials materialize|preflight|readback`; `ams-series`

[Trial contracts](evals/TRIALS.md); stopped series stay stopped.

## Clean up

Use `land`: verify publication and containment; retain unfinished work on its Spec branch; report blockers. Adoption rollback: `workbench/sessions/recovery/adoption-recovery.json`.
