# TK-002B - Readers understand S-003 examples and evidence without leaving the website

**Task ID:** TK-002B
**Spec ID:** S-003
**Slice:** Readers understand S-003 examples and evidence without leaving the website
**Status:** in-progress
**Blockers:** owner:s003-source-keyboard-correction
**Destination:** spec-acceptance: Content, Route, Trust
**Planned verification:** Built-output link checks plus rendered navigation through orientation/example/evidence at desktop and375px in both themes; build/site tests/hygiene.
**Claimed by:** s003-glossary
**Current claimant:** s003-glossary

## Assignment

Implement the confirmed JOT-09260032 website-only readback. Recover current dev after prior serial S-003 changes. Present useful examples and supporting material on-site; omit irrelevant material. Remove GitHub exits from S-003 reader flows, including source/footer links, while preserving honest source/revision identities and the deployed SHA as visible text. Do not copy private source, invent evidence or imply improvement. Preserve working historical entry routes, term anchors and useful reading order. Root owns records; assigned implementor owns site source/tests/docs. Return exact checked candidate, rendered QA and gaps; merge checked feature PR into dev only.

## Acceptance

- [ ] A reader can follow orientation, real-work example and supporting explanations without a GitHub exit. Useful supporting material is readable on-site, provenance/revision identity remains, deployed SHA remains visible, and no private or fabricated evidence is introduced.
- [ ] Build, required checks and implementor QA pass on the named candidate; limitations are retained.

## Receipt

| Run | Branch | HEAD SHA | Upstream | Dirty | Tests | Docs touched | Remaining gap | Checksum |
|---|---|---|---|---|---|---|---|---|
| 1 | codex/s003-on-site-sources | 8e211a119e80e20f9282d21a51beaea966cdc770 | ahead 0 behind 0 | 0 | Source8e211a119e80e20f9282d21a51beaea966cdc770: completed build; first npm229/230 failed nested refusal-list reader; semantic-reader repair and missing-refusal/citation controls pass231/231. Focused source/credit/toy browser92/92. Second verification60/64 enlarged-text cases: four About keyboard cases fail at375/1280 in both themes; overflow/contrast/console pass. Three-strike STOP; full browser already running, no retry. | Site README, on-site citations/credits and policy/identity/attribution checks; both failed logs and screenshots retained locally. | Task incomplete; no merge. Read-only diagnosis points to pre-clicked disclosure retaining sequential focus position, then detector stopping on body before earlier controls. Product unreachability not established. Owner must authorize a bounded correction; no repair/retry or new claim before approval. Human QA and owner-only production remain separate. | 35afe106e176ccefccfaf901d3dcca5c1c8232ec7acbaa03bb3db6f4b95c41ae |

## Current continuation

Stopped under AGENTS.md after two unexpected verification failures. The already-running whole-site suite subsequently finished 2406/2406; this does not waive the 60/64 enlarged-text result. All browser readers are finished and the loopback server is stopped. The build was frozen at coordination revision 21fc0e8 with the source bytes committed as 8e211a119e80e20f9282d21a51beaea966cdc770; no later rebuild or retry occurred.

Read-only diagnosis: the enlarged-text harness clicks the first source disclosure before scanning keyboard reachability. Blurring leaves its sequential focus position there; the detector stops on body before visiting the 15 earlier controls. This supports a harness-start problem, not proved product unreachability. Proposed correction: establish and fault-test a deterministic document-start traversal while preserving all-control reachability/focus checks, then rerun the same 64-case matrix and relevant checks. Execution requires a new bounded Task after owner authorization. Keep this incomplete run and both failed logs; do not close it as successful.
