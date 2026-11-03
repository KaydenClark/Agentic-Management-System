# TK-001Z - Readers understand RSI charts and evidence without leaving the site

**Task ID:** TK-001Z
**Spec ID:** S-007
**Slice:** Visible real-evidence charts and supporting information on the RSI page
**Status:** in-progress
**Blockers:** none
**Destination:** spec-acceptance: Feedback loop connection; Every number links; Build explanation
**Planned verification:** Renderer regressions for visible charts and on-site evidence links; production build and site tests; desktop and 375px browser inspection in both themes; applicable RUNBOOK checks.
**Claimed by:** codex-rsi-feedback
**Current claimant:** codex-rsi-feedback

## Authority and inputs

Kayden confirmed the RSI feedback readback and authorized fixing the website in chat, 2026-11-02. See [approval](../../../../../../wiki/context-website-presentation.md#jot-cf0db5e8-89b7-4766-85d7-1f101bfc3aaa). Recover the current dev reader, safe repair evidence and tests from `origin/dev` (inspection baseline `5151f0f`). Existing data and safe published summaries are available; this correction does not wait on new trial campaigns or whole-Spec completion.

## Assignment

One implementor owns this complete correction, focused tests, browser QA and hand-back. Make relevant existing results visibly understandable through charts, including the baseline/candidate development comparison. Put supporting explanations, values, evidence identity, failures, disposition and limitations on the site. Omit irrelevant repository plumbing instead of substituting links. RSI content and its shared chrome must not send readers to GitHub. Preserve source identity as readable metadata and use internal links to meaningful evidence, not redirects to GitHub.

Preserve the live reader and keep dev trials, held-out results, development observations and audit results separate. Empty or failed reads must remain honest; never fabricate values or imply demonstrated improvement from counts or smaller text. Preserve earlier failed attempts and pending work. Do not claim or close TK-002, change the shared skills, run new campaigns or expose private evidence. Coordinate overlapping reader files against current dev; do not take another writer's checkout.

The correction crosses safe evidence, route rendering, shared footer, styles, tests and browser verification. Keep it as one independently demoable run. Target checked feature delivery to dev under site controls; production promotion remains the owner's action.

## Acceptance

- [ ] Real recorded evidence produces visible, labeled charts with comparable scales and readable values in both themes at desktop and 375px.
- [ ] The baseline/candidate comparison and its supporting data, provenance, failures and limits can be understood entirely on-site.
- [ ] No GitHub link appears in the rendered RSI page, including shared chrome; internal evidence links resolve to useful on-site content.
- [ ] Empty/unavailable trial states, separate evidence classes and existing failure history remain accurate; synthetic/test trial rows never render.
- [ ] Focused regressions, production build, site suite and browser inspection pass; actual candidate, delivery and verification limits are recorded.

## Hand-back

Return the exact candidate and PR, actual checks, screenshots and limitations. A completed page correction does not establish S-007 acceptance, owner Human QA or measured RSI benefit.
