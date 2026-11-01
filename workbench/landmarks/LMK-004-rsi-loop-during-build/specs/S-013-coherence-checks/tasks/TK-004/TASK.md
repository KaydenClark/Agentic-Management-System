# TK-004 - A Spec review names its exact commit and comes from a context that did not build the Spec

**Task ID:** TK-004
**Spec ID:** S-013
**Slice:** A Spec review names its exact commit and comes from a context that did not build the Spec
**Status:** blocked
**Blockers:** TK-002
**Destination:** spec-acceptance: Independent review
**Planned verification:** procedure test refusing a builder-session review and a stale commit

## Assignment

**Target branch:** `main`. Branch from `origin/main`, open a PR into `main` and merge it once current and checked, per `AGENTS.md`. Orchestrator C's cloud lane: read through Git and GitHub only, hold no Supabase or Vercel secret, write no product code. Reports go to `workbench/feedback/coherence/`.

Read `AGENTS.md`, this Task, the parent Spec, ADR-001E under `workbench/docs/adr/`, `workbench/specs/REVIEW-RECEIPT-TEMPLATE.md` and the TK-002 report.

Deliver the independent Spec review procedure: a review receipt names the exact assembled commit and the reviewing context, is refused when that context built the Spec, and becomes stale when the reviewed commit or Spec content changes. Use the room's existing review and verdict tools where they fit; add only what they lack.

Hand back to S-013 with `close`.

## Acceptance

- [ ] A review recorded by the building session is refused (test).
- [ ] A review reused after the commit changed is reported stale (test).
- [ ] The procedure is documented where RUNBOOK points.
