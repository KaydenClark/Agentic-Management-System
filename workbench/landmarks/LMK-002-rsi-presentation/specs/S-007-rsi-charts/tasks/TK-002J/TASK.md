# TK-002J - Each skill's Alignment Score per RSI loop is charted over loops, with a fitness-level-per-loop strip

**Task ID:** TK-002J
**Spec ID:** S-007
**Slice:** Per-skill RSI trend charts and the fitness-level-per-loop strip from recorded loops
**Status:** in-progress
**Blockers:** none
**Destination:** spec-acceptance: Skill trends; Provenance and series; Not only up
**Planned verification:** Render tests on the recorded loop data and a labeled multi-loop fixture (contract break, model break, rejected attempt, regression); production build and site suite; desktop and 375px browser inspection in both themes; applicable RUNBOOK checks.
**Claimed by:** claude-s007-skill-trends
**Current claimant:** claude-s007-skill-trends

## Authority and inputs

Kayden chose the design from throwaway prototypes and approved implementation through orchestrate, 2026-11-03 ([JOT-5529977d](../../../../../../wiki/context-website-presentation.md#jot-5529977d-ad73-433f-9a3c-85dede8946ba)). The chosen views are a per-skill line chart (one point per loop, running average line, fitness-level strip under the axis, a break where a test contract or model changes) and a skills-by-loops "Fitness level per loop" strip. Better colors are wanted; Excellent is green.

Definitions come from `GLOSSARY.md`: the Alignment Score is the passed applicable checks pooled over the deciding runs, as a percentage; the fitness level is Excellent at three passing runs, Stable at two, Functional at one and Broken at none, with any Critical failure making it Broken.

Recorded loop data: the shared-skill repair round two on dev (`site/app/rsi/round-two-data.ts`) is loop 1 for setup-workbench, orchestrate, handoff, journey and land, each with its baseline (the start point) and kept candidate. Attempts that were not kept are recorded with their Mid scores in [S-011 history](../../../../../../wiki/history/S-011.md#resumed-per-pr-rsi-round-two). Scores compare only within one test contract and model: orchestrate and journey use contract v1, the others v2; the deciding tier is Mid. prune-artifact and writing-for-agents are measured by document length, not an Alignment Score, and author-skill is on hold.

## Assignment

One implementor owns this slice, its tests, browser QA and hand-back. Add the skill trends to `/rsi` ahead of the existing evidence: for each charted skill, a line chart with one point per loop taken from the kept version's Alignment Score and fitness level (the baseline is the start point), attempts not kept as distinct secondary marks, High and Small tier runs as secondary marks that never decide a point, a running average line, and a fitness-level strip; then one skills-by-loops strip colored by fitness level. A new test contract or model starts a new line and is labeled. Give the loop points one data seam a later Task can feed from stored rows; record attempt scores in the safe summary data with their source rather than inventing them. With one loop recorded, each skill honestly has a start and a loop-1 point.

Add fitness-level color tokens to `site/app/theme/tokens.css` outside the generated block, for light and dark, with Excellent green and Broken reading as trouble. Keep them distinguishable for color-blind readers and at WCAG contrast; state each color's meaning on the page, and ensure no color carries a second meaning on `/rsi` (DDR-000M).

Keep everything else on `/rsi` working: the live reader, data states, round-two and repair evidence, held-out separation, no outbound GitHub links and no test rows. Where trial places are still empty, keep their honest empty state but compact, so real results lead. Do not claim, change or close TK-002 or TK-003; do not compute improvement statistics in the browser; no new chart library or dependency; server-rendered SVG like the existing charts.

Work on `Feature/S-007-rsi-chart-pages`. Delivery to `dev` is the orchestrator's; production promotion remains the owner's.

## Acceptance

- [ ] Each charted skill shows one point per recorded loop from the kept version's Alignment Score and fitness level, with the start point, rejected attempts and High/Small runs distinguishable and never deciding a point.
- [ ] The fitness-level-per-loop strip shows every charted skill by loop, with stated level colors; Excellent is green.
- [ ] A labeled multi-loop fixture renders a contract change and a model change as separate lines and keeps a regression visible; the page itself shows no invented loop.
- [ ] Existing `/rsi` behavior and evidence stay intact; empty trial places stay honest and compact.
- [ ] Focused regressions, production build, site suite and browser inspection at 1280px and 375px in both themes pass; actual candidate and limits are recorded.

## Hand-back

Return the exact candidate commit on the Spec branch, actual checks, screenshots inspected and limitations. A completed slice does not establish S-007 acceptance, owner Human QA or measured RSI benefit.
