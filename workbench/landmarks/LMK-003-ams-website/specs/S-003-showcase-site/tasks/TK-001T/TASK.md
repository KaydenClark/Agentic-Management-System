# TK-001T - Visitors see the Grill Board palette throughout the site

**Task ID:** TK-001T
**Spec ID:** S-003
**Slice:** Visitors see the Grill Board palette throughout the site
**Status:** ready
**Blockers:** none
**Destination:** spec-acceptance: Presentation
**Planned verification:** Compare rendered representative pages with the Grill Board palette in light/dark at desktop and 375px. Run token, contrast and relevant component checks plus site build.

## Authority and inputs

[Approved five-item owner readback](../../../../../../wiki/context-website-presentation.md#jot-74a9fff6-dcf2-4e5b-91fb-8ae4765c9458), AMS website feedback chat, 2026-11-02. Preparation only: this record grants no execution, claim, deployment or dev-to-main promotion authority. A ready record describes available inputs; the next agent needs its implementation assignment. No completion or Human QA is recorded.

Source recovery baseline: c8cd5ee (planning checkout). Recover the current parent Spec, relevant decisions and current `origin/dev` implementation before coding; this baseline is not evidence of the deployed website. The additional website-only example-link feedback is pending its individual readback; do not invent an exemption for GitHub sources or silently treat the old source-link requirement as a new owner decision.

## Assignment

Use the existing Grill Board palette visibly in the website rather than leaving it almost entirely black and white. Recover the shared token source and DDR-000Y, preserve established semantic meanings and apply the colors coherently across shared components and representative content. Token equality alone is insufficient: the actual rendered site must visibly use the colors. Do not edit the local Grill Board or invent a replacement palette.

One assigned implementor owns the complete behavior, affected content/styles, focused checks, QA, repairs and hand-back to S-003. Execute these feedback Tasks serially because they share shell/content/styles; there is no artifact dependency between them. Each is independently demoable and sized as one behavior through content, route/shell rendering, accessibility and verification. Integrate each checked result before taking the next shared-file assignment. Preserve unrelated work and historical receipts.

For implementation, branch from current `origin/dev`, target a checked feature PR to `dev`, and respect site delivery controls. Only the owner promotes `dev` to `main`. Report the named candidate and actual local/deployed verification limits. Record site experience judgments only when actually supplied by the owner; automated checks cannot establish comfort, comprehension or approval.

## Acceptance

- [ ] The rendered website visibly uses the Grill Board colors across shared components and content in both themes.
- [ ] Shared color values match the existing Grill Board source and established signal meanings remain consistent.
- [ ] Color use preserves readable text and WCAG AA contrast; essential meaning is also available without color.

## Hand-back

Return the candidate/PR, observable result, checks actually run, screenshots where relevant and remaining gaps to S-003. No implementation is performed by this planning change.
