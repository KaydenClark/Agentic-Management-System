---
name: land
summary: Gets finished work safely onto its target branch, fixes what blocks the merge, proves the result, and cleans up with guards.
pin: 878241202bf7ec97c0952287f1633f6f0ddf1a6e
credit: adapted
credit_text: Combines Kayden Clark's combat-medic Land skill with the Workbench delivery path. Tree verification, worktree provenance, refused-removal handling and explicit-request-only discard are adapted from [obra/superpowers finishing-a-development-branch](https://github.com/obra/superpowers/tree/2ce8aa15d05bd57213e6f746f953aafb7ded7a8b/skills/finishing-a-development-branch) by Jesse Vincent, MIT License. That source's fixed option menu and unconditional local merge are not kept.
credit_license: MIT
---

## What it does

`land` carries finished work to the branch it belongs on and proves it arrived. It also repairs what stands in the way: unsaved changes, conflicts, a stale branch, a moved commit, or records that disagree with the code.

A **Workbench** is the project scaffolding the catalog's skills run on: a manifest, records for each **Spec** (a described destination) and **Task** (one unit of work toward it), and a CLI. Permissions come from the owner's real grants, never from files on the candidate.

Its core ideas:

- **Candidate and target.** The *candidate* is the branch plus its full commit SHA, since names move. The *target* is where it lands, normally `main`, matched to the pull request's real base.
- **Endpoint.** Each run names where it stops: **Check** (a read-only answer to "will this merge?"), **Publish** (committed, pushed, PR opened or updated), **Land** (the target contains the candidate and records are reconciled), **Release** (only where the project reserves it for the owner), or **Clean up**. A run that edited anything must at least commit and push, and may not leave work local or stashed.
- **Intensity.** You declare **Stabilize** (secure your work, touch nothing else) or **Repair** (fix the blocker, verify, continue) before changing anything. A **combat medic** request means repair.
- **Recovery boundary.** Before any risky command it stages your files by name, commits, pushes, then fetches to confirm the remote branch holds the commit. A push message is not proof; a fresh fetch is. It never stages credentials or `.env` files, and it checks repository visibility first, since a public push publishes everything committed.

It then simulates the merge against the fetched target without touching your working tree, and sorts any blocker into one of five modes:

| Mode | Looks like | Treatment |
|---|---|---|
| **Unsaved** | Dirty or ahead of the remote | Secure recovery only |
| **Diverged** | The simulation reports conflicts | Hand off to [resolving-merge-conflicts](/skills/resolving-merge-conflicts), then re-verify |
| **Moved** | Candidate or target changed since checks | Rerun checks; changed code needs fresh review |
| **Record drift** | Tracker or docs have fallen out of step with the code | Bring them back in line with what was verified, rebuilding generated files |
| **Rejected** | A test, review or gate refuses | Repair landing-side defects; wrong product logic goes back to its implementor |

For Diverged, the target is merged into the candidate in a separate worktree, never by rebasing.

Then it verifies the exact candidate, merges with the head commit pinned so a late push cannot slip in, and fetches the target to prove it contains that commit. Checks run again on the resulting target commit, since PR checks cannot show that. Queued PRs land one at a time; trouble with one leaves the rest untouched.

Inside a Workbench there are three more steps:

- **Merge gate.** The native gate runs on the exact candidate first. For a Task it reports; for a Spec it refuses incomplete work or content without a passing review verdict.
- **Landing record.** `record-landing` updates a few fields, mainly the next action. It never approves anything or marks a Task done, and it lands through a record-only PR.
- **Spec completion.** `complete` closes a Spec only when every Task is done, review has passed, owner approval matches current content, and that content is on the fetched remote `main`.

Every run ends with a receipt: outcome, what was wrong, changes, verification, and what remains, including any branch or worktree kept and why.

## When to use it

Reach for `land` when the work is built and the question is delivery: "land this", "will this merge?", a merge error, unpushed work, or a branch that moved under you.

Under the default policy, where feature branches merge straight into `main`, being asked to do the work already covers merging its own PR once it is current and required checks pass.

| What you have | Reach for |
|---|---|
| Text conflicts that need both sides' intent understood | [resolving-merge-conflicts](/skills/resolving-merge-conflicts), then back to `land` |
| A PR body to write | [pr](/skills/pr) |
| Independent review of a branch or PR | [code-review](/skills/code-review) |
| Wrong product logic or a failing test in the work itself | [journey](/skills/journey), or [diagnosing-bugs](/skills/diagnosing-bugs) if you are authorized to implement |
| Records that drifted, as a standalone job | [reconcile](/skills/reconcile) |

## Example request

> My feature branch has two uncommitted files, and main has moved since I branched. Land this on main, and tell me honestly if anything blocks it.

`land` would commit and push your two files first, simulate the merge against the fetched `main`, and list every conflicted path before editing. Conflicts go to the conflict skill, then checks rerun on the updated head. A failing test caused by your own logic goes back to the implementor.

## What it requires

- **A Workbench.** It checks for the manifest and the Workbench CLI first. If either is missing it stops and sends you to [setup-workbench](/skills/setup-workbench).
- **Trusted policy.** Branch policy read from the forge (the hosting service, such as GitHub) or an independent owner source, not from the candidate.
- **A controlled environment.** Test suites and Git helpers can run configured code, so it expects verified interpreters and checked hooks, and runs candidate code only in an isolated service or via verified CI.
- **Tools and authority.** `git`, `gh`, and Bash 4.4 plus CPython 3.4 or newer for cleanup. Push, merge, release and cleanup permissions come from the owner or trusted policy.

## What it does not authorize

- **No release.** A checked merge into `main` counts as landing, not releasing. Where the project keeps releases or production deploys for the owner, those need the owner's explicit say-so, which review, checks and a merge cannot supply.
- **No approval or completion.** A merge never signs off on, finishes or reassigns a Task, and a landed change can still be unfinished.
- **No Human QA.** Owner approval and **Human QA** (the owner's own hands-on check) stay with the owner. It records an approval only when it can verify it against the exact content, and never creates an approval, finding or verdict for someone else.
- **No self-review.** It never reviews work it built or repaired, and a repair after review voids that review.
- **No bypasses.** No admin merges, skipped protection or review holds, or merging failing work just to keep it safe.
- **No history surgery.** No force-pushes, shared-history rebases, stash, reset or clean to tidy a tree, and no branch renames.
- **No unrequested deletion.** Unmerged work goes only on explicit owner request, risks listed first.

## FAQs

### Why did it refuse to merge when my checks are green?

Green proves only the tree that was tested. If the candidate moved, the target advanced, or required review does not cover this exact commit, `land` stops and names the smallest gap. Rerun checks on the new head, and get fresh review for changed code.

### Why won't it clean up my worktree?

Cleanup runs only after the target is proven to contain the merged commit, and even then it is cautious. A clean status does not prove removal is safe, since removal silently destroys ignored files and some index flags hide changed ones. Those, an active writer, an unknown owner, or a host-created checkout make it keep the worktree and say why. Preserve or explicitly discard the contents, then retry.

### What if the same verification fails twice?

With no clearly safe next step, that is a hard stop. The skill records the blocker and the decision it needs instead of looping or weakening the check. Failed required review, new logins, irreversible remote deletion, credentials in the diff and unknown ownership also stop it.

### What if I can't run the checks safely here?

They count as blocked, not passed. It will not run candidate code in a privileged context or trust a green badge it cannot tie to the exact commit.

## It's working when

- The run names its endpoint and intensity, and your work is confirmed on the remote early by a fresh fetch.
- Every conflicted path is listed before any edit.
- The merge is pinned to the reviewed commit, and the fetched target is shown to contain it.
- Records name the real next action, and each retained branch or worktree has a stated reason.
- The closing receipt is honest, including outcomes such as blocked or "landed, unclosed".

## Where it fits in the workflow

`land` sits in the **Complete** stage (Land, preserve), beside [reconcile](/skills/reconcile). It follows the [journey](/skills/journey) (where an implementor builds one Task) and, when the Spec calls for assembled review, [code-review](/skills/code-review) in the Judge stage.

[resolving-merge-conflicts](/skills/resolving-merge-conflicts) handles text conflicts and [pr](/skills/pr) writes the PR body. Lasting knowledge goes to [jot](/skills/jot) or its documentation owner, and [reconcile](/skills/reconcile) keeps records in agreement afterward. Findings from a failed review go to a new Journey, not into `land`.
