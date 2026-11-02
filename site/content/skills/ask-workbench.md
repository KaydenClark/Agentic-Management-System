---
name: ask-workbench
summary: Picks the smallest skill flow that fits your current request, after reading the real procedures, and stops at a recommendation unless you authorized running it.
pin: 878241202bf7ec97c0952287f1633f6f0ddf1a6e
credit: adapted
credit_text: Adapted from [Matt Pocock's Ask Matt](https://github.com/mattpocock/skills/tree/a496f5513d4a4cf889bc48e189e579f4b0bdf6aa/skills/engineering/ask-matt) and Kayden Clark's Workbench router, MIT License.
credit_license: MIT
---

## What it does

`ask-workbench` is a router. You describe what you want, and it works out which skill, if any, should handle the next step. It does not do the work itself. Its aim is the **smallest route** from where the project stands to the result you asked for. Sometimes that is just a direct answer, and it says so.

A **Workbench** is the set of records, tools and rules that the `setup-workbench` skill creates in a project. It holds **Specs** (the written destination for a piece of work) and **Tasks** (the unit of work one agent run takes on, cut from a Spec), listed in a generated index called TASKBOARD. The router reads this structure instead of guessing.

It works in four moves:

1. **Recover the request and the position.** It reads the conversation for the wanted result, settled decisions, scope, who may do what and where to stop. Then it reads the project's **controls** (the rules the project sets for agents), glossary and decisions, and follows the Workbench's entry route to the assigned Spec and Task. It checks dependencies, claims and the **delivered revision** (the version of the work already handed in) before calling work ready, and resumes work underway instead of duplicating it. It asks one question only when an open choice changes the route or who holds authority.
2. **Select from actual methods.** It checks the **host catalog** (the agent app's list of installed skills) and the project's routing, then opens each candidate's `SKILL.md` and references before recommending or starting it. It matches the candidate's inputs, prerequisites, outputs, invocation policy and authority to your request. A name, an archive entry or an open pull request does not prove a skill is installed, and files on disk do not prove the host activated them. When no skill fits, it uses the project's native procedure if that covers the job within scope. Otherwise it reports the gap and its cost. It does not install an unmerged skill, invent commands or quietly water down the job.
3. **Return or continue.** It states the procedure and source, why it fits, the next action, the expected artifact and where it lives, and the stopping point, plus any prerequisite or rejected alternative that shaped the choice. This goes in chat unless a project coordination record owns the result.
4. **Check the route and the result.** A recommendation is checked against the chosen procedure's own contract. An executed flow is checked through its real artifact or state, with observed results kept apart from unverified claims. A failure goes back to the workflow that owns it, along with the requirement that was missed, the evidence and a narrowly scoped fix. Within its authority, the router fixes the problem, repeats the failed check along with related regression checks against the fixed version, and confirms the endpoint again. Unresolved findings stay on the record, and it stops at a real blocker.

## When to use it

Reach for it when you know the outcome you want but not which workflow gets you there, or when you are unsure a workflow is needed at all. A supporting file inside the skill lists common candidates. They narrow the choice; the router still reads the real procedure before acting.

| What you have | Reach for |
|---|---|
| An idea with open choices | [grilling](/skills/grilling) to interview you, [oracle](/skills/oracle) to challenge the question, [brainstorm](/skills/brainstorm) for a counterargument |
| A design question that needs something runnable | [prototype](/skills/prototype) |
| A large effort too uncertain for one plan | [wayfinder](/skills/wayfinder) |
| Settled intent that needs a destination | [map](/skills/map) |
| An accepted destination that needs executable slices | [plan](/skills/plan) |
| One authorized, ready Task | [journey](/skills/journey) |
| A small standalone behavior change, no Spec, where project controls permit | [tdd](/skills/tdd) |
| Several implementors, or a named multi-step objective | [orchestrate](/skills/orchestrate) or [carry](/skills/carry) |
| A fixed diff that needs findings | [code-review](/skills/code-review) |
| A finished change to deliver, or a blocker to clear | [land](/skills/land) |
| Raw incoming issues or outside requests | [triage](/skills/triage) |
| Broken behavior | [diagnosing-bugs](/skills/diagnosing-bugs) |
| A recurring problem that needs a recommended fix | [diagnose-and-propose](/skills/diagnose-and-propose) |
| Codebase upkeep to survey, or a chosen module to design | [improve-codebase-architecture](/skills/improve-codebase-architecture), then [codebase-design](/skills/codebase-design) |
| Muddled domain concepts | [domain-modeling](/skills/domain-modeling) |
| A question that needs outside evidence | [explore-kb](/skills/explore-kb) or [research](/skills/research) |
| Context to carry into another session | [handoff](/skills/handoff) |
| Durable, sourced understanding to keep | [jot](/skills/jot) |
| A new or revised skill | [author-skill](/skills/author-skill) |

Requests about the Workbench itself (orientation, setup, update, improvement, evaluation or audit) go to the room's routing index and the matching Workbench skills. If all you want is a status picture, ask for a sitrep and [sitrep](/skills/sitrep) reads the TASKBOARD for you.

## Example request

> I have a half-formed idea for adding export to CSV, and I'm not sure whether it needs a Spec, a prototype or just a quick change. Which skill should I start with, and what will it leave behind?

The router would read the project's records, check whether a Spec or Task for export exists, and open the likely candidates, including `tdd` if the change is small enough to skip a Spec. It would answer with one recommended procedure, the reason, the artifact to expect and where it stops.

## What it requires

- **A Workbench.** It confirms that `workbench/manifest.json` and `workbench/tools/spec-workbench.mjs` both exist at the project root. When either is absent it halts and sends you to `/setup-workbench`. It does not build Workbench records by hand or swap in another tracker.
- **Readable skill files.** Each candidate's `SKILL.md` and references, reached through the host catalog and the project route.
- **Project records.** Controls, the glossary, relevant decisions, the assigned Spec and Task, and the TASKBOARD.

## What it does not authorize

- **New authority.** Picking a route does not give the agent permission to delegate, spend money, publish, accept work or merge. A skill runs only inside the permissions you already gave.
- **Execution on a routing question.** If you only asked where to go, it stops after recommending. If you asked for execution, it follows the chosen method to the agreed endpoint, keeping that method's gates and invocation limits.
- **A whole-Workbench audit.** Ordinary routing never starts one. Drift audits, feedback reviews and Alignment Check scoring belong to [audit-workbench](/skills/audit-workbench).

## FAQs

### Does it run the skill it picks?

Only when you asked for execution. A request for a recommendation gets a recommendation. A request to do the work can authorize the selected step, and then the router follows that skill to the agreed endpoint without widening your permissions.

### What if the skill I need is not installed?

The router checks for a native project procedure that supplies the same method within your scope, and uses it if so. If none exists, it reports the gap and what it means for your goal. Fixing the gap is your call: you can add the skill yourself and ask again. The router will not install an unmerged skill for you.

### Why does it read other skills' files before answering?

Names can mislead; a skill's real inputs, outputs and limits live in its files.

### What if it recommends a long sequence for a small job?

The skill is built to skip any stage whose result already exists, and it imposes no fixed delivery sequence on reviews, questions or small edits. If you still get an over-long route, you can state the result you want and where it should stop. That is advice for you, not a documented router feature.

## It's working when

- It opens by confirming the Workbench files exist, or stops and points you to `/setup-workbench`.
- Its answer names the procedure, where it came from, and why it fits.
- It gives the next action, the artifact it will produce and where that lives, and where it stops.
- It picks the shortest route and skips stages whose results already exist.
- It resumes existing Specs and Tasks instead of duplicating them.
- It asks a question only when an open decision would meaningfully alter the route or who holds authority, and then asks just one at a time.
- A routing-only request ends with a recommendation and no side effects.
- When it executes, it checks the real artifact or state and reports observed results apart from unverified claims.

## Where it fits in the workflow

`ask-workbench` is the main skill of the **Route** stage, the stage for choosing a path. [sitrep](/skills/sitrep), [triage](/skills/triage), [handoff](/skills/handoff) and [setup-workbench](/skills/setup-workbench) are also used there. A Workbench must exist first, so [setup-workbench](/skills/setup-workbench) comes before it when the project has none.

It hands off to whichever skill it selects, for example [grilling](/skills/grilling), [map](/skills/map), [plan](/skills/plan), [journey](/skills/journey), [code-review](/skills/code-review) or [land](/skills/land). It sends whole-Workbench audits to [audit-workbench](/skills/audit-workbench). See [Start here](/start) for the chart of skills by stage.
