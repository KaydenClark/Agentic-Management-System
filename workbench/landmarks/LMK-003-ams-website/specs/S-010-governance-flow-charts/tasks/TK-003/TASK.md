# TK-003 - Governance stack page with worked examples

**Task ID:** TK-003
**Spec ID:** S-010
**Slice:** Governance stack page with worked examples
**Status:** in-progress
**Blockers:** none
**Destination:** spec-acceptance: S-010 Acceptance Criteria
**Claimed by:** codex-governance-charts
**Current claimant:** codex-governance-charts

Workspace baseline sha256:f320e58075d1dce44647fde8db74019b067578b6d5993eb905a6c8e215a7129f

## Receipt

| Run | Branch | HEAD SHA | Upstream | Dirty | Tests | Docs touched | Remaining gap | Checksum |
|---|---|---|---|---|---|---|---|---|
| 1 | Feature/S-010-governance-flow-charts | ee0e42ba6dfe49aa9c9d726b307ee9b7bb54995b | ahead 0 behind 0 | 1 | Source ee0e42ba6dfe49aa9c9d726b307ee9b7bb54995b: fresh build and 302 site tests passed; eight browser cases verified all six glossary links at 375/1440 in both themes with and without JavaScript. Final unmodified browser suite failed 4 of 2510 checks: start-toy no-request assertions observed navigation prefetch requests. Governance and glossary contrast checks and planted low-contrast negative passed. Earlier project pytest passed 867 with 5 skipped while source changed, so is mixed-source evidence. | Six governance claim roles, authority examples, both traversals and glossary backlinks. | Task remains in progress: diagnose and resolve the failed start-toy browser checks without weakening them. Earlier rendered-order detector failed on React whitespace, corrected with retained adverse checks. Independent Review, owner Human QA, Task004 and whole-Spec acceptance remain open. Snapshot recorded generated ignored cache names but omitted their bytes; workspace recovery remains unverified. | 2f20e69bffac88252cd796549ea59978516abda5ac5b8b58206720cb99b80601 |
| 2 | Feature/S-010-governance-flow-charts | b7f988feb62929bd250d915aa10a45600d5d2d8d | ahead 0 behind 0 | 1 | Assembled source b7f988feb62929bd250d915aa10a45600d5d2d8d: fresh build and 316 site tests passed; full browser suite passed 2746 checks, including native and derived closed-details controls, planted unreachable and toy-request faults; focused keyboard 10/10; six glossary links passed 8 width/theme/JS cases; project pytest 867 passed, 5 skipped; exact-source Python and site CI passed. Definitions compare directly to GLOSSARY.md and planted source/role/link defects are rejected. | Governance claim roles, worked examples, both traversals and glossary term links; preserved S003 source citations. | TK004, assembled S010 independent Review, owner Human QA and checked delivery remain. Earlier prefetch, whitespace-detector and closed-details failures remain in prior Receipt and feedback history; checked owner fixes resolved their observed checks. Workspace snapshot records ignored generated caches without byte capture; remote recovery and release remain unverified. | fc4ebb1a904902a961afc4268fcd0b7766f5275166da03bc7aaf8b4dad87586a |

## Acceptance

- [x] The page explains the authority order, confirmation and execution approval, Review and Human QA, and the limited meaning of a check with plain examples.
- [x] All six numbered governance planes appear in canonical order with current definitions and examples as roles of claims, with both traversal directions and no independent grant of authority.
- [x] Each glossary plane term links to its corresponding stable explanation; adverse tests detect changed or missing definitions, roles and links.
- [x] The assembled page is readable at 375 px and desktop in both themes, with and without JavaScript; actual verification and limits are retained in Receipts.
