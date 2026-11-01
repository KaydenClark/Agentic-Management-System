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
| 2026-11-01 | RUNBOOK version control / land cleanup | **Owner-recorded failure:** the AMS did not keep the repository clean. At 15:58Z `origin` held 62 branches besides `main` and `dev` for 6 active Specs: 41 fully merged into `main`, 14 merged into `dev` only, 7 unmerged. At the first coherence sweep (13:22Z) about 15 PR branches existed. Merged branches are never deleted; `dev` was 88 ahead and 72 behind `main`, past the 20-commit drift threshold. | The branch list no longer shows live work; owner counted it as a failure of the AMS | Delete a branch once its PR merges (`gh pr merge --delete-branch`), add a branch-count-per-active-Spec check to the S-013 drift sweep, and treat this as a failed result that may seed an S-002 round | open |
| 2026-11-01 | S-007 RSI chart pages / Alignment Check (audit-workbench r1) | **Owner request not done:** the owner asked a coordinator session to score the AMS with a Workbench Fitness Assessment and put the results on the website. Instead it built a private dashboard of build-activity counts. No fitness score of the AMS exists. What is needed: (1) an Alignment Check r1 drift audit, three independent runs, scored per audit-workbench `references/alignment-check.md`, at two pinned commits: pass 1 `8b70874` (first coherence sweep, 13:22Z) and pass 2 the current `main`; (2) the frozen inventory, per-check run ledger, pooled score and `level:score` recorded in this repo; (3) the build-history writer carrying them to Supabase; (4) `/rsi` showing both passes' `level:score`, linked to their records, with the 0 graded RSI trials stated. Known blockers: the installed rubric file's SHA-256 is `05c5713e…` but r1 requires `96636d4a…`, so a score taken now is not a valid r1 result until that is resolved; `evals/` holds only templates; there is no `tools/audit-workbench.mjs` in this room; the `/rsi` live reader sits unmerged on `site/s007-tk002-rsi-live`. | The site cannot show whether the AMS is fit, which is its purpose | Assign the four steps above to S-007 (site) and a scoring owner; resolve the rubric hash first | open |

Record open, investigating, disposition-recorded or superseded; link the report and its sourced [disposition](../../GLOSSARY.md#feedback-dispositions). Status alone never proves repair or improvement. Link an [RSI record](../research/IMPROVEMENT-TEMPLATE.md) when testing a change.

## What Belongs Here vs. TASKBOARD

- This project's own work, bugs, and Tasks -> owning Spec/Task records, projected by `TASKBOARD.md`.
- Problems with the *harness rules themselves* -> here.

If a harness problem is also blocking this project right now, log it here **and**
record a Task under its owning Spec for the local workaround, linking the two.
