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

## Current delivery model, 2026-11-06

The [exact confirmed repair scope](#jot-bc41fc6e-de68-4769-b8e6-0419470558c5) establishes bounded delivery branches independent of Landmark/Spec lifetime. Tasks can belong to Specs or directly to Landmarks; ordinary project maintenance uses its real owner. Ready project records/non-site work reaches main; website work reaches dev under the unchanged owner promotion gate. Verified delivery, owner reconciliation and guarded cleanup close a change branch while parent acceptance may remain open.

[RUNBOOK](../../RUNBOOK.md#delivery-and-recovery) and [SKILLS Delivery](../docs/SKILLS.md#delivery) govern the route. The [RSI repair record](../research/IMPROVEMENT-bounded-delivery-2026-11-06.md) owns source, qualification and adoption evidence. The manifest keeps main as default/general integration and explicitly permits main/dev verification targets. The earlier S-011 continuing-branch instruction and premature PR208 model are historical, superseded for new work by this owner-confirmed scope; unrelated unfinished candidates remain preserved. Adoption details below retain their original dates and observations.

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
### JOT-bc41fc6e-de68-4769-b8e6-0419470558c5
Kind: intent
State: confirmed
Recorded: 2026-11-06T22:27:21.085Z
Author: Kayden
Source: Kayden direct confirmation and scoped execution/publication/installation authorization, 2026-11-06
Topic: workbench-adoption
Supersedes: none

**Summary**

The proposed scope is a coordinated repair across **`KaydenClark/skills`**, its bundled runtime, the active skills installation and **AMS**.

The governing model is:

- **Landmarks and Specs own outcomes and requirements. Tasks own bounded execution and proof.**
- **Branches carry related, deliverable changes and close after verified delivery.** They do not remain open merely because their Spec or Landmark remains open.
- Ready project records and non-site changes merge into **main**.
- Website changes merge into **dev**. Their temporary branches can then close. Website promotion from dev into main remains owner-controlled.
- Landmark-only and project-wide work use their appropriate existing owners; they do not require artificial Specs.
- Unfinished work is committed and pushed for recovery, without treating recovery as merge readiness.

This readback proposes implementation and delivery **only after your confirmation**.

**The why**

The current workflow contains conflicting instructions, incomplete support for multiple delivery destinations and Spec-only assumptions in some procedures.

The repair must make the model consistent from assignment through cleanup. Changing prose without executable support would leave unsupported operations; changing runtime without correcting the instructions would leave agents following incompatible workflows.

**The intended result**

### 1. Shared skill changes

Changes are authored in a separate checkout of **`KaydenClark/skills`**, preserving the active installation.

| Package | Files and changes |
|---|---|
| **`orchestrate`** | Update `SKILL.md` and `references/workbench.md`. Replace mandatory continuing Spec branches with bounded delivery branches. Every assignment identifies its owner, branch, destination, writer boundary, verification and endpoint. Support existing Landmark-owned Tasks. Use temporary assembly branches only where changes cannot safely integrate independently. Preserve whole-destination review and acceptance. |
| **`journey`** | Update `SKILL.md` and `references/workbench.md`. Resolve the assignment’s branch and destination instead of automatically reusing a Spec branch. Preserve claims, receipts, checks and Task closure. Close delivered branches independently of parent completion; retain unfinished work and protect other writers. |
| **`land`** | Update `SKILL.md` and `references/workbench.md`. Cover Spec changes, Landmark changes and standalone maintenance through the complete sequence: establish owner and authority, preserve recovery, verify, merge, prove containment, reconcile evidence and clean up. Use the actual authorized destination, including dev. |
| **`setup-workbench`** | Update reached package instructions and generated `AGENTS.md`, `RUNBOOK.md`, `docs/SKILLS.md`, `GLOSSARY.md` and chats-and-roles articles. Remove the assumption that a Dispatcher’s Spec requires one continuing branch. Generate coherent delivery and closeout instructions. |

Land’s existing guarded-cleanup protections remain. The repair does not weaken checks, reviews, ownership rules or publication boundaries.

### 2. Runtime changes

The source changes happen under:

`setup-workbench/assets/runtime/workbench/tools/`

The bounded runtime work is:

- **`spec-workbench.mjs`:** Support recording a landing against an explicitly declared delivery destination while retaining exact-SHA, containment and content checks. Preserve the distinction between intermediate delivery and final Spec completion on the default branch.
- **`workspace-closeout.mjs`:** Support Spec Tasks, existing Landmark Tasks and bounded project work associated with a real owning record. Bind closeout evidence to the actual delivery destination rather than assuming one global integration branch.
- **Route declaration and validation:** Provide one validated project declaration for permitted delivery routes, extending manifest handling only as needed. Tool arguments must not silently nominate arbitrary destinations.
- **Claim coordination:** Reuse its existing Task-branch capability. Correct it only where focused verification demonstrates a conflict with the declared branch or target.
- Update affected command documentation, tests, package inventory and integrity receipts through the existing packaging mechanism.

This does **not** introduce a new tracker, standalone Task system, branch registry, cleanup service or dependency.

### 3. Enforcement and removal of contradictions

Responsibilities are explicit:

- **Project controls** establish scope, destinations and authority.
- **Skills** execute their part of that declared workflow.
- **Runtime** checks structural facts such as ownership, branch state, commits, destinations and containment.
- **Human judgments and authorization** remain sourced decisions; tools cannot manufacture them.

Inspect all reached instructions, templates and runtime consumers—not only the four entry-point files. Correct contradictory current claims, including parent ownership and branch-lifetime assumptions. Preserve historical decisions with explicit supersession.

If that inspection exposes a necessary change outside this bounded workflow repair, report it before expanding scope. Do not rewrite unrelated skills.

### 4. AMS adoption

Apply the verified catalog/runtime repair through the supported update procedure, preserving project customizations.

Reconcile:

- **`AGENTS.md`** — authority and routing.
- **`RUNBOOK.md`** — delivery, recovery and cleanup.
- **`workbench/docs/SKILLS.md`** — method responsibilities and project exceptions.
- **`workbench/manifest.json`** — main as default/general integration, with the supported website-dev route.
- **Existing delivery decision** — sourced amendment superseding incompatible rules.
- **Wiki adoption topic, chats-and-roles article and `MEMORY.md`** — exact confirmed intent, explanation and navigation.
- **Installed tools and receipts** — adopted from the checked package rather than independently patched copies.

Reconcile my premature policy edits and supersede PR #208 without merging its obsolete model. Preserve its historical commits and unrelated unfinished work.

### 5. Verification

Verify both instruction consistency and observable behavior.

Required cases:

1. A completed Task merges and its branch closes while its Spec remains open.
2. A Landmark-owned Task delivers without an artificial Spec.
3. Standalone CI and documentation changes reach main and close out.
4. Website work reaches dev and its branch closes without authorizing production promotion.
5. Ready records publish independently of unfinished implementation.
6. Dependent changes can use a temporary assembly branch and clean it up after delivery.
7. Wrong destinations, moved tips, uncontained work, competing writers and unpreserved local material prevent unsafe closeout.

Use focused regression tests for changed runtime behavior, existing setup/package tests, catalog validation and whitespace checks. Exercise representative skill instructions against these scenarios; a text search alone does not establish behavioral consistency.

After AMS adoption, run its applicable runtime, record, Wiki, hygiene and CI checks. Record failures and limits accurately. Do not claim owner Human QA or broad skill qualification from these checks.

**What I will do**

After confirmation of this scope:

1. Author and verify the coordinated catalog repair on a short-lived branch.
2. Publish a PR to **`skills/main`**, satisfy required checks and review, merge, and verify the resulting published revision.
3. Update the active catalog through its registered maintenance route. Preserve its location, discovery links and separately sourced imports.
4. Adopt the checked runtime and reconcile AMS through a bounded PR to **AMS main**, excluding unfinished implementation and website promotion.
5. Verify published results, reconcile completion evidence and safely clean up only this repair’s delivered branches and worktrees.

The endpoint is a **published, installed and verified workflow repair**, with any remaining blockers explicitly reported.

Existing unfinished-branch consolidation, unrelated Spec acceptance and production website promotion are excluded. **No changes will begin until you confirm this full scope.**
<!-- /jot-entry -->

<!-- jot-entry -->
### JOT-3a2975df-e456-4141-bf6b-27ae716f1f98
Kind: intent
State: confirmed
Recorded: 2026-11-06T23:53:37.053Z
Author: Kayden (owner words); Codex (filing context)
Source: Kayden, AMS chat 2026-11-06, exact full-scope confirmation and later delegation instruction; S-011 clerical filing by Codex
Topic: workbench-adoption
Supersedes: none

Owner authorization, Kayden's AMS conversation, 2026-11-06. Exact confirmation and execution instruction for the unchanged readback at [JOT-bc41fc6e-de68-4769-b8e6-0419470558c5](#jot-bc41fc6e-de68-4769-b8e6-0419470558c5):

> Confirmed. Implement the full scope across the skills, runtime, and AMS, verify the workflow, and carry it through publication, installation, and cleanup. Keep website promotion and unrelated unfinished work untouched.

The owner also instructed, exactly:

> Record the changes to the skills for the RSI Loop, and you can merge the skills into Kaydenclark/skills once they are stable or excellent and meet the requirements and dont fail with any of the recorded failures

> Every time we edit the skills and AMS, its for the RSI.

Administrative filing by Codex, not an owner quotation or newly confirmed requirement: S-011 is the existing Workbench destination for this bounded shared-delivery repair. Filing the already confirmed scope here supplies its stable owner identity; it does not claim that Kayden spoke that ID, approve this agent's mapping as new intent, or accept the whole older Spec. The exact readback and its confirmation remain unchanged. Its reached-instruction consistency requirement covers the remaining generic README/Specs-and-Tasks template correction; subsequent AMS adoption depends on verified published and installed source.

The owner's later tool-linked instruction requires root to be Director, delegate execution to Dispatchers, have them coordinate implementors, and complete Map/Plan before the remaining Journey. This sentence reports that instruction; it is not presented as a replacement exact quotation. Earlier missing preparation remains FAIL-201, with no backdated claim. The older TK-002/TK-003 campaign, frozen Terra/benefit criteria, website promotion, unrelated unfinished work and broader rollout remain excluded. This capture records existing scoped confirmation and execution authority, not Human QA, implementation evidence, acceptance or a new grant.
<!-- /jot-entry -->
