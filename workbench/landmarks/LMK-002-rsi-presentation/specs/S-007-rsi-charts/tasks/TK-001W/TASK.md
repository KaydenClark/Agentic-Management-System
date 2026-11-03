# TK-001W - A reader can inspect the checker repair evidence on RSI

**Task ID:** TK-001W
**Spec ID:** S-007
**Slice:** Show one safe, source-linked checker repair on the existing RSI page
**Status:** in-progress
**Blockers:** none
**Destination:** spec-acceptance: Feedback loop connection
**Planned verification:** Focused renderer test, site build and browser inspection against the committed evidence and candidate.
**Claimed by:** luna-site
**Current claimant:** luna-site

## Assignment

Owner direction, 2026-11-02: demonstrate one bounded repair and its evidence on dev. The checker candidate `7735c553bbe2cde0e5c5d6a26a56e7468773961b` changes checked criteria from false `met` to `unknown`, retaining resolved references. [PR 140](https://github.com/KaydenClark/Agentic-Management-System/pull/140) records the original failure, focused results and replay; its full suite and assembled verification remain pending. The record writer released the proof blocker for implementation using [safe evidence](../../../../../../feedback/coherence/CHECKER-REPAIR-2026-11-02.md) at `e8450d2`; full source and assembled checks remain final merge gates. Do not treat this planned record or the draft PR as proof of acceptance.

Use the existing `/rsi` repair evidence path to present the safe committed finding, repair, before/after and recurrence with sources and limits. Preserve the live-data work in TK-001F; this slice does not require live Supabase. One implementor owns the site evidence and tests; the shared record writer owns Task state. No deployment or owner promotion is implied.

## Acceptance

- [x] The page shows the false-met case, the repair, actual before/after and recurrence, exact source and candidate, disposition and limits.
- [x] Unrun or unavailable checks remain explicit; no audit score, behavioral benefit, owner QA or completed learning cycle is inferred.
- [x] A focused renderer regression, site build and browser inspection exercise the actual page and record results.
- [x] Hand-back identifies the exact candidate, commands, observations and remaining gaps.

## Check and QA

Site source `77ed4478ee8294f3f4cbd38e270c1514245ed170` is contained in recovery assembly merge `1b07f1e72cc4419ad017af3fe0f76fc7f1e8fc9e`. The implementor reported site build and 209 tests passing, including 10 focused checks, and inspected desktop. The root inspected the actual build at 375px: document width 360px; checker panel x=16px, width 328px, right edge 344px; text and links were readable without clipping or horizontal overflow. Browser console showed a favicon 404 and stylesheet preload warnings. The report citation was corrected to the maintained immutable source; a prior page-hash link test failed and was repaired. [PR 141](https://github.com/KaydenClark/Agentic-Management-System/pull/141) records the source and check evidence. No owner Human QA, full assembled Review, deployment or learning-cycle acceptance is claimed.
