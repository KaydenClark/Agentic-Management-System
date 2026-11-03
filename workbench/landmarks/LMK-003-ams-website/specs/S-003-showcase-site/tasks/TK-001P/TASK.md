# TK-001P - Visitors understand a coherent orientation without overlapping pages

**Task ID:** TK-001P
**Spec ID:** S-003
**Slice:** Visitors understand a coherent orientation without overlapping pages
**Status:** ready
**Blockers:** none
**Destination:** spec-acceptance: Content, Route
**Planned verification:** Open Home and follow the orientation links; check unique page purposes and all affected entry routes. Run site build and focused route/content/link checks.

## Authority and inputs

[Approved five-item owner readback](../../../../../../wiki/context-website-presentation.md#jot-74a9fff6-dcf2-4e5b-91fb-8ae4765c9458), AMS website feedback chat, 2026-11-02. Execution is authorized by the [S-003 orchestration assignment](../../../../../../wiki/context-website-presentation.md#jot-4adf0b91-665d-4abb-8644-4835b40e905a). Complete a checked feature PR into dev; Human QA and owner-only dev-to-main promotion remain separate.

Source recovery baseline: c8cd5ee (planning checkout). Recover the current parent Spec, relevant decisions and current `origin/dev` implementation before coding; this baseline is not evidence of the deployed website. The confirmed website-only material/link rule is assigned to TK-002B (JOT-09260032). Preserve provenance and useful on-site material; coordinate shared-file changes serially.

## Assignment

Resolve the overlap among Home, Start Here, Why and How It Works. Present Start Here as About; consolidate or relocate repeated content while retaining the explanation of AMS purpose, workflow, evidence limits, project identity and setup-workbench. Choose the smallest coherent structure from the actual current site. Repair navigation, inline links and reading-order links together; do not merely rename menu labels.

One assigned implementor owns the complete behavior, affected content/styles, focused checks, QA, repairs and hand-back to S-003. Execute these feedback Tasks serially because they share shell/content/styles; there is no artifact dependency between them. Each is independently demoable and sized as one behavior through content, route/shell rendering, accessibility and verification. Integrate each checked result before taking the next shared-file assignment. Preserve unrelated work and historical receipts.

For implementation, branch from current `origin/dev`, target a checked feature PR to `dev`, and respect site delivery controls. Only the owner promotes `dev` to `main`. Report the named candidate and actual local/deployed verification limits. Record site experience judgments only when actually supplied by the owner; automated checks cannot establish comfort, comprehension or approval.

## Acceptance

- [ ] Each retained orientation page has a distinct purpose; Start Here is presented as About rather than a competing introduction.
- [ ] Home, Why and How It Works content is consolidated or differentiated without losing the parent Spec explanatory requirements.
- [ ] Visitors can reach the orientation, example and evidence and return through working internal links; old entry routes still lead to relevant content.

## Hand-back

Return the candidate/PR, observable result, checks actually run, screenshots where relevant and remaining gaps to S-003. No implementation is performed by this planning change.
