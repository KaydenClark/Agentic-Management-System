# TK-002 - A committed up-to-Spec report lists each unmet acceptance criterion of one active Spec with evidence

**Task ID:** TK-002
**Spec ID:** S-013
**Slice:** A committed up-to-Spec report lists each unmet acceptance criterion of one active Spec with evidence
**Status:** in-progress
**Blockers:** none
**Destination:** spec-acceptance: Up to Spec
**Planned verification:** script test on a fixture Spec plus one real report

## Assignment

**Target branch:** `main`. Branch from `origin/main`, open a PR into `main` and merge it once current and checked, per `AGENTS.md`. Orchestrator C's cloud lane: read through Git and GitHub only, hold no Supabase or Vercel secret, write no product code. Reports go to `workbench/feedback/coherence/`.
**Claimed by:** orchestrator-C
**Current claimant:** orchestrator-C

Read `AGENTS.md`, this Task, the parent Spec, ADR-001F under `workbench/docs/adr/`, and `node workbench/tools/spec-workbench.mjs show S-004 --json` (or another active Spec).

Deliver a read-only up-to-Spec report for one named active Spec: for each acceptance criterion, met (with the evidence it cites: commit, test or row), not met, or unknown. A criterion is never met without evidence. Commit one real report.

Out of scope: fixing gaps; reviews (TK-004).

Hand back to S-013 with `close`.

## Acceptance

- [ ] A fixture Spec with one evidenced and one unevidenced criterion reports met and unknown respectively.
- [ ] A test fails if any criterion is reported met with no evidence.
- [ ] One real report is committed for a named active Spec at a named commit.
