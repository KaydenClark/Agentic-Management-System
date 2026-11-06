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
