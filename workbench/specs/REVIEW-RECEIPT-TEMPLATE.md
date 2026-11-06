# Review receipt: [scope]

> AMS-authored template, adapted from the [feedback format](../feedback/REPORT_FORMAT.md). Store it beside the reviewed Task, or link it from the owning Spec's Wiki history page (`workbench/wiki/history/S-###.md`); never paste it into the Spec.

**Reviewer / date:** [actual author]  
**Review type:** [self-review / independent review; actual prior involvement and eligibility]  
**Reviewing context:** [agent name + `review context` id; see the procedure below]\
**Candidate:** [repository + immutable commit; dirty candidates need file hashes and explicit limits]  
**Scope / exclusions:** [files, behavior, Spec and acceptance version]

## Method and evidence

[What was read, run and observed; commands/results and evidence references. Distinguish rerun checks from reported prior checks.]

## Findings

| Finding ID | Severity and impact | Location / evidence | Required correction or recommendation | Disposition / owner |
|---|---|---|---|---|

[State no findings only after actual review. Retain challenged findings and the evidence changing their disposition.]

## Conclusion

**Judgment:** [pending / changes required / no blocking findings in reviewed scope / unable to assess]  
**Unresolved findings / limits:** [values]  
**Re-review:** [changed candidate or affected scope requiring fresh assessment]

## Independent Spec review procedure

[ADR-001E](../docs/adr/001E-a-spec-needs-fresh-context-review-of-the-exact-commit.md): a Spec passes only on a review of the exact assembled commit from a context that did not build it. Run from the repository root:

1. Builders put `AMS-Context: <id>` (from `uv run python -m ams.coherence.review context`) in each commit trailer that touches or names the Spec.
2. The reviewer, in a fresh session, reads `node workbench/tools/spec-workbench.mjs report S-### --candidate SHA` and reviews that commit.
3. Record through the checker, never the bare native `verdict`:
   `uv run python -m ams.coherence.review record S-### --candidate SHA --result pass|fail --findings "none" --reviewer "MODEL MODE" --agent NAME`.
   It refuses (exit 1) a context or agent that claimed, closed or committed for the Spec, or a review naming no context; otherwise it calls `verdict` with `agent:` and `context:` (a session hash, never the id) in the reviewer cell.
4. `uv run python -m ams.coherence.review status S-### [--commit REF] [--write workbench/feedback/coherence/REVIEW-STATUS-S-###.md]` marks each verdict current, stale (the assembled commit outside the Spec's own records, or its content digest, changed), refused or unbound. It is non-blocking; a stale verdict needs a fresh review.

This receipt records the named review, not Human QA or merge/deployment approval. Link follow-up receipts; preserve the original candidate and judgment.
