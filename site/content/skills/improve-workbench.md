---
name: improve-workbench
summary: Fix one failing agent job by changing the Workbench around it, proving the change with checks and a fresh rerun, then keeping, revising or removing it.
pin: 878241202bf7ec97c0952287f1633f6f0ddf1a6e
credit: adapted
credit_text: The loop's shape is adapted from Ryan Lopopolo's [Harness Engineering](https://github.com/lopopolo/harness-engineering) improve-harness playbook (playbooks/improve-harness.md at 226c8d35), [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), rewritten for Workbench rooms with ownership routing, feedback records and dispositions added.
credit_license: CC BY 4.0
---

## What it does

A **Workbench** is the bundle of controls, skills, tools, records and checks a coding agent works inside. This skill repairs that bundle, which it calls the **harness**, not the model or your product code. You pick one job an agent got wrong, hold the model and job fixed, change the harness, and measure whether it helped.

1. **Observe the baseline.** Study one run, fresh or recorded, noting where a person had to relay something. Capture the Workbench's own measures first, such as `doctor` (its built-in structure and drift check, run through `spec-workbench`) and the full test suite.
2. **Find the earliest gap.** Trace the symptom upstream to the first point where the run lacked something, such as context, a capability, clear ownership or proof.
3. **State one intervention and a prediction.** Pick the smallest reversible change at the gap's owner; deleting counts. Favor a change that spares a person from relaying information, or that puts a rule right where it gets applied, over adding a new service. Write down what the same worker should do differently, what would confirm or weaken the guess, and who pays the upkeep.
4. **Change and verify.** Send it through a **Spec** (a written outcome), a **Task** (one assigned unit of work under it), a **Journey** (the skill that carries a Task through implement, check, QA and submit), review and landing. Re-measure, and check the real outcome, not only the score.
5. **Rerun fresh.** Repeat the job in a clean agent context and an equivalent starting state, such as a temporary clone that exposes no later history like tags or refs.
6. **Retain, revise or remove.** Keep the change if it was used, fits the predicted mechanism and earns its upkeep. Revise it if the gap was right but the change is hard to find or use. Remove it if it is noise, duplicates a better owner or keeps failing.

Steps 1 to 3 are read-only. A **job contract** written first governs them: target and revision, the job, the accepted outcome, the worker's model and tools, authority, outside state such as CI, and the suspected gap. Baseline and rerun share it; changing a field starts a new comparison.

Easy to miss: the **run without it**. If existing material might already explain the fix, withhold the change and rerun. If the job still closes, claim no improvement.

The pass ends with one result report in the feedback lane, one **disposition** per finding in its Spec (`diagnostic`, `test`, `repaired`, `declined` or `accepted-open`), and a new row in the Workbench Feedback log that names the original row instead of editing it.

## When to use it

Use it when a failed agent run, a retro, a review finding that keeps recurring, or a Workbench Feedback entry (the append-only log that carries harness problems from a project back to its upstream maintainer) implicates the controls, skills or tools. A trigger is evidence of a suspected gap, not an assignment. Keep the scope to one job that is cheap to rerun; if the evidence cannot pick it, the skill asks the owner.

| What you have | Reach for |
| --- | --- |
| A request to assess a harness without repairing it | [audit-workbench](/skills/audit-workbench) |
| A broad claim, such as beating generic instructions or the prior version | [evaluate-workbench](/skills/evaluate-workbench) |
| A session retrospective | [retro](/skills/retro), then bring one candidate here |
| Your own code is wrong, not the harness | [diagnosing-bugs](/skills/diagnosing-bugs) |
| Installing or updating a released harness | [setup-workbench](/skills/setup-workbench) |

A failed review verdict is first captured with [jot](/skills/jot) under a `review-finding:` tag and a short class slug. The second time the same class appears, it enters this loop, and the intervention is a deterministic check, either a test in the full suite or a registered `doctor` code. Superseded or corrected entries, and longer slugs, do not count as repeats.

## Example request

> Our last three Journeys on this repo each stalled because the agent picked the wrong test command. Run improve-workbench on that: baseline one of the runs, find where the agent first lacked what it needed, and give me the smallest change with a prediction. Don't change anything yet.

Because you asked for no changes, the skill stays read-only and returns the job contract, the earliest gap and a prediction to review.

## What it requires

- **A Workbench.** If `workbench/manifest.json` or `workbench/tools/spec-workbench.mjs` is missing, it stops and sends you to [setup-workbench](/skills/setup-workbench) rather than hand-building records.
- **The project's records.** It reads AGENTS.md, the RUNBOOK, the GLOSSARY, the Wiki and the manifest.
- **Scoped authority to change a control,** usually through an assigned Spec and Task. Running a fresh worker or a paid trial requires its own go-ahead.
- **The delivery skills** listed in the last section.

It also decides who owns the gap. A **room** is a project using an installed Workbench; the **producer**, LLM_Workbench, releases the Workbench and owns its core skills, tools and templates. In a room that carries a separately managed, legacy release, a producer-owned gap ends the loop after step 3: record the evidence, add a feedback row, and hand back. Inside the producer, the full loop runs. Ownership differs for a room built from the self-contained setup-workbench package under the personal-catalog normal setup (the `skillPolicy.normalSetup` value). In that case the personal skills repository holds the reusable methods, while the setup package holds the runtime and templates it bundles. The manifest or receipt points to the actual source and feedback owners, so no producer checkout is needed, and a repair authorized in that personal catalog does not halt at step 3.

## What it does not authorize

- A trigger, finding or feedback row is evidence, not an instruction or an approval.
- It will not widen permissions, redefine the accepted outcome, loosen a check so a run passes, or turn an uncorroborated worker self-report into a rule.
- It does not pre-approve fresh-worker runs or paid trials, or touch scheduled feedback adapters.
- A result record repairs nothing and grants no approval or release; a disposition does not schedule or authorize a repair.
- A landed fix does not close an [audit-workbench](/skills/audit-workbench) finding. The repaired revision goes back there for retest.

## FAQs

### What if I cannot reproduce the failure?

Record what blocked you, collect the missing fact, and stop without changing anything. The skill forbids inventing a failure to justify a change.

### Can I skip the fresh rerun?

You can, but the rerun is recorded as pending, and the change counts only as a fix for a wrong control, not as a demonstrated improvement.

### My score went up. Is that an improvement?

Not on its own. A score reflects only what its check reads. Confirm the worker actually used the change, and if a run without it also closes the job, claim no improvement.

### Why does `doctor` miss a collision I know exists?

In a project with an `origin` remote, `doctor` reads only remote branches already fetched locally and never fetches, so fetch all branches first. A new `doctor` code is producer-owned and becomes a feedback row in a room; a test in your own suite stays yours.

### Does one pass prove the change works generally?

No. It supports a claim about this job under these conditions. Broader claims go to [evaluate-workbench](/skills/evaluate-workbench), and a new feature in the shipped templates needs paired trials scored by the Alignment Check, the method [audit-workbench](/skills/audit-workbench) owns. One run also cannot blame the model.

## It's working when

- The job contract is written before any control changes, and baseline and rerun use the same one.
- The earliest gap is named by kind and traced to one owner, and the prediction exists before the change.
- The rerun happens in a fresh context, and the record lists which sources could have supplied the fix.
- The outcome is retain, revise, run without it or remove, with an owner, evidence and a condition for revisiting.
- Someone arriving cold can find the report, the Spec and the next step from repository state.

## Where it fits in the workflow

It belongs to the Improve stage (Learn and fix), next to [retro](/skills/retro), which usually supplies the candidate. Feedback rows, review findings and [audit-workbench](/skills/audit-workbench) findings feed it too.

It borrows the delivery chain: [map](/skills/map) when no Spec exists, [plan](/skills/plan) for the Task, [journey](/skills/journey) for implementation, [code-review](/skills/code-review) for review and [land](/skills/land) for delivery. Broader claims go to [evaluate-workbench](/skills/evaluate-workbench), and harness updates go through [setup-workbench](/skills/setup-workbench).
