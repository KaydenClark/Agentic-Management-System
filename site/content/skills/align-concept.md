---
name: align-concept
summary: Interviews you about a concept, saves the answers as notes, and records your exact confirmed readback as intent, then stops before any execution.
pin: 878241202bf7ec97c0952287f1633f6f0ddf1a6e
credit: adapted
credit_text: Adapted from [Matt Pocock's Grill Me](https://github.com/mattpocock/skills/blob/a496f5513d4a4cf889bc48e189e579f4b0bdf6aa/skills/productivity/grill-me/SKILL.md), MIT License, to compose grilling, readback and Jot for confirmed-intent capture.
credit_license: MIT
---

## What it does

`align-concept` is a saved interview. You bring a half-formed idea, and the agent questions you until you both agree on what it means. Unlike a chat-only interview, it writes down what it learns and keeps the final agreed wording as a durable record. It was previously called `grill-me`.

It is a wrapper, not a new interview method. It combines three other skills:

- [grilling](/skills/grilling) runs the interview itself.
- [readback](/skills/readback) writes the proposed statement of intent.
- [jot](/skills/jot) saves notes into the project's knowledge base.

Terms you will meet:

- **Workbench**: the project structure that the setup skill creates, with records, a manifest and a command-line tool. This skill works only inside one.
- **Question tree**: the decisions to settle, how they depend on each other, what is settled, and which branches are open.
- **Frontier**: the questions whose prerequisites are settled, so they can be asked now. Dependent questions wait.
- **Readback**: a four-section proposal of what the agent understood: Summary, The why, The intended result and What I will do.
- **Confirmed intent**: a readback you have explicitly approved, saved as the authoritative record of what you meant.
- **Knowledge base**: the Workbench Wiki where notes live. The skill reuses the project's authorized Wiki and never creates a second one.

The run goes in four moves:

1. **Prepare.** Before starting or resuming, the agent reads the three skills above plus the topic's sources, any confirmed readback and earlier corrections. It then shows the question tree, settled choices and first frontier.
2. **Interview.** You can answer several questions at once. The agent processes each answer, keeps the unanswered ones, and recomputes the tree. It investigates facts and contradictions itself, but documents never stand in for your answers.
3. **Record.** Useful answers, corrections, open questions and drafted readbacks are saved as **provisional context**: notes kept visibly apart from confirmed intent. One answer can settle an interview choice without confirming the whole intent.
4. **Confirm and hand off.** Once every relevant branch is resolved or deliberately deferred, the agent presents the readback, covering scope, exclusions, constraints, decisions, uncertainty, a proposed next action and a stopping point. It waits for your explicit confirmation, saves the confirmed text through Jot, and ends at handoff.

## When to use it

Reach for it by name. It is marked so agents do not trigger it on their own. Use it when the conversation should leave something behind: saved answers, and an agreed meaning that later work can cite. If you only want your thinking challenged, plain grilling is enough, since it keeps everything in chat.

| What you have | Reach for |
| --- | --- |
| An idea to stress-test, with no need to save anything | [grilling](/skills/grilling) |
| An idea to weigh against strong counterarguments | [brainstorm](/skills/brainstorm) |
| A concept to align and save, plus documentation or domain-model edits | [align-docs](/skills/align-docs) |
| A concept to align and save, with no documentation edits | `align-concept` |
| A claim or idea you want judged by a domain expert | [oracle](/skills/oracle) |
| Terminology that needs sharpening | [domain-modeling](/skills/domain-modeling) |

## Example request

> Run align-concept on the new notification settings idea. I have a rough sense of what I want, but nothing is written down. Interview me, save what we settle, and stop once I've confirmed the readback.

The agent shows a question tree, asks the ready questions in batches and saves your answers as provisional notes. When the branches are closed, it shows the readback and waits for your confirmation.

## What it requires

- **A Workbench.** Before anything else, the agent checks the project root for the Workbench manifest and command-line tool. If either is missing, it stops and tells you to run [setup-workbench](/skills/setup-workbench). It will not hand-build Workbench folders or records, or fall back to a different tracker.
- **The companion skills.** [grilling](/skills/grilling), [readback](/skills/readback) and [jot](/skills/jot) must be readable, since the agent reads them before each start.

Write access to the knowledge base is not a gate. If saving fails, the run continues in chat and the agent reports what is still unsaved.

## What it does not authorize

Alignment permits the interview, read-only investigation and scoped knowledge recording. It does not permit execution.

- Execution covers building out the concept, drafting or assessing any project map or plan, and starting the later workflow stages: Prepare ([map](/skills/map) and [plan](/skills/plan)), Journey ([journey](/skills/journey), which builds each **Task**, one assigned unit of work) and Judge ([code-review](/skills/code-review)). This holds even before any code exists. Designing an execution artifact is execution; summarizing the discussion is only recording.
- Taking part in alignment grants no execution authority. Existing owner authorization and its limits stay as they are.
- Staying quiet, answering interview questions, approving a definition, or accepting a documentation edit does not confirm the readback. Only your explicit confirmation does.
- A readback that covers only meaning or recording grants no execution scope. If its What I will do section proposes bounded steps, a plain yes confirms the meaning and authorizes those steps together.
- Recording a correction does not approve revised intent.
- It does not edit the glossary, specs or decision records, only the knowledge base.

## Saving and changing intent

The saved record is the exact text you confirmed, not a paraphrase. Jot stores it with its date, source, your confirmation, its scope and links to anything it replaces. Other notes link to it, and the agent checks the saved copy against what you confirmed.

If your intent changes, the agent drafts a revised readback and waits for your confirmation. The old version stays, linked as superseded. Until then, dependent execution is blocked, while unaffected decisions keep their standing.

## FAQs

### Why did it stop after I confirmed the readback?

That is the design. The skill ends at handoff, closing with the readback, a pointer to the saved note, the actual save state, the open frontier and the proposed next gate. If the confirmed readback already proposed bounded steps, your yes authorized them, but this skill still does not run them. Any other work needs authorization given separately.

### What if the save to the knowledge base fails?

The agent keeps the content in chat and reports what remains unsaved, so you know what the Workbench does not yet hold.

### I want the docs and glossary updated too. Can this skill do that?

No. This skill edits the knowledge base only. [align-docs](/skills/align-docs) follows this skill's method and adds documentation and domain-model edits under one question tree. Even there, confirming one definition permits that edit but not the whole intent.

### Will it ask me things I already answered?

It should not. Settled answers are recorded, and a resumed run picks up unresolved questions and any pending readback without repeating them.

## It's working when

- The run starts by showing a question tree, with settled choices and a first frontier.
- You can answer several questions in one message, and unanswered ones stay on the list.
- Answers and drafts are saved as provisional context, visibly separate from confirmed intent.
- The readback has four sections and names scope, exclusions, uncertainty, next action and stopping point.
- Nothing is treated as confirmed until you say so explicitly.
- The saved record matches your confirmed readback word for word.
- The run ends with a handoff summary instead of drifting into maps, plans or code.

## Where it fits in the workflow

It belongs to the Align stage (shared concept), as an extra alongside the main flow of [grilling](/skills/grilling) and [readback](/skills/readback). It builds on those two and on [jot](/skills/jot), and its sibling [align-docs](/skills/align-docs) extends it for documentation work.

You invoke it yourself, after [setup-workbench](/skills/setup-workbench) has created the Workbench. It hands off a confirmed readback and a saved-note pointer. Prepare, with [map](/skills/map) and [plan](/skills/plan), counts as execution here, so it starts only after you authorize it.
