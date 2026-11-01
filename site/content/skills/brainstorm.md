---
name: brainstorm
summary: Test an idea through an interview where each recommendation comes with its strongest opposing case, an alternative and its main risk.
pin: 878241202bf7ec97c0952287f1633f6f0ddf1a6e
credit: adapted
credit_text: Adapted from [Matt Pocock's grilling primitive](https://github.com/mattpocock/skills/tree/a496f5513d4a4cf889bc48e189e579f4b0bdf6aa/skills/productivity/grilling), MIT License, with a counterargument lens added by Kayden Clark.
credit_license: MIT
---

## What it does

Brainstorm is a thin layer on top of the [grilling](/skills/grilling) skill. Grilling supplies the interview itself: the **decision map** (grilling's question tree of the decisions, their dependencies and what is settled), the confirmation steps, how corrections reopen earlier choices, and how to recover when something goes missing. Brainstorm adds one rule on top: no recommendation reaches you until it has been argued against.

Before the agent recommends anything, it compares the plausible choices against the result you said you want. Doing less, or leaving things as they are, counts as a real option whenever it could solve the problem. For each recommendation the agent brings three things:

- the **strongest supported counterargument**, meaning the best case the evidence allows against its own pick;
- at least one **credible alternative**, along with what evidence or changed assumption would make that alternative the better pick;
- the recommendation's **main risk**.

If the evidence cannot support an opposing case, the agent says what is missing. It does not make up a rival argument.

The agent starts from what the conversation already holds: your question, the intended result, choices you have settled, and your constraints. It inspects whatever facts it can reach before asking you to decide anything. Then it asks the **ready frontier**, which is every decision whose prerequisites are already settled, in grilling's four-part format: Question, Recommended answer, Why, Impact. You decide. The agent keeps three things apart at all times: its own recommendations, answers still pending, and choices you have confirmed. Alternatives you reject are noted briefly on the matching entry of the decision map, so the reasoning survives.

## When to use it

Reach for it when you are weighing options or testing an idea before you commit, and you want each suggestion to come with its best objection instead of a confident pitch. It is invoked by asking for it by name or by describing that need; it is a conversation.

| What you have | Reach for |
|---|---|
| An idea or plan you want questioned, with trade-offs shown for each recommendation | `brainstorm` |
| A plan to stress-test until you and the agent share one confirmed understanding | [grilling](/skills/grilling) |
| An idea you want judged by a domain expert who gives its own verdict and tells you where it is wrong | [oracle](/skills/oracle) |
| A saved interview whose confirmed intent should be preserved for later | [align-concept](/skills/align-concept) |
| A concept interview that should also keep project documentation up to date | [align-docs](/skills/align-docs) |
| A large, uncertain effort spanning several sessions | [wayfinder](/skills/wayfinder) |

[align-concept](/skills/align-concept) and [align-docs](/skills/align-docs) run only when you ask for them. They and [wayfinder](/skills/wayfinder) need a **Workbench**, the project's record-keeping setup, which [setup-workbench](/skills/setup-workbench) creates. Brainstorm itself needs none.

## Example request

> I'm deciding whether our CLI should cache API responses on disk. Brainstorm it with me. For each thing you recommend, show me the best argument against it, and include "do nothing" if that might be enough.

The agent will first look at what it can check, such as how often the calls repeat and how slow they are. It will then ask the first ready questions, each with a recommendation, the strongest case against it, an alternative, and the main risk.

## What it requires

- The [grilling](/skills/grilling) skill. Brainstorm relies on it for the interview protocol. If it is unavailable, the agent reports the missing prerequisite and does not claim the protocol was followed.
- A question or intended result from the conversation to start from. The skill does not state any other required records, tools or setup.
- Ideally, reachable facts about your question. If some sources cannot be reached, the agent names the gap and keeps going only on decisions that do not depend on them.

## What it does not authorize

- It changes no project docs, specs or glossary. The interview is conversation.
- Agreement is not permission. Writing documentation, handing work off, and implementing all need the exit you actually requested, plus authorization that already exists. Reaching a shared direction does not grant any of them.
- Recommendations are not decisions. Only your answers settle a choice, and the agent keeps unanswered items marked as unanswered.

## Where the notes go

If the session needs continuation notes, they go to a path you name, or to a scratch or gitignored location. Those notes keep pending answers and any corrections you made, so a later session can resume without re-asking settled questions.

## FAQs

### Why does the agent keep naming risks to its own recommendation?

That is the point of the skill. A recommendation that arrives with its strongest opposing case, a real alternative and its main risk lets you see what you give up by saying yes. If you would rather get plain recommendations, use [grilling](/skills/grilling).

### What if there is no good argument against a recommendation?

The agent should say that the evidence is missing and name what it lacks. It is told not to invent an opposing case. Treat a named gap as a prompt to supply the evidence or accept the uncertainty.

### What happens if some sources are unavailable?

The agent states what it could not reach and carries on only with decisions that are independent of the gap. Questions that depend on the missing facts wait.

### When does the session end?

The session closes when you pause, or when you confirm the shared direction, which includes choosing to leave a question open. Confirmation follows [grilling](/skills/grilling)'s protocol, so it rests on the confirmed readback that grilling requires. Brainstorm then adds its own closing summary: the settled direction, the alternatives considered, the tensions that remain, the missing evidence and the next unresolved decision. If a notes path exists, the summary names it.

### I agreed with the direction. Why has nothing been written or built?

Agreement alone starts nothing. Turning the outcome into documentation, a handoff or implementation needs your explicit request for that exit, and the authorization to do it must already be in place.

## It's working when

- Each recommendation arrives with a counterargument, an alternative and a main risk, not just a pick.
- Doing nothing or leaving things unchanged is weighed whenever it could solve the problem.
- Where evidence is thin, the agent names the missing evidence instead of manufacturing opposition.
- The agent checks available facts before asking you to decide, and asks only what is ready.
- Recommendations, pending answers and your confirmed choices stay visibly separate.
- Rejected alternatives are recorded briefly beside the decision they belong to.
- No project docs, specs or glossary change during the interview.
- The closing summary lists the settled direction, alternatives, open tensions, missing evidence and the next decision.

## Where it fits in the workflow

Brainstorm sits in the Align stage (shared concept), where the main flow is [grilling](/skills/grilling) followed by [readback](/skills/readback). It is an optional side tool there, used when you want opposing cases surfaced during the interview. It leans on grilling for its protocol. Its summary of settled direction is something you can carry into the next stage, but it does not start that stage on its own: mapping, planning or building follows only if you ask for it and the authorization exists. If the work needs a durable saved record of confirmed intent, [align-concept](/skills/align-concept) is the neighbour built for that.
