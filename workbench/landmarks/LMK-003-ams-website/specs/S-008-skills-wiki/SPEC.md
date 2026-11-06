# S-008 - Skills wiki

**Spec ID:** S-008
**Status:** active
**Priority:** 3
**Owner:** Kayden; orchestrator A (Website, cloud)
**Stance:** Builder
**Updated:** 2026-11-06
**Catalog description:** Site-written articles on the owner's skills, one page per skill grouped by Workbench stage, modeled on aihero.dev/skills.
**Blockers:** none
**Confirmation:** [JOT-ba986c8a-508a-4f4a-94b4-8d0ae8e9641b](../../../../wiki/context-active-spec-approvals.md)
**Execution approval:** [JOT-ba986c8a-508a-4f4a-94b4-8d0ae8e9641b](../../../../wiki/context-active-spec-approvals.md)
**Next gate:** Close TK-0033 with verification and documentation proof.

## Intent and authority

The owner chose site-written articles modeled on https://www.aihero.dev/skills and its `/grilling` depth/tone (2026-11-01), supplied `skills-by-workbench-stage.svg` and set the template below. KaydenClark/skills is private: never publish its files. Authority/endpoint: JOT-ba986c8a. Bounded PR #111 inspection and recovery: [JOT-54c3a590-89e6-4bf7-95ef-4c50771e7ac8](../../../../wiki/context-website-presentation.md#jot-54c3a590-89e6-4bf7-95ef-4c50771e7ac8); current-base checks and review precede dev containment.

## Outcome

A reader browses AMS skills by Workbench stage and learns what each does, when to use it, its requirements and refusals, working signs and workflow fit.

## Why It Matters

Faithful explanations show the method behind AMS results without publishing private files.

## Current Verified State

- Historical delivery: `/skills` and 39 articles on dev19c06cc at skills8782412 ([evidence](../../../../wiki/history/S-008.md#acceptance-criteria)); no main delivery or owner QA is established here. Later refocus requirements remain unchecked.
- Source878241202bf7ec97c0952287f1633f6f0ddf1a6e: chart skills are top-level; grill-me/grill-with-docs map to align-concept/align-docs. Off-chart: clean-my-ai-harness-codex, obsidian-vault, ponder, teach. Notices exist; root LICENSE does not.

History: [S-008 history](../../../../wiki/history/S-008.md).

## Desired Behavior

- **Set.** One article per chart skill under its repository name at the pin: 39 at `8782412` (Route 5, Align 12, Prepare 2, Journey 7, Judge 1, Complete 4, Improve 8); none for off-chart skills.
- **Index (`/skills`).** Grouped by the chart's stages in order (Route, Align, Prepare, Journey, Judge, Complete, Improve), each with its gloss; main-flow skills first in order, then the rest. Each entry: name, one-line summary, link.
- **Article (`/skills/<name>`).** Sections in order:
  1. **What it does**: the mechanism in plain words, key terms defined.
  2. **When to use it**: how it is invoked; where neighbours overlap, a "what you have / reach for" table pointing to the right skill.
  3. **Example request**: one realistic request that brings it in.
  4. **What it requires**: helper skills, records/tools and whether Setup Workbench is required. Explain actual conditional prerequisites and Primitive/Compound composition.
  5. **What it does not authorize**: what running it never grants (e.g. merging, publishing, Human QA).
  6. **Skill-specific sections**: only where needed (e.g. `grilling`'s round and frontier).
  7. **FAQs**: readers' actual questions, answered directly, including known failure modes and workarounds.
  8. **It's working when**: a list of observable signs of a correct run.
  9. **Where it fits in the workflow**: its chart stage, what calls it and what it hands to, linking those articles.
- **Credit.** State inspiration/adaptation, original author/source and license from the pin's skill/notices; changed ownership does not erase origin credit.
- **Pin.** Each article derives from its skill file at the pinned commit and names it; a later pin updates affected articles.
- Layout follows the reference site; exact elements are confirmed against it at Task planning.

## Decisions And Contracts

- Write site articles; do not copy skill files.
- Credit adapted skills to their source, never as original.
- The owner chose the nine-section article (2026-11-01).
- Stages come from the chart, names from the repository at the pin; where they differ the repository name wins and this Spec leaves the chart alone.
- No "used to build this site" marks; that record belongs to the Supabase backend and GitHub (owner, 2026-11-01).

## Non-Goals

- Publishing the skills repository or any skill file; editing skills (their repository's process); off-chart articles; used marks.

## Dependencies And Blockers

- Satisfied: S-003 shell, theme and site tests on `dev`; stage data (`site/app/start/skills.mjs`, drawn by `/start` screen 3) on `dev`, not yet `main`.
- Read access to `KaydenClark/skills` at the pin for authoring.

## Vertical Implementation Slices

TK-001 (Builder) proves index, article shape, credit and pin on one skill. TK-002 (Builder) proves coverage.

## Acceptance Criteria

- [x] **Article shape.** Every article has sections 1-5 and 7-9 in order (6 optional, between 5 and 7), a credit line, and its skills commit. *Check:* content test over built articles. *Must fail:* no FAQs, no "It's working when", no "What it does not authorize", or sections out of order.
- [x] **Faithful.** Each described behavior, requirement and refusal appears in the pinned skill file. *Check:* a reviewer compares articles with the pinned files. *Must fail:* a behavior the skill lacks.
- [x] **Coverage.** Every chart skill has an article under its repository name at the pin; every stage names a skill. *Must fail:* a missing chart skill, an article named `grill-me`, an off-chart article, or an orphan stage.
- [x] **Index.** `/skills` lists every article under its chart stage, main-flow first in order, each linking `/skills/<name>`. *Must fail:* a skill under the wrong stage or an unlinked article.
- [x] **Credit.** An adapted skill names its source and license. *Must fail:* an adapted skill labeled original.
- [x] **No used marks.** No page marks a skill as used to build the site. *Must fail:* a "used" badge or list on any wiki page.
- [x] **No private files.** The hygiene check finds no copied skill-file content beyond short quoted lines. *Must fail:* a skill file reproduced on the site.
- [ ] **Refocus fidelity.** At an accepted S-000A pin, composition, Workbench prerequisites, job/method and adaptation credit match source; drafts and static checks are not outcome claims.

## RSI and website connection

S-002/S-011 measured changes and [S-000A](../../../LMK-004-rsi-loop-during-build/specs/S-000A-skills-refocus/SPEC.md) accepted refocus pins update affected articles. This prepares the contract, not site implementation.

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
