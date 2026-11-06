# TK-001Q - Visitors use a full-width navigation menu that stays visible

**Task ID:** TK-001Q
**Spec ID:** S-003
**Slice:** Visitors use a full-width navigation menu that stays visible
**Status:** in-progress
**Blockers:** none
**Destination:** spec-acceptance: Presentation, Route
**Planned verification:** Open a long page, scroll, use the home icon and theme toggle, and tab through the menu at desktop and 375px. Run focused header/navigation checks and site build.
**Claimed by:** s003-frontend
**Current claimant:** s003-frontend

## Authority and inputs

[Approved five-item owner readback](../../../../../../wiki/context-website-presentation.md#jot-74a9fff6-dcf2-4e5b-91fb-8ae4765c9458), AMS website feedback chat, 2026-11-02. Execution is authorized by the [S-003 orchestration assignment](../../../../../../wiki/context-website-presentation.md#jot-4adf0b91-665d-4abb-8644-4835b40e905a). Complete a checked feature PR into dev; Human QA and owner-only dev-to-main promotion remain separate.

Source recovery baseline: c8cd5ee (planning checkout). Recover the current parent Spec, relevant decisions and current `origin/dev` implementation before coding; this baseline is not evidence of the deployed website. The confirmed website-only material/link rule is assigned to TK-002B (JOT-09260032). Preserve provenance and useful on-site material; coordinate shared-file changes serially.

## Assignment

Replace the constrained reading-order header with conventional navigation using the available header width. The top-left home icon is the Home link, the header remains visible when scrolling, and the light/dark control is at the far right. Preserve current-page indication and keyboard access; adapt the menu to narrow screens without horizontal page overflow. Keep page-content reading width independent of the header width.

One assigned implementor owns the complete behavior, affected content/styles, focused checks, QA, repairs and hand-back to S-003. Execute these feedback Tasks serially because they share shell/content/styles; there is no artifact dependency between them. Each is independently demoable and sized as one behavior through content, route/shell rendering, accessibility and verification. Integrate each checked result before taking the next shared-file assignment. Preserve unrelated work and historical receipts.

For implementation, branch from current `origin/dev`, target a checked feature PR to `dev`, and respect site delivery controls. Only the owner promotes `dev` to `main`. Report the named candidate and actual local/deployed verification limits. Record site experience judgments only when actually supplied by the owner; automated checks cannot establish comfort, comprehension or approval.

## Acceptance

- [ ] The top-left icon returns to Home and has an accessible name.
- [ ] At desktop width the header uses the available width and the theme toggle occupies the far right.
- [ ] Navigation stays visible while scrolling without obscuring focused controls or anchor destinations.
- [ ] At 375px the menu remains usable with visible keyboard focus, accessible links and no horizontal page overflow.

## Hand-back

Return the candidate/PR, observable result, checks actually run, screenshots where relevant and remaining gaps to S-003. No implementation is performed by this planning change.

## Receipt

| Run | Branch | HEAD SHA | Upstream | Dirty | Tests | Docs touched | Remaining gap | Checksum |
|---|---|---|---|---|---|---|---|---|
| 1 | codex/s003-navigation | d929eeec1dd517132494797753a56abdd5f914a9 | ahead 0 behind 0 | 0 | Sourced929eeec1dd517132494797753a56abdd5f914a9: production build and217site tests pass. First focused browser330/347pass,17fail (clipped contrast undecidable and header prefetch interfering with toy network check). After repair browser347/347pass. Second completed navigation matrix76/80pass:4phone cases clip focused links at100/200-percent in both themes. Original no-JS RAF harness was canceled without a completed matrix; log retained. Three-strike STOP, no full keyboard QA or completion. | site README, shared header/styles and browser detectors; exact geometry and both failed attempts retained locally | Draft PR148 pushed, no merge. Owner-authorized corrective run must establish focus-scroll cause and fully reveal focused nav links, then rerun the80case matrix and affected browser checks on one completed frozen build. R/T/B remain undispatched; Human QA and production remain owner gates. | 8cba4c66ee76d3a3f21b2b2e28377a95f4fc58dc3434f1234568be289d0f975e |

## Current continuation

The later bounded corrective run TK-002D established the native-focus cause, repaired full-link visibility and met the inherited header behavior with its actual verification. This original failed run remains unchanged; native incomplete-run retirement is unavailable. Follow TK-002D and the parent Spec for current delivery.
