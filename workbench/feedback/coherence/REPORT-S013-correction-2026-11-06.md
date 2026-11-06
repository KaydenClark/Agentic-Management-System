# S-013 corrective validation — TK-001A

## Preserved findings and red evidence

Original source base: `c787b2958fa7a23f55c6406f3ce367a91e9162dc`, containing reviewed implementation `b932ba0211e7368c13f4114d09c9f4df222fdb2c`. Planning head: `b89b69a`. Product bytes remained unchanged through the separate inventory binding commit `2463dab`.

FAIL-183 and FAIL-184 were recorded validation-pending before this run. Both reproduce on those unchanged product bytes. Command (Python 3.14, project `src` on PYTHONPATH, bytecode/cache disabled): `python -m pytest -p no:cacheprovider -q tests/test_coherence_observe.py -k 'move_checks or competing_processes'`.

Observed before repair: **3 failed, 1 passed, 27 deselected**. Outside-to-allowed move returned no findings instead of `assignment-scope`; product-to-record move returned no findings instead of `prepare-stop-bypass`; within-allowed move passed. With first real publisher paused after fsync and before exclusive link, a distinct second process returned `created` instead of controlled refusal. The first publisher then also completed. These are synthetic owned Git/local-filesystem fixtures, not native host-use or improvement proof. Raw output is retained privately outside the checkout. Original TK-001D and earlier evidence remain unchanged.

Repair and final validation: pending. Independent review, exact-head shared CI, delivery, Human QA and whole-Spec acceptance remain separate gates. No campaign or attempt counters reset.

## Bounded repair and behavioral QA

The inventory now disables rename detection, retaining both removal and addition paths for scope/Prepare classification. A nonblocking advisory lock on an open report-directory descriptor spans recovery, recurrence/native-use validation and exclusive linking. No removable lock file or unlocked fallback is used. Busy/unsupported lock operations refuse; another occurrence for a retained use still refuses after contention ends.

Focused run after repair: **33 passed** (before the final additional retry assertion). The adverse moves now route to S-000A, the valid move stays clean, distinct real processes produce one winner and a controlled loser, and a fresh interpreter recovers the winner plus another owner's retained report. Identical replay is unchanged. Killing an owned paused publisher releases its lock; a later distinct process creates a report while the complete hidden temporary evidence and original owner's bytes remain identical. Corrupted-directory refusal retains every original byte. An injected unsupported-lock error refuses before creating a temporary/report file. Full/fresh candidate checks remain pending below.

Scoped implementor QA reads these scenarios and the guidebook as a caller: a loser retries the same occurrence later; a same-use competing occurrence remains refused; hidden interrupted evidence remains available without becoming a published report. Tests use local synthetic receipts only. Directory locking is cooperative and assumes a stable local directory and supported filesystem; Darwin/Python 3.14 was exercised, other hosts require verification. There is no distributed storage, hostile filesystem, power-loss, authentic native host, benchmark/improvement, independent Review or Human QA claim.

Attribution correction for this run: gpt-6.1-sol / OpenAI Codex is explicitly assigned; the reasoning tier is not exposed and remains unknown. The earlier appended High attribution was an inference and supplies no model-tier evidence.

## Candidate checks

Pushed product/test candidate: `a41c062acda0ab1d840b448b0850423b5054da48` against source base `c787b2958fa7a23f55c6406f3ce367a91e9162dc`. Draft delivery: [PR184](https://github.com/KaydenClark/Agentic-Management-System/pull/184). The working-checkout full Python suite passed **872 tests, 6 skipped in 272.89s**, using authorized loopback access for server fixtures. Its collected tests preceded the final additional post-contention retry assertion; the fresh exact-candidate run below covers the committed bytes. No site files changed and no site suites were run.

`spec-workbench render`, `doctor`, `next --json`, layout validation, Wiki validation, `git diff --check`, hygiene and synthetic observation replay ran. Hygiene: zero findings. Replay: weaker component green, acceptance miss detected/routed, unchanged replay, two fresh-process occurrences, linked recurrence. Doctor: no blocking finding, with existing S-011/TK-003 dependency exclusion, stale claims on S-006/S-002/S-011, undeclared legibility and Claude permission-scope drift. These unrelated findings remain unfixed. Fresh clone initially lacked an integration ref; configuring its owned origin and fetching main restored the same diagnostics, without changing another checkout.

Original TK-001D Task and original S-013 detection report compare byte-identical with planning head `b89b69a`; no original receipts were rewritten. Raw review bodies and all test logs remain privately retained outside the observed checkout. Diagnostic invocation/network failures are captured as FAIL-189–191 after collision inspection of main and 12 open PR heads.

Fresh immutable candidate `a41c062acda0ab1d840b448b0850423b5054da48`: **872 passed, 6 skipped in 284.52s**, with fresh clone `src` imports, Python 3.14, bytecode/cache disabled and authorized loopback. Fresh render/doctor/next, layout/Wiki validation, hygiene (zero findings), replay and diff checks passed with the same pre-existing nonblocking doctor findings. This run includes the final committed post-contention retry assertion.

Workspace preservation check at pushed record head `eaad62b` returned **accounted=false, remoteRecoverable=false, complete=false**. Missing discovery routes in integration prevent pushed-pending recovery certification; the checker also found two ignored bytecode directories produced by subprocess tests. Those owned generated files were moved intact to private retention outside this checkout and each digest verified; the baseline was not amended. No original-bytes-unverified finding occurred. The raw check and generated evidence remain private. A fresh check will still refuse release until the integration discovery requirement is satisfied. This is retained unfinished workspace recovery, not a claim of completion. FAIL-193 records it before remediation.

Task closure is expressly held for independent Standards/Spec review and exact-head shared CI. Product/test bytes remain those of `a41c062`; later commits update records only. The two Submit answers remain: **Can this exact candidate merge into main? Not yet: review and CI gates pending. Did this run meet bounded behavior acceptance? Local source behavior and scoped implementor QA pass; the Task stays open for required delivery gates.** Whole-Spec acceptance, real host observation, useful improvement and Human QA remain unproven.
