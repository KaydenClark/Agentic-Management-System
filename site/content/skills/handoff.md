---
name: handoff
summary: Writes a handoff note for the current conversation and pushes your work with it, so a fresh agent session can pick up where you stopped.
pin: 878241202bf7ec97c0952287f1633f6f0ddf1a6e
credit: adapted
credit_text: Adapted from [Matt Pocock's handoff skill](https://github.com/mattpocock/skills), MIT License. This catalog adds a Codex setting that keeps the skill user-invoked.
credit_license: MIT
---

## What it does

Handoff turns the current conversation into a **handoff document**: a note a fresh agent can read to continue the work. You start a new session and point it at the note.

What the skill does depends on where you are.

In a **Git repository**, the aim is that the next agent can find both the work and the note from GitHub alone. The agent does four things, in order:

1. Commits the real work on its feature branch and pushes it first, so the note describes something reachable. Stashing is ruled out.
2. Writes the note as `HANDOFF.md` at the repository root of that branch. The top of the file identifies the branch and the latest commit, links the pull request if one exists, and lays out where things stand: what is finished, what is not, which checks fail, and the next move.
3. Commits and pushes `HANDOFF.md`, then confirms the remote branch actually has it.
4. Later, the agent that takes the work over removes `HANDOFF.md` in its own commit. That happens once the content lives in the pull request or the task record, and before the pull request merges. The note is a temporary bridge, not a lasting file, so no stale copy stays in the branch.

**Outside a Git repository**, the agent saves the note in the operating system's temporary directory and tells you the full path, so you can give that path to the next session.

Either way, the note ends up with a **suggested skills** section that names the skills the next agent should load through the Skill tool (the agent's way of calling a skill). The new session then starts with the right methods in hand.

Two rules shape the content. The note does not copy what other artifacts already hold, such as specs, plans, decision records, issues, commits or diffs. It points to them by path or URL. And anything sensitive, like API keys, passwords or personal information, is redacted.

## When to use it

Use it when work has to pass to another agent session, or to you later, and you want that session to start informed. It is **user-invoked**: the skill is marked so the model does not run it on its own, and the Codex settings file (Codex is an agent runner) turns implicit invocation off. You ask for it.

You can add a short argument saying what the next session is for. The skill treats it as the focus and tailors the note to that purpose.

| What you have | Reach for |
| --- | --- |
| A session to pause so a new agent can continue the same work | `handoff` |
| Not sure which skill fits the next step | [ask-workbench](/skills/ask-workbench) |
| A read-only status report for the owner, drawn from the project's task board | [sitrep](/skills/sitrep) |
| Project records that disagree with what actually happened | [reconcile](/skills/reconcile) |
| A fact or correction to preserve while the work continues | [jot](/skills/jot) |

## Example request

> /handoff the next session will finish the failing export tests on this branch and open the pull request.

The agent commits and pushes the work, writes `HANDOFF.md` aimed at fixing those tests, pushes it too, and checks that the remote has it.

## What it requires

- A conversation with something worth continuing.
- In a Git repository: a feature branch you can commit to and push, and a remote. The skill assumes the work already lives on a feature branch and says nothing about other cases, so if you are on `main` or have no branch, create or switch to a feature branch before invoking it.
- Outside Git: a writable temporary directory.
- Nothing else. It does not need a **Workbench** (the structured project records of Specs and Tasks that much of this catalog works from). If a spec, plan or issue exists, the note links to it.

## What it does not authorize

The skill grants one consequential thing: committing and pushing the work and the note on the feature branch, plus writing the document. It says nothing about merging, reviewing or approving, so none of those follow from running it.

Redaction is part of the job, not an option, and stashing is ruled out because stashed work cannot be found from GitHub.

## FAQs

### What if there is no Git repository?

The note goes to the OS temporary directory and the agent reports the full path. The next session needs that path to find the file, so pass it along.

### Should the note repeat what is in my specs and issues?

No. The skill tells the writer to link to existing artifacts by path or URL instead of restating them.

### Does the model run this automatically?

No. It is user-invoked only. If you want a handoff, you ask for it.

### What if the push fails or the remote lacks the file?

The skill has the agent confirm that the remote branch contains `HANDOFF.md`. If the push failed or the file is missing, the handoff is not usable yet. As practical advice rather than skill behavior, fix the cause (credentials or branch protection are common ones) and check the remote again before pointing a new session at the note.

## It's working when

- The work is committed and pushed on a feature branch before the note exists, with nothing left in a stash.
- `HANDOFF.md` sits at the repository root and opens with the branch, latest commit, pull request link if any, what is done and not done, failing checks and the next action.
- The remote branch has been checked and contains `HANDOFF.md`.
- The note points to specs, issues and commits by path or URL instead of restating them.
- A suggested skills section tells the next agent what to load.
- No keys, passwords or personal details appear in the note.
- Outside Git, you were given the full path of the saved file.

## Where it fits in the workflow

Handoff is listed under the **Route** stage (Choose a path) as a supporting skill, alongside [sitrep](/skills/sitrep), [triage](/skills/triage) and [setup-workbench](/skills/setup-workbench). The main skill in that stage is [ask-workbench](/skills/ask-workbench). Handoff is user-invoked and is not tied to a fixed step, so you call it whenever one session ends and another begins.

The note is what the next session starts from. If the right next step is unclear there, [ask-workbench](/skills/ask-workbench) is a sensible stop; that is advice, not something the skill routes to. To keep project records accurate across the pause, see [reconcile](/skills/reconcile) and [jot](/skills/jot).
