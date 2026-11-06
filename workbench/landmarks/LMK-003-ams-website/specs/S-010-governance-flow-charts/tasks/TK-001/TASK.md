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

- [ ] A visitor can read the Task lifecycle and its actual transitions at 375 px and desktop in both themes without JavaScript.
- [ ] A drift check fails for an added unknown state, omitted state, added unknown edge and omitted edge against the runtime source.
- [ ] The built site and applicable tests pass; actual browser checks and remaining limits are recorded.
