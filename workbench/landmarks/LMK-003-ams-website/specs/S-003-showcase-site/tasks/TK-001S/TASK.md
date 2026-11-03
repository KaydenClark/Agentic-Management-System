# TK-001S - Visitors can comfortably read text across the website

**Task ID:** TK-001S
**Spec ID:** S-003
**Slice:** Visitors can comfortably read text across the website
**Status:** ready
**Blockers:** none
**Destination:** spec-acceptance: Presentation
**Planned verification:** Compare representative page screenshots before/after at the same viewport and zoom, including small labels and long content; check both themes and 375px. Run focused typography/reflow checks and site build.

## Authority and inputs

[Approved five-item owner readback](../../../../../../wiki/context-website-presentation.md#jot-74a9fff6-dcf2-4e5b-91fb-8ae4765c9458), AMS website feedback chat, 2026-11-02. Preparation only: this record grants no execution, claim, deployment or dev-to-main promotion authority. A ready record describes available inputs; the next agent needs its implementation assignment. No completion or Human QA is recorded.

Source recovery baseline: c8cd5ee (planning checkout). Recover the current parent Spec, relevant decisions and current `origin/dev` implementation before coding; this baseline is not evidence of the deployed website. The additional website-only example-link feedback is pending its individual readback; do not invent an exemption for GitHub sources or silently treat the old source-link requirement as a new owner decision.

## Assignment

Increase the effective type sizes across body text, navigation, labels and supporting content. Adjust line height, spacing and hierarchy coherently rather than enlarging only headings. Inspect all current routes and shared styles; retain the existing font family unless a demonstrated readability need warrants changing it. Do not invent a numerical size accepted by the owner; show before/after at normal zoom.

One assigned implementor owns the complete behavior, affected content/styles, focused checks, QA, repairs and hand-back to S-003. Execute these feedback Tasks serially because they share shell/content/styles; there is no artifact dependency between them. Each is independently demoable and sized as one behavior through content, route/shell rendering, accessibility and verification. Integrate each checked result before taking the next shared-file assignment. Preserve unrelated work and historical receipts.

For implementation, branch from current `origin/dev`, target a checked feature PR to `dev`, and respect site delivery controls. Only the owner promotes `dev` to `main`. Report the named candidate and actual local/deployed verification limits. Record site experience judgments only when actually supplied by the owner; automated checks cannot establish comfort, comprehension or approval.

## Acceptance

- [ ] Body text, navigation, labels and supporting information are visibly larger and comfortably readable at normal zoom.
- [ ] Text hierarchy and spacing remain coherent across current routes in both themes.
- [ ] At 375px and desktop, enlarged text neither clips controls nor creates horizontal page overflow, and zoom/reflow remains usable.

## Hand-back

Return the candidate/PR, observable result, checks actually run, screenshots where relevant and remaining gaps to S-003. No implementation is performed by this planning change.
