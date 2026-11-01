# TK-000L - Review FAIL at d6d4a6d corrected: readcheck pinned to a ref and comparing content; legacy-key claim narrowed

**Task ID:** TK-000L
**Spec ID:** S-006
**Slice:** Review FAIL at d6d4a6d corrected: readcheck pinned to a ref and comparing content; legacy-key claim narrowed
**Status:** ready
**Blockers:** TK-000B
**Destination:** spec-acceptance: Build history from real records; Key loads and authenticates; Real sources only
**Planned verification:** red-first pytest for each finding; after merge, live `ams-history import --refresh-changed`, then `ams-history readcheck --ref <main SHA> --dev-ref <dev SHA>` (missing 0, extra 0, content mismatches 0), every livecheck and keycheck

## Assignment

**Target branch:** `main`. Branch from `origin/main`, open a PR into `main` and merge it once current and checked, per `AGENTS.md`.

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

- [ ] A pinned readcheck passes with a later merge stored and fails, naming the key, on a missing earlier row.
- [ ] A service-key edit to a real row's summary fails readcheck and is named.
- [ ] Live after merge: missing 0, extra 0, content mismatches 0 at the new main SHA.
- [ ] Livechecks name the expected constraint for every refusal; keycheck sends the writers' headers.
- [ ] Spec: slice table filled, candidate cited, legacy-key and migration-drift limits recorded.
- [ ] `uv run pytest` passes.
