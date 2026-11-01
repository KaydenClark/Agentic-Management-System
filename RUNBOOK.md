# AMS - Runbook

> Generated from LLM Workbench v3.2.2. See the `setup-workbench` skill -> Update.

## Get oriented

1. Run `git status --short --branch`; keep others' work.
2. Read [AGENTS](AGENTS.md), [ARCHITECTURE](ARCHITECTURE.md#routes), [GLOSSARY](GLOSSARY.md) and the relevant [Wiki](workbench/wiki/MEMORY.md).
3. Read [TASKBOARD](TASKBOARD.md) and follow its Spec/Task owners; [S-001](workbench/specs/S-001-ams/SPEC.md) answers "Are we there yet?". Load the owning skill.

## Workflows

1. Capture request, reasons and corrections with `jot`; requirements go in the Spec.
2. A capability gets a Spec (`map`) and Tasks (`plan`) with observable acceptance; small edits need none. Run a Task with `journey`, coordinate with `orchestrate` ([SKILLS](workbench/docs/SKILLS.md)).
3. Check; keep proof, failures and limits. Record [review](workbench/specs/REVIEW-RECEIPT-TEMPLATE.md) and [Human QA](workbench/specs/HUMAN-QA-RECEIPT-TEMPLATE.md) only when they happen.
4. Deliver; update owners, run `render`, leave a [handoff](workbench/sessions/HANDOFF-TEMPLATE.md) if work remains.

### RSI during website work

Capture friction in a [feedback report](workbench/feedback/REPORT_FORMAT.md); test a bounded hypothesis with an [improvement record](workbench/research/IMPROVEMENT-TEMPLATE.md), eval task, result and comparison templates in [evals](evals/). Explain verified behavior with the [page template](site/PAGE-TEMPLATE.md).

## Preserve knowledge as it happens

Use existing topic owners; grow flat Wiki notes via [MEMORY](workbench/wiki/MEMORY.md) and its [schema](workbench/wiki/SCHEMA.md), with source, speaker, date and status.

## Test And Build

From the root: `uv run pytest` tests (`AMS_LIVE=1` adds a live test); `uv run ams-board` serves the [Grill Board](grill-board/README.md) on 127.0.0.1 only. Supabase, from orchestrator B's main checkout (key held, never printed): `uv run ams-keycheck` checks it; `uv run ams-writer record-merge|readcheck SHA` writes a merge; the site key reads, never writes; `uv run ams-history import|readcheck` imports build history idempotently. Room checks:

```bash
node workbench/tools/spec-workbench.mjs render
node workbench/tools/spec-workbench.mjs doctor
node workbench/tools/spec-workbench.mjs next --json
node workbench/tools/workbench-layout.mjs validate --project "$PWD"
git diff --check
```

`render` must leave no diff; `doctor` no blocking finding. On a fresh clone at the recorded commit, rerun them and `uv run pytest`.

## Version control and publication

Non-site work: branch, commit each step, push, PR into `main`, merge-commit once current and checked; delete the branch. Site work goes feature -> `dev` -> `main`; agents merge into `dev`, only the owner merges `dev` -> `main`. S-013 measures the `dev` lead. Report local, pushed, merged and deployed states separately.

## Recovery

Reopen the owning Spec/Task and Wiki; verify live state. Adoption rollback: `workbench/sessions/recovery/adoption-recovery.json` (local).
