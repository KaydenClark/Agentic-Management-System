---
name: triage
summary: Sorts incoming issues and outside pull requests into labelled states, checks each claim against the code, and leaves an agent-ready brief or a reason to stop.
pin: 878241202bf7ec97c0952287f1633f6f0ddf1a6e
credit: adapted
credit_text: Adapted from [Matt Pocock's skills](https://github.com/mattpocock/skills), MIT License, with the glossary file and the way the tracker is queried changed.
credit_license: MIT
---

## What it does

Triage is a maintainer's sorting desk for your issue tracker. It moves each item through a small set of labelled states, checking facts before it recommends anything. If your repository treats outside pull requests as a request surface, they get the same handling, because a pull request is an issue that carries code.

Each triaged item is meant to hold exactly one **category role** plus one **state role**. These are canonical names, and your tracker's real labels may differ, so the skill asks for the mapping if you have not supplied one.

- **Category roles:** `bug` (something is broken) and `enhancement` (a new feature or improvement).
- **State roles:** `needs-triage` (the maintainer still has to evaluate it), `needs-info` (waiting on the reporter), `ready-for-agent` (specified well enough for an unattended agent), `ready-for-human` (a person has to build it) and `wontfix`.

An unlabeled item normally goes to `needs-triage` first, then to one of the other four, and `needs-info` returns to `needs-triage` when the reporter replies. If an item carries conflicting state labels, the skill stops and asks you first.

When you pick an item, the skill reads the thread, earlier triage notes and, for a pull request, the diff, then runs two checks. The **redundancy check** looks for an existing implementation by domain concept, not only by the request's wording, and reports where it looked; a hit makes the item an already-implemented `wontfix` candidate. The **prior-rejection check** reads the **out-of-scope knowledge base**, a `.out-of-scope/` folder of notes on rejected feature requests, and surfaces any that resemble the new one.

Next it recommends a category and state with reasoning, and waits for your direction. Before any questioning it **verifies the claim**: it tries to reproduce a bug from the reporter's steps, or checks out a pull request and runs the relevant tests. The result is confirmed, failed, or too thin to judge, which usually points to `needs-info`. If the request still needs shaping, it runs [grilling](/skills/grilling) together with [domain-modeling](/skills/domain-modeling), which sharpens project terms and records decisions, updating the glossary and decision records (ADRs) as choices settle.

Then it applies the outcome you choose:

| State | What the skill does |
|---|---|
| `ready-for-agent` | Posts an **agent brief**, a comment written as the contract an unattended agent works from: category, summary, current and desired behavior, key interfaces, testable acceptance criteria and out-of-scope items. It names behavior and types, not file paths or line numbers, which go stale. |
| `ready-for-human` | Posts the same structure, plus why the work cannot be delegated. |
| `needs-info` | Posts notes listing what is established, including anything settled while grilling, and specific questions for the reporter. |
| `wontfix` | Closes the item. If the change already exists, the comment points to where. A rejected bug gets a polite explanation. A rejected enhancement is recorded in the out-of-scope folder, linked from the comment, then closed. |
| `needs-triage` | Applies the label, with an optional comment on partial progress. |

On a pull request, the brief describes what is left to do on the existing diff, such as finishing it or addressing review points. There, `ready-for-agent` means an agent should continue from the diff, while `ready-for-human` means a person can review and merge it.

## When to use it

You invoke it yourself by typing `/triage` and describing what you want in plain language. The model does not start it on its own. Typical requests:

- Asking what needs your attention. It shows three buckets, oldest first: unlabeled items, `needs-triage` items, and `needs-info` items where the reporter has replied since the last notes. Lines are tagged `[PR]` or `[issue]`.
- Naming an item, such as issue or pull request 42, or asking what is ready for agents to pick up.
- Forcing a state, such as moving 42 to `ready-for-agent`, which skips grilling.

If notes from an earlier session exist, it reads them first and shows an updated picture instead of repeating resolved questions.

| What you have | Reach for |
|---|---|
| An inbox of issues or outside pull requests to sort and label | `triage` |
| A read-only status report on your Workbench board (Specs and Tasks), not your issue tracker | [sitrep](/skills/sitrep) |
| A vague request you want pressure-tested one question at a time | [grilling](/skills/grilling) |
| A conversation to pass on to another agent | [handoff](/skills/handoff) |
| Unsure which workflow fits | [ask-workbench](/skills/ask-workbench) |

## Example request

> /triage Show me anything that needs my attention, then let's look at the oldest needs-triage item.

The skill lists the three buckets with counts and one-line summaries. You pick an item, and it recommends and verifies before changing any label.

## What it requires

- An issue tracker it can query, plus configuration saying whether external pull requests count and who is external.
- A mapping from the canonical role names to your tracker's labels, which it asks for if missing.
- Codebase access, with the ability to run tests or reproduction steps.
- A project glossary (`GLOSSARY.md`, or `CONTEXT.md` if one exists) and any decision records, which it reads and updates while grilling.
- Optionally a `.out-of-scope/` folder, read when present and written to when you reject an enhancement.
- The [grilling](/skills/grilling) and [domain-modeling](/skills/domain-modeling) skills for the shaping step. Domain-modeling itself expects a Workbench, the structured project setup these skills work inside.

## What it does not authorize

- Unusual state transitions. You can override any state, but it flags odd moves and asks first.
- Silent forced states. Even on a quick override, it lists the role changes, comment and close it is about to make before acting. If you force `ready-for-agent`, it also asks whether you still want a brief.
- Unmarked posts. Every comment or issue it creates must begin with a one-line notice that AI generated the text during triage.
- Recording built features as rejections. Closing as already implemented never writes to the out-of-scope folder.
- Writing bugs into the out-of-scope folder. Only rejected enhancements go there, whether they came in as issues or pull requests.

## The out-of-scope knowledge base

The folder holds one readable file per rejected concept, not per issue, with a durable reason (project scope, a technical constraint) and a list of prior requests. A deferral such as being too busy right now is not a rejection. Matching is by concept, so a night-theme request matches a dark-mode file.

On a match the skill shows the earlier decision and asks if you still agree. Confirm, and the item joins the prior requests and closes. Reconsider, and the file is deleted or updated; old issues are not reopened, but the new item goes through normal triage. Call them distinct, and triage carries on. A new rejection appends to a matching file rather than duplicating it.

## FAQs

### Can I skip grilling?

Yes. A direct instruction such as moving 42 to `ready-for-agent` skips grilling, and the skill asks whether you still want an agent brief. A verified reproduction or a checked diff is what makes a brief strong, so a forced state without that groundwork gives the agent less to go on.

### What if it cannot reproduce the bug?

It reports a failed attempt or insufficient detail. Thin reports usually belong in `needs-info`, where the notes ask specific questions rather than a generic request for more.

### Why did it not list a teammate's pull request?

Discovery only surfaces external pull requests, as your tracker configuration defines them. A collaborator's in-flight work is not triage work. If you name a pull request explicitly, it is triaged regardless of author.

## It's working when

- Each triaged item ends up with one category label and one state label.
- Each recommendation comes with reasoning and a note of where it searched for an existing implementation.
- Bug claims are reproduced and pull request claims checked against the diff before a brief is written.
- Agent briefs state behavior and testable acceptance criteria, with no file paths or line numbers, and every comment starts with the AI-generated notice.
- Rejected enhancements leave an out-of-scope note, while already-implemented items point to the existing code instead.
- Resumed items do not repeat questions the reporter already answered.

## Where it fits in the workflow

Triage sits in the **Route** stage (choose a path) as a supporting skill. The main flow there is [ask-workbench](/skills/ask-workbench), with [sitrep](/skills/sitrep), [handoff](/skills/handoff) and [setup-workbench](/skills/setup-workbench) alongside it. It works on the tracker's inbox, decides what each item is and whether it is ready, and calls [grilling](/skills/grilling) and [domain-modeling](/skills/domain-modeling) when an item needs shaping. Its output is a labelled, briefed item that a person or an agent can pick up next.
