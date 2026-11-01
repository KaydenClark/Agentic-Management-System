# TK-000O - Historical finding identity cannot bypass Regression or repaired-revision acceptance

**Task ID:** TK-000O
**Spec ID:** S-002
**Slice:** Historical finding identity cannot bypass Regression or repaired-revision acceptance
**Status:** done
**Blockers:** none
**Destination:** spec-acceptance: Scoring; Stops
**Planned verification:** Red/green collision fixture at score/record seams; independent review; final-head CI.
**Claimed by:** codex-s002
**Current claimant:** codex-s002
**Proof:** 42 focused; CI #38 pass

## Assignment

Same authorized S-002 delivery, codex-s002 writer, `codex/s002-assessment-loop` -> `main`, PR #78. [Automated finding](https://github.com/KaydenClark/Agentic-Management-System/pull/78#discussion_r4436884504) at `d8fc717` proved a historical Quality finding could collide with the generated ID of a currently failing Regression check, leaving Stable accepted. Reject incompatible check/class collisions before writing or retain a distinct current-class finding; preserve previous evidence and original classes. No storage, trial or rubric expansion.

## Acceptance

- [x] A historical Quality finding cannot hide a current Regression failure through an ID collision; incompatible check IDs/classes cannot reuse the current finding identity.
- [x] Refused collisions leave stored history unchanged, and normal repeat findings, enrichment, retests and recurrence still work.
- [x] Focused tests, independent review and required CI pass before merge; native proof/closure retained.

## Check and corrective review

Source candidate `67fc14a0d8d4d30909c671353c4ec12e52d3bf2e`: regression observed red, then 41 focused tests passed. Both fresh-context reviewers report no findings; Spec reviewer independently repeated all 41 and probed matching Regression findings, distinct historical Quality findings, wrong-check and unmapped collisions. Fresh clone: 432 passed, 4 skipped. Render/doctor/layout/ADR/diff checks passed after the follow-up prose was separated from TK-000N's native Receipt table; its checksummed row was not changed. The collision review thread is resolved after repair and verification.

S-006 and real trials remain blocked as recorded in the Spec. Required final-head CI is pending before merge, without any claimed model qualification, useful benefit or Human QA.

## Same-run retest correction

[Automated finding 4436904200](https://github.com/KaydenClark/Agentic-Management-System/pull/78#discussion_r4436904200) also showed unknown historical failure revisions could resolve after unchanged-candidate retests. This run additionally requires a known original/latest failing commit before resolution, permits validated enrichment of a missing original commit, preserves recorded sources and rejects the same failure revision. The new regression was observed red before repair.

- [x] Missing failure revision cannot close; supplying the unchanged revision remains open, while a distinct repaired revision can close after the normal qualified three-run retest.

## Final source verification

Candidate `3a607f8f3470cc276aa8e93a2b1ee941cf3f6561`: 42 focused tests pass, independently repeated by the Spec reviewer. Both reviewers report no findings after probing missing/null/malformed source revisions, unchanged original/latest failures and distinct repaired revisions. CI workflow `41338924932` (run #38) passed. The new identity/revision regression was observed red then green. All three automated PR findings are repaired and resolved. Final closure changes only records; final-head CI remains a merge gate. No assembled S-002 Review, qualification, behavioral benefit or Human QA is implied.

## Receipt

| Run | Branch | HEAD SHA | Upstream | Dirty | Tests | Docs touched | Remaining gap | Checksum |
|---|---|---|---|---|---|---|---|---|
| 1 | codex/s002-assessment-loop | ab607771763237701ff4f9217cc099e7e61286ab | ahead 0 behind 0 | 0 | 42 focused; CI #38 pass | evals | S-006/trials; close attribution: {"agent":"codex-s002","claimant":"codex-s002","onBehalfOf":null} | 9e992c4535d9b30e0b24cfb07eca91a91c673d2879ed900f531310ee88d39c7b |
