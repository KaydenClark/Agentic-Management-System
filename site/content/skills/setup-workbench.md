---
name: setup-workbench
summary: Builds a project's Workbench, adopts an existing repo into one, updates an installed one, or checks it read-only, while keeping the work already there.
pin: 878241202bf7ec97c0952287f1633f6f0ddf1a6e
credit: adapted
credit_text: Workbench setup procedures and runtime by Kayden Clark, MIT License. The bundled runtime also carries files derived from [Matt Pocock's skills](https://github.com/mattpocock/skills), MIT License.
credit_license: MIT
---

## What it does

Setup-workbench prepares a project so the rest of the catalog has somewhere to work. That somewhere is a **Workbench**: project files that tell agents the rules, hold the queue of work and explain how to verify it. A **Spec** records one capability with its acceptance criteria and evidence. A **Task** is a bounded slice of a Spec that one agent run can finish.

A finished Workbench is more than a folder scaffold. It has eight filled root files (`README.md`, `AGENTS.md`, `CLAUDE.md`, `BLUEPRINT.md`, `ARCHITECTURE.md`, `GLOSSARY.md`, `RUNBOOK.md` and a generated `TASKBOARD.md`), routed knowledge, a feedback log, Spec and Task records, and working lifecycle tools.

The skill inspects the project first, then a read-only classifier names the mode. Its verdict is evidence, not permission to write.

| Mode | Starting state | What happens |
|---|---|---|
| **Create** | An empty project, or a fresh Template copy you chose | A founding prompt becomes the root files, a minimal scaffold that runs, and a first Spec |
| **Adopt** | Existing code, history or a scaffold with no installation record | Existing intent and history move into the Workbench layout, after a dry run on a throwaway copy |
| **Update** | An installed Workbench taking a newer package | Records a before state, migrates additively, backs up tools before replacing them |
| **Check** | An installed Workbench, assessed without repairs | Compares installed identity with the package, runs diagnostics and verify operations, and reports each finding with the authority a repair needs |

Create and Adopt end with one actionable first Spec. Ready Tasks come with it only when planning is authorized; otherwise the setup records a readiness gap.

Adopt and Update give each old steering document a disposition: **Port** moves project truth to its current owner, **Fold** moves live rules into a control such as `AGENTS.md`, **Keep** leaves referenced material in place, and **Retire** sets aside competing authority once reconciled. Nothing is copied over an existing control, and your decisions, in-flight claims, finished proof and record IDs survive.

Everything ships inside the skill, and a damaged package is refused (`invalid-skill-package`); reinstall it rather than regenerate its inventory. Installed tools get a **receipt**, a record of their file hashes. The installed Workbench has its own command, `workbench/tools/spec-workbench.mjs`: `render` regenerates the Taskboard, `doctor` lists findings that block work, and `next --json` names the next eligible Task.

Methods such as `map` and `journey` live in your shared catalog, not in each project. Setup prepares a discovery link (`.claude/skills` pointing at `.agents/skills`) and checks that required methods resolve; it copies no skill. Setup work lands through a feature-branch PR into `main`, and a commit-guard hook stops an agent from ending a turn with unsaved work.

## When to use it

Reach for it when a project has no Workbench, a repo should join one, an installed Workbench should take a newer package, or you want a read-only diagnosis. Other Workbench skills send you here when the manifest or lifecycle tool is missing.

| What you have | Reach for |
|---|---|
| An unclear next step in a project that already has a Workbench | [ask-workbench](/skills/ask-workbench) |
| A broad fitness review of a Workbench | [audit-workbench](/skills/audit-workbench) |
| Two harness variants to compare on outcomes | [evaluate-workbench](/skills/evaluate-workbench) |
| A repeatable harness gap to fix with measurement | [improve-workbench](/skills/improve-workbench) |
| A working Workbench and a destination to describe | [map](/skills/map) |
| A working Workbench and a Spec to break into Tasks | [plan](/skills/plan) |

## Example request

> This repo has code and history but no Workbench. Classify it, tell me which mode applies, show me what you would change and what you need me to decide, and don't write anything until I approve. We merge feature branches into main through PRs.

Expect an Adopt verdict, a Port, Fold, Keep or Retire label on each existing doc, and the concrete changes plus blocking choices, all before a write.

## What it requires

- **Node.js 20 or newer and Git**, plus the skill's own install directory used by absolute path.
- **A clean recovery point.** Adopt branches from a clean commit and refuses a dirty tree. That commit is the **recovery SHA**, the state you can roll back to.
- **An existing authorized backup directory** for Adopt, Update and tool updates.
- **The personal catalog**, reachable by your host, with all sixteen required methods. Setup leans on [map](/skills/map) for the first Spec, [grilling](/skills/grilling) to confirm the architecture codemap row by row, and [domain-modeling](/skills/domain-modeling) for the authority decision record. A cloud session cannot see your local skill folders.
- **Owner answers**, asked only when an unresolved choice blocks the next action. For project authority it asks who holds each of eight rights (scope, merge, release, spend, privacy, assignment, conflict, shared writers), again only when a missing right blocks the next step.

## What it does not authorize

- **Product implementation.** Building the product stays the project's work.
- **Writing from inspection alone.** Classification is not permission to change files.
- **Merging, release or deployment.** Finishing setup is not approval to merge or release. The merge right comes from the project's recorded authority. Setup also grants no **Human QA**, a person's own check of the result. Converting a separate staging branch to `main` needs your go-ahead.
- **Publishing.** No creating a remote or changing visibility without authority.
- **Changing your personal skills, or hand-editing managed state.** It never hides or replaces a skill to clear a name clash, hand-copies tools, or edits receipts.
- **Weakening checks.** Zero findings is never reached by deleting skills, receipts, records or evidence.

## FAQs

### How do I know which mode I am in?

The classifier's verdict decides: genesis means Create, adoption means Adopt, upgrade means Update, and Check is the read-only route for an installed Workbench. A scaffold with all the right file names but no installation record is still Adopt, and a real project is never relabeled a template copy to skip Adoption.

### Why did setup refuse to start with a dirty working tree?

Adopt needs a clean, committed starting point so there is something to roll back to. The skill never stashes, discards or absorbs someone else's changes. Git cannot restore ignored files, so archive them outside the project before a migration that moves whole folders.

### What do blocked and partial results mean?

On the adoption and update routes, `blocked` is normally a refusal before any write, but check what was created before you retry. Adopt stops with `adoption-rehearsal-failed` if its dry run fails. `partial` means a failure after real writes, for example a legacy **Lexicon** (an old root vocabulary file whose meanings must move into the glossary and architecture files) still needing reconciliation. Keep the output, read the named cause and recovery SHA, and recover in a separate worktree, never by resetting your main checkout.

### What if my project already has skills with the same names as the catalog?

The personal skill wins. The project copy is reported as a **shadow**, never overwritten or deleted, and readiness stays blocked until it is reconciled. The check inspects `.agents/skills`, `.codex/skills`, `.gemini/skills` and `.github/skills`. Merge it into the real owner, or rename a genuinely distinct extension.

### Does passing setup prove the agents will use the skills?

No. Package checks and skill listings do not show that your host loads the skills. Invoke a harmless method in the real host and observe its loaded path and version; until then, activation stays unverified.

## It's working when

- Classification only reads, and the mode you are told matches the project's actual state.
- Before any write, you see the changes and the choices that block them.
- Existing controls, IDs, decisions and evidence are intact afterwards.
- `render` is deterministic, `doctor` reports nothing blocking, and `next --json` returns an eligible Task or `null` for a named gate.
- Tool and catalog verification pass, with no clash between project and personal skill names.
- The closing report separates local, committed, pushed, reviewed and merged states and names every missing condition.

## Where it fits in the workflow

Setup-workbench sits in the Route stage as a supporting skill, and it comes before everything else in a project. [ask-workbench](/skills/ask-workbench) checks for the Workbench before routing and tells you to run this skill if the manifest or lifecycle tool is missing. [map](/skills/map), [plan](/skills/plan), [orchestrate](/skills/orchestrate) and [journey](/skills/journey) carry the same requirement.

After setup, work moves to that ordinary loop. The wider fitness review goes to [audit-workbench](/skills/audit-workbench), outcome comparisons to [evaluate-workbench](/skills/evaluate-workbench), and measured repair of a reusable gap to [improve-workbench](/skills/improve-workbench). A change to the setup package itself belongs in the shared catalog, through improve-workbench and [author-skill](/skills/author-skill).
