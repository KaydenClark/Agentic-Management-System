# S-007 - RSI chart pages

**Spec ID:** S-007
**Status:** active
**Priority:** 2
**Owner:** Kayden; orchestrator A (Website, cloud)
**Stance:** Builder
**Updated:** 2026-11-07
**Catalog description:** Website pages that chart RSI results from Supabase, present and honestly empty from the first deploy, with every number linked to its rows.
**Blockers:** none
**Confirmation:** [JOT-9a370da6-d1ec-4f3f-a998-3dbbd7d82df1](../../../../wiki/context-active-spec-approvals.md)
**Execution approval:** [JOT-9a370da6-d1ec-4f3f-a998-3dbbd7d82df1](../../../../wiki/context-active-spec-approvals.md)
**Next gate:** Complete TK-002.

## Intent and authority

[RSI Map source](../../../../wiki/context-feedback-improvement-loop-plan.md#jot-7862917b-48cb-41bc-8f21-0ddfc611cdac); no execution release or reset of prior stops.

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

- Follow S-003’s populated, successful-empty, loading and unavailable states; show last successful read and retained-data timestamp. A failed read is never “no trials.” Static explanations/chart spaces remain visible from first deploy.
- An empty chart says no trials are recorded, explains task/trial/version and the next expected event. Never fabricate sample results. Synthetic/test rows do not render.
- Explain the website build from sourced S-006 events, linking activity to results or absent evidence. S-003 needs no separate build-history page. Prose may explain; Supabase owns displayed numbers.
- Show per-task/version results, development versus held-out, provider/model/effort/system/skills/host, source/strength, sample size/denominators and freshness. Model/contract/case-set changes form distinct series. Imports or broader detection cannot masquerade as worsening reliability. Every number links to rows.
- Display regressions, failed attempts, rejected/removed versions, variants and fired stops. Public improvement headlines require held-out tasks, controls, prior version/baseline and interval; an interval containing zero means no detected difference at that size.
- Per-skill and whole-Workbench views join canonical failure IDs, lifecycle stage/age/blockers, candidate lineage/dispositions, paired comparisons and later recurrence per eligible use. Show owner interventions, runtime and available usage alongside outcomes. A skill/case matrix distinguishes pass, failure, unrun and unavailable.
- Skill results separately show Quality Score, Regression Score, Critical result and severity grade, with actual completed audit counts (even fewer than three), versioned denominators and qualification limits. Whole-Workbench Alignment is a separately labeled assessment; activity/audits alone prove no benefit/generalization.
- Distinguish request, loading and use failures. Skipped explicit requests count as Critical failed requested uses. Later-use views identify accepted versions actually loaded; no uses means no recurrence rate, not a proven fix. No hand-maintained numeric website dataset replaces Supabase.

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

## Acceptance Criteria

- [ ] **Actual audits:** two stored runs display two, never the intended three; failed or unavailable reads do not imply zero audits. The synthetic 95% Quality / 100% Regression / Critical failure example displays Broken and cannot be mistaken for live results.
- [ ] **Separate meanings:** skill grades, each score, Critical results and whole-Workbench Alignment remain distinct. Accepted-but-not-loaded and no-later-use states cannot imply success or zero recurrence.

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

Map releases no website work or held Tasks; prior scopes/stops remain.
