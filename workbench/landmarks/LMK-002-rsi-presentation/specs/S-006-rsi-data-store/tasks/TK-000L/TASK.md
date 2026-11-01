# TK-000L - Review FAIL at d6d4a6d corrected: readcheck pinned to a ref and comparing content; legacy-key claim narrowed

**Task ID:** TK-000L
**Spec ID:** S-006
**Slice:** Review FAIL at d6d4a6d corrected: readcheck pinned to a ref and comparing content; legacy-key claim narrowed
**Status:** in-progress
**Blockers:** TK-000B
**Destination:** spec-acceptance: Build history from real records; Key loads and authenticates; Real sources only
**Planned verification:** red-first pytest for each finding; after merge, live `ams-history import --refresh-changed`, then `ams-history readcheck --ref <main SHA> --dev-ref <dev SHA>` (missing 0, extra 0, content mismatches 0), every livecheck and keycheck

## Assignment

**Target branch:** `main`. Branch from `origin/main`, open a PR into `main` and merge it once current and checked, per `AGENTS.md`.
**Claimed by:** orch-b
**Current claimant:** orch-b

Orchestrator B's lane only. Orchestrator B's live-half review of the assembled Spec at `d6d4a6d65cc6287b667fe78ee5db937440972a5e` returned FAIL (strike 2 of 3, ADR-002W). Correct its findings:

- **N2.** `ams-history readcheck` derives its expected rows from moving refs and live GitHub, so every later merge fails it, and it prints only counts. Pin it to `--ref` (default HEAD) and keep GitHub events up to that ref's commit time. Dev-only rows count only with `--dev-ref`. Name missing, extra and mismatched keys. Rows newer than the ref are not extra.
- **N1.** readcheck compares keys only. Compare subject, summary, time and link; fail on a mismatch. Rows changed by condensing (L1) are updated only through a logged `import --refresh-changed`.
- **Legacy key.** Narrow the claim to what is proven: `sb_secret_` live, legacy JWT by fakes only. keycheck sends the writers' headers.
- **N3.** Page review threads past 100 PRs.
- **N5.** Each livecheck refusal names its expected constraint.
- **N6.** Fill the Spec's slice table and cite the real candidate.
- **N4.** Record the baseline migration version drift.

Out of scope: completing S-006; a fresh independent review decides that.

Hand back to S-006 with `close`.

## Acceptance

- [x] A pinned readcheck passes with a later merge stored and fails, naming the key, on a missing earlier row.
- [x] A service-key edit to a real row's summary fails readcheck and is named.
- [x] Live after merge: missing 0, extra 0, content mismatches 0 at the new main SHA.
- [x] Livechecks name the expected constraint for every refusal; keycheck sends the writers' headers.
- [x] Spec: slice table filled, candidate cited, legacy-key and migration-drift limits recorded.
- [x] `uv run pytest` passes.

## 2026-11-01 merge follow-up

Owner requested merging all non-site work while retaining unfinished branches.
Resolved the generated Taskboard conflict by rendering current records. Added
regressions for late-discovered fix rows and legacy metadata backfill: both failed
before repair and passed afterward. Review-fix rows now keep their earliest
source reply time; pinned readchecks exclude fixes first derivable after the ref.
Explicit refresh backfills that metadata. Runbook import/readcheck scopes now
both include dev. Full checks and merge evidence are recorded in PR #65.
The live database verification and Task acceptance remain unfinished; this merge
request does not authorize accessing the local service key or refreshing live data.

## Receipt

| Run | Branch | HEAD SHA | Upstream | Dirty | Tests | Docs touched | Remaining gap | Checksum |
|---|---|---|---|---|---|---|---|---|
| 1 | codex/s006-local-verification | 5aa2621ec03a1d419615374ec31e4c3db12069b6 | none | 0 | Main 5aa2621/dev c0f6c67: live history 943 rows, missing/extra/mismatch/unsourced 0; summary tamper detected/restored; key/writer/RSI/source livechecks pass; pytest 433 passed,4 skipped | S-006 SPEC; TK-000L live evidence and limits | Fresh assembled Review; S-002 assessment persistence and unknown metrics compatibility remain | 64e5bf35f977574ca99a1d4670c1acd3ce7ec656a66c49bd7a9e97c3de521e99 |

## Resumed local verification, 2026-11-01

Owner instruction: "Resume S-006’s approved local writer work, then continue S-002 through its authorized endpoint." This resumes approved local writer scope beyond the earlier merge-only limitation. The resumed implementor acts on behalf of recorded claimant `orch-b`; earlier Review verdicts remain.

Verified main `5aa2621ec03a1d419615374ec31e4c3db12069b6`, dev `c0f6c67687f432cd75b55e7d4fdad460ea2f77db`:

- `ams-keycheck`: loaded sb_secret, authenticated HTTP 200; no key printed.
- `ams-history import --refresh-changed`: 292 inserted, 651 already recorded, 37 logged refreshes retaining previous values.
- `ams-history readcheck --ref 5aa2621ec03a1d419615374ec31e4c3db12069b6 --dev-ref c0f6c67687f432cd75b55e7d4fdad460ea2f77db`: 943 rows; missing, extra, content mismatches and unsourced all 0; ordered; one newer row excluded. Pinned/missing/later-row regressions pass in pytest.
- A live service-key summary edit on that main commit's real history row failed readcheck and named `mismatch: commit commit 5aa2621ec03a1d419615374ec31e4c3db12069b6: summary`. Original summary restored and read back in a finally block.
- `ams-writer readcheck d2686e69e0c871aa309f4f7c5975e8518bc74b46`: site SELECT 200, two real rows, INSERT/UPDATE/DELETE 401, unchanged.
- `ams-rsi livecheck`: missing skills pin and stale-update constraints refused; test rows hidden, all client writes refused; cleanup remaining 0.
- `ams-sources livecheck`: each expected source/strength constraint named; test rows hidden on all tables; cleanup remaining 0.
- `uv run pytest -q`: 433 passed, 4 skipped. Initial sandbox run could not bind loopback sockets; the authorized rerun with loopback permission passed.

QA: all six Task criteria met. Native tasks/ records own slices; duplicate table rows are refused by the runtime. Legacy JWT remains fake-only; baseline migration drift remains documented. No trial or assessment rows invented. Task completion does not complete the Spec or its independent Review.

Additional limit: `ams-writer record-merge` accepts GitHub's default `Merge pull request #...` title and refused main's custom `Merge PR #78` title; `ams-history` imported its actual commit and PR through the broader source route. S-002 still needs distinct assessment persistence and truthful unknown metrics; no real trial completion claimed.
