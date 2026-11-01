-- S-006 TK-002: the first data table, build events, read by the site.
-- Clients may only SELECT rows that are not test rows; the local Python
-- writer inserts with the service role key, which bypasses RLS.

-- Shared provenance vocabulary. Later tables (RSI results and runs in
-- TK-003, imported build history in TK-004) reuse these domains.
create domain public.ams_strength as text
  check (value in (
    'recorded_fact',          -- taken directly from a Git, GitHub or record file
    'anecdote',
    'single_trial',
    'repeated_trials',
    'held_out_with_interval'
  ));

create domain public.ams_source_kind as text
  check (value in ('commit', 'pr', 'path', 'jot'));

create table public.build_events (
  id          bigint generated always as identity primary key,
  kind        text not null check (kind ~ '^[a-z][a-z_]*$'),  -- merge, commit, pr, spec, task, return, correction, ...
  subject     text not null check (length(btrim(subject)) > 0),
  summary     text not null check (length(btrim(summary)) > 0),
  occurred_at timestamptz not null,
  source_kind public.ams_source_kind not null,
  source_ref  text not null check (length(btrim(source_ref)) > 0),  -- commit SHA, PR number or repository path
  source_url  text check (source_url is null or source_url ~ '^https://'),
  strength    public.ams_strength not null,
  is_test     boolean not null default false,  -- test and synthetic rows; never visible to the site
  detail      jsonb not null default '{}'::jsonb,
  recorded_at timestamptz not null default now(),
  -- One row per event from one source, so a re-import adds no duplicates.
  constraint build_events_one_per_source unique (kind, source_kind, source_ref)
);

comment on table public.build_events is
  'How AMS built itself: one row per Spec, Task, PR, commit, return or correction event, each naming its source and strength.';

-- The baseline trigger already enables RLS; state it here so the table
-- never depends on the trigger having run.
alter table public.build_events enable row level security;

revoke all on public.build_events from anon, authenticated;
grant select on public.build_events to anon, authenticated;
grant select, insert, update, delete on public.build_events to service_role;

create policy build_events_site_read on public.build_events
  for select to anon, authenticated
  using (not is_test);
