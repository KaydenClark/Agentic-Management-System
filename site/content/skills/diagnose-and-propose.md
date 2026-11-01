---
name: diagnose-and-propose
summary: Tests your explanation of a known problem against evidence and recommends the simplest next step that is enough. It grants no authority to implement.
pin: 878241202bf7ec97c0952287f1633f6f0ddf1a6e
credit: original
credit_text: Original to Kayden Clark.
---

## What it does

You bring a problem you already know about, such as a test that keeps failing, a process that keeps stalling, or a fix you are about to trust. **Diagnose and Propose** answers two things: what is actually causing it, and what is the smallest next step that would be enough. The output is a recommendation, aimed at a useful decision rather than agreement, contrarianism or a bigger investigation than the decision needs.

The answer starts with a **verdict** on the specific claim you made. It is one of four: supported, partly supported, unsupported, or not enough evidence. Behind it you get the diagnosis, the best evidence for it, and the open uncertainties, then one recommended step with the main alternative and its tradeoff. If the step needs setup, the answer says how to check that it worked, and it separates what can go ahead now from what waits on your input or approval.

Three habits make the verdict trustworthy.

- **It tests your explanation instead of adopting it.** The agent separates what it observed from what it inferred and what it merely guessed, and a story that fits the symptoms is not treated as a proven cause. It weighs other credible causes, hunts for evidence that would knock down the leading one, and checks current files or behavior rather than an old summary.
- **It judges your proposed fix too.** The agent decides whether your fix addresses the cause, only a symptom, or a different goal, and then accepts, rejects or qualifies it.
- **It picks the lightest response that works.** It compares only realistic options: do nothing, change a process or setting, use a tool you already have, or build something custom. It checks what it already has before suggesting anything new, and if something is missing it names the tool or access, why it matters and the least setup required, or says none is needed. It recommends one option and explains why the simpler ones fall short. If the cause stays uncertain, expect a bounded experiment, not a confident plan.

Your goal stays fixed. If the evidence suggests the framing itself is off, it says so before recommending work that depends on it, and it does not quietly change the goal or widen the scope.

## When to use it

Reach for it when you can describe a problem and want its cause plus a next step. It is built for asking why something keeps failing, what to do next, or whether a proposed fix is right. A small question gets a short answer.

| What you have | Reach for |
| --- | --- |
| A known problem or recurring failure, and you want the cause plus the simplest sufficient next step | `diagnose-and-propose` |
| A suspicion that you are asking the wrong question, or that the idea itself is unsound | [oracle](/skills/oracle) |
| A single bug that needs a tight reproduction and a proven root cause before any repair | [diagnosing-bugs](/skills/diagnosing-bugs) |
| A worry that the project's own controls, skills or tools are the weak point | [improve-workbench](/skills/improve-workbench) |
| A plain request to do the work | The execution path for that work, not this skill |

## Example request

> Our release checks have failed intermittently three times this month, and I think the cache setting is the cause. Is that right, and what should we do about it?

The reply opens with a verdict on the cache theory, lays out the evidence for and against it, and names one recommended step. If that step needs setup, it includes a check that would show the step worked.

## What it requires

Very little. The skill file names no required Workbench (a project setup with its own records and rules), no records and no companion skills. It does need access to the relevant sources and the current behavior, so it can check facts for itself, and it needs a concrete problem or claim to test. When evidence is missing, it says so and proposes the cheapest check that would resolve it, and it states plainly what is waiting on your input or approval.

## What it does not authorize

The skill grants no authority of any kind. A diagnosis is not permission to implement it, and the skill keeps three things apart: what you intend, what you have approved, and proof that something was actually implemented. A request for diagnosis alone ends with the proposal.

If you had already approved a piece of work, the agent may continue it within that scope without asking again. That permission comes from you, not from this skill. The skill never lets the agent widen the scope or swap your goal for one it prefers.

## FAQs

### Is this the same as debugging?

No. A recurring failure can turn out to be a bug, but this skill also covers processes, settings and tooling, and it ends in a recommended decision. For one bug that needs a reproduction and a proven root cause before repair, use [diagnosing-bugs](/skills/diagnosing-bugs).

### What if the agent cannot prove the cause?

Then the verdict is not enough evidence. The answer says which evidence is missing and proposes the cheapest check that would resolve it, so you get a small experiment to run rather than a confident plan.

### Will it keep digging until it is sure?

No. It stops once the evidence supports a decision, and it does not reread sources unless it has a new question. This is the skill's own guard against an investigation that grows without end.

### Does it fix the problem for me?

Not by itself. Without prior approval, the run ends at the proposal. If you have already approved the work, it continues within that approved scope on its normal execution path. A plain request to do the work goes straight to execution and does not need this skill.

## It's working when

- The answer opens with a verdict on the specific claim you named, not a general essay.
- Observations, inferences and guesses are visibly kept apart.
- At least one alternative cause was considered, and evidence that could have disproved the leading one was sought.
- The recommendation is a single option, with a reason the simpler options were not enough.
- It tells you what can go ahead now and what is waiting on your input or approval.
- Your original goal is intact, and any reframing is explained rather than slipped in.
- A request for diagnosis alone ends at the proposal.

## Where it fits in the workflow

Diagnose and Propose is also used in the Improve stage (Learn and fix), whose main flow is [retro](/skills/retro) and [improve-workbench](/skills/improve-workbench). [author-skill](/skills/author-skill) is another skill used there. [sitrep](/skills/sitrep) points to it when you want to know why something fails, and [oracle](/skills/oracle) can hand a question over to it when a practical plan is needed, though that hand-off is optional.

Its output is a proposal. Any follow-on work is authorized by your approval, not by the skill.
