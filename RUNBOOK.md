# AMS - Runbook

> Generated from LLM Workbench v3.2.2. See the `setup-workbench` skill -> Update.

## Get oriented

1. Run `git status --short --branch`; preserve other work.
2. Read [AGENTS](AGENTS.md), [ARCHITECTURE](ARCHITECTURE.md#routes), [GLOSSARY](GLOSSARY.md) and relevant [Wiki context](workbench/wiki/MEMORY.md).
3. Read [TASKBOARD](TASKBOARD.md); follow its Spec/Task owners for scope, claimant, blockers and next gate. Recover settled answers; load the owning skill.

## Workflows

1. Capture request, reasons, corrections and endpoint with `jot`; requirements belong in the Spec.
2. A capability gets a Spec (`map`) and bounded Tasks (`plan`); define observable acceptance first. Small edits need none. Execute a Task with `journey`; coordinate with `orchestrate`. Method map: [SKILLS](workbench/docs/SKILLS.md).
3. Check the outcome; keep proof, failures and limits. Record [review](workbench/specs/REVIEW-RECEIPT-TEMPLATE.md) and [Human QA](workbench/specs/HUMAN-QA-RECEIPT-TEMPLATE.md) only when they happen.
4. Deliver through the verified route; update owners, run `render`, leave a [handoff](workbench/sessions/HANDOFF-TEMPLATE.md) if work remains.

### RSI during website work

Capture friction in a [feedback report](workbench/feedback/REPORT_FORMAT.md) or [evidence audit](workbench/research/EVIDENCE-AUDIT-TEMPLATE.md); test a bounded hypothesis with an [improvement record](workbench/research/IMPROVEMENT-TEMPLATE.md), [eval tasks](evals/EVAL-TASK-TEMPLATE.md), [results](evals/EVAL-RESULT-TEMPLATE.md) and a [comparison](evals/EVAL-COMPARISON-TEMPLATE.md). Explain verified behavior with the [page template](site/PAGE-TEMPLATE.md); recheck later use.

## Preserve knowledge as it happens

Use existing topic owners; grow flat Wiki notes through [MEMORY](workbench/wiki/MEMORY.md) under its [schema](workbench/wiki/SCHEMA.md). Record source, speaker, date, status and corrections.

## Test And Build

No application, test suite or eval runner exists yet. Room checks, run from the root:

```bash
node workbench/tools/spec-workbench.mjs render
node workbench/tools/spec-workbench.mjs doctor
node workbench/tools/spec-workbench.mjs next --json
node workbench/tools/workbench-layout.mjs validate --project "$PWD"
git diff --check
```

`render` must leave no diff; `doctor` must report no blocking finding.

Fresh-clone check: `git clone https://github.com/KaydenClark/Agentic-Management-System.git CLONE && cd CLONE`, check out the recorded commit, then rerun the room checks.

## Version control and publication

`main` is the only long-lived branch: branch, commit each step, push, open a PR into `main`, merge with a merge commit once up to date and checked, confirm `main` has it, delete the branch. No deployment is configured; report local, pushed, merged and deployed states separately.

## Recovery

Reopen the owning Spec/Task and Wiki history; verify live state before resuming. Adoption rollback: `workbench/sessions/recovery/adoption-recovery.json` (local).
