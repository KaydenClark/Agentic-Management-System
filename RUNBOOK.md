# AMS - Runbook

> From LLM Workbench v3.2.2.

## Get oriented

Run `git status --short --branch`; preserve others' work. Read [AGENTS](AGENTS.md),
[Architecture routes](ARCHITECTURE.md#routes), [Glossary](GLOSSARY.md), relevant
[Wiki](workbench/wiki/MEMORY.md), [Taskboard](TASKBOARD.md) and assigned Spec/Task.
[S-001](workbench/specs/S-001-ams/SPEC.md) is the system yardstick. Load the owning
personal skill from [methods](workbench/docs/SKILLS.md).

## Workflows

Capture sourced intent/corrections with `jot` in the existing Wiki owner;
requirements belong in the Spec. Use `map`, `plan`, then `journey` for one Task
or `orchestrate` for authorized coordination. Retain proof/failures. Record
[Review](workbench/specs/REVIEW-RECEIPT-TEMPLATE.md) and
[Human QA](workbench/specs/HUMAN-QA-RECEIPT-TEMPLATE.md) only when performed.
Update owners and render before departure; leave a
[handoff](workbench/sessions/HANDOFF-TEMPLATE.md) when needed.

For website RSI, connect [feedback](workbench/feedback/REPORT_FORMAT.md),
[improvement records](workbench/research/IMPROVEMENT-TEMPLATE.md), [evals](evals/)
and [page evidence](site/PAGE-TEMPLATE.md). Static scores prove no benefit.

## Test And Build

`uv run pytest`; `AMS_LIVE=1` adds live Supabase tests. `uv run ams-board`
serves the [Grill Board](grill-board/README.md) on loopback only. Room checks:

```bash
node workbench/tools/spec-workbench.mjs render
node workbench/tools/spec-workbench.mjs doctor
node workbench/tools/spec-workbench.mjs next --json
node workbench/tools/workbench-layout.mjs validate --project "$PWD"
git diff --check
```

Render must leave no diff; doctor no blocking finding. Repeat these and pytest
on a fresh clone at the recorded candidate.

In B's main checkout, keys never printed: `uv run ams-keycheck`;
`ams-writer record-merge|readcheck SHA`; after each merge `ams-history import`,
then `ams-history readcheck --ref SHA --dev-ref origin/dev`. Refresh older rows
with `ams-history import --refresh-changed` before readcheck. `ams-rsi livecheck`
and `ams-sources livecheck` check RSI/source rules.

`ams-assess score|record|list` handles local r1 packets;
`ams-assessment-store import|readcheck|livecheck` verifies private Supabase storage
([contract](evals/ASSESSMENTS.md)). Storage proves no benefit. Trials use the
subscription meter; unknown stays unknown.
`ams-trials materialize|preflight|readback` prepares [private trial inputs](evals/TRIALS.md); it never calls a model.

### Shared CI

CI uses `workbench-ci` and
`workbench-runner-ams` service, never a GitHub-hosted fallback. Queued jobs may
mean the VM is unavailable. Fork jobs skip; inspect before internal execution.
[Shared CI](workbench/wiki/context-shared-ci.md) owns setup/operation details.
Keep keys and `AMS_LIVE` out of CI.

## Delivery and recovery

Non-site: feature branch -> checked PR -> merge commit into `main`, delete branch.
Site: feature -> checked `dev`; only the owner merges `dev` -> `main`.
Report push, merge and deploy separately. Reopen Spec/Task and Wiki for
recovery; adoption rollback: `workbench/sessions/recovery/adoption-recovery.json`.
