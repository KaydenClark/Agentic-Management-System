---
name: evaluate-workbench
summary: Gathers evidence on whether a Workbench's structure, installed skills and task results really work, without repairing anything or assigning a score.
pin: 878241202bf7ec97c0952287f1633f6f0ddf1a6e
credit: original
credit_text: Original to Kayden Clark.
---

## What it does

A **Workbench** is the set of controls, records, tools and skills a project installs so coding agents work in a disciplined way. A **room** is a project running an installed Workbench. `evaluate-workbench` inspects a room and reports what is true about it: whether the structure is sound, whether installed skills really load in the **host** you claim to support (the agent application, such as a coding assistant or CLI), and whether the Workbench yields better task results than the alternative.

Its core principle is that following a procedure proves nothing. A green checklist, a static score or a file in a listing doesn't show the Workbench works; the skill wants observed behavior and an independently checked end state.

It works in four moves.

1. **Bind the evaluation.** Fix the request, the target repository, the exact **candidate** (the revision under judgment), the scope and the stopping point. Read the target's controls and the assigned **Spec** and **Task**, check for uncommitted work and locks, and leave existing work alone. Then name the kind of evaluation: a focused diagnostic, a comparison against a baseline, or one scored with the **Alignment Check**, the rubric [audit-workbench](/skills/audit-workbench) owns.
2. **Check structure and capabilities.** Inventory what is installed at that revision and run the room's own static checks, noting command, revision, exit code and limits. For each claimed host, watch the skill get discovered, note which path and revision loaded, and see the action that followed. A listing, symlink or package receipt does not count, and a host you skipped stays on the report as untested.
3. **Test outcomes and benefit.** When someone says a change helps, lock the prompts, acceptance rules, conditions, grader, model, host and budget before running anything, then use bounded exercises with fresh agents. A worker's self-check is not independent grading, and an undemonstrated benefit is reported as unproven.
4. **Return the result.** Report scope, exact identities, what each check covered and where the raw evidence lives, with separate limits for static, activation and behavioral conclusions. Add failures, cost, uncertainty and stable finding identities with next owners, then read the saved report back to confirm its links.

## When to use it

Use it to ask whether a room is healthy, whether a skill truly activates in a given host, or whether a change beats no instructions, generic instructions or the previous version, and to collect a candidate's runs before an Alignment score is assigned.

| What you have | Reach for |
| --- | --- |
| Evidence already gathered and a score, fitness claim or audit to settle | [audit-workbench](/skills/audit-workbench) |
| One observed gap in a skill or control that needs a measured fix | [improve-workbench](/skills/improve-workbench) |
| A broader or comparative claim that a single fix loop cannot support | `evaluate-workbench` |
| No Workbench yet | [setup-workbench](/skills/setup-workbench) first |

## Example request

> Our new journey skill revision is on a branch. Check that the room still validates, confirm the skill actually loads in the agent host we ship for, and run a small comparison against the previous revision so we know whether it helped or hurt.

The skill pins that branch as the candidate, runs the existing checks, watches a real load in the named host, freezes a task set, and reports regression, benefit or an inconclusive result with evidence.

## What it requires

- **A Workbench from the setup skill.** If the manifest or spec tool is missing, it stops and points you to [setup-workbench](/skills/setup-workbench); it never builds Workbench records by hand.
- **Checks and runners that already exist.** A missing tool is logged as a gap, with a manual check where one can settle the point. It won't invent a runner to look thorough.
- **audit-workbench, for scoring only.** Without it you get the evidence and a note that scoring is pending, never a score from memory.
- **Spending authority.** Paid trial campaigns need authority already in place covering projects, models, trial counts, an attempt cap and a spending limit. Without it, paid work waits while static checks continue.
- **Disposable copies for new-feature comparisons.** Each trial runs in a throwaway local copy with no remote, and evidence is kept before cleanup. The Alignment Check sets the trial count, pairing and fixed conditions.

## What it does not authorize

Evaluating a Workbench never grants permission to change it.

- **No fixes or lifecycle changes.** Repairs, installs, deployments, retirements, automation edits and paid campaigns each need separate authority. So do ID allocation, seed repairs, Wiki moves, adoption, upgrades and rollbacks, which belong to the room's own Runbook operations. The skill notes what is needed and stops.
- **No rule bending.** If the registry and observed behavior disagree, it records the conflict and leaves both the registry and the check as they were. It also won't alter security, provider settings or test rules to rescue the evaluation environment.
- **No hidden writes.** Diagnosis sticks to read-only listing and viewing, with no claiming, closing or ID allocation unless the assignment includes them. It never finds commands by trying mutating ones.
- **No borrowed approvals.** Passing the Wiki validator does not authorize moving, retyping or deleting Wiki content, and a successful lifecycle classifier run does not choose a migration. A qualifying result gives no authority over main, distribution or adoption, and changed bytes need fresh proof.

## FAQs

### Does it fix the problems it finds?

No. It reports findings with owners and explicit retests. Repairs belong to the target's own workflow, or to [improve-workbench](/skills/improve-workbench) when you want a measured fix.

### Why does it say a skill isn't active just because it's installed?

Installed and activated are different claims, and a listing, symlink or receipt shows only that files exist. The skill wants to see the host discover the skill, load a specific path and revision, and act. A host you can't test is listed as untested, not passed.

### What if a check or the provider fails partway?

It saves the real failing output before retrying. An unreachable repository, provider outage or owner gate means missing evidence, not an idle result. Where manual inspection can settle the point, it does that; otherwise the report names the claims left weak. Incomplete proof is never marked accepted. The report goes in the target's own assessment format, or chat if none exists.

### Can it give me an Alignment score, or does a guardrail score count?

Only audit-workbench scores, and an older static, guardrail or HFI score never substitutes for its Alignment Score. A static evaluator only tests control coverage, and a guardrail score is a rough diagnostic, not proof of repeated outcomes. Read the Alignment Check first so your evidence maps to its check IDs.

### How does it decide a change helped?

It compares runs against runs under frozen conditions. If the baseline passed a behavior and the candidate then fails it, that is a regression. A benefit must clear a margin set in advance, and landing inside it is inconclusive, not equivalent. Workers never see grader answers, and an unknown or unparseable grade counts as missing evidence.

### The tests could not run, or a repaired revision came back. What carries over?

Unrun tests are not a pass: static inspection is labeled as such, and behavioral claims stay unverified. A repaired revision gets no inherited approval; it is tested on the original case plus affected regressions with the rubric and baseline unchanged, and a fresh case decides because the tuning case is spent.

## It's working when

- The report names the exact candidate, scope and host or configuration assessed, not just a project name.
- Each claim in scope maps to a check, with command, directory, revision, exit code and limits recorded.
- Activation claims cite what the host actually loaded, and untested hosts are listed as untested.
- Failures, incomplete trials, cost and uncertainty appear alongside passes.
- A benefit claim names its baseline, margin and a fresh deciding case, or is labeled unproven.
- Findings carry stable identities, owners and retests, and nothing in the target was changed.
- The saved report was read back and its evidence links checked.

## Where it fits in the workflow

Stage: **Improve** (learn and fix). It usually follows [setup-workbench](/skills/setup-workbench), which creates the Workbench and points outcome comparisons here. [improve-workbench](/skills/improve-workbench) hands broader or comparative claims here. Its evidence goes to [audit-workbench](/skills/audit-workbench) for scoring and back to the owners of any findings.
