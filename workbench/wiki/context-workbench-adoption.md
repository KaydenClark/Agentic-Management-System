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
| Eight root controls | Fold: reconciled in place to package formats; AGENTS, ARCHITECTURE and RUNBOOK pruned under 3,000 characters, owner rules were intended to be kept; the fidelity gaps below remained |
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

## Recovery accounting — 2026-11-02

The owner confirmed that AMS should recover the Workbench as an agentic management system with RSI, and that the private CONTINUE route conflicts with that model ([corrections](context-owner-answers-coherence.md)). The pinned legacy [AGENTS](https://github.com/KaydenClark/LLM_Workbench/blob/9d5e1f25b0d5870589ae1c5752f27f42acb796ef/AGENTS.md), [system definition](https://github.com/KaydenClark/LLM_Workbench/blob/9d5e1f25b0d5870589ae1c5752f27f42acb796ef/workbench/docs/ddr/000T-the-workbench-is-an-agentic-management-system-not-a-harness.md), [recursive delivery](https://github.com/KaydenClark/LLM_Workbench/blob/9d5e1f25b0d5870589ae1c5752f27f42acb796ef/workbench/docs/ddr/000A-the-workbench-aligns-to-the-owner-s-concept-and-delivers-on-it-recursively.md), and [Wiki history](https://github.com/KaydenClark/LLM_Workbench/blob/9d5e1f25b0d5870589ae1c5752f27f42acb796ef/workbench/docs/ddr/001M-current-state-documents-carry-no-history-narrative-the-wiki-holds-the-project-s-history.md) were inspected at that immutable revision. The object is unavailable in the local Git database; a dirty legacy checkout is not evidence of that revision.

| Area | Current evidence and limit |
|---|---|
| AGENTS duties | Partially adapted; the ten dropped and six changed lines above remain the historical accounting. Current control restores skill routing, scope readback, carry, claim and behavioral-test guidance; equivalence of all obligations is not proven. |
| Continuation | The private CONTINUE pointer contradicted the newer owner correction; current routing uses Spec/Task, Wiki and ignored handoffs. |
| Spec history | Spec-to-Wiki history implementation is retained; the Adoption Spec evidence row remains owed. |
| Tools and skills | Coordinator inspection found all 41 managed files match their receipt. The installed receipt source SHA `95d3c0c1cb98a0d1746fab9278a70bc719d9ea2af115bd38eac45db46c7d2f77` differs from the locally available package SHA `99080edd8e061ba6b1b142e27088338914b591cee27a7c5725383d405af7ceb2`: 11 tool hashes differ and spec-history was added by authorized update `0b58148359ae43ec9c15300414b4230c9dcc9b5a`. Preserve that update. Current sessions explicitly loaded orchestrate, carry, journey, plan and jot; automatic discovery and other host activation remain unverified. |
| Recursive delivery | The destination is retained; composed delivery remains partial or unknown. |
| Acceptance | Checks, independent Review and owner Human QA remain distinct; no owner acceptance follows from this reconciliation. |
| Website | The evidence surface is retained; a complete learning cycle and behavioral benefit remain unproved. |

This accounting is not a complete adoption audit or a claim that S-013 detection or S-007 presentation acceptance has passed. The bounded checker repair and later assembled evidence remain separate work.
