---
name: prototype
summary: Answer one concrete design or behavior question with a small reversible artifact, record the verdict, and clean the artifact up.
pin: 878241202bf7ec97c0952287f1633f6f0ddf1a6e
credit: adapted
credit_text: Adapted from [Matt Pocock's skills collection](https://github.com/mattpocock/skills), MIT License.
credit_license: MIT
---

## What it does

`prototype` turns a nagging "I can't tell which way this should work" into a small experiment you can run and look at. Instead of debating a design in prose, the agent builds the cheapest thing that makes the uncertainty visible, and the question gets an answer. The artifact is **reversible**: built to be undone, so nothing about it has to stick around.

The skill is short and works in three moves.

1. **Frame the experiment before building anything.** The agent states three things up front: the **question** (the one thing you need to know), the **observable verdict** (what you will see that settles it), and the **disposal boundary** (what is throwaway).
2. **Pick the smallest artifact that shows the uncertainty.** The skill names two shapes. For questions about state and behavior, build a runnable logic loop you can step through. For questions about interaction or appearance, build a few contrasting UI variants to compare. Either way, the artifact follows the project's local conventions and exposes the relevant state, so you can watch what is happening instead of guessing.
3. **Keep it isolated and temporary, then close the loop.** The prototype is clearly marked as temporary, kept apart from real code, and easy to run. Once the question is answered, the agent writes down the decision and any supporting evidence where the question was asked: a ticket, a pull request, or a decision note. If there is no such place, it reports in chat. Then the throwaway work is removed, unless that record explicitly needs it as proof.

The artifact is a means to a decision, and the decision is what survives.

## When to use it

Reach for it when you have a behavior or design question that a test-like experiment could settle faster than more discussion. For example, how a state machine responds to a sequence of events, or which of a few layouts feels right. The question should come with something observable that would settle it.

| What you have | Reach for |
|---|---|
| A concrete behavior or design question a small runnable artifact could answer | `prototype` |
| A plan or idea to stress-test through questions until you agree on it | [grilling](/skills/grilling) |
| An idea or claim you want examined for whether it is sound and the right question | [oracle](/skills/oracle) |
| A bug whose cause you need to establish | [diagnosing-bugs](/skills/diagnosing-bugs) |
| One behavior you want to build through a red-green-refactor loop | [tdd](/skills/tdd) |

## Example request

> We can't agree on how the retry button should behave when a request fails twice. Prototype the retry states as a small runnable loop I can step through, plus two or three variants of the button, so we can pick one. Throw it away when we've decided.

The agent restates the question and the verdict you will judge by, builds the loop and the variants in an isolated, labelled spot, and shows you how to run them. After you choose, it records the chosen behavior and the evidence where the question came from, then deletes the experiment.

## What it requires

Very little. The skill names no Workbench, no companion skills and no special tools. It needs:

- a question you can state, with a verdict you can observe;
- somewhere to build the artifact that is separate from real code and fits local conventions;
- a record to write the outcome into, or the chat if there is none.

## What it does not authorize

The skill covers building a temporary artifact and recording the result. Nothing in it grants shipping, merging, publishing or review of anything.

- **Removal is the default.** Keeping the artifact needs an explicit reason: the record has to want it as proof.
- **A working prototype is not the feature.** The skill describes the artifact as isolated and temporary. Moving any of it into real code is separate work.
- **Running it is not a preference.** When the choice depends on the owner's taste, [wayfinder](/skills/wayfinder) leaves that decision pending until the owner reacts. A prototype that runs cleanly cannot supply it.

## FAQs

### What if the prototype starts growing into the real feature?

Go back to the disposal boundary. If it was written down at the start, it tells you what was meant to be thrown away. Record the verdict and remove the artifact rather than extending it, then plan the real work separately.

### What if I can't say what would settle the question?

Then the experiment has no verdict, and you would end up with a demo rather than an answer. Narrow the question until you can name what you would observe. If the idea itself is murky, a questioning skill such as [grilling](/skills/grilling) may be a better first step.

### Where does the answer go?

Into the ticket, pull request or decision write-up where the question came from, along with the evidence. If none exists, the agent reports it in chat. Usually the artifact itself is then deleted; the exception is a record that explicitly needs it as proof.

## It's working when

- The question, the observable verdict and the disposal boundary are written down before any code appears.
- The artifact is the smallest one that makes the uncertainty visible, and its relevant state is on display.
- It is isolated, clearly marked temporary, and easy to run.
- The decision and its evidence land in the record that asked, or in chat if there is none.
- The throwaway work is gone afterward, or kept only because the record needs it as proof.

## Where it fits in the workflow

`prototype` sits in the Align stage ("Shared concept") as one of the supporting skills. Align's main flow is [grilling](/skills/grilling) and then [readback](/skills/readback), which get you and the agent to the same understanding. `prototype` covers the cases where that understanding depends on seeing a behavior or interaction rather than discussing it.

Two skills reach for it directly. [wayfinder](/skills/wayfinder) uses it for uncertain behavior or design that needs a test, records the prototype's path and result, and moves on. [plan](/skills/plan) turns to it when evidence is too thin to plan responsibly, asking for a prototype with a named question and result instead of building on unknowns. In both cases the result goes back into the record that asked.
