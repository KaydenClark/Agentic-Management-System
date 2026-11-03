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

- [x] A resolved reference alone never certifies behavioral acceptance; meaningful reference resolution is still reported.
- [x] Unrelated existing-file and ancestor-only citation cases cannot falsely establish acceptance.
- [x] Unchecked, missing and unmerged evidence remains truthfully reported.
- [x] Deterministic replay shows before/after and recurrence; focused tests and scoped QA record actual results and limitations.

## Check and QA

Source `7735c553bbe2cde0e5c5d6a26a56e7468773961b` is contained in assembly merge `e882efe9d905f074a0b36bff8976e49da03cc028`. The implementor reported 33 focused passes and deterministic before/after replay, including unrelated-file recurrence, ancestor-only, missing, unmerged and unchecked controls. A fresh context exercised S-001 and S-003; root inspected the bounded diff and accepted its conservative behavior for assembly. See the [safe report](../../../../../../feedback/coherence/CHECKER-REPAIR-2026-11-02.md) for hashes, observations and limits. Full source suite: 809 passed, 5 skipped, one inherited AGENTS-size failure; later recovery hygiene passed. Final assembly checks, independent Review and owner Human QA remain open. This closes only this checker slice, not S-013 or the learning cycle.
