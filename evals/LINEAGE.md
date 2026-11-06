# Safe RSI lifecycle lineage

S-006/TK-002N adds immutable lifecycle joins; existing `rsi_runs` and
`rsi_results` retain their measured outcomes. Persistence establishes neither
qualification, adoption authority nor useful project improvement.

`ams.lineage.Store(url, service_key)` uses the existing Python writer's HTTP
and key handling. The default REST mount is `/rest/v1`; a directly hosted
PostgREST server can explicitly use `rest_path=""`. Credentials belong only
to the trusted writer, never a candidate or public reader.

`append(records, expected_head=HEAD)` atomically saves a topologically ordered
batch. `None` names an empty namespace. An identical retry is a no-op; changed
bytes at the same identity and stale competing appends refuse. `read(namespace)`
reconstructs canonical original bytes, validates digest/predecessor continuity
and traverses the typed graph. `trace(records, record_id)` returns that record
and its ancestors in source order. Reads capture a high-water ordinal before
keyset pagination, so concurrent appends cannot shift a snapshot.

Records allow only `namespace`, `record_id`, `kind`, `parents`, `attributes`,
`source_commit`, `artifact_digest`, `occurred_at`, `is_test` and `synthetic`.
Each kind has exact parent roles and a small typed attribute allowlist;
nested packets, transcripts, arbitrary text, locators and unknown fields
refuse. The SQL guard independently validates these constraints, including
direct service-role inserts. Clients cannot select, mutate or invoke private
operations. A later public projection requires its own explicit allowlist.

The chain is failure occurrence → case → candidate/current candidate →
comparison → run → result → disposition → adoption → later use. Runs and
results without a synthetic label must reference the existing canonical RSI
row IDs. Their identity/state/grade must match those rows. A run without a
result stays a run; an interrupted outcome cannot silently become a pass.
Adoption references the retained exact source; rejected/inconclusive outcomes
cannot claim adoption through this graph. These consistency checks do not
certify the truth of a supplied qualification or adoption receipt.

Failure attributes distinguish the original intake occurrence (`failure_id`),
its broad `family`, and the stable improvement `chain_id`. Every descendant
preserves its chain. Candidate attempts are unique within namespace/chain,
with baseline 0 and candidates 1–3 requiring their immediate predecessor.
A new occurrence, case, Task or campaign label cannot reset this history;
a differently named chain cannot reuse the old candidate as its predecessor.
The original source/digest remains reachable through the candidate parents.

Test namespaces start with `test-` and require `is_test=true`. Synthetic
records additionally require `synthetic=true`; all parent labels must match.
Both labels are immutable. Synthetic acceptance fixtures prove storage only.

Commands use the existing ignored local environment/key-loading rules:

```sh
uv run ams-lineage append SAFE_RECORDS.json --expected-head DIGEST
uv run ams-lineage read NAMESPACE --trace RECORD_ID
```

Use `--expected-head ''` only for an empty namespace. A transport outage or
ambiguous response reports unpublished pending evidence, never success. Keep
the original safe input privately and reconcile by readback before retrying;
it is not another model attempt.

`supabase/lineage.sql` is the schema source for an isolated first application.
It is deliberately not an invented timestamped migration while the installed
Supabase CLI cannot start. Production migration registration/application
remains unperformed. The opt-in `tests/test_lineage_live.py` requires an
outside-repository `AMS_LINEAGE_TEST_CONFIG`, accepts only loopback URLs and
creates fresh synthetic namespaces. It exercises real Supabase PostgreSQL
and PostgREST, including raw RPC adversaries that bypass Python validation.

The isolated stack uses the versioned database and REST images from
[Supabase's official compose](https://github.com/supabase/supabase/blob/master/docker/docker-compose.yml).
Database functions follow [invoker privileges](https://supabase.com/docs/guides/database/functions)
and [row-level access controls](https://supabase.com/docs/guides/database/postgres/row-level-security).
Actual image digests and source/check identities belong in the Task receipt.
