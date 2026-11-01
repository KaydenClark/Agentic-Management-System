# Local r1 assessments

`uv run ams-assess` is S-002's manual assessment intake, scorer and local
readback. It makes no model calls. Local records can be imported into S-006’s private assessment store below.
They remain separate from behavioral trials; the website cannot read raw packets. The historical Loop #1 baseline is
unchanged; its incomplete/unqualified evidence is not silently upgraded.

```bash
uv run ams-assess score evals/assessment-example.json
uv run ams-assess record packet.json --store .local/assessments
uv run ams-assess list --store .local/assessments
```

The example is synthetic, deliberately unqualified and incomplete; it is a format
example, never a measured AMS result. Use a separate store for synthetic exercises.
Keep private evidence in its authorized local location. Public packets may contain
only safe pointers/summaries; this command does not sanitize arbitrary input.

## Packet contract (schema 1)

The JSON example supplies the shape. Required fields:

- `assessmentId`: unique immutable identity; `assessedAt`: ISO timestamp with
  timezone; `failureId`: stable identity of the original failure, shared by its
  baseline and all repairs. A display `label` does not change this identity.
- `attempt`: baseline `0`, then candidate `1`, `2`, `3`. A baseline is required
  before recording candidates. Renames and repairs continue the existing count.
- `rubric`: r1, check version 1 and approved source SHA-256. No new check IDs or
  class demotion. The 47 IDs/classes are from audit-workbench's approved r1.
- `candidate`, `baseline`, `skillsCommit`, `inventoryRevision`: full commit/hash
  identities. `scope`: `bounded` or `whole`. `conditions` names the host, tools,
  worker model, effort and loaded artifact identities. Whole scope covers all ten
  areas; an exclusion still needs substantive justification by the assessor.
- `inventory`: each included `id` and original `class`. A Quality check may be
  `Regression` only with `baselineEvidence` bound to `baseline`, recording
  `result: Yes` and `qualification: qualified`. Never infer a pass from a label.
- `excludedChecks`: every other r1 ID with its scope reason; an inventory omission
  cannot silently remove the obligation. Inventory and exclusions are disjoint.
- `evaluator`: exact model, prompt revision, qualification and candidate-bound
  qualification evidence. This records supplied qualification, not certification
  by this CLI. Keep an unqualified assessor explicitly unqualified.
- `runs`: exactly three distinct `runId`s, each with `rows`. Rows name an inventory
  `id`, `result`, `qualification` and `evidence`. Evidence has `type`
  (`harness-inspection`, `observed-use`, `behavioral-test`), `revision` equal to
  the candidate, and `locator`. Evidence must actually prove the obligation at
  the claimed strength; a syntactically valid pointer cannot prove its truth.
- `historicalFindings`: optional prior findings with `findingId`, `checkId`,
  `class`, original `candidate`, `sourceRunId` and observation. Unmapped historical
  classes or check mappings block acceptance. Later packets may fill missing
  `checkId`/`class` fields and a missing original `candidate` commit; existing
  mappings and source facts cannot change. Closure also needs a known original
  or latest failure commit, different from the repaired revision.
  A historical ID colliding with a current finding's different check/class is
  refused before writing; old metadata cannot hide a new Regression.
  Enrichment keeps the finding open until its normal retest. Recorded findings
  are retained even when omitted.
- `retests`: optional `findingId`, repaired `revision`, `originalCheckId` and
  `regressionCheckIds`, or a substantive `regressionExclusionReason`. Resolution
  requires qualified Yes evidence for the original and all named regressions in
  all three runs on a revision different from the latest failure, including recurrence. An exclusion
  is an assessor judgment; the CLI checks its presence, not its correctness.

Rows may be Yes, No or N/A with a reason. Unknown, Unrun, refused, interrupted,
missing rows and empty required evidence become No in the original class and
denominator. An observed No with evidence is complete evidence of failure;
missing proof is separately incomplete. Unqualified evidence never becomes
qualified merely because its row says Yes.

## Results and retained history

The CLI pools counts, reports the reduced exact percentage fraction (no rounding),
and separates `level`, `evidenceState`, `qualification` and `assessmentAccepted`.
An empty denominator has null percentage fields and cannot be accepted. Critical
failure overrides to Broken. Quality-only failure does not fail a run. Open
Critical/Regression findings and unmapped history prevent acceptance.

`retentionAccepted` remains false: retaining an improvement also requires the
predeclared useful-benefit comparison, controls and later-use judgment. This
scorer supplies none of those. A bounded result cannot certify whole AMS.

`record` freezes the comparison's original failure, baseline, rubric,
inventory/exclusions, scope, conditions and evaluator. Candidate/skills revisions
may change on repair. A changed grader or rubric needs a separately authorized,
qualified series; this CLI refuses to mix it into the existing series. It never
silently resets the failed candidate's counter. `nextAction: compare-benefit`
means only that audit acceptance passed; `stop` means three unsuccessful candidate
assessments have been recorded. There is no automated proposer or runner.

Records contain the original packet and recomputable result. IDs cannot be
reused for changed evidence; an identical retry returns the saved result. Readback
recomputes totals and finding transitions. One directory lock serializes writers;
a crash may leave `.record-lock` or a malformed incomplete file. Inspect that
interrupted state before recovery; never delete failures to restart a campaign.
This is a local, cooperating-writer integrity boundary, not tamper-proof storage.

The owner resumed S-002 on 2026-11-01. Use the existing subscription meter for
manual trials; unknown usage stays unknown. No API campaign budget or new paid
service is implied. S-006 persistence, qualified behavioral graders, the noise
floor/controls and coordination with the existing grilling redesign remain
required before the end-to-end improvement claim.

## Private Supabase persistence

`uv run ams-assessment-store import --store DIRECTORY` validates the entire local
store and the remote history before appending. `readcheck` paginates and recomputes
private results without printing packets; `--test` selects a separate synthetic
namespace. `livecheck` creates only marked probes, checks raw-table/RPC access
refusals and cleans its own chain. Keys load from the local gitignored environment.

Each immutable envelope retains its packet/result, assessment/failure/attempt/run
identities, frozen conditions, evidence, qualification, findings and retests.
The record stores format version and SHA-256 of the canonical scorer source.
Use the recorded reader revision when that digest changes; a changed scorer is
refused rather than silently reinterpreting old acceptance. Readback recomputes
canonical transitions and totals and verifies content/predecessor digests.

A transactional append RPC serializes writes, requires the expected chain head,
and refuses missing baseline, skipped/reset/fourth attempts and changed identity.
Exact retries are idempotent, including after a lost response. Import resumes a
matching prefix and refuses divergence without overwrite. The database protects
identity/order/immutability; Python replay supplies r1 semantic checks. A trusted
service-role caller can supply structurally valid false evidence; persistence is
not evaluator qualification or tamper-proof administration.

Raw `rsi_assessments` has no public/client SELECT policy or privileges. No raw
packet, locator, host metadata or private text is published. There is no public
summary or website reader in this slice; S-007 still owns safe presentation.
The historical baseline has its original older format and incomplete/unqualified
evidence; do not invent missing fields to import or upgrade it. No controlled
trial, useful benefit or Human QA is established by successful storage.
