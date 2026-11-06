# S-013 corrective validation — TK-001A

## Preserved findings and red evidence

Original source base: `c787b2958fa7a23f55c6406f3ce367a91e9162dc`, containing reviewed implementation `b932ba0211e7368c13f4114d09c9f4df222fdb2c`. Planning head: `b89b69a`. Product bytes remained unchanged through the separate inventory binding commit `2463dab`.

FAIL-183 and FAIL-184 were recorded validation-pending before this run. Both reproduce on those unchanged product bytes. Command (Python 3.14, project `src` on PYTHONPATH, bytecode/cache disabled): `python -m pytest -p no:cacheprovider -q tests/test_coherence_observe.py -k 'move_checks or competing_processes'`.

Observed before repair: **3 failed, 1 passed, 27 deselected**. Outside-to-allowed move returned no findings instead of `assignment-scope`; product-to-record move returned no findings instead of `prepare-stop-bypass`; within-allowed move passed. With first real publisher paused after fsync and before exclusive link, a distinct second process returned `created` instead of controlled refusal. The first publisher then also completed. These are synthetic owned Git/local-filesystem fixtures, not native host-use or improvement proof. Raw output is retained privately outside the checkout. Original TK-001D and earlier evidence remain unchanged.

Repair and final validation: pending. Independent review, exact-head shared CI, delivery, Human QA and whole-Spec acceptance remain separate gates. No campaign or attempt counters reset.
