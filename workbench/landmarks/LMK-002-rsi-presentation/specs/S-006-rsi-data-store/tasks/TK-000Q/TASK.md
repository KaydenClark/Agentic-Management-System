# TK-000Q - Private assessment history survives remote append and verified readback

**Task ID:** TK-000Q
**Spec ID:** S-006
**Slice:** Private assessment history survives remote append and verified readback
**Status:** done
**Blockers:** none
**Destination:** spec-acceptance: Private assessment persistence
**Planned verification:** Red/green append and replay tests; paginated remote readback, duplicate/conflict/resume probes; live marked synthetic roundtrip and client access refusals; full suite and room checks.
**Claimed by:** codex-assessment-writer
**Current claimant:** codex-assessment-writer
**Proof:** 56 focused; fresh source489 passed,4 skipped; private migration20261101193603; live duplicate200/conflict409/concurrent200-409/client401/update403/cleanup0; source CI45 pass

## Assignment

Owner: "Resume S-006’s approved local writer work, then continue S-002 through its authorized endpoint." S-002 requires assessment metadata, findings/retests and identity/history retention distinct from trials. Base `97bfcaa32225fd3f6fe1e00189798578a99607fc`; one writer `codex-assessment-writer`, feature branch into checked main PR. Deliver private immutable envelopes through the existing local scorer, atomic predecessor-checked append, idempotent retries, complete paginated replay and local/remote prefix verification. Raw packets have no site access. Preserve three-attempt and frozen-history safeguards. No site UI, public projection, trial or evaluator-qualification claims; no assessment reconstruction from missing source fields. Hand back to S-006; assembled Review remains separate.

## Acceptance

- [x] Remote readback retains packet/results, IDs, findings/retests and scorer identity and recomputes every result through canonical history.
- [x] Identical retry succeeds; changed ID content, divergent prefix, stale concurrent append and invalid attempts refuse without overwrite. Partial imports resume.
- [x] Raw rows and append RPC are inaccessible to site clients; only marked synthetic probes are cleaned up.
- [x] Relevant tests, live roundtrip and room checks pass; documentation states storage and qualification limits.

## Check and implementor QA

The missing remote module was observed red; 56 focused persistence/scorer tests now pass. Tests exercise page-size-one replay, exact retries, changed identities, tampered totals/digests/scorer identity, divergent prefixes, interrupted/import resume, a lost response, concurrent stale writes, reset/fourth/frozen/colliding histories, wrong filenames/symlinks, and retained original/repaired/recurred findings. CLI output contains counts and no planted private packet text.

Live migration `20261101193603` applied to the approved project; the filename matches the server-assigned identity because the installed CLI could not start. Raw table and invoker RPC have no anon/authenticated access. Tagged live probe: paginated roundtrip passes; duplicate200; changed identity409; simultaneous next appends200/409; all client GET/POST/PATCH/DELETE/RPC401; service UPDATE403; cleanup0. Role-privilege query independently confirms client raw SELECT/INSERT/RPC false. Security advisor has only the intentional informational RLS-without-policy notice for this private table.

The database guards identity, append order, stale heads and immutability. Python canonical replay checks r1 semantics; a trusted service-role caller or database administrator is not a qualified evaluator. No real assessment/trial was invented, older baseline inputs were not reconstructed, no public projection was created and no Human QA was recorded. Source `7e784494097d643e061b85a0da008298e21c2248`: full local run488 passed/4 skipped (the CLI-output test was added after that collection); full fresh clone489 passed/4 skipped. Corrected causal fixture head `4f99790413bb2ee9270fc19828da12b2a82b1f6b` changes tests only; all56 focused tests pass locally and in the updated fresh clone. Room checks pass with only the two pre-existing informational host findings. Source CI45 passed; final-head CI remains a merge gate.

## Receipt

| Run | Branch | HEAD SHA | Upstream | Dirty | Tests | Docs touched | Remaining gap | Checksum |
|---|---|---|---|---|---|---|---|---|
| 1 | codex/s006-assessment-persistence | 977575531f827a63807a4ed3aac4551927094944 | ahead 0 behind 0 | 0 | 56 focused; fresh source489 passed,4 skipped; private migration20261101193603; live duplicate200/conflict409/concurrent200-409/client401/update403/cleanup0; source CI45 pass | ASSESSMENTS; RUNBOOK; ARCHITECTURE; S-006 SPEC/TK-000Q | Final CI/checked merge; fresh assembled Review; native owner QA; safe S007 presentation and real S002 trials; close attribution: {"agent":"codex-assessment-writer","claimant":"codex-assessment-writer","onBehalfOf":null} | 1f75bc4d588e9160d65ce242a74eafd5015fa5cf7ddd1c1b5f0ed7407e1ce3b7 |

## Subsequent assembled Review failure

Independent reviewer `s006_review, independent Codex context` returned FAIL at `977ac08fed4a269182b67d6ada990042e2ceee88` (digest `cfc6d944ca5790364a2dedec20039979a70fa9ae28d83a8fd6fc579cc9562f8a`). P1: valid numeric metadata `1e20` roundtrips through JSONB as an expanded integer, invalidating the Python JSON-spelling hash and blocking private namespace readback. The reviewer ran348 relevant tests/3 skips, doctor/layout/diff; did not repeat live credentials. PostgreSQL numeric normalization is documented at https://www.postgresql.org/docs/16/datatype-json.html. Earlier successful limited probes and checks remain valid at their scope; they did not cover this failure. TK-000R owns correction and rereview. The closed Receipt is unchanged.
