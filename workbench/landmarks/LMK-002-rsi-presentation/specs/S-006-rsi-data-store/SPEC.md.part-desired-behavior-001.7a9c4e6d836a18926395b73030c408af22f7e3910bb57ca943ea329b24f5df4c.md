# Desired Behavior (part 1)

[Record](SPEC.md#desired-behavior)

<!-- workbench-record-body:start context=0 format=2 -->

- Persist chat/request/loading/use/failure identities separately, plus one occurrence for each true recurrence, candidate/skill versions, repair claims, attempts, three audit run identities, class counts, Critical results, grade, merge/update/loading and later-use evidence. An explicitly requested but skipped skill is a failed requested use, not an excluded non-use.
- Replayed transport is idempotent; missing/offline evidence remains pending and visible. Retain historical assessment contracts and failed attempts; new skill grading cannot relabel old r1 assessments. Public projections expose safe fields only, never raw transcripts, private research or credentials.


- Existing RSI result/run tables retain task, split, control arm, runtime/controls/skills commits, provider/model/effort, completion, grade and source. Assessments remain separate from behavioral trials.
- Presentation data is read-only to clients; private assessments and operational state are not publicly readable. Only the authorized worker writes lifecycle records; candidate agents receive no database credentials.
- Supabase owns worker-written, commit-pinned cases, runs, candidates, comparisons and dispositions. Git fixtures/contracts are referenced artifacts, not competing live statuses. Supabase owns shared failure and improvement history. Existing Markdown intake is a local capture/recovery route; transport references stable IDs, source revisions and corrections without creating a competing canonical shared history or duplicate occurrences. Git owns skill source and regression test versions.
- Link failures, case versions, experiment contracts, candidate parents, jobs, results, decisions and adoption/use receipts. Extend existing identities rather than creating a second ledger. Table/queue technology is left to implementation.
- Persist job authorization, claim, attempt, stage, next action and stop/block reason. Atomic claims and version conflicts prevent duplicate ownership; interrupted or uncertain writes reconcile before replay. S-000B owns execution semantics.
- Keep raw transcripts local/private. Store only safe derived fields and evidence identities. Git-committed exports preserve safe records, schema and completeness checkpoints; restore preserves attempts/corrections and refuses stale conflicts. Exports are recovery copies, not writable authorities; exclude secrets, host paths and private raw packets.
- Distinguish measured usage, subscription-meter availability and optional API-equivalent estimates; unknown is never zero or an invented bill. Free-plan outages/capacity failures remain visible; retain pending local evidence without claiming publication. No paid upgrade or cloud upload of raw evidence is implied.
- Build history comes from real Spec/Task/PR/commit events, including returns and corrections. Seeds carry source and strength; synthetic/test rows never reach the site.

<!-- workbench-record-body:end -->
