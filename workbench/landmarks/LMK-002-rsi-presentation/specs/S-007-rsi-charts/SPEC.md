# S-007 - RSI chart pages

**Spec ID:** S-007
**Status:** active
**Priority:** 2
**Owner:** Kayden; orchestrator A (Website, cloud)
**Stance:** Builder
**Updated:** 2026-11-03
**Catalog description:** Website pages that chart RSI results from Supabase, present and honestly empty from the first deploy, with every number linked to its rows.
**Blockers:** none
**Confirmation:** [JOT-9a370da6-d1ec-4f3f-a998-3dbbd7d82df1](../../../../wiki/context-active-spec-approvals.md)
**Execution approval:** [JOT-9a370da6-d1ec-4f3f-a998-3dbbd7d82df1](../../../../wiki/context-active-spec-approvals.md)
**Next gate:** Complete TK-002.

## Intent and authority

The [owner intent](../../../../wiki/context-feedback-improvement-loop-plan.md#jot-55876e5d-6957-4a4e-917b-8ba7245adee2) authorizes Map/Plan preparation; implementation and trial holds remain.

The owner named "a site page showing the improvement charts" as an example Spec, asked that chart places exist from the start so the owner can see where data will appear, and ruled out fabricated data.

## Outcome

A reader sees how skills and the build changed over time, per task and per version, including no change and regressions, and can follow any number to the rows behind it.

## Why It Matters

The site exists partly to show whether the loop works. Only traceable, labeled numbers can show that without overclaiming.

## Current Verified State

- **Not met:** every acceptance criterion. [TK-001](tasks/TK-001/TASK.md#receipt) (honest empty state slice) is done with its receipt; the criterion is not yet checked here.
- **Blocked:** [TK-002](tasks/TK-002/TASK.md) and [TK-003](tasks/TK-003/TASK.md), as their records state.

History: [S-007 history](../../../../wiki/history/S-007.md).

## Desired Behavior

- Follow S-003's shared data contract: distinguish populated, successful-empty, loading and unavailable states; identify the last successful read and any retained data. A failed read never becomes “no trials.” Static explanations and chart spaces remain visible.
- Explain the website build using sourced S-006 build events alongside the measured results. Readable prose connects the events; it need not itself be stored as rows. Distinguish build activity, assessments and demonstrated improvement. This page supplies the build-evidence explanation; S-003 has no separate “Under the hood” page.

- Chart places for each planned series exist from the first deploy.
- **Empty state.** With no rows a chart says that no trials are recorded yet, explains what a task, trial and version are, and names the next expected event. No sample chart or placeholder number.
- Results are shown per task and per version; dev and held-out are visibly separate.
- Each series shows its provenance: provider, model, effort and system version. A model change starts a new series.
- Regressions, variants, removed versions and fired stop rules are shown.
- Every number links to its rows. Each row's strength label is shown.
- **Headlines** come only from held-out tasks, with the interval and the baseline. An interval including zero reads as no difference detected at this size.
- Synthetic or test rows never render.

### Learning evidence views

Provide per-skill and whole-Workbench views from S-006, joined to canonical failure IDs rather than copied independent logs. Show lifecycle stage/age and blockers, candidate lineage and dispositions, paired baseline/candidate results with regressions, and later-use recurrence per eligible use. Owner interventions, runtime and available usage metrics show effort alongside outcomes. A skill-by-case matrix distinguishes pass, failure, unrun and unavailable evidence.

Every displayed metric identifies its case set/version, actual model/host/skills, sample size, evidence strength and freshness. Keep fixed benchmark trends separate from expanded historical coverage; imports or improved detection cannot appear as worsening reliability. Distinguish development/held-out results, operational errors, Fitness/Alignment levels and demonstrated benefit. No independently maintained numeric website dataset replaces the canonical Supabase rows; explanatory prose and clearly labeled test fixtures remain allowed.

## Decisions And Contracts

- The page reads Supabase with the publishable key only.
- No claim of improved outcomes without held-out rows, controls, the prior version and an interval.

## Non-Goals

- Computing statistics in the browser with a different method than the loop's.
- A development view on Vercel.

## Dependencies And Blockers

- The Next scaffold on `dev` (enough for TK-001); S-003's shell styles the page once it lands. S-006 (data store) for non-empty states (TK-002, TK-003).

## Vertical Implementation Slices

Every Task targets `dev`: branch from `origin/dev`, PR into `dev`, and only the owner merges `dev` -> `main`. Stack: a Next.js route in `site/`, Supabase reads with the publishable key, the build, render tests on labeled fixtures and the protected `dev` deployment.

| Task | Slice | Status | Blockers | Proof |
|---|---|---|---|---|

## Acceptance Criteria

- [ ] **Feedback connection:** safe failures, stopped attempts, assessments and dispositions render from S-006 with source, scope, freshness and next action. Workflow explanations link changed steps to evidence. Activity/audits alone cannot imply benefit.
- [ ] **Read states:** populated, empty, pending and unavailable follow S-003; failed reads cannot mean zero results, retained data needs its timestamp.
- [ ] **Build explanation:** sourced activity links to results or explicitly absent evidence; no separate build-history page is required.
- [ ] **Empty state:** chart places remain visible and explain the next event; sample numbers presented as results fail.
- [ ] **Traceability:** every metric links to its rows; independent hand-maintained numeric chart data fails.
- [ ] **Comparable series:** model/contract/case-set changes are separated, with sample sizes and denominators. Imported counts cannot masquerade as recurrence rates.
- [ ] **Regressions:** failed and rejected candidates remain visible; hidden failures or upward-only selection fail.
- [ ] **Headlines:** require held-out evidence, controls, prior version and interval; an interval including zero means no difference detected.
- [ ] **Privacy:** synthetic/test rows and private evidence never render.
- [ ] **Learning views:** per-skill/Workbench case matrix, candidate lineage and later-use evidence distinguish loop operation, qualification, behavioral benefit and recurrence; unknown usage stays unknown.

## RSI and website connection

This is the RSI presentation. Rows come from S-002 through S-006.

## Testing Seams

- Render tests against labeled fixture data, including empty, regressing, variant and model-change cases.

## Verification Procedure

```bash
node workbench/tools/spec-workbench.mjs show S-007
# site test command named at Task planning
```

## Documentation Impact

- The tour links the chart pages; the glossary defines task, trial and version.

## Context and Evidence

History and prior evidence are maintained in the [website Wiki](../../../../wiki/context-website-presentation.md). Audit the candidate against this destination rather than inferring acceptance from earlier work.

## Review and Human QA

The owner reviews each chart page through its Grill Board card (S-005).

## Completion Result

Pending.

## Remaining Limitations Or Follow-Up Specs

- none

## Supersession

- Supersedes: the earlier site draft's results board criteria, including the "since last release" view (no development view on Vercel).
- Superseded by: none

## Feedback-loop planning boundary

This Map does not activate website implementation or held Tasks. Existing approval scopes and stopped experiments remain. See the [mapped owner intent](../../../../wiki/context-feedback-improvement-loop-plan.md#current-mapped-destination).
