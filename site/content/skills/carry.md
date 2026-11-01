---
name: carry
summary: Tells your agent to own an objective end to end, answer its own questions from what you already said, and stop only for real blockers.
pin: 878241202bf7ec97c0952287f1633f6f0ddf1a6e
credit: original
credit_text: Original to Kayden Clark.
---

## What it does

`carry` is a short stance for an agent that has been handed a goal and permission to finish it. Instead of doing one step and checking in, the agent takes **ownership** of the whole objective. It follows your intent through the work and through verification, and it stays responsible for the combined result even when it brings in helpers.

The skill is a single file with no scripts or reference documents. It is a set of behaviors, not a pipeline. Three ideas matter.

**The authorized endpoint.** This is the furthest point you have already approved: a finished change, a pull request, a merged branch, whatever you actually said. The agent works up to that point and no further.

**Resolve before asking.** Before it asks you anything, the agent looks through the conversation and the relevant project sources for an answer you already gave, and settles what it can within the authority and tools it has. It asks only about a real preference, a tradeoff, a missing authorization, or a resource it cannot reach.

**Blockers and hand-backs.** A **blocker** is a genuine stopping point, and the skill treats it as normal rather than as a failure. At one, the agent names the specific cause and the smallest thing you could do to unblock it, and keeps going on work the blocker does not touch. A **hand-back** is any other return that is not a blocker. Each is recorded with its specific cause and the smallest supported correction, in the project's existing records or in the conversation, not in a new tracking format. If the correction is supported and in scope, the agent applies it. If not, it names the gap that remains.

## When to use it

Reach for `carry` when you have a clear goal, you have said how far the agent may take it, and you want it finished without a stream of check-in questions.

It is a stance you ask for, not an engine. It defines no stages, roles or record formats, so pair it with the skill that does when you need those. The skill itself names no neighbour except orchestration; the placement below comes from the catalog's chart.

| What you have | Reach for |
|---|---|
| A goal and an approved endpoint, and you want it finished with minimal interruption | `carry` |
| Several implementors to coordinate toward an endpoint | [orchestrate](/skills/orchestrate) |
| One authorized Task (a single assigned unit of work) to take through Implement, Check, QA and Submit | [journey](/skills/journey) |
| Finished work that needs to reach its target branch | [land](/skills/land) |
| An unclear request, or no sense of which workflow fits | [ask-workbench](/skills/ask-workbench) |

## Example request

> Carry the dark-mode settings fix through to a pull request. You have my go-ahead to implement and open the PR, nothing beyond that. If something is unclear, check what I already told you before you ask me.

The agent treats the pull request as the endpoint and comes back only for a real blocker, such as a design choice you have not weighed in on.

## What it requires

The skill file names no tools, records or other skills as prerequisites. It relies on an objective specific enough to act on, an endpoint you have already authorized, and the project's existing records and conversation, which it searches for answers and uses to log hand-backs. It does not say a Workbench (a project's structured set of records and skills) is required.

## What it does not authorize

Running `carry` adds nothing to your agent's permissions. The skill rules out inventing a substitute objective, expanding authorization, and bypassing your intent. As an illustration of the middle one, if you approved a pull request, `carry` does not turn that into a merge. It also does not let the agent fill in a missing preference, tradeoff, authorization or resource on its own; those are exactly what it asks you about.

## FAQs

### Does carry mean the agent will never ask me anything?

No. The agent asks only what it could not resolve from your earlier messages and the project sources. A real preference, tradeoff, missing authorization or unavailable resource still comes back to you.

### What does the agent do when it gets stuck?

It states the specific cause and the smallest input or action it needs from you, and unaffected work continues. If it just stops with a vague message, it has not followed the skill, so ask for the exact cause and the smallest unblocking step.

### The agent asked me something I had already told it. What now?

That is a miss against the skill, which requires checking the conversation and project sources first. Point the agent to where you answered and ask it to continue.

### How does this differ from orchestrate or journey, and will it merge for me?

`carry` is about ownership and when to ask. [orchestrate](/skills/orchestrate) coordinates implementors and [journey](/skills/journey) moves one Task through its stages; since the skill allows orchestration where useful, `carry` can sit above them. It merges or publishes only if you already authorized that endpoint.

## It's working when

- The agent keeps working toward your objective and stops at the endpoint you authorized.
- Its questions are real preferences, tradeoffs, authorizations or missing resources, not things you already answered.
- Each blocker comes with a specific cause and the smallest request to you, while unaffected work continues.
- Hand-backs are logged with a cause and a supported correction, in existing records or in the chat.
- The final report separates what was completed, what was verified, and what is still blocked.

## Where it fits in the workflow

`carry` belongs to the Journey stage (the build stage, where each Task gets built), alongside [orchestrate](/skills/orchestrate) and [journey](/skills/journey). In the catalog's general flow, that stage follows alignment and planning work such as [grilling](/skills/grilling), [readback](/skills/readback), [map](/skills/map) and [plan](/skills/plan), but `carry` itself does not require any of them. It can use [orchestrate](/skills/orchestrate) for execution. If your authorized endpoint stops short of merging, [land](/skills/land) takes finished work onto its target branch.
