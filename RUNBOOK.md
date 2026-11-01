# AMS - Runbook

> Generated from LLM Workbench v3.2.2. See the `setup-workbench` skill -> Update.

## Get oriented

1. Run `git status --short --branch`; preserve others' work.
2. Read [AGENTS](AGENTS.md), [ARCHITECTURE](ARCHITECTURE.md#routes), [GLOSSARY](GLOSSARY.md) and the relevant [Wiki](workbench/wiki/MEMORY.md).
3. Read [TASKBOARD](TASKBOARD.md); follow its Spec/Task owners for scope, claimant, blockers and next gate. [S-001](workbench/specs/S-001-ams/SPEC.md) answers "Are we there yet?". Load the owning skill.

## Workflows

1. Capture request, reasons, corrections and endpoint with `jot`; requirements belong in the Spec.
2. A capability gets a Spec (`map`) and bounded Tasks (`plan`); define observable acceptance first. Small edits need none. Execute a Task with `journey`; coordinate with `orchestrate`. Method map: [SKILLS](workbench/docs/SKILLS.md).
3. Check the outcome; keep proof, failures and limits. Record [review](workbench/specs/REVIEW-RECEIPT-TEMPLATE.md) and [Human QA](workbench/specs/HUMAN-QA-RECEIPT-TEMPLATE.md) only when they happen.
4. Deliver through the verified route; update owners, run `render`, leave a [handoff](workbench/sessions/HANDOFF-TEMPLATE.md) if work remains.

### RSI during website work

Capture friction in a [feedback report](workbench/feedback/REPORT_FORMAT.md); test a bounded hypothesis with an [improvement record](workbench/research/IMPROVEMENT-TEMPLATE.md), [eval tasks](evals/EVAL-TASK-TEMPLATE.md), [results](evals/EVAL-RESULT-TEMPLATE.md) and a [comparison](evals/EVAL-COMPARISON-TEMPLATE.md). Explain verified behavior with the [page template](site/PAGE-TEMPLATE.md).

## Preserve knowledge as it happens

Use existing topic owners; grow flat Wiki notes through [MEMORY](workbench/wiki/MEMORY.md) under its [schema](workbench/wiki/SCHEMA.md), with source, speaker, date, status and corrections.

## Test And Build

From the root, `uv run pytest` runs the tests; `uv run ams-board` serves the Grill Board (`grill-board/cards/`) on 127.0.0.1:8765 only. Room checks:

```bash
node workbench/tools/spec-workbench.mjs render
node workbench/tools/spec-workbench.mjs doctor
node workbench/tools/spec-workbench.mjs next --json
node workbench/tools/workbench-layout.mjs validate --project "$PWD"
git diff --check
```

`render` must leave no diff; `doctor` no blocking finding.

Fresh clone: check out the recorded commit; rerun `uv run pytest` and the room checks.

## Version control and publication

Non-site work: branch, commit each step, push, PR into `main`, merge with a merge commit once current and checked, confirm `main` has it; delete the branch. Site work goes feature -> `dev` -> `main`; agents merge into `dev`, only the owner merges `dev` -> `main`. S-013 measures how far `dev` is ahead of `main`. Report local, pushed, merged and deployed states separately.

## Recovery

Reopen the owning Spec/Task and Wiki history; verify live state. Adoption rollback: `workbench/sessions/recovery/adoption-recovery.json` (local).
