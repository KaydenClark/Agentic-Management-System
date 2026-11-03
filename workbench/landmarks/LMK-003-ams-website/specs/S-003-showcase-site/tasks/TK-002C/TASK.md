# TK-002C - Readers follow the consolidated orientation with verified alias navigation

**Task ID:** TK-002C
**Spec ID:** S-003
**Slice:** Readers follow the consolidated orientation with verified alias navigation
**Status:** in-progress
**Blockers:** none
**Destination:** spec-acceptance: Content, Route, Feedback
**Planned verification:** Order-independent alias checks with negative controls; completed production build and full site suite; focused rendered orientation, old entry routes and both themes at375px and desktop.
**Claimed by:** s003-frontend
**Current claimant:** s003-frontend

## Assignment

Owner authorizes this bounded corrective run after draft PR147 stopped. Recover candidate0be5c58 and the TK-001P receipt, preserving both failed verification attempts and the incomplete original run. Fix the new alias checker without depending on HTML attribute order; retain negative controls for wrong destinations, absent current-page state and unequal alias content. Inspect every remaining failing assertion before running the corrected full suite. Finish one build before tests and freeze it while browser readers run; never rebuild concurrently with them.

Finish and verify the consolidated orientation required by TK-001P: one About introduction, differentiated Home/Why/How, all required explanations and working old route/fragment entries. Preserve source/revision identity, privacy and honest evidence limits. s003-frontend owns site source/tests/docs only; orchestrator owns records. Correct in this run, commit/push and deliver checked PR147 to dev after parent inspection and current-head CI. Never promote dev to main. Full sibling demo/flow-chart features, paid services, new trial campaigns and shared-skill repair are excluded.

## Acceptance

- [ ] Valid About alias links pass regardless of attribute order; wrong destination, missing current-page state and changed alias content fail.
- [ ] The single About orientation, differentiated pages, required subjects and old route/fragment entries work at375px and desktop in both themes.
- [ ] Build, full site suite and affected browser QA pass on the named candidate; earlier failures and verification limits remain visible.
