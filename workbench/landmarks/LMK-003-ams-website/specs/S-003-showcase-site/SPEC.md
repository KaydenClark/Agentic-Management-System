# S-003 - Website shell and AMS orientation

**Spec ID:** S-003
**Status:** active
**Priority:** 1
**Owner:** Kayden; orchestrator A (Website, cloud)
**Stance:** Builder
**Updated:** 2026-11-03
**Catalog description:** Explain AMS and its evidence.
**Blockers:** none
**Next gate:** Close TK-001S with verification and documentation proof.
**Confirmation:** [JOT-5b41bab8-c88f-49c4-be9c-b438285490b0](../../../../wiki/context-active-spec-approvals.md)
**Execution approval:** [JOT-5b41bab8-c88f-49c4-be9c-b438285490b0](../../../../wiki/context-active-spec-approvals.md)

## Intent and authority

The [owner brief](../../../../wiki/context-website-presentation.md) governs shell/orientation; sibling Specs remain required. Execution: [owner assignment](../../../../wiki/context-website-presentation.md#jot-4adf0b91-665d-4abb-8644-4835b40e905a).

## Outcome

Explain what AMS manages, why, how intent becomes work/feedback and what evidence demonstrates, plainly for non-engineers with sources for technical readers. Present AMS without operating it.

## Why It Matters

Visitors can examine whether real work supports AMS claims.

## Current Verified State

No criterion is verified; none is audited at a named deployment.

History: [S-003 history](../../../../wiki/history/S-003.md).

## Desired Behavior

Pages explain ideas before IDs and define unfamiliar terms. Agents draft from approved records and owner feedback.

### Approved presentation feedback

The [approved feedback](../../../../wiki/context-website-presentation.md#jot-74a9fff6-dcf2-4e5b-91fb-8ae4765c9458) consolidates overlapping orientation pages: Start Here serves as About; retain the subjects below. Tasks TK-001P–TK-001T cover orientation, persistent full-width navigation (Home left, theme right), visual glossary, larger text and visible Grill Board colors in both themes. Execute shared-file Tasks serially under the owner assignment.

The [website-only link readback](../../../../wiki/context-website-presentation.md#jot-78d8b232-f2c6-4697-ab8c-9e25f60760ba) is pending before its Task. RSI links now follow its approved readback; other pages await confirmation.

### Orientation content

- **Start here** (`/start`, includes Quickstart): define AMS from the glossary, this project’s RSI addition and problem, and this website as its first outside product. Explain the route through introduction, real-work example, demonstration/skills and RSI evidence/limits, including what each teaches. Distinguish presentation from live controls. Name `setup-workbench` for Workbench setup; no command replay.
- **Why:** connect intent/corrections, delegated work and learning from failures to this build. Distinguish intended benefits from measured results; link RSI evidence.
- **How it works:** explain intent -> Landmark -> Spec -> Task -> implementation, checks, review, human judgment and delivery through one real sourced example. Explain feedback returning to its owner and failed results starting bounded RSI comparisons. Link governance/flow charts; distinguish achieved from intended behavior.
- **Limits:** the site runs no agents or record writes. Distinguish demos, activity, assessments and demonstrated improvement. Source capability limits and explain required human judgment.
- **Glossary:** define tour terms consistently with the root glossary, including implementation Tasks versus evaluation tasks/trials. Link definitions from their uses and back to the explanation.
- **About AMS:** explain the project, creator, purpose and relationship to this website; no employment history or CV requirement.

### Shell and related capabilities

Navigation shows current page, tour order/start/finish and direct subject links, without dead ends. Core text works without scripts. Light/dark follows system or manual override. Every page displays its deployed SHA on-site.

Introduce and link RSI charts (S-007), site-written skill summaries (S-008), the demo Grill Board with non-engineering sample questions (S-009), and governance/flow charts (S-010). Keep private skill source private.

No build-history/“Under the hood” page. S-007 explains S-006 build evidence/results; S-008 explains skills. Sourced prose need not map each sentence to a database row. Activity proves no improvement.

### Data and approvals

Read-only Supabase with publishable key; Python writes under S-006; service key stays local (ADR-003H). Shared states, including S-007:

- **Populated:** retain source/event/version identity and last successful read time.
- **Empty successful read:** explain no matching records and what belongs there. Keep chart spaces; no invented numbers/results.
- **Pending/failed:** distinguish loading, unavailable and zero results. Timestamp retained data; static explanations stay readable.
- Test/synthetic rows never appear as real evidence. S-007 owns result labels/comparisons; S-006 owns storage/access.

No page shows draft, approval or review status; page review stays on S-005's Grill Board cards (DDR-001B). No page quotes Kayden or uses his agent instructions as examples; paraphrase and link sources (DDR-001A).

## Decisions And Contracts

- Next.js in `site/`, Python backends, no FastAPI, free Vercel address. Feature -> protected `dev` -> `main`; only Kayden approves promotion. A holds no service key and deploys through Git pushes to `dev`.
- No third-party scripts, remote fonts, tracking or cookies. Resource loads: site/Supabase; GitHub links are navigation.
- Theme/fonts follow [DDR-000Y](../../../../docs/ddr/000Y-the-grill-board-theme-follows-the-grilling-board-redesign-artifact.md). Shared values match `grill-board/theme/tokens.json` in both themes. Site type/spacing is consistent; no equality to absent tokens.

## Non-Goals

CMS, accounts, comments, analytics, newsletter, custom domain, live dashboard, installation guide, CV, Under the hood or `/quickstart` page.

## Dependencies And Blockers

S-005 owns reviews; S-006 data; S-007/008/009/010 linked capabilities. Missing results do not block the tour. Inspect sources before asking; name real missing inputs or consequential decisions.

## Acceptance Criteria

Audit a named deployment; CI cannot prove editorial meaning.

- [ ] **Content:** satisfy each brief with explanations of purpose, workflow, evidence limits and project identity; titles alone fail.
- [ ] **Route:** follow Start here's route without setup, reach example/evidence and return; it names `setup-workbench`. Public revision-pinned Spec/Task sources survive record moves.
- [ ] **Scope:** sibling subjects have meaningful introductions/working links. No CV dependency, separate build-history page or live controls.
- [ ] **Data:** inspect populated, empty, pending and failed reads. Empty/unavailable differ; retained data has its read time; no fabricated/test evidence. S-007 also meets its own criteria.
- [ ] **Feedback:** demonstrate each approved presentation change above at desktop and 375px in both themes.
- [ ] **Presentation:** readable text/controls at 375px and desktop in both themes, no horizontal overflow, visible keyboard focus, WCAG AA contrast, reduced motion and matching shared tokens.
- [ ] **Trust:** deployed SHA matches; script-free core text, resolving sources, permitted resource loads and no secrets, host paths or private evidence.
- [ ] **Owner presentation:** no page shows review status, owner quotations or owner instructions as examples.

## Verification Procedure

At a named deployment/commit, inspect content/links, known data states, keyboard, themes and widths. Record evidence/gaps per criterion; automation proves neither comprehension nor human approval.

## Documentation Impact

S-007 consumes data states/build explanation; S-008 explains skills. Assignments follow this Spec.

## Review and Human QA

Bind evidence and Kayden’s Grill Board judgments to the candidate; checks, merges and deployment do not grant acceptance.

## Completion Result

Pending audit and Kayden's judgments.

## Remaining Limitations Or Follow-Up Specs

Video is undecided; no gate.
