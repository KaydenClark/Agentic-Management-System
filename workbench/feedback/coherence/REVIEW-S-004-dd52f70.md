# Review receipt: S-004 at `dd52f70`

- **Spec:** [S-004 Grill Board cards](../../landmarks/LMK-001-grill-board/specs/S-004-grill-board-cards/SPEC.md)
- **Candidate:** `dd52f705004aac5599a17935935d6fbc6d0a511c`. The S-004 code and records are byte-identical at `a03d739`.
- **Reviewer:** orchestrator C (Claude cloud session, no secrets, did not build S-004), plus one fresh-context read-only subagent. C reproduced every high and medium finding itself.
- **Verdict:** **fail**, recorded with `spec-workbench.mjs verdict`. It opened corrective Tasks TK-000F to TK-000J. A changed commit needs a fresh review.

## Method

- `uv run pytest` at the candidate: 321 passed, 3 skipped.
- `uv run ams-board` was run live in a throwaway clone on a branch.
- The board was driven with same-origin POSTs and with cross-origin POSTs.
- The board's own refusal messages were read for every refused write.

## Per criterion

| Criterion | Result | Evidence |
|---|---|---|
| Signals on every card | holds, but the line links no evidence | `cards.py` refuses a blank reason. Tests: `test_a_graded_card_without_a_reason_is_refused_never_rendered` and `test_every_fixture_card_renders_with_both_grades_and_reasons` |
| Answer lands in its owner | holds, with a defect (TK-000G) | Live: Confirm made one commit touching the card plus the owner record, with no second step. Defect: any tracked file is accepted as the owner. C committed a card's text into `.github/workflows/site-build.yml` with one click. |
| Conflict refusal | holds | Live: a stale `record_sha` and a stale `card_sha` each returned 409 with 0 commits. Writes run under a `flock` with an `update-ref` compare-and-swap. |
| Rating and flag | partly (TK-000H) | Live: rating 9 was refused, rating 4 was committed, and the flag was committed. An identical re-ask is refused, and whitespace or case changes are refused too. A punctuation change (`taxing ?`) passed. The subagent found that a zero-width character also passes. |
| Not a drafting surface | fails (TK-000I) | There is no edit route. However, a card titled "Page draft: About us" with a page body and valid headers is shown as a normal card. |
| Colors mean one thing | holds by test, with notes | `test_no_color_carries_two_meanings_within_a_theme` passes. Two meanings are compound: `--line-strong` and `--agent`, where `h-agent` tints both the Confirm button and the agent box. |
| Local only | holds | Live: listens on 127.0.0.1 only and is unreachable on the container IP. Cross-origin POSTs get 403. One documented command. No Vercel route. |
| Looks like the artifact | partly (TK-000J) | Served tokens equal `tokens.json` (test). Fonts are self-hosted, with no third-party URL (live). The `qa/` shots date from `83747aa`, before the rating and flag controls were added. The 375px layout is untested. |
| Every line | fails (TK-000F) | No line is checked or links evidence (ADR-001F). |

## Notes, not blocking

- B's request described "a single repo-wide writer lock". The code locks per checkout (`--absolute-git-dir`), and its docstring says exactly that.
- An editor that does not take the lock can still change a file between the check and the write (inferred, not reproduced).
- The Spec was 7,986 of 8,000 characters. The verdict row brings it to 9,131, so it returns to B to prune (ADR-002V).
