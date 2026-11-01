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

From the root: `uv run pytest` (`AMS_LIVE=1` adds live tests); `uv run ams-board` serves the [Grill Board](grill-board/README.md) on 127.0.0.1 only. Supabase (`uv run` in orchestrator B's main checkout; key never printed): `ams-keycheck` checks it; `ams-writer record-merge|readcheck SHA` (a merge), `ams-history import` then `readcheck` after each merge (no schedule); `ams-rsi`/`ams-sources livecheck` test RSI and source rules. Room checks:

```bash
node workbench/tools/spec-workbench.mjs render
node workbench/tools/spec-workbench.mjs doctor
node workbench/tools/spec-workbench.mjs next --json
node workbench/tools/workbench-layout.mjs validate --project "$PWD"
git diff --check
```

`render` must leave no diff, `doctor` no blocking finding. On a fresh clone at the recorded commit, rerun them and `uv run pytest`.

### Shared CI VM

Both GitHub Actions checks (`python tests` and `site builds`) use
`[self-hosted, Linux, ARM64, servitor]` on the existing `workbench-ci` VM.
AMS has a dedicated unprivileged runner account and the systemd service
`workbench-runner-ams`; it shares neither credentials nor workspaces with
other projects. The service starts with the VM and restarts after failure.
An unavailable VM queues checks; there is no GitHub-hosted fallback.

The runner cannot use sudo. Provision Playwright's Chromium system dependencies
on the VM as an administrator with `playwright install-deps chromium` when
installing or updating Playwright; the workflow downloads Chromium as the
runner account. Keep Supabase keys and `AMS_LIVE` out of CI. Fork PRs skip
these jobs: inspect their changes before bringing them onto an internal branch.

Inspect the service with `systemctl status workbench-runner-ams` inside the VM;
use GitHub job details to verify the actual runner and tested commit.
[CI context](workbench/wiki/context-shared-ci.md) records the owner's requirement.

## Version control and publication

Non-site work: branch, commit each step, push, PR into `main`, merge-commit once current and checked; delete the branch. Site work goes feature -> `dev` -> `main`; agents merge into `dev` once CI `site builds` passes; only the owner merges `dev` -> `main`. Report local, pushed, merged and deployed states separately.

## Recovery

Reopen the owning Spec/Task and Wiki; verify live state. Adoption rollback: `workbench/sessions/recovery/adoption-recovery.json` (local).
