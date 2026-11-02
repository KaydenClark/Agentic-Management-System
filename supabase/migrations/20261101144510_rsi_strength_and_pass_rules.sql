-- S-006 TK-000E (review M2, L2 at c87bf4e): RSI rows are graded evidence.
-- recorded_fact labels build history read from records, so the RSI tables refuse it;
-- a completed trial must carry passed (pass rate and cost per pass, ADR-002J), and
-- score stays optional detail on a completed trial only. Both tables held 0 rows.

alter table public.rsi_runs
  add constraint rsi_runs_trial_strength check (strength <> 'recorded_fact');

alter table public.rsi_results
  add constraint rsi_results_trial_strength check (strength <> 'recorded_fact');

alter table public.rsi_results
  drop constraint rsi_results_graded_when_completed;

alter table public.rsi_results
  add constraint rsi_results_passed_when_completed check (
    (execution_state = 'completed') = (passed is not null));

alter table public.rsi_results
  add constraint rsi_results_score_when_completed check (
    score is null or execution_state = 'completed');
