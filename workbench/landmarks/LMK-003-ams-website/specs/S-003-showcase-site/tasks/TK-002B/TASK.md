# TK-002B - Readers understand S-003 examples and evidence without leaving the website

**Task ID:** TK-002B
**Spec ID:** S-003
**Slice:** Readers understand S-003 examples and evidence without leaving the website
**Status:** ready
**Blockers:** none
**Destination:** spec-acceptance: Content, Route, Trust
**Planned verification:** Built-output link checks plus rendered navigation through orientation/example/evidence at desktop and375px in both themes; build/site tests/hygiene.

## Assignment

Implement the confirmed JOT-09260032 website-only readback. Recover current dev after prior serial S-003 changes. Present useful examples and supporting material on-site; omit irrelevant material. Remove GitHub exits from S-003 reader flows, including source/footer links, while preserving honest source/revision identities and the deployed SHA as visible text. Do not copy private source, invent evidence or imply improvement. Preserve working historical entry routes, term anchors and useful reading order. Root owns records; assigned implementor owns site source/tests/docs. Return exact checked candidate, rendered QA and gaps; merge checked feature PR into dev only.

## Acceptance

- [ ] A reader can follow orientation, real-work example and supporting explanations without a GitHub exit. Useful supporting material is readable on-site, provenance/revision identity remains, deployed SHA remains visible, and no private or fabricated evidence is introduced.
- [ ] Build, required checks and implementor QA pass on the named candidate; limitations are retained.
