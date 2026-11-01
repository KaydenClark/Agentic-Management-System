# Review receipt: S-006 repo-only half at `d6d4a6d` (fresh review)

- **Spec:** [S-006 RSI data store](../../landmarks/LMK-002-rsi-presentation/specs/S-006-rsi-data-store/SPEC.md)
- **Candidate:** `d6d4a6d65cc6287b667fe78ee5db937440972a5e` (`main` after PR #55). From the code reviewed at `a4470a4`, it changes records only.
- **Reviewer:** orchestrator C, a Claude cloud session. C did not build S-006 and holds no Supabase key. B's local reviewer covers the live-database half.
- **Verdict:** **pass** for the repository half, recorded with `spec-workbench.mjs verdict`. It replaces the fail at `c87bf4e` ([receipt](REVIEW-S-006-c87bf4e.md)).

## Method and evidence

- `uv run pytest` at the candidate: 339 passed, 3 skipped.
- Each test named in [TK-000B's proof table](../../landmarks/LMK-002-rsi-presentation/specs/S-006-rsi-data-store/tasks/TK-000B/TASK.md#proof) exists at the candidate. Those 18 tests run as 53 cases, and all pass.
- C read the new migration `20261101144510_rsi_strength_and_pass_rules.sql` and the `check_source` and `rsi_rows` changes.

## Earlier findings

| Earlier finding (`c87bf4e`) | Now |
|---|---|
| No acceptance line linked evidence | Fixed. All 8 lines are checked, and each links the TK-000B proof table, which names tests and live results per line. |
| No repeatable secret hygiene check | Fixed. `tests/test_secret_scan.py` scans the tracked files and full history. The one commit it allows (`75d1fad`) holds a test fake whose payload is only `{"role":"service_role"}`, with no issuer, project or expiry. C decoded it without printing the value. |
| `recorded_fact` was accepted on the trial tables | Fixed in both the writer (`check_source(table=...)`) and the database (`*_trial_strength` constraints). |
| A hand-typed build-history row was not detectable | Fixed. `readcheck` reports extra rows (`test_readcheck_fails_on_a_hand_typed_row_no_record_derives`). |

## Notes, not blocking

- The legacy-JWT key path is proven with fakes only, because the project has no legacy key. TK-000B states this.
- Every line links the same proof anchor rather than its own row. That is acceptable, because the table has one row per criterion.
- The verdict row brings the Spec to 8,183 of 8,000 characters, so it returns to B to prune (ADR-002V).
