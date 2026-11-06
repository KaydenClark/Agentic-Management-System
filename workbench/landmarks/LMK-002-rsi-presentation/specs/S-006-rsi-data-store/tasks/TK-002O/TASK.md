# TK-002O - A worker recovers one job and exports a safe checkpoint

**Task ID:** TK-002O
**Spec ID:** S-006
**Slice:** A worker recovers one job and exports a safe checkpoint
**Status:** in-progress
**Blockers:** TK-002N
**Destination:** spec-acceptance: Recovery
**Planned verification:** Representative public-seam demonstration, adverse cases, focused checks and scoped QA.
**Claimed by:** codex-s006-recovery
**Current claimant:** codex-s006-recovery

## Assignment

One writer owns S-006 job persistence and safe export for a representative job, with schema, writer, readback and tests together. Save an authorized job referencing the existing Task and campaign, claim atomically, persist attempt and uncertain-write state, and recover it without duplicate effect. Export and reconstruct a complete safe checkpoint without changing identities, refusing partial or conflicting restore. The canonical store remains Supabase and Git export is recovery only. Release after Stage A finalizes the contract and separately launched implementation, and after the S-006 lineage artifact exists and is verified. No cross-Spec edge is implied.

Planning source: owner RSI Map/Plan request of 2026-11-04 and mapped base 8319e81f399923f920a686e8f68dad3f40cfe7f5. Size to one representative case with Check, QA, repair and hand-back in one run. Preserve all prior evidence and existing holds. Hand back exact revision, checks, observed result, remaining gaps and responsible owner.

## Acceptance

- [ ] Competing claims and duplicate intake produce one logical job; a crash with uncertain publication cannot create another attempt.
- [ ] A safe complete checkpoint reconstructs the same identities; partial, stale-conflicting and private exports fail.
- [ ] An operator can replay the saved example through the writer and readback; checks and limitations are recorded.

## Scoped implementation release

On 2026-11-05 the owner explicitly requested this implementation under orchestrate/carry and confirmed the readback. Start with an isolated test namespace; preserve synthetic labels, privacy, original identities and stopped campaigns. This releases owner:feedback-loop-implementation only for this Task. Verified TK-002N remains a prerequisite. No model campaign, installation or production promotion is released.

## Verified prerequisite and scoped continuation

N is natively done at 3228d58fe3fb8afbfbc04abf01e42fad72c48ac0 (product d03bb10a0045bf55bd7b0b629afa18a8951a8918), with accepted isolated write/readback and exact-head CI. On 2026-11-06 the orchestrator released O under the confirmed owner implementation request. N main containment is not this Task's prerequisite. This corrects the extra sequencing condition previously added to the Spec; N publication remains separately held. Preserve all stopped work, identity/attempt limits and isolated-only scope; no production/model/installation/deployment authority is added.
