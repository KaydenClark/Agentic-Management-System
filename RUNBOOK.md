# AMS Runbook

## Get oriented

Every session, questions included, before any reply or action: check git status,
remotes, locks; read AGENTS, ARCHITECTURE, GLOSSARY, TRACKER, TASKBOARD, [Wiki](workbench/wiki/MEMORY.md),
[SKILLS](workbench/docs/SKILLS.md), assigned Spec/Task and the topic's records and failures.
Open it with **Orientation**: records read, what exists, owner answers,
contradictions. It overrides answer-first style. No CONTINUE files.

## Workflows

`map` → `plan` → `journey`, or authorized `orchestrate`. Jot corrections in their owning records.
Run each role at its [model tier](workbench/docs/adr/003K-model-tiers-pair-claude-and-codex-models.md) on your own harness; claim as `claude-…` or `codex-…`.

Use Landmark -> Spec -> Task; at most six active Landmarks. Specs need no slots;
block Tasks only on required inputs ([ADR-003J](workbench/docs/adr/003J-limit-active-landmarks-not-specs.md)).

## Test And Build

Diagnose failures; use red/green/refactor when practical. Never weaken checks;
name unavailable checks. Three strikes: run, failed test, second failed test;
stop and report both attempts.

```sh
uv run pytest
S=workbench/tools/spec-workbench.mjs
node $S render && node $S doctor && node $S next --json
node workbench/tools/workbench-layout.mjs validate --project .
git diff --check
uv run ams-hygiene
```

Repeat on a fresh candidate checkout. `site/`: `npm run build`, `npm test`.
Root: `uv run ams-hygiene --site site`. Live tests: `AMS_LIVE=1`.

`uv run ams-board` (loopback). Concepts: `node workbench/tools/landmark-tracker.mjs show --committed --json`; [Board procedure](grill-board/README.md). Other commands use `uv run`:

- `ams-keycheck`; `ams-writer record-merge|readcheck SHA`
- `ams-history import [--refresh-changed]|readcheck --ref SHA --dev-ref origin/dev`
- `ams-rsi livecheck`; `ams-sources livecheck`
- `ams-assess score|record|list`; `ams-assessment-store import|readcheck|livecheck`
- `ams-trials materialize|preflight|readback`; `ams-series`; `ams-orientation`

[Trial contracts](evals/TRIALS.md); stopped series stay stopped.

## Shared CI VM

Use [shared CI](workbench/wiki/context-shared-ci.md) VM `workbench-ci` and AMS runner;
no GitHub-hosted fallback. Skip forks; inspect before internal execution.
Keep keys and `AMS_LIVE` out of CI.

## Delivery and recovery

Commit coherent steps with what/why; the [guard](.agents/hooks/require-committed.sh) checks dirt.
Never commit to main, stash, reset or discard to clean.
Merge current, checked non-site PRs into main with merge commits.
Site: feature -> checked dev; only owner merges dev -> main.
Follow [delivery reporting](workbench/docs/SKILLS.md#delivery).

Recover via Spec/Task and Wiki; adoption rollback: `workbench/sessions/recovery/adoption-recovery.json`.
Handoffs stay local and ignored in `workbench/sessions/handoffs/`; publish Tasks.

## Clean up

Use `land` after checks: verify publication/containment and no owned dirt. Retain unfinished Spec work; report blockers.
