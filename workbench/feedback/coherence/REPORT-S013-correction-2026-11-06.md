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

## Later native blocker — closure withheld

Final fresh native verification after remote refresh supersedes the earlier limited doctor result: **doctor exits 1 with remote-id-collision**. The newly assigned S-013/TK-001A collides with the different published S-002/TK-001A record. The native recommended full remote fetch/prune confirmed the same blocker in both checkouts. Earlier doctors ran before complete remote-branch discovery; they remain preserved results with that limit, not final gate passes.

FAIL-196 records this actual blocker. Source inspection of the installed `move-task --replacement` route requires a done record, exact immutable source/collision revisions, Task hash and Director reason; this in-progress Task does not qualify. No move, manual identity/status edit or tool repair was attempted. Two failed read-only allocator-discovery invocations are separately retained as FAIL-197/198. Parent owns the lifecycle disposition; closure remains withheld. The full fresh 872/6 behavioral result remains valid for unchanged source/tests `a41c062`.

Updated Submit answers: **Can the candidate merge into main? No: native identity collision, independent review and exact-head CI remain required. Did the Task meet acceptance? The local bounded behaviors and scoped QA pass, but the Task remains incomplete because required native/delivery gates do not pass.** No merge, Task close, workspace release, improvement or Human QA is claimed. S-007 delegated environmental failure/retry intake was serialized as FAIL-194/195 without editing its source or claims.


## Source-qualified feedback reconciliation

Current correction identities are **FAIL-S013-PR182-C4491077658** (rename endpoints) and **FAIL-S013-PR182-C4491077662** (publication race). Earlier bare183/184 in this report and native receipts are historical references at their recorded source, not dev's different S-003/S-010 events. The canonical log's appended source-qualified table pins every owned historical189–198 intake too, without changing any original row or receipt. New reviewer/root/reader diagnostics use named source-bound occurrences, with no new ordinal. This is the existing feedback log, not a second ledger or campaign reset.

Inspection pinned main `c787b2958fa7a23f55c6406f3ce367a91e9162dc`, dev `40acb3a491a55599e5b1f00fd92a27315739a4a9`, PR184 `de50063b5b89b46cdd32a3ae25323b4f2c7fc906`, PR185 `6e58a67cf9f3f1e4e43a0f09bfa2e4dede5ecaef` and ten other open PR heads (181/180/175/174/151/145/142/135/111/101). Dev's alias convention was read directly. Other owners'183–188 rows remain untouched; no different189–198 occurrence was observed in these snapshots. Raw inspection and preservation checks remain outside the checkout.

Coordinator supplied independent Standards PASS at `de50063b5b89b46cdd32a3ae25323b4f2c7fc906`, with 33 focused passes in 10.29s after two retained environment diagnostics. That evidence is independent source review, not final-head CI, Spec acceptance or Human QA. Spec review remains active and the latest supplied original CI state is queued. Installed/package native Task recovery remains done-only: the in-progress Task collision stays open, with no fake close, manual rename or managed-runtime edit. Product/tests remain exactly `a41c062acda0ab1d840b448b0850423b5054da48`.
