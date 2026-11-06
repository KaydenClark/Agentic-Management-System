# TK-001 - Task lifecycle diagram generated from the code's status set, with a drift test, on `dev`

**Task ID:** TK-001
**Spec ID:** S-010
**Slice:** Task lifecycle diagram generated from the code's status set, with a drift test, on `dev`
**Status:** in-progress
**Blockers:** none
**Destination:** spec-acceptance: S-010 Acceptance Criteria

**Planned verification:** Compare states and transitions with the current native runtime; prove unknown and omitted states and edges fail; build the site before site tests; inspect 375 px and desktop in both themes with JavaScript disabled.
**Claimed by:** codex-governance-charts
**Current claimant:** codex-governance-charts

## Assignment

Deliver the first readable Task lifecycle diagram at a visitor-facing route using the existing site shell. Identify runtime states and actual transitions from the Node handlers and contracts, not a copied model. Include a drift check against the runtime at the build commit. Own S-010's page and its focused tests; shared navigation, tour, glossary and page inventory remain assigned separately. This Task does not close the Spec or establish independent Review or Human QA.

## Acceptance

- [x] A visitor can read the Task lifecycle and its actual transitions at 375 px and desktop in both themes without JavaScript.
- [x] A drift check fails for an added unknown state, omitted state, added unknown edge and omitted edge against the runtime source.
- [x] The built site and applicable tests pass; actual browser checks and remaining limits are recorded.

Workspace baseline sha256:3fa637d179e1dcd78a6e453e26c4bb36b515f63cc1e42a9ba82e8c50f4ecf504

## Receipt

| Run | Branch | HEAD SHA | Upstream | Dirty | Tests | Docs touched | Remaining gap | Checksum |
|---|---|---|---|---|---|---|---|---|
| 1 | Feature/S-010-governance-flow-charts | 6af751c5547532648be8db31d694e8b77f2d2bbf | none | 0 | At 6af751c: npm run build and npm test passed 278; browser 375 and 1440 light/dark with and without JavaScript passed eight cases; tour 375 passed 40 checks before final chart styling. Drift negatives passed; transitions manually audited with source fingerprints. Root pytest running. | S-010 Task lifecycle page, tour navigation and glossary links. | First site suite found orphan route; fixed via navigation. First browser run lacked matching Chromium; rerun passed using installed Playwright. Workspace closeout not complete: discovery, retained refs and ignored entries remain. Full project checks, independent Review and Human QA remain. | 9923deeea9d13da592d292670d47c05207036d16d7e25f527885e9c37d90c8c0 |
