-- TK-002N schema source. Apply to an isolated test database first.
-- The native CLI is unavailable; this is deliberately not an invented
-- timestamped migration. Production migration registration remains separate.
begin;
set local lock_timeout = '5s';
set local statement_timeout = '30s';

create table public.rsi_lineage (
  namespace text not null,
  ordinal bigint not null,
  record_id text not null,
  kind text not null,
  failure_id text not null,
  chain_id text not null,
  is_test boolean not null,
  synthetic boolean not null,
  format_version integer not null default 1 check (format_version = 1),
  record_text text not null,
  record_digest text not null check (record_digest ~ '^[0-9a-f]{64}$'),
  previous_digest text check (previous_digest ~ '^[0-9a-f]{64}$'),
  parents jsonb generated always as (record_text::jsonb->'parents') stored,
  attributes jsonb generated always as (record_text::jsonb->'attributes') stored,
  recorded_at timestamptz not null default clock_timestamp(),
  primary key (namespace, record_id),
  unique (namespace, ordinal),
  unique (namespace, record_digest),
  check (record_digest = encode(sha256(convert_to(record_text, 'UTF8')), 'hex'))
);
create unique index rsi_lineage_attempt_identity on public.rsi_lineage
  (namespace, chain_id, ((attributes->>'attempt')::integer)) where kind = 'candidate';
create unique index rsi_lineage_occurrence_identity on public.rsi_lineage
  (namespace, failure_id) where kind = 'failure';
alter table public.rsi_lineage enable row level security;
revoke all on public.rsi_lineage from public, anon, authenticated;
grant select, insert on public.rsi_lineage to service_role;
revoke update, delete, truncate on public.rsi_lineage from service_role;

create function public.ams_guard_lineage() returns trigger
language plpgsql security invoker set search_path = '' as $$
declare
  r jsonb := new.record_text::jsonb;
  p jsonb := r->'parents';
  a jsonb := r->'attributes';
  needed text[];
  allowed text[];
  required_roles jsonb;
  link record;
  parent public.rsi_lineage;
  other public.rsi_lineage;
  last_row public.rsi_lineage;
  expected_kind text;
  value record;
  family text;
  occurrence_role text;
begin
  if tg_op <> 'INSERT' then raise exception 'immutable lineage' using errcode='PT409'; end if;
  if jsonb_typeof(r) <> 'object' or (r - array['namespace','record_id','kind','parents','attributes',
      'source_commit','artifact_digest','occurred_at','is_test','synthetic']) <> '{}'::jsonb
    or (select count(*) from jsonb_object_keys(r)) <> 10
    or jsonb_typeof(p) <> 'object' or jsonb_typeof(a) <> 'object'
    or jsonb_typeof(r->'is_test') <> 'boolean' or jsonb_typeof(r->'synthetic') <> 'boolean'
    or coalesce(r->>'namespace','') !~ '^[a-z][a-z0-9_-]{2,79}$'
    or coalesce(r->>'record_id','') !~ '^[A-Za-z0-9][A-Za-z0-9_.:-]{0,199}$'
    or coalesce(r->>'source_commit','') !~ '^[0-9a-f]{40}$'
    or coalesce(r->>'artifact_digest','') !~ '^[0-9a-f]{64}$'
    or coalesce(r->>'occurred_at','') !~ '^\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d(\.\d+)?Z$'
  then raise exception 'unsafe lineage shape' using errcode='23514'; end if;
  perform (r->>'occurred_at')::timestamptz;
  new.namespace := r->>'namespace'; new.record_id := r->>'record_id'; new.kind := r->>'kind';
  new.is_test := (r->>'is_test')::boolean; new.synthetic := (r->>'synthetic')::boolean;
  if (new.is_test <> (new.namespace like 'test-%')) or (new.synthetic and not new.is_test) then
    raise exception 'test/synthetic labels required' using errcode='23514'; end if;
  case new.kind
    when 'failure' then needed:=array['failure_id','family','chain_id']; required_roles:='{}';
    when 'case' then needed:=array['version']; required_roles:='{"failure":"failure"}';
    when 'candidate' then needed:=array['attempt','skills_commit']; required_roles:='{"case":"case"}';
    when 'comparison' then needed:=array['campaign_id','contract_digest']; required_roles:='{"case":"case","current_candidate":"candidate","candidate":"candidate"}';
    when 'run' then needed:=array['run_key']; required_roles:='{"comparison":"comparison","candidate":"candidate"}';
    when 'result' then needed:=array['execution_state','passed']; required_roles:='{"run":"run"}';
    when 'disposition' then needed:=array['decision']; required_roles:='{"comparison":"comparison","result":"result"}';
    when 'adoption' then needed:=array['receipt_digest','adopted_commit']; required_roles:='{"candidate":"candidate","disposition":"disposition"}';
    when 'use' then needed:=array['task_id','loaded_digest','outcome']; required_roles:='{"adoption":"adoption"}';
    else raise exception 'unknown lineage kind' using errcode='23514';
  end case;
  allowed := needed || case new.kind when 'run' then array['rsi_run_id'] when 'result' then array['rsi_result_id'] else array[]::text[] end;
  if not (a ?& needed) or a - allowed <> '{}'::jsonb
     or not (p ?& array(select jsonb_object_keys(required_roles)))
     or p - (array(select jsonb_object_keys(required_roles)) || case when new.kind='candidate' then array['previous_candidate'] else array[]::text[] end) <> '{}'::jsonb
  then raise exception 'lineage fields are allowlisted' using errcode='23514'; end if;
  for value in select * from jsonb_each(a) loop
    if value.key in ('version','attempt','rsi_run_id','rsi_result_id') then
      if jsonb_typeof(value.value) <> 'number' or value.value::text !~ '^(0|[1-9][0-9]*)$'
        or (value.value::text)::numeric > 9223372036854775807
        or (value.key<>'attempt' and (value.value::text)::numeric<1) then
        raise exception 'invalid lineage integer' using errcode='23514'; end if;
    elsif value.key='passed' then
      if jsonb_typeof(value.value) not in ('boolean','null') then raise exception 'invalid grade' using errcode='23514'; end if;
    elsif jsonb_typeof(value.value)<>'string' or not ((value.value #>> '{}') ~
      case when value.key like '%commit' then '^[0-9a-f]{40}$' when value.key like '%digest' then '^[0-9a-f]{64}$'
      else '^[A-Za-z0-9][A-Za-z0-9_.:-]{0,199}$' end) then
      raise exception 'unsafe lineage attribute' using errcode='23514';
    end if;
  end loop;
  perform pg_catalog.pg_advisory_xact_lock(710006, hashtext(new.namespace));
  select * into last_row from public.rsi_lineage where namespace=new.namespace order by ordinal desc limit 1;
  if new.previous_digest is distinct from last_row.record_digest then
    raise exception 'stale lineage head' using errcode='PT409'; end if;
  new.ordinal := coalesce(last_row.ordinal,0)+1;
  new.recorded_at := clock_timestamp();
  -- Explicit chain_id is distinct from both the Markdown occurrence ID and
  -- broad failure family. Campaign/case names never key candidate counters.
  family := case when new.kind='failure' then a->>'chain_id' else null end;
  if new.kind='failure' and exists(select 1 from public.rsi_lineage where
    namespace=new.namespace and kind='failure' and chain_id=family
    and attributes->>'family'<>a->>'family') then
    raise exception 'stable chain family changed' using errcode='23514'; end if;
  for link in select * from jsonb_each(p) loop
    expected_kind := coalesce(required_roles->>link.key,'candidate');
    select * into parent from public.rsi_lineage where namespace=new.namespace and record_id=link.value #>> '{}';
    if not found or parent.kind<>expected_kind or parent.is_test<>new.is_test or parent.synthetic<>new.synthetic then
      raise exception 'missing or incompatible lineage parent' using errcode='23514'; end if;
    if family is not null and family<>parent.chain_id then
      raise exception 'conflicting improvement chain' using errcode='23514'; end if;
    family := parent.chain_id;
  end loop;
  new.chain_id := family;
  if new.kind='failure' then new.failure_id:=a->>'failure_id';
  else
    occurrence_role:=case new.kind when 'case' then 'failure' when 'candidate' then 'case'
      when 'comparison' then 'case' when 'run' then 'comparison' when 'result' then 'run'
      when 'disposition' then 'comparison' when 'adoption' then 'candidate' when 'use' then 'adoption' end;
    select failure_id into new.failure_id from public.rsi_lineage
      where namespace=new.namespace and record_id=p->>occurrence_role;
  end if;
  if new.kind='candidate' then
    if (a->>'attempt')::integer not between 0 and 3
      or ((a->>'attempt')::integer>0) <> (p ? 'previous_candidate') then
      raise exception 'candidate attempt identity' using errcode='23514'; end if;
    if p ? 'previous_candidate' then
      select * into parent from public.rsi_lineage where namespace=new.namespace and record_id=p->>'previous_candidate';
      if (parent.attributes->>'attempt')::integer<>(a->>'attempt')::integer-1 then
        raise exception 'candidate attempt skips predecessor' using errcode='23514'; end if;
    end if;
  elsif new.kind='comparison' then
    if exists (select 1 from public.rsi_lineage where namespace=new.namespace
      and record_id in (p->>'current_candidate',p->>'candidate') and parents->>'case' <> p->>'case') then
      raise exception 'comparison case differs' using errcode='23514'; end if;
  elsif new.kind='run' then
    select * into parent from public.rsi_lineage where namespace=new.namespace and record_id=p->>'comparison';
    if parent.parents->>'candidate' <> p->>'candidate' then raise exception 'run candidate differs' using errcode='23514'; end if;
    if not new.synthetic and not exists(select 1 from public.rsi_runs where id=(a->>'rsi_run_id')::bigint
      and run_key=a->>'run_key' and is_test=new.is_test) then
      raise exception 'real run identity missing' using errcode='23514'; end if;
  elsif new.kind='result' then
    if a->>'execution_state' not in ('completed','runner_error','auth_error','timeout','capped','interrupted')
      or ((a->>'execution_state')='completed') <> (jsonb_typeof(a->'passed')='boolean') then
      raise exception 'result state/grade differs' using errcode='23514'; end if;
    select * into parent from public.rsi_lineage where namespace=new.namespace and record_id=p->>'run';
    if not new.synthetic and not exists(select 1 from public.rsi_results where id=(a->>'rsi_result_id')::bigint
      and run_id=(parent.attributes->>'rsi_run_id')::bigint and is_test=new.is_test
      and execution_state=a->>'execution_state' and passed is not distinct from (a->>'passed')::boolean) then
      raise exception 'real result identity missing' using errcode='23514'; end if;
  elsif new.kind='disposition' then
    if a->>'decision' not in ('retained','rejected','inconclusive') then raise exception 'invalid disposition' using errcode='23514'; end if;
    select * into parent from public.rsi_lineage where namespace=new.namespace and record_id=p->>'result';
    select * into other from public.rsi_lineage where namespace=new.namespace and record_id=parent.parents->>'run';
    if other.parents->>'comparison' <> p->>'comparison' then raise exception 'result comparison differs' using errcode='23514'; end if;
  elsif new.kind='adoption' then
    select * into parent from public.rsi_lineage where namespace=new.namespace and record_id=p->>'disposition';
    select * into other from public.rsi_lineage where namespace=new.namespace and record_id=parent.parents->>'comparison';
    if parent.attributes->>'decision'<>'retained' or other.parents->>'candidate'<>p->>'candidate' then
      raise exception 'adoption lacks retained candidate' using errcode='23514'; end if;
    select * into parent from public.rsi_lineage where namespace=new.namespace and record_id=p->>'candidate';
    if a->>'adopted_commit'<>parent.attributes->>'skills_commit' then raise exception 'adopted source differs' using errcode='23514'; end if;
  elsif new.kind='use' and a->>'outcome' not in ('success','failure','unknown') then
    raise exception 'invalid use outcome' using errcode='23514';
  end if;
  return new;
end; $$;
revoke all on function public.ams_guard_lineage() from public, anon, authenticated;
grant execute on function public.ams_guard_lineage() to service_role;
create trigger rsi_lineage_guard before insert or update or delete on public.rsi_lineage
  for each row execute function public.ams_guard_lineage();

create function public.ams_append_lineage(p_namespace text,p_expected_head text,p_records jsonb) returns integer
language plpgsql security invoker set search_path = '' as $$
declare item jsonb; existing public.rsi_lineage; head text; added integer:=0; missing boolean:=false;
begin
  if p_namespace !~ '^[a-z][a-z0-9_-]{2,79}$' or jsonb_typeof(p_records)<>'array' or jsonb_array_length(p_records)=0 then
    raise exception 'invalid lineage batch' using errcode='23514'; end if;
  if exists(select 1 from jsonb_array_elements(p_records) x group by (x->>'record_text')::jsonb->>'record_id' having count(*)>1) then
    raise exception 'duplicate lineage identity in batch' using errcode='23514'; end if;
  perform pg_catalog.pg_advisory_xact_lock(710006,hashtext(p_namespace));
  for item in select * from jsonb_array_elements(p_records) loop
    if item - array['record_text','record_digest'] <> '{}'::jsonb
      or item->>'record_digest' is distinct from encode(sha256(convert_to(item->>'record_text','UTF8')),'hex')
      or (item->>'record_text')::jsonb->>'namespace' is distinct from p_namespace then
      raise exception 'lineage batch identity/digest differs' using errcode='23514'; end if;
    select * into existing from public.rsi_lineage where namespace=p_namespace and record_id=(item->>'record_text')::jsonb->>'record_id';
    if found then
      if existing.record_text is distinct from item->>'record_text' then
        raise exception 'immutable lineage conflict' using errcode='PT409'; end if;
    else missing:=true; end if;
  end loop;
  if not missing then return 0; end if;
  select record_digest into head from public.rsi_lineage where namespace=p_namespace order by ordinal desc limit 1;
  if head is distinct from p_expected_head then raise exception 'stale lineage head' using errcode='PT409'; end if;
  for item in select * from jsonb_array_elements(p_records) loop
    if exists(select 1 from public.rsi_lineage where namespace=p_namespace and record_id=(item->>'record_text')::jsonb->>'record_id') then continue; end if;
    insert into public.rsi_lineage(namespace,ordinal,record_id,kind,failure_id,chain_id,is_test,synthetic,record_text,record_digest,previous_digest)
      values(p_namespace,0,'pending','pending','pending','pending',true,true,item->>'record_text',item->>'record_digest',head);
    head:=item->>'record_digest'; added:=added+1;
  end loop;
  return added;
end; $$;
revoke all on function public.ams_append_lineage(text,text,jsonb) from public, anon, authenticated;
grant execute on function public.ams_append_lineage(text,text,jsonb) to service_role;
comment on table public.rsi_lineage is 'Private immutable safe lifecycle joins. Not trial grades, qualification, adoption authority or public benefit evidence. Test/synthetic namespaces remain labelled.';
commit;
