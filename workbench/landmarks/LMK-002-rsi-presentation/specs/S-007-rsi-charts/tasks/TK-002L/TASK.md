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
- [x] Build, focused regression tests and required checks pass; actual failures and limits recorded.

Workspace baseline sha256:eb5a7cca4ddbafa39d4daab2c03211289a0e85911273e2d00cfa6bca80b5562a

## Check and QA checkpoint

Focused red: four new render tests failed for timestamp hashing, both grader cases and absent run-only evidence; Chrome reproduced identical candidate/baseline fills. Green: build and 266 site tests pass, including 20 reader/repair tests. Browser actual CSS passes contrasting candidate interior and double border in light/manual-dark/system-dark with a planted solid-fill negative control. Run-only source fixtures visible at 375/1280 in both themes without overflow or invented points. No live database/model calls or owner QA. Python suite and fresh-candidate verification pending.

[Failure evidence and attribution limits](../../../../../../feedback/REPORT-s007-four-fixes-2026-11-04.md): historical skill/model tier unknown; current harness Codex, exact model/tier unknown. PR164 merged during this run; its accepted canonical log is preserved with appended FAIL-035 through FAIL-051. Earlier IDs remain intact.

## Final local verification and delivery boundary

Fresh checkout at5cc0cdf: build and266/266 site tests passed; full Python811 passed/4 skipped (200.79s). Product bytes equal4e3aa13. Root and built-site hygiene0; Wiki, decisions, layout, render and whitespace checks pass. Doctor retains pre-existing unrelated attention/slice findings. Browser checks and screenshots are fixture-only, not a deployed readback. React server-component review: stable row keys, no new client state/effects, no extra fetches.

Public push was denied by automatic approval review: explicit publication approval is required. Remote feature tip remains7af73e7 (claim only); product/verification commits are local. No PR, shared CI, dev merge, deployment, owner QA or production promotion is claimed. Native close is not attempted while required delivery is blocked.

Initial preservation gap: baseline recorded dirty generated Taskboard, so the original-commit-before-snapshot sequence was incomplete. Exact original bytes have a verified independent local copy. No chronology is reconstructed. Native accounting remains incomplete because the feature ref is unpushed; ignored local test caches/evidence also remain local. Preserve this checkout, its commits and local recovery until publication is authorized.

## Receipt

| Run | Branch | HEAD SHA | Upstream | Dirty | Tests | Docs touched | Remaining gap | Checksum |
|---|---|---|---|---|---|---|---|---|
| 1 | Feature/S-007-rsi-chart-pages | 5cc0cdf5b020991b0cc889b9b9ca8331db82cbc7 | ahead 3 behind 0 | 3 | Fresh5cc0cdf: build;266 site tests;811 Python passed/4 skipped. Product tree matches4e3aa13. Chrome contrast and375/1280 run-only fixtures pass. Root/build hygiene0; Wiki/layout/decisions/render/diff checks pass. | site README; owner intent; TK-002L; accepted main failure log plus FAIL-034 through FAIL-050 and supporting report. | Public push denied; explicit push/PR/checked-dev-merge approval pending. No PR/CI/deploy/QA. Native preservation incomplete: unpushed ref, local test caches, missed pre-snapshot original Taskboard commit; exact original bytes preserved locally. | e1294657a58e1abb4b1940c85100d50879531db3933affaae56b69f380774383 |

## Publication approval resumed

Owner,2026-11-04: approved merging into dev and main for the things belonging in each, after the explicit public-publication request. Scope: checked website PR into dev; records-only PR into main. This releases the earlier public-push blocker without granting Human QA or broad website promotion. Remote dev remainsae231ee and feature7af73e7; no overlapping site work found. Another published writer used FAIL-034, so these entries move to unused FAIL-035 through FAIL-051. Existing FAIL-034 is preserved on its owner branch.

## Checked publication candidate

Published2e842724de126391cb3c4ed0e59524dedcc9caaf is current with devae231ee. Both exact-head shared CI jobs passed: site41790083913 (build, tests, public hygiene) and Python41790084156 (suite, hygiene, records and375px Board). PR165 targets dev; PR166 carries only failure records to main. Local source product bytes still equal fully checked4e3aa13. No unresolved new review threads observed; independent Review and Human QA are not claimed. Close records change no site source; exact final-head CI is required before merge.

Receipt recovery: native close refused after the failure-ID reconciliation changed historical receipt text. Restored row1 byte-for-byte from original6bd979c, keeping its original checksum and original IDs. Current IDs are explained outside the immutable receipt; no hash was recomputed. Failure FAIL-053 records the invocation and recovery.
