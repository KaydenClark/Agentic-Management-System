-- S-006 TK-003: RSI runs and their per-task results, read by the site.
-- Clients may only SELECT rows that are not test rows; the local Python
-- writer (src/ams/rsi_rows.py) writes with the service role key.
--
-- A run is one arm of one round at one system version: provider, model and
-- effort held fixed (ADR-002F), the skills commit pinned (ADR-002R) and the
-- grader taken from the accepted version (ADR-002K). A result is one trial of
-- one task in that run, with cost, tokens, turns, wall time and execution
-- state (ADR-002J). Each result repeats its run's provenance, and a composite
-- foreign key keeps the two equal, so a result row alone names its full
-- system version. Every update must claim the next version of the row it
-- read; a stale update is refused (ADR-002U).

create domain public.ams_commit as text
  check (value ~ '^[0-9a-f]{40}$');

create domain public.ams_label as text
  check (length(btrim(value)) > 0);

-- Optimistic concurrency for the RSI tables. An insert starts at version 1;
-- an update must set version to the stored version + 1, or it is refused
-- with SQLSTATE PT409, which PostgREST answers with HTTP 409.
create function public.ams_guard_version()
returns trigger
language plpgsql
set search_path = ''
as $$
begin
  if tg_op = 'INSERT' then
    new.version := 1;
    new.recorded_at := now();
    new.updated_at := new.recorded_at;
    return new;
  end if;
  if new.version is distinct from old.version + 1 then
    raise exception 'stale update: % id % is at version %, the update claimed %',
      tg_table_name, old.id, old.version, new.version
      using errcode = 'PT409';
  end if;
  new.recorded_at := old.recorded_at;
  new.updated_at := now();
  return new;
end;
$$;
revoke execute on function public.ams_guard_version() from public, anon, authenticated;

create table public.rsi_runs (
  id              bigint generated always as identity primary key,
  run_key         public.ams_label not null unique,  -- the runner's own id, so a rerun adds no duplicate
  arm             text not null check (arm in ('ams', 'no_ams', 'plain_instructions')),
  provider        public.ams_label not null,
  model           public.ams_label not null,  -- exact model ID
  effort          public.ams_label not null,
  runtime_commit  public.ams_commit not null,  -- AMS runtime (src/) commit
  controls_commit public.ams_commit not null,  -- AMS controls (AGENTS, skills adapters) commit
  skills_commit   public.ams_commit not null,  -- skills repository commit the run used
  grader_version  public.ams_commit not null,  -- accepted version that supplied runner and graders
  state           text not null check (state in ('running', 'completed', 'stopped', 'failed')),
  started_at      timestamptz not null,
  finished_at     timestamptz check (finished_at is null or finished_at >= started_at),
  source_kind     public.ams_source_kind not null,
  source_ref      public.ams_label not null,  -- run log path or commit
  source_url      text check (source_url is null or source_url ~ '^https://'),
  strength        public.ams_strength not null,
  is_test         boolean not null default false,  -- test and synthetic rows; never visible to the site
  detail          jsonb not null default '{}'::jsonb,
  version         integer not null default 1,
  recorded_at     timestamptz not null default now(),
  updated_at      timestamptz not null default now(),
  constraint rsi_runs_finished_when_done check ((state = 'running') = (finished_at is null)),
  constraint rsi_runs_provenance unique (id, arm, provider, model, effort, runtime_commit,
    controls_commit, skills_commit, grader_version, is_test)
);

create table public.rsi_results (
  id              bigint generated always as identity primary key,
  run_id          bigint not null,
  arm             text not null,
  provider        public.ams_label not null,
  model           public.ams_label not null,
  effort          public.ams_label not null,
  runtime_commit  public.ams_commit not null,
  controls_commit public.ams_commit not null,
  skills_commit   public.ams_commit not null,
  grader_version  public.ams_commit not null,
  task_id         public.ams_label not null,
  split           text not null check (split in ('dev', 'held_out')),
  trial           integer not null check (trial >= 1),
  execution_state text not null check (execution_state in
                    ('completed', 'runner_error', 'auth_error', 'timeout', 'capped')),
  passed          boolean,
  score           numeric check (score is null or (score >= 0 and score <= 1)),
  cost_usd        numeric(12, 6) not null check (cost_usd >= 0),
  input_tokens    bigint not null check (input_tokens >= 0),
  output_tokens   bigint not null check (output_tokens >= 0),
  turns           integer not null check (turns >= 0),
  wall_seconds    numeric(12, 3) not null check (wall_seconds >= 0),
  source_kind     public.ams_source_kind not null,
  source_ref      public.ams_label not null,
  source_url      text check (source_url is null or source_url ~ '^https://'),
  strength        public.ams_strength not null,
  is_test         boolean not null default false,  -- test and synthetic rows; never visible to the site
  detail          jsonb not null default '{}'::jsonb,
  version         integer not null default 1,
  recorded_at     timestamptz not null default now(),
  updated_at      timestamptz not null default now(),
  -- Only a completed trial is graded; a runner or auth error is a row, not a failure (ADR-002J).
  constraint rsi_results_graded_when_completed check (
    (execution_state = 'completed') = (passed is not null or score is not null)),
  constraint rsi_results_one_per_trial unique (run_id, task_id, trial),
  constraint rsi_results_run_provenance
    foreign key (run_id, arm, provider, model, effort, runtime_commit, controls_commit,
                 skills_commit, grader_version, is_test)
    references public.rsi_runs (id, arm, provider, model, effort, runtime_commit,
                                controls_commit, skills_commit, grader_version, is_test)
);

comment on table public.rsi_runs is
  'One RSI run: one arm of one round at one pinned system version, provider, model, effort and grader.';
comment on table public.rsi_results is
  'One trial of one task in an RSI run, with its grade, cost, tokens, execution state and source.';

create trigger rsi_runs_guard_version
  before insert or update on public.rsi_runs
  for each row execute function public.ams_guard_version();
create trigger rsi_results_guard_version
  before insert or update on public.rsi_results
  for each row execute function public.ams_guard_version();

-- The baseline trigger already enables RLS; state it here so the tables
-- never depend on the trigger having run.
alter table public.rsi_runs enable row level security;
alter table public.rsi_results enable row level security;

revoke all on public.rsi_runs from anon, authenticated;
revoke all on public.rsi_results from anon, authenticated;
grant select on public.rsi_runs to anon, authenticated;
grant select on public.rsi_results to anon, authenticated;
grant select, insert, update, delete on public.rsi_runs to service_role;
grant select, insert, update, delete on public.rsi_results to service_role;

create policy rsi_runs_site_read on public.rsi_runs
  for select to anon, authenticated
  using (not is_test);
create policy rsi_results_site_read on public.rsi_results
  for select to anon, authenticated
  using (not is_test);
