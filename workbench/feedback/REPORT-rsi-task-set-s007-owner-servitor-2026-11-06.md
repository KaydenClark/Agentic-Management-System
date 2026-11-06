# RSI task-set comparability finding

**Disposition:** accepted-open, routed to existing S-007 ownership.
**Source:** [PR142 review](https://github.com/KaydenClark/Agentic-Management-System/pull/142#discussion_r4490731421).
**Verified candidate:** `6cdb647d2d415a8400d1d26cad2614b492c03926`.
**Investigation:** independent Astra strategy/investigation context; no implementation or live data.

The finding reproduces in both dev and held-out splits. Two runs use identical arm/provider/model/effort/grader but disjoint tasks: the first evaluates only `synthetic-old-easy-task` with three passing results; the second evaluates only `synthetic-new-hard-task` with one pass and two failures. Executing the unchanged pinned grouping code produces:

| View | Series | Observed comparison |
|---|---:|---|
| Per task | 2 | Singleton points, no regression |
| Per version | 1 | Connected3/3 to1/3 points; second marked regression |

No task was evaluated on both versions. A changed case set is therefore presented as a comparable regression. In [data.ts at the verified commit](https://github.com/KaydenClark/Agentic-Management-System/blob/6cdb647d2d415a8400d1d26cad2614b492c03926/site/app/rsi/data.ts), lines222–236 omit task identity from per-version grouping, pool rows by version and compare pass shares. The [view](https://github.com/KaydenClark/Agentic-Management-System/blob/6cdb647d2d415a8400d1d26cad2614b492c03926/site/app/rsi/view.tsx) connects the resulting graded points. This conflicts with S-007's comparable-case-set contract and ADR-002I's paired comparisons.

The disposable native-Node probe used pinned `data.ts`, `series.ts` and the existing synthetic fixture. Both split controls exited0 with the reproduction above; per-task separation supplies the negative control. No repository source, actual records, credentials or services changed. This narrow probe is not a full site/browser check.

## Existing owner and next action

[S-007](../landmarks/LMK-002-rsi-presentation/specs/S-007-rsi-charts/SPEC.md) remains the owner, with orchestrator A, reader TK-002 (`ams-records-site`) and recovery TK-0031 (`codex-rsi-recovery`) in the inspected records. Use its existing `Feature/S-007-rsi-chart-pages` lane and current claimant coordination; create no competing implementation here. PR165's grader/freshness/empty-run repairs are already merged, but do not separate task-set changes.

The owner should add this adverse case and its same-case-set control, then separate aggregate series by evaluated task set or restrict comparisons to a fixed comparable set under the existing Spec. Preserve paired task behavior, split/grader/model identities and unknown evidence. Obtain scoped verification and fresh review before treating the finding as resolved. No additional owner preference was identified by this investigation.
