# TK-002 - A committed up-to-Spec report lists each unmet acceptance criterion of one active Spec with evidence

**Task ID:** TK-002
**Spec ID:** S-013
**Slice:** A committed up-to-Spec report lists each unmet acceptance criterion of one active Spec with evidence
**Status:** done
**Blockers:** none
**Destination:** spec-acceptance: Up to Spec
**Planned verification:** script test on a fixture Spec plus one real report

## Assignment

**Target branch:** `main`. Branch from `origin/main`, open a PR into `main` and merge it once current and checked, per `AGENTS.md`. Orchestrator C's cloud lane: read through Git and GitHub only, hold no Supabase or Vercel secret, write no product code. Reports go to `workbench/feedback/coherence/`.
**Claimed by:** orchestrator-C
**Current claimant:** orchestrator-C
**Proof:** uv run pytest: 47 pass at 206fa51 (6 up-to-Spec fixture tests incl. must-fail invariant; mutation forcing met-without-evidence fails 4 tests); report workbench/feedback/coherence/UP-TO-SPEC-S-004-2026-11-01.md for S-004 at main 8b70874 (0 met, 7 not met)

Read `AGENTS.md`, this Task, the parent Spec, ADR-001F under `workbench/docs/adr/`, and `node workbench/tools/spec-workbench.mjs show S-004 --json` (or another active Spec).

Deliver a read-only up-to-Spec report for one named active Spec: for each acceptance criterion, met (with the evidence it cites: commit, test or row), not met, or unknown. A criterion is never met without evidence. Commit one real report.

Out of scope: fixing gaps; reviews (TK-004).

Hand back to S-013 with `close`.

## Acceptance

- [ ] A fixture Spec with one evidenced and one unevidenced criterion reports met and unknown respectively.
- [ ] A test fails if any criterion is reported met with no evidence.
- [ ] One real report is committed for a named active Spec at a named commit.

## Receipt

| Run | Branch | HEAD SHA | Upstream | Dirty | Tests | Docs touched | Remaining gap | Checksum |
|---|---|---|---|---|---|---|---|---|
| 1 | claude/vigilant-wright-r50huh | 206fa51e0d7799ae99dd6897f9e3728904407c71 | ahead 0 behind 0 | 0 | uv run pytest: 47 pass at 206fa51 (6 up-to-Spec fixture tests incl. must-fail invariant; mutation forcing met-without-evidence fails 4 tests); report workbench/feedback/coherence/UP-TO-SPEC-S-004-2026-11-01.md for S-004 at main 8b70874 (0 met, 7 not met) | workbench/feedback/coherence/UP-TO-SPEC-S-004-2026-11-01.md; RUNBOOK line blocked by COH-003 | Specs do not yet use an Evidence: clause on acceptance lines; checked lines without one report unknown by design; close attribution: {"agent":"orchestrator-C","claimant":"orchestrator-C","onBehalfOf":null} | f9c0b5833d28f64962cedff915a4a1b16bd692747a49f28832490d52f5abbfe5 |
