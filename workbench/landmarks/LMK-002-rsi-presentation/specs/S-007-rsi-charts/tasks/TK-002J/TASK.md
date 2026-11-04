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

- [x] Each charted skill shows one point per recorded loop from the kept version's Alignment Score and fitness level, with the start point, rejected attempts and High/Small runs distinguishable and never deciding a point.
- [x] The fitness-level-per-loop strip shows every charted skill by loop, with stated level colors; Excellent is green.
- [x] A labeled multi-loop fixture renders a contract change and a model change as separate lines and keeps a regression visible; the page itself shows no invented loop.
- [x] Existing `/rsi` behavior and evidence stay intact; empty trial places stay honest and compact.
- [x] Focused regressions, production build, site suite and browser inspection at 1280px and 375px in both themes pass; actual candidate and limits are recorded.

## Hand-back

Return the exact candidate commit on the Spec branch, actual checks, screenshots inspected and limitations. A completed slice does not establish S-007 acceptance, owner Human QA or measured RSI benefit.

## Check and QA

Candidate `9531b0f9cc433cbf8b3662a54f52dd44a78b0a99` on `Feature/S-007-rsi-chart-pages`, parent `77bfb38` (contains dev `0fdd1e1`). New: `site/app/rsi/skill-loops.ts` (the loop-point seam over the round-two safe summary, with not-kept attempt scores sourced from S-011 history), `site/app/rsi/skill-trends.tsx`, a labeled multi-loop test fixture and `site/tests/rsi-skill-trends.test.mjs`. The section leads `/rsi`; empty trial places keep their message, explanation and next event in a compact frame.

Fitness-level colors sit in a second marked block of `site/app/theme/tokens.css` after the generated Grill Board block, which stays unchanged. `site/tests/tokens-json.test.mjs` failed on them as written, so its contract was extended: the new block may hold only stated `--level-*` hex or recorded-token values, alike in the light, manual-dark and system-dark rules; planted faults prove each rule fails. Everything outside both blocks keeps the old rule. Excellent is green (`#157A47` light, `#3FC27F` dark), Stable blue, Functional amber, Broken uses `--heat`; each fill also carries its name or short form, and agent green does not appear on `/rsi`.

Implementor checks: production build; site suite 261 of 261; built-site hygiene 0 findings; `git diff --check` clean; doctor no S-007 finding. Browser check with Playwright from a scratch install: all 49 `/rsi` checks pass (axe AA with contrast, no horizontal scroll, focus, reduced motion, network) at 375, 1280 and 1440 px in both themes; one `/start` toy request check failed intermittently across runs and was not compared with the baseline. Screenshots of the trends, cards, strip and empty places were inspected in both themes. Orchestrator re-ran the build, the site suite (261 of 261), hygiene and diff checks on the candidate and confirmed it merges cleanly with dev `0fdd1e1`.

Limits: tests were written alongside the code, with planted faults as the must-fail proof. One loop is recorded, so the running average and line breaks are exercised only by the fixture, not by the real page. No local Supabase environment, so the page shows trial data as unavailable locally. No owner Human QA, deployment readback, measured RSI benefit or Spec acceptance is claimed.

## Receipt

| Run | Branch | HEAD SHA | Upstream | Dirty | Tests | Docs touched | Remaining gap | Checksum |
|---|---|---|---|---|---|---|---|---|
| 1 | detached at 72952d8 | 72952d8fde8d222c9e44853aaaf9c897371a84e5 | none | 0 | Production build; site suite 261/261; built-site hygiene 0; diff check clean; /rsi browser checks 49/49 at 375/1280/1440 both themes; /start toy request check intermittent, not baselined | site/README.md; S-007 TK-002J Check and QA | Delivery to dev, deployment readback and owner Human QA | 837c6164b95a1a4f2027b5ab0055f81c4b89f63a3b18aa542a9e5217130afa34 |
