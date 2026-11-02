---
name: oracle
summary: Have an agent judge your idea, claim or question as a skeptical domain expert, with evidence for its verdict and a plain statement of where you are wrong.
pin: 878241202bf7ec97c0952287f1633f6f0ddf1a6e
credit: original
credit_text: Original to Kayden Clark.
---

## What it does

Oracle turns an agent into a skeptical expert for a single question. You bring an idea, a claim or a question, and the agent returns a **verdict** it can defend, even when that means telling you that you are wrong. It starts from the view that most ideas are mostly right, so it hunts for the one part that is not. Agreement has to be earned with evidence just as much as disagreement does.

A run moves from your question, to the evidence, to a verdict.

**Reading the question.** The agent recovers your goal, the problem you noticed, your limits and the choices already made, and keeps apart the question, its hidden assumptions and the proposed answer. A goal it had to guess is labeled as a guess. It asks you something only when two readings would lead to different verdicts; otherwise it states its assumptions and goes on. It also tests the question's silent premises: is the problem real, is the cause what you think, is progress measured sensibly, and are there choices nobody listed?

**Naming the likely errors.** Before judging, the agent lists the one to three likeliest ways you could be wrong, ranked by probability and cost, including slips from other agents and from its own reasoning. A model reviewing itself is not an independent check.

**Investigating.** The agent states the strongest form of your claim and separates facts from inferences, guesses and values. The facts that decide the outcome get checked against primary evidence or real behavior, and changing facts against a current, cited source. It tests each suspected error, tries a credible alternative and hunts for a counterexample. It asks whether the idea fixes the problem, only moves it, or improves a stand-in number, and it counts doing nothing as an option.

**Stopping rule.** The agent digs further only where more doubt could change the verdict. It stops at a bounded judgment or at a named missing piece.

The answer opens with one of four verdict labels:

- **Supported**
- **Partly supported**
- **Unsupported**
- **Undecidable with current evidence**

Each issue follows with its evidence and the agent's confidence, with factual errors kept apart from tradeoffs of taste. When an idea fails, the agent names the false premise or missing link. When your question misleads, it offers a **better question** aimed at the same goal. It closes with the **smallest next step**, an action or test with a visible sign it worked.

## When to use it

Reach for Oracle when you want to be told where you are wrong, not helped to build the thing: a design claim you are about to commit to, a diagnosis you doubt, or a question that may point at the wrong target. An owner or an agent can call it. It gives a bounded judgment, though it may ask a clarifying question first.

| What you have | Reach for |
| --- | --- |
| A known problem needing a cause, or a specific fix you want proven right or wrong | [diagnose-and-propose](/skills/diagnose-and-propose) |
| Doubt about the question or idea itself | Oracle |
| A plan you want questioned until you and the agent share one understanding | [grilling](/skills/grilling) |
| An idea you want tested against its strongest opposing case | [brainstorm](/skills/brainstorm) |
| A finding you want saved with its source | [jot](/skills/jot) |

Grilling and brainstorm are interviews that run with you. Oracle is a judgment handed back.

## Example request

> I'm about to put a cache in front of our search endpoint because it feels slow. Before I do, ask oracle whether caching is the right fix or whether I'm asking the wrong question.

The agent would recover the goal (faster search for users), list the likeliest ways the plan is wrong, check real timings instead of guessing, and return a verdict with a small test to run first.

## What it requires

Very little. The verdict is only as good as the primary evidence, observed behavior and current sources the agent can reach. Oracle does not need a **Workbench**, the set of records and rules many other skills here depend on. Its optional hand-off to [jot](/skills/jot) does, so set one up first if you want a finding saved.

## What it does not authorize

The skill states two limits. Running it gives no right to implement anything or to edit project records, so the agent answers where you asked and stops at the verdict. Separately approved work can continue within its own scope, but the Oracle run adds nothing to it. And it leaves your open choices open.

A consequence for you, not a statement from the skill: a supported verdict judges evidence. Do not read it as approval to merge, publish or deploy, or as a substitute for a review your project requires.

## FAQs

### Will it just disagree with me to look useful?

It should not. When the evidence backs you, the correct output is a supported verdict with that evidence shown. Disagreement with nothing behind it breaks the skill as badly as empty agreement.

### What if the agent cannot reach the evidence it needs?

Then the honest verdict is undecidable with current evidence. The agent should say what it could not reach, name the smallest check that would settle the question and say what each result would mean. Missing evidence is not proof of absence, so a confident verdict that ignores the gap means the run went wrong.

### How deep does it go?

Only as deep as the verdict needs. A run that sprawls into broad research unrelated to the verdict has broken the stopping rule.

### Does it reopen decisions I have already made?

It does not reopen your stated preferences. A settled decision that the evidence contradicts is different: the agent flags it instead of silently accepting it. You remain free to keep your decision after reading the flag.

### My problem is real and I need to fix it. Should I use Oracle?

Usually not first. If the problem is known and you need its cause and a sufficient next step, use [diagnose-and-propose](/skills/diagnose-and-propose). That skill points back to Oracle for the other case, where the question or idea itself is in doubt.

## It's working when

- The answer opens with one of the four verdict labels, tied to the specific claim you named.
- Inferred goals and assumptions are labeled, not stated as fact.
- Each issue comes with its evidence and a stated level of confidence.
- Facts, tradeoffs of taste and guesses are kept apart.
- Claims that decide the verdict rest on primary evidence or observed behavior, and changing outside facts carry sources.
- The agent says what it could not reach instead of treating silence as proof.
- A failed idea has its false premise or missing link named.
- The next step is small and has a visible sign of success.
- Oracle itself changed no project records, and your open choices are still open.

## Where it fits in the workflow

Oracle belongs to the Align stage, where you and the agent build a shared concept of what to make before any planning. It is a supporting skill there, beside the main flow of [grilling](/skills/grilling) and [readback](/skills/readback), for when a claim needs an outside check before the concept settles. Align hands its result to the Prepare stage, where [map](/skills/map) describes the destination and [plan](/skills/plan) breaks it into Tasks.

Oracle is not a required step. It can hand off to [diagnose-and-propose](/skills/diagnose-and-propose) for a practical plan, or to [jot](/skills/jot) to save a finding with its source. Other Align skills close by are [brainstorm](/skills/brainstorm) and [research](/skills/research).
