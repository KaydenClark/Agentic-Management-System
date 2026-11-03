# AMS Runbook

## Get oriented

`git status --short --branch`; read [AGENTS](AGENTS.md) and assigned Spec/Task.

## Workflows

`map` → `plan` → `journey`, or authorized `orchestrate`. Jot corrections in Wiki.
Run each role at its [model tier](workbench/docs/adr/003K-model-tiers-pair-claude-and-codex-models.md) on your own harness; claim as `claude-…` or `codex-…`.

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

Repeat on a fresh candidate checkout. `site/`: `npm run build`, `npm test`.
Root: `uv run ams-hygiene --site site`. Live tests: `AMS_LIVE=1`.

`uv run ams-board` (loopback). Other commands use `uv run`:

- `ams-keycheck`; `ams-writer record-merge|readcheck SHA`
- `ams-history import [--refresh-changed]|readcheck --ref SHA --dev-ref origin/dev`
- `ams-rsi livecheck`; `ams-sources livecheck`
- `ams-assess score|record|list`; `ams-assessment-store import|readcheck|livecheck`
- `ams-trials materialize|preflight|readback`; `ams-series`

[Trial contracts](evals/TRIALS.md); stopped series stay stopped.

## Clean up

Use shared `land` under [project delivery](AGENTS.md#delivery-and-recovery).
