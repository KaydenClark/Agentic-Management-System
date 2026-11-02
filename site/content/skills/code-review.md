---
name: code-review
summary: Reviews a branch, PR or working changes on two axes, coding standards and the accepted request, reporting each separately and fixing nothing.
pin: 878241202bf7ec97c0952287f1633f6f0ddf1a6e
credit: adapted
credit_text: Adapted from [Matt Pocock's code-review skill](https://github.com/mattpocock/skills/tree/a496f5513d4a4cf889bc48e189e579f4b0bdf6aa/skills/engineering/code-review), MIT License, keeping Kayden Clark's separate Standards and Spec reports and adding pinned review targets, source recovery from Workbench records and honest handling of unavailable review. Smell baseline after Martin Fowler's Refactoring.
credit_license: MIT
---

## What it does

Code can follow every house convention and still build the wrong thing, or deliver exactly what was asked while ignoring how the repo writes code. So this skill answers two separate questions with two independent reviews:

- **Standards** asks whether the change conforms to the coding rules the repository documents.
- **Spec** asks whether the change faithfully implements the accepted request: the **Spec** (the written destination for a body of work) and the **Task** (one assigned slice of it), including corrections and acceptance criteria.

Each review goes to its own **fresh-context subagent**, a helper with no memory of your session, so neither inherits the other's assumptions. Both see the same evidence and run in parallel when delegation is available and authorized.

The skill works in a fixed order:

1. **Pin the target.** It resolves the base and the candidate to commit SHAs, then records the diff and commit list between them. For a PR with no stated base, it recovers the real base from PR metadata and asks you only if the comparison is still ambiguous. It stops if a ref is invalid or the diff is empty.
2. **Find the spec source.** It reads the Spec, Task or accepted request you supplied, or digs them out of the PR, its commits and the task board of your **Workbench** (the project structure that holds Specs, Tasks and their tooling). When sources disagree, it names the consequential conflict instead of quietly picking a side. If acceptance can't be established, the Spec review is skipped, Spec is reported as uncovered, and Standards still runs.
3. **Find the standards sources.** It collects every repo file that documents how code should be written.
4. **Run the two reviews.** Each subagent gets its own brief, described below.
5. **Aggregate.** Reports appear under separate `## Standards` and `## Spec` headings, never merged or re-ranked across axes.

### What each reviewer looks for

The **Standards** reviewer lists every breach of a documented repo rule, citing the file and the rule. It also checks the diff against a built-in smell baseline, naming any smell it finds and quoting the hunk. It keeps hard violations apart from heuristic judgements.

The **Spec** reviewer hunts for requirements that are missing or only partly done, behaviour nobody asked for (scope creep), and requirements that look implemented wrongly. Each finding quotes the request line behind it, because a Spec finding you can't trace to the request is just an opinion.

### The smell baseline

Standards always carries a fixed checklist of twelve code smells from Martin Fowler's *Refactoring*, used even when the repo has no standards file: Mysterious Name, Duplicated Code, Feature Envy, Data Clumps, Primitive Obsession, Repeated Switches, Shotgun Surgery, Divergent Change, Speculative Generality, Message Chains, Middle Man and Refused Bequest. Each pairs a definition with a usual remedy. Duplicated Code suggests extracting the shared shape, and Middle Man suggests cutting the pass-through and calling the real target.

Two rules keep this from becoming noise. Smells are judgement calls, worded as possibilities ("possible Feature Envy"), never hard violations. And documented repo standards win: a smell is dropped when the repo endorses the pattern, and anything your tooling already enforces is skipped.

For **workspace reviews** of uncommitted changes, the skill snapshots the selected tracked and untracked files with a manifest and hashes, says what it included and left out, and never stages, commits or resets your files to get a clean target.

## When to use it

Reach for it when you have a branch, a PR, workspace changes or a range since a fixed point and want an independent read before anything lands. For a PR you can leave out the fixed point; the skill derives it and tells you what it chose.

| What you have | Reach for |
|---|---|
| A finished candidate that needs an independent two-axis review | `code-review` |
| A quick self-check of your own Task diff before handing back | [journey](/skills/journey), which includes a scoped self-review that is not independent review |
| Review findings you now want fixed | [journey](/skills/journey), as a new run on the corrective work |
| A reviewed candidate ready to publish, merge and clean up | [land](/skills/land) |
| An unclear next step in the workflow | [ask-workbench](/skills/ask-workbench) |

## Example request

> Review the changes on this branch against main. Check them against our coding standards and against Task TK-0042, and give me the two reports separately.

The skill records both SHAs in the report, then returns a Standards report and a Spec report with a closing tally of findings and the worst issue on each side.

## What it requires

- **A Workbench**, created by the [setup-workbench](/skills/setup-workbench) skill. The skill first checks for the Workbench manifest and its tool script. If either is missing, it stops and tells you to run setup. It won't create records by hand or substitute another tracker.
- **Readable git history:** valid base and candidate refs and a non-empty diff.
- **Spec and Task records**, or an explicit accepted request, for the Spec axis, recovered through the Workbench's own tools.
- **Subagent delegation** for truly independent review. The FAQs cover what happens without it.

## What it does not authorize

A review never grants permission to fix the code, publish it, approve it on GitHub or merge it, and the skill repairs nothing while it reviews. A review done by you or the same agent that wrote the code isn't independent: it is labeled self-review and can't satisfy a gate that requires independence.

## FAQs

### What if I haven't written a spec file?

An explicit accepted request is enough. State it in your message and the Spec reviewer works from that. If nothing supports what counts as accepted, the Spec axis is marked uncovered rather than guessed, and Standards still runs. Missing evidence counts as unknown, never as a pass.

### Why are there two reports instead of one merged list?

Merging would hide which axis a finding came from. Apart, they show at a glance whether the code is conventional but wrong, or right but sloppy.

### What if subagents aren't available?

Independent review needs delegation that is both available and authorized. Without it, the skill preserves both briefs, reports the unmet independence requirement, and labels anything it reviews itself as self-review. If only one axis has the evidence it needs, it runs that axis and reports the gap. The workaround is to authorize delegation, or give the briefs to a different agent or person.

### Does a smell finding mean the code is wrong?

No. The baseline is heuristic. A note like "possible Middle Man" is a prompt to look, and a documented repo standard that endorses the pattern overrides it.

### What if I keep editing while the review runs?

The review covers only the commits or snapshot it pinned. Changed content must be reviewed before it counts as covered, and an incomplete workspace capture is reported before any coverage claim.

## It's working when

- The report names the base and candidate SHAs, or the snapshot, that were reviewed.
- Standards and Spec appear as two separate sections, with no findings blended between them.
- Each finding points to a file or hunk and to the rule, heuristic or request line behind it.
- Smell findings are worded as heuristics, and none contradicts a documented repo standard.
- Gaps are stated openly: an uncovered Spec, missing standards, an unavailable subagent or an incomplete snapshot.
- Nothing in your repo changed to produce the review: no commits, staging or resets.
- The report closes with a one-line tally of findings per axis and the most serious issue on each side.

## Where it fits in the workflow

Code review is the main skill of the **Judge** stage (Review, verify). It follows the Journey stage: [journey](/skills/journey) takes a Task through implementation and checks, and independent review then happens on the assembled result. Findings become a new Journey run rather than being fixed inside the review. When a candidate is clean enough to ship, the next stop is the Complete stage, where [land](/skills/land) handles publishing, merging and cleanup under existing authority. Land points back here when it needs independent review. If you're unsure what comes next, ask [ask-workbench](/skills/ask-workbench).
