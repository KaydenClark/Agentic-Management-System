---
name: handoff
summary: Prepares continuity for another session; AMS keeps its session notes local, even though the published catalog still describes a pushed note.
pin: fb7ad23c963e183b930b23bc5fdf4d309dff292a
credit: adapted
credit_text: Adapted from [Matt Pocock's handoff skill](https://github.com/mattpocock/skills), MIT License. This catalog adds a Codex setting that keeps the skill user-invoked.
credit_license: MIT
---


## What it does

Handoff prepares a short continuation note for a later session. It should identify the work, its current revision, unfinished checks and the next step, while pointing to durable records instead of copying them.

**AMS boundary:** session notes stay on the owner's machine in ignored storage. Publish the work and its Task records through the normal branch route; do not publish the session note. A later session needs access to that local note as well as the repository.

The catalog revision named below still describes a different Git procedure: publish the work, put a temporary note at the branch root, publish that note, and remove it after takeover. That source has not yet been repaired on catalog main. Its instruction to publish a note conflicts with AMS policy and must not be followed here. The current repair effort and its limits are described on [RSI results](/rsi).

## When to use it

Ask for continuity when another session must resume unfinished work. The published skill requires an explicit request; merely reaching the end of a session does not invoke it.

| What you have | Reach for |
| --- | --- |
| Work another session must resume | `handoff`, within the project's storage rules |
| Facts that belong in durable project records | [jot](/skills/jot) |
| Records that no longer match the work | [reconcile](/skills/reconcile) |
| Uncertainty about the next method | [ask-workbench](/skills/ask-workbench) |

## Example request

> Save a local continuation note for the export Task. Link its published candidate and identify the failing check and next action. Keep the note out of GitHub.

In AMS, the resulting note is local and ignored; the agent reports where the next session can find it. The published Task remains the durable execution record.

## What it requires

- A known next-session purpose and enough evidence to describe the current state.
- Access to the project's storage and publication rules before choosing a note location.
- A local ignored destination in AMS, with no secrets in the note.
- Durable work and Task records published only through their authorized delivery route.

The catalog method itself needs no Workbench. That does not remove AMS's project-specific rules.

## What it does not authorize

A note grants no new execution, review, merge, deployment or acceptance authority. It cannot make unpushed work remotely recoverable, and a local note cannot be recovered from GitHub alone.

In AMS, a catalog instruction to commit a session note does not override the local-only boundary. Do not install or promote an unfinished repair merely to make this article match an intended method.

## FAQs

### Is the catalog source already corrected?

No. At the published revision named below, it still asks for a temporary note in the branch. The public article records that conflict rather than claiming a completed repair.

### Where does an AMS continuation note go?

In the project's local ignored handoff area. Share its location with the next session on that machine; keep durable execution facts in the published Task.

### Can a cloud session recover that local note from GitHub?

No. It can read the published work and Tasks, but access to a local session note must be arranged separately. Do not upload the note to solve that access gap.

### What should the note contain?

A compact account of the candidate, completed and unfinished work, verification limits and next step, with links to the records that own the details. Exclude credentials and private source material.

## It's working when

- The continuation points to the actual candidate and its published work records.
- The next session can locate its required context without relying on the previous conversation.
- In AMS, the note remains local and ignored, and no publication claim is made for it.
- Missing access and failed checks remain visible.

## Where it fits in the workflow

The chart places handoff among the supporting methods in Route. It helps another session resume; it does not replace [jot](/skills/jot), [reconcile](/skills/reconcile) or a Task's durable proof.
