---
name: retro
summary: Reviews a finished coding session and proposes ranked changes to the agent's checks, standards, docs and steering files so the next run goes better.
pin: 878241202bf7ec97c0952287f1633f6f0ddf1a6e
credit: adapted
credit_text: Adapted from [Matt Pocock's retro skill](https://github.com/mattpocock/skills), MIT License. The entrypoint changes only how it points at the writing-for-agents skill.
credit_license: MIT
---

## What it does

`retro` runs a **retrospective** on a coding session. It does not grade the agent or fix the code. It suggests improvements to the agent's **environment**: the files, checks, rules and tools around it, so future runs hit fewer of the same problems.

It works in four moves. It loads the `writing-for-agents` skill for style. It reads the primary sources for the session you name, which can mean searching session logs on your machine, and it defaults to the current session if you name none. It looks for improvement candidates in seven categories. Then it presents them to you, most severe first.

The seven categories:

- **Navigation**: how hard it was to find the right files, and whether files depend on each other in ways nobody wrote down. A **navigation pointer** is a short link from a file the agent always reads to the place that holds the detail.
- **Automated checks**: linting, typing, tests or filesystem linters that would have caught a mistake. The retro reads the repo's own check scripts and CI workflow first, so a check that exists but is unwired or silently broken becomes the finding. A **guardrail** is any automated gate, either a commit hook or a CI job, that runs the repo's lint, type or test command. A repo with none is a finding on its own.
- **Coding standards**: whether the **reviewer agent** needs a new rule, or an old one removed or clarified. The retro sorts the violation first. If a program could detect it, such as a banned call, a wrong import form or a misplaced file, that is a **mechanical** violation, and it should get a custom lint rule, a pre-commit hook or a CI job. The written standards file is kept for **judgement calls**, like cross-file consistency.
- **Global AGENTS.md**: steering text that belongs in coding standards or checks instead.
- **Tool economy**: expensive tool calls, or custom CLIs and MCP servers that waste tokens.
- **No-ops**: steering lines that change nothing about what the agent does.
- **Information access**: facts the agent could not reach, such as dev server logs or read-only access to a third-party service.

A short reference in the skill says where fixes should live. The implementation agent carries the most **context pressure**, since it explores, writes and debugs. The review agent gets only a diff, so standards are best enforced there. Steering files like `CLAUDE.md` and `AGENTS.md` load into every agent's context and should hold little beyond navigation pointers. `CODING_STANDARDS.md` is read at review time and should gain pointers into docs folders past about a thousand lines. Docs are reference files that other files point to, and existing docs come before new ones.

## When to use it

Use `retro` after a session that went badly, slowly or expensively, or after a stretch of work when you want the setup tuned. You have to ask for it. The skill file turns off model invocation, and its Codex metadata turns off implicit invocation, so the agent will not start it on its own.

A **Workbench** is a project's set of records, rules and tools managed by the Workbench skills. The neighbours below mostly work on one.

| What you have | Reach for |
|---|---|
| A finished session and a hunch the setup could be better | `retro` |
| One candidate from a retro that you want fixed and measured | [`improve-workbench`](/skills/improve-workbench) |
| A read-only check of whether a Workbench's controls and records agree | [`audit-workbench`](/skills/audit-workbench) |
| A recurring failure whose cause you do not yet know | [`diagnose-and-propose`](/skills/diagnose-and-propose) |

## Example request

> Run a retro on the session where the agent spent an hour hunting for where invoice totals are computed, then reported done with a broken type check. What should we change in the repo so that doesn't happen again?

For a session like this, expect candidates in categories such as Navigation (the totals logic had no pointer) and Automated checks (nothing ran the type check before the work was reported finished), listed by severity.

## What it requires

- A session to review: the current one, or one you name whose logs the agent can find on the machine.
- Read access to the repo's steering files, check scripts and CI workflow.
- The `writing-for-agents` skill, which it loads first. The skill calls for no Workbench or other record.

## What it does not authorize

The skill frames the agent as suggesting improvements, and its last step is to present the candidates to you. It describes no edits.

- Running a retro does not edit steering files, add checks, change standards or install anything. Those are separate changes for you to decide on.
- It does not show that a suggestion would help. Nothing in the skill reruns a job or measures an effect. For that, take one candidate to [`improve-workbench`](/skills/improve-workbench).
- The skill says nothing about approval, merging or publishing. In a project with its own rules for those, the project's rules govern any follow-up.

## FAQs

### How is this different from improve-workbench?

`retro` produces candidates from one session. `improve-workbench` takes a single job through a measured loop and records whether a change helped. It names a retro as one thing that can start it, and says to bring one candidate there, not the whole list.

### What if I do not say which session to review?

It defaults to the current session. If you meant an older one, name it, because the skill may need to search session logs on the machine to find the primary sources.

### Why does it keep proposing a hook or lint rule instead of a written rule?

By design. The skill says to default to building a check for anything a program can detect, and to keep written standards for judgement calls.

### What if the repo already has a lint or test command?

The retro should read it first. A check that exists but is not wired into a hook or CI, or is silently broken, is the finding. If it suggests a check you already have, ask it to read your check scripts and CI workflow.

## It's working when

- It names the session it reviewed, and its findings point at things that happened in that session.
- Candidates fall under the named categories and are ordered by severity, with mechanical problems answered by hooks, lint rules or CI jobs rather than prose rules.
- Checks the repo already has are recognized, and unwired or broken ones show up as findings.
- The output is a list of suggestions for you to review, with no files changed.

## Where it fits in the workflow

`retro` belongs to the **Improve** stage, which covers learning from work and fixing the system around it. It comes after a session or a stretch of Journey work (a **Journey** carries one Task, a single assigned unit of work, from build to submit), and it uses [`writing-for-agents`](/skills/writing-for-agents) for style. Its output feeds [`improve-workbench`](/skills/improve-workbench), which takes one candidate through a measured change. [`audit-workbench`](/skills/audit-workbench) and [`diagnose-and-propose`](/skills/diagnose-and-propose) sit beside it in the same stage.
