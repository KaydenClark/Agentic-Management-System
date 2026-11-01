---
name: tdd
summary: Builds one behavior at a time: a test that fails for the expected reason, the least code to pass it, then cleanup while the test stays green.
pin: 878241202bf7ec97c0952287f1633f6f0ddf1a6e
credit: adapted
credit_text: Adapted from [Matt Pocock's skills](https://github.com/mattpocock/skills), MIT License.
credit_license: MIT
---

## What it does

TDD (test-driven development) puts the test before the code. This skill is a short version of that habit. It takes **one behavior** through a **red-green-refactor loop**:

1. **Red.** Write the smallest focused test for the behavior and run it. It has to fail, and for the reason you expected.
2. **Green.** Write only enough code to make that test pass.
3. **Refactor.** Clean up while the test is passing. Keeping it green means the behavior it checks stays unchanged, which is why the project's required checks come next.

Before the first test, you name the behavior and its **public seam**: the stable place where the behavior can be observed from outside, such as a function others call, a command's output or an API response. Tests are kept **behavioral** (they check what the code does) and **deterministic** (same result every run).

Some seams cannot be tested. The skill does not let you skip the proof quietly. You explain why, then use the strongest alternative you can repeat. For delivery work, meaning work that ends in a PR or a recorded handoff, you note the meaningful proof in the PR description or the task record (the written record of the assigned Task, defined below).

## When to use it

Reach for it when you are adding or changing behavior and a test at a public seam can express it. It handles one behavior per loop, so a bigger change is a series of loops.

| What you have | Reach for |
|---|---|
| A behavior to build or change, with a testable seam | tdd |
| A bug with an unknown cause | [diagnosing-bugs](/skills/diagnosing-bugs) |
| An unsettled module interface or seam to design | [codebase-design](/skills/codebase-design) |
| A whole assigned Task to take from start to submission | [journey](/skills/journey) |
| A PR body to write after the work is done | [pr](/skills/pr) |

Diagnosing-bugs overlaps at one point: if you ask it to repair a bug, it adds a regression test first. The starting question differs. TDD starts from a behavior you want. Diagnosing-bugs starts from a failure you do not yet understand.

## Example request

> The export endpoint should return a CSV with only the header row when a user has no records. Use tdd: write the failing test at the endpoint first, make it pass, then tidy up and run the project's checks.

## What it requires

- A behavior you can state and a public seam where it can be observed.
- A way to run tests, so the red and green results are real runs.
- The project's own required checks. The skill defers to them and does not define them.
- For delivery work, a place to record proof: the PR description or the task record.

The skill is one short file with no helper files. Inside a Workbench (the project folder that holds Specs and Tasks), a **Task** is one bounded unit of assigned work, and a **Spec** is the agreed description of what that work should achieve. TDD is something a Task run reaches for; see the last section.

## What it does not authorize

The skill describes a test-and-verify loop and nothing more. It does not mention merging, publishing, accepting a Spec or Human QA (a person's own hands-on check of the result), and it does not grant any of them. Those still come from the owning Task and the Workbench's rules. [journey](/skills/journey), for example, treats whether a change can merge and whether the Task is complete as separate questions.

## FAQs

### What if my first test passes immediately?

The skill wants a test that fails for the expected reason before any implementation. A test that already passes has not shown the new behavior is missing, so tighten it until it fails, then write the code.

### What if the test fails, but for the wrong reason?

That is not yet the failure the loop calls for. A broken setup or a typo, for example, is a different failure from the behavior being absent. Fix the test or setup first, so the failure you see is the one you expected.

### What if the thing I need to change has no testable seam?

Say so and explain why. Then use the strongest check you can repeat, and for delivery work record that proof in the PR description or task record.

### Does a passing new test mean I am done?

No. After the loop, run the checks the owning project requires. The new test covers one behavior only.

## It's working when

- You can name the behavior and its public seam before the first test exists.
- The new test was run and seen failing, for the reason you expected, before the implementation.
- The implementation added only what that test needed.
- Refactoring happened while the test passed, and it still passes.
- Tests check observable behavior and give the same result on every run.
- The project's required checks were run after the loop.
- Any untestable seam comes with a stated reason and a repeatable alternative.

## Where it fits in the workflow

TDD is a supporting skill in the **Journey** stage (Build each Task). The main flow there is [carry](/skills/carry), [orchestrate](/skills/orchestrate) and [journey](/skills/journey). Journey's Implement step uses TDD when an executable seam is useful, and points to [diagnosing-bugs](/skills/diagnosing-bugs) for unknown causes and [codebase-design](/skills/codebase-design) for unsettled interfaces.

Earlier, [codebase-design](/skills/codebase-design) names TDD for authorized execution, and [plan](/skills/plan) writes each Task's proof as a check at a public seam, the way TDD drives behavior. Afterward, [pr](/skills/pr) can carry the proof into a PR body, and [code-review](/skills/code-review) in the Judge stage reviews the finished work.
