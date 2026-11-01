---
name: sitrep
summary: Gives you a short, read-only status report from the project board: what needs your review, what only you can unblock, what is moving and what is ready next.
pin: 878241202bf7ec97c0952287f1633f6f0ddf1a6e
credit: original
credit_text: Original to Kayden Clark.
---

## What it does

`sitrep` answers the owner's question about the project: where do we stand, and what is waiting on me? It reads the task board and the records behind it, then writes a compact report in the conversation, changing nothing and claiming no work.

A **Workbench** is the folder structure and tooling a project uses to track agent work. A **Spec** is a written destination with acceptance criteria, and a **Task** is one assignable slice of it. The **board** is a generated summary of both. The Specs, Tasks, issues and pull requests own the facts, so the board never outranks them.

A run goes like this:

1. **Pick the scope.** The default is the whole board. You can ask for one landmark (a larger goal that groups Specs), one Spec, one PR or one branch; outside work appears only if it blocks that scope.
2. **Check freshness.** The skill fetches the remote and compares your checkout with the integration branch. If you are behind, it reads the board as it stands at the remote tip, and it notes uncommitted or unpushed work, which no board shows. A stale board is never regenerated: the skill reads the owning records instead and names who should refresh it.
3. **Sort the work** into the four sections below, each item once. Complete and Backlog show as counts only.
4. **Verify.** For every item in the first two sections, the skill opens the Spec, Task, issue or PR behind it to check that you act next and the blocker still holds. If board and record differ, the report goes with the record and names the mismatch.
5. **Report.** About 300 words for a whole board, readable in a minute, ending with one safe next action and at most one decision for you.

### The four sections

- **Needs your review** is work waiting on your judgment: Human QA (your hands-on check of a delivered result), approving a named candidate, promoting to main or releasing, answering an open question, or approving a draft. An open integration-to-main PR that only you can merge lands here too.
- **You can unblock** is work stuck on something only you can supply: a decision, permission, a credential, a paid service, a missing machine or access, or a priority call between competing work. The report names what you would supply.
- **In progress** is claimed or running work you should know about: stale claims, failed checks or reviews, gates you deferred, and top-priority work. Each line says who holds it, what is done and what is next.
- **To do** is ready work nobody holds, then work queued behind other work, naming what it waits on.

You are listed under Needs your review only when you are the next actor. If an agent must first reconcile findings or prepare the candidate, the item sits under In progress. Within a section, items follow board priority, then how much other work your action releases, up to five lines.

The skill's reference maps board rows onto these sections through their Current slice, Blocker and Next gate cells. A Task blocked on another Task goes under To do. One blocked on your decision or authority goes under You can unblock, and so does a Task missing a capability only you can supply. A Spec parked at its acceptance gate goes under Needs your review when you act next, and under In progress when an agent acts first or you deferred your own gate.

The report also keeps delivery states apart: committed, pushed, PR open, merged and released are different facts.

## When to use it

Ask for a sitrep, status or situation report by name. Models never invoke it on their own: the skill is marked that way, and its bundled agent policy also turns off implicit invocation.

| What you have | Reach for |
|---|---|
| You want status and to know what needs you | `sitrep` |
| You are not sure which skill fits | [ask-workbench](/skills/ask-workbench) |
| A ready Task you want built | [journey](/skills/journey) for one Task, [orchestrate](/skills/orchestrate) for several implementors |
| Something keeps failing and you want the cause | [diagnose-and-propose](/skills/diagnose-and-propose) |
| A merge is blocked or a landing went wrong | [land](/skills/land) |
| Records and board disagree with what really happened | [reconcile](/skills/reconcile) |
| A correction or decision surfaced and should be kept | [jot](/skills/jot) |

## Example request

> Sitrep. I've been away for three days. What needs me, and is the board even current?

## What it requires

- A Workbench created by [setup-workbench](/skills/setup-workbench). The skill first checks for the Workbench manifest and the `spec-workbench` tool. If either is missing, it stops and tells you to run setup rather than building records by hand.
- Read access to the Markdown board, following each Next page link for a whole-room report. A JSON board is planned but not delivered at the pinned revision, and `render --format json` is no substitute, since it only writes a preview file and can refuse a room.
- The read-only `spec-workbench` commands. `doctor` flags a stale board, stale claims and Tasks blocked on other Tasks. `next` shows what is ready, and with `--review` what awaits review; it never claims anything and takes no Spec scope, so a scoped report uses `show`. `list` supplies counts. If a command refuses, the skill says so and falls back to the board files and `show`.
- A Grill Board, only if the project has one. Its pending items go under Needs your review.
- Git access to fetch remote references, the only write-adjacent action allowed.

The Markdown board has no review or Backlog lane and no Task-level Complete totals, so the skill derives these itself and says the counts are Spec-level.

## What it does not authorize

A sitrep routes; it does not authorize.

- **Read-only.** It never claims, closes, renders, edits a record, comments, labels, pushes, merges or starts a service. The reference bans commands such as `render`, `claim`, `close`, `approve`, `verdict` and `complete`, plus the move and retire commands for Specs, Tasks and landmarks.
- **No starting work.** That goes through [journey](/skills/journey) or [orchestrate](/skills/orchestrate). Causes belong to [diagnose-and-propose](/skills/diagnose-and-propose), and blocked merges to [land](/skills/land).
- **No approval.** It records no review, approval or Human QA. It only tells you whether one is waiting.
- **No new files.** If lasting knowledge surfaces, it offers to capture it with [jot](/skills/jot) and never copies live status into docs.

## FAQs

### Why does the report say the board is stale instead of refreshing it?

Refreshing writes files, and a sitrep is read-only. It reads the owning records instead and names who should regenerate the board. Once someone has, ask again.

### Why is something I expected under Needs your review listed as In progress?

You are not yet the next actor. If an agent must still finish a review or prepare the candidate, the item stays In progress with that step named.

### My checkout is behind the remote. Does the report describe my local state?

No. When you are behind, the skill reads the board at the remote tip. Dirty or unpushed work appears on no board, so check that yourself.

## It's working when

- The first line names the scope, the board's revision or date, and whether it is fresh or stale, with the reason.
- Every item in the first two sections was checked against its owning record and says exactly what you are asked to judge or supply.
- Each section stays within five lines, and the report ends with one safe next action and at most one decision.
- No files changed and nothing was claimed.

## Where it fits in the workflow

`sitrep` lives in the **Route** stage (Choose a path), as an also-used skill beside the main entry point [ask-workbench](/skills/ask-workbench). Only a Workbench from [setup-workbench](/skills/setup-workbench) must exist first.

It hands off rather than doing other stages' work. Ready Tasks go to [journey](/skills/journey) or [orchestrate](/skills/orchestrate) in the Journey stage, and blocked merges to [land](/skills/land) in the Complete stage. Records that drifted go to [reconcile](/skills/reconcile), the writing counterpart that updates the owning records and regenerates the board. Durable findings go to [jot](/skills/jot).
