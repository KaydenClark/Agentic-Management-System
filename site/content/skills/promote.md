---
name: promote
summary: Moves selected, supported claims from working notes into the one durable record that should own them, checks the result, and publishes only as far as you asked.
pin: 878241202bf7ec97c0952287f1633f6f0ddf1a6e
credit: original
credit_text: Original to Kayden Clark.
---

## What it does

Understanding usually lands first in working material such as notes or a Wiki page, and that is a poor place for it to stay. `promote` takes a chosen set of claims from that material and writes them into the durable record that must retain them. Each claim keeps its source, status and corrections, so the result shows where it came from and how settled it is.

Some terms. A **Workbench** is the folder of records, tools and rules that `setup-workbench` creates in a project. A **Spec** states what a capability must do and how it is accepted, and a **Task** is one assigned unit of work under it. An **owner** is the single existing record responsible for a kind of claim: the glossary, a Spec, the Runbook (operating procedures), a decision record (a consequential choice and its rationale) or a Wiki article (maintained explanation). **Claim promotion** means moving understanding into an owner. It is not promoting a Git branch into `main`, and the skill keeps the two apart.

The work runs in five steps.

1. **Recover the selection.** It reads the Workbench's controls, then pins down the source, the exact claims, corrections and your endpoint. It inspects the branch, remote, locks and dirty state before writing, and uses `jot` to recover current understanding.
2. **Sort by kind.** Meaning you confirmed, things verified, the agent's own reading, proposals and open questions stay separate. Only supported, current claims move; pending, withdrawn or superseded material stays behind with its history.
3. **Pick one owner per claim.** A routing table maps each job to a home, for example vocabulary to the glossary, procedures to the Runbook, requirements to the assigned Spec and rationale to decision records. Other records link to the owner rather than copy it. If the owner already says the same thing, nothing is added and the report says why.
4. **Write and audit.** It edits through the owner's own supported method, preserving earlier text and correction chains, then rereads each changed owner against the source. A matching hash or a passing command does not prove the meaning survived.
5. **Retain the source and publish.** The source stays, with the destination added to its history. The verified change is committed on a feature branch and pushed, then goes only as far as your endpoint allows.

Your endpoint can be local recording, branch recovery, a draft PR, or published, checked work on a named target branch. Recording does not imply publishing. A publishing PR carries the already-promoted result, so nothing is promoted twice, and after the merge the skill confirms the target holds the change and reads the landed owner before calling it published.

If an owner's text carries a confirmed **readback** (your own words, confirmed as an accurate statement of your intent), `promote` keeps them exactly and wraps them in marker comments tied to a shared Jot entry, a source-linked record kept through `jot`. A later check can compare that region with the confirmation, and an agent's rewrite cannot inherit it.

## When to use it

Reach for it when understanding has piled up in notes or a Wiki page and needs to become the record others rely on, including a decision you confirmed. A settled decision does not need a new Spec just to be recorded.

| What you have | Reach for |
| --- | --- |
| Vocabulary you are still shaping (terms confirmed there need no second promotion) | [domain-modeling](/skills/domain-modeling) |
| A fact or correction to capture in a note right now | [jot](/skills/jot) |
| Spec or Task records that disagree with what actually happened | [reconcile](/skills/reconcile) |
| A stuck or conflicted merge, or a broader landing job | [land](/skills/land) |
| Settled understanding that must become a durable owner entry | `promote` |

## Example request

> The team settled how handoffs work in last week's notes, including one correction. Promote the supported parts into the right owners, commit it on a branch, and open a PR into main. Don't merge it.

The skill selects the confirmed claims and the correction, leaves open questions in the notes, and stops at an open PR because that was your endpoint.

## What it requires

- A Workbench. The skill checks for the manifest and tool script first. If either is missing, it stops and sends you to [setup-workbench](/skills/setup-workbench) instead of creating records by hand.
- A named source and an exact selection of claims.
- Destination owners it can read and edit through their own supported procedures. A missing owner is created only through its authorized workflow.
- `jot`, and Git with a remote for the commit, push and PR steps.
- Optionally, [audit-workbench](/skills/audit-workbench), when the promotion feeds an audit. Without it, the skill returns its evidence and says Alignment Check scoring (that skill's audit-scoring step) is pending.

## What it does not authorize

- **No implementation or planning.** Promotion starts no interview, build or task claim, and touches `main` only through the publication endpoint you named. Mapping, planning, a Journey (the run that builds and checks one Task) and acceptance each need their own scoped authority.
- **No acceptance or wider permission.** A proposal stays a proposal until its real acceptance route is met, confirmed intent is not delivered work, and a note cannot widen scope or safety rules.
- **No exposure.** A private or ignored source does not license tracked or shared publication.
- **No cleanup of the source.** Trimming or deleting a note is a separate step needing its own approval, after checking that nothing depends on it.
- **No audit, trial or paid campaign.** The local check starts no whole-Workbench audit. Scoring belongs to `audit-workbench`.
- **No release acceptance.** Finishing locally does not mean the change is accepted for release, confirmed on the target branch, installed or in real use.

## Preserved legacy notes

Where the installed tooling supports it, entries from an older JSON notepad can be promoted with one checked command. You note the source revision and the destination's SHA-256, and write the full proposed destination as a temporary ignored draft inside the project.

The checked command is the `promote` subcommand of the Workbench's `sessions.mjs` tool. It takes the note to promote from and that note's revision number, the comma-separated IDs of the entries to move, the owner file to write to, the SHA-256 expected for that file, and the path of the authored draft.

The command rejects stale inputs, missing entries, unsafe paths and private material, and you may not route around a rejection. After a refusal or partial write, keep the source and draft, reread both, and retry only once the cause is resolved. If the result names a retained backup under `recovery`, keep it and inspect the destination first. Never change the expected hash without reading the edits made in between. There is no protection against crashes or concurrent writers, so keep to one writer.

## FAQs

### What if the owner already holds the claim?

Nothing is added. It checks that the existing text still carries the right meaning, source and status, and reports that no content changed.

### What happens when the source mixes settled and unsettled material?

Only the settled, supported claims move. If destination, ordering or exposure is unresolved, it holds that part, continues with the independent claims, and asks only about the decision other work depends on.

### My readback check fails. What now?

This marker and check exist only where the installed owner procedure asks for a readback region. In a Workbench generation that provides the check, `doctor` reports `readback-mismatch` when the cited region is absent, malformed, private, unconfirmed or reworded. Restore the confirmed wording, or get a newly confirmed readback, record it and cite that. Deleting the marker or weakening the check is not a fix.

### Will it leave my edits uncommitted, or merge them?

It never leaves them uncommitted: even a record-only request ends with a verified commit on a feature branch, pushed. A PR and merge happen only within the endpoint you authorized, once required checks pass. If checks fail or something blocks the merge, it stops with the branch pushed and the PR open, and reports partial progress.

## It's working when

- Each moved claim lands in exactly one owner, and other records link to it instead of copying it.
- The owner text still shows what was confirmed, what is proposed and what is open.
- The source, with its unresolved and superseded material, is still there, and unrelated owner text is untouched.
- Confirmed readback words match the cited confirmation exactly.
- The final report names the claims, destinations, checks and gaps, and whether the change is local, pushed, in a PR or landed.
- It stopped at the endpoint you named.

## Where it fits in the workflow

`promote` belongs to the Complete stage (Land, preserve). It usually follows [jot](/skills/jot) or [domain-modeling](/skills/domain-modeling), which produce the settled understanding, and sits beside [land](/skills/land) and [reconcile](/skills/reconcile). It opens and merges its own PR within your endpoint, so reach for [land](/skills/land) only when a merge gets stuck. It hands its evidence to [audit-workbench](/skills/audit-workbench) when the promotion feeds an Alignment Check, and hands the settled source to the room's [map](/skills/map) and [plan](/skills/plan) route when preparation was also authorized.
