# TK-002 - Spec lifecycle, idea-to-delivered and review-and-return diagrams under the same test

**Task ID:** TK-002
**Spec ID:** S-010
**Slice:** Spec lifecycle, idea-to-delivered and review-and-return diagrams under the same test
**Status:** done
**Blockers:** TK-001
**Destination:** spec-acceptance: S-010 Acceptance Criteria
**Claimed by:** codex-governance-charts
**Current claimant:** codex-governance-charts
**Proof:** Source b6a8ad9cc7005dc1bf3823114fe2e4558011f3c3: site build and 285 tests passed; full browser suite 2510/2510 including six governance contrast cases and planted low-contrast fault; 8 cases at 375/1440, light/dark, JS/noJS passed; missing and unknown states/edges rejected. Shared Python and site CI passed on source; local pytest 841 passed, 5 skipped while chart edits were underway.

Workspace baseline sha256:346b7e069c0bbb9b9bfbcdd58973c1f6914d5a0223d64fa6743335b7efaffd54

## Acceptance

- [x] A reader can follow the Spec's accepted states and the current tools' actual status transitions.
- [x] The idea-to-delivery and review-return diagrams show decisions, corrective returns, owner approval and the separate permission to deliver.
- [x] Drift checks reject unknown and missing states and arrows; source fingerprints require reinspection when the audited runtime or workflow sources change.
- [x] The diagrams are readable at 375 px and desktop in both themes, with and without JavaScript; actual checks and remaining limits are recorded in the Receipt.

## Receipt

| Run | Branch | HEAD SHA | Upstream | Dirty | Tests | Docs touched | Remaining gap | Checksum |
|---|---|---|---|---|---|---|---|---|
| 1 | Feature/S-010-governance-flow-charts | b6a8ad9cc7005dc1bf3823114fe2e4558011f3c3 | ahead 0 behind 0 | 1 | Source candidate b6a8ad9cc7005dc1bf3823114fe2e4558011f3c3: site build and 285 tests passed; unchanged full browser suite passed 2510 checks including six governance contrast checks and a planted low-contrast fault; eight browser cases passed 375/1440 light/dark with and without JS; planted missing/unknown stages and arrows failed as intended. Python suite passed 841, skipped 5 while chart edits were underway; exact-head CI remains required. | Spec lifecycle, idea-to-delivery and review-return diagrams; source-bound drift checks; corrected arrow relation. | S-008 found inherited symbol-only arrows caused undecided contrast; corrected and rerun. Initial repair edit used a wrong working-directory path and changed nothing; corrected. Spec and process transitions are manually audited with source fingerprints, not dynamically replayed. Snapshot excludes generated ignored caches; workspace recovery remains unverified. Remaining S-010 diagrams, independent Review and Human QA remain open. | e4b4a2a5c0d6bcc90c01067b97cfcf1c326883515f77ae7f0016e166827004d7 |
| 2 | Feature/S-010-governance-flow-charts | cd8c0cd581229d0f105c3f4df8793cd1ca8d2184 | ahead 0 behind 0 | 0 | Source b6a8ad9cc7005dc1bf3823114fe2e4558011f3c3: site build and 285 tests passed; full browser suite 2510/2510 including six governance contrast cases and planted low-contrast fault; 8 cases at 375/1440, light/dark, JS/noJS passed; missing and unknown states/edges rejected. Shared Python and site CI passed on source; local pytest 841 passed, 5 skipped while chart edits were underway. | Spec lifecycle, workflow and review-return diagrams; S-008 contrast correction; source-bound drift checks. | Remaining S-010 governance and process charts, inventory, independent Review and owner Human QA remain. Transition maps are manually audited with fingerprints, not runtime replay. Snapshot omits generated ignored caches and workspace recovery remains unverified. S-008 contrast failure and initial wrong-path repair attempt remain recorded in the prior Receipt and feedback intake.; close attribution: {"agent":"codex-governance-charts","claimant":"codex-governance-charts","onBehalfOf":null} | 9d4690e3da9ccd20f4d8aab7fd7d6b93989449a50f15cb804e250c5cd428b492 |
