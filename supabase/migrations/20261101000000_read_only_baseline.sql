-- Read-only baseline for the AMS Supabase project.
-- The public site uses the publishable (anon) key and may only read.
-- The local Python writer uses the service role key, which bypasses RLS.

-- Clients never write to public tables, now or in future migrations.
revoke insert, update, delete, truncate on all tables in schema public from anon, authenticated;
alter default privileges in schema public revoke insert, update, delete, truncate on tables from anon, authenticated;
alter default privileges in schema public revoke usage, update on sequences from anon, authenticated;
alter default privileges in schema public revoke execute on functions from anon, authenticated, public;

-- Every new public table starts with row-level security on, so a table
-- with no SELECT policy is invisible to the site rather than open.
create or replace function public.ams_enable_rls_on_create()
returns event_trigger
language plpgsql
security definer
set search_path = pg_catalog, public
as $$
declare obj record;
begin
  for obj in
    select * from pg_event_trigger_ddl_commands()
    where command_tag = 'CREATE TABLE' and schema_name = 'public'
  loop
    execute format('alter table %s enable row level security', obj.object_identity);
  end loop;
end;
$$;
revoke execute on function public.ams_enable_rls_on_create() from public, anon, authenticated;

drop event trigger if exists ams_enable_rls_on_create;
create event trigger ams_enable_rls_on_create
  on ddl_command_end
  when tag in ('CREATE TABLE')
  execute function public.ams_enable_rls_on_create();
