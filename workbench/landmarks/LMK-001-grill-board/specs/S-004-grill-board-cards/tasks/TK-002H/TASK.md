# TK-002H - A project captures and confirms a DQC through a safely installed tracker

**Task ID:** TK-002H
**Spec ID:** S-004
**Concept source:** [DQC-000A](../../../../../../landmark-tracker/destination-questions/DQC-000A.json) — confirmed Grilling Board lifecycle.
**Slice:** A project captures and confirms a DQC through a safely installed tracker
**Status:** done
**Blockers:** none
**Destination:** spec-acceptance: DQC lifecycle acceptance
**Planned verification:** Native CLI/setup and disposable Git/HTTP/browser cases described below; applicable Runbook checks and exact-candidate delivery verification.
**Claimed by:** codex-s004-tracker
**Current claimant:** codex-s004-tracker
**Proof:** f833633: Mac810pass/4skip; CI41770272779 809pass/5skip; source PR68/69 reviewed+merged; packagef38e2b3e; native clone/retry/recovery and hygiene/layout/projection pass. Evidence above.

## Assignment

Implement the shared native DQC lifecycle and setup-workbench support through author-skill and setup-workbench, using an isolated catalog source clone on the S-004 Spec branch. Read the exact confirmed intent and implementation instruction in the parent Spec. Source baseline: AMS main 1a11f25; catalog main 804ba1ed (refresh narrow refs before relying on mutable state). High tier on Codex; one named implementor owns source changes and AMS managed-tool update. The active catalog remains unchanged.

Deliver an observable path: fresh Create/Adopt and explicit existing-project Update yield a usable supported tracker and root TRACKER.md; CLI capture → full proposed readback → exact confirmation/correction/feedback → round continuation/history remains consistent and safe. Extend existing native APIs, preserve schema/declaration compatibility, and expose stable typed execution links with reverse references in owning records. Python Board and terminal must share owning operations. Serialize concurrent writes and bind confirmation to displayed content; stale/idempotent/failed Git operations must preserve every affected file and unrelated staged/dirty work. Prefer one native transactional operation rather than split Node write then Python commit. Coordinate an explicit API contract with the Board implementor before coding divergent adapters.

Use focused behavioral red/green checks where practical. Exercise fresh setup, adoption, update/recovery, old records, malicious paths, concurrent/stale actions, exact history, confirmation invalidation, retries and deterministic projections. Preserve a complete setup method baseline; request separate fresh-context author-skill pruning and retest the same cases. Follow current catalog source checks/review/delivery gates; do not reopen S-011’s stopped r1 campaign. Publish and merge the checked source PR independently, then consume the exact candidate through supported tools update with an inventory, authentic receipt and retained ignored recovery. No hand-copy of managed files/receipt editing. Changes may include native runtime/package/templates/references/tests and AMS manifest, managed tools/receipt, TRACKER.md, initial DQCs and their reciprocal record references. Avoid Python Board source/tests, global controls and root Spec/Task/Wiki writes owned by the director except native claim/close.

Seed this session’s four interview branches with stable DQCs using sourced settled answers; preserve the complete confirmed readback on its owning DQC without marking every derived synthesis confirmed. Link sources to the exact confirmed Wiki entry. Existing concepts, owner answers, private fixtures and dirty worktrees stay intact. No live synthetic owner actions, paid services, installed personal-catalog update or website deployment.

Return exact source/AMS SHAs, branch/PR, API contract, before/after checks, source/installed identity, preserved inventory, implementor QA, remaining gaps and two answers: may the candidate merge to its target, and did it complete this Task? Native close stays truthful and requires current claimant attribution; parent handles assembly records.

## Acceptance

- [x] A fresh and existing Workbench can capture/read/confirm a complete DQC and produce deterministic root TRACKER.md through supported setup operations.
- [x] Terminal actions preserve exact readbacks, correction/feedback/source/scope history, pending confirmation boundaries, stable related IDs and round continuation; simultaneous/stale/repeated/failed writes are safe.
- [x] Catalog source passes applicable checks and actual review; baseline/pruning/retest evidence is retained. Checked source delivery and supported AMS update preserve original catalog/private/project work and receipt integrity.
- [x] Four initial branch DQCs and the exact confirmed concept are recoverable with honest confirmation states and reciprocal execution references; no synthetic owner confirmation or Human QA.

## Verified handback

Director accepted the native/setup result at `f833633ff421d7e0d7220bc0d4c812174bf428fd`; Board Task TK-002I and assembled Review remain.

- [Source PR68](https://github.com/KaydenClark/skills/pull/68) and [persistence follow-up PR69](https://github.com/KaydenClark/skills/pull/69) merged. Independent source Review passed exact heads fde0090 and 2f9d45a; source 57/57 plus final strengthened clone case 1/1. Final source main 41e537f Catalog and cleanup checks passed. Independent pruning and same-case retest are recorded in the source candidate.
- Supported AMS update receipt identifies package `f38e2b3e15caa7e883e1bcca424c17a2da34bd66cb164f4865d6972894c40658`. Existing formation provenance is retained; ignored backups support tested rollback/reapply and valid tool verification.
- Local full suite: 810 passed/4 skipped. [Exact fresh CI](https://github.com/KaydenClark/Agentic-Management-System/actions/runs/41770272779): 809 passed/5 skipped; hygiene zero; layout/ADR/render and existing 375px checks passed. Platform skips differ; neither run supplies new Board QA.
- Actual fresh clone works before repair: both collection markers, native committed action/replay and deterministic projections pass. Root independently compared exact confirmed readback with proposal, immutable snapshot and primary answer. DQC-000A is confirmed; B/C/D are non-actionable pending context with no invented confirmations. Execution owners link stable IDs back.
- All 757 original tracked paths remain; no product/site/legacy Board bytes changed. Installed personal catalog's 3137 file/link identities are unchanged. Earlier candidates, ignored recovery and the pre-existing REBASE_HEAD marker remain. Original before-work closeout snapshot was not captured; later inventory cannot establish that earlier boundary.

Merge answer: native/runtime content is eligible; source is merged, AMS assembly delivery waits TK-002I and independent assembled Review. Completion answer: this Task's scoped acceptance is met. Human QA, website deployment and personal-catalog installation are not claimed.

## Receipt

| Run | Branch | HEAD SHA | Upstream | Dirty | Tests | Docs touched | Remaining gap | Checksum |
|---|---|---|---|---|---|---|---|---|
| 1 | Feature/S-004-dqc-grilling-board | 944f0eb8cf5bce202b224e62733b6321de29229d | ahead 0 behind 0 | 0 | f833633: Mac810pass/4skip; CI41770272779 809pass/5skip; source PR68/69 reviewed+merged; packagef38e2b3e; native clone/retry/recovery and hygiene/layout/projection pass. Evidence above. | Tracker/runtime/receipt/DQCs; source and director records. | TK-002I/assembly/HumanQA pending; snapshot/REBASE_HEAD limits retained; no install/deploy.; close attribution: {"agent":"codex-s004-tracker","claimant":"codex-s004-tracker","onBehalfOf":null} | bfa5b7dabcf289e2656940330e50100ce6f01ad7ca96633678e0b0a0899e5e1d |
