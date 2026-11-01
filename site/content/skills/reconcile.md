---
name: reconcile
summary: Brings your project's Spec, Task records and board back in line with what the code and evidence show, so the next agent can continue from the records alone.
pin: 878241202bf7ec97c0952287f1633f6f0ddf1a6e
credit: original
credit_text: Original to Kayden Clark.
---

## What it does

Records go stale fast. A run finishes, a review fails, a branch lands or the owner changes their mind, and the written record still describes the old world. `reconcile` compares each written claim with evidence you can check, then corrects the claim in the one place that owns it.

It works on a **Workbench**, the folder of structured project records that [setup-workbench](/skills/setup-workbench) creates. Three kinds of record matter here:

- A **Spec** is the **destination** record: what "done" means, the acceptance checklist, decisions and an append-only evidence log. It also holds the **next gate**, the next substantive check or action before work can advance.
- A **Task** records one implementor run: status, proof, receipts and decisions.
- The **board** is a generated summary of Specs and Tasks. A tool regenerates it; nobody edits it by hand.

A pass has four parts.

**Pin the result.** The skill identifies what made the records stale and how far the assignment lets it publish. For Git work it resolves the base and the candidate to full commit SHAs after a fresh fetch, and keeps dirty files apart from committed proof. A hand-back note or green badge shows only what someone reported, so the skill checks claims at their named revision and reruns a cheap check when the evidence is missing.

**Classify every claim** as **supported**, **stale**, **contradicted** or **unknown**. A stale or contradicted claim is then an **implementation gap** (accepted intent is newer than the code, so work remains and the intent is never bent to fit), **documentation drift** (the code was verified and the description lags, so the description is fixed) or an **ambiguity** that stays open.

**Fix each claim where it lives, once.** Acceptance and the next gate go in the Spec, one run's receipt and proof in its Task, term meanings in the glossary, procedure in the runbook. A durable choice a Task made goes into its durable owner (a Spec decision, a decision record or the glossary) and only then is the Task's decision row marked reconciled. Nothing is deleted: corrections are appended and link to the row they fix. A stale instruction such as "merge this" is replaced with what actually comes next, or what blocks it.

**Regenerate and read back.** The board is regenerated, records are published only as far as the assignment allows, and the skill rereads the owners as a stranger would. A cold reader must be able to say which revision was achieved and where it sits, what was checked and what was not, which acceptance lines remain open, and the single next action with its owner. If they cannot, the skill repairs the records rather than writing a longer report.

For Git proof it documents a protected-read helper that clears inherited `GIT_*` variables and disables replacement refs, so a stray setting cannot redirect a check to the wrong commit. Containment proves ancestry only.

## When to use it

Reach for it when records and reality may have drifted apart: a run came back, a reviewer or the owner's **Human QA** (their own hands-on check) rejected a candidate, a candidate landed, the owner corrected a decision that running work depends on, a record disagrees with the code, or work stopped early.

| What you have | Reach for |
| --- | --- |
| A read-only status report on the board | [sitrep](/skills/sitrep) |
| A finished candidate that must reach its target branch | [land](/skills/land) |
| Working notes that should become durable docs | [promote](/skills/promote) |
| A destination that needs rewriting after a confirmed change | [map](/skills/map) |
| New Task records for remaining work | [plan](/skills/plan) |
| Records that no longer match what happened | `reconcile` |

## Example request

> TK-014 just came back with a green test run and a note saying it merges cleanly. Reconcile S-005: check what was delivered against the Task's acceptance, update the records, and tell me the next gate.

The skill pins the returned commit, checks the claimed result at that revision and records the outcome. If the Task's acceptance is met, it closes the run through the project's lifecycle command. If not, it leaves the Task open and records the gap. Either way it replaces the generic next gate with the real one.

## What it requires

- A Workbench. If `workbench/manifest.json` or `workbench/tools/spec-workbench.mjs` is missing, the skill stops and sends you to set one up. It will not create records by hand or use another tracker.
- The room's own `AGENTS.md`, runbook, glossary and manifest, read before anything is written. Room policy wins.
- The native `spec-workbench` commands, such as `doctor`, `report`, `receipt`, `close`, `record-landing` and `render`. Their refusals are recorded, not worked around.
- For cited Git proof, a trusted `git` and `bash` and a fresh fetch, since a local ref says nothing reliable about the remote.
- A single writer per record. If another writer owns one, the skill prepares the exact correction instead of editing it.

## What it does not authorize

Reconciling is bookkeeping, not approval. Running it never gives you a review PASS, the owner's sign-off, a Task closure the lifecycle would reject, a finished destination, a merge or a release. It records Human QA only from the owner's real decision. Completing, retiring or discarding a Spec is a separate closure sequence. An author who switches roles to reconcile is still not an independent reviewer.

It never ticks an acceptance line without its own evidence, hand-edits a generated board or bypasses a validator. For changed intent it leaves acceptance and Task assignments alone and prepares proposed corrections for `map` and `plan`, running them only if the assignment also authorizes that.

## How each event is handled

- **Task complete.** The skill records the receipt and closes the run, then compares the destination's open acceptance lines with the remaining Tasks. Uncovered lines get a new Task or a note on why they wait. Dependents that need the run's content hold off until the target branch holds it and passes the checks; a push or open PR does not release them, because the runtime treats a done blocker as satisfied.
- **Task incomplete.** The old Task stays open with its acceptance untouched, and the leftover work becomes a new, smaller Task. If the tooling has no way to retire the old one, the skill records a **lifecycle gap** (a missing operation, written down openly) instead of deleting or falsely closing anything.
- **Failed review or owner finding.** A new commit or green test never clears the finding. The skill unchecks each acceptance line a confirmed finding contradicts, resets any Completion Result claiming the failed behavior, and turns each finding into a corrective Task. The repaired candidate needs new **whole-Spec QA** (checking the assembled destination against all its acceptance once the last Task closes) and a new independent review. It never records a verdict on its own assembly, and a gap against delivered work belongs to a new Spec.
- **Landing.** It records the landed candidate, the fetched target SHA and the next gate. A merge approves nothing.
- **Changed intent.** It traces what depends on the corrected idea, holds back affected merges, pauses affected runs it controls, and lets other work carry on.

## FAQs

### Why did it leave a Task open when the tests are green?

A green run shows a check passed, not that the Task's acceptance was met. The skill closes a Task only when its acceptance holds at the pinned candidate. Otherwise it records the gap and queues a smaller follow-up Task. To close the original, put the missing acceptance evidence at the candidate.

### Why won't it tick the Spec's acceptance boxes after a hand-back?

A box gets ticked only when evidence exists for that exact line. Per-run progress goes in the evidence log, and the boxes are checked during whole-Spec QA.

### A helper skill it mentions is not installed. What then?

It uses whatever procedure the project documents for that step. If none exists, it prepares the proposed edit with its evidence, records the missing procedure and who is responsible, and holds only the dependent work.

## It's working when

- A cold reader can name the achieved revision and separate what was verified, and where, from what was not.
- Each claim is marked supported, stale, contradicted or unknown, with evidence behind it.
- Every record names a single next action or blocker and who owns it, even when work is unfinished.
- Old evidence, receipts and failed findings are still there, with corrections linked to what they fix.
- A checked acceptance line always has its own evidence, and the validator passes on a board the tool regenerated.

## Where it fits in the workflow

`reconcile` belongs to the **Complete** stage (land and preserve), beside [land](/skills/land). [orchestrate](/skills/orchestrate) calls it to record the hand-backs it accepts.

- **Before it:** [journey](/skills/journey) delivers a run, [land](/skills/land) merges and proves containment, and a reviewer or the owner may return findings.
- **After it:** [plan](/skills/plan) writes the next Task records, [map](/skills/map) rewrites a destination when intent changed, and [land](/skills/land) sends a finished candidate to its target.
- **Beside it:** [promote](/skills/promote) and [jot](/skills/jot) take the durable understanding it routes to them, and [sitrep](/skills/sitrep) reads the board it regenerates.
