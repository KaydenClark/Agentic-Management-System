# AMS Runbook

## Get oriented

Read [AGENTS](AGENTS.md), [architecture](ARCHITECTURE.md), [glossary](GLOSSARY.md), [Wiki](workbench/wiki/MEMORY.md), [Taskboard](TASKBOARD.md), assigned Spec/Task and [skill](workbench/docs/SKILLS.md).


## Test And Build

Red/green/refactor when practical; never weaken checks. Run `uv run pytest`, `git diff --check`, `uv run ams-hygiene` and `node workbench/tools/workbench-layout.mjs validate --project .`. With `node workbench/tools/spec-workbench.mjs`, run `render`, `doctor`, `next --json`, `show SPEC_ID`. Render: no diff; doctor: no global blockers. Repeat on fresh checkout. Site: `npm run build`, `npm test`; root: `uv run ams-hygiene --site site`. Live tests: `AMS_LIVE=1`. [Shared CI](workbench/wiki/context-shared-ci.md).

`uv run ams-board` (loopback); also `uv run`:

- `ams-keycheck`; `ams-writer record-merge|readcheck SHA`
- `ams-history import [--refresh-changed]|readcheck --ref SHA --dev-ref origin/dev`
- `ams-rsi livecheck`; `ams-sources livecheck`
- `ams-assess score|record|list`; `ams-assessment-store import|readcheck|livecheck`
- `ams-trials materialize|preflight|readback`; `ams-series`

[Trial contracts](evals/TRIALS.md); stopped series stay stopped.

## Clean up

`land`: verify publication and containment; keep unfinished work on its Spec branch; report blockers. Rollback: `workbench/sessions/recovery/adoption-recovery.json`.
