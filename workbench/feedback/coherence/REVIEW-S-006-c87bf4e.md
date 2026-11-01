# Review receipt: S-006 repo-only half at `c87bf4e`

- **Spec:** [S-006 RSI data store](../../landmarks/LMK-002-rsi-presentation/specs/S-006-rsi-data-store/SPEC.md)
- **Candidate:** `c87bf4ec86206bd5f734af7b828c81c3d3356a00` (`main` after PR #42), reviewed in a detached worktree.
- **Reviewer:** orchestrator C, a Claude cloud session. C did not build S-006 and holds no Supabase key.
- **Scope:** the repository half: schema and migrations, writer code and tests, the source and strength rule, client write refusal, and test-row hiding as written. The live-database half belongs to orchestrator B's local reviewer.
- **Verdict:** **fail**, recorded with `spec-workbench.mjs verdict`. It created corrective Tasks TK-000B, TK-000C and TK-000D. A changed commit needs a fresh review.

## Method and evidence

- At the candidate, `uv run pytest` gave 290 passed and 3 skipped. This was rerun by C, not taken from a report.
- C read all three migrations in full, plus `src/ams/source_rules.py` and the conflict paths in `writer.py`, `rsi_rows.py` and `build_history.py`.
- C ran a secret scan of the tree and full history at the candidate, looking for `sb_secret_…` and JWT-shaped values. It found 0 matches. `.gitignore` covers `.env` and `.env.*`.

## Acceptance lines: repository half

| Line | Repository evidence C observed | Repo-half result |
|---|---|---|
| Schema and provenance | `rsi_results` and `rsi_runs` hold every named field as `not null`. Commits are 40-hex domains. A composite foreign key keeps each result's provenance equal to its run's. Test: `test_migration_requires_the_provenance_and_hides_test_rows`. | Supported, but the line links no evidence |
| No client writes | The baseline revokes client insert, update, delete and truncate, including default privileges. Each table does `revoke all` and then grants `select` only. RLS has only `for select` policies. Test: `test_migration_grants_clients_select_only_and_hides_test_rows`. | Supported as written, but the line links no evidence. Live proof is B's half. |
| Writer works end to end | Live only | B's half |
| Conflict refusal | The `ams_guard_version` trigger raises `PT409` unless the update claims version+1. `rsi_rows.Conflict` maps the 409. Test: `test_a_database_version_refusal_is_a_conflict`. `build_events` is insert-only, with a unique source key and `ignore-duplicates` on import. | Supported, but the line links no evidence |
| Real sources only | `check_source` runs in every writer. The DB has the `ams_source_kind` and `ams_strength` domains and checks for a non-blank `source_ref`. Test: `test_every_site_table_requires_a_source_and_strength_and_hides_test_rows`. See finding 3. | Supported with finding 3 |
| Key loads and authenticates | Live only | B's half |
| Build history from real records | The unique key `(kind, source_kind, source_ref)` and `ignore-duplicates` prevent duplicate rows. `recorded_fact` is checked on each row. The row counts are live. | Partly B's half |
| No secrets in Git | C's scan found 0 matches. No repeatable hygiene check exists. | Fails: finding 2 |

Test rows are hidden because every site-read policy uses `using (not is_test)` (all three tables).

## Findings

| # | Severity | Finding | Disposition |
|---|---|---|---|
| 1 | blocking | All 8 acceptance lines are unchecked and none links its evidence. ADR-001F refuses a pass. | New Task TK-000B |
| 2 | blocking | "The hygiene check" named by No secrets in Git does not exist. TK-001 grepped only its own diff. | New Task TK-000C |
| 3 | low | `recorded_fact` is accepted on `rsi_runs` and `rsi_results` by both `check_source` and the domain, although the Spec reserves it for build history. | New Task TK-000D |
| 4 | process | The Spec was 7,989 of 8,000 characters before review. The verdict row puts it at 9,071. | Return to B to prune (ADR-002V) |
