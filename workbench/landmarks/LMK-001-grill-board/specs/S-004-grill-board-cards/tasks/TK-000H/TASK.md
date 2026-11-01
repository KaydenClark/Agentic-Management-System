# TK-000H - The re-ask guard compares only the question line and is defeated by punctuation or a zero-width character (C reproduced 'too taxing ?'). Normalize punctuation and invisible characters or compare more than the question line

**Task ID:** TK-000H
**Spec ID:** S-004
**Slice:** The re-ask guard compares only the question line and is defeated by punctuation or a zero-width character (C reproduced 'too taxing ?'). Normalize punctuation and invisible characters or compare more than the question line
**Status:** done
**Blockers:** none
**Destination:** spec-acceptance: S-004 Acceptance Criteria
**Planned verification:** Answers evidence row 7 (fail verdict at dd52f705004aac5599a17935935d6fbc6d0a511c on 2026-11-01): The re-ask guard compares only the question line and is defeated by punctuation or a zero-width character (C reproduced 'too taxing ?'). Normalize punctuation and invisible characters or compare more than the question line
**Claimed by:** Claude implementor (Orchestrator B)
**Current claimant:** Claude implementor (Orchestrator B)
**Proof:** pytest 367 passed; re-ask must-fail 4 cases

## Receipt

| Run | Branch | HEAD SHA | Upstream | Dirty | Tests | Docs touched | Remaining gap | Checksum |
|---|---|---|---|---|---|---|---|---|
| 1 | fix/s004-review | 5199b1a8f4f804532809b57be04965c987dcbcfb | ahead 0 behind 0 | 0 | pytest 367 passed; re-ask must-fail 4 cases | grill-board/README.md | Owner QA; close attribution: {"agent":"Claude implementor (Orchestrator B)","claimant":"Claude implementor (Orchestrator B)","onBehalfOf":null} | 9374b6a7a37b4b440273a38c03c5a20919597e8958495c957fac0e560c36011d |
