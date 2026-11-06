---
type: guidebook
status: active
sensitivity: normal
knowledge_role: curated
provenance:
  - S-013 TK-001D scoped detection implementation, 2026-11-06
source_paths:
  - src/ams/coherence/observe.py
  - tests/test_coherence_observe.py
  - evals/coherence_observation_replay.py
last_verified: 2026-11-06
---

# Detect and recover coherence observations

[S-013/TK-001D](../../landmarks/LMK-004-rsi-loop-during-build/specs/S-013-coherence-checks/tasks/TK-001D/TASK.md)
owns this non-blocking check. The [RSI release graph](rsi-task-release.md) retains
all producer and assembly gates. This detects bounded observable mismatches;
it supplies no general semantic grader, repair, scheduler or adoption authority.

## Open post-merge correction

PR182 review at `b932ba0` found a rename scope/Prepare bypass and a concurrent
native-use publication race. Do not rely on those affected protections until
[TK-001A](../../landmarks/LMK-004-rsi-loop-during-build/specs/S-013-coherence-checks/tasks/TK-001A/TASK.md)
reproduces, repairs and delivers them through the required gates. Earlier
checks and Task closure remain historical evidence, not coverage of these cases.

## Replay before relying on it

From the project root:

```sh
uv run python evals/coherence_observation_replay.py
uv run pytest -q tests/test_coherence_observe.py
```

The replay creates an isolated synthetic website Task, freezes its required page
text in a source commit, then commits a page missing that text. A component check
still passes. The observer finds the escaped acceptance miss, routes it to the
same Spec/Task, publishes in the existing Markdown coherence-report lane,
replays unchanged, and records a distinct recurrence linked to the original.
A fresh process retrieves both findings for the responsible Task. The Task's
status is preserved. Output names exact fixture source/candidate identities and
elapsed time; those fixture commits are temporary, and reproducible by rerun.
They are never labeled project delivery, a real native run or improvement proof.

## Supply a bounded observation

The replay script contains the complete schema-1 contract example. Commit the
reviewed contract before the candidate change and pin that full source SHA.
An orchestrator chooses probes from the accepted Task, with authoritative source
and expected behavior; candidate code cannot replace this frozen expectation.
Each probe checks required text in an ordinary committed artifact. This seam
does not judge meaning, browser reachability or arbitrary application behavior.
Use existing browser/review procedures for those outcomes.

```sh
uv run python -m ams.coherence.observe check \
  --source SOURCE_SHA --candidate CANDIDATE_SHA \
  --contract evidence/contract.json --occurrence STABLE_OCCURRENCE_ID \
  --observed-at UTC_TIMESTAMP --write
uv run python -m ams.coherence.observe recover --spec S-003 --task TK-003
```

Replace placeholders with actual full immutable SHAs and a UTC timestamp like
`2026-11-06T09:00:00Z`. The occurrence belongs to the observed event, not a retry.
`--previous EARLIER_OCCURRENCE_ID` binds a new recurrence to its retained finding.
Reusing an occurrence with changed bytes refuses; a native use ID cannot be
recounted under another occurrence name. Recover before an orchestration pass
and before completing the responsible Task. A finding routes to that owner;
the observer never edits another writer's Task or silently completes it.

## Preparation, recurrence and skill identity

Large AMS and cross-repository shared-skill work requires existing Map/Plan
artifacts matching the frozen hashes. Missing or changed preparation, changes
outside the assignment, and changes past a Prepare stop route to S-000A with
the original failure-intake identity. Small authorized edits need no new large
workflow. Hash matching proves those declared bytes, not preparation quality
or human confirmation. An orchestrator still validates the accepted scope.

A normalized native-use receipt separates accepted source, the frozen expected
version, installed bytes, loaded bytes and observed use. Missing identity stays
unknown; stale loaded bytes produce a finding even when source is merged and
installed bytes match. An intentional baseline retains its frozen version.
Eligible-use counts include successful observations as a denominator alongside
failed occurrences. They are conditional on the supplied host receipt: this
checker does not authenticate native host observations, infer skill causation,
or qualify a repair. S-000B must establish real tool execution and trusted host
observation; S-002 owns qualification; S-011 owns adoption and later use.
All current replay/native receipt cases are synthetic. `expected-red` probes
remain separate from escaped failures and are excluded from eligible use.

## Safe evidence and operational limits

Reports contain allowlisted IDs, Git identities, digests, reason codes and owner
routes; they copy no expected text or artifact bodies. Keep contracts and any
raw source material under the project's exposure rules. Private paths and
unknown fields refuse. No provider/database credentials are forwarded to Git,
no network or product command is executed by the checker, and no Supabase or
Vercel connector is used. Publication here writes local Markdown; Git delivery
still follows the Runbook. Readback is neither acceptance nor safe-publication
review of arbitrary upstream material.

The command runs when an orchestrator invokes it; there is no background watch.
Adopt it in the existing orchestration/review pass, selecting representative
checks beyond green components. A report is a pending finding, not a disposition
decision. Canonical failure intake remains
[WORKBENCH_FEEDBACK](../../feedback/WORKBENCH_FEEDBACK.md); S-006 receives safe
derived failure/occurrence identities through its own writer. This task adds no
second failure counter, trial ledger, campaign reset or personal skill copy.
