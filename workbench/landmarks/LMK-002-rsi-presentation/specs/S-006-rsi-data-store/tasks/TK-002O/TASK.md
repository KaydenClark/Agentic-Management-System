# TK-002O - A worker recovers one job and exports a safe checkpoint

**Task ID:** TK-002O
**Spec ID:** S-006
**Slice:** A worker recovers one job and exports a safe checkpoint
**Status:** blocked
**Blockers:** TK-002N
**Destination:** spec-acceptance: Recovery
**Planned verification:** Representative public-seam demonstration, adverse cases, focused checks and scoped QA.

## Assignment

One writer owns S-006 job persistence and safe export for a representative job, with schema, writer, readback and tests together. Save an authorized job referencing the existing Task and campaign, claim atomically, persist attempt and uncertain-write state, and recover it without duplicate effect. Export and reconstruct a complete safe checkpoint without changing identities, refusing partial or conflicting restore. The canonical store remains Supabase and Git export is recovery only. Release after Stage A finalizes the contract and separately launched implementation, and after the S-006 lineage artifact exists and is verified. No cross-Spec edge is implied.

Planning source: owner RSI Map/Plan request of 2026-11-04 and mapped base 8319e81f399923f920a686e8f68dad3f40cfe7f5. Size to one representative case with Check, QA, repair and hand-back in one run. Preserve all prior evidence and existing holds. Hand back exact revision, checks, observed result, remaining gaps and responsible owner.

## Acceptance

- [ ] Competing claims and duplicate intake produce one logical job; a crash with uncertain publication cannot create another attempt.
- [ ] A safe complete checkpoint reconstructs the same identities; partial, stale-conflicting and private exports fail.
- [ ] An operator can replay the saved example through the writer and readback; checks and limitations are recorded.

## Scoped implementation release

On 2026-11-05 the owner explicitly requested this implementation under orchestrate/carry and confirmed the readback. Start with an isolated test namespace; preserve synthetic labels, privacy, original identities and stopped campaigns. This releases owner:feedback-loop-implementation only for this Task. Verified TK-002N remains a prerequisite. No model campaign, installation or production promotion is released.
