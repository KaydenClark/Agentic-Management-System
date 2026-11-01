# TK-000N - A retained historical finding can acquire its missing mapping and pass an explicit repaired-revision retest

**Task ID:** TK-000N
**Spec ID:** S-002
**Slice:** A retained historical finding can acquire its missing mapping and pass an explicit repaired-revision retest
**Status:** ready
**Blockers:** none
**Destination:** spec-acceptance: Cycle; Stops (historical finding recovery)
**Planned verification:** Red/green CLI record/readback case, refusal of conflicting remaps, no resolution by enrichment alone; full suite and room checks.

## Assignment

Same authorized S-002 delivery. One writer: codex-s002; branch `codex/s002-assessment-loop`, target `main`, PR #78. Automated review of `be5db734aae27c57fd8bd475ebf090ceb79ffd14` found a recovery miss after TK-000M closed: [finding 4436853780](https://github.com/KaydenClark/Agentic-Management-System/pull/78#discussion_r4436853780). Preserve TK-000M's proof and this corrective history rather than manually reopening its native state.

Allow only validated enrichment of missing historical check/class mappings. Preserve stable identity, original observation/revision, failures, prior packets and normal three-run retest requirements. Reject changes to already recorded mappings, and apply original r1 class compatibility after merging supplied/missing fields. Enrichment alone never closes a finding. Do not change storage, trials, paid-service scope or the rubric.

## Acceptance

- [ ] A baseline's unmapped historical finding can receive a valid mapping in a later candidate and resolve only through its repaired-revision, original/affected-regression qualified three-run retest.
- [ ] Existing mappings and original source/observation fields cannot be overwritten; malformed or demoting mappings fail before any record write.
- [ ] Enrichment without a retest retains the open finding; old immutable packets/readback and attempt limits remain valid.
- [ ] Focused/full checks pass; independent corrective review and final-head CI are recorded before merging PR #78.
