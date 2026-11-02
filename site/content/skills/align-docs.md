---
name: align-docs
summary: Talk a concept through with an agent while it updates your docs and domain model, then stop at a confirmed record of intent before anything gets built.
pin: 878241202bf7ec97c0952287f1633f6f0ddf1a6e
credit: adapted
credit_text: Adapted from [Matt Pocock's skills](https://github.com/mattpocock/skills) (this skill was formerly called grill-with-docs), MIT License, rebuilt on the align-concept interview with documentation editing, domain modeling and confirmed-intent preservation added.
credit_license: MIT
---

## What it does

`align-docs` is the documentation-editing version of [align-concept](/skills/align-concept). You and the agent talk a concept through until you share one understanding, and along the way the agent also maintains the project's written knowledge: the glossary, the knowledge base, decision records and explanatory docs. The editing sits on top of the interview and never replaces it. Most of the method lives in the skills it points to. A run works like this:

- **One question tree.** A **question tree** is a map of the open decisions and how they depend on each other, worked through in batches. Questions about terminology, concrete scenarios, conflicts between docs and the underlying source of truth, and downstream consequences all join that one tree's **ready frontier** (the questions that can be asked now). No separate docs interview runs beside it. You can answer several questions at once. Unanswered ones stay open and the tree is recomputed.
- **Read freely, plan nothing.** The agent may read the project to check facts and contradictions, but documents never answer a question that belongs to you.
- **Provisional versus confirmed.** What you say is recorded with a status. Only vocabulary you explicitly confirm reaches the glossary. Accepted decisions become decision records under the rules of [domain-modeling](/skills/domain-modeling).
- **The confirmed readback.** Once the relevant branches are settled or deliberately deferred, the agent presents a **readback**: a four-part statement of the summary, the reasons, the intended result and what the agent proposes to do (see [readback](/skills/readback)). When you confirm it, that exact text becomes the **intent record**. Docs point to it, never to a paraphrase.
- **Intended versus verified.** Docs separate what is meant to happen from what has been shown to work.
- **A hard stop.** The run ends at handoff. Turning intent into maps, plans or code needs your separate authorization.

A **Workbench** is the project scaffold of manifest, tools and records that [setup-workbench](/skills/setup-workbench) creates. This skill only operates inside one.

## When to use it

You invoke it yourself, by name. Agents will not pick it up on their own. Use it when settling a concept should also leave the glossary, decision records or knowledge base in better shape.

| What you have | Reach for |
|---|---|
| A concept to settle, plus docs or domain-model edits wanted | `align-docs` |
| A concept to settle, with only knowledge-base notes wanted | [align-concept](/skills/align-concept) |
| A plan or idea to stress-test, with no saved record | [grilling](/skills/grilling) |
| A name, boundary or term that is overloaded or in conflict | [domain-modeling](/skills/domain-modeling) |
| Notes or corrections you want captured | [jot](/skills/jot) |
| A question that may be the wrong question | [oracle](/skills/oracle) |

## Example request

> We keep using "landing" to mean three different things across the docs. Align this concept with the documentation: interview me, fix the glossary once I confirm the terms, and read back what we agreed before anyone starts building.


## What it requires

- **A Workbench.** The agent first looks for the Workbench manifest and the `spec-workbench` tool. If either is missing, it stops and sends you to run `setup-workbench`. It will not invent Workbench folders or records itself, or swap in a different tracker.
- **The align-concept method.** That skill supplies the interview, the knowledge-base capture, the readback confirmation and the execution boundary. It builds on [grilling](/skills/grilling), [readback](/skills/readback) and [jot](/skills/jot).
- **domain-modeling.** The agent reads it before touching domain terms or decision records.
- **Your answers.** Documents inform the interview but never replace what only you can say.

## What it does not authorize

- **Execution.** Drafting a map, a plan or a design, or reviewing one, is execution even though it is only text. Permission to edit docs does not cover it, nor does it cover the later stages: Prepare, Journey and Judge.
- **Whole-intent confirmation.** Confirming a definition or approving a record permits that one recording, not the assembled intent.
- **Confirmation by silence or edits.** Silence, interview answers, approving a definition and accepting a doc edit never confirm the readback. Only your explicit statement about it does.
- **Implied permission to proceed.** Taking part in alignment grants no authority to execute. If the readback lists bounded steps and you confirm it, those steps can be authorized together. A readback that only records meaning grants no execution scope.
- **Claims of working behavior.** Docs describe intent, not verified implementation, unless it was actually verified.

## Changing the intent later

If the intent shifts, the current intent changes only after you explicitly confirm a revised readback. The earlier version is kept and linked as superseded. While a revision is pending, affected work is blocked and untouched decisions keep their standing.

## FAQs

### Why did it stop and not start building?

That is by design. Maps, plans and implementation are execution and need a confirmed readback plus authorization for that scope. If the readback lists bounded next steps, a plain yes covers them. If it only records meaning, tell the agent what you want done next.

### It stopped immediately and told me to run setup-workbench. Why?

It checks for a Workbench first and refuses rather than improvising its own records. Run `setup-workbench`, then invoke it again.

### The agent didn't pick it up when I described a docs problem. Why?

It runs only on explicit invocation. Name the skill, or plainly ask to align a concept with documentation.

### A document and the underlying source disagree. What happens?

The conflict goes into the question tree to be investigated and resolved. The agent checks each changed document against its source of truth, such as code or original material, along with its state, links and current revision.

### The note could not be saved. Is the work lost?

It should not be. When writing fails, the content stays in the chat and the closing report names what remains unsaved. Check the stated save state before assuming the record exists.

## It's working when

- One question tree drives the whole session, with terminology, scenarios and contradictions as branches of it rather than a separate checklist.
- Only terms you explicitly confirmed show up in the glossary, and unconfirmed understanding is labeled provisional.
- Decision records appear only for accepted decisions.
- Edited docs cite the exact confirmed readback, not a summary of it.
- Proposed features are described as intended, never as working.
- The agent stops at the readback and waits for your explicit confirmation.
- The closing report gives the intent record, changed-document pointers, open questions, the real save state and the next gate.

## Where it fits in the workflow

It belongs to the Align stage, where you reach a shared understanding of the concept. The main flow there is [grilling](/skills/grilling) then [readback](/skills/readback), and `align-docs` is used around it, beside [align-concept](/skills/align-concept), [brainstorm](/skills/brainstorm), [oracle](/skills/oracle) and [domain-modeling](/skills/domain-modeling). It builds on align-concept for the interview, uses [jot](/skills/jot) to save the intent record, and leans on domain-modeling for glossary and decision-record rules.

Once the readback is confirmed and you have authorized execution, work moves to the Prepare stage with [map](/skills/map) and [plan](/skills/plan). If you are unsure which skill fits, ask [ask-workbench](/skills/ask-workbench).
