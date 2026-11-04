# TK-002L - Trial evidence stays comparable, visible and stable under refresh

**Task ID:** TK-002L
**Spec ID:** S-007
**Slice:** Repair four owner-approved RSI presentation defects end to end
**Status:** in-progress
**Blockers:** none
**Destination:** spec-acceptance: Provenance and series; Not only up; Shared data states
**Planned verification:** Candidate fill contrast in both themes; rendered hash invariance under freshness changes and sensitivity to evidence; grader isolation; run-only failure visibility without fabricated results; site build and suite.
**Claimed by:** codex-rsi-four-fixes
**Current claimant:** codex-rsi-four-fixes

## Assignment

Owner approval in website repair chat, 2026-11-04: approved four previously reported fixes and requested actual skill failures, model tier, failed activity and correct outcome. Use existing `Feature/S-007-rsi-chart-pages` into `dev`; only owner promotes dev to main. Source baseline dev `ae231ee`. Review findings: PR154 discussion4457357231 and PR142 discussion4457543895, discussion4450929584, discussion4450929591.

One writer `codex-rsi-four-fixes` owns this corrective Task and its source/tests/docs. Preserve TK-002 claimant `ams-records-site` and all prior receipts. Initial inventory: clean retained S-007 checkout, behind published branch, no overlapping dirt; existing PR162 merged. No redesign, new campaign, grader changes, invented scores or Human QA. Record only attributable observed failures; tier unknown without reliable evidence. Hand back exact candidate, checks and publication limits to S-007.

## Acceptance

- [x] Candidate bars retain contrasting interior and double border in both themes.
- [x] Freshness-only changes keep the review hash; actual evidence changes alter it.
- [x] Different graders produce separate series with visible provenance, never pooled counts or cross-grader regression.
- [x] Stopped/failed runs without rows remain visible with source and stop/failure evidence; no invented task, split, count or score; test runs hidden.
- [ ] Build, focused regression tests and required checks pass; actual failures and limits recorded.

Workspace baseline sha256:eb5a7cca4ddbafa39d4daab2c03211289a0e85911273e2d00cfa6bca80b5562a

## Check and QA checkpoint

Focused red: four new render tests failed for timestamp hashing, both grader cases and absent run-only evidence; Chrome reproduced identical candidate/baseline fills. Green: build and 266 site tests pass, including 20 reader/repair tests. Browser actual CSS passes contrasting candidate interior and double border in light/manual-dark/system-dark with a planted solid-fill negative control. Run-only source fixtures visible at 375/1280 in both themes without overflow or invented points. No live database/model calls or owner QA. Python suite and fresh-candidate verification pending.

[Failure evidence and attribution limits](../../../../../../feedback/REPORT-s007-four-fixes-2026-11-04.md): historical skill/model tier unknown; current harness Codex, exact model/tier unknown. Canonical log has an active PR164 writer; this report preserves evidence without overwriting that log.
