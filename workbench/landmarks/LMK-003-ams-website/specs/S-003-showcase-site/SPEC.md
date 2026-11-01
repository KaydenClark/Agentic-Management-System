# S-003 - Website shell and AMS orientation

**Spec ID:** S-003
**Status:** active
**Priority:** 1
**Owner:** Kayden; orchestrator A (Website, cloud)
**Stance:** Builder
**Updated:** 2026-11-01
**Catalog description:** Explain AMS and its evidence.
**Blockers:** none
**Latest event:** Destination clarified.
**Next gate:** Reconcile assignments.
**Confirmation:** [JOT-5b41bab8-c88f-49c4-be9c-b438285490b0](../../../../wiki/context-active-spec-approvals.md)
**Execution approval:** [JOT-5b41bab8-c88f-49c4-be9c-b438285490b0](../../../../wiki/context-active-spec-approvals.md)

## Intent and authority

The owner's [brief and corrections](../../../../wiki/context-website-presentation.md) establish this destination. S-003 owns shell/orientation; siblings remain required in the four-Landmark build. This revision authorizes specification repair only.

## Outcome

Visitors come for understanding: what AMS manages, why, how intent becomes work/feedback and what evidence demonstrates. Non-engineers get plain explanations; technical readers can follow sources. The website presents AMS without operating it.

## Why It Matters

The site preserves the owner’s explanation of AMS and lets visitors examine whether its real work supports its claims.

## Desired Behavior

Pages open plainly, define/link unfamiliar terms, then offer detail/sources. Explain ideas before IDs. Agents draft from approved records and owner feedback, without requiring owner-written copy.

### Orientation content

- **Start here:** define AMS: managing Kayden's agents, workflows, intent, skills and AI tools. Explain the problem, identify this website as its first outside product, and orient visitors to the tour, demonstrations and evidence. Distinguish presentation from live controls.
- **Why:** explain preserving intent/corrections, organizing delegated work and learning from failures. Connect these purposes to this build. Separate intended benefits from measured results; link RSI evidence.
- **How it works:** explain intent -> Landmark -> Spec -> Task, then implementation, checks, review, human judgment and delivery. Walk through one real, sourced Spec/Task. Explain feedback returning to its durable owner and failed results starting bounded RSI comparisons. Link governance/flow charts; do not imply every step has succeeded.
- **Quickstart:** a reading route through the introduction, real-work example, demonstration or skill summary, then RSI evidence/limits. Explain what each stop teaches. No installation, credentials or command replay.
- **Limits:** explain that the site runs no agents or record writes. Distinguish demonstrations, build activity, assessments and demonstrated improvement. Source incomplete/unsupported capabilities and explain where human judgment remains necessary.
- **Glossary:** define tour terms consistently with the root glossary, including implementation Tasks versus evaluation tasks/trials. Link definitions from their uses and back to the explanation.
- **About AMS:** explain the project, who made it, why it exists and its relationship to this website. Project context, not employment history; no CV/resume request.

### Shell and related capabilities

Navigation shows current page, tour order/start/finish and direct subject links, without dead ends. Core text works without scripts. Light/dark follows system or manual override. Every page links its deployed SHA to GitHub.

Introduce and link RSI charts (S-007), site-written skill summaries (S-008), the demo Grill Board with non-engineering sample questions (S-009), and governance/flow charts (S-010). Keep private skill source private.

No separate build-history/“Under the hood” page. S-007 explains build evidence/results from S-006; S-008 explains skills. Prose explains sourced events; sentences need not be database rows. Activity alone proves no improvement.

### Data and approvals

Read-only Supabase with publishable key; Python writes under S-006; service key stays local (ADR-003H). Shared states, including S-007:

- **Populated:** records retain sources/event/version identity; show last successful read time.
- **Empty successful read:** say no matching records exist and explain what belongs there. Keep chart spaces visible; no sample numbers or fabricated results.
- **Pending/failed:** distinguish loading from unavailable and from zero results. Label retained data with its last successful read time. Static explanations remain readable.
- Test/synthetic rows never appear as real evidence. S-007 owns result labels/comparisons; S-006 owns storage/access.

Draft until Kayden approves via S-005 (chat fallback). Approval binds content hash/dated source; edits restore draft. Owner quotations are verbatim/sourced.

## Decisions And Contracts

- Next.js in `site/`, Python backends, no FastAPI, free Vercel address. Feature -> protected `dev` -> `main`; only Kayden approves promotion. A holds no service key and deploys through Git pushes to `dev`.
- No third-party scripts, remote fonts, tracking or cookies. Resource loads: site/Supabase; GitHub links are navigation.
- Theme/fonts follow [DDR-000Y](../../../../docs/ddr/000Y-the-grill-board-theme-follows-the-grilling-board-redesign-artifact.md). Shared values match `grill-board/theme/tokens.json` in both themes. Site type/spacing is consistent; no equality to absent tokens.

## Non-Goals

CMS, accounts, comments, analytics, newsletter, custom domain, live dashboard, installation guide, CV, Under the hood page.

## Dependencies And Blockers

S-005 owns reviews; S-006 data; S-007/008/009/010 linked capabilities. Missing results do not block the tour. Inspect sources/configuration before asking for input. Only consequential unresolved decisions or inaccessible required resources block affected criteria; name them precisely.

## Acceptance Criteria

Audit a named deployment. CI cannot establish editorial meaning.

- [ ] **Content:** rendered pages satisfy every brief. A reviewer can locate purpose, workflow, evidence limits and project identity; titles/slogans alone fail.
- [ ] **Route:** follow Quickstart without setup, reach example/evidence and return. Public revision-pinned Spec/Task sources survive record moves.
- [ ] **Scope:** sibling subjects have meaningful introductions/working links. No CV dependency, separate build-history page or live controls.
- [ ] **Data:** inspect populated, empty, pending and failed reads. Empty/unavailable differ; retained data has its read time; no fabricated/test evidence. S-007 also meets its own criteria.
- [ ] **Presentation:** at 375px and desktop, both themes, text/controls are readable without horizontal page overflow. Keyboard operation has visible focus; contrast meets WCAG AA; reduced motion is respected. Shared tokens match their source.
- [ ] **Trust:** SHA matches deployment; core text works without scripts; sources resolve; public output has no secrets, host paths or private evidence. Only permitted resource loads.
- [ ] **Approval:** unapproved/changed content is draft; only sourced owner approval removes it for bound content. Human QA and promotion remain separate.

## Verification Procedure

At a recorded deployed URL/commit, inspect content/links, data states against known inputs, keyboard, themes and widths. Record each criterion’s evidence/gap. Automation proves neither comprehension nor human approval.

## Documentation Impact

S-007 consumes data states/build explanation; S-008 explains skills. Assignments follow this Spec.

## Review and Human QA

Bind evidence and Kayden’s Grill Board judgments to the candidate. Checks, merges and deployment alone are not acceptance.

## Completion Result

Pending audit and Kayden's judgments. History is in the [website Wiki](../../../../wiki/context-website-presentation.md), not acceptance of this destination.

## Remaining Limitations Or Follow-Up Specs

Video remains undecided, not a gate.
