# Handoff: orchestrator C (Coherence)

STATUS: wrapped · 2026-11-01 15:45 UTC · by orchestrator C (Claude cloud session, no secrets)

Plain-language continuation for a fresh orchestrator C. It preserves context and grants no authority. Verify live state before acting. This file lives in C's tracked lane because `workbench/sessions/handoffs/` is gitignored and would not reach a cloud cold start.

## The job

Keep the AMS coherent and up to Spec (S-013). That means three things. Run an independent review of each assembled Spec at its exact commit. Run repeated coherence sweeps: CDRs, character limits, the active-Spec cap, skills pinning, drift between `dev` and `main`, and three-strikes stops. Do web research for the site. C holds no secrets, never calls the Supabase or Vercel connectors (owner, 2026-11-01), and writes no product code.

## Verified state at `main` `b0fd71f`

**Reviews done** (receipts in this folder):

| Spec | Commit | Verdict | Receipt |
|---|---|---|---|
| S-006 (repo-only half) | `c87bf4e` | fail; opened TK-000B, TK-000C, TK-000D | [REVIEW-S-006-c87bf4e](REVIEW-S-006-c87bf4e.md) |
| S-006 (repo-only half) | `d6d4a6d` | **pass** | [REVIEW-S-006-d6d4a6d](REVIEW-S-006-d6d4a6d.md) |
| S-004 | `dd52f70` | fail; opened TK-000F to TK-000J | [REVIEW-S-004-dd52f70](REVIEW-S-004-dd52f70.md) |
| S-004 | `4d49bfc` | **pass**; layout fidelity is owner Human QA | [REVIEW-S-004-4d49bfc](REVIEW-S-004-4d49bfc.md) |

S-006's live-database half belongs to orchestrator B's local reviewer. C has not seen a recorded verdict for it.

**Reviews pending:** none assembled and waiting. The next candidates are the active Specs S-002, S-003, S-007 and S-013 (whoever reviews S-013 must not be C), once each Spec says it is assembled. Review the exact `main` commit named at that time.

**S-013 Tasks:**

| Task | State | Notes |
|---|---|---|
| TK-001 drift | done | `src/ams/coherence/drift.py` |
| TK-002 up-to-Spec | done | `src/ams/coherence/up_to_spec.py` |
| TK-003 skills sync | blocked on S-006 | It can start once S-006 is accepted, live half included. |
| TK-004 review procedure | ready in fact | The record still says blocked by TK-002 (COH-023). |
| TK-005 drift breach to Grill Board card | blocked on S-004 | S-004 now passes review, so this is ready once S-004 is accepted. |

**Open coherence findings**, from the sweep in [COHERENCE-2026-11-01](COHERENCE-2026-11-01.md) (one disposition each):

| ID | Severity | Finding |
|---|---|---|
| COH-021 | high | `dev` is 84 commits ahead of `main`, a breach ([DRIFT-2026-11-01-wrap](DRIFT-2026-11-01-wrap.md)). |
| COH-004 | high | There is no mapping from the owner's 81 items to the 107 CDRs. |
| COH-007 to COH-011 | | CDRs are bundled, duplicated, partly unsourced, or use colliding bare IDs. |
| COH-001 | | README is at 4,245 characters, over its limit. |
| COH-003 | | RUNBOOK is at 2,986 characters, so the coherence commands cannot be added. |
| COH-022 | | S-004 is at 8,218 characters and S-006 at 8,183, both over the limit. |
| COH-013 | | A Task can only be blocked by a whole Spec. |
| COH-015 | | Skills cannot be installed in cloud sessions, and doctor and claim disagree about it. |
| COH-020 | | C's checker does not resolve reference-style links. |
| COH-023 | | TK-004's blocker is stale. |

Repaired or declined: COH-005, COH-006, COH-016, COH-017 and COH-019.

## Open questions for the owner

- **COH-021:** `dev` is 84 commits ahead of `main`. Only you merge `dev` -> `main`.
- **COH-002:** does the 3,000-character root limit apply to the generated TASKBOARD (3,956 characters)?
- **COH-004:** would you like B to map your 81 confirmed items to the CDRs, so the extra and unconfirmed records can be pruned?

## Limits

C cannot message B's local session, because cross-session messages from this cloud session are refused. Requests to B travel through these records and through PRs. The PR for S-004's pass (`b0fd71f`) merged with CI green and Codex's code review clean. Codex's security review of the final merge-up commit had not finished. It had passed the previous head, and the merge-up only added `main`'s CI workflow.

## Resume point

Claim S-013 TK-004 (the independent review procedure). Clear its stale blocker first, then follow TK-004's Assignment.
