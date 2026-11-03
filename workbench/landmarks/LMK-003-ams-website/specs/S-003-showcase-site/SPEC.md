# S-003 - Website shell and AMS orientation

**Spec ID:** S-003
**Status:** active
**Priority:** 1
**Owner:** Kayden; orchestrator A (Website, cloud)
**Stance:** Builder
**Updated:** 2026-11-03
**Catalog description:** Explain AMS and its evidence.
**Blockers:** none
**Next gate:** Owner retry of TK-001Q focused-link clipping; then TK-001R/T and TK-002B.
**Confirmation:** [JOT-5b41bab8-c88f-49c4-be9c-b438285490b0](../../../../wiki/context-active-spec-approvals.md)
**Execution approval:** [JOT-5b41bab8-c88f-49c4-be9c-b438285490b0](../../../../wiki/context-active-spec-approvals.md)

## Intent and authority

The [owner brief](../../../../wiki/context-website-presentation.md) governs shell/orientation; sibling Specs remain required. Execution: [owner assignment](../../../../wiki/context-website-presentation.md#jot-4adf0b91-665d-4abb-8644-4835b40e905a).

## Outcome

Explain AMS purpose, intent-to-work/feedback and evidence, plainly for non-engineers with technical sources. Present AMS without operating it.

## Why It Matters

Visitors can test AMS claims against real work.

## Current Verified State

No criterion is verified; none is audited at a named deployment.

History: [S-003 history](../../../../wiki/history/S-003.md).

## Desired Behavior

Explain ideas before IDs and define terms. Draft from approved records and owner feedback.

### Approved presentation feedback

The [approved feedback](../../../../wiki/context-website-presentation.md#jot-74a9fff6-dcf2-4e5b-91fb-8ae4765c9458) consolidates overlapping orientation pages: Start Here serves as About; retain the subjects below. TK-001P–TK-001T cover orientation, persistent full-width navigation (Home left/theme right), visual glossary, larger text and visible Grill Board colors in both themes. Serialize shared writes.

The [confirmed link readback](../../../../wiki/context-website-presentation.md#jot-09260032-786b-47fb-8c71-1d7c4f387bb2) requires on-site examples/evidence, useful material retained and irrelevant material omitted. Preserve source/revision identities; no GitHub exits, including footer/source links.

### Orientation content

- **About / Start here** (`/start`, Quickstart included): define glossary AMS, this project’s RSI addition/problem and this site as its first outside product. Explain the route through orientation, sourced work, demonstration/skills and RSI evidence/limits, and what each teaches. Distinguish presentation/live controls; name `setup-workbench`; no command replay.
- **Why:** connect intent/corrections, delegated work and learning from failures to this build. Distinguish intended benefits from measured results; link RSI evidence.
- **How it works:** explain intent -> Landmark -> Spec -> Task -> implementation, checks, review, human judgment and delivery through a real sourced example. Return feedback to its owner and failures to bounded RSI comparisons. Link governance/flow charts; distinguish achieved/intended behavior.
- **Limits:** no agents or record writes run here. Distinguish demos, activity, assessments and demonstrated improvement; source limits and required human judgment.
- **Glossary:** use root glossary meanings, distinguishing implementation Tasks/evaluation tasks/trials. Link uses to definitions and back to explanations.
- **About AMS:** explain the project, creator, purpose and relationship to this website; no employment history or CV requirement.

### Shell and related capabilities

Navigation shows current page, tour order/start/finish and direct subject links, without dead ends. Core text works script-free. Light/dark follows system or manual override. Every page displays its deployed SHA on-site.

Introduce/link RSI charts (S-007), site-written skill summaries (S-008), the demo Grill Board with non-engineering questions (S-009), and governance/flow charts (S-010). Keep private skill source private.

No Under-the-hood/build-history page. S-007 explains S-006 evidence/results; S-008 explains skills. Prose need not map every sentence to a row. Activity proves no improvement.

### Data and approvals

Supabase read-only/publishable key; Python writes (S-006); service key local (ADR-003H). Shared states, including S-007:

- **Populated:** retain source/event/version identity and last successful read time.
- **Empty successful read:** explain no matching records and what belongs there. Keep chart spaces; no invented numbers/results.
- **Pending/failed:** distinguish loading, unavailable and zero results. Timestamp retained data; static explanations stay readable.
- Test/synthetic rows never appear as real evidence. S-007 owns result labels/comparisons; S-006 owns storage/access.

No public draft/approval/review status: page review stays on S-005 Grill Board cards (DDR-001B). No Kayden quotations or actual agent instructions as examples; paraphrase with on-site sources (DDR-001A).

## Decisions And Contracts

- Next.js in `site/`, Python backends, no FastAPI, free Vercel address. Feature -> protected `dev` -> `main`; only Kayden approves promotion. A holds no service key and deploys through Git pushes to `dev`.
- No third-party scripts, remote fonts, tracking or cookies. Resource loads: site/Supabase; Reader links stay on-site.
- Theme/fonts follow [DDR-000Y](../../../../docs/ddr/000Y-the-grill-board-theme-follows-the-grilling-board-redesign-artifact.md). Shared values match `grill-board/theme/tokens.json` in both themes. Site type/spacing is consistent; no equality to absent tokens.

## Non-Goals

CMS, accounts, comments, analytics, newsletter, custom domain, live dashboard, installation guide, CV, Under the hood or `/quickstart` page.

## Dependencies And Blockers

S-005 owns reviews; S-006 data; S-007/008/009/010 linked capabilities. Missing results do not block the tour. Inspect sources before asking; name real missing inputs or consequential decisions.

## Acceptance Criteria

Audit a named deployment; CI proves no comprehension.

- [ ] **Content:** satisfy each brief with explanations of purpose, workflow, evidence limits and project identity; titles alone fail.
- [ ] **Route:** follow Start here's route without setup, reach example/evidence and return; it names `setup-workbench`. On-site sourced examples preserve revision identity and survive record moves.
- [ ] **Scope:** sibling subjects have meaningful introductions/working links. No CV dependency, separate build-history page or live controls.
- [ ] **Data:** inspect populated, empty, pending and failed reads. Empty/unavailable differ; retained data has its read time; no fabricated/test evidence. S-007 also meets its own criteria.
- [ ] **Feedback:** demonstrate each approved presentation change above at desktop and 375px in both themes.
- [ ] **Presentation:** readable text/controls at 375px and desktop in both themes, no horizontal overflow, visible keyboard focus, WCAG AA contrast, reduced motion and matching shared tokens.
- [ ] **Trust:** deployed SHA matches; script-free core text, resolving sources, permitted resource loads and no secrets, host paths or private evidence.
- [ ] **Owner presentation:** no page shows review status, owner quotations or owner instructions as examples.

## Verification Procedure

At a named deployment/commit, inspect content/links, data states, keyboard, themes and widths; record evidence/gaps per criterion. Automation proves no comprehension or human approval.

## Documentation Impact

S-007 consumes data states/build explanation; S-008 explains skills. Assignments follow this Spec.

## Review and Human QA

Bind evidence and Kayden’s Grill Board judgments to the candidate. Checks, merges and deployment grant no acceptance.

## Completion Result

Pending audit and Kayden's judgments.

## Remaining Limitations Or Follow-Up Specs

Video is undecided; no gate.
