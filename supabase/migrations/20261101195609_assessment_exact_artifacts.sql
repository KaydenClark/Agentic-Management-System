-- TK-000R: retain the original canonical artifact instead of JSONB number spelling.
set local lock_timeout = '5s';
set local statement_timeout = '30s';
lock table public.rsi_assessments in access exclusive mode;
do $$ begin
  if exists (select 1 from public.rsi_assessments) then
    raise exception 'original assessment text unavailable: preserve existing rows and reconcile before migration';
  end if;
end $$;
alter table public.rsi_assessments
  add column envelope_text text not null,
  drop constraint rsi_assessments_format_version_check,
  add constraint rsi_assessments_format_version_check check (format_version = 2),
  add constraint rsi_assessments_exact_artifact check (
    jsonb_typeof(envelope_text::jsonb) = 'object'
    and envelope_text::jsonb = envelope
    and content_digest = encode(sha256(convert_to(envelope_text,'UTF8')),'hex'));
comment on column public.rsi_assessments.envelope_text is
  'Exact original canonical packet/result JSON. Hash and replay TEXT; JSONB is only an identity/semantic projection.';
create or replace function public.ams_append_assessment(p_row jsonb) returns jsonb
language plpgsql security invoker set search_path = '' as $$
declare saved public.rsi_assessments;
begin
  perform pg_catalog.pg_advisory_xact_lock(710006, 1);
  select * into saved from public.rsi_assessments where assessment_id=p_row->>'assessment_id';
  if found then
    if (to_jsonb(saved)-array['id','recorded_at']) = p_row then return to_jsonb(saved); end if;
    raise exception 'assessment identity content changed' using errcode='PT409';
  end if;
  insert into public.rsi_assessments
    (assessment_id,failure_id,attempt,is_test,format_version,scorer_digest,content_digest,previous_digest,envelope,envelope_text)
  values (p_row->>'assessment_id',p_row->>'failure_id',(p_row->>'attempt')::integer,
    (p_row->>'is_test')::boolean,(p_row->>'format_version')::integer,p_row->>'scorer_digest',
    p_row->>'content_digest',p_row->>'previous_digest',p_row->'envelope',p_row->>'envelope_text') returning * into saved;
  return to_jsonb(saved);
end; $$;
revoke execute on function public.ams_append_assessment(jsonb) from public, anon, authenticated;
grant execute on function public.ams_append_assessment(jsonb) to service_role;
