# S-007 - RSI chart pages

**Spec ID:** S-007
**Status:** planned
**Priority:** 2
**Owner:** Kayden; orchestrator A (Website, cloud)
**Stance:** Builder
**Updated:** 2026-11-01
**Catalog description:** Website pages that chart RSI results from Supabase, present and honestly empty from the first deploy, with every number linked to its rows.
**Blockers:** S-003
**Latest event:** Mapped from the owner's confirmed decisions of 2026-11-01.
**Next gate:** Task planning after the site shell (S-003) exists.

## Intent and authority

The owner named "a site page showing the improvement charts" as an example Spec, asked that chart places exist from the start so the owner can see where data will appear, and ruled out fabricated data.

## Outcome

A reader sees how skills and the build changed over time, per task and per version, including no change and regressions, and can follow any number to the rows behind it.

## Why It Matters

The site exists partly to show whether the loop works. Only traceable, labeled numbers can show that without overclaiming.

## Current Verified State

- No site pages and no RSI rows exist.

## Desired Behavior

- Chart places for each planned series exist from the first deploy.
- **Empty state.** With no rows a chart says that no trials are recorded yet, explains what a task, trial and version are, and names the next expected event. No sample chart or placeholder number.
- Results are shown per task and per version; dev and held-out are visibly separate.
- Each series shows its provenance: provider, model, effort and system version. A model change starts a new series.
- Regressions, variants, removed versions and fired stop rules are shown.
- Every number links to its rows. Each row's strength label is shown.
- **Headlines** come only from held-out tasks, with the interval and the baseline. An interval including zero reads as no difference detected at this size.
- Synthetic or test rows never render.

## Decisions And Contracts

- The page reads Supabase with the publishable key only.
- No claim of improved outcomes without held-out rows, controls, the prior version and an interval.

## Non-Goals

- Computing statistics in the browser with a different method than the loop's.
- A development view on Vercel.

## Dependencies And Blockers

- S-003 (site shell); S-006 (data store) for non-empty states.

## Vertical Implementation Slices

| Task | Slice | Status | Blockers | Proof |
|---|---|---|---|---|
| TK-001 | Chart page with every series place and the honest empty state, deployed to `dev` | ready | none | pending |
| TK-002 | Render rows from Supabase per task and version with links and strength labels | ready | TK-001 | pending |
| TK-003 | Held-out headline with interval and baseline; zero-crossing wording | ready | TK-002 | pending |

### TK-001 - Empty but present

**Stance:** Builder

Proves the empty-state criterion.

### TK-002 - Rows to charts

**Stance:** Builder

Proves the link, provenance and synthetic-row criteria.

### TK-003 - Headline rules

**Stance:** Builder

Proves the headline criterion.

## Acceptance Criteria

- [ ] **Honest empty state.** With zero rows the page builds, shows each chart place and the "no trials yet" explanation. *Check:* render against an empty fixture. *Must fail:* a hidden section, a sample chart or any number.
- [ ] **Every number links.** Each rendered number links to its rows. *Check:* a link-coverage test over rendered numbers. *Must fail:* a bare number.
- [ ] **Provenance and series.** Two models never share one trend line. *Must fail:* a model change drawn as a continuation.
- [ ] **Not only up.** Regressions and variants are marked as such. *Must fail:* a timeline that hides a recorded regression.
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

## Append-Only Evidence And Execution Log

| Date | Task | Event | Verification | Docs | Remaining gap |
|---|---|---|---|---|---|
| 2026-11-01 | none | Mapped as planned | render, doctor | this Spec | Every criterion |

## Review and Human QA

The owner reviews each chart page through its Grill Board card (S-005).

## Completion Result

Pending.

## Remaining Limitations Or Follow-Up Specs

- none

## Supersession

- Supersedes: the earlier site draft's results board criteria, including the "since last release" view (no development view on Vercel).
- Superseded by: none
