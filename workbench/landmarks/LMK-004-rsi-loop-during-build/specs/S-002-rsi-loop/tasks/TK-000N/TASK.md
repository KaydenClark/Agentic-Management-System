# TK-000N - A retained historical finding can acquire its missing mapping and pass an explicit repaired-revision retest

**Task ID:** TK-000N
**Spec ID:** S-002
**Slice:** A retained historical finding can acquire its missing mapping and pass an explicit repaired-revision retest
**Status:** done
**Blockers:** none
**Destination:** spec-acceptance: Cycle; Stops (historical finding recovery)
**Planned verification:** Red/green CLI record/readback case, refusal of conflicting remaps, no resolution by enrichment alone; full suite and room checks.
**Claimed by:** codex-s002
**Current claimant:** codex-s002
**Proof:** 40 focused; fresh 431/4 skip; CI #32 pass

## Assignment

Same authorized S-002 delivery. One writer: codex-s002; branch `codex/s002-assessment-loop`, target `main`, PR #78. Automated review of `be5db734aae27c57fd8bd475ebf090ceb79ffd14` found a recovery miss after TK-000M closed: [finding 4436853780](https://github.com/KaydenClark/Agentic-Management-System/pull/78#discussion_r4436853780). Preserve TK-000M's proof and this corrective history rather than manually reopening its native state.

Allow only validated enrichment of missing historical check/class mappings. Preserve stable identity, original observation/revision, failures, prior packets and normal three-run retest requirements. Reject changes to already recorded mappings, and apply original r1 class compatibility after merging supplied/missing fields. Enrichment alone never closes a finding. Do not change storage, trials, paid-service scope or the rubric.

## Acceptance

- [x] A baseline's unmapped historical finding can receive a valid mapping in a later candidate and resolve only through its repaired-revision, original/affected-regression qualified three-run retest.
- [x] Existing mappings and original source/observation fields cannot be overwritten; malformed or demoting mappings fail before any record write.
- [x] Enrichment without a retest retains the open finding; old immutable packets/readback and attempt limits remain valid.
- [x] Focused/full checks pass; independent corrective review and final-head CI are recorded before merging PR #78.

## Corrective Check and QA

Candidate `4e111c97d3e1aa06c6ff12b88a5ab49371ed4ea4`: 40 focused tests pass. Independent Spec reviewer repeated all 40; both fresh-context reviewers report no remaining corrective findings. The first recovery case and malformed partial-class case each failed for the expected reason before the fix, then passed. Fresh-clone full suite: 431 passed, 4 skipped; render leaves no diff. Room/ADR/layout/diff checks pass; doctor retains its two original nonblocking setup findings.

Records preserve baseline and prior packets, reject source/remapping changes before writing, and keep enrichment open without a retest. The automated PR finding is resolved after repair and independent verification. Final-head CI gates merge; no S-006 storage or model trials are claimed. Closed TK-000M proof remains historical, supplemented by this correction.

CI workflow `41337850971` (run #32) passed at `4e111c9`, including the browser/records checks. Final closure changes only owner records; final-head CI will be verified on PR #78 before merge.

## Receipt

| Run | Branch | HEAD SHA | Upstream | Dirty | Tests | Docs touched | Remaining gap | Checksum |
|---|---|---|---|---|---|---|---|---|
| 1 | codex/s002-assessment-loop | 5ec9fd3041f0ede1585e825db1fa8095f19dd54f | ahead 0 behind 0 | 0 | 40 focused; fresh 431/4 skip; CI #32 pass | evals | S-006/trials; close attribution: {"agent":"codex-s002","claimant":"codex-s002","onBehalfOf":null} | 011bf1a471bfe9520c4233bb833f38fdb6c7b4e94fbec755b8dd4fbc681c61d2 |

Final PR review found a separate historical-ID/current-Regression collision at `d8fc717`; [TK-000O](../TK-000O/TASK.md) owns the correction before delivery. Prior proof remains historical.
