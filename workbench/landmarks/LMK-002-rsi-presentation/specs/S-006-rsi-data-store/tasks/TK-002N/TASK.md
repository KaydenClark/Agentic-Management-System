# TK-002N - A worker saves and reads one linked improvement record

**Task ID:** TK-002N
**Spec ID:** S-006
**Slice:** A worker saves and reads one linked improvement record
**Status:** in-progress
**Blockers:** none
**Destination:** spec-acceptance: Lifecycle lineage
**Planned verification:** Representative public-seam demonstration, adverse cases, focused checks and scoped QA.
**Claimed by:** codex-s006-lineage
**Current claimant:** codex-s006-lineage

## Assignment

One writer owns the S-006 writer, schema, tests and docs for this narrow vertical slice. On an isolated approved database, carry one safe failure identity through pinned case, candidate, comparison, disposition and later-use readback; reject missing or orphaned identities and preserve privacy and site read-only access. Deliver actual writer-to-store-to-readback evidence, including outage and duplicate behavior; do not claim a full loop or restart a campaign. Release only after Stage A confirms the exact data and identity contract and the owner separately launches implementation.

Planning source: owner RSI Map/Plan request of 2026-11-04 and mapped base 8319e81f399923f920a686e8f68dad3f40cfe7f5. Size to one representative case with Check, QA, repair and hand-back in one run. Preserve all prior evidence and existing holds. Hand back exact revision, checks, observed result, remaining gaps and responsible owner.

## Acceptance

- [ ] A caller writes and reads back one complete linked safe lineage with original IDs and pins; orphaned or conflicting records fail.
- [ ] Private/raw evidence and privileged operations are inaccessible to the presentation role; outage is not reported as publication.
- [ ] Focused checks and scoped QA prove the public seam; the exact revision and limits are handed back.

## Scoped implementation release

On 2026-11-05 the owner explicitly requested this implementation under orchestrate/carry and confirmed the readback. Start with an isolated test namespace; preserve synthetic labels, privacy, original identities and stopped campaigns. This releases owner:feedback-loop-implementation only for this Task. No model campaign, installation or production promotion is released.
