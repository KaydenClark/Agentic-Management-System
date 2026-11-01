---
name: jot
summary: Saves what the owner decided, corrected or found in the right project record, with its source and status, so the next session can resume cold.
pin: 878241202bf7ec97c0952287f1633f6f0ddf1a6e
credit: original
credit_text: Original to Kayden Clark.
---

## What it does

Agents lose context between sessions. **Jot** writes down what the owner decided, corrected or discovered, in a place the next agent will look, and reads it back when work resumes.

It works inside a **Workbench**, the project structure created by [setup-workbench](/skills/setup-workbench). A Workbench holds **Specs** (records of an intended result), **Tasks** (single assigned units of work), a **Wiki** (a notes area routed from `MEMORY.md`) and the tools agents use. Jot captures *understanding*: what the owner wants, what they corrected, what an agent found, and why. Task progress, acceptance and proof stay in their own records, which a jot links to.

The key ideas:

- **Claim.** A statement carried by some artifact. Jot first works out what the claim is for, based on what it targets and what is being done with it. One Spec can hold acceptance criteria, evidence, rationale and unconfirmed intent side by side.
- **Role.** The job a claim does right now, one of six in the **Governance Stack**. Roles are relative to the work at hand, not folders, stages or a ranking.
- **Entry.** A saved record with a kind (intent, observation, inference, proposal, question or verification), a state (unresolved, confirmed, current or experimental), a dated source, what it supersedes, the claim and the next action. Owner reasons stay separate from agent inference.
- **Owner.** The smallest existing document that should hold the claim, such as a Spec, glossary or decision record. If none covers the topic, Jot creates a small Wiki topic and links it from `MEMORY.md`.

The six roles each answer one question:

| Role | Question it answers |
|---|---|
| Intent | What is wanted but not yet confirmed? |
| Enduring Context | What do we know about meaning and past choices? |
| Grounding | What does the evidence prove, within what limits? |
| Canon | What authority is this target judged against? |
| Actuality | What is currently present and under work? |
| Projection | What gets displayed, derived from other claims? |

The flow has three beats: capture while the answer is fresh, verify by reading it back, and resume by rereading the topic, its corrections and pending items, then rechecking live state.

## When to use it

Say "jot this" when the owner answers a question, corrects an agent, or reveals something a later reader would need. Use it before a report that depends on a fresh finding, and to recover what was decided when you start cold. Capture as understanding arrives, not at closeout.

| What you have | Reach for |
|---|---|
| An answer, correction or discovery worth keeping | `jot` |
| A confirmed decision to turn into a durable document | [promote](/skills/promote) |
| A concept to interview out and lock in | [align-concept](/skills/align-concept) |
| A concept that touches documentation as well | [align-docs](/skills/align-docs) |
| Wording to get approved in four sections | [readback](/skills/readback) |
| Terms or a glossary entry to settle | [domain-modeling](/skills/domain-modeling) |
| Work records that disagree with what happened | [reconcile](/skills/reconcile) |
| A conversation to pass to another agent | [handoff](/skills/handoff) |

## Example request

> The owner just told me the dashboard should only show shared pages, never private ones, and that this replaces what we assumed last week. Jot that so the next session doesn't redo the question.

Because the meaning changed, Jot does not just append a note. It finds the smallest existing owner for the dashboard topic (or a new Wiki topic if none covers it) and records a pending correction, then asks the owner to confirm a revised readback. Until they do, the earlier confirmed intent stands and dependent work is blocked. After confirmation, Jot saves the confirmed text exactly, moves the current-intent pointer, links old to new, reads it back, and reports where it saved and whether anything is unpublished.

## What it requires

- **A Workbench.** Jot looks for the Workbench manifest and the `spec-workbench` tool at the project root and stops if either is absent, telling you to run `setup-workbench` first.
- **The capture tool.** The Workbench ships one, currently `workbench/tools/jot.mjs`, and Jot resolves its current interface before use. At this pin it offers `read`, `add`, `correct` and `search` for active Markdown Wiki topics. A write needs the page's current revision hash (from `read`), a visibility, kind, state, source and author, and design-concept pages also need an `--operation` naming the authorized operation. It cannot edit passages inside a Spec or decision record, so Jot uses those documents' own procedures there.
- **Context to read first.** Project instructions, ownership routes, the glossary and the topic's sources and corrections. `read` returns entries and the revision but not the page's surrounding prose, so Jot reads that prose and its governing links too.
- **A confirmed readback, for intent.** For concept intent, the owner's explicitly confirmed [readback](/skills/readback) is the record to save.

## What it does not authorize

Saving a claim grants nothing beyond the save. Capture authorizes no:

- edit to a governing document, map or plan, implementation, verdict, publishing or merging;
- execution of the intent it records. Confirming meaning, permitting an operation and accepting delivery are three separate things, even when they arrive together. A confirmation is reusable only for its own revision and scope, and execution needs an explicit owner grant of scope, either in that confirmation or in a separate instruction;
- proof. Confirmed understanding can be saved before any code exists, and it shows neither working behavior nor accepted delivery.

An agent-written readback, a recommendation, silence or a bare command does not make intent confirmed. The `confirmed` flag only stores a supplied judgment, so the source must show a real owner confirmation.

## Corrections and privacy

Jot never edits history. A material change goes through a pending correction, as in the example. A smaller one becomes a sourced entry naming what it supersedes.

New context defaults to shared after an exposure review. Private capture needs an explicit request, stays local and ignored, and reading it needs an explicit flag. Jot omits trivia, duplicates, raw transcripts and secrets.

## FAQs

### Where does a jot actually get saved?

In the smallest existing owner of that claim. If none fits, in a Wiki topic reached from `MEMORY.md`.

### What happens if my write fails because the page changed?

The write is refused and nothing is saved. Jot rereads, reconciles with the new content and retries with the new revision. If saving still fails, it keeps the text and reports exactly what stayed unsaved.

### Does a jot need its own pull request?

No. It publishes through existing authority and the project's checked workflow, then fetches the target fresh before claiming delivery. A local write, a branch push and arrival on the target are different states, and the receipt says which is true. If publishing fails, Jot keeps the recoverable work and names the failed boundary.

### What if the docs and the code disagree when I resume?

Jot rechecks live state against the accepted claims. Newer Canon can reveal an implementation gap, and newer verified Actuality can reveal documentation drift. Neither side wins automatically or authorizes changing the other.

### Will it re-ask questions I already answered?

Not if they are sourced and confirmed. They stay settled unless a named premise, a contradiction or an owner correction reopens them. Note that individual answers can settle a choice or a fact, but only the owner's confirmed readback makes assembled intent confirmed. On resume Jot also reads omitted entries and the correction chain.

## It's working when

- Answers and corrections land in an owner before the report or action that depends on them.
- Each entry carries a kind, a state, a dated source and speaker, and what it supersedes.
- Corrections link to the claim they replace, and earlier claims stay readable.
- Confirmed intent matches the owner's confirmed readback text exactly, and the current-intent pointer leads to it.
- Before a voluntary closeout, Jot reconciles important uncaptured understanding and returns a brief receipt with the location, the real save or publication state, and any remaining gap.
- A later session resumes from the topic page and its pending readbacks without re-asking settled questions.

## Where it fits in the workflow

Jot sits in the Align stage as a supporting skill. It records the state of [align-concept](/skills/align-concept) and [align-docs](/skills/align-docs), which run the interview and handoff, without starting execution, and it stores the owner-confirmed [readback](/skills/readback) as the intent record. For glossary changes and consequential decision records it uses [domain-modeling](/skills/domain-modeling).

Downstream, [promote](/skills/promote) moves selected, supported claims into their durable owners, and [reconcile](/skills/reconcile) brings work records back in line with what happened. Jot needs [setup-workbench](/skills/setup-workbench) to have run first.
