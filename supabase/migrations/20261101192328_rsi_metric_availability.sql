-- S-006 TK-000P: preserve unavailable measurements, never invent zero.
-- Existing known rows and all provenance/RLS/version controls remain unchanged.
set local lock_timeout = '5s';
set local statement_timeout = '30s';

create function public.ams_metric_available(measurement numeric, unavailable jsonb)
returns boolean
language sql immutable
set search_path = ''
as $$
  select case when measurement is not null then
    unavailable is null and measurement >= 0
      and measurement::text not in ('NaN', 'Infinity', '-Infinity')
  else coalesce(
    jsonb_typeof(unavailable) = 'object'
    and jsonb_typeof(unavailable->'reason') = 'string'
    and length(btrim(unavailable->>'reason')) > 0
    and jsonb_typeof(unavailable->'source') = 'string'
    and length(btrim(unavailable->>'source')) > 0, false)
  end;
$$;
revoke execute on function public.ams_metric_available(numeric, jsonb) from public, anon, authenticated;
grant execute on function public.ams_metric_available(numeric, jsonb) to service_role;

alter table public.rsi_results
  alter column cost_usd drop not null,
  alter column input_tokens drop not null,
  alter column output_tokens drop not null,
  alter column turns drop not null,
  alter column wall_seconds drop not null,
  add column metric_unknowns jsonb not null default '{}'::jsonb,
  add constraint rsi_results_metric_unknowns_object check (
    jsonb_typeof(metric_unknowns) = 'object'
    and metric_unknowns - array['cost_usd','input_tokens','output_tokens','turns','wall_seconds']::text[] = '{}'::jsonb),
  add constraint rsi_results_metric_availability check (
    public.ams_metric_available(cost_usd, metric_unknowns->'cost_usd')
    and public.ams_metric_available(input_tokens, metric_unknowns->'input_tokens')
    and public.ams_metric_available(output_tokens, metric_unknowns->'output_tokens')
    and public.ams_metric_available(turns, metric_unknowns->'turns')
    and public.ams_metric_available(wall_seconds, metric_unknowns->'wall_seconds'));

comment on column public.rsi_results.metric_unknowns is
  'Each null metric maps to its unavailable reason and source. Known zero has no entry. Never coalesce null to zero or present partial sums as totals.';
