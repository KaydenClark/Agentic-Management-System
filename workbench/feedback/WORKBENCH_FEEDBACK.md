# Agentic Management System - Workbench Feedback

> AMS template adapted from LLM_Workbench `templates/WORKBENCH_FEEDBACK.md` at `227d7c2a3ca0`. This is a starting format, not evidence of installed software, approved AMS policy, or completed work.

This is the feedback log for the AMS work structure.
When the control docs themselves (`AGENTS.md`, `BLUEPRINT.md`, `GLOSSARY.md`,
`ARCHITECTURE.md`, `TASKBOARD.md`, `RUNBOOK.md`) are unclear, wrong, missing guidance, or actively
slow the work down, record it here instead of silently working around it. Changes can be evaluated through `evals/` using the evaluation templates; automated execution remains unimplemented; no improvement is claimed by this template.

This log is append-only. Do not edit or delete prior rows; add a new one.

## How To Log

Add a row whenever the AMS work structure caused
friction or could be improved. Keep it concrete: name the doc and section, say
what happened, and propose a change if you have one.

| Date | Doc / section | What happened | Impact | Proposed change | Status |
|---|---|---|---|---|---|
| 2026-11-01 | setup-workbench Adopt / budgets | AGENTS, ARCHITECTURE and RUNBOOK already exceeded the 3,000-character root limit, and the package AGENTS template itself is 3,082 characters, so restoring every template line beside AMS rules cannot fit. No tool enforces the budget at doctor time. | Fidelity divergences remain (10 dropped, 6 changed AGENTS lines) | Ship a template under its own budget, or enforce the budget in doctor; record the AMS divergences in an ADR | open |
| 2026-11-01 | setup-workbench Adopt / migration preflight | The first migration refused `sessions-not-ignored` because the scaffold's root `workbench/sessions/*` rule hid the lane's own ignore file and notepad templates. | One extra reconcile-and-commit round | Name the required ignore shape in adopt.md before migration | open |
| 2026-11-01 | Wiki validation / scaffold templates | AMS Wiki templates with placeholder frontmatter inside `workbench/wiki/` failed `invalid-note` (30 errors) after adoption; the schema has no exemption for templates. | Templates had to be retired to `archive/` | Let the validator skip `*-TEMPLATE.md`, or document where room templates belong | open |
| 2026-11-01 | Adopt / host settings | The procedure requires `Edit` allow rules in `.claude/settings.json`, but the agent's write was refused by the host's auto-mode classifier as self-modification. | `permission-scope-drift` stays a non-blocking doctor error until the owner edits the file | Owner applies the rules; setup-workbench should tell agents this edit needs the owner | open |
| 2026-11-01 | specs / TASK-TEMPLATE.md | The earlier agreed `T-NNN` Task naming conflicts with installed tooling, which writes and reads `tasks/TK-###/TASK.md`. | A ported Task in `T-NNN` form would not be record-backed | Owner decides; then align the template | open |
| 2026-11-01 | Adopt / branches | The manifest `git` block accepts only `defaultBranch` and `integrationBranch`; a separate `dev` deploy branch for Vercel cannot be declared. | Deploy-branch policy needs another owner (Runbook or a decision record) | Add a deploy-branch field to the package, or record it outside the manifest | open |
| 2026-11-01 | Coherence sweep (S-013) | Orchestrator C's first sweep found harness-rule issues: CDR contradictions and bundling, no owner-item-to-CDR map, unenforced README budget, whole-Spec-only blockers, doctor/claim disagreement on `personal-catalog-unavailable`, managed `workbench/tools` refusing project checks | See report; nothing silently fixed | Per finding in [COHERENCE-2026-11-01](coherence/COHERENCE-2026-11-01.md) (COH-001 to COH-018) | open |

Record open, investigating, disposition-recorded or superseded; link the report and its sourced [disposition](../../GLOSSARY.md#feedback-dispositions). Status alone never proves repair or improvement. Link an [RSI record](../research/IMPROVEMENT-TEMPLATE.md) when testing a change.

## What Belongs Here vs. TASKBOARD

- This project's own work, bugs, and Tasks -> owning Spec/Task records, projected by `TASKBOARD.md`.
- Problems with the *harness rules themselves* -> here.

If a harness problem is also blocking this project right now, log it here **and**
record a Task under its owning Spec for the local workaround, linking the two.
