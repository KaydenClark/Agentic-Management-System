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

Own one representative S-006 recovery job: atomic claims, stable attempts/effects, uncertain-write reconciliation and complete safe export/restore through Python/Supabase. Preserve Task/campaign/case identities and evidence; reject duplication, partial/stale-conflicting restore and private data. Supabase stays canonical; export is recovery only. Prove public seams/adverse cases, scoped QA and exact-source delivery with explicit limits.

Owner Map/Plan: 2026-11-04, base 8319e81f399923f920a686e8f68dad3f40cfe7f5. Prerequisites: frozen Stage A contract, separate implementation launch, verified lineage. Preserve holds; no cross-Spec edge.

## Acceptance

- [ ] Competing claims and duplicate intake produce one logical job; a crash with uncertain publication cannot create another attempt.
- [ ] A safe complete checkpoint reconstructs the same identities; partial, stale-conflicting and private exports fail.
- [ ] An operator can replay the saved example through the writer and readback; checks and limitations are recorded.

## Scoped implementation release

Owner request/readback confirmed 2026-11-05; orchestrator released O 2026-11-06 on verified N (native 3228d58fe3fb8afbfbc04abf01e42fad72c48ac0, product d03bb10a0045bf55bd7b0b629afa18a8951a8918, isolated readback/exact CI). N main containment was an extra condition, now corrected; N publication stays held. Resolves owner:feedback-loop-implementation only here. Preserve labels/privacy, identities, attempts and stopped campaigns. No model campaign, installation, production migration or deployment release.

## Starting inventory

Workspace baseline sha256:059c7b58c9f3dffc63722a4762e37d8188454ea1938e931f290630211cb2eca2

Claim 10797e22e38f19c9a3b54c57aa5244f941d6c634 and rendered originals committed before complete snapshot. Raw inventory/private unrelated refs retained locally; whole-workspace remote recovery unclaimed.

## Receipt

| Run | Branch | HEAD SHA | Upstream | Dirty | Tests | Docs touched | Remaining gap | Checksum |
|---|---|---|---|---|---|---|---|---|
| 1 | Feature/S-006-rsi-data-store | 6a3dcf5b4c204df866097c5cedc87b0d79aa9057 | ahead 1 behind 0 | 0 | Core19 pass with actual SQL/process races, effect-before-receipt crash recovery, stale fences, gates, native-slot non-repeat and semantic slot uniqueness. Initial schema IF/CASE parse failure fixed. Checkpoint suite26pass/3fail: valid restores HTTP400; PG confirms token counts parse error in restore IF. Negative restore assertions hit same parser failure and are not accepted proof. STOP/report. | Frozen worker/recovery contract retained; API/SQL/tests are incomplete WIP | O incomplete. Fix restore operator grouping and inspect aliases; require semantic SQLSTATEs, then prove complete/partial/divergent/private/pinned restores and outage pending. Root scope correction needed after this checkpoint. No production change, model call, qualification, P release, or N publication retry. | ab31b0722a5f5c3190285a731407623b51eb046b2f1e274cf59455e03981a9ba |
| 2 | Feature/S-006-rsi-data-store | b14e5f7c9e20bdc0a16c31ef800c97c003da66df | ahead 0 behind 0 | 0 | Bounded correction after preserved STOP: restored grouped JSON counts operator; read-only PG probe confirmed alias42702 and corrected it. Fresh isolated target valid complete restore passed first; then33 recovery checks pass with semantic SQLSTATE/unchanged-store controls. Exact b14e5f7 fresh checkout with PYTHONPATH=src:244pass2existing-skip including lineage and currentmain detection; hygiene0, layoutvalid, doctor no blocking finding. CI42200594882 queued, not a pass. | evals/RECOVERY.md defines API, transactions, trusted checkpoint pin, private effect seam and limits; prior failed evidence retained. | O remains open pending exacthead sharedCI and orchestrator source/API acceptance. Isolated schema only; no production migration, native model invocation, general exactly-once claim, qualification, adoption or P release. N publication remains separately held; unrelated retained refs are not claimed remote-recoverable. | 15a33aa914cb00f395d7c069bae5f4a04db4bb9a0ad1cbb4236554a4403f47f0 |
| 3 | Feature/S-006-rsi-data-store | af6e27d10744f4b309dda1da53329236cc7e2f3f | ahead 0 behind 0 | 0 | Independent Frontier Standards review FAIL at b14e5f7: raw service RPC accepted null effect_type, issued begin and absent-retry execution without keyed-file contract; null observation outcome persisted invalid data. Prior244green did not cover this boundary. Spec review requests positive restore with matching preexisting canonical parents. Reviewer probes retained separately. Full local session31067 final output unavailable here; no pass claimed. | No prior receipt altered. Bounded same-TK002O SQL total-validation and canonical-parent proof correction assigned by orchestrator under existing owner authority. | O remains open. Correct SQL enum null/type handling, audit related nullable parameters, add raw-RPC unchanged-state controls and matching canonical-parent restore; freeze and independently recheck exact correction. No P release, production write, model call, campaign reset or PR-body retry. | a461448ba38334677bf3341bcc2039d9904205b9d640d207ffce0fdaf316bc3e |
| 4 | Feature/S-006-rsi-data-store | 2e63ba969147e58907c0d9258a565bb311487967 | ahead 0 behind 0 | 0 | Exact2e63ba9 fresh checkout:288pass2existing-skip, including77O. Raw NULL/missing/type enums and nullable controls reject with expected SQLSTATE and unchanged state; explicit keyed retry passes/native retry refuses. Matching preexisting canonical-parent pinned restore/readback/noop and hidden client reads pass with guards enabled. EarlierreviewFAIL retained; unavailable full-run output remains unverified. Hygiene0; doctor no blocking finding. | RECOVERY API documents SQL authority, canonical-reference fixtures and limits; correction source/tests frozen. | O open pending fresh independent Standards/Spec rechecks and exacthead fullCI. Isolated schema/fixtures only, no production migration or measured model outcome. No P release, qualification/adoption, campaign reset, PR-body retry or whole-workspace recovery claim. | 569ba25d5c8f3f85ffc28dbd329c85afbb2a724c1c356dd5ad31b76120d6195a |
| 5 | Feature/S-006-rsi-data-store | e8839751e800e2cee66521a6446f23379b3fcc4c | ahead 0 behind 0 | 1 | Standards recheck FAIL at2e63: originalNULLs fixed; raw numeric proof/payload digests persisted and blocked export. N guard also accepted numeric record_id/source_commit/parent refs that its reader refused. Reviewer31unit+64SQLpass does not override these probes. New verified N/O roundtrip defects; old N closure and all prior proofs remain prior-source evidence. | Existing O correction only: systematically align persisted scalar types/canonical representation with readers; valid all-digit strings must remain valid. Prior guarded receipt rows unchanged. | O open. One coherent N/O SQL correction, rawRPC red/green strict SQLSTATE/unchanged-fullstate controls and fullchain/export/restore positives required before independent rechecks. No new Task/campaign/counter, P release, model call, production write or publicbody retry. | 6b5e5af40f7b739f841fb16a473ec23e691d5025d8a5db28ce4bcfba70c56a12 |
