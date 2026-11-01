# S-008 - Skills wiki

**Spec ID:** S-008
**Status:** planned
**Priority:** 3
**Owner:** Kayden; orchestrator A (Website, cloud)
**Stance:** Builder
**Updated:** 2026-11-01
**Catalog description:** Site-written summaries of the owner's skills, one entry per skill, modeled on the format of aihero.dev/skills.
**Blockers:** S-003
**Latest event:** Mapped from the owner's confirmed decisions of 2026-11-01.
**Next gate:** Task planning after the site shell (S-003) exists.

## Intent and authority

The owner chose site-written summaries of the owner's skills, modeled on https://www.aihero.dev/skills. The skills repository is private, so the site publishes summaries, not skill files.

## Outcome

A reader can browse the skills that operate the AMS, see what each does, when to use it and what it does not authorize, and see which ones were actually used to build the site.

## Why It Matters

The skills are how agents operate the AMS. Explaining them faithfully, without publishing private files, shows the method behind the results.

## Current Verified State

- No wiki pages exist. The skills live in the owner's skills repository, outside this one.

## Desired Behavior

- An index of the owner's skills, grouped by workflow stage, and one entry per skill.
- Each entry gives: what it does, when to use it, what it does not authorize, an example request, and its provenance or license.
- Each entry is derived from that skill's file at a pinned skills commit, and names the commit.
- "Used to build this site" appears only where a record links the skill to a Task or review.
- Layout follows the reference site's format; the exact elements are confirmed against that page at Task planning.

## Decisions And Contracts

- Summaries are written for the site; skill files are not copied.
- An adapted skill is credited to its source, never labeled original.

## Non-Goals

- Publishing the skills repository or any skill file.
- Editing skills; skill changes go through the skills repository's own process.

## Dependencies And Blockers

- S-003 (site shell); a pinned skills commit readable by the authoring session.

## Vertical Implementation Slices

| Task | Slice | Status | Blockers | Proof |
|---|---|---|---|---|
| TK-001 | Skills index page and one complete entry from a pinned skill, deployed to `dev` | ready | none | pending |
| TK-002 | Entries for every skill in the owner's set, grouped by stage | ready | TK-001 | pending |
| TK-003 | "Used to build this site" marks driven by Task and review records | ready | TK-002 | pending |

### TK-001 - First entry

**Stance:** Builder

Proves the entry-shape and pin criteria on one skill.

### TK-002 - Full set

**Stance:** Builder

Proves the coverage criterion.

### TK-003 - Used marks

**Stance:** Builder

Proves the "used" criterion.

## Acceptance Criteria

- [ ] **Entry shape.** Every entry has all five parts and names its skills commit. *Check:* a content test over entries. *Must fail:* an entry with no "does not authorize" line.
- [ ] **Faithful.** Each described behavior appears in the pinned skill file. *Check:* a reviewer compares entries with the pinned files. *Must fail:* a behavior the skill does not have.
- [ ] **Coverage.** Every skill in the owner's set has an entry and every stage names at least one skill. *Must fail:* an orphan stage.
- [ ] **Used means recorded.** A "used" mark links the Task or review record. *Must fail:* a mark with no record.
- [ ] **No private files.** The hygiene check finds no copied skill file content beyond short quoted lines. *Must fail:* a skill file reproduced on the site.

## RSI and website connection

Skill changes measured by the loop (S-002, S-011) update the affected entries at the new pin.

## Testing Seams

- Content tests over the built entries; a pin comparison against the skills commit.

## Verification Procedure

```bash
node workbench/tools/spec-workbench.mjs show S-008
# site test command named at Task planning
```

## Documentation Impact

- The glossary links the wiki for skill names.

## Append-Only Evidence And Execution Log

| Date | Task | Event | Verification | Docs | Remaining gap |
|---|---|---|---|---|---|
| 2026-11-01 | none | Mapped as planned | render, doctor | this Spec | Every criterion |

## Review and Human QA

The owner reviews the wiki pages through their Grill Board cards (S-005).

## Completion Result

Pending.

## Remaining Limitations Or Follow-Up Specs

- none

## Supersession

- Supersedes: none
- Superseded by: none
