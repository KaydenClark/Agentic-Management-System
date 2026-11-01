-- S-006 TK-000Q: private assessment envelopes, not behavioral trial rows.
set local lock_timeout = '5s';
set local statement_timeout = '30s';
create table public.rsi_assessments (
  id bigint primary key,
  assessment_id text not null unique check (length(btrim(assessment_id)) > 0),
  failure_id text not null check (length(btrim(failure_id)) > 0),
  attempt integer not null check (attempt between 0 and 3),
  is_test boolean not null,
  format_version integer not null check (format_version = 1),
  scorer_digest text not null check (scorer_digest ~ '^[0-9a-f]{64}$'),
  content_digest text not null check (content_digest ~ '^[0-9a-f]{64}$'),
  previous_digest text check (previous_digest is null or previous_digest ~ '^[0-9a-f]{64}$'),
  envelope jsonb not null,
  recorded_at timestamptz not null default now(),
  unique (failure_id, is_test, attempt),
  constraint rsi_assessments_envelope_identity check (
    coalesce(jsonb_typeof(envelope) = 'object'
    and envelope - array['packet','result']::text[] = '{}'::jsonb
    and jsonb_typeof(envelope->'packet') = 'object'
    and jsonb_typeof(envelope->'result') = 'object'
    and jsonb_typeof(envelope->'packet'->'assessmentId') = 'string'
    and jsonb_typeof(envelope->'packet'->'failureId') = 'string'
    and jsonb_typeof(envelope->'packet'->'attempt') = 'number'
    and envelope->'packet'->>'assessmentId' = assessment_id
    and envelope->'packet'->>'failureId' = failure_id
    and envelope->'packet'->>'attempt' = attempt::text
    and envelope->'result'->>'assessmentId' = assessment_id
    and envelope->'result'->>'attempt' = attempt::text, false)
  )
);
create sequence public.rsi_assessments_id_seq owned by public.rsi_assessments.id;
alter table public.rsi_assessments enable row level security;
revoke all on public.rsi_assessments from public, anon, authenticated;
grant select, insert, delete on public.rsi_assessments to service_role;
revoke update, truncate on public.rsi_assessments from service_role;
grant usage, select on sequence public.rsi_assessments_id_seq to service_role;
comment on table public.rsi_assessments is
  'Private immutable raw r1 packets/results. No public SELECT policy. Supplied evidence and qualification are not certified by persistence.';

create function public.ams_guard_assessment() returns trigger
language plpgsql security invoker set search_path = '' as $$
declare prior public.rsi_assessments;
begin
  -- Serialize all appends to keep committed identity order stable for keyset snapshots.
  perform pg_catalog.pg_advisory_xact_lock(710006, 1);
  if tg_op = 'DELETE' then
    if not old.is_test then raise exception 'real assessment deletion refused' using errcode='PT409'; end if;
    return old;
  end if;
  if tg_op = 'UPDATE' then raise exception 'immutable assessment update refused' using errcode='PT409'; end if;
  select * into prior from public.rsi_assessments
    where failure_id=new.failure_id and is_test=new.is_test order by attempt desc limit 1;
  if found then
    if new.attempt <> prior.attempt+1 or new.previous_digest is distinct from prior.content_digest
       or new.scorer_digest <> prior.scorer_digest then
      raise exception 'stale assessment predecessor or scorer' using errcode='PT409';
    end if;
  elsif new.attempt <> 0 or new.previous_digest is not null then
    raise exception 'assessment baseline required' using errcode='PT409';
  end if;
  -- Allocate only after serialization, including direct trusted-service inserts.
  new.id := nextval('public.rsi_assessments_id_seq'::regclass);
  return new;
end; $$;
revoke execute on function public.ams_guard_assessment() from public, anon, authenticated;
grant execute on function public.ams_guard_assessment() to service_role;
create trigger rsi_assessments_append_guard before insert or update or delete
  on public.rsi_assessments for each row execute function public.ams_guard_assessment();

create function public.ams_append_assessment(p_row jsonb) returns jsonb
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
    (assessment_id,failure_id,attempt,is_test,format_version,scorer_digest,content_digest,previous_digest,envelope)
  values (p_row->>'assessment_id',p_row->>'failure_id',(p_row->>'attempt')::integer,
    (p_row->>'is_test')::boolean,(p_row->>'format_version')::integer,p_row->>'scorer_digest',
    p_row->>'content_digest',p_row->>'previous_digest',p_row->'envelope') returning * into saved;
  return to_jsonb(saved);
end; $$;
revoke execute on function public.ams_append_assessment(jsonb) from public, anon, authenticated;
grant execute on function public.ams_append_assessment(jsonb) to service_role;
