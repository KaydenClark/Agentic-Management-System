---
name: readback
summary: Has your agent write down what it understood, why, what result you want and what it will do, so you can correct it before any work starts.
pin: 878241202bf7ec97c0952287f1633f6f0ddf1a6e
credit: original
credit_text: Original to Kayden Clark.
---

## What it does

A **readback** is a short written record of what the agent believes you meant. You read it, correct it and approve it before anything is built on it. The skill is one small file: a fixed format plus rules about honesty. The record stays concise and easy to correct, and you can use it in your own systems.

The record always has four sections, in this order:

1. **Summary.** The subject, request, idea or direction, with the important details, constraints and distinctions you gave.
2. **The why.** The reasoning or worry behind the request. If you never said why, the readback labels any guess as an interpretation or says the reason is unstated.
3. **The intended result.** The outcome and the conditions you set for it. It names the agreed artifact and what form it takes, so you can recognize it later.
4. **What I will do.** The agent's own steps, up to where it stops: the artifact or destination, its form, any checks, and any delivery you actually authorized. These are steps for the agent, never chores for you, and need no exact code.

The first three sections use neutral, declarative voice, the way a durable record reads: "The proposed change is..." instead of "I want...".

Two ideas run through the skill. **Meaning and uncertainty are preserved**: the agent separates what you said outright from what it inferred and names missing information instead of filling it in. And **the record is proposed until you approve it**: approval confirms the documented meaning, while starting work needs its own authorization.

The fourth section keeps what you have already authorized distinct from the plan it describes. When you have forbidden implementation, the readback ends at the record and presents later steps as depending on a go-ahead. Limits you stated, like staying local or opening a draft pull request without merging, stay in the text. The agent also lists any consequential open choices (ownership, artifact, format, delivery, stopping point) and makes up neither a destination nor a permission to publish. A half-formed idea can end at the readback with those gaps in plain view.

## When to use it

Ask for a readback when you want to check the agent's understanding before it acts, or want a clean statement of intent to keep. It works in any conversation or project, from early alignment through handoffs.

Other skills use it too. [Grilling](/skills/grilling) finishes only when you explicitly confirm a four-section readback; individual interview answers do not count. [Align-concept](/skills/align-concept) uses readback for the proposed intent it asks you to confirm.

| What you have | Reach for |
|---|---|
| A request you want the agent to restate and check before acting | `readback` |
| A vague plan you want challenged branch by branch until it is settled | [grilling](/skills/grilling) |
| A confirmed readback you want kept as the intent record | [align-concept](/skills/align-concept) or [jot](/skills/jot) |
| Confirmed intent you want written up as a Spec (a document describing the destination) | [map](/skills/map) |
| A Spec or settled plan you want split into Tasks (single-run work assignments) | [plan](/skills/plan) |

## Example request

> Before you touch anything, give me a readback of what you think I'm asking for: move the invoice export off the nightly job and into the request handler. Local only, no PR yet.

The agent answers with the four sections. The limits (local only, no PR) appear in "What I will do," with steps phrased as conditional on your approval.

## What it requires

Very little. The skill is one instruction file with no scripts or special tools. It does not need a Workbench, the repo structure of records that many of the catalog's other skills read and write. It needs only the conversation or project context the readback is about.

## What it does not authorize

- **Execution.** Approving a readback confirms the meaning it documents. Doing the work still requires authorization for that scope.
- **Publishing or delivery.** Only delivery you actually authorized appears in the plan. The skill tells the agent to invent no destination and no permission to publish.
- **Overriding limits.** A prohibition on implementation, or a limit such as local-only work, is carried into the readback and keeps binding.
- **Settling open choices for you.** If it is unclear who owns the work, what the output is, or where the agent stops, the readback lists those gaps and leaves them for you to decide.

Align-concept adds its own rule: a plain "yes" to a displayed readback that proposes bounded steps confirms the meaning and authorizes those steps together. That is align-concept's policy, not readback's.

## FAQs

### Is a readback just a summary?

No. A summary says what was said. A readback also records why, what result counts as done and what the agent plans to do, keeps your limits attached, and marks interpretations and gaps instead of smoothing them over.

### Does saying yes start the work?

Not on its own. Approval confirms the meaning, and execution requires authorization for that scope. Align-concept defines when one reply can do both. If you only want to approve the wording, say so.

### What happens when the readback is wrong?

The record is proposed until you approve it, so a wrong version is never settled. Tell the agent what to change and ask for a revised readback before approving. Align-concept spells out this revise-and-reconfirm loop for saved intent.

### Where does the approved readback get saved?

Not in this skill, which only produces the record. [Align-concept](/skills/align-concept) uses [jot](/skills/jot) to save the exact confirmed text as the intent record.

## It's working when

- The record has just four sections, in order: Summary, then The why, then The intended result, then What I will do.
- The first three sections read as neutral statements, not "I want" or "you want."
- Inferences are labeled, and missing information, including an unstated reason, is named instead of invented.
- The result names a specific artifact and form you could recognize later.
- The record is short enough to correct quickly, and its plan lists only the agent's steps, up to a stopping point.
- Your limits, such as no implementation or no merge, appear in the plan, with later steps marked conditional.
- Open choices about ownership, format, delivery or stopping point are visible, not decided silently.
- The agent waits for your approval before treating the readback as confirmed.

## Where it fits in the workflow

Readback sits in the **Align** stage, where you and the agent build a shared concept. It is the second skill in the main flow, after [grilling](/skills/grilling), which gathers and challenges the details; readback is the artifact you confirm at the end. [Align-concept](/skills/align-concept) and [align-docs](/skills/align-docs) build on both and hand the confirmed text to [jot](/skills/jot) for storage.

Next comes the Prepare stage, where [map](/skills/map) and [plan](/skills/plan) turn confirmed intent into a destination and Tasks. You can also use readback outside that sequence whenever you want the agent's understanding on paper first.
