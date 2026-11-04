# S-007 - RSI chart pages

**Spec ID:** S-007
**Status:** active
**Priority:** 2
**Owner:** Kayden; orchestrator A (Website, cloud)
**Stance:** Builder
**Updated:** 2026-11-04
**Catalog description:** Website pages that chart RSI results from Supabase, present and honestly empty from the first deploy, with every number linked to its rows.
**Blockers:** none
**Confirmation:** [JOT-9a370da6-d1ec-4f3f-a998-3dbbd7d82df1](../../../../wiki/context-active-spec-approvals.md)
**Execution approval:** [JOT-9a370da6-d1ec-4f3f-a998-3dbbd7d82df1](../../../../wiki/context-active-spec-approvals.md)
**Next gate:** Complete TK-002.

## Intent and authority

The owner named "a site page showing the improvement charts" as an example Spec, asked that chart places exist from the start so the owner can see where data will appear, and ruled out fabricated data.

## Outcome

A reader sees how skills and the build changed over time, per task and per version, including no change and regressions, and can follow any number to the rows behind it.

## Why It Matters

The site exists partly to show whether the loop works. Only traceable, labeled numbers can show that without overclaiming.

## Current Verified State

- **Not met:** every acceptance criterion. [TK-001](tasks/TK-001/TASK.md#receipt) (honest empty state slice) is done with its receipt; the criterion is not yet checked here.
- **In progress:** [TK-002](tasks/TK-002/TASK.md) resumes the retained live reader with actual safe S-011 development evidence; required table/source inputs are delivered. Dev publication and deployment readback remain unverified. [TK-003](tasks/TK-003/TASK.md) still waits on TK-002. No skill improvement or Spec acceptance is inferred.

History: [S-007 history](../../../../wiki/history/S-007.md).

## Desired Behavior

- Follow S-003's shared data contract: distinguish populated, successful-empty, loading and unavailable states; identify the last successful read and any retained data. A failed read never becomes “no trials.” Static explanations and chart spaces remain visible.
- Explain the website build using sourced S-006 build events alongside the measured results. Readable prose connects the events; it need not itself be stored as rows. Distinguish build activity, assessments and demonstrated improvement. This page supplies the build-evidence explanation; S-003 has no separate “Under the hood” page.

- Chart places for each planned series exist from the first deploy.
- **Empty state.** With no rows a chart says that no trials are recorded yet, explains what a task, trial and version are, and names the next expected event. No sample chart or placeholder number.
- Results are shown per task and per version; dev and held-out are visibly separate.
- Each series shows its provenance: provider, model, effort and system version. A model change starts a new series.
- Regressions, variants, removed versions and fired stop rules are shown.
- Every trial number links to its rows on-site. Each row's strength label is shown. Relevant explanations and evidence stay on the site; omit irrelevant material and GitHub exits. Show real development comparisons visibly without inventing trial data.
- **Headlines** come only from held-out tasks, with the interval and the baseline. An interval including zero reads as no difference detected at this size.
- Synthetic or test rows never render.
- **Skill trends** ([TK-002J](tasks/TK-002J/TASK.md)): one point per skill per RSI loop (the kept version's Alignment Score and fitness level), per skill and in a level-per-loop strip; Excellent is green. A contract or model change starts a new line.

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

- [ ] **Feedback loop connection:** Progress is visible: safe existing failures, assessments, stopped attempts and dispositions are read through S-006 and rendered on dev with source, scope, freshness and next action. A versioned workflow explanation links each changed step to its reason/evidence. Failed reads cannot appear as no activity, and activity/audit scores cannot become improvement claims.

- [ ] **Shared data states.** Populated, empty, pending and failed reads satisfy [S-003's contract](../../../LMK-003-ams-website/specs/S-003-showcase-site/SPEC.md#data-and-approvals). A failed read shown as zero results fails; retained data without its read time fails.
- [ ] **Build explanation.** A reader can follow sourced build activity into its related results or an explicit statement that no measured result exists. Activity alone is never labeled improvement; explanatory prose is allowed. No separate build-history page is required.

- [ ] **Honest empty state.** With zero rows the page builds, shows each chart place and the "no trials yet" explanation. *Check:* render against an empty fixture. *Must fail:* a hidden section, a sample chart or any number.
- [ ] **Every number links.** Each rendered trial number links to its rows on-site. *Check:* link coverage over trial numbers. *Must fail:* a bare number.
- [ ] **Provenance and series.** Two models never share one trend line. *Must fail:* a model change drawn as a continuation.
- [ ] **Not only up.** Regressions and variants are marked as such. *Must fail:* a timeline that hides a recorded regression.
- [ ] **Skill trends.** *Must fail:* a contract or model change in one line, a point from a rejected attempt or High/Small run, or an invented loop.
- [ ] **Held-out headlines.** A headline appears only from held-out rows, with its interval and baseline. *Must fail:* a dev-task number as a headline, or an interval including zero shown as improvement.
- [ ] **No test rows.** A marked test row in the fixture never renders.

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

The bounded checker-evidence presentation and its checks are recorded in [TK-001W](tasks/TK-001W/TASK.md); live data and assembled acceptance remain open.

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

Owner instruction, 2026-11-02, held in the [cross-Spec plan](../../../../wiki/context-feedback-improvement-loop-plan.md): TK-001F keeps its execution hold; earlier approvals and evidence keep their scope.
