# TK-000B - Every S-006 acceptance line is unchecked and links no evidence at c87bf4e (ADR-001F). Check each line that is met and link its receipt, test or migration evidence on the line itself, then request a fresh review

**Task ID:** TK-000B
**Spec ID:** S-006
**Slice:** Every S-006 acceptance line is unchecked and links no evidence at c87bf4e (ADR-001F). Check each line that is met and link its receipt, test or migration evidence on the line itself, then request a fresh review
**Status:** done
**Blockers:** none
**Destination:** spec-acceptance: S-006 Acceptance Criteria
**Planned verification:** Answers evidence row 7 (fail verdict at c87bf4ec86206bd5f734af7b828c81c3d3356a00 on 2026-11-01): Every S-006 acceptance line is unchecked and links no evidence at c87bf4e (ADR-001F). Check each line that is met and link its receipt, test or migration evidence on the line itself, then request a fresh review
**Claimed by:** orch-b
**Current claimant:** orch-b
**Proof:** 8 lines checked, proof in TK-000B at a4470a4

## Proof

Each S-006 acceptance line links here. Candidate: main `a4470a4`. The live commands ran from orchestrator B's checkout at that commit, and none printed a key. Every test name below is in `tests/` and passes in `uv run pytest` (339 passed, 3 skipped).

| Criterion | Tests | Live at a4470a4 |
|---|---|---|
| Schema and provenance | `test_result_without_skills_commit_is_refused_and_nothing_is_sent`, `test_migration_requires_the_provenance_and_hides_test_rows` ([TK-003](../TK-003/TASK.md)) | `ams-rsi livecheck`: missing skills_commit refused by the writer and the database (23502) |
| No client writes | `test_migration_grants_no_client_write`, `test_readcheck_reads_with_publishable_key_and_all_writes_refused`, `test_migration_grants_clients_select_only_and_hides_test_rows` | `ams-writer readcheck 884d021`: build_events insert, update and delete each refused (401), row unchanged; `ams-rsi livecheck`: the same three writes refused (401) on rsi_runs and rsi_results; selects return 200 |
| Writer works end to end | `test_record_merge_posts_with_service_key_and_prints_no_key` ([TK-002](../TK-002/TASK.md)) | `ams-writer readcheck 884d021`: the site key reads the merge row `ams-writer` wrote for PR #15 (id 1), select 200 |
| Conflict refusal | `test_an_update_against_a_row_changed_since_it_was_read_is_refused`, `test_a_database_version_refusal_is_a_conflict` | `ams-rsi livecheck`: stale update refused by the writer and the database (409 PT409); row unchanged |
| Real sources only | `test_a_row_without_a_source_or_with_an_unlisted_strength_is_refused`, `test_recorded_fact_is_for_build_history_only` ([TK-005](../TK-005/TASK.md), [TK-000E](../TK-000E/TASK.md)) | `ams-sources livecheck`: writer and database refused no source, a blank ref and an unlisted strength on all 3 tables, and `recorded_fact` on the RSI tables; the site key saw 0 test rows. No seed row exists yet; S-002 writes them under these rules |
| Key loads and authenticates | `test_format_is_recognized`, `test_key_goes_in_apikey_header_of_rest_root`, `test_no_path_leaks_the_key` (both `sb_secret_` and legacy-JWT fakes) ([TK-001](../TK-001/TASK.md)) | `ams-keycheck`: loaded yes, format sb_secret, authenticated yes. The project has no legacy key, so the legacy path is proven with fakes only |
| Build history from real records | `test_import_twice_adds_no_rows`, `test_readcheck_fails_on_a_hand_typed_row_no_record_derives` ([TK-004](../TK-004/TASK.md), [TK-000E](../TK-000E/TASK.md)) | `ams-history readcheck`: rows 632, missing 0, extra 0, unsourced 0; a second `ams-history import` inserted 0 |
| No secrets in Git | `test_no_tracked_file_holds_a_service_key`, `test_no_commit_in_history_holds_a_service_key`, `test_the_scan_fails_on_a_planted_fake` ([TK-000C](../TK-000C/TASK.md)) | The suite above |

## Receipt

| Run | Branch | HEAD SHA | Upstream | Dirty | Tests | Docs touched | Remaining gap | Checksum |
|---|---|---|---|---|---|---|---|---|
| 1 | feat/s006-tk000bcd | 6ce47a5df6a481dc76d3b9f7f3f4116f8a088698 | ahead 0 behind 0 | 0 | 8 lines checked, proof in TK-000B at a4470a4 | Spec | Fresh review; close attribution: {"agent":"orch-b","claimant":"orch-b","onBehalfOf":null} | 9acd540e939810fc873c1f1bd6a58b177cfc12ae7c3b0701ef522b774b6dcc9a |
