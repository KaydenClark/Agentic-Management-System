---
name: pr
summary: Writes a pull request body that reviewers can absorb fast, with a small visual, before-and-after evidence and an honest note on how risky the merge is.
pin: 878241202bf7ec97c0952287f1633f6f0ddf1a6e
credit: adapted
credit_text: Adapted from [Matt Pocock's pr skill](https://github.com/mattpocock/skills), MIT License. Its Summary visuals come from the `show-me` skill by [Dex Horthy](https://github.com/dexhorthy) (HumanLayer) and are carried over nearly unchanged. The glossary reference now points at the project's own glossary, and the credits metadata was reformatted.
credit_license: MIT
---

## What it does

`pr` is a fixed template plus a few writing rules for one job: the description of a pull request, called the **PR body**. It shapes the text a reviewer reads. It does not open the PR, push a branch or merge anything.

The template has three sections, always in this order:

| Section | What goes in it |
|---|---|
| **Summary** | A small visual (or a few) that shows the key point of the change |
| **Evidence** | A before and after that shows the change works |
| **Merge Danger** | Whether the merge is a one-way or two-way door, plus its blast radius |

Two rules apply throughout. Skip preambles and keep prose short. Use the vocabulary of the project's glossary when it has one, so the PR reads like the rest of the codebase.

**Choosing the Summary visual.** The skill offers a menu and tells you to pick the leanest view that gets the point across:

- Pseudocode for logic or an algorithm.
- A call tree for runtime control flow.
- A component tree for UI structure, with any state or module boundaries that matter.
- A shallow file tree for file responsibilities or a broad refactor.
- A Mermaid diagram for how parts talk to each other or how data moves.
- A `diff` sketch when the shape already exists and the point is what changed. The same trick works on component trees, file layouts, call trees and control flow.
- The full code block, for mostly new code, for code where trimming would hide ordering or ownership, or when the reader needs a shape to copy.

Put each visual beside the short text it supports. Cut everything that does not help the reader answer their question about this change. You may use one visual or several, but using all of them is unlikely to help.

**Evidence.** The skill ranks it. A screenshot is best, provided your environment can capture one and the change looks different on screen. Execution output comes next: test results or console output. For tests, name the exact test that failed before and passes now, described in pseudocode. Either way, show the before next to the after.

**Merge Danger.** A **two-way door** is a change you can walk back; a **one-way door** involves destructive actions or decisions that are hard to reverse. The cheaper a PR is to roll back, the lower its risk. The **blast radius** is the reach of the change, such as layout shift, broken consumers or mobile responsiveness. Give it as one word, then optionally spell out the ramifications. The skill asks you to consider all the possibilities.

## When to use it

Reach for it when you are about to write or rewrite a PR description. Two neighbouring skills point to it: `journey` uses it when a merge-request body with before-and-after evidence and risks is requested, and `land` uses it at its publish step when a PR is requested.

A **Task** is one assigned unit of work in a Workbench, the project's record system for Specs and Tasks.

| What you have | Reach for |
|---|---|
| A finished change that needs a PR description | `pr` |
| A Task you want carried through build, check and submit | [journey](/skills/journey) |
| Finished work that has to reach its target branch, including merge trouble | [land](/skills/land) |
| A branch or PR that needs an independent review | [code-review](/skills/code-review) |

## Example request

> The retry fix is committed on my branch and the tests pass. Write the PR body: show how the call path changed, give me before and after test output, and tell me honestly how risky the merge is.

A good result uses a call-tree diff for the Summary, a failing run and a passing run under Evidence, and a door label with a one-word blast radius.

## What it requires

Very little. The skill is one instruction file with no scripts and no declared Workbench requirement. In practice you supply:

- The change itself, so the agent can pick a visual and describe what moved.
- Evidence you can really show: command output, a failing test run, or a screenshot when the change is visual.
- Optionally, the project's glossary, so the wording matches.

## What it does not authorize

`pr` writes text and nothing more. It gives no permission to commit, push, open or publish a PR, or merge one. The project's own rules govern those steps, along with branch cleanup.

## FAQs

### Does it open the pull request for me?

No. It only produces the body. Opening, pushing and merging belong to other skills and the project's rules. `journey` can open a requested PR as part of its submit step and calls `pr` for the text.

### What if I have no screenshot or test run to show?

The skill lists a screenshot for visual changes, then test results or console output, always as a before and after. It does not say what to do when you have none, so produce a small real before and after first, even a one-line command output.

### The change touches many files. Do I include every visual?

No. The skill expects you to choose, and says using all of them is unlikely. For a broad refactor a shallow file tree usually carries the point; for a small logic change a short diff does. An overloaded Summary defeats the purpose of making the PR quick to review.

### How do I decide between one-way and two-way?

Ask whether the change can be walked back after merging. Destructive actions and hard-to-reverse decisions make it a one-way door; anything cheap to roll back is two-way. Label the door, give the blast radius in one word, and use the optional description line if the label needs explaining.

## It's working when

- The body has Summary, Evidence and Merge Danger, in that order.
- The Summary uses the smallest visual (or visuals) that make the point, each beside a short line of text rather than a wall of prose.
- Each visual keeps only the files, calls and boundaries that matter to this change.
- Evidence shows a before and an after, ideally a screenshot or the exact test that now passes.
- Merge Danger names the door as one-way or two-way and gives the blast radius in one word.
- The wording matches the project's glossary, and there is no preamble.

## Where it fits in the workflow

`pr` is a supporting skill in the **Journey** stage (build each Task), outside the main flow of `carry`, `orchestrate` and `journey`. [journey](/skills/journey) calls it when a merge-request body is wanted at submit time, and [land](/skills/land), in the **Complete** stage, calls it when publishing a PR. It hands the finished body back to whichever skill is publishing, and the project's rules decide what happens next. Independent review of the result belongs to [code-review](/skills/code-review).
