---
name: writing-for-agents
summary: A short method for writing and trimming documents that agents read, such as skills, AGENTS.md files, Specs and Tasks, so each stays small, clear and reviewable.
pin: 878241202bf7ec97c0952287f1633f6f0ddf1a6e
credit: adapted
credit_text: Adapted from [Matt Pocock's writing-for-agents skill](https://github.com/mattpocock/skills/tree/d81f3a183412e71a5b1e84ca21bc1a35eea03a60/skills/productivity/writing-for-agents), MIT License. The compact method in the skill is Kayden Clark's revision, and the skill-mechanics companion adapts upstream guidance to this catalog's actual rules.
credit_license: MIT
---

## What it does

Some documents exist mainly for an agent to read: a skill, an `AGENTS.md` or `CLAUDE.md` file, a **Spec** (a document describing a goal and how to tell it has been met) or a **Task** (one assignable unit of work). This skill is a short writing method for composing and trimming them. The idea behind it: every word spends the reader's attention and context, files that load often spend it repeatedly, and a file too large for its owner to review has already failed.

The method has four stages, each protecting something different.

- **Scoping** guards against writing the wrong thing. Pin down the document's purpose, its audience and its **information owner** (the document or person responsible for a given fact). Find the size limit that already applies to this kind of artifact instead of making one up, and sort what belongs here from what belongs elsewhere.
- **Composing** guards the first read. The main point comes first, in concrete words, with one term per idea and one job per paragraph.
- **Placing and pruning** guards against sprawl. Each fact gets one home, and other places point to it and say why a reader would follow. Filler, repeats, obvious advice and idle examples come out, and related statements merge. Spare room is not a reason to fill it.
- **Reviewing** guards against fooling yourself. Reread the draft from the audience's seat, then from the owner's. Recheck the limit, the links and fidelity to the source, and tighten again wherever nothing is lost.

Two guardrails run through all four. Brevity must not hide logic: constraints, exceptions and distinctions stay, since a reader forced to guess a missing step is worse off than with a longer page. And compression must not turn cryptic: use precise wording, never shorthand.

While drafting, the skill points to the plain-language guide owned by [author-skill](/skills/author-skill), a table of habits to avoid (synonym rotation, verbs turned into nouns, jargon, run-ons) and their fixes.

## When to use it

Reach for it when you draft, rewrite or shrink a document whose main reader is an agent. It covers scope (what the document holds versus leaves to another owner) and wording. An agent can match a request to its one-line description, or you can name it.

| What you have | Reach for |
|---|---|
| A bloated `AGENTS.md`, Spec or Task file to tighten | `writing-for-agents` (this skill) |
| A skill to create, repair or consolidate from an agreed workflow | [author-skill](/skills/author-skill), which hands its pruning pass to a separate agent that uses this skill |
| Skill descriptions and pointers whose wording needs sharpening | `writing-for-agents`, plus its skill-mechanics note |

## Example request

> Our AGENTS.md has grown to four screens of rules and half repeat what package.json already says. Use the writing-for-agents skill to cut it to what an agent really needs, and keep the exceptions.

The agent would look up the limit for that file type, drop what the repository already answers, keep the unwritten conventions and reasons, and reread the result as a fresh agent would.

## What it requires

- The document to write or revise, plus who reads it and who owns its content.
- A size limit. The skill says to find the one that applies and not invent it. The folder includes a budgets file counting characters (Unicode code points), not words. `AGENTS.md`, `BLUEPRINT.md`, `ARCHITECTURE.md` and `RUNBOOK.md` target 900 to 1,500 with a maximum of 3,000. `LANDMARK.md`, `SPEC.md`, `TASK.md` and `TASKS.md` max out at 8,000. Anything else falls back to 15,000.
- The plain-language guide in the author-skill folder, reached by a relative link, so the two skills sit side by side.
- For skills only: the skill-mechanics and invocation notes in the writing-for-agents folder.

It names no other prerequisite and never says it needs a Workbench (the project records and tools most catalog skills work against).

## What it does not authorize

- **No new authority from a helper.** Calling another skill grants nothing the caller lacked. The caller's scope and the host's invocation limits still apply. The host is the agent app running the skill.
- **No starting a skill by naming it.** A skill name in a catalog, a history or a recommendation is only a reference, and suggesting an option reserved for the user does not give the agent leave to run it.
- **No approval of any kind.** The skill edits prose. It has no review, merge, publishing or sign-off step, so a tidy rewrite does not mean the owner accepted it.
- **No dropping required material.** When revising a skill, its required behavior, credits and invocation restrictions survive every cut. A description alone also proves neither reachability nor context cost.

## Writing a skill specifically

When the document is a skill, the mechanics note adds three rules.

**Invocation.** A **model-invoked** skill (one the agent can pick up on its own) needs a description that names the job it does and the separate situations that should trigger it. A **user-only** skill needs a stated explicit-request boundary and the host's supported policy. In this catalog, keep the required description and put that boundary in it. A vendor flag (a host-specific switch) may not hide a skill on every host, so confirm how your own host behaves before relying on one.

**Splitting.** Divide a skill only when a caller has a separate need of its own, and keep deeper material one link away, with the link text describing the contents and the moment to open it. A **router** is a skill that looks at the actual candidate skills and points to the lightest route that fits, as [ask-workbench](/skills/ask-workbench) does. Include one only when it spares the reader navigation work.

**Calling other skills.** To make an instruction run another skill, name it and give its trigger. Without native invocation, the agent opens that skill's file, follows it, and reports what was missing, never claiming a native call it did not make. The note presents this as a writing convention rather than a measured success rate.

## Background in the upstream reference

The folder preserves Matt Pocock's full upstream guide. It is background, not something the skill runs, and the skill's instructions never link to it.

## FAQs

### Does shorter always mean better?

No. The goal is the smallest document that keeps the meaning. Cutting until the reader must rebuild missing logic, or until the wording turns cryptic, is a failure the method names. Constraints, exceptions and distinctions survive every pass.

### How is this different from author-skill?

author-skill builds or repairs a whole skill and owns the plain-language guide. This skill is the prose method underneath, and it also covers documents that are not skills. At author-skill's pruning pass a separate agent applies this method, because the author never prunes its own work, and the author reruns its cases afterward. If delegation is unavailable, author-skill keeps the full draft and reports pruning as incomplete.

### What if my artifact is not in the budgets file?

Do not invent a number. The file offers a 15,000-character default ceiling, but the skill's rule is to use the limit that applies, which only the artifact's owner can confirm. Also check the unit: the skill speaks of a word budget while the file counts characters.

## It's working when

- The document opens with its essential meaning, and each paragraph does one job.
- Every fact or rule has one home, and links say when to follow them.
- The same concept always uses the same word, and filler and repetition are gone.
- Constraints and exceptions survive pruning, with nothing squeezed into shorthand.
- The result fits the applicable limit and the owner can realistically review it.
- A reread as the intended reader needs no guessing, and links and source fidelity check out.

## Where it fits in the workflow

It belongs to the Improve stage (Learn and fix), as a supporting skill beside the main flow of [retro](/skills/retro) then [improve-workbench](/skills/improve-workbench). Its neighbours there include [audit-workbench](/skills/audit-workbench), [evaluate-workbench](/skills/evaluate-workbench) and [diagnose-and-propose](/skills/diagnose-and-propose). Its closest tie is author-skill, which delegates its pruning pass to a separate agent that uses this skill. The output is the revised document, which goes back to the owner of that artifact for review.
