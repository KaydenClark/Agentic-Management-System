# Desired Behavior (part 1)

[Record](SPEC.md#desired-behavior)

<!-- workbench-record-body:start context=0 format=2 -->

- **Up to Spec.** For each active Spec, compare delivered behavior on `main` or `dev` with its acceptance criteria and report gaps.
- **Skills pinned and in sync.** Every RSI row names a skills commit; report rows whose commit is behind the current skills `main` and sessions that could not install skills.
- **`dev` ahead of `main`.** Report commits and days `dev` is ahead of `main`, with a threshold that raises a Grill Board item.
- **Independent Spec review.** A fresh-context reviewer passes or returns the exact assembled commit against the Spec's conditions; a changed commit needs a fresh review.
- Reports are committed records; findings are visible, never silently fixed.
- **Preparation routing.** Detect a large shared-skill or other AMS change proceeding without its Map/Plan or past a Prepare stop. Route the [recorded failure](../../../../feedback/REPORT-skills-workbench-bypass-2026-11-02.md) and recurrence to [S-000A](../S-000A-skills-refocus/SPEC.md) for source repair; check preparation before claiming a reliability improvement. This addition is preparation only.

### Failure detection and use evidence

The S-000B per-chat Python observer supplies events. Detect requests, loading, actual use and failures distinctly; skipping an explicitly requested skill is Critical and counts as failed requested use, including a skill named in chat. Unknown observation must remain unknown; the mere presence of a skill file proves no use. This observer does not give the secret-free coherence actor access to credentials. Route failures to the owning cause and one active repair per skill; do not misclassify every tool/environment problem as a skill defect.


Detect and route observed mismatches before owner prompting, preserving a separate occurrence for each recurrence. Link detection to the existing failure intake and S-006 safe identities; classify suspected cause without asserting skill causation from involvement alone. Count eligible successful uses alongside failures for later recurrence measurement.

Distinguish accepted source version, installed bytes, actual host loading and observed use. A deliberately pinned baseline is not an accidental stale installation; report the condition rather than silently upgrading a comparison. S-000B owns recovery; S-002 qualification/retention. Installation needs separate authority; C stays secret-free.

<!-- workbench-record-body:end -->
