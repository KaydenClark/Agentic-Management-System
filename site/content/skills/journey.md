---
name: journey
summary: Takes one assigned Task from first read to a pushed, checked candidate, with honest answers on whether it can merge and whether the Task is done.
pin: 878241202bf7ec97c0952287f1633f6f0ddf1a6e
credit: adapted
credit_text: Derived from Kayden Clark's Workbench Journey and adapted from [Matt Pocock's Implement skill](https://github.com/mattpocock/skills/tree/a496f5513d4a4cf889bc48e189e579f4b0bdf6aa/skills/engineering/implement), MIT License, reshaped around Task QA and submission boundaries. It is not an unchanged import.
credit_license: MIT
---

## What it does

Journey is the skill an implementing agent follows to carry **one Task** to a finished hand-back. A **Task** is a single bounded assignment for one implementor run. Its parent **Spec**, the written destination with its acceptance criteria, owns the larger goal across many runs, and a **landmark** is the bigger goal that groups related Specs. A **Workbench** is the set of records, tools and rules that [setup-workbench](/skills/setup-workbench) creates for a project. Journey works only inside one.

A run has four phases, always in this order.

**Implement** changes the real source or product. Where the behavior can be expressed as a test, Journey sends you to [tdd](/skills/tdd): see the test fail, make the smallest change, tidy up while green. Unknown causes go to [diagnosing-bugs](/skills/diagnosing-bugs) and unsettled interfaces to [codebase-design](/skills/codebase-design). Never weaken a test to get green. Docs and records are checked for accuracy and links instead of forced into artificial failing tests. New scope or a changed meaning goes back to the Map or Plan that owns the intent (see [map](/skills/map) and [plan](/skills/plan)). Intent is never bent to fit the code.

**Check** runs the project's automated tests, builds, linters and diagnostics against the exact candidate. Run focused checks while you work and the full required suite before you claim readiness. Reuse evidence for unchanged content, and rerun affected checks after any change. You write down the real commands, results, candidate and gaps. If a check cannot run, you say why and lean on the strongest other observation, never calling it a pass.

**QA** judges the Task against its intended outcome, beyond what the checks prove. You try a representative user or caller scenario, edge cases and the updated docs, and you inspect the resulting artifact. State what you observed, what you concluded and what you are unsure of. In-scope misses are repaired, then Check and QA repeat. Unmet acceptance leaves the Task incomplete even with every test green. QA also covers a self-review: your own pass over the change, what you claim about it, who else it affects and the docs. That self-review is neither independent Review nor the owner's **Human QA**, which is acceptance by a person.

**Submit** hands back the exact candidate and answers two separate questions.

1. Is it ready to merge? Name the target branch, the base and head commits, the checks and their results, any conflict or rebase state, and what is still unverified.
2. Is the Task complete? Say yes only when acceptance is met. Otherwise name the gap and say whether the fix stays in this run or becomes a fresh Task under the same Spec.

Before any of this comes a preflight. Confirm the Workbench exists, read the project instructions and the Task with its parent, and inspect the branch, worktrees and uncommitted work. Verify that dependencies are satisfied and who currently holds the **claim**, the Workbench record that a named agent (the claimant) owns the Task. A Task already in progress under you resumes from its recorded claimant, branch and proof, with no second claim. Claiming, updating and closing go through the Workbench's own tool.

## When to use it

Reach for Journey when you hold an eligible implementor assignment: a ready, specific Task you are authorized to carry out. That includes a corrective run, where a failed review has sent more work back to an open Spec. It does not cover reviewing the assembled result, since independent Review happens afterward on the whole Spec or landmark.

| What you have | Reach for |
| --- | --- |
| A destination or Spec that is not yet cut into Tasks | [plan](/skills/plan) |
| An objective to push through to an already-authorized endpoint | [carry](/skills/carry) |
| Several implementors to coordinate toward an endpoint | [orchestrate](/skills/orchestrate) |
| A finished candidate that needs merging, repair or cleanup | [land](/skills/land) |
| Finished work that needs an independent look | [code-review](/skills/code-review) |

## Example request

> Take the export Task under the export Spec through Journey. Implement it on its feature branch, run the full suite, QA it against the acceptance list, and hand it back with both answers.

## What it requires

- A Workbench, meaning that `workbench/manifest.json` and `workbench/tools/spec-workbench.mjs` both exist at the top level of the project. When one is absent, Journey halts and points you to [setup-workbench](/skills/setup-workbench). It will not create Workbench records by hand or use another tracker.
- An assigned, executable Task and its parent Spec. A planned Spec, or a bare row on the generated task board, is not an assignment, and the board grants no authority.
- Confirmation and execution authority that already exists within scope. Invoking Journey or seeing a ready label supplies neither.
- Satisfied blockers. Journey never clears one just to make a claim succeed.
- Companions it calls on as needed: [tdd](/skills/tdd), [diagnosing-bugs](/skills/diagnosing-bugs), [codebase-design](/skills/codebase-design), and [pr](/skills/pr) when a merge-request body is requested.

## What it does not authorize

- Invoking Journey or seeing a ready label does not give you the right to start or claim a Task. Existing authority has to cover that.
- A passing Task is not independent Review, owner approval, Human QA or a release, and neither is merging it.
- Closing a Task does not complete the Spec and does not replace Task acceptance. A Task with unmet acceptance is never closed.
- A refusal is a stop. A competing claimant, missing authority or a lifecycle refusal blocks that step, and editing records directly is not a way around it.
- A local hand-back is not remote recovery.
- Journey never deletes an uncontained branch, and it never merges a candidate that still awaits required review.

## Committing, pushing and merging

Stage only the paths you own, and commit after each logical step on the Task's own feature branch. Then push, and open a PR against the target branch (normally `main`), kept as a draft until the work is finished. Never end with work uncommitted, unpushed or stashed, and read back the remote commit and the PR's base, head and draft state.

Merging happens only when both Submit answers are yes. In that case the branch is first updated onto the current target, then the PR merges once required checks pass and no required review is pending, and finally containment in the target is proved. If an orchestrator assigned the merge to itself, the orchestrator performs it, and containment is still proved. When you are blocked, the candidate, finished work, failed checks, gap, writer and next action stay recorded with the existing work owner.

## FAQs

### Does a green test suite mean the Task is complete?

No. Check shows the tests pass, while QA asks whether the intended outcome and acceptance were actually met. If tests are green and acceptance is not, the Task is reported incomplete with the gap named.

### What happens if the claim, push or close step is refused?

Treat it as a stop, not an obstacle: report the gap and keep your progress. Close refuses dirty or unpushed state by default, so fix that or record a supported Git-state reason without inventing success.

### The review failed after I submitted. What now?

Corrective work returns to the open Spec. A repair in the same run continues under this Task, while a later implementor run gets a new bounded Task after the records are reconciled. Existing IDs, status and recorded checks stay put, and a Task file being disposable scaffolding is never a reason to erase that history.

### Why does the hand-back carry two answers?

They can differ. A candidate can merge cleanly yet leave acceptance unmet, or meet acceptance yet sit behind a conflict. The parent checks each against the real merge route. A **Receipt**, the Task's recorded check results and Git facts, logs what happened but is not a review.

## It's working when

- The run begins by confirming the Workbench files exist and the Task is an actual executable assignment with a known claimant.
- Where behavior could be tested, a test failed first and then passed, and no test was weakened to get green.
- The hand-back lists the real commands run, their results, the exact candidate and any check that could not run.
- The hand-back says complete only where acceptance is met, and names the gap otherwise.
- The branch is committed and pushed, and any PR's remote commit and base, head and draft state were read back.
- Nothing in the run claims independent Review, owner approval, Human QA or release.

## Where it fits in the workflow

Journey belongs to the Journey stage ("Build each Task"), whose main flow is [carry](/skills/carry), [orchestrate](/skills/orchestrate), then Journey. It calls on [tdd](/skills/tdd), [diagnosing-bugs](/skills/diagnosing-bugs), [codebase-design](/skills/codebase-design) and [pr](/skills/pr) when needed. Tasks come from [plan](/skills/plan) in the Prepare stage. After Journey, the parent orchestrator validates the hand-back, and independent review of the assembled Spec happens in the Judge stage with [code-review](/skills/code-review), whose findings become a new Journey. Further landing and cleanup follow the project's branch-completion procedure, which is the territory of [land](/skills/land) in the Complete stage.
