---
name: diagnosing-bugs
summary: Finds why something is broken by building a small reliable reproduction and proving the root cause, then repairs only if you asked for a fix.
pin: 878241202bf7ec97c0952287f1633f6f0ddf1a6e
credit: adapted
credit_text: Adapted from [Matt Pocock's skills](https://github.com/mattpocock/skills), MIT License.
credit_license: MIT
---

## What it does

Bad debugging often starts with a guess and a patch. This skill reverses that order. The agent proves what is wrong before it changes anything, and it names the assumption that turned out to be false.

The work follows one shape:

1. **State the gap.** The agent defines the **observed behavior** (what happens now) and the **expected behavior** (what should happen).
2. **Build a reproduction.** A **reproduction** is the smallest run that fails reliably. A check that only fails sometimes cannot confirm or refute anything.
3. **Make the loop go red.** Run the reproduction and watch it fail. If it never fails, you do not have the bug yet.
4. **Reduce it.** Strip the reproduction down to the inputs that actually cause the failure.
5. **Test each hypothesis.** Every suspected cause is checked against evidence, not accepted because it sounds plausible.
6. **Separate cause from symptoms.** The report names the **root cause**, meaning the broken assumption underneath the failure, and not just the place where the error showed up.

Diagnosis is the default outcome. If you also ask for a repair, the order changes: a **regression test** (a test that fails on the bug and guards against its return) comes first, then the least invasive change that fixes it.

The agent writes up the reproduction, the root cause and how it was verified. The write-up goes on the bug's issue or pull request when there is one, and in chat when there is not.

## When to use it

Reach for it when behavior is wrong and the cause is unknown: a failure you do not understand, or a result that contradicts what the code seems to say. You want evidence before anyone edits source.

Several neighbours are close, so pick by what you already have. A **Workbench** is a project set up with this catalog's records and skills, and a **Task** is one assigned unit of work in it.

| What you have | Reach for |
| --- | --- |
| Wrong behavior and an unknown cause | `diagnosing-bugs` |
| A behavior to build or change that a test can express | [tdd](/skills/tdd) |
| A recurring failure, where you want a recommended next step | [diagnose-and-propose](/skills/diagnose-and-propose) |
| A raw issue or external pull request to categorize and label | [triage](/skills/triage) |
| An unsettled interface | [codebase-design](/skills/codebase-design) |
| A problem in the harness (the controls, skills and tools around the agent), not the product | [improve-workbench](/skills/improve-workbench) |

Triage is a step you invoke yourself to sort reports, and it includes a quick check that the reported bug reproduces. This skill is where the reproduction is reduced and the cause is proven.

[Journey](/skills/journey), the skill that takes a Task through Implement, Check, QA and Submit, names `diagnosing-bugs` for an unknown cause during Implement.

## Example request

> The CSV export drops the last row whenever the file has more than 1,000 lines. Find out why. Don't change anything yet, just show me how to reproduce it and what the actual cause is.

Because this asks only for the cause, the run ends at the report. Adding "and fix it" would bring in the regression test and the smallest change.

## What it requires

Very little. The skill is one short instruction file with no references, scripts or agents folder. It needs access to the code and a way to run it, so a reproduction can be executed and seen failing. Telling it what you expected makes the first step quicker, though the agent defines expected behavior itself.

The skill does not require a Workbench on its own, but skills that call it, such as Journey, do.

## What it does not authorize

Diagnosis does not authorize repair. A repair needs an explicit request, and then the skill's order applies: regression test first, smallest change second. The routing guide in [ask-workbench](/skills/ask-workbench) says the same.

The skill grants nothing beyond investigating and, when asked, repairing. Accepting work and landing it belong to other steps.

## FAQs

### Will it fix the bug for me?

Only if you ask. By default you get a reproduction, a root cause and the evidence for it. Ask for a repair and it adds a regression test first, then makes the least invasive change.

### What if I cannot get it to fail reliably?

The skill asks for a reproduction that fails on demand and goes red. Without one, the cause is not yet proven. Beyond that the skill gives no special handling for intermittent failures, so treat a report built on a guess as unconfirmed.

### How is a root cause different from a symptom?

A symptom is what you see: an exception, a wrong number, a missing row. The root cause is the broken assumption underneath it. The report is meant to name that assumption.

### Why add a test before the repair?

The test pins the failure down first, so the fix is judged against it. It also keeps guarding against the bug after the repair.

## It's working when

- The run states observed and expected behavior side by side.
- A reproduction exists, was run, and was seen to fail before any source changed.
- The reproduction was reduced to the inputs that matter.
- Each suspected cause was tested with evidence.
- The report names the broken assumption, not only where the error appeared.
- With no repair request, no source files changed.
- With a repair request, a regression test fails first and passes after a small, targeted change.

## Where it fits in the workflow

It sits in the Journey stage (Build each Task) as a supporting skill, not a main step. The main flow there is [carry](/skills/carry), [orchestrate](/skills/orchestrate) and [journey](/skills/journey). Journey names this skill for an unknown cause and [tdd](/skills/tdd) for building behavior at a testable seam, as separate options for the Implement step. The skill's own repair order, test first and then a small change, matches the red-green habit in tdd.

Other stages reach it too. [ask-workbench](/skills/ask-workbench) in Route points to it for broken behavior. [land](/skills/land) in Complete names it when a rejected candidate (the finished work proposed for landing) has wrong product logic and the person is authorized to implement. [improve-workbench](/skills/improve-workbench) in Improve points to it when the product, not the harness, is at fault.
