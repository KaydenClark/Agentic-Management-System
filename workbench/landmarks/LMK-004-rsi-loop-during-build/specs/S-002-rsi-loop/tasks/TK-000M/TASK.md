# TK-000M - A local caller records a frozen three-run assessment with exact scoring and retained attempt history

**Task ID:** TK-000M
**Spec ID:** S-002
**Slice:** A local caller records a frozen three-run assessment with exact scoring and retained attempt history
**Status:** in-progress
**Blockers:** none
**Destination:** spec-acceptance: Scoring; Stops; Cycle (assessment and retest safeguards only)
**Planned verification:** CLI known-outcome fixtures for pooled counts, levels, missing proof, findings/retests, immutable records and fourth-attempt refusal; full pytest and room checks.
**Claimed by:** codex-s002
**Current claimant:** codex-s002

## Assignment

Kayden requested carrying S-002 through Journey on 2026-11-01. Reconcile its newer approved audit contract into this independent, bounded implementation Task. One writer: codex-s002. Branch `codex/s002-assessment-loop`, target `main`, checked PR and merge commit. Use the existing Python package, stdlib and pytest conventions.

Deliver a local CLI from frozen assessment JSON through deterministic validation/scoring to immutable readback and attempt/finding history. Read the parent Spec, the r1 method and rubric owned by audit-workbench, and the existing baseline under `evals/rsi-loop-1/`. Keep rubric classes and identities frozen; treat unknown/missing evidence as No; distinguish evidence validity from truth and qualification from scores. Preserve historical reports unchanged. Document the format and manual operation in evals and RUNBOOK.

Local assessment records are preparation and evidence, not S-006 persistence, model trials, useful-benefit proof, semantic evaluator qualification or Spec acceptance. Do not call paid services, modify personal skills, the site, S-006 or managed tools. Storage integration, controlled behavioral trials and the first grilling redesign remain under their existing owners.

## Acceptance

- [ ] The CLI pools `8/10 + 1/2 + 1/2` as `10/14`, emits an exact ratio and no percentage for an empty set; computes all four levels and Critical override.
- [ ] Missing/unknown/refused/interrupted proof stays No in its original class; unjustified exclusions, invented IDs/classes, unpinned evidence and Regression without baseline proof cannot silently pass.
- [ ] Acceptance is separate from score/level, qualification and scope; no incomplete, unqualified, Broken, Functional or bounded-as-whole result is accepted.
- [ ] Immutable local assessment readback retains every attempt, including baseline zero and failures; a fourth candidate attempt or label-only counter reset is refused.
- [ ] Omitted findings remain open; closure requires an explicit repaired-revision retest of the original and affected regression checks in all three runs; recurrence remains visible.
- [ ] Known-good, known-bad and do-nothing cases exercise the CLI and the full suite/room checks pass, with actual limitations recorded.
