# TK-004 - Build-history rows are imported from this build's real Spec, Task, PR and commit records, returns and corrections included

**Task ID:** TK-004
**Spec ID:** S-006
**Slice:** Build-history rows are imported from this build's real Spec, Task, PR and commit records, returns and corrections included
**Status:** blocked
**Blockers:** TK-002
**Destination:** spec-acceptance: Build history from real records
**Planned verification:** import run, row counts against the records, and a rerun adding none

## Assignment

**Target branch:** `main`. Branch from `origin/main`, open a PR into `main` and merge it once current and checked, per `AGENTS.md`.

Orchestrator B's lane only. Read `AGENTS.md`, this Task, the parent Spec (`../../SPEC.md`), the build-history table and writer from TK-002, and `node workbench/tools/spec-workbench.mjs list --all`.

Deliver the proof-of-construction import: a command that reads this repository's real records (Spec and Task files and their evidence logs and receipts, `git log` of `main` and `dev`, and pull requests through `gh`) and writes one build-history row per event, each naming its source path, PR number or commit SHA and its time. Returned work and corrections (a PR closed unmerged, a reverted commit, a Task reopened, a Jot correction) are rows with their own kind. The import is idempotent. It never invents an event or edits history.

Out of scope: rendering (S-003 TK-006).

Hand back to S-006 with `close`.

## Acceptance

- [ ] After an import, row counts match the counts read from the records for at least Specs, Tasks, merged PRs and `main` commits.
- [ ] At least one return or correction appears as a row in order, if the records hold one; otherwise the report says none exist.
- [ ] Running the import twice adds no rows.
- [ ] Every row names a source; a test fails on a row without one.
