# TK-002A - Visitors can enlarge readable text without clipping or overflow

**Task ID:** TK-002A
**Spec ID:** S-003
**Slice:** Visitors can enlarge readable text without clipping or overflow
**Status:** in-progress
**Blockers:** none
**Destination:** spec-acceptance: Presentation, Feedback
**Planned verification:** One completed production build; site suite; full browser checks and200-percent text scaling with all checks completed before further rebuild.
**Claimed by:** s003-frontend
**Current claimant:** s003-frontend

## Assignment

Correct the incomplete TK-001S candidate9f81ba1, with both failed checks preserved in its receipt. Owner explicitly authorized this corrective run in chat. Use the existing typography and wrapping changes, finish one production build, freeze .next and finish the full browser suite plus the94-case 200-percent reflow matrix before any rebuild. Repair scoped defects if needed; repeat only affected checks after a completed rebuild. Keep fonts/palette. No unrelated features or tool changes. Root owns all records; s003-frontend owns site files. Return source commit, exact checks, screenshots and both merge/completion answers; checked PR targets dev.

## Acceptance

- [ ] At desktop and375px in both themes, body/nav/labels/support text is larger with coherent hierarchy; no clipping, horizontal overflow or unusable zoom/reflow.
- [ ] Build, required checks and implementor QA pass on the named candidate; limitations are retained.
