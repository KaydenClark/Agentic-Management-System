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
| [YYYY-MM-DD] | [Doc / section] | [What happened] | [Impact] | [Proposed change or open] | [Status] |

Record open, investigating, disposition-recorded or superseded; link the report and its sourced [disposition](../../GLOSSARY.md#feedback-dispositions). Status alone never proves repair or improvement. Link an [RSI record](../research/IMPROVEMENT-TEMPLATE.md) when testing a change.

## What Belongs Here vs. TASKBOARD

- This project's own work, bugs, and Tasks -> owning Spec/Task records, projected by `TASKBOARD.md`.
- Problems with the *harness rules themselves* -> here.

If a harness problem is also blocking this project right now, log it here **and**
record a Task under its owning Spec for the local workaround, linking the two.
