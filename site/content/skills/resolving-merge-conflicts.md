---
name: resolving-merge-conflicts
summary: Settles a text merge conflict by working out what each side meant to change, keeping both where they fit together, and checking the result before you move on.
pin: 878241202bf7ec97c0952287f1633f6f0ddf1a6e
credit: adapted
credit_text: Adapted from [Matt Pocock's skills](https://github.com/mattpocock/skills), MIT License.
credit_license: MIT
---

## What it does

`resolving-merge-conflicts` is a short method for the moment Git hands you a conflict. Instead of keeping whichever marked block seems right, or whichever came last, this skill asks a question: what was each side trying to accomplish?

The agent works in roughly this order.

1. **Read both sides before editing.** That means the conflicting changes themselves and the tests around them.
2. **State each side's intent.** A **change intent** is a plain statement of the purpose behind one branch's edit, for example *this side renames a setting* or *that side adds a retry*. Writing intents out first makes the agent understand both edits before it touches either.
3. **Find the overlap.** Some of the two intents may truly collide. Often much of them does not, and Git simply cannot tell.
4. **Preserve compatible behavior.** Where both intents can hold at once, the result keeps both. The skill rules out choosing by line order, which is the failure where one block silently wins and the other side's work disappears.
5. **Escalate only a real product choice.** If the intents cannot both be true and the choice is about what the product should do, the agent stops and asks. Anything short of that, it resolves itself.
6. **Verify.** It runs focused tests for the touched area, then the project's relevant checks, and inspects the final diff.
7. **Record only what matters.** A consequential decision goes in the merge commit message or the pull request description. Otherwise the merge history and the tests are the evidence.

The skill says nothing about branches, merge strategy or delivery.

## When to use it

Use it when a merge, or an update of a branch from its target, leaves conflicting text that someone has to decide. You can ask for it directly. The [land](/skills/land) skill also hands text conflicts to it, and uses it when a branch has diverged from its target.

Neighbouring problems belong elsewhere:

| What you have | Reach for |
|---|---|
| Conflicting text that needs both sides understood and combined | `resolving-merge-conflicts` |
| Finished work that must reach its target branch, including checking whether it will merge | [land](/skills/land) |
| A conflict that is really an open product decision | The owner, the person who decides what the product should do, with the options laid out (this is where the skill stops) |
| Project records that disagree with the code after a merge | [reconcile](/skills/reconcile) |
| A resolved candidate that needs independent review | [code-review](/skills/code-review) |

Here, a **candidate** is the branch or pull request being landed.

## Example request

> My feature branch conflicts with main in the session-handling module. Main renamed the timeout setting and my branch added a retry that reads it. Resolve the conflict, keep both changes working, and tell me what you checked.

A good run restates the two intents, notes that they fit together once the retry uses the new name, writes that merged result, runs the module's tests and the project checks, and shows you the final diff.

## What it requires

The skill file names no tools and no Workbench. You need:

- A repository with a conflict to resolve, and access to both sides of it.
- Tests near the changed code, plus the project's usual checks, so the result can be verified.
- An owner you can reach, in case the conflict turns out to be a real product choice.

Its neighbour `land` does require a **Workbench**, a project's set of structured work records, created with [setup-workbench](/skills/setup-workbench). Reaching this skill through `land` therefore happens inside one; the skill itself has no Workbench step.

## What it does not authorize

The skill's job ends at a verified resolution. It grants none of the following, so treat each as a separate decision:

- **Choosing a product direction.** When the conflict hides an undecided product choice, the agent escalates it rather than deciding.
- **Pushing or landing.** When `land` calls this skill, `land` takes the work back afterward to verify and push. Resolving the text is not delivery.
- **Review approval.** `land` treats changed candidate lines, conflict resolutions included, as needing fresh checks and new required review. That review must come from a context that did not build or repair the work, so the agent that resolved the conflict cannot be the one that approves it.

## FAQs

### What if both sides really cannot be kept?

Then it is no longer a mechanical merge. If the two intents contradict and the choice is about what the product should do, the skill says to escalate. Bring the owner the two intents, the options and a recommendation. Do not let the agent pick quietly.

### The tests pass. Am I done?

Not yet. The skill also asks for the project's relevant checks and a look at the final diff. A clean text merge shows only that the text combined, not that the combined code works, and `land` says as much in its own limits. Reading the diff and running the checks are how you verify the result.

### Does it write a long record of every conflict?

No. Only a consequential decision is recorded, in the merge commit message or the pull request description. Otherwise the merge history and the tests are the record.

### What goes wrong if I skip stating the intents?

You drift back toward choosing by line order, the habit the skill rules out. If a resolution looks like it just took one side, ask the agent to list both intents and show where each one lives in the result.

## It's working when

- The agent describes what each branch was trying to do before it changes any conflicted file.
- It read the nearby tests as well as the conflicting lines.
- The merged result keeps behavior from both sides wherever they are compatible, rather than one side winning wholesale.
- A real product disagreement is raised with you instead of being settled silently.
- Focused tests and the project checks were run.
- You were shown the final diff, and any consequential decision is written in the merge commit or PR description.

## Where it fits in the workflow

It sits in the **Complete** stage (land and preserve), as a helper rather than a main step. The main flow there is [land](/skills/land) and then [reconcile](/skills/reconcile). `land` hands it text conflicts and diverged branches, updating a diverged branch by merging the target in, not by rebasing. Once the conflict is resolved, work returns to `land` to verify and push the updated candidate. Any required review comes from [code-review](/skills/code-review), not from this skill.
