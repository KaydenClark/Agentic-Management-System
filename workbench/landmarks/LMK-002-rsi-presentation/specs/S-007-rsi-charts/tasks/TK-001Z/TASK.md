# TK-001Z - Readers understand RSI charts and evidence without leaving the site

**Task ID:** TK-001Z
**Spec ID:** S-007
**Slice:** Visible real-evidence charts and supporting information on the RSI page
**Status:** done
**Blockers:** none
**Destination:** spec-acceptance: Feedback loop connection; Every number links; Build explanation
**Planned verification:** Renderer regressions for visible charts and on-site evidence links; production build and site tests; desktop and 375px browser inspection in both themes; applicable RUNBOOK checks.
**Claimed by:** codex-rsi-feedback
**Current claimant:** codex-rsi-feedback
**Proof:** Source f893f6d; production build and 211 site tests pass; Python 811 passed and 4 skipped with socket permissions; Chromium 1280px and 375px both themes: visible charts, no outbound links or overflow, zero relevant console errors or scoped WCAG findings; data disclosure and theme interactions pass. Source and verification records published on codex/rsi-results-feedback.

## Authority and inputs

Kayden confirmed the RSI feedback readback and authorized fixing the website in chat, 2026-11-02. See [approval](../../../../../../wiki/context-website-presentation.md#jot-cf0db5e8-89b7-4766-85d7-1f101bfc3aaa). Recover the current dev reader, safe repair evidence and tests from `origin/dev` (inspection baseline `5151f0f`). Existing data and safe published summaries are available; this correction does not wait on new trial campaigns or whole-Spec completion.

## Assignment

One implementor owns this complete correction, focused tests, browser QA and hand-back. Make relevant existing results visibly understandable through charts, including the baseline/candidate development comparison. Put supporting explanations, values, evidence identity, failures, disposition and limitations on the site. Omit irrelevant repository plumbing instead of substituting links. RSI content and its shared chrome must not send readers to GitHub. Preserve source identity as readable metadata and use internal links to meaningful evidence, not redirects to GitHub.

Preserve the live reader and keep dev trials, held-out results, development observations and audit results separate. Empty or failed reads must remain honest; never fabricate values or imply demonstrated improvement from counts or smaller text. Preserve earlier failed attempts and pending work. Do not claim or close TK-002, change the shared skills, run new campaigns or expose private evidence. Coordinate overlapping reader files against current dev; do not take another writer's checkout.

The correction crosses safe evidence, route rendering, shared footer, styles, tests and browser verification. Keep it as one independently demoable run. Target checked feature delivery to dev under site controls; production promotion remains the owner's action.

## Acceptance

- [x] Real recorded evidence produces visible, labeled charts with comparable scales and readable values in both themes at desktop and 375px.
- [x] The baseline/candidate comparison and its supporting data, provenance, failures and limits can be understood entirely on-site.
- [x] No GitHub link appears in the rendered RSI page, including shared chrome; internal evidence links resolve to useful on-site content.
- [x] Empty/unavailable trial states, separate evidence classes and existing failure history remain accurate; synthetic/test trial rows never render.
- [x] Focused regressions, production build, site suite and browser inspection pass; actual candidate, delivery and verification limits are recorded.

## Hand-back

Return the exact candidate and PR, actual checks, screenshots and limitations. A completed page correction does not establish S-007 acceptance, owner Human QA or measured RSI benefit.

## Check and QA

Source candidate `f893f6df65fe22a59949b080020d91df64c56168`, based on dev `5151f0f81dd2d1544e92f4adbfd5693a4d7629b0`. The regression first reproduced the absent paired chart and outbound evidence links. Updated link-contract assertions retain source identity and on-site destinations. The full site suite then caught literal chart dimensions; converting them to existing theme tokens returned green without weakening the check.

Production build and all 211 site tests pass. Python: the sandbox run returned 97 failures and 9 errors because local server sockets were denied; the permitted rerun passed 811 tests with 4 skipped. Wiki, layout, decision records, diff whitespace and built-site hygiene pass. Doctor reports no blocking finding for this Task; existing S-011 dependency and host-setup attention remain separate.

The actual built RSI page was checked with existing Playwright/Chromium at 1280px and 375px in both themes. Page identity, meaningful content, visible comparison bars, zero horizontal overflow, no outbound links, no framework overlay, zero relevant console errors and zero scoped WCAG A/AA violations pass. Chart links open the on-site data table; keyboard Enter operates its disclosure, and the theme toggle changes the theme. Screenshots were inspected; the comparison now follows the introduction directly. React self-review confirms server-rendered content, stable list keys, labeled values and no new client chart library or dependency.

No live database read was verified: this local build lacks the publishable environment and honestly shows unavailable trial data. Development evidence remains visible. No owner Human QA, held-out improvement, skill acceptance or production promotion is claimed.

## Publication gate

Initially, the source was committed locally and automatic approval review rejected the feature push even after verifying the configured public repository, its owner and push access, and zero hygiene findings; it requires explicit owner approval for public publication separately from implementation. Kayden then explicitly answered Publish and merge into dev. The source and verification records were pushed on codex/rsi-results-feedback at c259d19; the PR will target dev and merge only after its exact-head shared CI passes. No production promotion or live database verification is claimed.

## Receipt

| Run | Branch | HEAD SHA | Upstream | Dirty | Tests | Docs touched | Remaining gap | Checksum |
|---|---|---|---|---|---|---|---|---|
| 1 | codex/rsi-results-feedback | f843b009a99113dccd1f292e21e159a99b3926e4 | ahead 0 behind 0 | 0 | Source f893f6d; production build and 211 site tests pass; Python 811 passed and 4 skipped with socket permissions; Chromium 1280px and 375px both themes: visible charts, no outbound links or overflow, zero relevant console errors or scoped WCAG findings; data disclosure and theme interactions pass. Source and verification records published on codex/rsi-results-feedback. | Updated S-007 on-site evidence contract, shared footer contract, approved owner context and TK-001Z verification/limits. | Exact-head shared CI and PR merge to dev follow; live database and protected deployment readback unavailable locally. No production promotion, Human QA or measured RSI benefit claimed.; close attribution: {"agent":"codex-rsi-feedback","claimant":"codex-rsi-feedback","onBehalfOf":null} | f2c772d49d02f2d08acc36f9e93b3f3704cb7eaa2355451b7a7ad1fef9fc46f4 |
