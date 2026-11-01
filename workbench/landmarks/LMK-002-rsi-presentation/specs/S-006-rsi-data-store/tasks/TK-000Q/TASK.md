# TK-000Q - Private assessment history survives remote append and verified readback

**Task ID:** TK-000Q
**Spec ID:** S-006
**Slice:** Private assessment history survives remote append and verified readback
**Status:** ready
**Blockers:** none
**Destination:** spec-acceptance: Private assessment persistence
**Planned verification:** Red/green append and replay tests; paginated remote readback, duplicate/conflict/resume probes; live marked synthetic roundtrip and client access refusals; full suite and room checks.

## Assignment

Owner: "Resume S-006’s approved local writer work, then continue S-002 through its authorized endpoint." S-002 requires assessment metadata, findings/retests and identity/history retention distinct from trials. Base `97bfcaa32225fd3f6fe1e00189798578a99607fc`; one writer `codex-assessment-writer`, feature branch into checked main PR. Deliver private immutable envelopes through the existing local scorer, atomic predecessor-checked append, idempotent retries, complete paginated replay and local/remote prefix verification. Raw packets have no site access. Preserve three-attempt and frozen-history safeguards. No site UI, public projection, trial or evaluator-qualification claims; no assessment reconstruction from missing source fields. Hand back to S-006; assembled Review remains separate.

## Acceptance

- [ ] Remote readback retains packet/results, IDs, findings/retests and scorer identity and recomputes every result through canonical history.
- [ ] Identical retry succeeds; changed ID content, divergent prefix, stale concurrent append and invalid attempts refuse without overwrite. Partial imports resume.
- [ ] Raw rows and append RPC are inaccessible to site clients; only marked synthetic probes are cleaned up.
- [ ] Relevant tests, live roundtrip and room checks pass; documentation states storage and qualification limits.
