# TK-003 - A skills report lists RSI rows with no skills commit or one behind the current skills `main`

**Task ID:** TK-003
**Spec ID:** S-013
**Slice:** A skills report lists RSI rows with no skills commit or one behind the current skills `main`
**Status:** blocked
**Blockers:** S-006
**Destination:** spec-acceptance: Skills in sync
**Planned verification:** script test on fixture rows plus one real report

## Assignment

**Target branch:** `main`. Branch from `origin/main`, open a PR into `main` and merge it once current and checked, per `AGENTS.md`. Orchestrator C's cloud lane: read through Git and GitHub only, hold no Supabase or Vercel secret, write no product code. Reports go to `workbench/feedback/coherence/`.

Read `AGENTS.md`, this Task, the parent Spec, and S-006's result-table migration under `supabase/migrations/`.

Deliver a read-only skills report: query RSI rows with the publishable key and list rows with no skills commit, and rows whose commit is behind the current skills `main`. If this lane cannot read the skills repository, report those rows as unknown rather than guessing. Commit one real report.

Hand back to S-013 with `close`.

## Acceptance

- [ ] On fixture rows, an unpinned row and a behind row are each listed; a current row is not.
- [ ] The check uses only the publishable key; no secret is configured in this lane.
- [ ] One real report is committed.
