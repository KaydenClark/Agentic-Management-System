-- LMK-004 TK-003F. Apply to an isolated AMS database with the baseline
-- migrations installed. Register as a migration separately before deployment.
begin;
set local lock_timeout = '5s';
set local statement_timeout = '30s';

-- Keep the source rows outside the exposed API schema. The service role can
-- append and read, and presentation roles have only the privileges the view uses.
create schema ams_rsi_private;
revoke all on schema ams_rsi_private from public, anon, authenticated, service_role;
grant usage on schema ams_rsi_private to service_role;

create table ams_rsi_private.observations (
  event_id text primary key check (event_id ~ '^[A-Za-z0-9][A-Za-z0-9_.:-]{0,127}$'),
  chat_id text not null check (chat_id ~ '^[A-Za-z0-9][A-Za-z0-9_.:-]{0,127}$'),
  occurred_at timestamptz not null check (isfinite(occurred_at)),
  kind text not null,
  skill text check (skill ~ '^[a-z0-9][a-z0-9-]{0,63}$'),
  skill_revision text check (skill_revision ~ '^[0-9a-f]{40}$'),
  request_event_id text references ams_rsi_private.observations(event_id),
  outcome text,
  evidence_id text check (evidence_id ~ '^[A-Za-z0-9][A-Za-z0-9_.:-]{0,127}$'),
  recorded_at timestamptz not null default clock_timestamp(),
  -- Record independently observed requests, loads, uses, failures and statuses.
  -- Observed loading requires a revision and evidence. A skipped request or
  -- observed use requires a reference to its evidence.
  constraint observation_kind_fields check ((
    case kind
      when 'skill_requested' then skill is not null and skill_revision is null
        and request_event_id is null and outcome is null
      when 'skill_loaded' then skill is not null and outcome is null
        and skill_revision is not null and evidence_id is not null
      when 'skill_used' then skill is not null and outcome in ('used', 'skipped', 'unknown')
        and (outcome = 'unknown' or evidence_id is not null)
        and (outcome <> 'skipped' or request_event_id is not null)
      when 'failure' then outcome in ('routine', 'blocking') and evidence_id is not null
      when 'work_status' then skill is null and skill_revision is null and request_event_id is null
        and outcome in ('ongoing', 'finished', 'blocked')
        and (outcome = 'ongoing' or evidence_id is not null)
    end
  ) is true)
);
create index observations_request_event_id on ams_rsi_private.observations(request_event_id);

create table ams_rsi_private.skill_audits (
  audit_run_id text primary key check (audit_run_id ~ '^[A-Za-z0-9][A-Za-z0-9_.:-]{0,127}$'),
  audit_set_id text not null check (audit_set_id ~ '^[A-Za-z0-9][A-Za-z0-9_.:-]{0,127}$'),
  skill text not null check (skill ~ '^[a-z0-9][a-z0-9-]{0,63}$'),
  skills_commit text not null check (skills_commit ~ '^[0-9a-f]{40}$'),
  contract_version text not null check (contract_version = 'skill-audit-v1'),
  contract_digest text not null check (contract_digest ~ '^[0-9a-f]{64}$'),
  provider text not null check (provider ~ '^[A-Za-z0-9][A-Za-z0-9_.:-]{0,63}$'),
  model text not null check (model ~ '^[A-Za-z0-9][A-Za-z0-9_./:-]{0,127}$'),
  model_tier text not null check (model_tier in ('small', 'mid', 'high')),
  quality_passed integer not null,
  quality_total integer not null check (quality_passed between 0 and quality_total),
  regression_passed integer not null,
  regression_total integer not null check (regression_passed between 0 and regression_total),
  critical_missed boolean,
  evidence_complete boolean not null,
  completion_state text not null check (completion_state in ('completed', 'interrupted')),
  completed_at timestamptz check (isfinite(completed_at)),
  is_test boolean not null,
  is_public boolean not null,
  recorded_at timestamptz not null default clock_timestamp(),
  -- An observed miss fails a completed run even if some other evidence is
  -- missing. Interrupted, clean incomplete, and all-inapplicable runs have
  -- no pass verdict.
  passed boolean generated always as (
    case when completion_state = 'completed' then
      case
        when critical_missed or quality_passed < quality_total or regression_passed < regression_total then false
        when evidence_complete and (quality_total > 0 or regression_total > 0 or critical_missed is not null) then true
      end
    end
  ) stored,
  constraint audit_completion_fields check (
    (completion_state = 'completed') = (completed_at is not null)
    and (completion_state = 'completed' or not (is_public or evidence_complete))
  )
);
create index skill_audits_set_id on ams_rsi_private.skill_audits(audit_set_id);
create index skill_audits_public_order on ams_rsi_private.skill_audits(completed_at desc, audit_run_id)
  where is_public and not is_test and completion_state = 'completed';

alter table ams_rsi_private.observations enable row level security;
alter table ams_rsi_private.skill_audits enable row level security;
revoke all on ams_rsi_private.observations, ams_rsi_private.skill_audits
  from public, anon, authenticated, service_role;
grant select, insert on ams_rsi_private.observations, ams_rsi_private.skill_audits to service_role;
create policy observations_service_read on ams_rsi_private.observations for select to service_role using (true);
create policy observations_service_append on ams_rsi_private.observations for insert to service_role with check (true);
create policy audits_service_read on ams_rsi_private.skill_audits for select to service_role using (true);
create policy audits_service_append on ams_rsi_private.skill_audits for insert to service_role with check (true);

-- Make the public projection read-only and allowlist its columns explicitly.
-- Anonymous callers get row policy checks even when querying through the view.
create policy audits_public_read on ams_rsi_private.skill_audits for select to anon, authenticated
  using (is_public and not is_test and completion_state = 'completed');
grant select (
  audit_run_id, audit_set_id, skill, skills_commit, contract_version, contract_digest,
  provider, model, model_tier, quality_passed, quality_total, regression_passed, regression_total,
  critical_missed, evidence_complete, passed, completed_at, recorded_at, is_public, is_test, completion_state
) on ams_rsi_private.skill_audits to anon, authenticated;
-- Grade only a full public assessment set. The append boundary caps the set
-- at three runs, so a hidden or interrupted run cannot contribute to its grade.
-- An observed miss determines severity. Excellent requires complete evidence
-- and at least one applicable check. A public grade carries no qualification.
create view public.rsi_skill_audit_results with (security_invoker = true, security_barrier = true) as
  select audit_run_id, audit_set_id, skill, skills_commit, contract_version, contract_digest,
    provider, model, model_tier, quality_passed, quality_total, regression_passed, regression_total,
    critical_missed, evidence_complete, passed, completed_at, recorded_at,
    (
      select case when count(*) = 3 then
        case
          when bool_or(graded.critical_missed) then 'Broken'
          when bool_or(graded.regression_passed < graded.regression_total) then 'Functional'
          when bool_or(graded.quality_passed < graded.quality_total) then 'Stable'
          when bool_and(graded.evidence_complete) and bool_or(
            graded.quality_total > 0 or graded.regression_total > 0 or graded.critical_missed is not null
          ) then 'Excellent'
        end
      end
      from ams_rsi_private.skill_audits as graded
      where graded.audit_set_id = run.audit_set_id
        and graded.is_public and not graded.is_test and graded.completion_state = 'completed'
    ) as assessment_grade
  from ams_rsi_private.skill_audits as run
  where is_public and not is_test and completion_state = 'completed';
revoke all on public.rsi_skill_audit_results from public, anon, authenticated, service_role;
grant select on public.rsi_skill_audit_results to anon, authenticated, service_role;

-- Reject extra, missing or mistyped input fields before PostgreSQL coerces JSON
-- to column types. Private API functions pass their own closed field sets.
create function ams_rsi_private.require_row(p_row jsonb, p_fields jsonb) returns void
language plpgsql immutable security invoker set search_path = '' as $$
begin
  if jsonb_typeof(p_row) is distinct from 'object'
    or p_row - array(select jsonb_object_keys(p_fields)) <> '{}'::jsonb
    or exists (
      select 1 from jsonb_each_text(p_fields) as field(key, types)
      where not coalesce(jsonb_typeof(p_row->field.key) = any(string_to_array(field.types, '|')), false)
        or (field.types = 'number' and p_row->>field.key !~ '^(0|[1-9][0-9]*)$')
    )
  then
    raise exception 'unexpected RSI fields or value types' using errcode = '23514';
  end if;
end;
$$;
revoke all on function ams_rsi_private.require_row(jsonb, jsonb) from public, anon, authenticated, service_role;
grant execute on function ams_rsi_private.require_row(jsonb, jsonb) to service_role;

create function public.ams_append_rsi_observation(p_row jsonb) returns jsonb
language plpgsql security invoker set search_path = '' set timezone = 'UTC' as $$
declare
  incoming ams_rsi_private.observations;
  saved ams_rsi_private.observations;
begin
  perform ams_rsi_private.require_row(p_row, '{
    "event_id":"string", "chat_id":"string", "occurred_at":"string", "kind":"string",
    "skill":"string|null", "skill_revision":"string|null", "request_event_id":"string|null",
    "outcome":"string|null", "evidence_id":"string|null"
  }');
  if p_row->>'occurred_at' !~ '^\d{4}-\d{2}-\d{2}T([01]\d|2[0-3]):[0-5]\d:[0-5]\d(\.\d{1,6})?(Z|[+-]\d{2}:\d{2})$' then
    raise exception 'observation timestamp must include an offset' using errcode = '23514';
  end if;
  incoming := jsonb_populate_record(null::ams_rsi_private.observations, p_row);
  perform pg_advisory_xact_lock(710007, hashtext(incoming.event_id));
  select * into saved from ams_rsi_private.observations where event_id = incoming.event_id;
  -- Serialize by immutable identity. A replay returns the original row and
  -- timestamp. A divergent replay raises a conflict without replacing either.
  if found then
    if to_jsonb(saved) - 'recorded_at' = to_jsonb(incoming) - 'recorded_at' then
      return to_jsonb(saved);
    end if;
    raise exception 'observation identity content changed' using errcode = 'PT409';
  end if;
  -- A request reference must resolve to a request for the same chat and skill
  -- already recorded at or before this observation.
  if incoming.request_event_id is not null and not exists (
    select 1 from ams_rsi_private.observations as request
    where request.event_id = incoming.request_event_id
      and request.kind = 'skill_requested'
      and request.chat_id = incoming.chat_id
      and request.skill = incoming.skill
      and request.occurred_at <= incoming.occurred_at
  ) then
    raise exception 'missing or incompatible skill request' using errcode = '23514';
  end if;
  insert into ams_rsi_private.observations
    (event_id, chat_id, occurred_at, kind, skill, skill_revision, request_event_id, outcome, evidence_id)
  values (incoming.event_id, incoming.chat_id, incoming.occurred_at, incoming.kind, incoming.skill,
    incoming.skill_revision, incoming.request_event_id, incoming.outcome, incoming.evidence_id)
  returning * into saved;
  return to_jsonb(saved);
end;
$$;

create function public.ams_append_skill_audit(p_row jsonb) returns jsonb
language plpgsql security invoker set search_path = '' set timezone = 'UTC' as $$
declare
  incoming ams_rsi_private.skill_audits;
  saved ams_rsi_private.skill_audits;
begin
  perform ams_rsi_private.require_row(p_row, '{
    "audit_run_id":"string", "audit_set_id":"string", "skill":"string", "skills_commit":"string",
    "contract_version":"string", "contract_digest":"string", "provider":"string", "model":"string",
    "model_tier":"string", "quality_passed":"number", "quality_total":"number",
    "regression_passed":"number", "regression_total":"number", "critical_missed":"boolean|null",
    "evidence_complete":"boolean", "completion_state":"string", "completed_at":"string|null",
    "is_test":"boolean", "is_public":"boolean"
  }');
  if p_row->>'completed_at' !~ '^\d{4}-\d{2}-\d{2}T([01]\d|2[0-3]):[0-5]\d:[0-5]\d(\.\d{1,6})?(Z|[+-]\d{2}:\d{2})$' then
    raise exception 'audit timestamp must include an offset' using errcode = '23514';
  end if;
  incoming := jsonb_populate_record(null::ams_rsi_private.skill_audits, p_row);
  perform pg_advisory_xact_lock(710008, hashtext(incoming.audit_run_id));
  select * into saved from ams_rsi_private.skill_audits where audit_run_id = incoming.audit_run_id;
  -- Completed and interrupted runs are immutable occurrences. Replaying either
  -- returns its original row. New attempts need their own actual run identity.
  if found then
    if to_jsonb(saved) - array['recorded_at', 'passed'] = to_jsonb(incoming) - array['recorded_at', 'passed'] then
      return to_jsonb(saved);
    end if;
    raise exception 'audit identity content changed' using errcode = 'PT409';
  end if;
  -- Each assessment set freezes its skill, audit contract and evaluator model.
  -- Interrupted attempts stay in its three-run budget.
  perform pg_advisory_xact_lock(710009, hashtext(incoming.audit_set_id));
  if exists (
    select 1 from ams_rsi_private.skill_audits as audit
    where audit.audit_set_id = incoming.audit_set_id
      and (audit.skill, audit.skills_commit, audit.contract_version, audit.contract_digest,
        audit.is_test, audit.provider, audit.model, audit.model_tier) is distinct from
        (incoming.skill, incoming.skills_commit, incoming.contract_version, incoming.contract_digest,
          incoming.is_test, incoming.provider, incoming.model, incoming.model_tier)
  ) or (
    select count(*) from ams_rsi_private.skill_audits where audit_set_id = incoming.audit_set_id
  ) >= 3 then
    raise exception 'audit set differs from its pinned contract or has three runs' using errcode = 'PT409';
  end if;
  insert into ams_rsi_private.skill_audits (
    audit_run_id, audit_set_id, skill, skills_commit, contract_version, contract_digest, provider,
    model, model_tier, quality_passed, quality_total, regression_passed, regression_total,
    critical_missed, evidence_complete, completion_state, completed_at, is_test, is_public
  ) values (
    incoming.audit_run_id, incoming.audit_set_id, incoming.skill, incoming.skills_commit,
    incoming.contract_version, incoming.contract_digest, incoming.provider, incoming.model, incoming.model_tier,
    incoming.quality_passed, incoming.quality_total, incoming.regression_passed, incoming.regression_total,
    incoming.critical_missed, incoming.evidence_complete, incoming.completion_state, incoming.completed_at,
    incoming.is_test, incoming.is_public
  ) returning * into saved;
  return to_jsonb(saved);
end;
$$;

-- Let the trusted outbox distinguish an already recorded payload from a missing
-- one after an interrupted response, without exposing the source tables over REST.
create function public.ams_get_rsi_observation(p_event_id text) returns jsonb
language sql stable security invoker set search_path = '' set timezone = 'UTC' as $$
  select to_jsonb(saved) from ams_rsi_private.observations as saved where event_id = p_event_id
$$;
create function public.ams_get_skill_audit(p_audit_run_id text) returns jsonb
language sql stable security invoker set search_path = '' set timezone = 'UTC' as $$
  select to_jsonb(saved) from ams_rsi_private.skill_audits as saved where audit_run_id = p_audit_run_id
$$;

revoke all on function public.ams_append_rsi_observation(jsonb), public.ams_append_skill_audit(jsonb),
  public.ams_get_rsi_observation(text), public.ams_get_skill_audit(text)
  from public, anon, authenticated, service_role;
grant execute on function public.ams_append_rsi_observation(jsonb), public.ams_append_skill_audit(jsonb),
  public.ams_get_rsi_observation(text), public.ams_get_skill_audit(text) to service_role;

commit;
