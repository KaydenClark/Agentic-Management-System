# TK-000D - rsi_runs and rsi_results accept strength recorded_fact in both check_source and the ams_strength domain, though the Spec reserves recorded_fact for build history read from records. Restrict the trial tables to the four trial labels, or state in the Spec why recorded_fact is allowed there

**Task ID:** TK-000D
**Spec ID:** S-006
**Slice:** rsi_runs and rsi_results accept strength recorded_fact in both check_source and the ams_strength domain, though the Spec reserves recorded_fact for build history read from records. Restrict the trial tables to the four trial labels, or state in the Spec why recorded_fact is allowed there
**Status:** done
**Blockers:** none
**Destination:** spec-acceptance: S-006 Acceptance Criteria
**Planned verification:** Answers evidence row 7 (fail verdict at c87bf4ec86206bd5f734af7b828c81c3d3356a00 on 2026-11-01): rsi_runs and rsi_results accept strength recorded_fact in both check_source and the ams_strength domain, though the Spec reserves recorded_fact for build history read from records. Restrict the trial tables to the four trial labels, or state in the Spec why recorded_fact is allowed there
**Claimed by:** orch-b
**Current claimant:** orch-b
**Proof:** TK-000E, a4470a4: test_recorded_fact_is_for_build_history_only; DB check 20261101144510

## Receipt

| Run | Branch | HEAD SHA | Upstream | Dirty | Tests | Docs touched | Remaining gap | Checksum |
|---|---|---|---|---|---|---|---|---|
| 1 | feat/s006-tk000bcd | 76065ed7d6e5ca3b74103fe2a6634f974268f421 | ahead 0 behind 0 | 0 | TK-000E, a4470a4: test_recorded_fact_is_for_build_history_only; DB check 20261101144510 | Spec | none; close attribution: {"agent":"orch-b","claimant":"orch-b","onBehalfOf":null} | 3755b33fb9bc775ce8709a7c36634d50136cd962673103a3fc3e742130e163bf |
