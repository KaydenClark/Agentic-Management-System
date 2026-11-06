---
type: project
status: active
sensitivity: normal
knowledge_role: curated
provenance:
  - Kayden, owner instruction approved 2026-11-01, relayed by the AMS foundation coordinator
  - setup-workbench v3.2.2 Adoption run, 2026-11-01
source_paths:
  - workbench/manifest.json
  - workbench/tools/.workbench-tools.json
  - workbench/research/template-inventory.md
last_verified: 2026-11-01
---

# Workbench adoption

Record of the first Workbench Adoption of AMS: what ran, what moved where, what was checked and what remains open. It explains; the manifest, tool receipt and controls own the live state. A Spec evidence row for this Adoption is still owed (see Open gaps).

## Current branch and delivery model, 2026-11-06

The [owner's correction](#jot-9dad0413-d13a-4949-91c4-2b78574cbc39) establishes one
`feature/spec-####-<spec-name>` branch for each Spec creating new things, retained
for its entire lifecycle. Tasks, fixes, intent and docs share that branch.
Ready intent/docs reach main independently of unfinished implementation;
completed implementation reaches dev before main. Commit and push attributable
work instead of stashing it. Partial delivery does not close the Spec branch:
cleanup follows completion, verified merges and preservation checks.

[RUNBOOK](../../RUNBOOK.md#delivery-and-recovery) owns the procedure;
[SKILLS Delivery](../docs/SKILLS.md#delivery) explains selective record publication
and the unchanged owner-only website promotion gate. The manifest now names
`dev` as implementation integration and `main` as default/publication destination.
This supersedes the earlier direct-to-main implementation route and generic
per-Task branch defaults. The adoption snapshot below remains historical;
existing branches have not been renamed or consolidated by this rule update.

## Request and scope

Kind: intent. State: confirmed. Source: Kayden, owner instruction approved 2026-11-01: "Run `setup-workbench` (mode Adopt) on the AMS repo; verify `render`, `doctor` and `next`; merge through a checked PR." The coordinator excluded product Specs, landmarks and decision records from this step: porting S-001/S-003, their decisions and landmarks follows in the next PR.

## Mode, package and recovery

- Classification: `adoption` — an ordinary `workbench/` scaffold without manifest, version stamp or installed tools; all eight controls present, none bracketed.
- Package: `https://github.com/KaydenClark/skills.git` `setup-workbench` v3.2.2, SHA-256 `99080edd8e061ba6b1b142e27088338914b591cee27a7c5725383d405af7ceb2` (lineage: LLM_Workbench `9d5e1f25b0d5`). Node.js v26.3.0, Git 2.54.0.
- Recovery point: `main` at `49d4999` (published on origin). Migration rollback record: `workbench/sessions/recovery/adoption-recovery.json` (ignored, local to the adopting checkout).
- Branches: `git.defaultBranch` and `git.integrationBranch` are both `main`. The manifest `git` block accepts only those two keys, so a separate `dev` deploy branch cannot be declared there.
- Baseline: no product suite existed (`unavailable`, nothing to run); the scaffold's only checks were document checks.

## Port, Fold, Keep, Retire

| Item | Disposition |
|---|---|
| Eight root controls | Fold: reconciled in place to package formats; AGENTS, ARCHITECTURE and RUNBOOK pruned under 3,000 characters, all owner rules kept |
| GLOSSARY feedback-disposition table | Port into Language terms (parser forbids other sections) |
| Notepad JSON examples | Port to `workbench/sessions/notepads/templates/` (byte-identical to the package) |
| Session ignore rule | Fold: root rule now re-includes lane subfolders; `workbench/sessions/.gitignore` keeps live contents local |
| ADR/DDR templates, `workbench/decisions/` | Retire to `archive/ams-scaffold-templates/`; `adr.mjs new` writes `workbench/docs/adr/` and `workbench/docs/ddr/` |
| Five Wiki templates | Retire to the same archive; their frontmatter vocabulary fails the [schema](SCHEMA.md) |
| Spec, Task, review and Human QA templates; research, eval and site templates | Keep in place |
| `require-committed` Stop hook | Keep as the commit guard; the package's `git-save-guard.py` was not added to avoid a second Stop hook |
| Pre-adoption ARCHITECTURE ownership table | Retire to Git history at `49d4999`; the condensed table keeps each owner |

## Verification (candidate before PR)

- `render` twice: identical `TASKBOARD.md`. `doctor`: no blocking finding. `next --json`: `null`; the Taskboard names the gate (no Spec yet; port follows). `workbench-layout.mjs validate`, `tools verify` and `skills verify`: valid. `git diff --check`: clean.
- Disposable lifecycle on a clone: confirmed Jot -> landmark with child Spec S-001 -> `convert-tasks` -> `claim --local` -> refusals (second claim, missing `--proof`/`--docs`/`--remaining-gap`, unpushed state, claim without Confirmation/Execution approval) -> `close` -> render showing the acceptance gate. Legacy IDs (`S-001`, `LMK-001`) and top-level `workbench/specs/S-003-slug/` both render.
- Host activation of personal skills: unverified (`skills verify` checks presence only).

## Open gaps

- No Spec owns this Adoption, so its evidence row is owed; add it when S-001/S-003 are ported.
- `doctor` reports `permission-scope-drift`: `.claude/settings.json` needs `Edit` allow rules for the authorship lanes. The agent's edit was refused by the host's permission classifier; the owner must add it.
- AGENTS fidelity: ten template lines dropped and six changed to fit the limit (personal-skill-first, `carry`, `claim`, pre-edit readback, Task-review policy, closeout). Restore them or record them in an ADR.
- `TASK-TEMPLATE.md` keeps the earlier agreed `T-NNN` naming; installed tooling uses `TK-###`.
- Legibility `run`, `journey`, `measure` are bracketed gaps until an application and eval runner exist.

<!-- jot-entry -->
### JOT-9abd9e46-08ae-4283-a950-a96e6095759f
Kind: intent
State: current
Recorded: 2026-11-03T19:41:00.470Z
Author: Kayden
Source: Kayden, AMS chat, 2026-11-03
Topic: workbench-adoption
Supersedes: none

Owner correction: AGENTS.md still contains material that belongs elsewhere, specifically the three-strike rule. Authorized repair: keep core authority, safety and collaboration rules in AGENTS; route testing, CI, scheduling, RSI and delivery procedures to their existing owning documents. Relocation preserves the existing policies; this request does not retire the three-strike stop or authorize deployment.
<!-- /jot-entry -->

<!-- jot-entry -->
### JOT-9dad0413-d13a-4949-91c4-2b78574cbc39
Kind: intent
State: confirmed
Recorded: 2026-11-06T21:20:49.323Z
Author: Kayden
Source: Kayden direct AMS chat, 2026-11-06; intended branch model and instruction to update the recorded model first
Topic: workbench-adoption
Supersedes: none

Owner-defined model: One feature/spec-####-<spec-name> branch per Spec creating new things. All its Tasks, fixes, intent capture, and documentation use that branch. Intent and documentation are published to main as they become ready, while unfinished implementation stays on the Spec branch. Completed implementation is integrated into dev, then main, following applicable checks and existing website promotion authority. The Spec branch stays open until the entire Spec is completed; once its remaining work is merged and verified, clean up the branch. Commit and push attributable uncommitted work instead of stashing it; determine the safe destination and remaining checks before merging. Owner follow-up: update the recorded model and the instructions used first. This supersedes direct-to-main implementation and per-Task work branches; it grants no website dev-to-main promotion, Spec acceptance or cleanup of uncontained work.
<!-- /jot-entry -->
