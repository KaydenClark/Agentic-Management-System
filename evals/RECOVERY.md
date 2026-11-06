# Durable job and effect recovery

S-006/TK-002O extends the [safe lineage store](LINEAGE.md). Supabase owns job
state and receipts; a local outbox/checkpoint is a recovery copy, never a
second writable authority. No API here invokes a model or grants campaign,
installation or qualification authority.

`ams.recovery.Store(url, service_key, pending_dir=PRIVATE_DIRECTORY)` uses the
existing writer transport. Direct PostgREST may specify `rest_path=""`.
Service credentials stay in the trusted controller, outside case processes.

An immutable job references existing lineage case/candidate identities and
pins case bytes, source commits, release digest, Spec/Task and campaign. A
finite `slots` list freezes role, arm, repetition, effect type and payload
digest. Chain/attempt are derived from lineage, never caller counters. Slot
keys exclude job, Task and campaign labels; their semantic JSON identity is
also unique in SQL, so alternative encodings cannot reserve another effect.
Baseline 0 remains distinct from candidates 1–3; no job renaming resets them.

```text
create_job → set gates → claim
  → begin_effect (durable intent before execution)
  → supported effect/readback → observe_effect
  → finish → release after process cleanup
```

Claims use expected version, bounded server-time lease and monotonic fence.
Renew requires the current actor/fence/version; another claim, including the
same actor label, cannot steal an active lease. Refresh version after renewal.
Every new effect checks stop, approval and recent available capacity again.
Candidate disposition and consumed slots remain attached to their chain.
Uncertain completion does not become another model attempt.

`begin_effect` returns either one new execution permission or an existing
intent requiring reconciliation. A fresh controller queries the actual effect
by its stable key, then records observed payload identity, artifact and proof
digests. Matching readback seals the existing receipt; unavailable/conflicting
readback stays uncertain. Stale fences/leases cannot publish receipts. A
reserved native-call slot is never blindly repeated, even after observed
absence. A retry is available only for a frozen keyed-file contract, proven
absence, current claim and fresh gates, using the same key.

`KeyedFileEffect` is the explicitly scoped test seam: exclusive object creation,
content hashing and fsync support keyed readback. It does **not** establish
general exactly-once execution for arbitrary tools, model providers or paused
old processes. S-000B must prove its own supported reconciliation and cleanup;
unsupported native completion remains unknown rather than replayed.
Its object directory must be privately owned, outside the untrusted case tree;
the adapter is not a sandbox for an adversary replacing parent directories.

The controller writes safe mutation requests to a private local outbox before
HTTP. Unknown outcomes stay pending; explicit refusals and committed responses
are retained as receipt copies. Reconcile against canonical readback before
resubmission. Outbox files grant no execution authority and never automatically
replay a model/effect. Raw prompts, labels, transcripts and credentials are not
stored in these request projections.

## Checkpoints

`export(namespace)` captures one locked safe projection with schema/reader
identities, exact per-record digests, counts, namespace, source head, optional
predecessor export and manifest digest. It includes safe lineage, immutable job
definitions, version/fence high-water, consumed intents and receipts. Active
leases, claimant authority, approval/capacity grants and raw evidence are
excluded. Completeness means this declared projection, not a private-evidence
or whole-database backup.

Restore requires **both** the destination's expected head and an independently
trusted expected manifest digest. Never obtain that trusted pin from the file
being restored. Internal counts/hashes cannot prove an omitted independent
chain was present; the retained owner/receipt pin binds the exact export.

```python
store.restore(checkpoint, expected_head=known_destination_head,
              expected_manifest_digest=trusted_export_receipt_digest)
```

Empty compatible destinations reconstruct exact identities and receipts.
Matching restores are no-ops. An identical existing prefix may append missing
records. Divergent records, partial/private projections, unsupported reader or
schema, stale heads and changed same-ID bytes refuse atomically. An older
snapshot refuses against newer canonical data rather than rolling it back.
Nonterminal restored jobs are blocked with no live lease or grants; a fresh
claim is required to record readback of existing intents. Any new execution
also requires fresh gates; checkpoint authority cannot authorize it.
Synthetic labels and original attempt/slot identities survive restoration.

For non-synthetic run/results, only canonical table/ID/hash references are
exported. Restore requires those existing canonical parents to match under
lock; it never fabricates their raw rows or private evidence from redaction.

SQL writes are confined to a fixed-search-path definer in an unexposed private
schema, behind service-only invoker wrappers and a service-role check. Clients
cannot read or invoke private operations; even service clients cannot directly
edit operational tables to bypass fences. `supabase/recovery.sql` is isolated
schema source; production migration registration/application remains separate.
Each RPC is one database transaction. Namespace advisory locks serialize it
with lineage appends; row locks, version comparisons and SQL uniqueness protect
claims and slot intents across independent controllers. The external effect
occurs after that transaction, so recovery depends on actual effect readback.

Replay the retained operator scenarios with the two private loopback configs:

```sh
uv run pytest -q tests/test_recovery.py tests/test_recovery_live.py tests/test_recovery_checkpoint_live.py
```

Live tests opt in through `AMS_LINEAGE_TEST_CONFIG` and
`AMS_RECOVERY_RESTORE_CONFIG`. They use actual isolated PostgreSQL/PostgREST,
independent processes, crash-after-effect recovery, strict SQLSTATE adverse
controls, lost-leaf/whole-chain attacks and unchanged-target assertions.

Raw-RPC regressions also bypass Python to reject null, omitted and wrongly
typed slot roles, effect types and observation outcomes. Null control/checkpoint
parameters refuse without partial writes; only an explicit keyed-file contract
can retry a proven-absent effect.

The canonical-parent positive test additionally needs `canonical_parent_fixture`
with `run_id` and `result_id` in the private source config. Provision matching
existing canonical rows in both isolated databases before running it, preserving
their IDs and all hashed metadata; these parents are outside the safe checkpoint.
The retained fixtures are `is_test=true`, `model=no-model-call`, with unknown
metrics and an ungraded runner-error result. They are constructed as canonical
reference fixtures from the start, never by relabeling a synthetic lineage chain.
Bookkeeping guards and ordinary constraints are enabled during the proof. The
test verifies exact parent equality, hidden client reads, pinned restore and
idempotent readback; it establishes no real model measurement or public event.
