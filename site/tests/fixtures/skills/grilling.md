---
name: grilling
summary: "Fixture article: questions a plan one round at a time until you and the agent agree on what it means."
pin: 878241202bf7ec97c0952287f1633f6f0ddf1a6e
credit: adapted
credit_text: Fixture credit adapted from [an example public source](https://example.com/skills), MIT License.
credit_license: MIT
---

## What it does

This is a **fixture article** for the skills wiki tests, not the published article. It exercises every block the renderer supports: a **round** is one question with *why* it matters, and a `frontier` is the set of open questions.

## When to use it

Reach for it when a plan has open choices.

| What you have | Reach for |
| --- | --- |
| A plan with open choices | [grilling](/skills/grilling) |
| A settled plan to read back | [readback](/skills/readback) |
| A long cell with `improve-codebase-architecture` and a pipe \| inside | [map](/skills/map) |

## Example request

> Grill me on this plan before we write the Spec.

The fixture request is one sentence.

## What it requires

- A plan or idea to question.
- A Workbench, for the records it reads.

## What it does not authorize

1. Writing the Spec.
2. Merging, publishing or Human QA.

## Rounds and the frontier

A skill-specific section sits between the fixed ones.

### One round

Each round asks one question.

```
node workbench/tools/spec-workbench.mjs doctor
```

## FAQs

### What if the agent asks two questions at once?

Ask it for one.

### Can I stop early?

Yes, say so.

### Does it write anything?

Only notes you ask for.

## It's working when

- Each round asks one question.
- You can say what was settled.

## Where it fits in the workflow

It is the first main-flow skill of the Align stage. After it comes [readback](/skills/readback); see the [stage on the index](/skills#align) and [Start here](/start).
