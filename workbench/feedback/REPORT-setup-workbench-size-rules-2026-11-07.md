# setup-workbench: generated writer and project size rules disagree

Status: recorded for investigation; no shared-skill repair authorized or performed here.
Owner: setup-workbench source in KaydenClark/skills; AMS consumes its generated tools.
Failure: FAIL-215. Source: Kayden’s direct request, 2026-11-07, to record this failure so a new chat can investigate and fix setup-workbench’s size rules.

## Observed mismatch

The RSI Map initially exceeded AMS’s 8,000-character Spec/Landmark limit (FAIL-210). The agent used the supplied `workbench/tools/record-parts.mjs` pagination API. It successfully emitted `.md.part-…` files and primary references; native record/Wiki checks accepted that structure. This did not satisfy the project’s publication rules.

`src/ams/hygiene.py` defines `RECORD_LIMIT = 8000`, applies it to physical record files and rejects every tracked filename containing `.part-`. The first resumed hygiene run therefore reported eight split-record findings. The additional untracked Landmark page was not included because hygiene scans `git ls-files`.

`planRecordWrite` accepts selected sections and a page budget, defaulting to 15,000 characters; it neither applies AMS’s 8,000-character primary-file limit nor consults its no-split rule. `paginateRecord` forwards these options and returns the resulting primary character count without rejecting an oversized primary. A previous pagination retry left LMK-004 at 8,597 characters (FAIL-213). This establishes a generated-tool/project-policy mismatch and an agent preflight mistake, not yet the exact upstream cause.

Inspection base: AMS main `5f0c1d783cdf04fdf9fd87c5c54caf61aaf132a8`; generated source and hygiene were unchanged by this Map. The failed pagination candidate is retained in local commit `469745bf7429d09fdd4bbc0ed53258196256d79d` and its parent. No public availability of that local commit is assumed until publication.

## Expected result

Generated writing guidance and tools respect the consuming project’s declared record sizes and split policy. In AMS, a Spec/Landmark remains one file of at most 8,000 characters, with requirements preserved. A successful write must not imply publication eligibility when a required project check rejects it. Detect unsupported pagination and primary-file overflow before mutation, or route explicitly to a permitted compacting operation. Preserve other projects’ legitimate pagination where allowed.

## Continue in a new chat

1. Recover this report, FAIL-210/213/215, current AMS rules and setup-workbench’s source/package/generated-runtime lineage. Verify current source/install versions; do not edit generated tool bytes directly or replace the active personal catalog.
2. Trace where setup-workbench discovers, records and enforces a project’s size/no-split policy. Inspect writer callers, templates, validators, hygiene and tracked/untracked coverage. Distinguish missing policy configuration, missing enforcement and stale generated copies before choosing a repair.
3. Map/Plan the smallest source-owned correction. Preserve requirements, existing accepted workflows, project-specific limits and allowed pagination elsewhere; do not hard-code AMS policy globally or weaken hygiene.
4. Reproduce the discrepancy, then verify exact/over-limit boundaries, prohibited and allowed splitting, oversized primary after pagination, stale/partial writes and no mutation on refusal. Include a real AMS record write/readback and the consumer’s final hygiene check.
5. Follow author-skill and setup-workbench qualification/delivery/update authority. Keep investigation, source repair, generated-tool adoption, personal installation and observed use distinct. This report creates no Task, launches no repair and resets no existing attempts.

## Current Map correction

The Map removes its own generated parts and condenses the original destination records; it does not modify setup-workbench, tools, limits or hygiene. Final Map checks/publication remain separately evidenced in the PR and LMK-004 history. Repairing this Map does not establish that the reusable failure is fixed.
