# TK-004 - A Spec review names its exact commit and comes from a context that did not build the Spec

**Task ID:** TK-004
**Spec ID:** S-013
**Slice:** A Spec review names its exact commit and comes from a context that did not build the Spec
**Status:** done
**Blockers:** TK-002
**Destination:** spec-acceptance: Independent review
**Planned verification:** procedure test refusing a builder-session review and a stale commit

## Assignment

**Target branch:** `main`. Branch from `origin/main`, open a PR into `main` and merge it once current and checked, per `AGENTS.md`. Orchestrator C's cloud lane: read through Git and GitHub only, hold no Supabase or Vercel secret, write no product code. Reports go to `workbench/feedback/coherence/`.
**Claimed by:** claude-impl-s013-tk004
**Current claimant:** claude-impl-s013-tk004
**Proof:** uv run pytest: 606 passed, 4 skipped at dd1e2e8 (11 in tests/test_coherence_review.py: builder session/agent/closed-Task claimant refused before native verdict; verdict stale after a code change or Spec digest change); end-to-end probe in a throwaway clone: record -> native verdict -> status current, then stale after a README change; render no diff, doctor no blockers, layout valid, git diff --check clean

Read `AGENTS.md`, this Task, the parent Spec, ADR-001E under `workbench/docs/adr/`, `workbench/specs/REVIEW-RECEIPT-TEMPLATE.md` and the TK-002 report.

Deliver the independent Spec review procedure: a review receipt names the exact assembled commit and the reviewing context, is refused when that context built the Spec, and becomes stale when the reviewed commit or Spec content changes. Use the room's existing review and verdict tools where they fit; add only what they lack.

Hand back to S-013 with `close`.

## Acceptance

- [x] A review recorded by the building session is refused (test). Evidence: `tests/test_coherence_review.py` (`RecordRefusesBuilderTest`, `test_verdict_by_the_building_session_is_reported_refused`).
- [x] A review reused after the commit changed is reported stale (test). Evidence: `tests/test_coherence_review.py` (`test_review_reused_after_the_commit_changed_is_stale`, `test_review_reused_after_spec_content_changed_is_stale`).
- [x] The procedure is documented where RUNBOOK points. Evidence: [review receipt template](../../../../../../specs/REVIEW-RECEIPT-TEMPLATE.md), section Independent Spec review procedure.

## Receipt

| Run | Branch | HEAD SHA | Upstream | Dirty | Tests | Docs touched | Remaining gap | Checksum |
|---|---|---|---|---|---|---|---|---|
| 1 | feature/s013-tk004-review-procedure | dd1e2e83882a8f68c1d2946956d8617a98ecfcf9 | ahead 0 behind 0 | 0 | uv run pytest: 606 passed, 4 skipped at dd1e2e8 (11 in tests/test_coherence_review.py: builder session/agent/closed-Task claimant refused before native verdict; verdict stale after a code change or Spec digest change); end-to-end probe in a throwaway clone: record -> native verdict -> status current, then stale after a README change; render no diff, doctor no blockers, layout valid, git diff --check clean | workbench/specs/REVIEW-RECEIPT-TEMPLATE.md (Independent Spec review procedure; Reviewing context field); workbench/feedback/coherence/REVIEW-STATUS-S-004-2026-11-02.md; RUNBOOK unchanged (2,995 of 3,000 chars; it already points Review at the template) | Checker lives at src/ams/coherence/review.py, not in the native gate: bare spec-workbench verdict and complete still accept a builder or stale-commit verdict until setup-workbench adopts the check; builder sessions are known only from AMS-Context trailers (earlier commits carry none, so older builders are matched by agent name only); S-013 itself has orchestrator-C as a builder, so its review must come from another context; close attribution: {"agent":"claude-impl-s013-tk004","claimant":"claude-impl-s013-tk004","onBehalfOf":null} | 70f34fff1dfc00f5e7a2a4a85656e3329fcc6caffff951a2a61d6721e12b8220 |
