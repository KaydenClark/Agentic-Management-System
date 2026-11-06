# TK-004 - Branch model, orchestrator and RSI round diagrams

**Task ID:** TK-004
**Spec ID:** S-010
**Slice:** Branch model, orchestrator and RSI round diagrams
**Status:** in-progress
**Blockers:** TK-001
**Destination:** spec-acceptance: S-010 Acceptance Criteria
**Claimed by:** codex-governance-charts
**Current claimant:** codex-governance-charts

Workspace baseline sha256:054ea7747e64b161910f5828ed6abed1450727161ac00654fafb7d851787da6b

## Acceptance

- [x] The branch, historical responsibilities and RSI diagrams explain their actual authority and current limits, including owner-only website promotion, C's connector prohibition and the local Python writer.
- [x] The RSI diagram shows qualified and rejected/inconclusive outcomes, baseline 0 excluded, and the initial attempt followed by at most two retries before stop for the same improvement chain.
- [x] The page presents all eight named charts and working inventory links; checks reject missing or extra charts, states, transitions, required boundaries and links.
- [x] The page is readable at 375 px and desktop in both themes with and without JavaScript; actual verification and limitations are retained in Receipts.

## Receipt

| Run | Branch | HEAD SHA | Upstream | Dirty | Tests | Docs touched | Remaining gap | Checksum |
|---|---|---|---|---|---|---|---|---|
| 1 | Feature/S-010-governance-flow-charts | 69de1c040469b048ec5db0c601eeadf23adb662a | ahead 0 behind 0 | 1 | Source 69de1c040469b048ec5db0c601eeadf23adb662a: fresh build/postbuild, frozen pages:check and 320 site tests passed; full browser 2746/2746; eight inventory/anchor cases at 375/1440 light/dark with and without JavaScript passed; source Python and site CI passed. Planted missing/extra charts, links, states, edges, no-adoption path and key-boundary faults were rejected. Process transitions are manually audited and fingerprint-bound, not runtime replay. | Branch model, historical responsibility split, RSI round and eight-chart inventory; current six-plane and source citations retained. | Root reviewed an uncommitted draft and found no no-adoption path plus ambiguous attempt identity; both were corrected before source 69de1c0 and the bounded re-review passed. This is not S005 feedback evidence or assembled independent Review. A pages:check against server-mutated build output failed on duplicate cache artifacts; after browser exit a fresh build and check passed without collector changes. TK004 delivery, assembled S010 independent Review and Human QA remain. Ignored generated caches were inventoried by name but not byte-captured; workspace recovery and release unverified. | 71246703a323e87acbd1395344b08e37d51f58de94151b226b393824e9ba5fb7 |
