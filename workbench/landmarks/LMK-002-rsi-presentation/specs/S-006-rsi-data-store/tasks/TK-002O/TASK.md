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

## Starting inventory

Workspace baseline sha256:059c7b58c9f3dffc63722a4762e37d8188454ea1938e931f290630211cb2eca2

Native claim 10797e22e38f19c9a3b54c57aa5244f941d6c634 and rendered original records were committed before this complete snapshot. Raw inventory stays in local private recovery; retained unrelated refs remain local, without a whole-workspace remote-recovery claim.

## Receipt

| Run | Branch | HEAD SHA | Upstream | Dirty | Tests | Docs touched | Remaining gap | Checksum |
|---|---|---|---|---|---|---|---|---|
| 1 | Feature/S-006-rsi-data-store | 6a3dcf5b4c204df866097c5cedc87b0d79aa9057 | ahead 1 behind 0 | 0 | Core19 pass with actual SQL/process races, effect-before-receipt crash recovery, stale fences, gates, native-slot non-repeat and semantic slot uniqueness. Initial schema IF/CASE parse failure fixed. Checkpoint suite26pass/3fail: valid restores HTTP400; PG confirms token counts parse error in restore IF. Negative restore assertions hit same parser failure and are not accepted proof. STOP/report. | Frozen worker/recovery contract retained; API/SQL/tests are incomplete WIP | O incomplete. Fix restore operator grouping and inspect aliases; require semantic SQLSTATEs, then prove complete/partial/divergent/private/pinned restores and outage pending. Root scope correction needed after this checkpoint. No production change, model call, qualification, P release, or N publication retry. | ab31b0722a5f5c3190285a731407623b51eb046b2f1e274cf59455e03981a9ba |
| 2 | Feature/S-006-rsi-data-store | b14e5f7c9e20bdc0a16c31ef800c97c003da66df | ahead 0 behind 0 | 0 | Bounded correction after preserved STOP: restored grouped JSON counts operator; read-only PG probe confirmed alias42702 and corrected it. Fresh isolated target valid complete restore passed first; then33 recovery checks pass with semantic SQLSTATE/unchanged-store controls. Exact b14e5f7 fresh checkout with PYTHONPATH=src:244pass2existing-skip including lineage and currentmain detection; hygiene0, layoutvalid, doctor no blocking finding. CI42200594882 queued, not a pass. | evals/RECOVERY.md defines API, transactions, trusted checkpoint pin, private effect seam and limits; prior failed evidence retained. | O remains open pending exacthead sharedCI and orchestrator source/API acceptance. Isolated schema only; no production migration, native model invocation, general exactly-once claim, qualification, adoption or P release. N publication remains separately held; unrelated retained refs are not claimed remote-recoverable. | 15a33aa914cb00f395d7c069bae5f4a04db4bb9a0ad1cbb4236554a4403f47f0 |
| 3 | Feature/S-006-rsi-data-store | af6e27d10744f4b309dda1da53329236cc7e2f3f | ahead 0 behind 0 | 0 | Independent Frontier Standards review FAIL at b14e5f7: raw service RPC accepted null effect_type, issued begin and absent-retry execution without keyed-file contract; null observation outcome persisted invalid data. Prior244green did not cover this boundary. Spec review requests positive restore with matching preexisting canonical parents. Reviewer probes retained separately. Full local session31067 final output unavailable here; no pass claimed. | No prior receipt altered. Bounded same-TK002O SQL total-validation and canonical-parent proof correction assigned by orchestrator under existing owner authority. | O remains open. Correct SQL enum null/type handling, audit related nullable parameters, add raw-RPC unchanged-state controls and matching canonical-parent restore; freeze and independently recheck exact correction. No P release, production write, model call, campaign reset or PR-body retry. | a461448ba38334677bf3341bcc2039d9904205b9d640d207ffce0fdaf316bc3e |
