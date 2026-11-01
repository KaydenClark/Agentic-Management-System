---
name: plan
summary: Splits an agreed destination into Tasks that each fit one run and cross every layer, with honest dependencies and a start-now list, saved as TASK.md files.
pin: 878241202bf7ec97c0952287f1633f6f0ddf1a6e
credit: adapted
credit_text: Adapted from [Matt Pocock's To Tickets skill](https://github.com/mattpocock/skills/tree/a496f5513d4a4cf889bc48e189e579f4b0bdf6aa/skills/engineering/to-tickets), MIT License, reshaped for single-run TASK.md records, a generated TASKBOARD, authority and retention rules. It also absorbs the earlier tracer-bullet, to-tasks and to-tickets skills.
credit_license: MIT
---

## What it does

`plan` takes a destination someone has already accepted (a Spec, an issue, a written plan, or a conversation that ended in agreement) and cuts it into **Tasks** an agent can pick up. A **Task** is one assignment sized for a single implementor run: recover the source, build, check, run QA, repair, and report back (the **hand-back**). A **Spec** is the long-lived record of where the work is going and what counts as done. The Spec keeps the goal; a Task is disposable scaffolding. Both live in a **Workbench**, the folder of Specs, Tasks and generated tracker files that the catalog's skills share.

One-run sizing is a planning unit, not permission to quit early; the run still goes to its assigned endpoint unless something truly blocks it.

The skill works in four moves.

1. **Map the stack.** It names the layers a finished behavior must cross in your project, learned from your instructions, build docs and source. A web feature might touch storage, service, interface and tests.
2. **Find the smallest route that works.** It starts from one Task and splits only for outcomes that can be checked separately, a real dependency, different writers, or a run too big for the usable context window.
3. **Build the dependency tree.** Each Task records the behavior it delivers, the acceptance it covers, scope, one writer, a check that could fail, and where the hand-back goes. Every Spec requirement lands in a Task or a named dependency.
4. **Review, write, return.** It smell-tests each Task and shows you a numbered breakdown. Records are written only where preparation authority exists, either already granted or confirmed by you. It then validates the tracker and returns the ready frontier, open choices and a next action.

Key terms:

- **Tracer bullet:** the smallest slice a caller can see working, touching each mapped layer once.
- **Horizontal shard:** a Task confined to one layer, such as only the schema. It proves nothing alone and hides integration risk, so `plan` re-cuts it.
- **Blocker edge:** a claim that another Task's finished, verified output must exist first. Merely related Tasks get no edge, and the graph never loops.
- **Ready frontier:** the Tasks whose prerequisites are all met.
- **TASK.md** is the assignment: Task ID, Spec ID, status, blockers, destination, planned verification and acceptance checkboxes. **TASKBOARD.md** is a tracker generated from those records, never an authority.

Name each Task for what someone can observe, such as saving a record and reading it back, not for a layer. Each should be demoable alone, with a quick check run through the entry point a real caller uses (the **public seam**), the way [tdd](/skills/tdd) tests behavior. The opening Task is a thin working path; later Tasks extend it one behavior at a time.

Prefactoring (a prep change that alters no behavior) and wide mechanical refactors are exempt. They pass on unchanged behavior and green CI, and a wide refactor runs in steps: add the new form, migrate callers in batches, remove the old one.

## When to use it

Reach for `plan` when the destination is settled and you need work an agent can pick up. It also fits repairing a Task that covers one layer, and smell-testing Tasks someone else wrote before they are assigned. For an unsettled destination it sends you to `map` or `grilling` instead.

| What you have | Reach for |
|---|---|
| An unsettled or disputed idea | [grilling](/skills/grilling), then [map](/skills/map) |
| A settled destination with no written Spec | [map](/skills/map) |
| An accepted Spec or plan that needs agent-ready work | `plan` |
| A Task that may be a one-layer slice | `plan`, to smell-test and re-cut it |
| An assigned Task ready to build and hand back | [journey](/skills/journey) |
| An authorized endpoint needing several implementors coordinated | [orchestrate](/skills/orchestrate) |
| A gap in evidence that needs a bounded experiment | [prototype](/skills/prototype) |

## Example request

> The checkout Spec is accepted. Break S-004 into Tasks. Start with one demoable path from cart to saved order, keep the blockers honest, and show me the breakdown before you write any records.

The skill maps the layers checkout crosses, proposes a numbered breakdown with titles, blockers, delivered behavior and sizing rationale, and holds there for your go-ahead, as you asked.

## What it requires

- **A Workbench.** It checks the project root for the manifest and the Workbench tool. If either is missing it stops and tells you to run [setup-workbench](/skills/setup-workbench), and it will not hand-build records or switch trackers.
- **An accepted destination** with its owner, evidence and current implementation, plus project context: instructions, terms, decisions, source and tests.
- **The Task record method** in the skill's reference file, covering fields, ID allocation and lifecycle commands. Legacy Task tables are converted with the Workbench's convert step, and completed rows stay as history.
- **Two sign-offs:** confirmation to leave the Explore phase, and execution approval to leave the Prepare phase. Approval already given is reused.

## What it does not authorize

- **Implementation.** `plan` stops before building unless that is authorized and handed to the executing workflow. Preparation, publication and execution are separate permissions.
- **Records without preparation authority.** Lacking it, the skill writes nothing and changes no tracker state.
- **Activation or claiming.** A planned Spec can hold ready records that claiming still refuses. With both sign-offs cited, the Workbench's activation step starts the Spec, and even that claims no Task.
- **New scope.** Repairs inside an approved outcome stay in that Task; a new outcome needs its owner's authority.
- **Skipping review.** Work that follows Judge, the review stage after delivery, carries a post-delivery marker and waits for review and owner approval.
- **Proof.** Acceptance and verification lines describe future work. A planned check is not evidence.

## Blockers and closing out

A blocker is a Task ID the Workbench recognizes, never prose, paired with the missing input and the condition that releases it. An unanswered owner choice goes into the Spec, and affected Tasks carry an `owner:` marker until it is settled.

At hand-back, results are reconciled into the Spec, and leftovers become a smaller bounded assignment. One catch: the native close command records a receipt without reading acceptance checkboxes, so a Task can be marked done with every box empty. That is why `plan` writes acceptance that the implementor, QA and orchestrator can each compare with the real result.

## FAQs

### Why not one Task per layer?

Layer-sized Tasks are horizontal shards. Each can look finished while the feature still does not run, and integration problems appear only when the last one lands. If a run is too big, `plan` thins the behavior but keeps it crossing every layer.

### What if the evidence isn't there to plan a piece of work?

Weak evidence calls for a scoped exploration or a [prototype](/skills/prototype) with a named question, not a guess dressed up as an accepted Task. The open choice is recorded in the Spec and dependent Tasks stay blocked. A destination that was never agreed goes to `map` or `grilling`.

### Will plan start the work once the Tasks exist?

No. It returns pointers, the ready frontier, open choices and the next action, then stops. Execution belongs to a workflow such as [journey](/skills/journey) or [orchestrate](/skills/orchestrate) and needs execution approval.

### Can I retire or delete a Task I no longer want?

Not freely. The skill preserves a record's history and repairs anything that depends on it, using only supported lifecycle operations. The inspected runtime has no generic way to discard an incomplete run or rewrite dependencies, so the record stays and the limit is reported.

## It's working when

- The layers your feature crosses are named before any Task is proposed.
- Every Task title is an observable outcome, and each behavior-changing Task has a quick check at a public seam.
- The first Task is independent and delivers a thin path that works from end to end.
- Every blocker names a real prerequisite with a release condition, the graph has no cycles, and every Spec requirement maps to a Task or dependency.
- You get a numbered breakdown, and records are written only where preparation authority exists.
- Saved records read back with correct IDs, parent, blockers and acceptance coverage, and the tracker validates through its native procedure.
- The run ends with the ready frontier, open choices and a next action, with nothing implemented or claimed.

## Where it fits in the workflow

`plan` sits in the **Prepare** stage (Map and Plan), the second half of it. [map](/skills/map) comes first and describes the destination that `plan` cuts into Tasks. Earlier, the Align stage ([grilling](/skills/grilling), [readback](/skills/readback)) settles a destination that is not yet agreed.

From `plan`, work moves to the Journey stage, where [carry](/skills/carry), [orchestrate](/skills/orchestrate) and [journey](/skills/journey) run the ready Tasks. Results flow back into the Spec, and follow-up work becomes a new bounded Task under the same Spec.
