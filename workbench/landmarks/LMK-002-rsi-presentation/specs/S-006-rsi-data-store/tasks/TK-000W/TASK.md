# TK-000W - Historical source declarations exclude multiline inline code

**Task ID:** TK-000W
**Spec ID:** S-006
**Slice:** Historical source declarations exclude multiline inline code
**Status:** in-progress
**Blockers:** none
**Destination:** spec-acceptance: Build history from real records
**Planned verification:** Red-first public collector/readcheck article and router fixtures, exact delimiter/escape/unmatched cases, plain declaration retention, focused/full/fresh/room/CI and independent corrected-source review.
**Claimed by:** codex-history-consumer
**Current claimant:** codex-history-consumer

## Assignment

Parent assigned this bounded correction within the approved S-006 historical-consumer outcome after PR #91 finding4437461401. At exact source28d43cf, the public record reader derives8 archive events from a valid multiline inline-code example in either the article or MEMORY router (expected0). Matching source_paths and real ancestor blobs do not make an example a declaration. The line-by-line inline-code substitution loses multiline span state. Primary synthetic proof contains valid paragraph-scoped examples, no DB/credentials/model calls.

Preserve closed TK-000U receipt and its historical source-specific reviews. On the same feature branch and isolated worktree, repair only visibility parsing and causal tests/docs/this owner/projection. Track exact matching backtick delimiters across eligible paragraph lines, retaining literal shorter runs and proper escaped/unmatched behavior; preserve actual declarations and existing comment/fence controls. Audit article/router callers for this same cause. No broad Markdown framework, Wiki source rewrite, table restoration, blanket row ignores/deletes, schema/scorer changes, primary checkout edits or live calls before merge. CommonMark0.31.2 code spans and block precedence provide the primary syntax source. Main17293a0 prerequisite is already merged.

After corrected immutable source and final record binding pass independent review/full/fresh/CI, merge PR #91 normally. Same authorized run continues through live import/readcheck, durable Spec proof only on actual pass and checked owner followup. Keep actual failed6e history check, superseded U source review scope, and formal owner HumanQA gate. Do not alter the immutable U receipt or claim whole-Spec acceptance from this correction.

## Acceptance

- [ ] Valid multiline inline-code examples in article or router authorize0 archive events; readcheck still flags their8 retained rows as extra rather than waiving comparison.
- [ ] Exact delimiter lengths, interior literal backticks, escaped/unmatched cases and paragraph boundaries preserve ordinary declarations; actual8 source events still derive exactly once. Existing route/security refusals remain.
- [ ] Focused/full/fresh/room/CI and independent corrected-source review pass; preserve prior evidence and name live/owner gates truthfully.

## Stopped: unaccepted recovery

The parent stopped this repair under the room three-strike rule. Task W remains in-progress and unaccepted; its acceptance boxes are not checked. No further source correction, merge or live import is authorized in this stopped run.

- Failed corrected pin `813465decdac6fceff63ade2e42b74c8e69e4fba`: an indented paragraph continuation flushed an existing inline-code span, exposing8 code-only events in article/router. Independent review found the cause. Focused126 passed; full/fresh631passed/4skipped did not cover it and did not clear that failure.
- Corrected pin `5e02eadec8aaaf5476d916a98dc88035022a7ea6`: indentation/link escaping corrections passed154 focused tests and a scoped independent source review, but the implementor's subsequent public-reader audit proved generic list detection still exposes8 events from each code example. Ordered marker2, an empty bullet and a10-digit marker cannot interrupt the existing paragraph. Both callers fail; six causal cases derive8 instead of0. Earlier source-specific PASS reports remain historical and are superseded for merge readiness.
- Latest causal list tests:6 failed/6 passed/69 deselected. Their20 new lines are committed only as unaccepted recovery; no list-interruption source fix has been applied. Other confirmed new causes and prior U receipt are preserved. A no-op unchanged-input fixture commit error was separately corrected; irrelevant environment representations were removed from its private diagnostics, never committed.

Smallest proposed correction, not implemented: distinguish valid new list blocks from paragraph continuation. Only nonempty valid bullets or an ordered start of1 (at most9 digits) may interrupt an open paragraph; preserve actual list starts and literal code state. Parent is investigating the recurring parsing approach before deciding the next bounded step. No broad renderer/dependency is introduced here.

Main10c57ba is reconciled in the feature branch. This incomplete PR remains draft and unmerged. Full/fresh verification of a successful final corrected source, current accepted CI, actual import/readcheck, durable Spec proof, assembled review and owner HumanQA remain gates. No credentials/model calls/DB actions occurred. Build-history acceptance stays unchecked; no row is deleted, ignored or restored to a destination Spec. The source remains held pending parent diagnosis/disposition.

## Receipt

| Run | Branch | HEAD SHA | Upstream | Dirty | Tests | Docs touched | Remaining gap | Checksum |
|---|---|---|---|---|---|---|---|---|
| 1 | feature/s006-wiki-history-source | 5e02eadec8aaaf5476d916a98dc88035022a7ea6 | ahead 0 behind 0 | 2 | Stopped unaccepted:813465d failed independent indentation case;5e02ead failed public list-continuation audit. Latest causal tests6failed6passed69deselected; source fix not applied. Earlier154focus and scopedPASS insufficient; old813full/fresh631pass4skip historical only. | TaskW stopped checkpoint and causal list regression tests; closed U receipt unchanged | Room three-strike stop; parent diagnosis/disposition pending. PR91 must not merge; no live import. Build-history criterion and ownerHumanQA remain open. | 432a3df6213ed559d7be91090d0d60597e708936bcba06300bf98ca9dfb94132 |
