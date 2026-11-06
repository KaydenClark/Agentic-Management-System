-- TK-002O isolated schema source. Production migration registration is separate.
begin;
set local lock_timeout='5s';
set local statement_timeout='30s';
create schema ams_recovery_private;
revoke all on schema ams_recovery_private from public,anon,authenticated;
grant usage on schema ams_recovery_private to service_role;

create table public.rsi_jobs (
  namespace text not null,
  job_id text not null,
  job_text text not null,
  job_digest text not null check(job_digest=encode(sha256(convert_to(job_text,'UTF8')),'hex')),
  chain_id text not null,
  candidate_id text not null,
  case_digest text not null,
  release_digest text not null,
  attempt integer not null check(attempt between 0 and 3),
  version bigint not null default 1 check(version>=1),
  fence bigint not null default 0 check(fence>=0),
  claimant text,
  lease_until timestamptz,
  state text not null default 'blocked' check(state in('ready','running','effect_uncertain','awaiting_evidence','completed','failed','blocked','stopped')),
  terminal_state text check(terminal_state in('completed','failed','stopped')),
  evidence_digest text check(evidence_digest ~ '^[0-9a-f]{64}$'),
  approved boolean not null default false,
  capacity text not null default 'unknown' check(capacity in('available','unknown','exhausted')),
  capacity_observed_at timestamptz,
  capacity_digest text,
  stop_requested boolean not null default false,
  block_reason text default 'approval-required',
  primary key(namespace,job_id),
  unique(namespace,chain_id,candidate_id,case_digest,release_digest),
  foreign key(namespace,candidate_id) references public.rsi_lineage(namespace,record_id)
);
create table public.rsi_effects (
  namespace text not null,
  effect_key text not null check(effect_key ~ '^[0-9a-f]{64}$'),
  job_id text not null,
  key_text text not null check(effect_key=encode(sha256(convert_to(key_text,'UTF8')),'hex')),
  slot_identity jsonb generated always as (key_text::jsonb) stored,
  payload_digest text not null check(payload_digest ~ '^[0-9a-f]{64}$'),
  intent_fence bigint not null check(intent_fence>=1),
  version bigint not null default 1 check(version>=1),
  state text not null default 'pending' check(state in('pending','uncertain','absent','completed')),
  observation_text text,
  receipt_digest text check(receipt_digest ~ '^[0-9a-f]{64}$'),
  primary key(namespace,effect_key),
  unique(namespace,slot_identity),
  foreign key(namespace,job_id) references public.rsi_jobs(namespace,job_id),
  check((state='completed')=(receipt_digest is not null)),
  check(receipt_digest is null or receipt_digest=encode(sha256(convert_to(observation_text,'UTF8')),'hex'))
);
alter table public.rsi_jobs enable row level security;
alter table public.rsi_effects enable row level security;
revoke all on public.rsi_jobs,public.rsi_effects from public,anon,authenticated,service_role;
grant select on public.rsi_jobs,public.rsi_effects to service_role;

-- Definer authority is confined to this unexposed schema. Public wrappers
-- are invoker functions, service-only. Even service clients cannot directly
-- UPDATE a fence/receipt or bypass the transactional state machine.
create function ams_recovery_private.require_service() returns void
language plpgsql security definer set search_path='' as $$
begin
  if coalesce(nullif(current_setting('request.jwt.claims',true),''),'{}')::jsonb->>'role' is distinct from 'service_role' then
    raise exception 'service controller required' using errcode='42501';
  end if;
end; $$;

create function ams_recovery_private.validate_job(p_text text,p_digest text) returns jsonb
language plpgsql security definer set search_path='' as $$
declare x jsonb:=p_text::jsonb; s jsonb; entry record;
begin
  if p_digest is distinct from encode(sha256(convert_to(p_text,'UTF8')),'hex')
    or jsonb_typeof(x) is distinct from 'object' or (select count(*) from jsonb_object_keys(x))<>14
    or x-array['namespace','job_id','spec_id','task_id','campaign_id','case_id','candidate_id','case_digest',
      'skills_commit','release_digest','source_commit','is_test','synthetic','slots']<>'{}'::jsonb
    or jsonb_typeof(x->'is_test') is distinct from 'boolean' or jsonb_typeof(x->'synthetic') is distinct from 'boolean'
    or coalesce(x->>'namespace','') !~ '^[a-z][a-z0-9_-]{2,79}$'
    or jsonb_typeof(x->'slots') is distinct from 'array' or jsonb_array_length(x->'slots') not between 1 and 64
    then raise exception 'unsafe job definition' using errcode='23514'; end if;
  if p_text is distinct from public.ams_canonical_jsonb(x) then
    raise exception 'job JSON must retain canonical reader bytes' using errcode='23514'; end if;
  for entry in select * from jsonb_each(x-array['slots','is_test','synthetic']) loop
    if jsonb_typeof(entry.value) is distinct from 'string'
      or (entry.value#>>'{}') ~ '^(sk-|sb_secret_|eyJ[^.]*\.[^.]*\.[^.]*$)' or (entry.value#>>'{}') !~
      (case when entry.key like '%digest' then '^[0-9a-f]{64}$' when entry.key like '%commit' then '^[0-9a-f]{40}$'
      else '^[A-Za-z0-9][A-Za-z0-9_.:-]{0,199}$' end) then
      raise exception 'invalid job identity/pin' using errcode='23514'; end if;
  end loop;
  if ((x->>'is_test')::boolean)<>(x->>'namespace' like 'test-%')
    or ((x->>'synthetic')::boolean and not (x->>'is_test')::boolean) then
    raise exception 'test/synthetic labels required' using errcode='23514'; end if;
  for s in select * from jsonb_array_elements(x->'slots') loop
    if jsonb_typeof(s) is distinct from 'object' or (select count(*) from jsonb_object_keys(s))<>5
      or s-array['role','arm','repetition','effect_type','payload_digest']<>'{}'::jsonb
      or jsonb_typeof(s->'role') is distinct from 'string'
      or jsonb_typeof(s->'effect_type') is distinct from 'string'
      or coalesce(s->>'role','') not in('worker','grader','publication','checkpoint')
      or coalesce(s->>'effect_type','') not in('native-call','keyed-file')
      or s->>'arm' ~ '^(sk-|sb_secret_|eyJ[^.]*\.[^.]*\.[^.]*$)'
      or jsonb_typeof(s->'arm') is distinct from 'string' or coalesce(s->>'arm','') !~ '^[A-Za-z0-9][A-Za-z0-9_.:-]{0,199}$'
      or jsonb_typeof(s->'repetition') is distinct from 'number' or coalesce(s->>'repetition','') !~ '^[1-9][0-9]*$'
      or (s->>'repetition')::numeric>9223372036854775807
      or jsonb_typeof(s->'payload_digest') is distinct from 'string' or coalesce(s->>'payload_digest','') !~ '^[0-9a-f]{64}$'
      then raise exception 'invalid frozen execution slot' using errcode='23514'; end if;
  end loop;
  if exists(select 1 from jsonb_array_elements(x->'slots') q group by q->>'role',q->>'arm',q->>'repetition' having count(*)>1) then
    raise exception 'duplicate frozen execution slot' using errcode='23514'; end if;
  return x;
end; $$;

create function ams_recovery_private.validate_observation(p_text text,p_digest text,p_key text,p_payload text) returns jsonb
language plpgsql security definer set search_path='' as $$
declare x jsonb:=p_text::jsonb;
begin
  if p_digest is distinct from encode(sha256(convert_to(p_text,'UTF8')),'hex')
    or jsonb_typeof(x) is distinct from 'object' or (select count(*) from jsonb_object_keys(x))<>6
    or x-array['effect_key','payload_digest','outcome','object_id','artifact_digest','proof_digest']<>'{}'::jsonb
    or p_text is distinct from public.ams_canonical_jsonb(x)
    or jsonb_typeof(x->'effect_key') is distinct from 'string'
    or jsonb_typeof(x->'payload_digest') is distinct from 'string'
    or jsonb_typeof(x->'proof_digest') is distinct from 'string'
    or x->>'object_id' ~ '^(sk-|sb_secret_|eyJ[^.]*\.[^.]*\.[^.]*$)'
    or x->>'effect_key' is distinct from p_key or x->>'payload_digest' is distinct from p_payload
    or jsonb_typeof(x->'outcome') is distinct from 'string'
    or coalesce(x->>'outcome','') not in('matched','absent','unavailable','conflict')
    or coalesce(x->>'proof_digest','') !~ '^[0-9a-f]{64}$'
    or (jsonb_typeof(x->'object_id') is distinct from 'null' and (jsonb_typeof(x->'object_id') is distinct from 'string' or x->>'object_id' !~ '^[A-Za-z0-9][A-Za-z0-9_.:-]{0,199}$'))
    or (jsonb_typeof(x->'artifact_digest') is distinct from 'null' and (jsonb_typeof(x->'artifact_digest') is distinct from 'string' or x->>'artifact_digest' !~ '^[0-9a-f]{64}$'))
    or (x->>'outcome'='matched' and (jsonb_typeof(x->'object_id') is distinct from 'string' or jsonb_typeof(x->'artifact_digest') is distinct from 'string'))
    then raise exception 'unsafe effect observation' using errcode='23514'; end if;
  return x;
end; $$;

create function ams_recovery_private.snapshot(p_namespace text) returns jsonb
language plpgsql security definer set search_path='' as $$
declare s jsonb; raw text;
begin
  perform ams_recovery_private.require_service();
  if coalesce(p_namespace,'') !~ '^[a-z][a-z0-9_-]{2,79}$' then raise exception 'invalid namespace' using errcode='23514'; end if;
  perform pg_advisory_xact_lock(710006,hashtext(p_namespace));
  select jsonb_build_object('namespace',p_namespace,
    'lineage',coalesce((select jsonb_agg(jsonb_build_object('ordinal',l.ordinal,'record_text',l.record_text,
      'record_digest',l.record_digest,'previous_digest',l.previous_digest,'format_version',l.format_version) order by l.ordinal)
      from public.rsi_lineage l where namespace=p_namespace),'[]'::jsonb),
    'jobs',coalesce((select jsonb_agg(jsonb_build_object('job_text',j.job_text,'job_digest',j.job_digest,
      'chain_id',j.chain_id,'attempt',j.attempt,'version',j.version,'fence',j.fence,
      'terminal_state',j.terminal_state,'evidence_digest',j.evidence_digest) order by j.job_id)
      from public.rsi_jobs j where namespace=p_namespace),'[]'::jsonb),
    'effects',coalesce((select jsonb_agg(jsonb_build_object('effect_key',e.effect_key,'job_id',e.job_id,
      'key_text',e.key_text,'payload_digest',e.payload_digest,'intent_fence',e.intent_fence,'version',e.version,
      'state',e.state,'observation_text',e.observation_text,'receipt_digest',e.receipt_digest) order by e.effect_key)
      from public.rsi_effects e where namespace=p_namespace),'[]'::jsonb),
    'externals',coalesce((select jsonb_agg(ref order by ref->>'table',(ref->>'id')::bigint) from (
      select distinct jsonb_build_object('table','rsi_runs','id',r.id,
        'digest',encode(sha256(convert_to(to_jsonb(r)::text,'UTF8')),'hex')) as ref
      from public.rsi_lineage l join public.rsi_runs r on r.id=(l.attributes->>'rsi_run_id')::bigint
      where l.namespace=p_namespace and l.kind='run' and not l.synthetic
      union
      select distinct jsonb_build_object('table','rsi_results','id',r.id,
        'digest',encode(sha256(convert_to(to_jsonb(r)::text,'UTF8')),'hex')) as ref
      from public.rsi_lineage l join public.rsi_results r on r.id=(l.attributes->>'rsi_result_id')::bigint
      where l.namespace=p_namespace and l.kind='result' and not l.synthetic
      ) refs),'[]'::jsonb)) into s;
  raw:=s::text;
  return jsonb_build_object('snapshot_text',raw,'head',encode(sha256(convert_to(raw,'UTF8')),'hex'));
end; $$;

create function ams_recovery_private.operate(p_action text,p_request jsonb) returns jsonb
language plpgsql security definer set search_path='' as $$
declare ns text; jid text; j public.rsi_jobs; e public.rsi_effects; x jsonb; slot jsonb; material jsonb; required text[];
  c public.rsi_lineage; k public.rsi_lineage; seen jsonb; candidate_closed boolean; field text;
begin
  perform ams_recovery_private.require_service();
  if coalesce(jsonb_typeof(p_request),'') is distinct from 'object' then raise exception 'invalid recovery request' using errcode='23514'; end if;
  required:=case p_action
    when 'create' then array['job_text','job_digest'] when 'get' then array['namespace','job_id']
    when 'snapshot' then array['namespace']
    when 'gates' then array['namespace','job_id','expected_version','approved','capacity','observed_at','capacity_digest','stopped']
    when 'claim' then array['namespace','job_id','expected_version','claimant','lease_seconds']
    when 'renew' then array['namespace','job_id','expected_version','claimant','fence','lease_seconds']
    when 'release' then array['namespace','job_id','expected_version','claimant','fence']
    when 'begin' then array['namespace','job_id','expected_version','claimant','fence','slot_index','key_text','effect_key']
    when 'observe' then array['namespace','job_id','expected_version','claimant','fence','effect_key','observation_text','observation_digest']
    when 'retry_absent' then array['namespace','job_id','expected_version','claimant','fence','effect_key']
    when 'finish' then array['namespace','job_id','expected_version','claimant','fence','state','evidence_digest']
    when 'restore' then array['manifest_text','manifest_digest','expected_head','expected_manifest_digest','reader_digest','schema_digest'] else null end;
  if required is null or not(p_request ?& required) or p_request-required<>'{}'::jsonb then
    raise exception 'recovery request fields are allowlisted' using errcode='23514'; end if;
  -- All other declared request fields are strings. Do not turn JSON numbers
  -- into identities, pins, claimant labels or receipt text with ->> coercion.
  foreach field in array required loop
    continue when field=any(array['expected_version','fence','lease_seconds','slot_index','approved','stopped','expected_head']);
    if jsonb_typeof(p_request->field) is distinct from 'string' then
      raise exception 'recovery request string type differs' using errcode='23514';end if;
  end loop;
  if p_action='restore' then return ams_recovery_private.restore(p_request); end if;
  if p_action='create' then
    if p_request-array['job_text','job_digest']<>'{}'::jsonb then raise exception 'unsafe create request' using errcode='23514'; end if;
    x:=ams_recovery_private.validate_job(p_request->>'job_text',p_request->>'job_digest');
    ns:=x->>'namespace';jid:=x->>'job_id';
  else ns:=p_request->>'namespace';jid:=p_request->>'job_id'; end if;
  if coalesce(ns,'') !~ '^[a-z][a-z0-9_-]{2,79}$' then raise exception 'invalid namespace' using errcode='23514'; end if;
  perform pg_advisory_xact_lock(710006,hashtext(ns));
  if p_action='snapshot' then
    if p_request-array['namespace']<>'{}'::jsonb then raise exception 'unsafe snapshot request' using errcode='23514'; end if;
    return ams_recovery_private.snapshot(ns);
  end if;
  if coalesce(jid,'') !~ '^[A-Za-z0-9][A-Za-z0-9_.:-]{0,199}$' then raise exception 'invalid job identity' using errcode='23514'; end if;
  select * into j from public.rsi_jobs where namespace=ns and job_id=jid for update;
  if p_action='get' then
    if p_request-array['namespace','job_id']<>'{}'::jsonb then raise exception 'unsafe read request' using errcode='23514'; end if;
    return jsonb_build_object('job',case when j.job_id is null then null else to_jsonb(j) end);
  end if;
  if p_action='create' then
    if j.job_id is not null then
      if j.job_text is distinct from p_request->>'job_text' then raise exception 'job identity changed' using errcode='PT409'; end if;
      return jsonb_build_object('job',to_jsonb(j));
    end if;
    select * into c from public.rsi_lineage where namespace=ns and record_id=x->>'case_id' and kind='case';
    select * into k from public.rsi_lineage where namespace=ns and record_id=x->>'candidate_id' and kind='candidate';
    if c.record_id is null or k.record_id is null or c.chain_id<>k.chain_id
      or k.chain_id ~ '^(sk-|sb_secret_|eyJ[^.]*\.[^.]*\.[^.]*$)'
      or c.is_test<>(x->>'is_test')::boolean or c.synthetic<>(x->>'synthetic')::boolean
      or k.is_test<>c.is_test or k.synthetic<>c.synthetic or c.record_text::jsonb->>'artifact_digest'<>x->>'case_digest'
      or k.attributes->>'skills_commit'<>x->>'skills_commit' then
      raise exception 'job lineage/source/labels differ' using errcode='23514'; end if;
    if exists(select 1 from public.rsi_jobs where namespace=ns and chain_id=k.chain_id and candidate_id=k.record_id
      and case_digest=x->>'case_digest' and release_digest=x->>'release_digest') then
      raise exception 'duplicate logical job alias' using errcode='PT409'; end if;
    insert into public.rsi_jobs(namespace,job_id,job_text,job_digest,chain_id,candidate_id,case_digest,release_digest,attempt)
      values(ns,jid,p_request->>'job_text',p_request->>'job_digest',k.chain_id,k.record_id,x->>'case_digest',x->>'release_digest',
             (k.attributes->>'attempt')::integer) returning * into j;
    return jsonb_build_object('job',to_jsonb(j));
  end if;
  if j.job_id is null then raise exception 'missing job' using errcode='23514'; end if;
  if jsonb_typeof(p_request->'expected_version') is distinct from 'number' or coalesce(p_request->>'expected_version','') !~ '^[1-9][0-9]*$'
    or (p_request->>'expected_version')::numeric<>j.version then raise exception 'stale job version' using errcode='PT409'; end if;
  if p_action='gates' then
    if p_request-array['namespace','job_id','expected_version','approved','capacity','observed_at','capacity_digest','stopped']<>'{}'::jsonb
      or jsonb_typeof(p_request->'approved') is distinct from 'boolean' or jsonb_typeof(p_request->'stopped') is distinct from 'boolean'
      or jsonb_typeof(p_request->'observed_at') is distinct from 'string'
      or coalesce(p_request->>'capacity','') not in('available','unknown','exhausted')
      or coalesce(p_request->>'capacity_digest','') !~ '^[0-9a-f]{64}$' then raise exception 'unsafe release gates' using errcode='23514'; end if;
    if j.terminal_state is not null then raise exception 'terminal job cannot restart' using errcode='PT409'; end if;
    update public.rsi_jobs set approved=(p_request->>'approved')::boolean,capacity=p_request->>'capacity',
      capacity_observed_at=(p_request->>'observed_at')::timestamptz,capacity_digest=p_request->>'capacity_digest',
      stop_requested=(p_request->>'stopped')::boolean,version=version+1,
      terminal_state=case when (p_request->>'stopped')::boolean then 'stopped' else null end,
      state=case when (p_request->>'stopped')::boolean then 'stopped' when not (p_request->>'approved')::boolean
        or p_request->>'capacity'<>'available' then 'blocked' when state='blocked' then 'ready' else state end,
      block_reason=case when (p_request->>'stopped')::boolean then 'stop-requested'
        when not (p_request->>'approved')::boolean then 'approval-required'
        when p_request->>'capacity'<>'available' then 'capacity-held' else null end
      where namespace=ns and job_id=jid returning * into j;
    return jsonb_build_object('job',to_jsonb(j));
  end if;
  if p_action='claim' then
    if p_request-array['namespace','job_id','expected_version','claimant','lease_seconds']<>'{}'::jsonb
      or coalesce(p_request->>'claimant','') !~ '^[A-Za-z0-9][A-Za-z0-9_.:-]{0,199}$'
      or jsonb_typeof(p_request->'lease_seconds') is distinct from 'number' or coalesce(p_request->>'lease_seconds','') !~ '^[1-9][0-9]*$'
      or (p_request->>'lease_seconds')::numeric not between 1 and 300 then raise exception 'invalid lease' using errcode='23514'; end if;
    if j.lease_until>clock_timestamp()
      or j.terminal_state='completed' or (j.terminal_state is not null and not exists(select 1 from public.rsi_effects
        where namespace=ns and job_id=jid and state<>'completed')) then
      raise exception 'job claimed or terminal' using errcode='PT409'; end if;
    update public.rsi_jobs set version=version+1,fence=fence+1,claimant=p_request->>'claimant',
      lease_until=clock_timestamp()+make_interval(secs=>(p_request->>'lease_seconds')::integer),
      state=coalesce(terminal_state,case when exists(select 1 from public.rsi_effects where namespace=ns and job_id=jid
        and state<>'completed') then 'effect_uncertain' when not approved or capacity<>'available'
        or capacity_observed_at is null or capacity_observed_at<clock_timestamp()-interval '5 minutes'
        then 'blocked' else 'running' end)
      where namespace=ns and job_id=jid returning * into j;
    return jsonb_build_object('job',to_jsonb(j));
  end if;
  if jsonb_typeof(p_request->'fence') is distinct from 'number'
    or coalesce(p_request->>'fence','') !~ '^[1-9][0-9]*$'
    or jsonb_typeof(p_request->'claimant') is distinct from 'string' then
    raise exception 'invalid fenced claim' using errcode='23514'; end if;
  if p_request->>'claimant' is distinct from j.claimant or (p_request->>'fence')::numeric is distinct from j.fence::numeric
    or j.lease_until is null or j.lease_until<=clock_timestamp() then
    raise exception 'stale fence/lease' using errcode='PT409'; end if;
  if p_action='renew' then
    if jsonb_typeof(p_request->'lease_seconds') is distinct from 'number'
      or coalesce(p_request->>'lease_seconds','') !~ '^[1-9][0-9]*$' or
      (p_request->>'lease_seconds')::numeric not between 1 and 300 then raise exception 'invalid lease' using errcode='23514';end if;
    update public.rsi_jobs set version=version+1,lease_until=clock_timestamp()+make_interval(secs=>(p_request->>'lease_seconds')::integer)
      where namespace=ns and job_id=jid returning * into j;
    return jsonb_build_object('job',to_jsonb(j));
  end if;
  if p_action='release' then
    update public.rsi_jobs set version=version+1,claimant=null,lease_until=null,
      state=coalesce(terminal_state,case when exists(select 1 from public.rsi_effects where namespace=ns and job_id=jid
        and state<>'completed') then 'effect_uncertain' else 'ready' end)
      where namespace=ns and job_id=jid returning * into j;
    return jsonb_build_object('job',to_jsonb(j));
  end if;
  if p_action='finish' then
    if p_request-array['namespace','job_id','expected_version','claimant','fence','state','evidence_digest']<>'{}'::jsonb
      or coalesce(p_request->>'state','') not in('awaiting_evidence','completed','failed','stopped','blocked')
      or coalesce(p_request->>'evidence_digest','') !~ '^[0-9a-f]{64}$' then raise exception 'invalid finish evidence' using errcode='23514'; end if;
    if j.terminal_state is not null then raise exception 'terminal outcome immutable' using errcode='PT409'; end if;
    if p_request->>'state'='completed' and ((select count(*) from public.rsi_effects where namespace=ns and job_id=jid)
       <>jsonb_array_length(j.job_text::jsonb->'slots') or exists(select 1 from public.rsi_effects where namespace=ns and job_id=jid and state<>'completed')) then
      raise exception 'job has missing/unresolved execution slots' using errcode='23514'; end if;
    update public.rsi_jobs set version=version+1,state=p_request->>'state',evidence_digest=p_request->>'evidence_digest',
      terminal_state=case when p_request->>'state' in('completed','failed','stopped') then p_request->>'state' else null end
      where namespace=ns and job_id=jid returning * into j;
    return jsonb_build_object('job',to_jsonb(j));
  end if;
  -- Refuse an invalid persisted prototype contract as well as new intake.
  perform ams_recovery_private.validate_job(j.job_text,j.job_digest);
  if p_action='begin' then
    if p_request-array['namespace','job_id','expected_version','claimant','fence','slot_index','key_text','effect_key']<>'{}'::jsonb
      or jsonb_typeof(p_request->'slot_index') is distinct from 'number' or coalesce(p_request->>'slot_index','') !~ '^(0|[1-9][0-9]*)$' then
      raise exception 'unsafe slot request' using errcode='23514'; end if;
    slot:=j.job_text::jsonb->'slots'->(p_request->>'slot_index')::integer;
    if slot is null then raise exception 'unknown frozen slot' using errcode='23514'; end if;
    material:=jsonb_build_object('protocol',1,'chain_id',j.chain_id,'attempt',j.attempt,'case_digest',j.case_digest,
      'role',slot->>'role','arm',slot->>'arm','repetition',slot->'repetition');
    if p_request->>'key_text' is distinct from public.ams_canonical_jsonb(material) or p_request->>'effect_key' is distinct from
       encode(sha256(convert_to(p_request->>'key_text','UTF8')),'hex') then raise exception 'execution slot identity changed' using errcode='23514'; end if;
    select * into e from public.rsi_effects where namespace=ns and effect_key=p_request->>'effect_key';
    if e.effect_key is not null then
      if e.job_id<>jid or e.payload_digest<>slot->>'payload_digest' or e.key_text<>p_request->>'key_text' then
        raise exception 'effect identity/owner conflict' using errcode='PT409'; end if;
      return jsonb_build_object('job',to_jsonb(j),'effect',to_jsonb(e),'execute',false,'reconcile',e.state<>'completed');
    end if;
  elsif p_action in('observe','retry_absent') then
    select * into e from public.rsi_effects where namespace=ns and effect_key=p_request->>'effect_key' and job_id=jid for update;
    if e.effect_key is null then raise exception 'missing effect intent' using errcode='23514'; end if;
    select s into slot from jsonb_array_elements(j.job_text::jsonb->'slots') s where
      jsonb_build_object('protocol',1,'chain_id',j.chain_id,'attempt',j.attempt,'case_digest',j.case_digest,
        'role',s->>'role','arm',s->>'arm','repetition',s->'repetition')=e.key_text::jsonb;
    if slot is null then raise exception 'effect outside frozen slots' using errcode='23514'; end if;
  else raise exception 'unknown recovery operation' using errcode='23514'; end if;
  if p_action='observe' then
    if p_request-array['namespace','job_id','expected_version','claimant','fence','effect_key','observation_text','observation_digest']<>'{}'::jsonb then
      raise exception 'unsafe observation request' using errcode='23514'; end if;
    seen:=ams_recovery_private.validate_observation(p_request->>'observation_text',p_request->>'observation_digest',e.effect_key,e.payload_digest);
    if e.state='completed' then
      if e.observation_text is distinct from p_request->>'observation_text' then raise exception 'effect receipt changed' using errcode='PT409'; end if;
      return jsonb_build_object('job',to_jsonb(j),'effect',to_jsonb(e),'execute',false);
    end if;
    update public.rsi_effects set version=version+1,observation_text=p_request->>'observation_text',
      receipt_digest=case when seen->>'outcome'='matched' then p_request->>'observation_digest' else null end,
      state=case when seen->>'outcome'='matched' then 'completed' when seen->>'outcome'='absent' then 'absent' else 'uncertain' end
      where namespace=ns and effect_key=e.effect_key returning * into e;
    update public.rsi_jobs set version=version+1,state=coalesce(terminal_state,case when e.state='completed' then 'running' else 'effect_uncertain' end)
      where namespace=ns and job_id=jid returning * into j;
    return jsonb_build_object('job',to_jsonb(j),'effect',to_jsonb(e),'execute',false);
  end if;
  if j.terminal_state is not null or j.stop_requested or not j.approved or j.capacity<>'available'
    or j.capacity_observed_at is null or j.capacity_observed_at<clock_timestamp()-interval '5 minutes'
    or j.capacity_observed_at>clock_timestamp()+interval '5 seconds' then
    raise exception 'stop/approval/capacity gate held' using errcode='PT409'; end if;
  select exists(select 1 from public.rsi_lineage d join public.rsi_lineage comparison
    on comparison.namespace=d.namespace and comparison.record_id=d.parents->>'comparison'
    where d.namespace=ns and d.kind='disposition' and d.attributes->>'decision'='rejected'
      and comparison.parents->>'candidate'=j.candidate_id) into candidate_closed;
  if slot->>'role' in('worker','grader') and candidate_closed then
    raise exception 'assessed rejected candidate is closed; preserve attempts' using errcode='PT409'; end if;
  if p_action='retry_absent' then
    if p_request-array['namespace','job_id','expected_version','claimant','fence','effect_key']<>'{}'::jsonb
      or slot->>'effect_type' is distinct from 'keyed-file' or e.state is distinct from 'absent'
      or e.observation_text::jsonb->>'outcome' is distinct from 'absent' then
      raise exception 'consumed native/uncertain slot cannot repeat' using errcode='PT409'; end if;
    update public.rsi_effects set version=version+1,state='pending',observation_text=null where namespace=ns and effect_key=e.effect_key returning * into e;
  else
    insert into public.rsi_effects(namespace,effect_key,job_id,key_text,payload_digest,intent_fence)
      values(ns,p_request->>'effect_key',jid,p_request->>'key_text',slot->>'payload_digest',j.fence) returning * into e;
  end if;
  update public.rsi_jobs set version=version+1,state='effect_uncertain' where namespace=ns and job_id=jid returning * into j;
  return jsonb_build_object('job',to_jsonb(j),'effect',to_jsonb(e),'execute',true,'reconcile',false);
end; $$;

create function ams_recovery_private.restore(p_request jsonb) returns jsonb
language plpgsql security definer set search_path='' as $$
declare m jsonb; s jsonb; before jsonb; after jsonb; current_data jsonb; ns text; category text;
  row jsonb; prior jsonb; listed jsonb; jobdef jsonb; material jsonb; slot jsonb; observed jsonb;
  j public.rsi_jobs; existing public.rsi_effects; record_id text; nhead text; batch jsonb; count_records integer:=0;
  expected_keys text[]; actual_hash text; field text; string_fields text[]; integer_fields text[]; nullable_fields text[];
begin
  perform ams_recovery_private.require_service();
  if jsonb_typeof(p_request->'manifest_text') is distinct from 'string'
    or coalesce(p_request->>'manifest_digest','') !~ '^[0-9a-f]{64}$'
    or coalesce(p_request->>'expected_manifest_digest','') !~ '^[0-9a-f]{64}$'
    or not (jsonb_typeof(p_request->'expected_head')='null'
      or (jsonb_typeof(p_request->'expected_head')='string' and p_request->>'expected_head' ~ '^[0-9a-f]{64}$')) then
    raise exception 'invalid checkpoint pins/head' using errcode='23514'; end if;
  if p_request->>'manifest_digest' is distinct from p_request->>'expected_manifest_digest'
    or p_request->>'manifest_digest' is distinct from encode(sha256(convert_to(p_request->>'manifest_text','UTF8')),'hex') then
    raise exception 'checkpoint differs from pinned manifest' using errcode='PT409'; end if;
  m:=(p_request->>'manifest_text')::jsonb;
  expected_keys:=array['format_version','reader_version','reader_digest','schema_digest','projection','namespace',
    'complete','export_id','previous_export','snapshot_text','source_head','counts','records'];
  if p_request->>'manifest_text' is distinct from public.ams_canonical_jsonb(m)
    or coalesce(jsonb_typeof(m),'') is distinct from 'object' or not(m ?& expected_keys) or m-expected_keys<>'{}'::jsonb
    or m->>'format_version' is distinct from '1' or m->>'reader_version' is distinct from '1' or m->'complete'<>'true'::jsonb
    or m->>'projection' is distinct from 'safe-lineage-job-effects-v1'
    or m->>'reader_digest' is distinct from p_request->>'reader_digest'
    or m->>'schema_digest' is distinct from p_request->>'schema_digest'
    or coalesce(m->>'reader_digest','') !~ '^[0-9a-f]{64}$' or coalesce(m->>'schema_digest','') !~ '^[0-9a-f]{64}$'
    or coalesce(m->>'export_id','') !~ '^[A-Za-z0-9][A-Za-z0-9_.:-]{0,199}$'
    or (jsonb_typeof(m->'previous_export') is distinct from 'null' and coalesce(m->>'previous_export','') !~ '^[0-9a-f]{64}$')
    or m->>'source_head' is distinct from encode(sha256(convert_to(m->>'snapshot_text','UTF8')),'hex') then
    raise exception 'unsupported/unsafe checkpoint manifest' using errcode='23514'; end if;
  s:=(m->>'snapshot_text')::jsonb;ns:=m->>'namespace';
  if coalesce(ns,'') !~ '^[a-z][a-z0-9_-]{2,79}$' or s->>'namespace' is distinct from ns
    or coalesce(jsonb_typeof(s),'') is distinct from 'object' or not(s ?& array['namespace','lineage','jobs','effects','externals'])
    or s-array['namespace','lineage','jobs','effects','externals']<>'{}'::jsonb
    or coalesce(jsonb_typeof(m->'records'),'') is distinct from 'array' or coalesce(jsonb_typeof(m->'counts'),'') is distinct from 'object'
    or (m->'counts')-array['lineage','jobs','effects','externals']<>'{}'::jsonb then
    raise exception 'incomplete checkpoint projection' using errcode='23514'; end if;
  foreach category in array array['lineage','jobs','effects','externals'] loop
    if jsonb_typeof(m->'counts'->category) is distinct from 'number'
      or coalesce(m->'counts'->>category,'') !~ '^(0|[1-9][0-9]*)$'
      or coalesce(jsonb_typeof(s->category),'') is distinct from 'array'
      or m->'counts'->category is distinct from to_jsonb(jsonb_array_length(s->category)) then
      raise exception 'checkpoint counts differ' using errcode='23514'; end if;
    for row in select * from jsonb_array_elements(s->category) loop
      if category='lineage' then expected_keys:=array['ordinal','record_text','record_digest','previous_digest','format_version'];
        record_id:=(row->>'record_text')::jsonb->>'record_id';
      elsif category='jobs' then expected_keys:=array['job_text','job_digest','chain_id','attempt','version','fence','terminal_state','evidence_digest'];
        record_id:=(row->>'job_text')::jsonb->>'job_id';
      elsif category='effects' then expected_keys:=array['effect_key','job_id','key_text','payload_digest','intent_fence','version','state','observation_text','receipt_digest'];
        record_id:=row->>'effect_key';
      else expected_keys:=array['table','id','digest'];record_id:=(row->>'table')||':'||(row->>'id');end if;
      if coalesce(jsonb_typeof(row),'') is distinct from 'object' or not(row ?& expected_keys) or row-expected_keys<>'{}'::jsonb
        or (select count(*) from jsonb_array_elements(m->'records') r where r->>'kind'=category and r->>'id'=record_id)<>1 then
        raise exception 'unsafe/duplicate checkpoint record' using errcode='23514'; end if;
      case category
        when 'lineage' then string_fields:=array['record_text','record_digest'];integer_fields:=array['ordinal','format_version'];nullable_fields:=array['previous_digest'];
        when 'jobs' then string_fields:=array['job_text','job_digest','chain_id'];integer_fields:=array['attempt','version','fence'];nullable_fields:=array['terminal_state','evidence_digest'];
        when 'effects' then string_fields:=array['effect_key','job_id','key_text','payload_digest','state'];integer_fields:=array['intent_fence','version'];nullable_fields:=array['observation_text','receipt_digest'];
        when 'externals' then string_fields:=array['table','digest'];integer_fields:=array['id'];nullable_fields:=array[]::text[];
      end case;
      foreach field in array string_fields loop
        if jsonb_typeof(row->field) is distinct from 'string' then raise exception 'checkpoint string type differs' using errcode='23514';end if;
      end loop;
      foreach field in array integer_fields loop
        if jsonb_typeof(row->field) is distinct from 'number' or coalesce(row->>field,'') !~ '^(0|[1-9][0-9]*)$'
          or (row->>field)::numeric>9223372036854775807 or (field not in('attempt','fence') and (row->>field)::numeric<1) then
          raise exception 'checkpoint integer type differs' using errcode='23514';end if;
      end loop;
      foreach field in array nullable_fields loop
        if jsonb_typeof(row->field) not in('null','string') then raise exception 'checkpoint nullable string type differs' using errcode='23514';end if;
      end loop;
      select r into listed from jsonb_array_elements(m->'records') r where r->>'kind'=category and r->>'id'=record_id;
      if not(listed ?& array['kind','id','text','digest']) or listed-array['kind','id','text','digest']<>'{}'::jsonb
        or listed->>'text' is distinct from public.ams_canonical_jsonb(row) or listed->>'digest' is distinct from
          encode(sha256(convert_to(listed->>'text','UTF8')),'hex') then
        raise exception 'checkpoint record digest differs' using errcode='23514'; end if;
      count_records:=count_records+1;
    end loop;
  end loop;
  if jsonb_array_length(m->'records')<>count_records then raise exception 'partial checkpoint record inventory' using errcode='23514'; end if;
  perform pg_advisory_xact_lock(710006,hashtext(ns));
  before:=ams_recovery_private.snapshot(ns);current_data:=(before->>'snapshot_text')::jsonb;
  if (jsonb_typeof(p_request->'expected_head')='null' and exists(select 1 from jsonb_each(current_data-array['namespace']) a
      where jsonb_array_length(a.value)>0)) or
    (jsonb_typeof(p_request->'expected_head') is distinct from 'null' and p_request->>'expected_head' is distinct from before->>'head') then
    raise exception 'stale destination checkpoint head' using errcode='PT409'; end if;
  if before->>'head'=m->>'source_head' then return before||jsonb_build_object('restored',false);end if;
  -- A live destination is authoritative. Only a byte-matching subset may be
  -- appended; mutable old states are never overwritten from an old snapshot.
  foreach category in array array['lineage','jobs','effects','externals'] loop
    for prior in select * from jsonb_array_elements(current_data->category) loop
      if not exists(select 1 from jsonb_array_elements(s->category) candidate where candidate=prior) then
        raise exception 'divergent destination record' using errcode='PT409';end if;
    end loop;
  end loop;
  -- Hash-only external references disclose no raw packets/rows. Lock matching
  -- canonical parents through commit; absent/redacted evidence is not invented.
  for row in select * from jsonb_array_elements(s->'externals') loop
    if jsonb_typeof(row->'table') is distinct from 'string' or jsonb_typeof(row->'id') is distinct from 'number'
      or jsonb_typeof(row->'digest') is distinct from 'string' or coalesce(row->>'id','') !~ '^[1-9][0-9]*$' or coalesce(row->>'digest','') !~ '^[0-9a-f]{64}$' then
      raise exception 'invalid external parent identity' using errcode='23514';end if;
    if row->>'table'='rsi_runs' then
      perform 1 from public.rsi_runs where id=(row->>'id')::bigint for share;
      select encode(sha256(convert_to(to_jsonb(r)::text,'UTF8')),'hex') into actual_hash from public.rsi_runs r where id=(row->>'id')::bigint;
    elsif row->>'table'='rsi_results' then
      perform 1 from public.rsi_results where id=(row->>'id')::bigint for share;
      select encode(sha256(convert_to(to_jsonb(r)::text,'UTF8')),'hex') into actual_hash from public.rsi_results r where id=(row->>'id')::bigint;
    else raise exception 'unsupported canonical parent table' using errcode='23514';end if;
    if actual_hash is distinct from row->>'digest' then raise exception 'missing/divergent canonical parent' using errcode='PT409';end if;
  end loop;
  select record_digest into nhead from public.rsi_lineage where namespace=ns order by ordinal desc limit 1;
  select coalesce(jsonb_agg(jsonb_build_object('record_text',r->>'record_text','record_digest',r->>'record_digest')
    order by (r->>'ordinal')::bigint),'[]'::jsonb) into batch from jsonb_array_elements(s->'lineage') r;
  if jsonb_array_length(batch)>0 then perform public.ams_append_lineage(ns,nhead,batch);end if;
  for row in select * from jsonb_array_elements(s->'jobs') loop
    jobdef:=ams_recovery_private.validate_job(row->>'job_text',row->>'job_digest');
    if jobdef->>'namespace'<>ns or coalesce(row->>'attempt','') !~ '^[0-3]$'
      or coalesce(row->>'version','') !~ '^[1-9][0-9]*$' or coalesce(row->>'fence','') !~ '^(0|[1-9][0-9]*)$'
      or jsonb_typeof(row->'attempt') is distinct from 'number'
      or jsonb_typeof(row->'version') is distinct from 'number'
      or jsonb_typeof(row->'fence') is distinct from 'number'
      or jsonb_typeof(row->'chain_id') is distinct from 'string'
      or (row->>'version')::bigint<=(row->>'fence')::bigint
      or (jsonb_typeof(row->'terminal_state') is distinct from 'null' and row->>'terminal_state' not in('completed','failed','stopped'))
      or (jsonb_typeof(row->'evidence_digest') is distinct from 'null' and coalesce(row->>'evidence_digest','') !~ '^[0-9a-f]{64}$') then
      raise exception 'invalid safe job high-water projection' using errcode='23514';end if;
    select * into j from public.rsi_jobs where namespace=ns and job_id=jobdef->>'job_id';
    if j.job_id is not null then continue;end if;
    perform ams_recovery_private.operate('create',jsonb_build_object('job_text',row->>'job_text','job_digest',row->>'job_digest'));
    select * into j from public.rsi_jobs where namespace=ns and job_id=jobdef->>'job_id';
    if row->>'chain_id' is distinct from j.chain_id or (row->>'attempt')::integer<>j.attempt then
      raise exception 'restored job lineage identity differs' using errcode='23514';end if;
    update public.rsi_jobs set version=(row->>'version')::bigint,fence=(row->>'fence')::bigint,
      terminal_state=row->>'terminal_state',evidence_digest=row->>'evidence_digest',
      state=coalesce(row->>'terminal_state','blocked'),approved=false,capacity='unknown',
      capacity_observed_at=null,capacity_digest=null,claimant=null,lease_until=null,
      stop_requested=coalesce(row->>'terminal_state'='stopped',false),block_reason='restore-approval-required'
      where namespace=ns and job_id=jobdef->>'job_id';
  end loop;
  for row in select * from jsonb_array_elements(s->'effects') loop
    if coalesce(row->>'effect_key','') !~ '^[0-9a-f]{64}$' or row->>'effect_key' is distinct from
      encode(sha256(convert_to(row->>'key_text','UTF8')),'hex') or coalesce(row->>'payload_digest','') !~ '^[0-9a-f]{64}$'
      or coalesce(row->>'intent_fence','') !~ '^[1-9][0-9]*$' or coalesce(row->>'version','') !~ '^[1-9][0-9]*$'
      or jsonb_typeof(row->'effect_key') is distinct from 'string'
      or jsonb_typeof(row->'job_id') is distinct from 'string'
      or jsonb_typeof(row->'key_text') is distinct from 'string'
      or jsonb_typeof(row->'payload_digest') is distinct from 'string'
      or jsonb_typeof(row->'intent_fence') is distinct from 'number'
      or jsonb_typeof(row->'version') is distinct from 'number'
      or coalesce(row->>'state','') not in('pending','uncertain','absent','completed') then
      raise exception 'invalid effect projection' using errcode='23514';end if;
    select * into j from public.rsi_jobs where namespace=ns and job_id=row->>'job_id';
    if j.job_id is null or (row->>'intent_fence')::bigint>j.fence then raise exception 'missing effect parent/fence' using errcode='23514';end if;
    material:=(row->>'key_text')::jsonb;
    select entry into slot from jsonb_array_elements(j.job_text::jsonb->'slots') entry where
      jsonb_build_object('protocol',1,'chain_id',j.chain_id,'attempt',j.attempt,'case_digest',j.case_digest,
        'role',entry->>'role','arm',entry->>'arm','repetition',entry->'repetition')=material;
    if slot is null or slot->>'payload_digest' is distinct from row->>'payload_digest'
      or row->>'key_text' is distinct from public.ams_canonical_jsonb(jsonb_build_object(
        'protocol',1,'chain_id',j.chain_id,'attempt',j.attempt,'case_digest',j.case_digest,
        'role',slot->>'role','arm',slot->>'arm','repetition',slot->'repetition')) then
      raise exception 'restored effect outside frozen slots' using errcode='23514';end if;
    if jsonb_typeof(row->'observation_text')='null' then
      if row->>'state'<>'pending' or jsonb_typeof(row->'receipt_digest') is distinct from 'null' then
        raise exception 'missing effect observation' using errcode='23514';end if;
    else
      actual_hash:=encode(sha256(convert_to(row->>'observation_text','UTF8')),'hex');
      observed:=ams_recovery_private.validate_observation(row->>'observation_text',actual_hash,row->>'effect_key',row->>'payload_digest');
      if not coalesce(((row->>'state'='completed' and observed->>'outcome'='matched' and row->>'receipt_digest'=actual_hash)
        or (row->>'state'='absent' and observed->>'outcome'='absent' and jsonb_typeof(row->'receipt_digest')='null')
        or (row->>'state'='uncertain' and observed->>'outcome' in('unavailable','conflict') and jsonb_typeof(row->'receipt_digest')='null')),false) then
        raise exception 'effect state/receipt differs' using errcode='23514';end if;
    end if;
    select * into existing from public.rsi_effects where namespace=ns and effect_key=row->>'effect_key';
    if existing.effect_key is not null then continue;end if;
    insert into public.rsi_effects(namespace,effect_key,job_id,key_text,payload_digest,intent_fence,version,state,observation_text,receipt_digest)
      values(ns,row->>'effect_key',row->>'job_id',row->>'key_text',row->>'payload_digest',(row->>'intent_fence')::bigint,
        (row->>'version')::bigint,row->>'state',row->>'observation_text',row->>'receipt_digest');
  end loop;
  if exists(select 1 from public.rsi_jobs stored_job where namespace=ns and terminal_state='completed' and
    ((select count(*) from public.rsi_effects e where e.namespace=ns and e.job_id=stored_job.job_id)<>jsonb_array_length(stored_job.job_text::jsonb->'slots')
      or exists(select 1 from public.rsi_effects e where e.namespace=ns and e.job_id=stored_job.job_id and state<>'completed'))) then
    raise exception 'completed job has unresolved frozen slots' using errcode='23514';end if;
  after:=ams_recovery_private.snapshot(ns);
  if after->>'head' is distinct from m->>'source_head' then raise exception 'restored projection differs' using errcode='PT409';end if;
  return after||jsonb_build_object('restored',true);
end; $$;

create function public.ams_recovery(p_action text,p_request jsonb) returns jsonb
language sql security invoker set search_path='' as $$ select ams_recovery_private.operate(p_action,p_request); $$;
revoke all on all functions in schema ams_recovery_private from public,anon,authenticated;
grant execute on function ams_recovery_private.operate(text,jsonb) to service_role;
revoke all on function public.ams_recovery(text,jsonb) from public,anon,authenticated;
grant execute on function public.ams_recovery(text,jsonb) to service_role;
comment on table public.rsi_jobs is 'Private operational state. Source attempt identity comes from lineage; keys and gates cannot grant evaluator qualification.';
comment on table public.rsi_effects is 'Stable frozen-slot intents and readback receipts. Expired leases never imply permission to repeat native effects.';
commit;
