# Desired Behavior (part 1)

[Record](SPEC.md#desired-behavior)

<!-- workbench-record-body:start context=0 format=2 -->

- A per-chat Python observer records skill requests, loading, actual use and failures as distinct evidence, with chat/event identity and observed source version. It reacts to available session events; unavailable or interrupted observation is explicit, never invented success. S-013 owns detection/classification and S-006 durable shared history.
- The orchestrator starts routine repair after the current work finishes; blocking repair proceeds in a separate chat. One repair may be active per skill across participating chats; duplicate triggers join its history rather than create competing repairs. Completion and ownership must survive interruption.
- The first proof runs on Servitor. Draft and related skills run in a separate AMS website test session. Keep candidate loading isolated from everyday skills until qualified merge; preserve actual loaded identities and the website task end state.
- Workbench setup does not require RSI. Participation enables observer/repair behavior explicitly; no silent observation, credentials or Supabase account requirement for ordinary skill use.


- Start locally in Python using supported Codex/Claude harnesses and isolated workspaces, with actual tools needed by each case. Host availability is visible; Supabase availability does not imply a running worker. Always-on hosting and paid upgrades are not authorized.
- Consume S-006 durable jobs referencing existing Spec/Task scope, frozen S-002 contracts, exact sources and campaign authorization. Reuse existing records rather than create a second project tracker.
- Record actual provider/model/effort, host and loaded skill identities. Use Mid/Small by default, High when needed with reason recorded. Freeze conditions within comparisons; preserve older campaign pins. Author and deciding evaluator are independent; accepted-version graders cannot be edited by the candidate.
- Continue eligible stages within campaign authority; stop at required approval, meter unavailability/exhaustion, explicit stop or attempt exhaustion. Never silently purchase API capacity or switch models to continue. Unknown meter state is explicit and does not justify an unlimited run.
- Preserve initial attempt -> retry -> retry -> stop, baseline excluded. Rename, repair, restart and re-delivery cannot reset counters. Transport recovery is distinct from another model execution; uncertain completion is reconciled before retry, and every actual attempt remains visible.
- Atomic claims, bounded ownership and progress receipts prevent simultaneous writers. After interruption, determine whether work completed, failed or has an unknown outcome; recover evidence or block for resolution before replaying effects. Duplicate notifications cannot create duplicate jobs, commits or result rows.
- Operational recovery, candidate revision and adoption monitoring have separate states. A grader failure is not a measured skill failure or pass. A merge is not installation or actual host loading. For this mapped loop, eligible merged repairs automatically update everyday Servitor skills under S-011; Map itself performs no installation. Other installation scopes retain their own authority.
- Keep credentials in trusted execution/writer boundaries; candidate agents cannot access private graders, database secrets or unrestricted publication. Preserve sandbox rules and unrelated work. Short scheduling/queue mechanisms are optional implementation choices, not mandates for new services.

<!-- workbench-record-body:end -->
