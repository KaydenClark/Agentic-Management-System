# TK-001Q - Visitors use a full-width navigation menu that stays visible

**Task ID:** TK-001Q
**Spec ID:** S-003
**Slice:** Visitors use a full-width navigation menu that stays visible
**Status:** ready
**Blockers:** none
**Destination:** spec-acceptance: Presentation, Route
**Planned verification:** Open a long page, scroll, use the home icon and theme toggle, and tab through the menu at desktop and 375px. Run focused header/navigation checks and site build.

## Authority and inputs

[Approved five-item owner readback](../../../../../../wiki/context-website-presentation.md#jot-74a9fff6-dcf2-4e5b-91fb-8ae4765c9458), AMS website feedback chat, 2026-11-02. Preparation only: this record grants no execution, claim, deployment or dev-to-main promotion authority. A ready record describes available inputs; the next agent needs its implementation assignment. No completion or Human QA is recorded.

Source recovery baseline: c8cd5ee (planning checkout). Recover the current parent Spec, relevant decisions and current `origin/dev` implementation before coding; this baseline is not evidence of the deployed website. The additional website-only example-link feedback is pending its individual readback; do not invent an exemption for GitHub sources or silently treat the old source-link requirement as a new owner decision.

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
