---
name: wayfinder
summary: Charts a big, uncertain effort as a map of linked decisions, then settles them one per session until the route to your destination is clear enough to plan.
pin: 878241202bf7ec97c0952287f1633f6f0ddf1a6e
credit: adapted
credit_text: Adapted from [Matt Pocock's Wayfinder skill](https://github.com/mattpocock/skills/blob/a496f5513d4a4cf889bc48e189e579f4b0bdf6aa/skills/engineering/wayfinder/SKILL.md), MIT License, with project-owned glossary, decision records and trackers, and authorized delegation and delivery added.
credit_license: MIT
---

## What it does

Some efforts are too large and foggy to plan in one sitting: you know the destination, but not which questions to answer first. Wayfinder builds a **decision map** for a named destination, then resolves its questions one at a time, each in its own bounded session.

A decision map records open questions and how they depend on each other. It is not a glossary, a record of accepted behavior, or a queue of work to build. The default **endpoint**, meaning how far the work is authorized to go, is planning, with no authority to implement or publish. It runs inside a **Workbench**, the folder of records and tools the Workbench skills maintain in a project.

**Recover the destination and the language.** Before asking anything, the agent reads your request, the project's controls, any existing map and earlier answers, and extracts the destination, its purpose, the limits, what is out of scope, the endpoint, and what is settled or paused. An existing map is resumed only after checking who owns it and whether anyone changed it. The agent also loads the project's glossary (or its index plus relevant sections, stating the coverage) and follows term links to accepted decisions. Questions those already answer are not asked again. If your wording clashes with an accepted term, the agent cites both sources and tests the difference with a concrete example. A proposed change of meaning goes through [domain-modeling](/skills/domain-modeling) and stays pending until the term's **owner**, the person or record with authority over that choice, confirms it. If the destination itself is unsettled, [grilling](/skills/grilling) comes first: the agent asks you the one consequential open question, with a recommendation and its tradeoff.

**Chart only the knowable frontier.** The map indexes the destination, constraints, sources, decisions, questions, fuzzy areas still in scope, and stated exclusions. A **sharp question** is well specified and answerable, as opposed to a vague area. It can still be blocked, and the map records exactly what blocks it. Each records what must come first, the options, the agent's recommendation, the evidence it needs, where it stands and what its answer touches, and is sized for one agent session. Vague areas stay rough until an answer firms them up. Rejected options are kept with reasons. Outside the endpoint, the map comes back in chat instead of being written anywhere.

**Work one ready decision.** A question is **ready** when what it depends on is settled, someone has authority to act, and the evidence is enough to start. It takes the question you named if ready, or else the first unblocked, unclaimed one that serves the destination. Method follows the kind of uncertainty:

- Facts you can look up are researched with whichever installed research method fits, not asked of you.
- Behavior or design that needs a test goes to [prototype](/skills/prototype). The map records where the disposable artifact lives and what it showed.
- Preferences, priorities and tradeoffs go to [grilling](/skills/grilling) with you. The agent never answers these for you.
- A prerequisite action, such as getting access, is named along with who must do it, and done only if already authorized.

Delegation happens only when authorized: each helper gets a bounded question, the evidence, the endpoint and an output owner, and the agent inspects the answer before using it.

**Check the answer and continue.** Before marking a question resolved, the agent checks the answer and the updated map against what you said, the glossary, accepted decisions and the evidence, and names any assumption that failed. A correction from you reopens only the decisions that depend on it. Superseded answers and their reasons are kept, and the affected decision is retested. If a correction needs new authority or a choice only you can make, the agent reports that and continues independent work.

The session ends once its result is recorded, when only you can unblock it, or when every needed decision is settled and no fog remains. Then the agreed destination, the limits on it, links to the decisions behind it, open risks and the supporting evidence go to [map](/skills/map) or whatever planning route the project uses.

## When to use it

Reach for Wayfinder when the effort is big, will span several sessions, and you cannot yet say what the route is. If the destination and route are already clear, skip it.

| What you have | Reach for |
|---|---|
| A large, foggy effort with many linked unknowns | `wayfinder` (this skill) |
| One decision or plan to stress-test, no saved map | [grilling](/skills/grilling) |
| A factual question you can look up | [research](/skills/research) or [explore-kb](/skills/explore-kb), the sort of research route Wayfinder defers to |
| A settled destination to write down as a Spec (what a capability should do and how it is accepted) | [map](/skills/map) |
| An accepted destination ready to cut into Tasks (single executable assignments) | [plan](/skills/plan) |
| A question about what a term should mean | [domain-modeling](/skills/domain-modeling) |
| A design question only a small experiment can answer | [prototype](/skills/prototype) |
| Unsure which skill fits | [ask-workbench](/skills/ask-workbench) |

## Example request

> We want to move our customer-facing app to a different hosting platform, and I don't know where to start: auth, data, DNS, cost, who owns what. Use wayfinder to chart the decisions and work the first ready one. Planning only, no changes to anything.

Wayfinder would write or resume a map, work one ready question and report what is left, without touching the migration.

## What it requires

- **A Workbench.** The skill checks the project root for the Workbench manifest and spec tool. If either is missing it stops and tells you to run [setup-workbench](/skills/setup-workbench), and it does not hand-build records or substitute another tracker.
- **The project's glossary and decision records,** which the map links to instead of restating.
- **A place to write,** meaning the existing decision map, issue or notes owner, inside the endpoint.
- **The Workbench's procedures.** Decision questions stay apart from build Tasks, with no second work queue.

## What it does not authorize

- **Implementation or publication.** Creating Tasks and building anything need their own authorization.
- **Writes outside the map.** Maintaining the map does not allow running Jot (the Workbench's note-capture skill), updating the Wiki (its shared project knowledge), publishing issues, or editing other knowledge owners.
- **Provisioning or spending.** A pending access request blocks only the decisions that depend on it. The map authorizes neither setting up access nor paid services.
- **Throwaway branches.** Optional parallel research does not permit creating or pushing temporary branches.
- **Answering for you.** Preferences and tradeoffs belong to the actual owner, and a prototype that runs cannot stand in for one.
- **Redefining accepted terms.** Implementation evidence can expose a gap but does not overrule an accepted meaning.

## FAQs

### What happens if the project has no Workbench?

It stops and tells you to run [setup-workbench](/skills/setup-workbench). Set that up, then ask again.

### Which question does it work first?

The one you name, if it is ready. If it is blocked, the agent explains the dependency and works an independent ready question in scope. If nothing is ready, it says what small input or owner action would unblock one.

### Why only one decision per session?

That is the skill's rule. Each session records the answer, dated sources, doubts and any confirmation still owed, and marks a question resolved only when the evidence meets its own resolution test. Charting a brand-new map may end a session with no decision resolved.

### Is this the same as planning?

No. Wayfinder settles what must be known; planning turns an accepted destination into Tasks. Wayfinder hands settled intent to [map](/skills/map) or your project's planning route. [plan](/skills/plan) is the catalog's planning skill, but Wayfinder does not require it, and creating Tasks afterward needs its own authorization.

### Do I need a formal Alignment check?

Not for ordinary planning. The comparison of each answer against your sources, the glossary and the evidence is enough. Formal Alignment qualification is required only when assigned.

## It's working when

- The map names the destination, constraints, exclusions and sources, and links each decision to its one detailed owner.
- Each sharp question shows what blocks it, the options, a recommendation, the evidence required, its status and what it affects.
- The session works one ready decision, or names the smallest missing input when nothing is ready.
- Facts are researched, tests go to a prototype, and your preferences are asked of you rather than decided for you.
- Questions already settled by you or the glossary are not asked again, and rejected options and superseded answers stay on the map with reasons.
- The closing report covers where the map is, what was answered, what changed, what remains unclear or blocked, and the smallest next step.

## Where it fits in the workflow

Wayfinder sits in the **Align** stage, where you and the agent build a shared concept before anything is mapped or built. It is a supporting skill there, for efforts too uncertain for one interview, and it calls on [grilling](/skills/grilling) for your preferences, [prototype](/skills/prototype) for experiments and [domain-modeling](/skills/domain-modeling) for vocabulary changes. When every needed decision is resolved, it hands settled intent onward to [map](/skills/map) or the project's own planning route in the **Prepare** stage, where [plan](/skills/plan) is the catalog's planning skill.
