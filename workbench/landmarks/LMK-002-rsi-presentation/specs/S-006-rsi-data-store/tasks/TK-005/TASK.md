# TK-005 - Seed and test rows: a row without source and strength label is refused and test rows never reach the publishable key

**Task ID:** TK-005
**Spec ID:** S-006
**Slice:** Seed and test rows: a row without source and strength label is refused and test rows never reach the publishable key
**Status:** done
**Blockers:** TK-003
**Destination:** spec-acceptance: Real sources only
**Planned verification:** live tests for the refusal and the hidden test row

## Assignment

**Target branch:** `main`. Branch from `origin/main`, open a PR into `main` and merge it once current and checked, per `AGENTS.md`.
**Claimed by:** orchestrator-b-tk005-implementor
**Current claimant:** orchestrator-b-tk005-implementor
**Proof:** PR #42 at 55c3856, Codex no findings: ams.source_rules checks every write; pytest 250 passed, 3 skipped (red first); live ams-sources livecheck: writer and DB refused no source, blank ref, bad strength on all 3 tables; site key saw 0 test rows; 0 left; no migration; advisors none

Orchestrator B's lane only. Read `AGENTS.md`, this Task, the parent Spec (`../../SPEC.md`), DDR-000T and DDR-000W, and the writer under `src/`.

Deliver the writer rules S-002's seeding depends on: a row is refused unless it names its source and a strength label from a closed list (anecdote, single trial, repeated trials, held-out with interval); a row may be marked as a test row, and the site's read policy never returns test rows.

Out of scope: choosing or writing seed rows (S-002 TK-001).

Hand back to S-006 with `close`.

## Acceptance

- [x] A row with no source, or a strength label outside the list, is refused.
- [x] A marked test row is readable with the service key and invisible to the publishable key.
- [x] `uv run pytest` passes.

## Receipt

| Run | Branch | HEAD SHA | Upstream | Dirty | Tests | Docs touched | Remaining gap | Checksum |
|---|---|---|---|---|---|---|---|---|
| 1 | feat/s006-tk005-source-rules | 55c38564bd862bc86ecb0c6399dd99f9029dbd32 | ahead 0 behind 0 | 0 | PR #42 at 55c3856, Codex no findings: ams.source_rules checks every write; pytest 250 passed, 3 skipped (red first); live ams-sources livecheck: writer and DB refused no source, blank ref, bad strength on all 3 tables; site key saw 0 test rows; 0 left; no migration; advisors none | RUNBOOK, ARCHITECTURE, Spec (recorded_fact) | S-002 picks seed rows; close attribution: {"agent":"orchestrator-b-tk005-implementor","claimant":"orchestrator-b-tk005-implementor","onBehalfOf":null} | 9cadb70740bcfd6764db579a5e761652d834d8c83150985c0f5b1f933df9c91c |
