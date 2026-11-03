# TK-001V - Evidence links do not certify behavioral acceptance

**Task ID:** TK-001V
**Spec ID:** S-013
**Slice:** Report evidence reference resolution without treating file existence as behavioral proof
**Status:** in-progress
**Blockers:** none
**Destination:** spec-acceptance: Up to Spec
**Planned verification:** Deterministic before/after replay, unrelated-file and ancestor-only cases, unchecked/missing/unmerged evidence cases and focused regression checks.
**Claimed by:** terra-checker
**Current claimant:** terra-checker

## Assignment

The owner authorized one bounded repair and visible evidence on dev, 2026-11-02. A checked criterion linking an existing file currently produces a false met result. One implementor repairs the existing up-to-Spec checker and its tests and replay fixture; the S-013 writer maintains this record. Preserve meaningful reference resolution while representing behavioral acceptance honestly. No semantic grader or paid evaluation is in scope. Return exact source revision, red/green evidence, recurrence observation and gaps for assembly and website presentation.

## Acceptance

- [ ] A resolved reference alone never certifies behavioral acceptance; meaningful reference resolution is still reported.
- [ ] Unrelated existing-file and ancestor-only citation cases cannot falsely establish acceptance.
- [ ] Unchecked, missing and unmerged evidence remains truthfully reported.
- [ ] Deterministic replay shows before/after and recurrence; focused tests and scoped QA record actual results and limitations.
