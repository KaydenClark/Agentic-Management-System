# Trial metric availability

S-006's `rsi_results` stores each trial's measurements separately from its grade,
execution state and provenance. `ams.rsi_rows.Store` inserts and reads the rows;
`uv run ams-rsi livecheck` exercises tagged rows and removes them afterward.

Supply all five metric fields: `cost_usd`, `input_tokens`, `output_tokens`,
`turns`, `wall_seconds`. A measured zero is the number `0`. An unavailable value
is explicit JSON `null` (Python `None`) with an entry in `metric_unknowns`:

```json
{
  "cost_usd": null,
  "metric_unknowns": {
    "cost_usd": {
      "reason": "Subscription meter did not report per-trial cost",
      "source": "evals/runs/actual-run.json"
    }
  }
}
```

This excerpt is a shape, not an observed trial. Every null needs its own nonblank
reason and source; known values must have no unknown entry. The writer refuses
omitted fields, negative/nonfinite values, fractional token/turn counts and
values outside the database range. SQL constraints independently require each
null to have availability evidence. SQL cannot distinguish an omitted nullable
column from an explicit null; both require that evidence. Existing known rows
remain valid with the empty availability map.

Readback preserves null and its evidence. Consumers must show **unknown**, never
coalesce null to zero. Report complete totals/cost-per-pass only when all needed
measurements are known; otherwise label the result incomplete and, if useful,
show the measured subtotal with its coverage. Do not divide partial cost by a
full pass count. Current site code has no RSI reader or aggregation; S-007 must
apply this contract when implementing them.

Only public-safe reasons and source pointers belong in non-test rows; never
copy private logs, host paths or credential text. Availability does not supply
missing provider/model/pin/grade information or turn history into a controlled
trial. Assessment packets use a distinct private storage path ([contract](ASSESSMENTS.md)); they are not trial rows.
