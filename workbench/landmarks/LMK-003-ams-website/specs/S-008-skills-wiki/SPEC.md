# S-008 - Skills wiki

**Spec ID:** S-008
**Status:** active
**Priority:** 3
**Owner:** Kayden; orchestrator A (Website, cloud)
**Stance:** Builder
**Updated:** 2026-11-02
**Catalog description:** Site-written articles on the owner's skills, one page per skill grouped by Workbench stage, modeled on aihero.dev/skills.
**Blockers:** none
**Confirmation:** [JOT-ba986c8a-508a-4f4a-94b4-8d0ae8e9641b](../../../../wiki/context-active-spec-approvals.md)
**Execution approval:** [JOT-ba986c8a-508a-4f4a-94b4-8d0ae8e9641b](../../../../wiki/context-active-spec-approvals.md)
**Latest event:** TK-001 and TK-002 closed: `/skills` and 39 articles at skills commit `8782412` merged into `dev` at `19c06cc` (PR #93), 2026-11-01.
**Next gate:** Owner page approvals and Human QA of the 40 draft-marked pages on protected `dev`; only the owner merges `dev` -> `main`; then `complete`.

## Intent and authority

In chat on 2026-11-01 the owner chose site-written articles on the owner's skills, modeled on https://www.aihero.dev/skills, with its `/grilling` page as the model of depth and tone. The source, `KaydenClark/skills`, is private, so the site never publishes skill files. The owner supplied the stage chart (`skills-by-workbench-stage.svg`, beside this Spec) and set the template and decisions below. Execution authority and endpoint: JOT-ba986c8a.

## Outcome

A reader browses the skills that operate the AMS by Workbench stage, opens any one, and learns what it does, when to reach for it, what it needs and refuses, how to tell it is working and where it fits.

## Why It Matters

The skills are how agents operate the AMS. Explaining them faithfully, without publishing private files, shows the method behind the results.

## Current Verified State

- `dev` at `19c06cc` (PR #93), not `main`: `/skills` and 39 draft-marked articles at skills commit `8782412`; checks and reviews are in the TK-001 and TK-002 close rows.
- Skills commit `878241202bf7ec97c0952287f1633f6f0ddf1a6e`: every chart skill is a top-level directory, `grill-me` and `grill-with-docs` renamed `align-concept` and `align-docs`; off the chart: `clean-my-ai-harness-codex`, `obsidian-vault`, `ponder`, `teach`; a `THIRD_PARTY_NOTICES.md`, no root `LICENSE`.

## Desired Behavior

- **Set.** One article per chart skill under its repository name at the pin: 39 at `8782412` (Route 5, Align 12, Prepare 2, Journey 7, Judge 1, Complete 4, Improve 8); none for off-chart skills.
- **Index (`/skills`).** Grouped by the chart's stages in order (Route, Align, Prepare, Journey, Judge, Complete, Improve), each with its gloss; main-flow skills first in order, then the rest. Each entry: name, one-line summary, link.
- **Article (`/skills/<name>`).** Sections in order:
  1. **What it does**: the mechanism in plain words, key terms defined.
  2. **When to use it**: how it is invoked; where neighbours overlap, a "what you have / reach for" table pointing to the right skill.
  3. **Example request**: one realistic request that brings it in.
  4. **What it requires**: skills, records, tools or Workbench it depends on.
  5. **What it does not authorize**: what running it never grants (e.g. merging, publishing, Human QA).
  6. **Skill-specific sections**: only where needed (e.g. `grilling`'s round and frontier).
  7. **FAQs**: readers' actual questions, answered directly, including known failure modes and workarounds.
  8. **It's working when**: a list of observable signs of a correct run.
  9. **Where it fits in the workflow**: its chart stage, what calls it and what it hands to, linking those articles.
- **Credit.** A closing line: original to the owner, or adapted from a named source with its license, as the skill file and `THIRD_PARTY_NOTICES.md` state at the pin.
- **Pin.** Each article derives from its skill file at the pinned commit and names it; a later pin updates affected articles.
- Layout follows the reference site; exact elements are confirmed against it at Task planning.

## Decisions And Contracts

- Articles are written for the site; skill files are not copied.
- Adapted skills are credited to their source, never labeled original.
- The nine-section article is the owner's (2026-11-01) and replaces the earlier five-part entry (does, when, does not authorize, example request, provenance).
- Stages come from the chart, names from the repository at the pin; where they differ the repository name wins and this Spec leaves the chart alone.
- No "used to build this site" marks; that record belongs to the Supabase backend and GitHub (owner, 2026-11-01).

## Non-Goals

- Publishing the skills repository or any skill file; editing skills (their repository's process); off-chart articles; used marks.

## Dependencies And Blockers

- Satisfied: S-003 shell, theme and site tests on `dev` (checked `2a89fe4`, 2026-11-01); PR #87 stage data (`site/app/start/skills.mjs`, drawn by `/start` screen 3), merged into `dev`, not yet `main`.
- Read access to `KaydenClark/skills` at the pin for authoring.

## Vertical Implementation Slices

| Task | Slice | Status | Blockers | Proof |
|---|---|---|---|---|

### TK-001 - Index and first article

**Stance:** Builder

Proves the index, the article shape, credit and pin criteria on one skill.

### TK-002 - Full set

**Stance:** Builder

Proves the coverage criterion.

## Acceptance Criteria

- [x] **Article shape.** Every article has sections 1-5 and 7-9 in order (6 optional, between 5 and 7), a credit line, and its skills commit. *Check:* content test over built articles. *Must fail:* no FAQs, no "It's working when", no "What it does not authorize", or sections out of order. *Evidence:* the loader refuses malformed articles; `tests/skills-wiki.test.mjs` plants faults (165/165 at `19c06cc`).
- [x] **Faithful.** Each described behavior, requirement and refusal appears in the pinned skill file. *Check:* a reviewer compares articles with the pinned files. *Must fail:* a behavior the skill lacks. *Evidence:* the orchestrator judged all 39 against their pinned folders (16 failed, were revised and re-judged); an independent Spec reviewer re-checked land, setup-workbench, improve-workbench, sitrep, oracle and triage claim by claim: no invented behavior.
- [x] **Coverage.** Every chart skill has an article under its repository name at the pin; every stage names a skill. *Must fail:* a missing chart skill, an article named `grill-me`, an off-chart article, or an orphan stage. *Evidence:* coverage test at `19c06cc`: 39 equal the chart's 39 (5/12/2/7/1/4/8), `align-concept` and `align-docs`, none off-chart.
- [x] **Index.** `/skills` lists every article under its chart stage, main-flow first in order, each linking `/skills/<name>`. *Must fail:* a skill under the wrong stage or an unlinked article. *Evidence:* index test and browser check at `19c06cc`.
- [x] **Credit.** An adapted skill names its source and license. *Must fail:* an adapted skill labeled original. *Evidence:* loader credit rules; independent review of all 39 credits against `THIRD_PARTY_NOTICES.md` and folder notices.
- [x] **No used marks.** No page marks a skill as used to build the site. *Must fail:* a "used" badge or list on any wiki page. *Evidence:* used-marks test with planted faults at `19c06cc`.
- [x] **No private files.** The hygiene check finds no copied skill-file content beyond short quoted lines. *Must fail:* a skill file reproduced on the site. *Evidence:* site hygiene test (165/165); `check:skills-source`: 0 copied runs of 10+ words at `8782412`.

## RSI and website connection

Skill changes measured by the loop (S-002, S-011) update the affected articles at the new pin.

## Testing Seams

- Content tests over the built index and articles; pin comparison with the skills commit; site hygiene and browser checks.

## Verification Procedure

```bash
node workbench/tools/spec-workbench.mjs show S-008
cd site && npm ci && npm run build && npm test
npm run check:browser                                   # needs Playwright with Chromium
npm run check:skills-source -- --skills DIR             # DIR: private skills checkout at 8782412
```

## Documentation Impact

- The glossary links the wiki for skill names.

## Append-Only Evidence And Execution Log

| Date | Task | Event | Verification | Docs | Remaining gap |
|---|---|---|---|---|---|
| 2026-11-01 | none | Mapped as planned | render, doctor | this Spec | Every criterion |
| 2026-11-01 | none | Entry shape revised to the owner's seven-section template; open choices listed | render, doctor | this Spec | Every criterion; open owner choices |
| 2026-11-01 | none | Owner settled the open choices: nine sections, stage grouping, chart skills at pin `8782412` under repository names, index plus page per skill, used marks dropped (TK-003 removed); implementation not started | render, doctor | this Spec | Every criterion |
| 2026-11-01 | TK-001 | Task closed | PR #93 merged into dev at 19c06ccaf3236228f78d5b1ab8b4ebf87be07f50 (tree equal to checked head 49841646); Vercel status success for that commit. /skills index and 39 articles build; npm test 165/165; check:browser 1984/1984; tour-375 24/24; check:skills-source 0 findings at pin 8782412; independent Standards and Spec reviews (fresh contexts) found no hard breach and every acceptance criterion met. | site/README.md Skills wiki section (files, format, tests, source check) | none for TK-001; TK-002 (full set) delivered in the same PR; close attribution: {"agent":"Orchestrator (Claude Opus 5.5)","claimant":"Orchestrator (Claude Opus 5.5)","onBehalfOf":null} |
| 2026-11-01 | TK-002 | Task closed | All 39 chart skills have articles under repository names at pin 8782412 (Route 5, Align 12, Prepare 2, Journey 7, Judge 1, Complete 4, Improve 8), delivered in PR #93 merged into dev at 19c06cc; coverage test passes (no grill-me/grill-with-docs, no off-chart article, no orphan stage). Each article: Sonnet writer, independent Sonnet audit, final writer, orchestrator judgment against the pinned skill folder (23 passed, 16 failed and were revised and re-judged). Independent Spec review spot-checked six articles claim by claim and all 39 credits. | site/content/skills/*.md; site/README.md | Owner page approvals (draft marks on all 40 pages), Grill Board review cards (S-005), page-list.json entries (orchestrator A), glossary link to the wiki, chart image still shows old names, dev -> main by owner; close attribution: {"agent":"Orchestrator (Claude Opus 5.5)","claimant":"Orchestrator (Claude Opus 5.5)","onBehalfOf":null} |
| 2026-11-02 | none | Prose pruned toward the 8,000-character limit (owner, 2026-11-02); no decision, criterion, tick or log row changed | render, doctor | this Spec | Still over 8,000; no native review verdict was bound |

## Review and Human QA

The owner reviews the wiki pages through their Grill Board cards (S-005).

## Completion Result

Pending.

## Remaining Limitations Or Follow-Up Specs

- The chart image shows `grill-me` and `grill-with-docs` until the owner updates it.
- Documentation Impact is not done: the site Glossary is S-003 TK-003 (PR #84, open); `GLOSSARY.md` edits go through domain-modeling.
- `site/page-list.json` lacks `/skills` and the articles; orchestrator A is its only writer.
- `check:skills-source` needs the private skills checkout, so it runs locally, not in CI.

## Supersession

- Supersedes: none
- Superseded by: none
