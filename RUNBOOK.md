# AMS Runbook

## Get oriented

Every session, questions included, before replying or acting: check git status,
remotes, locks; read AGENTS, ARCHITECTURE, GLOSSARY, TRACKER, TASKBOARD, [Wiki](workbench/wiki/MEMORY.md),
[SKILLS](workbench/docs/SKILLS.md), assigned Spec/Task and the topic's records and failures.
Perform orientation silently; do not announce reading or routine checks.
Report findings or contradictions only when relevant to the request. No CONTINUE files.

## Workflows

`map` → `plan` → `journey`, or authorized `orchestrate`. Jot corrections in owners.
Use each role’s [model tier](workbench/docs/adr/003K-model-tiers-pair-claude-and-codex-models.md) on your own harness; claim as `claude-…` or `codex-…`.

Use Landmark -> Spec -> Task; at most six active Landmarks. Specs need no slots;
block Tasks only on required inputs ([ADR-003J](workbench/docs/adr/003J-limit-active-landmarks-not-specs.md)).

## Test And Build

Diagnose failures; use red/green/refactor when practical. Never weaken checks;
name unavailable checks. Three strikes: run, failed test, second failed test;
stop; report both attempts.

```sh
uv run pytest
S=workbench/tools/spec-workbench.mjs
node $S render && node $S doctor && node $S next --json
node workbench/tools/workbench-layout.mjs validate --project .
git diff --check
uv run ams-hygiene
```

Repeat on a fresh checkout. `site/`: `npm run build`, `npm test`.
`uv run ams-hygiene --site site`. Live: `AMS_LIVE=1`.

`uv run ams-board` (loopback). Concepts: `node workbench/tools/landmark-tracker.mjs show --committed --json`; [Board procedure](grill-board/README.md). Commands use `uv run`:

- `ams-keycheck`; `ams-writer record-merge|readcheck SHA`
- `ams-history import [--refresh-changed]|readcheck --ref SHA --dev-ref origin/dev`
- `ams-rsi livecheck`; `ams-sources livecheck`
- `ams-assess score|record|list`; `ams-assessment-store import|readcheck|livecheck`
- `ams-trials materialize|preflight|readback`; `ams-series`; `ams-orientation`

[Trial contracts](evals/TRIALS.md); stopped series stay stopped.

## Shared CI VM

Use [shared CI](workbench/wiki/context-shared-ci.md) VM `workbench-ci` and AMS runner;
No GitHub-hosted fallback. Skip forks; inspect before internal execution.
Keep keys and `AMS_LIVE` out of CI.

## Delivery and recovery

One `feature/spec-####-<spec-name>` branch per Spec creating new things, for all
Tasks, fixes, intent/docs. Commit/push owned work; never stash, reset,
discard to clean or commit to main. Publish ready intent/docs to main separately
from unfinished code. Code: Spec -> checked dev -> checked main;
only owner promotes website work. Merge commits; follow the
[delivery procedure](workbench/docs/SKILLS.md#delivery).

Recover via Spec/Task, Wiki; rollback: `workbench/sessions/recovery/adoption-recovery.json`.
Handoffs stay ignored in `workbench/sessions/handoffs/`; publish Tasks.

## Clean up

Keep the Spec branch until completion and all remaining work merged
and verified. Then `land` for guarded cleanup; report blockers.
