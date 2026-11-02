# Approved pinned history import — actual verification

On 2026-11-02 the owner answered **“Approve this history import”** to the explicit local-writer question. Approval is captured as JOT-ada1ea57-1afe-40b0-986d-eb4567bc2884 in the existing active-Spec approvals owner. The prior two pre-execution authorization rejections remain historical evidence.

## Exact scope

- Data main: `771bd1e264ff15ab89217c8f91f79fc38c57f96b`; dev: `fe9870fe93f715c859fc5059b0b4c52f38f4a640`.
- Checked collector: `3a25cacf797743ca8189739a46661ec4e3a76a09`, contained in engineering main `c67ca8d3f8c07c4a1eb6380eca036397359f0337`; its runtime bytes are unchanged.
- Lifecycle/Git records came from a detached snapshot at main771; both explicit refs and the installed cutoff convention (`2026-11-02T01:38:27-07:00`) were applied through `collect(Sources(...))`. The import CLI alone would not pin lifecycle HEAD, so it was not used with ambiguous defaults.
- Existing destination: `hqvtnpvwwppbeurponnn`, `build_events` only. Local `load_settings` read the existing ignored environment file in place. No key value was printed, copied or stored in proof.
- Frozen rows SHA256: `c4c765a9578848fc6e5b80a27e1c55e45b7e6ad7dad9f125c71e5a0a00251bb7`. The exact same 1,161-row payload governed import, direct canonical readback and pinned global comparison. Later c67/history-proof records are **not imported** by this approval.

## Actual outcome

One `import_rows(..., refresh_changed=True)` call completed: **131 inserted, 1,030 already recorded, 41 refreshed**. Six POSTs returned201, 41 conditional Task PATCHes returned200, and six subsequent import/readback GETs returned200. No DELETE, schema change, alternate destination or write retry occurred.

Direct current readback matches all **74 canonical Task birth projections**, including source-key presence; zero mismatches. This is independent of historical refresh-state matching. Pinned global `readcheck` returns0: missing0, extra0, newer-than-ref0, content mismatches0, unsourced0, and rows ordered. All 1,161 keys are unique.

All original **three S-008** rows retain e0ca3a8 creation provenance and require no refresh. All **eight archived S-003/S-007 facts** remain exact, including original source commits. F and renumbered K remain historical identity declarations for the same coverage assignment, not two independent work executions; no old Task was reactivated.

Before/after audit proves every prior ID retained, all 989 unrefreshed old rows identical, every one of 41 refreshes preserving unrelated annotations/prior audit and exact previous values, bounded canonical undo without recursive audit copies, and current values matching the frozen source.

## Actual changes

All refreshes are Task rows. There were 26 summary/time/URL/detail corrections, four time/URL/detail corrections, one summary/detail correction and ten metadata-only corrections. The current corrected reader detected and verified all of them.

| Identity | Refreshed fields |
|---|---|
| S-001/TK-001 | occurred_at, source_url, detail |
| S-001/TK-002 | occurred_at, source_url, detail |
| S-001/TK-003 | occurred_at, source_url, detail |
| S-002/TK-000M | detail |
| S-002/TK-000N | detail |
| S-002/TK-000O | summary, detail |
| S-002/TK-001 | summary, occurred_at, source_url, detail |
| S-002/TK-002 | summary, occurred_at, source_url, detail |
| S-002/TK-003 | summary, occurred_at, source_url, detail |
| S-002/TK-004 | summary, occurred_at, source_url, detail |
| S-003/TK-001 | summary, occurred_at, source_url, detail |
| S-003/TK-002 | summary, occurred_at, source_url, detail |
| S-003/TK-003 | summary, occurred_at, source_url, detail |
| S-003/TK-004 | summary, occurred_at, source_url, detail |
| S-003/TK-005 | summary, occurred_at, source_url, detail |
| S-004/TK-000A | detail |
| S-004/TK-001 | summary, occurred_at, source_url, detail |
| S-004/TK-002 | summary, occurred_at, source_url, detail |
| S-004/TK-003 | summary, occurred_at, source_url, detail |
| S-004/TK-004 | summary, occurred_at, source_url, detail |
| S-005/TK-000K | occurred_at, source_url, detail |
| S-005/TK-001 | summary, occurred_at, source_url, detail |
| S-005/TK-002 | summary, occurred_at, source_url, detail |
| S-005/TK-003 | summary, occurred_at, source_url, detail |
| S-006/TK-000E | detail |
| S-006/TK-000L | detail |
| S-006/TK-000P | detail |
| S-006/TK-000Q | detail |
| S-006/TK-000R | detail |
| S-006/TK-000S | detail |
| S-006/TK-001 | summary, occurred_at, source_url, detail |
| S-006/TK-002 | summary, occurred_at, source_url, detail |
| S-006/TK-003 | summary, occurred_at, source_url, detail |
| S-006/TK-004 | detail |
| S-007/TK-001 | summary, occurred_at, source_url, detail |
| S-007/TK-002 | summary, occurred_at, source_url, detail |
| S-007/TK-003 | summary, occurred_at, source_url, detail |
| S-013/TK-001 | summary, occurred_at, source_url, detail |
| S-013/TK-002 | summary, occurred_at, source_url, detail |
| S-013/TK-003 | summary, occurred_at, source_url, detail |
| S-013/TK-004 | summary, occurred_at, source_url, detail |

Inserted record counts: commit 77, correction 10, merge 10, pr_opened 10, spec_event 6, task 6, task_claimed 5, task_receipt 7.

## Evidence and limits

Primary local evidence retains frozen rows/inputs/failures and hashes, planned changes, actual before/after public readbacks, HTTP status/count trace, direct-current comparison, global pinned output and per-row undo audit. These artifacts contain no service key and remain available to independent review; complete API data is not duplicated here.

This proves only the expressly approved main771/devfe snapshot using the checked corrected collector. It does not claim latest c67 coverage, a second import, whole-S006 acceptance, owner Human QA, W completion, trial/evaluator qualification or improvement. The Build-history acceptance coverage judgment remains with independent whole-S006 review; W stays stopped/unaccepted and actual owner QA remains open.
