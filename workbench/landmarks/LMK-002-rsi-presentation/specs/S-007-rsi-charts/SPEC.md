# S-007 - RSI chart pages

**Spec ID:** S-007
**Status:** active
**Priority:** 2
**Owner:** Kayden; orchestrator A (Website, cloud)
**Stance:** Builder
**Updated:** 2026-11-06
**Catalog description:** Traceable RSI charts from Supabase, with honest empty states.
**Blockers:** none
**Confirmation:** [JOT-9a370da6-d1ec-4f3f-a998-3dbbd7d82df1](../../../../wiki/context-active-spec-approvals.md)
**Execution approval:** [JOT-9a370da6-d1ec-4f3f-a998-3dbbd7d82df1](../../../../wiki/context-active-spec-approvals.md)
**Next gate:** Complete TK-003.

## Intent and authority

The [owner intent](../../../../wiki/context-feedback-improvement-loop-plan.md#jot-55876e5d-6957-4a4e-917b-8ba7245adee2) authorizes Map/Plan preparation; implementation and trial holds remain.

Owner requires chart places from the first deploy and no fabricated data.

## Outcome

Show skill/build changes per task/version, including no change and regressions, with every metric traceable to its rows.

## Why It Matters

Traceable, labeled evidence lets readers assess whether the loop works.

## Current Verified State

- Whole-Spec acceptance remains unverified. [TK-001](tasks/TK-001/TASK.md#receipt) closed the bounded empty-state slice.
- [TK-002](tasks/TK-002/TASK.md) closed the checked live reader; [proof and limits](tasks/TK-002/CURRENT-CHECK.md) retain failures and originals. Native accounting remains unverified; no workspace release, full closeout or Spec acceptance. TK-003 is next; lineage inputs remain unverified.

History: [S-007 history](../../../../wiki/history/S-007.md).

## Desired Behavior

- Follow S-003 data states: populated, successful-empty, loading and unavailable. Retained data identifies its last successful read; failure never means no trials. Keep explanations and chart places visible.
- Connect sourced S-006 build events and measured results with readable prose; prose need not be rows. Distinguish activity, assessment and demonstrated benefit. No separate Under-the-hood page.

- Chart places for each planned series exist from the first deploy.
- **Empty state.** With zero rows, explain no trials, task/trial/version meanings and the next event; no sample chart or placeholder number.
- Results are shown per task and per version; dev and held-out are visibly separate.
- Each series shows its provenance: provider, model, effort and system version. A model change starts a new series.
- Regressions, variants, removed versions and fired stop rules are shown.
- Trial numbers link to on-site rows with strength labels. Keep relevant explanations/evidence on-site, omit irrelevant material and GitHub exits; show real development comparisons without invented data.
- **Headlines** come only from held-out tasks, with the interval and the baseline. An interval including zero reads as no difference detected at this size.
- Synthetic or test rows never render.
- **Skill trends** ([TK-002J](tasks/TK-002J/TASK.md)): one point per skill per RSI loop (the kept version's Alignment Score and fitness level), per skill and in a level-per-loop strip; Excellent is green. Contract/model changes start new lines.

### Learning evidence views

Provide per-skill and whole-Workbench views from S-006, joined to canonical failure IDs rather than copied independent logs. Show lifecycle stage/age and blockers, candidate lineage and dispositions, paired baseline/candidate results with regressions, and later-use recurrence per eligible use. Owner interventions, runtime and available usage metrics show effort alongside outcomes. A skill-by-case matrix distinguishes pass, failure, unrun and unavailable evidence.

Metrics identify case set/version, actual model/host/skills, sample size, strength and freshness. Separate fixed benchmarks from expanded coverage: imports/better detection cannot imply worsening reliability. Distinguish development/held-out results, operational errors, Fitness/Alignment and benefit. Canonical Supabase rows supply numbers; prose and labeled test fixtures remain allowed.

## Decisions And Contracts

- The page reads Supabase with the publishable key only.
- No claim of improved outcomes without held-out rows, controls, the prior version and an interval.

## Non-Goals

- Computing statistics in the browser with a different method than the loop's.
- A development view on Vercel.

## Dependencies And Blockers

- The Next scaffold on `dev` (enough for TK-001); S-003's shell styles the page once it lands. S-006 (data store) for non-empty states (TK-002, TK-003).

## Vertical Implementation Slices

Tasks target checked `dev`; only the owner promotes to `main`. Stack: Next.js, publishable-key Supabase reads, build, labeled-fixture rendering and protected deployment readback.

| Task | Slice | Status | Blockers | Proof |
|---|---|---|---|---|

## Acceptance Criteria

- [ ] **Feedback loop connection:** safe failures, stopped attempts, assessments and dispositions render from S-006 with source, scope, freshness and next action. Workflow explanations link changed steps to evidence. Activity/audits alone cannot imply benefit.
- [ ] **Read states:** populated, empty, pending and unavailable follow S-003; failed reads cannot mean zero results, retained data needs its timestamp.
- [ ] **Build explanation:** sourced activity links to results or explicitly absent evidence; no separate build-history page is required.
- [ ] **Empty state:** chart places remain visible and explain the next event; sample numbers presented as results fail.
- [ ] **Traceability:** every metric links to its rows; independent hand-maintained numeric chart data fails.
- [ ] **Comparable series:** model/contract/case-set changes are separated, with sample sizes and denominators. Imported counts cannot masquerade as recurrence rates.
- [ ] **Regressions:** failed and rejected candidates remain visible; hidden failures or upward-only selection fail.
- [ ] **Headlines:** require held-out evidence, controls, prior version and interval; an interval including zero means no difference detected.
- [ ] **Privacy:** synthetic/test rows and private evidence never render.
- [ ] **Learning views:** per-skill/Workbench case matrix, candidate lineage and later-use evidence distinguish loop operation, qualification, behavioral benefit and recurrence; unknown usage stays unknown.
- [ ] **Skill trends:** a contract or model change in one line, a point from a rejected attempt or High/Small run, or an invented loop fails. Rejected and failed attempts remain visible separately from qualified trend points.

## RSI and website connection

This is the RSI presentation. Rows come from S-002 through S-006.

## Testing Seams

- Labeled render fixtures: empty, regressing, variant and model-change cases.

## Verification Procedure

```bash
node workbench/tools/spec-workbench.mjs show S-007
# site test command named at Task planning
```

## Documentation Impact

- The tour links the chart pages; the glossary defines task, trial and version.

## Context and Evidence

[TK-001W](tasks/TK-001W/TASK.md) records bounded checker-presentation checks; the [website Wiki](../../../../wiki/context-website-presentation.md) retains prior evidence. Live data and assembled acceptance remain open; audit this destination, not prior success labels.

## Review and Human QA

Owner Human QA uses S-005 page cards.

## Completion Result

Pending.

## Remaining Limitations Or Follow-Up Specs

- none

## Supersession

- Supersedes: the earlier site draft's results board criteria, including the "since last release" view (no development view on Vercel).
- Superseded by: none

## Feedback-loop planning boundary

This Map does not activate website implementation or held Tasks. Existing approval scopes and stopped experiments remain. See the [mapped owner intent](../../../../wiki/context-feedback-improvement-loop-plan.md#current-mapped-destination).
