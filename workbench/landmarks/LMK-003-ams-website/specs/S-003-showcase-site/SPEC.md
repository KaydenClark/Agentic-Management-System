# S-003 - Website shell and AMS orientation

**Spec ID:** S-003
**Status:** active
**Priority:** 1
**Owner:** Kayden; orchestrator A (Website, cloud)
**Stance:** Builder
**Updated:** 2026-11-02
**Catalog description:** Explain AMS and its evidence.
**Blockers:** none
**Next gate:** Assign feedback Tasks; confirm website-only link readback.
**Confirmation:** [JOT-5b41bab8-c88f-49c4-be9c-b438285490b0](../../../../wiki/context-active-spec-approvals.md)
**Execution approval:** [JOT-5b41bab8-c88f-49c4-be9c-b438285490b0](../../../../wiki/context-active-spec-approvals.md)

## Intent and authority

The owner's [brief and corrections](../../../../wiki/context-website-presentation.md) establish this destination. S-003 owns shell/orientation; siblings remain required in the four-Landmark build. This revision authorizes specification repair only.

## Outcome

Visitors come for understanding: what AMS manages, why, how intent becomes work/feedback and what evidence demonstrates. Non-engineers get plain explanations; technical readers can follow sources. The website presents AMS without operating it.

## Why It Matters

Visitors can examine whether real work supports AMS claims.

## Current Verified State

No criterion is verified; none is audited at a named deployment.

History: [S-003 history](../../../../wiki/history/S-003.md).

## Desired Behavior

Pages explain ideas before IDs and define unfamiliar terms. Agents draft from approved records and owner feedback.

### Approved presentation feedback

The [2026-11-02 owner readback](../../../../wiki/context-website-presentation.md#jot-74a9fff6-dcf2-4e5b-91fb-8ae4765c9458) supersedes separate overlapping orientation pages: Start Here serves as About; preserve the explanatory subjects below while consolidating their presentation. Five prepared Tasks, TK-001P through TK-001T, cover coherent orientation, persistent full-width navigation (Home icon left, theme toggle right), visual glossary, larger readable text and visible Grill Board colors in both themes. Execute serially because they share files; preparation grants no implementation authority.

The [website-only link readback](../../../../wiki/context-website-presentation.md#jot-78d8b232-f2c6-4697-ab8c-9e25f60760ba) is pending before its Task. It conflicts with the GitHub source/SHA requirements below; do not invent an exception.

### Orientation content

- **Start here** (`/start`, includes Quickstart): define AMS from the glossary, this project’s RSI addition and problem, and this website as its first outside product. Explain the route through introduction, real-work example, demonstration/skills and RSI evidence/limits, including what each teaches. Distinguish presentation from live controls. Name `setup-workbench` for Workbench setup; no command replay.
- **Why:** explain preserving intent/corrections, organizing delegated work and learning from failures. Connect these purposes to this build. Separate intended benefits from measured results; link RSI evidence.
- **How it works:** explain intent -> Landmark -> Spec -> Task -> implementation, checks, review, human judgment and delivery through one real sourced example. Explain feedback returning to its owner and failed results starting bounded RSI comparisons. Link governance/flow charts; distinguish achieved from intended behavior.
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

Audit a named deployment. CI cannot establish editorial meaning.

- [ ] **Content:** rendered pages satisfy every brief. A reviewer can locate purpose, workflow, evidence limits and project identity; titles/slogans alone fail.
- [ ] **Route:** follow Start here's route without setup, reach example/evidence and return; it names `setup-workbench`. Public revision-pinned Spec/Task sources survive record moves.
- [ ] **Scope:** sibling subjects have meaningful introductions/working links. No CV dependency, separate build-history page or live controls.
- [ ] **Data:** inspect populated, empty, pending and failed reads. Empty/unavailable differ; retained data has its read time; no fabricated/test evidence. S-007 also meets its own criteria.
- [ ] **Feedback:** coherent orientation with Start Here presented as About; persistent full-width navigation with Home icon left and theme toggle right; visual glossary; larger readable text; visible Grill Board colors in both themes.
- [ ] **Presentation:** at 375px and desktop, both themes, text/controls are readable without horizontal page overflow. Keyboard operation has visible focus; contrast meets WCAG AA; reduced motion is respected. Shared tokens match their source.
- [ ] **Trust:** SHA matches deployment; core text works without scripts; sources resolve; public output has no secrets, host paths or private evidence. Only permitted resource loads.
- [ ] **Owner presentation:** no page shows review status, owner quotations or owner instructions as examples.

## Verification Procedure

At a recorded deployed URL/commit, inspect content/links, data states against known inputs, keyboard, themes and widths. Record each criterion’s evidence/gap. Automation proves neither comprehension nor human approval.

## Documentation Impact

S-007 consumes data states/build explanation; S-008 explains skills. Assignments follow this Spec.

## Review and Human QA

Bind evidence and Kayden’s Grill Board judgments to the candidate. Checks, merges and deployment alone are not acceptance.

## Completion Result

Pending audit and Kayden's judgments.

## Remaining Limitations Or Follow-Up Specs

Video remains undecided, not a gate.
