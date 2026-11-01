# TK-000P - Trial metrics preserve explicit unknown values and their sources

**Task ID:** TK-000P
**Spec ID:** S-006
**Slice:** Trial metrics preserve explicit unknown values and their sources
**Status:** done
**Blockers:** none
**Destination:** spec-acceptance: Schema and provenance; Writer works end to end; Real sources only
**Planned verification:** Public writer roundtrip and rejection tests; live tagged test row readback and cleanup; database constraint probes; full room checks
**Claimed by:** codex-local-writer
**Current claimant:** codex-local-writer
**Proof:** 475 passed,4 skipped; focused99/1; migration20261101192328; live null and zero roundtrip; DB bad availability23514; client writes401/test hiding; cleanup0; advisors empty

## Assignment

Owner resumes S-006 approved local writer work then S-002 through its authorized endpoint. S-002's settled subscription-meter rule says unknown cost/tokens stay unknown, never zero. At main 7053866 the writer and database require all five metric values to be numbers, preventing truthful records.

One local implementor owns schema, Python writer/tests and documentation, plus this Task/Spec and generated board. Target main via checked feature PR and merge commit. Preserve existing architecture, provenance, optimistic concurrency, RLS and known values. Require each metric field at the writer seam; an explicit null requires its own nonblank reason/source. Reject malformed/nonfinite/negative values and fractional counts. Readback must preserve unknown and known zero distinctly. Live probes use marked test rows and clean them up.

Do not invent trials, grades, model IDs or missing measurements. Distinct assessment persistence remains separate. The site currently has no RSI reader/aggregation; document the future consumer contract without implementing website changes or promoting the site. No paid purchase or deployment.

## Acceptance

- [x] Explicit unknown metrics roundtrip with reasons/sources; known zero stays known zero.
- [x] Writer refuses omitted metrics, unproven nulls, contradictory availability, nonfinite/negative values and fractional counts.
- [x] Database constraints reject unproven null/contradictory availability; existing known rows remain valid.
- [x] Live marked-row roundtrip passes; site key cannot write or see test rows; cleanup zero remaining.
- [x] Consumer documentation forbids coalescing unknown to zero or reporting partial sums as totals; required checks pass.

## Check and implementor QA

- Red/green: unknown-metric public writer tests initially 19 failed/18 passed;
  after implementation, focused tests passed. Livecheck extension failed first
  for missing roundtrip output, then passed. Oversized integer regression failed
  first with OverflowError; now refused safely. Final focused: 99 passed, 1 skip.
- `uv run pytest -q`: 475 passed, 4 skipped. Render stable; doctor no blocking
  finding (two existing host informational findings); layout and ADR valid;
  diff check clean.
- Remote migration `20261101192328_rsi_metric_availability` applied. Installed
  and temporary official CLI were terminated by the host with SIGKILL; used the
  supported remote migration tool and recovered its actual version from migration
  history for the repository filename, rather than inventing a timestamp.
- Live `ams-rsi livecheck`: unknown metrics and known zero roundtrip yes;
  stale update refused; test rows invisible; every site write 401; cleanup 0.
- Raw service-key probes independently refused unproven null, blank reason,
  contradictory known value, NaN and unsupported metric key (23514); cleanup 0.
  Final database count: 0 result rows, including 0 test rows.
- Security advisors: no lints. Helper EXECUTE denied to anon/authenticated,
  granted to service_role; helper is invoker with empty search_path.

Judgment: all five Task criteria met. Null and known zero remain distinct through
writer, database and readback. No new real trial or assessment was created.
The site currently has no reader/aggregation to repair; its future consumer
contract is explicit. S-002 assessment storage and real qualified trials remain.

## Receipt

| Run | Branch | HEAD SHA | Upstream | Dirty | Tests | Docs touched | Remaining gap | Checksum |
|---|---|---|---|---|---|---|---|---|
| 1 | codex/s006-unknown-metrics | 70538664906d66a3f7597f1e3228e3b1ab697379 | none | 9 | 475 passed,4 skipped; focused99/1; live unknown and zero roundtrip; raw DB invalid availability23514; site writes401/test rows hidden; cleanup0; security advisors empty; room checks valid | TRIAL-ROWS; result template; rsi_rows docstring; S-006 SPEC/TK-000P | Fresh assembled Review; distinct private assessment persistence and S-002 real trials | 55393812c472e057b065d0dd16e9b51ba44491fb741287a2fcb49e0e0df726be |
| 2 | codex/s006-unknown-metrics | 9afdb9ee7e0be510777c61a3c38eca1f66dadf71 | ahead 0 behind 0 | 0 | 475 passed,4 skipped; focused99/1; migration20261101192328; live null and zero roundtrip; DB bad availability23514; client writes401/test hiding; cleanup0; advisors empty | TRIAL-ROWS; template; rsi_rows; S-006 SPEC/TK-000P | Fresh assembled Review; private assessment storage; real qualified S-002 trials; close attribution: {"agent":"codex-local-writer","claimant":"codex-local-writer","onBehalfOf":null} | 2ff206112497a20fe907b0c6b513a3d81ff2b615d3832d8fedaca16469308224 |
