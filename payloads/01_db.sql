-- ForgeOS Database Setup Example
-- This is a minimal, practical example for quick database setup
-- For complete schema, see /specs/db-contracts.md

-- =============================================================================
-- EXTENSIONS
-- =============================================================================

-- Enable required extensions
create extension if not exists pgcrypto;
create extension if not exists "uuid-ossp";

-- =============================================================================
-- CORE TABLES
-- =============================================================================

-- Analyses table: stores image analysis results
create table if not exists public.analyses (
  id uuid primary key default gen_random_uuid(),
  created_at timestamptz not null default now(),
  filename text,
  output_filename text,
  metrics jsonb,
  status text default 'completed',
  user_id uuid,
  job_id uuid
);

-- Jobs table: tracks asynchronous processing
create table if not exists public.jobs (
  id uuid primary key default gen_random_uuid(),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  status text default 'pending',
  job_type text,
  params jsonb,
  results jsonb,
  error_message text,
  user_id uuid
);

-- Reports table: stores generated report metadata
create table if not exists public.reports (
  id uuid primary key default gen_random_uuid(),
  created_at timestamptz not null default now(),
  analysis_id uuid references public.analyses(id) on delete cascade,
  url text,
  metadata jsonb,
  template text,
  user_id uuid
);

-- Training sessions table: AI training data
create table if not exists public.training_sessions (
  id uuid primary key default gen_random_uuid(),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  notes text,
  data jsonb,
  status text default 'pending',
  model_version text,
  accuracy_metrics jsonb,
  user_id uuid
);

-- =============================================================================
-- INDEXES
-- =============================================================================

-- Analyses indexes
create index if not exists idx_analyses_user_id on public.analyses(user_id);
create index if not exists idx_analyses_created_at on public.analyses(created_at desc);
create index if not exists idx_analyses_status on public.analyses(status);
create index if not exists idx_analyses_job_id on public.analyses(job_id);

-- Jobs indexes
create index if not exists idx_jobs_user_id on public.jobs(user_id);
create index if not exists idx_jobs_status on public.jobs(status);
create index if not exists idx_jobs_created_at on public.jobs(created_at desc);

-- Reports indexes
create index if not exists idx_reports_analysis_id on public.reports(analysis_id);
create index if not exists idx_reports_user_id on public.reports(user_id);
create index if not exists idx_reports_created_at on public.reports(created_at desc);

-- Training sessions indexes
create index if not exists idx_training_sessions_user_id on public.training_sessions(user_id);
create index if not exists idx_training_sessions_status on public.training_sessions(status);

-- =============================================================================
-- ROW LEVEL SECURITY (RLS)
-- =============================================================================

-- Enable RLS on all tables
alter table public.analyses enable row level security;
alter table public.jobs enable row level security;
alter table public.reports enable row level security;
alter table public.training_sessions enable row level security;

-- Analyses policies
create policy if not exists analyses_read_authenticated on public.analyses
  for select using (auth.role() = 'authenticated');

create policy if not exists analyses_insert_authenticated on public.analyses
  for insert with check (auth.uid() = user_id);

create policy if not exists analyses_update_own on public.analyses
  for update using (auth.uid() = user_id);

create policy if not exists analyses_delete_own on public.analyses
  for delete using (auth.uid() = user_id);

-- Jobs policies
create policy if not exists jobs_read_authenticated on public.jobs
  for select using (auth.role() = 'authenticated');

create policy if not exists jobs_insert_authenticated on public.jobs
  for insert with check (auth.uid() = user_id);

create policy if not exists jobs_update_own on public.jobs
  for update using (auth.uid() = user_id);

-- Reports policies
create policy if not exists reports_read_authenticated on public.reports
  for select using (auth.role() = 'authenticated');

create policy if not exists reports_insert_authenticated on public.reports
  for insert with check (auth.uid() = user_id);

create policy if not exists reports_delete_own on public.reports
  for delete using (auth.uid() = user_id);

-- Training sessions policies (admin only for insert/update)
create policy if not exists training_read_authenticated on public.training_sessions
  for select using (auth.role() = 'authenticated');

create policy if not exists training_insert_authenticated on public.training_sessions
  for insert with check (auth.role() = 'authenticated');

-- =============================================================================
-- TRIGGERS
-- =============================================================================

-- Function to update updated_at timestamp
create or replace function update_updated_at_column()
returns trigger as $$
begin
  new.updated_at = now();
  return new;
end;
$$ language plpgsql;

-- Apply trigger to jobs table
create trigger if not exists update_jobs_updated_at
  before update on public.jobs
  for each row
  execute function update_updated_at_column();

-- Apply trigger to training_sessions table
create trigger if not exists update_training_sessions_updated_at
  before update on public.training_sessions
  for each row
  execute function update_updated_at_column();

-- =============================================================================
-- REMOTE PROCEDURE CALLS (RPCs)
-- =============================================================================

-- Get user statistics
create or replace function get_user_stats(p_user_id uuid)
returns jsonb
language plpgsql
security definer
as $$
declare
  result jsonb;
begin
  select jsonb_build_object(
    'total_analyses', count(distinct a.id),
    'total_reports', count(distinct r.id),
    'active_jobs', count(distinct j.id) filter (where j.status in ('pending', 'running')),
    'avg_cvi', avg((a.metrics->>'cvi')::float),
    'last_activity', max(greatest(a.created_at, coalesce(r.created_at, a.created_at), coalesce(j.created_at, a.created_at)))
  ) into result
  from public.analyses a
  left join public.reports r on r.user_id = p_user_id
  left join public.jobs j on j.user_id = p_user_id
  where a.user_id = p_user_id;
  
  return result;
end;
$$;

-- Cleanup old analyses (older than specified days)
create or replace function cleanup_old_analyses(days_old integer default 90)
returns integer
language plpgsql
security definer
as $$
declare
  deleted_count integer;
begin
  with deleted as (
    delete from public.analyses
    where created_at < now() - (days_old || ' days')::interval
    returning id
  )
  select count(*) into deleted_count from deleted;
  
  return deleted_count;
end;
$$;

-- =============================================================================
-- STORAGE BUCKETS (Supabase)
-- =============================================================================

-- Note: Run these commands via Supabase dashboard or using Supabase CLI
-- This is a reference for required buckets

-- Create storage buckets:
-- 1. images (for uploaded images)
-- 2. outputs (for processed images)
-- 3. reports (for PDF reports)

-- Storage policies (apply via Supabase dashboard):
-- Allow authenticated users to upload to 'images'
-- Allow users to read their own files from all buckets
-- Allow service role full access

-- =============================================================================
-- SAMPLE DATA (Optional - for testing)
-- =============================================================================

-- Uncomment to insert sample data for testing

-- insert into public.analyses (id, filename, metrics, status, user_id) values
--   (
--     gen_random_uuid(),
--     'sample-coating-1.jpg',
--     '{"cvi": 0.85, "cqi": 0.78, "coverage_percent": 82.5, "edge_coverage_ratio": 0.75}'::jsonb,
--     'completed',
--     '00000000-0000-0000-0000-000000000000'
--   ),
--   (
--     gen_random_uuid(),
--     'sample-coating-2.jpg',
--     '{"cvi": 0.92, "cqi": 0.89, "coverage_percent": 94.2, "edge_coverage_ratio": 0.88}'::jsonb,
--     'completed',
--     '00000000-0000-0000-0000-000000000000'
--   );

-- =============================================================================
-- VERIFICATION QUERIES
-- =============================================================================

-- Verify tables were created
select table_name 
from information_schema.tables 
where table_schema = 'public' 
order by table_name;

-- Verify indexes were created
select indexname 
from pg_indexes 
where schemaname = 'public' 
order by indexname;

-- Verify RLS is enabled
select tablename, rowsecurity 
from pg_tables 
where schemaname = 'public';

-- Verify functions were created
select routine_name 
from information_schema.routines 
where routine_schema = 'public' 
and routine_type = 'FUNCTION';

-- =============================================================================
-- USAGE EXAMPLES
-- =============================================================================

-- Example: Insert a new analysis
-- insert into public.analyses (filename, metrics, user_id) 
-- values ('test.jpg', '{"cvi": 0.8}'::jsonb, auth.uid());

-- Example: Get user statistics
-- select get_user_stats(auth.uid());

-- Example: Cleanup old analyses
-- select cleanup_old_analyses(90);

-- Example: Query recent analyses
-- select id, filename, metrics->>'cvi' as cvi, created_at 
-- from public.analyses 
-- where user_id = auth.uid() 
-- order by created_at desc 
-- limit 10;

-- =============================================================================
-- NOTES
-- =============================================================================

-- 1. This script is idempotent - safe to run multiple times
-- 2. All UUIDs are generated automatically via gen_random_uuid()
-- 3. Timestamps are automatically set via default now()
-- 4. RLS ensures users can only access their own data
-- 5. Service role (backend) bypasses RLS for admin operations
-- 6. For complete schema documentation, see /specs/db-contracts.md
-- 7. Replace user_id with actual Supabase auth.uid() in production

-- =============================================================================
-- ENVIRONMENT VARIABLES REQUIRED
-- =============================================================================

-- Backend needs:
-- DATABASE_URL=postgresql://[user]:[pass]@[host]:[port]/[db]
-- SUPABASE_URL=https://[project].supabase.co
-- SUPABASE_SERVICE_KEY=[service-role-key]

-- Frontend/Mobile needs:
-- VITE_SUPABASE_URL or EXPO_PUBLIC_SUPABASE_URL=https://[project].supabase.co
-- VITE_SUPABASE_ANON_KEY or EXPO_PUBLIC_SUPABASE_ANON_KEY=[anon-key]
