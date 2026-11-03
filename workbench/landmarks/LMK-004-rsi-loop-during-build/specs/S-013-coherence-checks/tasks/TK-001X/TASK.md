# TK-001X - A reader can account for recovered Workbench capabilities

**Task ID:** TK-001X
**Spec ID:** S-013
**Slice:** Map the pinned legacy catalog to current owners, dispositions and evidence; restore concise control routes
**Status:** in-progress
**Blockers:** none
**Destination:** spec-acceptance: Feedback loop connection
**Planned verification:** Compare inventory against pinned source catalogs; check owners, links, control targets, render, wiki, layout, doctor and hygiene.
**Claimed by:** codex-recovery
**Current claimant:** codex-recovery

## Assignment

Independent review of recovery candidate `b7efbaba15baa354eafbc92b91a352ae54d94c71` returned the assembled candidate: the Spec review found a P1 gap in the legacy inventory, and the standards review carried a P2 for oversized ARCHITECTURE and its stale RUNBOOK anchor. Root also found the oversized BLUEPRINT and stale Wiki route. Preserve TK-001U's completed bounded receipt and the failed verdict. One writer records an explicit pinned-source inventory and reconciles ARCHITECTURE, BLUEPRINT and stale Wiki routes. Retain confirmed destination, historical evidence, existing implementation and remaining gaps; no full equivalence, promotion or owner acceptance is implied.

## Acceptance

- [x] The pinned legacy decision and capability catalog is accounted for with source, current owner, retained/adapted/retired/missing/unknown disposition, reason, implementation and proof or limit; useful unported work has an owner and next action.
- [x] ARCHITECTURE and BLUEPRINT retain their current meaning and useful routes at the 900–1,500 character target; stale RUNBOOK anchors are corrected.
- [x] Focused checks and scoped QA record the exact candidate and unresolved gaps; the failed prior review is preserved and final independent review remains separate.

## Observations during correction

The earlier `b7efbaba` site CI found two glossary projection mismatches after the Workbench definition changed. The existing generator refreshed `site/app/glossary/glossary.json`. The first local build launch could not find `next` because dependencies were absent; after `npm ci`, the site build, three focused glossary tests and all 209 site tests passed. The build reported RSI data unavailable because Supabase configuration was absent. The earlier CI failures remain evidence; no live read is claimed.

## Check and scoped QA

The [recovery inventory](../../../../../../wiki/context-workbench-adoption.md) enumerates the pinned catalog scope and all 51 captures, 52 operation rows, 33 core and seven maintainer skills, 18 utilities, 82 ADR and 57 DDR IDs. Exact ID set comparison found no missing, extra or duplicate IDs. Dispositions describe current record evidence or explicitly unknown parity with S-001 next actions; the catalog's later evidence snapshots are not asserted as pinned behavior. Root controls measure ARCHITECTURE 1,406 and BLUEPRINT 1,495 codepoints. Local link/anchor inspection, wiki, layout, hygiene and whitespace checks passed. Doctor had no global blocker; its S-011 slice, S-002 stale claim, legibility and permission findings remain. The glossary projection correction passed site build, three focused tests and all 209 site tests after `npm ci`; the build reported unavailable RSI data without Supabase configuration. The earlier two CI failures and unavailable initial build launch remain recorded above. This is scoped self-QA, not independent Review or owner Human QA; final assembled checks and fresh review remain. Full Workbench parity is not established.
