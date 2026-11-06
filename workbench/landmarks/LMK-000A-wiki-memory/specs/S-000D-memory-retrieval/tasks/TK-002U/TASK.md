# TK-002U - Recover a sourced explanation and detect changed evidence

**Task ID:** TK-002U
**Spec ID:** S-000D
**Slice:** Bounded maintained-section/Jot recall with claim-source change reporting and runnable evaluation
**Status:** in-progress
**Blockers:** none
**Destination:** spec-acceptance: R1, R2, R5 initial baseline, R6 preservation
**Planned verification:** Public ams-memory query/check/evaluate exercises, source change/restore and privacy refusal tests, focused pytest and native checks.
**Claimed by:** codex-wiki-retrieval
**Current claimant:** codex-wiki-retrieval

## Assignment

High-tier implementor uses journey, TDD and writing-for-agents; recover Spec and its linked contract at Map b9417d2 plus this prepared Task's final revision. Read actual CLI/package and native Jot interfaces before implementation. One writer owns additive project Python code, tests, pyproject entrypoint, evaluation fixtures and scoped docs; do not edit managed workbench/tools or shared skills. Serialize this checkout with the orchestrator; report actual model/harness, never infer them from the tier.

Deliver `ams-memory query`, `check` and a runnable initial `evaluate` path. Cross input parsing, eligible Markdown section/Jot/correction parsing, contextual keyword ranking, source binding/fingerprinting, bounded readable/JSON output and tests. Start with at least two real routed AMS topics, including Wiki's independent Landmark correction, and a compact development question set. General eligible Wiki recall must work; do not hardcode question answers. Use Markdown claim metadata compatible with native validation, supporting several claims/sources per page and retained observation/supersession lineage. Source references are identities/links, not arbitrary recursive ingestion.

Freeze question/source/budget identity and capture an actual baseline through pinned MEMORY navigation plus native Jot before candidate comparison. Distinguish source-hit checks from answer judgments. The initial runner may record explicit unmeasured independent/human fields; missing CLI at baseline is never an accuracy failure. Final broader evaluation stays in TK-002W.

Size: one narrow usable recall/change-detection path, including tests, QA and repair, fits one High run. Keep optional ranking experiments out unless observed keyword failures justify them. No paid services or required embeddings. Hand back committed candidate, CLI demo, fixture/source identities, actual results, remaining gaps and updated owners to S-000D/orchestrator.

## Acceptance

- [ ] MEMORY-first query retrieves a prose-only claim and relevant native entry/source references with title, heading, subject, state, correction context and bounded continuation; query is read-only.
- [ ] `check` reports exactly the bound explanations affected by changed public source bytes; missing/unavailable/unbound sources and restored bytes are explicit. Neither the source nor verification/confirmation state is rewritten.
- [ ] Several claim/source bindings survive rebuild with observed revisions/digests/dates and supersession; derived cache deletion changes no durable knowledge.
- [ ] Public CLI tests prove private/restricted/ignored content is excluded before body reads, malformed handling metadata fails closed, symlink/path escapes refuse, and referenced secrets/arbitrary external bodies are not ingested.
- [ ] Initial real AMS development cases execute through evaluate with pinned navigation/Jot baseline and candidate outputs, context/source measures and explicit judgment/owner-effort limits. Wrong/stale answers are retained as failures, not silently regraded.
- [ ] Implementor Check/QA and focused tests/native Wiki validation pass; exact prior sources/confirmations are preserved. R1/R2 remaining corpus or behavior limits are explicit, never claimed complete from a skeleton alone.

## Starting preservation

Claim originals committed as `9ccae2f`. Workspace baseline sha256:296c63314038c19e04f8b3f7e372a2295a934102a1ef3e6da008071a9938db24. Native inventory is explicitly incomplete: pre-existing `REBASE_HEAD` residue, no active rebase directories; root independently verified. It remains untouched. Public retrieval corpus frozen at `280725648ed4a2a7d0e97236fd51def5c02aaa65` before implementation; private recovery retains source and inventory bytes. Local publication hold prevents remote recovery proof. Owned-path preservation will be checked separately; no complete workspace-closeout claim.

## Stopped implementation handback

Actor: OpenAI gpt-6.1-sol / High on Codex; journey/TDD/writing-for-agents/codebase-design. Root STOP follows FAIL-118–121; no further code/retests authorized. Task and acceptance stay open.

Additive candidate: `ams.memory` query/check/evaluate, entrypoint,16 tests and four frozen development cases. Expected TDD red13: absent module. Unexpected sequence:12pass/1fail fixture(118), repaired13pass; archive-manifest refusal(119); repaired preflight, then3/4evaluation(120 false unknown hit); threshold/source guards repaired,16focused and4/4development passed before root STOP arrived. No final Check/QA or independent Review.

Baseline: public prepared revision `280725648ed4a2a7d0e97236fd51def5c02aaa65`, unchanged cases and limit6/max6400. Global native Jot search blocks on pre-existing malformed `context-owner-answers-coherence.md`; valid routed native reads are separately retained. Baseline source hits3/3; requested Wiki correction Jot missed under bound; unknown global search unavailable. Candidate same-source source/context checks4/4, correction source present, unknown abstained. These are development retrieval observations, not independent answers, stale-answer judgments, transfer or owner-effort measurements.

Cases/baseline: `evals/wiki-memory/`. Private recovery retains both evaluations, initial archive-inclusive baseline, public snapshot and incomplete inventory. Failure120 evaluation sha256:741a1b0beb87ca3e5608f804f8d560c33500cd73605ecdfd2f0cd9f4452538fe; later evaluation sha256:11e38e9ccf86122fe868690696146dac971487e69c95207234601180071245e8. Tool output retains pytest results. Wiki sources/Jots/confirmations, managed tools and shared skills remain untouched.

Remaining: real multi-claim/source metadata and observed lineage on two topics; source selector/safety and baseline edge-case QA; concise operating documentation; final required native/check suite and preservation proof. Public console entrypoint is declared but not exercised; current demos use `uv run --no-sync python -m ams.memory`. R1/R2/R5/R6 and the Task are not accepted complete. Root must obtain bounded continuation authority before implementation or retest, then inspect source/candidate and arrange independent probes. Publication remains separately held; no push, merge, deployment or Human QA.

## Receipt

| Run | Branch | HEAD SHA | Upstream | Dirty | Tests | Docs touched | Remaining gap | Checksum |
|---|---|---|---|---|---|---|---|---|
| 1 | Feature/S-000D-wiki-memory | 28e4b122b7503348fcc119bfb98640dda2632a03 | ahead 6 behind 0 | 7 | STOPPED: expected missing-module red13; FAIL118 12pass/1fail; corrected13pass; FAIL119 baseline refusal; FAIL120 evaluation3/4; later focused16pass and development4/4 before root STOP. Final checks/QA not run. | Task/Spec and feedback preserve stopped state; real binding/operating docs unfinished. | FAIL121 Runbook stop bypass; owner continuation required. Task open; publication held. R1/R2/R5/R6 incomplete. | a502c6a2db09a723cd1f0cc1da5ce2f3fbbb375387ef8dc5fcc20fb3b5926bc5 |
