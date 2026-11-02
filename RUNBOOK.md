# AMS - Runbook

> From LLM Workbench v3.2.2.

## Get oriented

Run `git status --short --branch`; preserve others' work. Read [AGENTS](AGENTS.md),
[GLOSSARY](GLOSSARY.md), relevant [Wiki](workbench/wiki/MEMORY.md),
[TASKBOARD](TASKBOARD.md) and assigned Spec/Task. [ARCHITECTURE](ARCHITECTURE.md#routes)
routes owners. Load the [owning skill](workbench/docs/SKILLS.md).

## Workflows

Jot sourced intent/corrections in the Wiki owner; requirements go in the Spec.
Use `map`, `plan`, then `journey` for one Task or `orchestrate` for authorized
coordination. Retain proof/failures.

Website RSI: [record workflow/process issues](workbench/feedback/REPORT_FORMAT.md),
fix shared skills, prove before/after here in [RSI records](workbench/research/IMPROVEMENT-TEMPLATE.md)
and [evals](evals/), then [show the log](site/PAGE-TEMPLATE.md).
This project improves skills; it never installs them elsewhere.

## Test And Build

`uv run pytest`; `AMS_LIVE=1` adds live Supabase tests. `uv run ams-board`
serves the [Grill Board](grill-board/README.md) on loopback only. Room checks:

```bash
node workbench/tools/spec-workbench.mjs render
node workbench/tools/spec-workbench.mjs doctor
node workbench/tools/spec-workbench.mjs next --json
node workbench/tools/workbench-layout.mjs validate --project "$PWD"
git diff --check
uv run ams-hygiene [--site site]
```

Render: no diff; doctor: no blockers. Repeat checks and pytest
on a fresh clone at the candidate.

B's checks (keys never printed): `uv run ams-keycheck`;
`ams-writer record-merge|readcheck SHA`; after each merge `ams-history import`,
then `ams-history readcheck --ref SHA --dev-ref origin/dev`. Refresh rows
with `ams-history import --refresh-changed` before readcheck. `ams-rsi livecheck`
and `ams-sources livecheck` check RSI/source rules.

`ams-assess score|record|list` handles local r1 packets;
`ams-assessment-store import|readcheck|livecheck` verifies private Supabase storage
([contract](evals/ASSESSMENTS.md)). Storage proves no benefit. Trials use the
subscription meter; unknown stays unknown.
[Trial preparation](evals/TRIALS.md) never calls a model.

## Clean up

Follow `land` and [AGENTS' delivery rules](AGENTS.md#delivery-and-recovery):

1. Inspect `git status --short --branch -uall`, index, refs and `git worktree list`;
   inventory ignored evidence in owned checkouts.
2. Commit owned changes, push the exact branch and verify its remote SHA.
   Merge checked work to its authorized target; fetch and prove containment.
   Keep unfinished work pushed on its Spec's Feature branch with draft PR and next action.
3. Use guarded cleanup for contained temporary branches/worktrees. Preserve
   active writers, unique commits and needed ignored recovery material.
4. Reconcile owners and next actions, render TASKBOARD and rerun affected checks.
   Verify owned checkouts are clean; account for retained items with owner/reason.
   Report blocked publication or cleanup. Never stash/discard or commit others' work.
