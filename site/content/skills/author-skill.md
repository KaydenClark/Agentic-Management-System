---
name: author-skill
summary: Turns an agreed workflow into a working skill, or repairs and merges existing ones, with a tested full draft, a separate pruner and a retest.
pin: 878241202bf7ec97c0952287f1633f6f0ddf1a6e
credit: adapted
credit_text: Adapted from Kayden Clark's writing-great-skills guidance, which derives from Matt Pocock's MIT-licensed [skills](https://github.com/mattpocock/skills), and from the evaluation guidance in [Anthropic's skill-creator](https://github.com/anthropics/skills/tree/ca45fc496a3436251f191354091d557da31c15b5/skills/skill-creator) (Apache-2.0), with Kayden Clark's own authoring process, plain-language guidance and owner decisions.
credit_license: MIT and Apache-2.0
---

## What it does

`author-skill` is the procedure an agent follows when it writes or revises a **skill**: a folder with a `SKILL.md` file that teaches an agent a repeatable job. It puts the method into the instructions themselves, so you are not left supplying the missing steps. A good run means a dependable process, not identical output.

The work runs in four passes.

1. **Recover the job.** The agent reads the conversation, sources, review comments (with replies) and any existing skill, and recovers who the skill is for, the problem, what a good result looks like, the vocabulary, the scope and where to stop. The newest correction wins, untouched decisions stay, and named conflicts are reported while unaffected work continues. When revising, every useful responsibility in the old skill ends up **retained**, **repaired**, **moved** to an owner that can still be reached, or **explicitly retired**. The agent asks only about gaps that would change the process.
2. **Develop the method.** The agent walks one concrete request from inputs to result. At each consequential decision it settles the evidence, the choice, the next action and what happens on failure. Vague verbs such as plan, coordinate or reconcile become operating instructions naming real artifacts, owners and handoffs. It also checks neighbouring skills so no work is duplicated or left unowned.
3. **Write the full procedure.** Shared steps go in `SKILL.md`; large conditional methods go in supporting files, each with a stated condition for reading it. The agent says where output goes and how to tell it is finished, using formats and commands it has verified. It also decides the **invocation policy**: should the agent pick the skill on its own, or only when someone asks? The catalog requires a description, and deleting one is not a portable way to hide a skill, so the agent checks real host behavior. The description names the job and its distinct triggers, and attribution is kept.
4. **Test, prune, test again.** The agent exercises the whole draft and keeps the draft, cases and results as the **baseline**. A separate fresh-context subagent then prunes it using the writing-for-agents skill. The author never prunes its own draft. If a retest shows meaning lost in compression, the author returns the failing case to the pruner instead of patching it. If the author repairs a real gap in the method, that is a new baseline and goes back to the pruner. The behavior a passage protects settles any dispute, not brevity. This repeats until the required behavior survives.

Test cases include a normal request, one with incomplete or conflicting inputs, a neighbouring request, the exception most likely to be lost in compression, and near misses that check the description does not trigger the wrong method. If independent trials claim added value, they include a no-skill run.

Before handing over, the agent checks frontmatter, links, names, dependencies and size budgets.

## When to use it

Use it when you have an agreed workflow to teach as a skill, a skill that works poorly, or several skills to merge without losing any distinct job. Investigating whether a capability exists at all needs your request; ordinary source reading does not.

| What you have | Reach for |
|---|---|
| An agreed workflow to turn into a skill, a weak skill to repair, or skills to consolidate | `author-skill` (this page) |
| Agent-facing prose that needs tightening | [writing-for-agents](/skills/writing-for-agents) |
| One agent job in your project's **Workbench** (its records and controls for agent work) that keeps going wrong and needs one measured fix | [improve-workbench](/skills/improve-workbench) |
| A question of whether a Workbench's controls and evidence agree | [audit-workbench](/skills/audit-workbench) |
| A recurring failure with an unknown cause | [diagnose-and-propose](/skills/diagnose-and-propose) |

## Example request

> We agreed how to triage flaky tests: reproduce, quarantine, name an owner, then re-enable. Turn that into a skill. There's already a vague `flaky-tests` skill with two review comments on it, so repair that one instead of starting over. You may use a separate subagent to prune it and run fresh-context trials.

The agent would read the old skill and comments, walk a real flaky test through the steps, test the full draft, have a pruning subagent shorten it, and retest. Without that permission, it would deliver the full draft and report pruning as incomplete.

## What it requires

- **A source of the job.** The conversation, supplied sources, review comments or an existing skill. Where these are thin, the agent derives a procedure and labels consequential choices it could not support.
- **The writing-for-agents skill and permission to delegate.** Pruning must be done by a separate subagent, and delegation needs authorization in your assignment.
- **Test material.** Fresh-context trials happen only when authorized; otherwise the agent runs labeled self-walkthroughs.
- **The real project's formats and tools.** The agent verifies them before teaching them. A skill for a Workbench may need its records, but `author-skill` itself does not require a Workbench.

## What it does not authorize

- **Delegation or extra agents.** Authoring never grants permission to launch them.
- **Rewriting other skills.** Needed changes elsewhere are reported, not made, and approved neighbours are preserved.
- **Publishing or installing.** The agent states whether the result is local, published or installed, and stops at the endpoint you authorized.
- **Claims of proof.** A format check shows neither behavior nor **host activation**, meaning whether the agent runtime really loads and selects the skill. A self-walkthrough cannot establish reliability, and a passing trial cannot promise you will never need to correct the skill again.

## FAQs

### Can the same agent write and prune the skill?

No. A separate pruner in a fresh context receives the draft, requirements, cases and results. A role switch inside one conversation does not count. With no subagent available, the agent delivers the full draft and says pruning is not done.

### Does a shorter skill mean the job is finished?

No. The pruned version must pass the same cases as the baseline, including the reference files a run actually reaches. Hiding required text behind a link saves nothing if every run must read it.

### What if my description of the method is only a label, like "reconcile the records"?

The skill treats a bare label as a gap. The agent derives a procedure from your sources, using real artifacts and owners, and reports a missing mechanism instead of inventing a command. If both full and pruned versions miss a requirement, equal failure is not preservation, so the full method is repaired first.

## It's working when

- The job, audience and stopping point are recovered from your sources, and questions asked would change the process.
- Every useful responsibility in an old skill is retained, repaired, moved or retired.
- The draft names real artifacts, owners and handoffs, with failure paths, instead of bare verbs.
- Invocation policy and the description are deliberate, attribution is kept, and near misses were tested.
- A full-draft baseline with cases and results exists before any pruning.
- A different subagent in a fresh context does the pruning, and regressions go back to it with the failing case.
- The final report separates self-review from independent trials, lists what is untested, and says whether the skill is local, published or installed.

## Where it fits in the workflow

`author-skill` is a supporting skill in the Improve stage (Learn and fix). The main flow there is [improve-workbench](/skills/improve-workbench) and retro; the chart lists this skill beside [audit-workbench](/skills/audit-workbench), [diagnose-and-propose](/skills/diagnose-and-propose) and [writing-for-agents](/skills/writing-for-agents). The skill does not name its callers, but a typical trigger is a finding from an improvement loop or audit that points at a weak skill. It uses writing-for-agents through the separate pruner, then hands back the skill, material changes, before-and-after validation and remaining limits. Review, landing and publishing stay with whoever is authorized.
