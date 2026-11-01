---
name: orchestrate
summary: Coordinates implementor agents on a Workbench Spec, checks what they hand back against the destination, and stops at the endpoint you authorized.
pin: 878241202bf7ec97c0952287f1633f6f0ddf1a6e
credit: original
credit_text: Original to Kayden Clark.
---

## What it does

`orchestrate` turns an agent into a coordinator. It does not write the code. It decides which Tasks are ready, briefs a worker for each, inspects what comes back, and keeps going until the endpoint you authorized is reached or nothing safe can move.

A **Workbench** is the project scaffolding that [`setup-workbench`](/skills/setup-workbench) creates: a manifest, a command-line tool and folders of records. A **Spec** is the destination record for a piece of work, with its acceptance criteria. A **Task** is one bounded run for one implementor, described in its own TASK.md. An **implementor** is the agent that carries out a Task. A **landmark** is a larger destination spanning Specs.

There are two coordinator levels. A **Director** oversees assigned Specs or landmarks by working through Dispatchers. A **Dispatcher** runs the implementors for one Spec, giving each Task one bounded run. Use only the levels the work needs and as few workers as can make real parallel progress. While you hold the orchestrator role, you never do an implementor's Task or patch its output yourself.

A run moves through four phases:

1. **Recover the assignment.** From the owner's instruction, pin down the endpoint, scope and how success is judged. Read project rules, check the repository, worktrees, open PRs and current claimants, and confirm which delegation tools really exist.
2. **Assign ready work.** Pick authorized, unblocked work whose prerequisites are already in the revision the worker starts from. Dependencies and shared-file conflicts both limit parallelism. One writer owns shared Spec and Task state, implementation lanes get separate worktrees, and each run is sized to fit the implementor's context window.
3. **Inspect, integrate and continue.** Compare each returned diff or artifact, and its evidence, with the assignment. Accept complete results within your delegated authority and send misses back to the implementor. If the owner's intent changed, it returns to the Map or Plan that owns it before affected work resumes.
4. **Close or preserve the blocker.** Verify the changed records and delivery revision, then report what was delivered, the exact candidate, which checks ran, where review stopped, what remains and the next gate. If you cannot finish, leave the Spec ready for the next person to resume.

Each worker brief carries the governing instruction, acceptance checks, source pointers, an exact base, owned files and exclusions, the branch or worktree, and the endpoint. A Dispatcher also learns who may write shared records and where to report back. In return you get the real artifact or commit, Check results, the implementor's own QA, and two answers: is this change safe to merge, and is the Task's acceptance fully met, or what is still open? You verify both against the diff.

The records are the source of truth: the manifest locates Specs and branches, SPEC.md holds acceptance and evidence, each TASK.md covers one run, and TASKBOARD.md is a generated view. Stay inside your assignment even if the tool's `next` command suggests unrelated work.

## When to use it

Reach for it when you hold a Director or Dispatcher assignment: several Tasks, workers to run and an endpoint to reach. Naming the skill does not permit launching workers, and a simple single-agent job needs no orchestration.

| What you have | Reach for |
|---|---|
| One authorized Task to implement, check and submit | [`journey`](/skills/journey) |
| One objective you want owned end to end through its authorized endpoint, without a formal Director or Dispatcher assignment | [`carry`](/skills/carry) |
| A settled destination but no Tasks yet | [`plan`](/skills/plan) |
| Intent that has no Spec yet | [`map`](/skills/map) |
| An independent verdict on an assembled candidate | [`code-review`](/skills/code-review) |
| Finished work that must reach its target branch, or a merge that is stuck | [`land`](/skills/land) |

## Example request

> You are the Dispatcher for S-012. Run the ready Tasks through implementors, check what each hands back, make sure the checked PRs land in main one at a time, and stop when the Spec is assembled and ready for independent review.

## What it requires

- **A Workbench.** The first thing it confirms is that the project has a manifest at `workbench/manifest.json` and the command-line tool at `workbench/tools/spec-workbench.mjs`. Should one of them be missing, it halts and points you to `/setup-workbench` rather than building records manually or adopting a different tracker.
- **An assignment** with a clear endpoint, scope and exclusions.
- **The room's own procedures.** It reads the project's AGENTS.md, RUNBOOK and task lifecycle before dispatching. It never treats a merely proposed skill as installed, and never installs or replaces project controls.
- **Delegation ability.** It respects your model and cost preferences and does not invent controls.

## What it does not authorize

- **Doing the work itself.** It does not do implementors' Tasks or repair their artifacts, even when no workers are available. Role changes need explicit approval.
- **Taking over claims or bypassing the tool.** It does not reassign work someone else holds, and a refusal from the Workbench's lifecycle commands stands.
- **Making boards look ready.** Generated views such as TASKBOARD.md are rebuilt from their sources, never hand-edited.
- **Overstating a step.** A push alone does not satisfy an integration dependency, a passing Check is not acceptance, and merging is different from deploying or adopting.
- **Reviewing its own assembly.** A Dispatcher cannot approve what it assembled, and an implementor's QA is not independent Review.
- **Faking a verdict.** A report or gate printout is not a PASS or owner approval. It never invents a reviewer identity or reuses an old approval after the candidate changed.
- **Human QA or default-branch delivery.** Human QA means a person trying the result themselves. An orchestration assignment satisfies neither that nor delivery to the default branch, and a release or production deploy kept for the owner stays theirs.

## Merging and review

Implementors work on separate feature branches and open their own PRs into `main`. A PR merges once it is current with `main` and its required checks pass. If several are waiting, they go in one at a time, each rechecked against the newest `main`, with no further owner approval.

Independent Review is a different gate. It covers the whole assembled Spec, pinned to a fixed commit, and is done by a context that contributed nothing to it. It does not hold back the checked merges, but the Spec is not accepted without it where project rules require one. The Workbench's report command ties the Spec's acceptance criteria and its Tasks to a digest of that candidate, so the verdict is about exactly what was assembled. A failed review keeps the Spec open and sends scoped corrections as a new bounded Task; a green test never erases a failed verdict.

## FAQs

### What if I have no way to launch workers?

Say so. The skill reports the limit, keeps the assignments ready for someone to pick up, and continues with coordination that needs no workers. It does not pretend workers ran or start implementing.

### A worker came back with passing checks but the Task is not done. What happens?

The passing Check is evidence, not acceptance. The miss goes back to that implementor with the failed requirement and the visible mismatch. A fix inside the same run stays in the same Task. A later run becomes a fresh bounded Task in the same Spec, with earlier proof and the unmet acceptance intact. Records are never deleted to push the work forward.

### What happens on a merge conflict?

The conflict goes to the implementor who owns that branch. The orchestrator then verifies the checks and that `main` contains the work, records the result in its owning record, and only then releases dependent Tasks at that revision.

## It's working when

- It checked for the Workbench first, or stopped and sent you to setup.
- Every worker brief names the owner instruction, acceptance checks, exact base, owned files, exclusions and endpoint.
- Returned work is judged against acceptance and allowed files at an exact base and head, not on a green Check.
- The final report links the destination, names the exact candidate and checks, admits review limits and gaps, and keeps completion, Human QA, delivery to main and installation separate.
- Each worker's changes are committed and pushed, and merged worktrees are cleaned up.

## Where it fits in the workflow

`orchestrate` sits in the Journey stage of the chart (Build each Task), alongside [`carry`](/skills/carry) and [`journey`](/skills/journey). That stage is not a single Task's own Journey, the implement, check, QA and submit path that [`journey`](/skills/journey) runs for each dispatched Task. It comes after [`map`](/skills/map) and [`plan`](/skills/plan) have produced a Spec with Tasks, and it keeps lasting context in [`jot`](/skills/jot) instead of copying work state into notes.

The assembled Spec then goes to independent review with [`code-review`](/skills/code-review), and work still needing to reach its target branch can go to [`land`](/skills/land). If you are unsure orchestration is warranted at all, start with [`ask-workbench`](/skills/ask-workbench).
