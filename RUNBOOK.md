# AMS - Runbook

> From LLM Workbench v3.2.2.

## Get oriented

`git status --short --branch`; preserve others' work. Read [AGENTS](AGENTS.md),
[GLOSSARY](GLOSSARY.md), relevant [Wiki](workbench/wiki/MEMORY.md),
[TASKBOARD](TASKBOARD.md) and assigned Spec/Task. [ARCHITECTURE](ARCHITECTURE.md#routes)
routes owners; load the [skill](workbench/docs/SKILLS.md).

## Workflows

Jot intent/corrections with sources in Wiki; requirements in Spec.
Use `map` -> `plan` -> `journey`, or authorized `orchestrate`. Retain proof/failures.

Website RSI: [record workflow/process issues](workbench/feedback/REPORT_FORMAT.md),
fix skills, prove before/after in [RSI records](workbench/research/IMPROVEMENT-TEMPLATE.md)
and [evals](evals/), then [show the log](site/PAGE-TEMPLATE.md).
Repair `KaydenClark/skills`. Owner instruction (2026-11-02) authorizes qualifying
repairs in the machine personal catalog used to build this website, never an
AMS-specific skills folder or other projects.
Handoffs: local ignored `workbench/sessions/handoffs/`; publish Tasks/safe proof.

## Test And Build

`uv run pytest`; `AMS_LIVE=1` adds live Supabase tests. `uv run ams-board`
serves [Grill Board](grill-board/README.md) on loopback only. Checks:

```bash
node workbench/tools/spec-workbench.mjs render
node workbench/tools/spec-workbench.mjs doctor
node workbench/tools/spec-workbench.mjs next --json
node workbench/tools/workbench-layout.mjs validate --project "$PWD"
git diff --check
uv run ams-hygiene [--site site]
```

Render: no diff; doctor: no blockers. Repeat checks/pytest
on a fresh candidate clone.

B checks (never print keys): `uv run ams-keycheck`;
`ams-writer record-merge|readcheck SHA`; after each merge `ams-history import`,
then `ams-history readcheck --ref SHA --dev-ref origin/dev`. Refresh rows
with `ams-history import --refresh-changed` before readcheck. `ams-rsi livecheck`
and `ams-sources livecheck` check RSI/source rules.

`ams-assess score|record|list` handles local r1 packets;
`ams-assessment-store import|readcheck|livecheck` checks private Supabase storage
([contract](evals/ASSESSMENTS.md)). Storage proves no benefit. Trials use the
subscription meter; unknown stays unknown.
[Trial preparation](evals/TRIALS.md) never calls a model.

## Clean up

Follow `land` and [AGENTS' delivery rules](AGENTS.md#delivery-and-recovery):

1. Inspect `git status --short --branch -uall`, index, refs and `git worktree list`;
   inventory owned ignored evidence.
2. Commit/push owned changes; verify remote SHA.
   Merge checked work to its target; fetch/prove containment.
   Keep unfinished work pushed on its Spec Feature branch with draft PR/next action.
3. Guard cleanup of contained temporary branches/worktrees. Preserve
   active writers, unique commits and needed ignored recovery material.
4. Reconcile owners/next actions; render TASKBOARD; rerun affected checks.
   Verify clean owned checkouts; name retained items/owners/reasons.
   Report blocked publication/cleanup; never stash/discard or commit others' work.
