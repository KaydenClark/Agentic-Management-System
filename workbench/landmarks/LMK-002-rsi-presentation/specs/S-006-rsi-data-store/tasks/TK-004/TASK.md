# TK-004 - Build-history rows are imported from this build's real Spec, Task, PR and commit records, returns and corrections included

**Task ID:** TK-004
**Spec ID:** S-006
**Slice:** Build-history rows are imported from this build's real Spec, Task, PR and commit records, returns and corrections included
**Status:** done
**Blockers:** TK-002
**Destination:** spec-acceptance: Build history from real records
**Planned verification:** import run, row counts against the records, and a rerun adding none

## Assignment

**Target branch:** `main`. Branch from `origin/main`, open a PR into `main` and merge it once current and checked, per `AGENTS.md`.
**Claimed by:** claude-s006-tk004
**Current claimant:** claude-s006-tk004
**Proof:** PR #31 merged as 4d74e90 and PR #37 as d26bb8c: ams-history derives build_events rows from git, gh and the lifecycle tool's JSON. Tests came first: an import error, then 2 red real-record cases, then 3 red regressions for Codex P2 findings 4435914075 and 4435914076 (fixed, replied and resolved), then 2 red widened-ID cases. uv run pytest: 160 passed, 1 skipped. Live import from the main checkout at d26bb8c inserted 446 rows (1 already recorded). Its counts match the records: 242 commits on origin/main+dev (git rev-list), 29 merges against 29 merged PRs (gh), 13 Specs and 50 Tasks (spec-workbench list/show), 37 PRs opened. Further reruns inserted only events that had newly occurred (2, 1, 13); a back-to-back rerun inserted 0. readcheck with the publishable key: rows 463, missing 0, extra 0, unsourced 0, in time order yes. Corrections include the Codex findings and fixes on PRs #16 and #18; PR #26 closed unmerged is a return. render left no diff; doctor reported no blocking finding.

Orchestrator B's lane only. Read `AGENTS.md`, this Task, the parent Spec (`../../SPEC.md`), the build-history table and writer from TK-002, and `node workbench/tools/spec-workbench.mjs list --all`.

Deliver the proof-of-construction import: a command that reads this repository's real records (Spec and Task files and their evidence logs and receipts, `git log` of `main` and `dev`, and pull requests through `gh`) and writes one build-history row per event, each naming its source path, PR number or commit SHA and its time. Returned work and corrections (a PR closed unmerged, a reverted commit, a Task reopened, a Jot correction) are rows with their own kind. The import is idempotent. It never invents an event or edits history.

Out of scope: rendering (S-003 TK-006).

Hand back to S-006 with `close`.

## Acceptance

- [x] After an import, row counts match the counts read from the records for at least Specs, Tasks, merged PRs and `main` commits.
- [x] At least one return or correction appears as a row in order, if the records hold one; otherwise the report says none exist.
- [x] Running the import twice adds no rows.
- [x] Every row names a source; a test fails on a row without one.

## Receipt

| Run | Branch | HEAD SHA | Upstream | Dirty | Tests | Docs touched | Remaining gap | Checksum |
|---|---|---|---|---|---|---|---|---|
| 1 | feat/s006-tk004-close | ab2118ce64c101873eda4b72b2cc0c0fdb91f6d1 | ahead 0 behind 0 | 0 | PR #31 merged as 4d74e90 and PR #37 as d26bb8c: ams-history derives build_events rows from git, gh and the lifecycle tool's JSON. Tests came first: an import error, then 2 red real-record cases, then 3 red regressions for Codex P2 findings 4435914075 and 4435914076 (fixed, replied and resolved), then 2 red widened-ID cases. uv run pytest: 160 passed, 1 skipped. Live import from the main checkout at d26bb8c inserted 446 rows (1 already recorded). Its counts match the records: 242 commits on origin/main+dev (git rev-list), 29 merges against 29 merged PRs (gh), 13 Specs and 50 Tasks (spec-workbench list/show), 37 PRs opened. Further reruns inserted only events that had newly occurred (2, 1, 13); a back-to-back rerun inserted 0. readcheck with the publishable key: rows 463, missing 0, extra 0, unsourced 0, in time order yes. Corrections include the Codex findings and fixes on PRs #16 and #18; PR #26 closed unmerged is a return. render left no diff; doctor reported no blocking finding. | RUNBOOK names ams-history import\|readcheck (2,990 chars); ARCHITECTURE names ams-history (2,999); the Spec's verified state describes build_events | Spec and Task records are read from main only; records that exist only on dev (S-003, S-007 Task closes) are not imported, though dev commits and PRs are. Evidence and receipt rows are keyed by table index, so rewriting a log (as S-004's prune did) leaves rows from the earlier text. Review-thread resolution reads only the first 100 PRs, and the import refuses beyond that. No scheduled re-import: new events appear only when ams-history import runs. The Spec's RSI-table clause in Current Verified State is TK-003's to update.; close attribution: {"agent":"claude-s006-tk004","claimant":"claude-s006-tk004","onBehalfOf":null} | 01a223ccbb50e5a4107efbe125fdc70b7669d63eecef1553ad994be266c1fbca |
