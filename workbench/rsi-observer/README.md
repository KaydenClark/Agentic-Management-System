# Optional RSI observer

A participating Workbench calls Python for each observed event. The process records the event, updates chat state and exits. The calling integration supplies stable opaque IDs and evidence references. The same input on restart returns the same identity. Workbench use requires no observer or credentials until a project opts in by invoking it.

```sh
uv run python -m ams.rsi_observer record event.json
uv run python -m ams.rsi_observer status chat-1
uv run python -m ams.rsi_observer audit-score packet.json
uv run python -m ams.rsi_observer audit-record --test packet.json
uv run python -m ams.rsi_observer flush
```

Run from the project root or put `--project PATH` before the command. Input defaults to stdin. Local recording creates `.local/observer.sqlite3` in this directory. Keep it private. Event, run and set IDs are immutable. A restarted flush checks the exact remote row before retrying and acknowledges it only after matching readback. A failed or uncertain response leaves evidence pending. Run flush only from the authorized trusted writer with its Supabase service-role settings. The client uses the trusted writer's environment or the selected project's ignored `.env`.

## Observation input

```json
{
  "event_id": "request-1",
  "chat_id": "chat-1",
  "occurred_at": "2026-11-07T09:00:00Z",
  "kind": "skill_requested",
  "skill": "setup-workbench"
}
```

`skill_requested` records an explicit request. `skill_loaded` independently records a load with an observed `skill_revision` commit and an opaque `evidence_id`. When the loaded revision is unavailable, leave the load unconfirmed. `skill_used` has a `used`, `skipped` or `unknown` outcome. A linked load or use names an earlier `request_event_id` for the same chat and skill. Used and skipped outcomes require an opaque `evidence_id`. A skip also needs an explicit request. A load alone leaves the use unknown, and a skipped request appears in `critical_failure_ids`. Supply opaque identifiers only and retain source evidence privately.

`failure` records a `routine` or `blocking` outcome and an evidence ID. `work_status` records `ongoing`, `finished` or `blocked`. Finished and blocked require evidence of the corresponding work state. An absent status is unknown. A reply, chat switch or chat closure leaves this status unchanged. The caller owns the evidence and any decision to schedule repair.

## Audit input

Use `version: skill-audit-v1`, an `audit_set_id`, `skill`, and full `skills_commit`, `candidate` and `baseline` commits. Pin the shared r1 `rubric`, the `conditions` of the audit and the `evaluator` with qualification evidence when applicable. Freeze the check inventory by ID and class. Quality checks use the shared IDs. Regression and additional Critical checks use the skill's own IDs. Supply up to three actual runs with stable `audit_run_id`, `completion_state`, UTC `completed_at` for completed runs and the applicable check results with candidate evidence. Justify N/A on its check. An interrupted run can retain partial rows. The synthetic packet in the observer tests shows every required field.

Actual runs contribute applicable checks to the assessment totals, including interrupted runs. Missing, unknown, refused or interrupted evidence contributes a No. Only completed runs count as completed, and unrun slots contribute no checks. Exact scores use passed/total, and zero totals mean unavailable. Skill qualification requires three complete runs, a qualified evaluator and a Stable or Excellent grade. Repair acceptance and useful benefit are separate decisions. Historical r1 scoring keeps its own entry point and semantics.

`audit-record` retains the frozen packet and runs in the private local database. Each transport row contains the allowlisted identity, model metadata, completion and score counts only. Completed rows stay private by default. Use `--test` for synthetic fixtures, and use `--public` only with publication authority. Interrupted rows stay private.
