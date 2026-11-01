# Local r1 assessments

`uv run ams-assess` is S-002's manual assessment intake, scorer and local
readback. It makes no model calls. These records are not S-006 rows or behavioral
trials, and the website does not read them. The historical Loop #1 baseline is
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
  classes block acceptance. Recorded findings are retained even when omitted.
- `retests`: optional `findingId`, repaired `revision`, `originalCheckId` and
  `regressionCheckIds`, or a substantive `regressionExclusionReason`. Resolution
  requires qualified Yes evidence for the original and all named regressions in
  all three runs on a revision different from the original finding. An exclusion
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
