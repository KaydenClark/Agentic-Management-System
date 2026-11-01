# TK-000Q - Private assessment history survives remote append and verified readback

**Task ID:** TK-000Q
**Spec ID:** S-006
**Slice:** Private assessment history survives remote append and verified readback
**Status:** in-progress
**Blockers:** none
**Destination:** spec-acceptance: Private assessment persistence
**Planned verification:** Red/green append and replay tests; paginated remote readback, duplicate/conflict/resume probes; live marked synthetic roundtrip and client access refusals; full suite and room checks.
**Claimed by:** codex-assessment-writer
**Current claimant:** codex-assessment-writer

## Assignment

Owner: "Resume S-006’s approved local writer work, then continue S-002 through its authorized endpoint." S-002 requires assessment metadata, findings/retests and identity/history retention distinct from trials. Base `97bfcaa32225fd3f6fe1e00189798578a99607fc`; one writer `codex-assessment-writer`, feature branch into checked main PR. Deliver private immutable envelopes through the existing local scorer, atomic predecessor-checked append, idempotent retries, complete paginated replay and local/remote prefix verification. Raw packets have no site access. Preserve three-attempt and frozen-history safeguards. No site UI, public projection, trial or evaluator-qualification claims; no assessment reconstruction from missing source fields. Hand back to S-006; assembled Review remains separate.

## Acceptance

- [ ] Remote readback retains packet/results, IDs, findings/retests and scorer identity and recomputes every result through canonical history.
- [ ] Identical retry succeeds; changed ID content, divergent prefix, stale concurrent append and invalid attempts refuse without overwrite. Partial imports resume.
- [ ] Raw rows and append RPC are inaccessible to site clients; only marked synthetic probes are cleaned up.
- [ ] Relevant tests, live roundtrip and room checks pass; documentation states storage and qualification limits.

## Check and implementor QA

The missing remote module was observed red; 56 focused persistence/scorer tests now pass. Tests exercise page-size-one replay, exact retries, changed identities, tampered totals/digests/scorer identity, divergent prefixes, interrupted/import resume, a lost response, concurrent stale writes, reset/fourth/frozen/colliding histories, wrong filenames/symlinks, and retained original/repaired/recurred findings. CLI output contains counts and no planted private packet text.

Live migration `20261101193603` applied to the approved project; the filename matches the server-assigned identity because the installed CLI could not start. Raw table and invoker RPC have no anon/authenticated access. Tagged live probe: paginated roundtrip passes; duplicate200; changed identity409; simultaneous next appends200/409; all client GET/POST/PATCH/DELETE/RPC401; service UPDATE403; cleanup0. Role-privilege query independently confirms client raw SELECT/INSERT/RPC false. Security advisor has only the intentional informational RLS-without-policy notice for this private table.

The database guards identity, append order, stale heads and immutability. Python canonical replay checks r1 semantics; a trusted service-role caller or database administrator is not a qualified evaluator. No real assessment/trial was invented, older baseline inputs were not reconstructed, no public projection was created and no Human QA was recorded. Full suite/fresh clone/CI remain pending before delivery.
