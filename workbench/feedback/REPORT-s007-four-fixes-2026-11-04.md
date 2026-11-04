# Four RSI presentation repairs: observed failures and expected outcomes

Attribution: owner-assistant. Owner-approved scope, 2026-11-04. Owner: [S-007 correction PR165](https://github.com/KaydenClark/Agentic-Management-System/pull/165). Baseline: dev `ae231ee`. This is supporting evidence for the existing failure log, not a replacement log or a measured skill-improvement claim. PR164 merged to main as69fc587 during this repair. Its exact accepted log is retained here with appended FAIL-035 through FAIL-051; no earlier rows are overwritten.

## Attribution limits

The four source defects below are reproduced product failures. Their originating skill invocation, provider, exact model and tier are **unknown** from the inspected evidence. Review-bot identity is not implementor identity. No specific design or workflow skill is blamed without an invocation trace. Current repair harness: Codex; exact model and tier are unknown in the available task metadata. No personal names are used.

## Reproduced defects

| ID | Failed activity | Observed failure | Correct outcome | Evidence | Disposition |
|---|---|---|---|---|---|
| F-001 | Display baseline/candidate encodings | Candidate arm's later background overrides the contrasting interior; both bars become solid ink | Contrasting interior and double ink border in both themes | [PR154 finding](https://github.com/KaydenClark/Agentic-Management-System/pull/154#discussion_r4457357231); `rsi-bars.check.mjs` reproduced identical fills | test; S-007 TK-002L |
| F-002 | Keep page review tied to evidence | Changing read time alone changes the content hash | Timestamp remains visible; identical evidence keeps the hash; evidence or availability changes alter it | [PR142 finding](https://github.com/KaydenClark/Agentic-Management-System/pull/142#discussion_r4457543895); first `rsi-repairs.test.mjs` run fails freshness equality | test; S-007 TK-002L |
| F-003 | Compare results across versions | Different graders pool into one point or produce a false continuous trend/regression | Grader version is visible series identity; counts and regressions stay within one grader | [PR142 finding](https://github.com/KaydenClark/Agentic-Management-System/pull/142#discussion_r4450929584); both same/changed-system grader fixtures fail with one series instead of two | test; S-007 TK-002L |
| F-004 | Preserve failed/stopped attempts | A run without results has no point and disappears | Separate run-level source/provenance/stop evidence, with unknown task/split/grade and no fabricated score | [PR142 finding](https://github.com/KaydenClark/Agentic-Management-System/pull/142#discussion_r4450929591); no run-only reader at baseline; terminal run fixture reproduced omission | test; S-007 TK-002L |

## Actual invocation failures in this repair

Skill context: installed Journey Check procedure and TDD; no skill-source defect is established. Provider/harness: OpenAI/Codex; exact model and tier: unknown. The expected red tests above intentionally reproduced existing product defects and are not failed repair attempts.

| ID | Failed activity | Observed failure | Correct outcome and handling | Disposition |
|---|---|---|---|---|
| I-001 | Launch browser contrast check | Playwright's expected Chromium executable was absent; no check executed | Use an installed supported browser or identify the missing prerequisite. Installed Chrome then reproduced F-001 and verified the repair | diagnostic; environment prerequisite, no skill repair claimed |
| I-002 | Run repository hygiene through uv | Restricted DNS blocked Python dependency download (`iniconfig`); hygiene did not run in that invocation | Install locked dependencies through approved network access, then execute the unchanged check. Approved sync succeeded and hygiene reported zero findings | diagnostic; environment restriction, no skill repair claimed |
| I-003 | Apply documentation patch | A README line fragment did not match the full existing line; the atomic patch applied nothing | Read back current bytes, make the exact bounded replacement and verify the diff. Corrected replacement preserved surrounding text | diagnostic; editing invocation, no skill repair claimed |

| I-004 | Invoke hygiene with default uv cache | Default cache was outside writable roots; no hygiene check executed | Reuse the task-local UV_CACHE_DIR already established; unchanged check then passes | diagnostic; local invocation |
| I-005 | Full Python repository verification | 810 passed, 4 skipped, 1 failed: native claim expanded S-007 Next gate enough to exceed the 8000-character record limit (8026) | Keep the Task-owned next-gate field concise without dropping requirements; then rerun repository hygiene and full suite on a fresh checkout. This is a current Journey Check failure, not a historical attribution | test; S-007 TK-002L |

## Publication blocker

Automatic approval review denied the public push of product commit `4e3aa13`: implementation was authorized, but the reviewer requires explicit public-publication approval. The earlier native claim was pushed as `7af73e7`; subsequent product changes were not pushed. No connector or indirect workaround was attempted. Retain local commits, finish local checks, and request approval for push, PR and checked dev merge. No owner QA or production promotion.

## Verification and limits

`node --test tests/rsi-repairs.test.mjs tests/rsi-rows.test.mjs`: 20 passed after repair, versus four new expected red tests before it. Production build and `npm test`: 266 passed. Browser contrast check passes light/manual-dark/system-dark including a deliberately broken solid-fill negative control; run-only fixtures visible without overflow at 375/1280 in both themes. Actual results, availability and run failures remain review-hash-bound. Test runs are excluded; result-backed failures stay on their existing point.

No real model trials, private credentials or database writes were used. Fixtures are labeled and never imported by the production page. Fresh checkout5cc0cdf passed build,266 site tests and811 Python tests with4 skipped; source bytes match4e3aa13. Shared CI, deployment and delivery state are recorded in TK-002L; they are not implied by these local results. Human QA and production promotion remain owner-only. Repairing presentation is not evidence that AMS itself improved.

## Preservation and invocation corrections

I-006: The baseline status itself recorded a dirty generated Taskboard; not every original was committed before snapshot. Exact original bytes are retained in the local Git object and independently copied with matching digest. This does not reconstruct the required earlier chronology; preservation remains local and incomplete until delivery. I-007: abbreviated baseline ID was refused; I-008: a subsequently supplied incorrect full ID failed binding. The actual Git-resolved full SHA was then used. Correct outcome: resolve identifiers from Git and commit owned originals before taking the baseline, never guess or reconstruct history. I-009 through I-012 capture the initial DNS and tool-interface refusals in the canonical log; these are invocation/environment diagnostics, not evidence of a skill-source defect.

## Publication authorization correction

Owner,2026-11-04, explicitly authorized merging into dev and main for the things that belong in each. This releases publication for this candidate, with website changes to dev and records to main; no unrelated site promotion or Human QA. The prior denial remains historical. Another writer assigned FAIL-034 before this push; our entries use FAIL-035 through FAIL-051 and leave that writer unchanged.

## Receipt preservation failure during delivery

FAIL-053: failure-ID reconciliation accidentally changed text inside receipt row1, causing native close to refuse its checksum before changing Task state. Exact original row bytes were restored from6bd979c without recalculating the checksum; new ID meaning is recorded outside the receipt. Correct outcome: preserve immutable historical receipt text during record reconciliation. Skill context Journey/native close; current Codex exact model and tier unknown. This records the implementor mistake, not a proven skill-source defect.

## Post-close STOP: record budget

FAIL-054: after exact original receipt recovery, native close succeeded and appended receipt2, expanding TK-002L to8194 characters. Post-close hygiene failed the8000-character limit. This follows the earlier full-Python Spec-limit failure (FAIL-043). Under RUNBOOK Test And Build, the second verification failure stops further website correction/retry. No Task pruning, source changes or further site tests followed. Website merge remains blocked despite earlier source CI passing; native done status is engineering history, not accepted delivery. Preserve the complete candidate and both receipts. Required next authorization: bounded coherent Task-record pruning preserving receipts and requirements, then rerun the same gates. Failure-record-only main delivery can continue independently.
