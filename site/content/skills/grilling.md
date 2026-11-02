---
name: grilling
summary: Interviews you about a plan in batches, with a recommendation on every question, until you explicitly confirm you and the agent mean the same thing.
pin: 878241202bf7ec97c0952287f1633f6f0ddf1a6e
credit: adapted
credit_text: Adapted from [Matt Pocock's grilling skill](https://github.com/mattpocock/skills/blob/a496f5513d4a4cf889bc48e189e579f4b0bdf6aa/skills/productivity/grilling/SKILL.md), MIT License, with Why/Impact fields, correction checks and caller-owned persistence added.
credit_license: MIT
---

## What it does

Grilling turns a vague plan into settled decisions by interviewing you. The agent handles the facts, you make the calls, and nothing moves forward until you confirm the result.

It opens with an **interview question tree**: the decisions to make, their dependencies, what is settled, what is open, and what can be asked right now. The tree organizes the conversation. It is not a project plan. Before asking, the agent looks for answers you already gave in a sourced place, so you are not asked twice. Documents can inform the interview, but they never answer a decision that is yours.

The interview runs in **rounds**. The **frontier** is the set of decisions whose prerequisites are all settled, so they can be asked now. Each round the agent shows the frontier as a numbered batch (or one question), and you can answer several at once, since each is worded so a plain "yes" accepts its recommendation. Each carries four parts:

- **Question**: the choice, plus the meaningful alternatives.
- **Recommended answer**: what the agent would pick.
- **Why**: the reasoning and evidence behind that pick.
- **Impact**: what the choice changes downstream.

After you reply, the agent processes each answer, keeps unanswered questions alive, parks the ones that depended on them, then recomputes the tree and shows the next frontier. Branches that stopped mattering are dropped. A clear answer settles its choice, and the agent only clarifies where an answer is ambiguous. If you answer only part of a question, it asks about the missing piece instead of deciding for you.

Two rules keep it honest. Facts are the agent's job and decisions are yours: it investigates what it can reach, and a missing fact blocks only the questions that depend on it. And a recommendation is not an answer. Silence accepts nothing, and your stated reasons stay separate from the agent's inferences. After every round it checks the tree against what you said, your intended result and your constraints, and challenges contradictions.

## When to use it

Reach for grilling when you want a plan, decision or idea challenged before anyone builds on it, or when you simply ask to be grilled. It is the plain interview engine and works in any conversation. It needs no Workbench (the project structure of records and tools that the Workbench skills maintain).

The neighbours below wrap it or sit beside it. The saved-interview, docs-editing and domain-model rows require a Workbench, a project set up by `setup-workbench`, and `align-concept` and `align-docs` run only when you ask for them. Plain grilling needs none of that.

| What you have | Reach for |
|---|---|
| A plan or decision to stress-test, nothing saved | `grilling` (this skill) |
| An idea where each recommendation should face its strongest opposing case | [brainstorm](/skills/brainstorm) |
| A concept to interview, with the confirmed intent saved in the project knowledge base | [align-concept](/skills/align-concept) |
| A concept where documentation and the domain model should be edited too | [align-docs](/skills/align-docs) |
| Fuzzy or clashing terminology to sharpen, often beside an interview | [domain-modeling](/skills/domain-modeling) |
| You want to be told where you are wrong, not interviewed | [oracle](/skills/oracle) |
| Agreement already reached, needing a reviewable written statement | [readback](/skills/readback) |

## Example request

> Grill me on this migration plan. I want to move our job queue from cron scripts to a hosted scheduler, but I haven't decided on rollout order, who owns on-call, or whether to keep the old scripts as a fallback.

The agent would show the tree, answer what it can from your repository, then ask a first batch such as rollout order and fallback, holding on-call ownership back because it depends on both.

## What it requires

- No Workbench, tool or record beyond the conversation itself.
- The [readback](/skills/readback) skill, the one skill it depends on, which shapes the confirmed summary you approve at the end.
- Optionally, sources the agent can read. Where evidence is out of reach, the agent says so and still asks everything that does not depend on it.
- Optionally, your permission to hand independent fact-finding to a fresh-context helper, used only when one is available.

## What it does not authorize

- **Execution.** Finishing a batch starts a check, not work. Confirming the interview establishes shared meaning, and authority stays limited to the scope you explicitly gave. Creating project maps or plans, implementing them and judging them all count as execution. Read-only investigation and the interview itself count as alignment.
- **Saved documents.** The interview stays in chat. It creates no notes, wiki pages, glossary entries or project docs on its own.
- **Decisions you did not make.** Silence, an unanswered question, a recommendation or a definition you merely liked does not settle a choice.

## Finishing: the confirmed readback

The interview ends one of two ways. You can ask it to stop, and the agent reports the open choices, what still blocks them, and the next frontier. Or it finishes properly: every relevant branch is resolved or explicitly deferred, the agent presents a [readback](/skills/readback), and you explicitly confirm it.

That readback covers what the concept is, its scope, the choices made, the constraints and the remaining uncertainty. The readback skill lays it out as Summary, The why, The intended result and What I will do. Approving single answers or definitions along the way does not confirm it, and deferred items and missing evidence appear in it even when the frontier is empty.

## FAQs

### Does grilling write notes or docs for me?

No. The interview lives in chat. To keep answers, corrections and open questions, invoke another skill that owns saving: [align-concept](/skills/align-concept) for saved interviews and confirmed intent, or [align-docs](/skills/align-docs) when documentation is edited too. Neither is required to run a session.

### What happens if I change my mind?

If you correct something or the premise shifts, the agent reopens that decision and whatever hangs off it, and leaves unrelated settled choices alone. It checks the revised picture with you before relying on it, so you never need to restart the whole interview.

### The agent never seems to finish. Why?

Check what is still open. It ends only when each relevant branch is resolved or consciously deferred and you have confirmed the readback. Decide the open branch, defer it explicitly so it appears in the readback, or tell the agent to stop and take the pause report.

### The agent asked me something it could have looked up. What went wrong?

It should investigate available sources first and recover answers you already gave. Point it to the source, or say which facts it cannot reach. Missing evidence blocks only the dependent questions, so the rest should continue.

### Did my "yes" to the readback mean the work is approved?

No. Confirming the readback settles what you mean. It does not start mapping, planning or implementing. Those steps need your explicit scope.

## It's working when

- You see a question tree up front, with settled, open and dependent items distinguishable.
- Questions arrive in numbered batches, each with a recommendation, reasoning and impact.
- Facts the agent could find are found, not asked about.
- Dependent questions appear only after their prerequisites are settled, and irrelevant branches get dropped.
- Contradictions between your answers and your stated goals get challenged.
- A correction reopens only the affected choices.
- The session ends with a readback you explicitly confirm, or with a pause report, and no files appear that you did not ask for.

## Where it fits in the workflow

Grilling is the first main step of the Align stage ("Shared concept"), followed by [readback](/skills/readback), which is how its result gets confirmed. [brainstorm](/skills/brainstorm) builds on it, and [align-concept](/skills/align-concept) and [align-docs](/skills/align-docs) wrap it when the outcome should be saved or documented. [domain-modeling](/skills/domain-modeling) can run beside it when terminology is being reworked, though grilling completes without it. When you are unsure which skill fits, [ask-workbench](/skills/ask-workbench) routes you.

It hands off confirmed meaning. The next stage, Prepare, begins with [map](/skills/map), which describes a destination from established intent. That counts as execution, so it starts only with your explicit scope.
