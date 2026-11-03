# TK-001R - Visitors learn glossary definitions through visual explanations

**Task ID:** TK-001R
**Spec ID:** S-003
**Slice:** Visitors learn glossary definitions through visual explanations
**Status:** ready
**Blockers:** none
**Destination:** spec-acceptance: Content, Presentation
**Planned verification:** Follow a term link from a content page and explain its definition and relationship using the rendered visual. Inspect accessible text, both themes and narrow width; run focused glossary/link checks and site build.

## Authority and inputs

[Approved five-item owner readback](../../../../../../wiki/context-website-presentation.md#jot-74a9fff6-dcf2-4e5b-91fb-8ae4765c9458), AMS website feedback chat, 2026-11-02. Execution is authorized by the [S-003 orchestration assignment](../../../../../../wiki/context-website-presentation.md#jot-4adf0b91-665d-4abb-8644-4835b40e905a). Complete a checked feature PR into dev; Human QA and owner-only dev-to-main promotion remain separate.

Source recovery baseline: c8cd5ee (planning checkout). Recover the current parent Spec, relevant decisions and current `origin/dev` implementation before coding; this baseline is not evidence of the deployed website. The additional website-only example-link feedback is pending its individual readback; do not invent an exemption for GitHub sources or silently treat the old source-link requirement as a new owner decision.

## Assignment

Replace the plain term/explanation list with an engaging visual experience. Choose visual relationships, examples, diagrams or cards that teach the definitions rather than merely decorating the same list. Read the whole root glossary, preserve its meanings and distinguish implementation Tasks from evaluation tasks/trials. Retain stable term links from prose and readable explanations without scripts.

One assigned implementor owns the complete behavior, affected content/styles, focused checks, QA, repairs and hand-back to S-003. Execute these feedback Tasks serially because they share shell/content/styles; there is no artifact dependency between them. Each is independently demoable and sized as one behavior through content, route/shell rendering, accessibility and verification. Integrate each checked result before taking the next shared-file assignment. Preserve unrelated work and historical receipts.

For implementation, branch from current `origin/dev`, target a checked feature PR to `dev`, and respect site delivery controls. Only the owner promotes `dev` to `main`. Report the named candidate and actual local/deployed verification limits. Record site experience judgments only when actually supplied by the owner; automated checks cannot establish comfort, comprehension or approval.

## Acceptance

- [ ] The glossary teaches definitions through meaningful visuals and examples rather than a plain list alone.
- [ ] Visual relationships and definitions agree with the root glossary; implementation Tasks and evaluation tasks/trials remain distinct.
- [ ] Definition links from the site still work, and text equivalents make visual meaning available to assistive technology.
- [ ] The experience is readable and keyboard usable in both themes at desktop and 375px.

## Hand-back

Return the candidate/PR, observable result, checks actually run, screenshots where relevant and remaining gaps to S-003. No implementation is performed by this planning change.
