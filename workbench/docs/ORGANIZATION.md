# Selected-file organization and recovery

Use this procedure only for an authorized assignment with a complete selected
file inventory. The [structure reference](WORKBENCH_STRUCTURE.md) describes the
shared homes. The manifest remains the path authority; this operation does not
change its lanes, application layout, skill sources or Git registrations.

The runtime moves individual shared files from legacy `research/` or `releases/`
(or their existing docs homes) into `workbench/docs/research/` or
`workbench/docs/releases/`. Other selected files are retained. Directories,
protected reference material, nested repositories and ambiguous paths refuse.
Private or ignored context is retained in place; organization never promotes it.

## Prepare and inspect the map

List every selected tracked, untracked and relevant ignored file once. Name its
owner, privacy, disposition and reason. Retain meaningful work with its owner;
reconciling its meaning is the assigned agent's job. Do not rename a stale copy
into a live owner merely to finish the map.

A local map uses this schema:

```json
{
  "schemaVersion": 1,
  "owner": "S-006M/TK-00BK",
  "entries": [
    {
      "source": "research/topic/README.md",
      "destination": "workbench/docs/research/topic/README.md",
      "action": "move",
      "owner": "research/topic",
      "privacy": "shared",
      "reason": "Maintain this investigation in the docs lane"
    },
    {
      "source": "README.md",
      "action": "retain",
      "owner": "project orientation",
      "privacy": "shared",
      "reason": "Update the current route while retaining its history"
    }
  ]
}
```

Retained Markdown files participate in current-link repair. Include every
current inbound reference that must follow the move. Outgoing links from moved
Markdown files are rebased too. The existing append-only evidence section stays
byte-identical and its links read at the plan's `snapshot.head` revision.
Immutable web citations remain unchanged. Other prose that describes historical
paths needs explicit review before selection; the runtime cannot infer its intent.

Keep the map and returned plan locally. They contain paths, hashes and Git
metadata, so review them before any shared publication. The dry run reads the
selected files, records hashes, modes, Git state, expected transformations and
inverse destinations, and writes nothing:

```bash
node workbench/tools/workbench-layout.mjs organize-plan --project /absolute/room --map /absolute/room/map.json
```

Save only the JSON response's `plan` member to an ordinary local file inside the
room, then inspect its entries, rewrite counts, preserved history, source commit,
index and registered worktrees. Confirm that the selection is complete. A plan
proves its explicit selection; it does not discover all valuable material.

## Apply, inspect and reverse

Keep one writer for the selected files. The cooperative layout lock serializes
these operations with other native layout/identity changes; it cannot freeze an
editor or another Git client. Changes to selected contents, the manifest, index,
refs or worktree topology invalidate a plan. Replan after reconciling them.

```bash
node workbench/tools/workbench-layout.mjs organize-apply --project /absolute/room --plan /absolute/room/plan.json
```

Apply requires the existing recovery collection to be ignored. Before movement,
it records original bytes and modes in a private receipt under that collection.
The receipt includes expected before/after states and created destination
parents. It is local recovery, never shared proof or a new tracker. Keep it and
its originals through forward/reverse proof and required review. The command
repairs selected current links, preserves historical anchors and leaves the Git
index and registrations unchanged. Inspect the result, then commit only the
assignment's intended source and documentation through the room's normal flow.

The result names the exact receipt. Before committing or changing refs, rehearse
rollback and reapplication on the disposable room:

```bash
node workbench/tools/workbench-layout.mjs organize-rollback --project /absolute/room --receipt /absolute/room/workbench/sessions/recovery/organization/DIGEST.json
node workbench/tools/workbench-layout.mjs organize-apply --project /absolute/room --plan /absolute/room/plan.json
```

A repeated successful apply returns `current` without changing the selected
files. Rollback restores recorded contents and modes, preserves the original
index and Git relationships, and removes only created empty destination parents.
It refuses new or changed work instead of overwriting it. After a commit/ref or
index change, retain the old receipt and reconcile against its source revision;
do not reset Git merely to satisfy rollback.

## Interruption and limits

A caught write failure attempts restoration and reports whether it succeeded.
An abrupt process exit leaves its prepared receipt and may leave
`workbench/.identity.lock`. Preserve both. Establish which operation owns the
lock and that its process has ended before that owner releases the orphan lock.
The runtime never steals it. Then use the exact receipt to recover a mixed
before/after state. A third state, unexpected data or unavailable recovery
leaves an explicit blocker and keeps the originals. No power-loss atomicity,
remote backup or cross-device recovery is claimed.

Project-created worktrees belong under `.worktrees/<assignment>/` through Git
worktree commands. External host-managed worktrees stay registered in place;
organization inventories them and refuses topology drift, but creates, relocates
and deletes none. Safe closeout belongs to its separate owning procedure.

Portable fixtures cover spaces, relative adapters, casing refusal and preserved
line endings. Symlink creation, executable bits and native host discovery depend
on the actual platform. Record unavailable Windows or host observations as gaps;
a fixture pass does not supply them. Main promotion, live consumer installation,
cleanup and release readiness retain their existing authority and proof gates.
