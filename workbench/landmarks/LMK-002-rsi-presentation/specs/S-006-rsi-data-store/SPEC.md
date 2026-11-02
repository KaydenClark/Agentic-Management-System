# S-006 - RSI data store

**Spec ID:** S-006
**Status:** active
**Priority:** 1
**Owner:** Kayden; orchestrator B (local keys)
**Stance:** Builder
**Updated:** 2026-11-02
**Catalog description:** Sourced Supabase data and local writers.
**Blockers:** none
**Confirmation:** [JOT-a85076a7-25a3-45bd-bd33-220c62d87882](../../../../wiki/context-active-spec-approvals.md)
**Execution approval:** [JOT-a85076a7-25a3-45bd-bd33-220c62d87882](../../../../wiki/context-active-spec-approvals.md)
**Latest event:** Approved pinned import/readback passed.
**Next gate:** Coverage/W disposition, whole Review, actual owner QA.

[a]: ../../../../wiki/context-active-spec-approvals.md
[b]: tasks/TK-000Z/approved-history-import-771bd1e.md
[p]: tasks/TK-000B/TASK.md#proof

## Intent and authority

Python pushes RSI/history/cost/tokens to Supabase; site only reads. Gitignored local service key; site publishable key. [Approvals][a] govern.

## Outcome

One sourced store, local writers, site reads under RLS.

## Why It Matters

Sourced charts; local credentials.

## Current Verified State

W remains stopped/unaccepted: failed 813465d/5e02ead;550 recovery retained. X/Z proofs below retain setext corrections and original3 S008+8 archives/F→K/R/CAS.

JOT-ada1ea57-1afe-40b0-986d-eb4567bc2884 approved only main771bd1e264ff15ab89217c8f91f79fc38c57f96b/devfe9870fe93f715c859fc5059b0b4c52f38f4a640. [Actual batch][b]:one call;131 inserted/1030 existing/41 refreshed;1161 unique;74 current Task projections match; global missing/extra/newer/mismatch/unsourced 0, ordered. 3+8 originals/1030 IDs retained;989 untouched;41 audit/annotation/undo checks pass. No delete/key leak. Earlier 2 write refusals ran no key/write; failed GET retained. Later history unimported; no second batch/latest coverage claim.

## Desired Behavior

Results:task, held-out/dev, arm(AMS/no-AMS/plain),runtime/controls/skills commits, provider/model/effort,pass,cost/tokens, state/source. Completed needs `passed`; score optional(ADR-002J). Unknown needs reason/source,never zero([rules](../../../../../evals/TRIAL-ROWS.md)). Real build/improvement/skills-fix seeds; strength:anecdote/single/repeated/held-out with interval. `recorded_fact` only history. Mark/hide synthetic; empty valid.

History:Spec/Task/PR/commit/return/correction; immutable IDs,idempotence,stale/conflict refusal. Private assessments:frozen packets/run IDs/attempts/findings/retests,recomputable results; no client reads/RPC writes. Presentation SELECT only; key never Git/site.

## Non-Goals

Charts:S007; trials:S002; no benefit claims.

## Dependencies And Blockers

Project hqvtnpvwwppbeurponnn(ADR-003C); uv/Python3.14.5(ADR-003D).

## Vertical Implementation Slices

Native `tasks/` own proof/Receipts; no duplicate table.

## Acceptance Criteria

- [x] **Schema/provenance:** required fields; missing skills commit fails.[p]
- [x] **No client writes:** insert/update/delete denied; presentation SELECT/private denial.[p]
- [x] **Writer:** real remote event/site-key readback.[p]
- [x] **Conflicts:** no silent concurrent overwrite.[p]
- [x] **Real sources:** strength labels; no samples as real.[p]
- [x] **Key authentication:** secret/legacy formats; no value output; legacy fakes only.[p]
- [ ] **Build history:** sourced real events above; no duplicate reimport/handtyped/unsourced row. Approved pinned proof[b]; latest coverage open.
- [x] **Secret hygiene:** tree/history scan.[p]
- [x] **Private assessments:** canonical remote replay/idempotence; tamper/reset/conflict/client denial(Q/R/S).

## RSI and website connection

S002 writes; S007 reads; RUNBOOK/ARCHITECTURE own commands/path.

## Verification Procedure

Native show/doctor; locked pytest; DB/writer/site-key checks. Import/readcheck only approved pins.

## Append-Only Evidence And Execution Log

All 28 events retained; Receipts/Git own full proof/attribution. Gaps are historical.

|Date|Task|Event|Verification|Docs|Remaining gap|
|---|---|---|---|---|---|
|2026-11-01|none|Mapped as planned; baseline migration noted|render/doctor|Spec|All criteria|
|2026-11-01|TK-001|Task closed|PR15 884d021|RUNBOOK/ARCH|Legacy JWT fakes only|
|2026-11-01|TK-002|Task closed|PR18 d279ae1|RUNBOOK/ARCH|none|
|2026-11-01|TK-003|Task closed|PR29 74b446e|RUNBOOK/ARCH|RSI awaits S002|
|2026-11-01|TK-004|Task closed|PR31/37 4d74e90/d26bb8c|RUNBOOK/ARCH|Dev not imported|
|2026-11-01|TK-005|Task closed|PR42 55c3856|RUNBOOK/ARCH|S002 seeds|
|2026-11-01|review|Review verdict: fail at c87bf4ec86206bd5f734af7b828c81c3d3356a00 [a2124994b4d9] #1|Tasks B/C/D|C repo review|3|
|2026-11-01|TK-000E|B review FAIL c87bf4e: H1, M1-M3, L1, L2|live review|Spec|Task E|
|2026-11-01|TK-000E|Task closed|PR49 a03d739; live/readcheck0|Task E|Fresh Review|
|2026-11-01|TK-000C|Task closed|a4470a4 secret tree/history scan|Task C|none|
|2026-11-01|TK-000D|Task closed|a4470a4; DB20261101144510|Task D|none|
|2026-11-01|TK-000B|Task closed|a4470a4;8 criteria|Task B|Fresh Review|
|2026-11-01|review|Review verdict: pass at d6d4a6d65cc6287b667fe78ee5db937440972a5e [213a7241e512] #2|none|C repo review|none|
|2026-11-01|TK-000L|B review FAIL d6d4a6d: N1-N6, legacy key|live review|Spec|Task L|
|2026-11-01|TK-000L|Task closed|5aa2621/c0f6c67;943 rows/0 gaps;433/4|[Task L](tasks/TK-000L/TASK.md)|Review; assessments/metrics|
|2026-11-01|TK-000P|Task closed|475/4; migration20261101192328; live cleanup0|[Task P](tasks/TK-000P/TASK.md)|Review; assessments/trials|
|2026-11-01|TK-000Q|Task closed|56 focused;489/4; migration20261101193603; live|[Task Q](tasks/TK-000Q/TASK.md)|Delivery/Review/QA; S007/S002|
|2026-11-01|review|Review verdict: fail at 977ac08fed4a269182b67d6ada990042e2ceee88 [cfc6d944ca57] #3|P1 JSONB normalization poisons digest; exact TEXT repair|s006_review independent|1|
|2026-11-01|TK-000R|Task closed|62 focused;495/4; migration20261101195609; live/CI53|[Task R](tasks/TK-000R/TASK.md)|Delivery/Review/QA; S007/S002|
|2026-11-01|review|Review verdict: pass at 906f71f936ccbb4ccc777cbea5643ca2668d3a85 [079d355dd065] #4|none|s006_review independent|none|
|2026-11-01|review-detail|Independent PASS receipt at 906f71f|[receipt](../../../../feedback/REVIEW-S-006-906f71f.md)|direct reviewer|Owner QA/delivery separate|
|2026-11-01|TK-000S|Task closed|84 focused;517/4;CI61;4 live pairs/0 mutation; cleanup0|[Task S](tasks/TK-000S/TASK.md)|Review/QA/S007/S002; unowned SVG retained|
|2026-11-01|review|Review verdict: pass at e5a8c33a24226fd1f3eb595fa227f385a04934bd [6df68e2822de] #5|none|s006_review independent|none|
|2026-11-01|review-detail|Independent whole PASS receipt at e5a8c33|[receipt](../../../../feedback/REVIEW-S-006-e5a8c33.md)|direct reviewer|Owner QA/delivery separate|
|2026-11-01|TK-000U|Task closed|9f3a6ca/main172;590/4;85 focused;d50 scoped PASS;8 facts|[Task U](tasks/TK-000U/TASK.md)|CI/binding/live/QA|
|2026-11-02|TK-000X|Task closed|3cd0637;699/4;166 focused;8 facts; scoped PASS;2 setext oracles corrected|[Task X](tasks/TK-000X/TASK.md)|Binding/CI/live; W/owner QA open|
|2026-11-02|TK-000X|Checked source delivered; live verification incomplete|PR91 771; GET 1030:missing130/extra1/mismatch2/unsourced0;8 exact;2 rejected writes unrun|Task X|Approval/S008 lineage/W/owner QA then held|
|2026-11-02|TK-000Z|Task closed|3a25cac;764/4;215+49;1232→1234/61;3+8/R;fake CAS/undo/current;GET1/0;CI41435710340|[Task Z](tasks/TK-000Z/TASK.md)|At close:CI/merge/import/current DB/live unrun; W/whole Review/QA|

## Review and Human QA

Verdicts bind candidates. Presentation QA:S007; native completion needs actual owner HumanQA.

## Completion Result

Implemented; approved batch passes. NOT accepted:latest coverage/W/whole Review/owner QA open. No trial/evaluator qualification.

## Remaining Limitations Or Follow-Up Specs

Region:nearest US unless chosen. Table-index condensation re-dates; refresh logs prior values. Legacy JWT:fakes only. Baseline migration repo20261101000000/DB20261101123819 unchanged.

## Supersession

Draft JSONL superseded; no successor.
