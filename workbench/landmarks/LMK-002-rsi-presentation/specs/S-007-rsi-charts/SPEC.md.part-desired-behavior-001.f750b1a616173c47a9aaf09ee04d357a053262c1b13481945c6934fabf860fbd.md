# Desired Behavior (part 1)

[Record](SPEC.md#desired-behavior)

<!-- workbench-record-body:start context=0 format=2 -->

- RSI Charts show each skill’s Quality Score, Regression Score, Critical result and overall severity grade as distinct results, with actual completed audit counts (including fewer than three), versioned denominators, failed attempts and evidence limits. Whole-Workbench Alignment remains a separately labeled assessment.
- Show requested/loading/use failures distinctly; skipped explicitly requested skills count as failed requested uses and Critical failures. Later-use views identify the accepted version actually loaded and recurrence; no uses means no recurrence rate, not a proven fix.


- Follow S-003's shared data contract: distinguish populated, successful-empty, loading and unavailable states; identify the last successful read and any retained data. A failed read never becomes “no trials.” Static explanations and chart spaces remain visible.
- Explain the website build using sourced S-006 build events alongside the measured results. Readable prose connects the events; it need not itself be stored as rows. Distinguish build activity, assessments and demonstrated improvement. This page supplies the build-evidence explanation; S-003 has no separate “Under the hood” page.

- Chart places for each planned series exist from the first deploy.
- **Empty state.** With no rows a chart says that no trials are recorded yet, explains what a task, trial and version are, and names the next expected event. No sample chart or placeholder number.
- Results are shown per task and per version; dev and held-out are visibly separate.
- Each series shows its provenance: provider, model, effort and system version. A model change starts a new series.
- Regressions, variants, removed versions and fired stop rules are shown.
- Every number links to its rows. Each row's strength label is shown.
- **Headlines** come only from held-out tasks, with the interval and the baseline. An interval including zero reads as no difference detected at this size.
- Synthetic or test rows never render.

### Learning evidence views

Provide per-skill and whole-Workbench views from S-006, joined to canonical failure IDs rather than copied independent logs. Show lifecycle stage/age and blockers, candidate lineage and dispositions, paired baseline/candidate results with regressions, and later-use recurrence per eligible use. Owner interventions, runtime and available usage metrics show effort alongside outcomes. A skill-by-case matrix distinguishes pass, failure, unrun and unavailable evidence.

Every displayed metric identifies its case set/version, actual model/host/skills, sample size, evidence strength and freshness. Keep fixed benchmark trends separate from expanded historical coverage; imports or improved detection cannot appear as worsening reliability. Distinguish development/held-out results, operational errors, Fitness/Alignment levels and demonstrated benefit. No independently maintained numeric website dataset replaces the canonical Supabase rows; explanatory prose and clearly labeled test fixtures remain allowed.

<!-- workbench-record-body:end -->
