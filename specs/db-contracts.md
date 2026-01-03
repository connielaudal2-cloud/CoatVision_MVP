# Database Contracts - ForgeOS Platform

**Version:** 1.0.0  
**Last Updated:** 2026-01-03  
**Database:** PostgreSQL 15+  
**Provider:** Supabase

---

## Overview

This document defines the database schema and contracts for the ForgeOS platform. The database uses PostgreSQL with Supabase extensions for authentication, storage, and real-time capabilities.

## Connection

### Connection String Format
```
postgresql://[user]:[password]@[host]:[port]/[database]?sslmode=require
```

### Environment Variable
```bash
DATABASE_URL=postgresql://user:password@host:port/database
```

### Supabase Configuration
```bash
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_KEY=your-service-role-key
SUPABASE_ANON_KEY=your-anon-public-key
```

---

## Extensions

Required PostgreSQL extensions:

```sql
create extension if not exists pgcrypto;
create extension if not exists "uuid-ossp";
```

- **pgcrypto**: Cryptographic functions, secure UUID generation
- **uuid-ossp**: UUID generation functions

---

## Schema Overview

```
┌─────────────────┐
│    analyses     │
│  (main table)   │
└────────┬────────┘
         │
         │ FK: job_id
         ▼
    ┌────────┐
    │  jobs  │
    └────────┘
         ▲
         │
         │ FK: analysis_id
         ▼
   ┌──────────┐
   │ reports  │
   └──────────┘

   ┌────────────────────┐
   │ training_sessions  │
   │  (independent)     │
   └────────────────────┘
```

---

## Tables

### Table: `analyses`

Primary table storing image analysis results and metrics.

```sql
create table if not exists public.analyses (
  id uuid primary key default gen_random_uuid(),
  created_at timestamptz not null default now(),
  filename text,
  output_filename text,
  metrics jsonb,
  status text default 'completed',
  user_id uuid,
  job_id uuid references public.jobs(id) on delete set null
);
```

**Columns**:

| Column | Type | Nullable | Default | Description |
|--------|------|----------|---------|-------------|
| `id` | uuid | NO | gen_random_uuid() | Primary key |
| `created_at` | timestamptz | NO | now() | Creation timestamp |
| `filename` | text | YES | NULL | Original image filename |
| `output_filename` | text | YES | NULL | Processed image filename |
| `metrics` | jsonb | YES | NULL | Analysis metrics (JSON) |
| `status` | text | YES | 'completed' | Analysis status |
| `user_id` | uuid | YES | NULL | User who created the analysis |
| `job_id` | uuid | YES | NULL | Associated job ID (if batch) |

**Status Values**:
- `pending`: Analysis queued
- `processing`: Currently analyzing
- `completed`: Analysis finished successfully
- `failed`: Analysis failed

**Metrics JSON Schema**:
```json
{
  "cvi": 0.0-1.0,
  "cqi": 0.0-1.0,
  "coverage_percent": 0.0-100.0,
  "edge_coverage_ratio": 0.0-1.0,
  "defects_detected": integer,
  "severity": "low|medium|high",
  "confidence": 0.0-1.0,
  "processing_time_ms": integer
}
```

**Indexes**:
```sql
create index if not exists idx_analyses_user_id on public.analyses(user_id);
create index if not exists idx_analyses_created_at on public.analyses(created_at desc);
create index if not exists idx_analyses_status on public.analyses(status);
create index if not exists idx_analyses_job_id on public.analyses(job_id);
```

**Row-Level Security**:
```sql
alter table public.analyses enable row level security;

-- Users can read their own analyses
create policy analyses_read_authenticated on public.analyses
  for select using (auth.role() = 'authenticated');

-- Users can insert their own analyses
create policy analyses_insert_authenticated on public.analyses
  for insert with check (auth.uid() = user_id);

-- Users can update their own analyses
create policy analyses_update_own on public.analyses
  for update using (auth.uid() = user_id);
```

---

### Table: `jobs`

Tracks asynchronous processing jobs.

```sql
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
```

**Columns**:

| Column | Type | Nullable | Default | Description |
|--------|------|----------|---------|-------------|
| `id` | uuid | NO | gen_random_uuid() | Primary key |
| `created_at` | timestamptz | NO | now() | Creation timestamp |
| `updated_at` | timestamptz | NO | now() | Last update timestamp |
| `status` | text | YES | 'pending' | Job status |
| `job_type` | text | YES | NULL | Type of job |
| `params` | jsonb | YES | NULL | Job parameters (JSON) |
| `results` | jsonb | YES | NULL | Job results (JSON) |
| `error_message` | text | YES | NULL | Error message if failed |
| `user_id` | uuid | YES | NULL | User who created the job |

**Status Values**:
- `pending`: Queued for processing
- `running`: Currently processing
- `completed`: Successfully completed
- `failed`: Processing failed
- `cancelled`: Cancelled by user

**Job Types**:
- `batch_analysis`: Process multiple images
- `model_training`: Train custom ML model
- `report_generation`: Generate multiple reports
- `data_export`: Export data

**Params JSON Schema** (batch_analysis):
```json
{
  "image_ids": ["uuid1", "uuid2"],
  "options": {
    "sensitivity": "high"
  }
}
```

**Results JSON Schema** (batch_analysis):
```json
{
  "processed": 10,
  "successful": 9,
  "failed": 1,
  "analysis_ids": ["uuid1", "uuid2"],
  "failed_ids": ["uuid3"]
}
```

**Indexes**:
```sql
create index if not exists idx_jobs_user_id on public.jobs(user_id);
create index if not exists idx_jobs_status on public.jobs(status);
create index if not exists idx_jobs_created_at on public.jobs(created_at desc);
```

**Triggers**:
```sql
-- Update updated_at on row update
create or replace function update_updated_at_column()
returns trigger as $$
begin
  new.updated_at = now();
  return new;
end;
$$ language plpgsql;

create trigger update_jobs_updated_at
  before update on public.jobs
  for each row
  execute function update_updated_at_column();
```

---

### Table: `reports`

Stores generated report metadata and references.

```sql
create table if not exists public.reports (
  id uuid primary key default gen_random_uuid(),
  created_at timestamptz not null default now(),
  analysis_id uuid references public.analyses(id) on delete cascade,
  url text,
  metadata jsonb,
  template text,
  user_id uuid
);
```

**Columns**:

| Column | Type | Nullable | Default | Description |
|--------|------|----------|---------|-------------|
| `id` | uuid | NO | gen_random_uuid() | Primary key |
| `created_at` | timestamptz | NO | now() | Creation timestamp |
| `analysis_id` | uuid | YES | NULL | Associated analysis ID |
| `url` | text | YES | NULL | Report file URL |
| `metadata` | jsonb | YES | NULL | Report metadata (JSON) |
| `template` | text | YES | NULL | Template used |
| `user_id` | uuid | YES | NULL | User who created the report |

**Metadata JSON Schema**:
```json
{
  "pages": integer,
  "size_bytes": integer,
  "format": "pdf|xlsx|csv",
  "generated_at": "ISO 8601 timestamp",
  "includes_images": boolean,
  "language": "en|no"
}
```

**Indexes**:
```sql
create index if not exists idx_reports_analysis_id on public.reports(analysis_id);
create index if not exists idx_reports_user_id on public.reports(user_id);
create index if not exists idx_reports_created_at on public.reports(created_at desc);
```

**Foreign Key Cascade**:
- Deleting an analysis will cascade delete associated reports

---

### Table: `training_sessions`

Stores AI model training session data.

```sql
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
```

**Columns**:

| Column | Type | Nullable | Default | Description |
|--------|------|----------|---------|-------------|
| `id` | uuid | NO | gen_random_uuid() | Primary key |
| `created_at` | timestamptz | NO | now() | Creation timestamp |
| `updated_at` | timestamptz | NO | now() | Last update timestamp |
| `notes` | text | YES | NULL | Session notes |
| `data` | jsonb | YES | NULL | Training data (JSON) |
| `status` | text | YES | 'pending' | Training status |
| `model_version` | text | YES | NULL | Model version identifier |
| `accuracy_metrics` | jsonb | YES | NULL | Model accuracy metrics |
| `user_id` | uuid | YES | NULL | User who created the session |

**Data JSON Schema**:
```json
{
  "images": ["uuid1", "uuid2"],
  "labels": ["good", "defect", "good"],
  "annotations": [
    {
      "image_id": "uuid1",
      "regions": [
        {"x": 100, "y": 100, "width": 50, "height": 50, "label": "defect"}
      ]
    }
  ]
}
```

**Accuracy Metrics JSON Schema**:
```json
{
  "accuracy": 0.95,
  "precision": 0.93,
  "recall": 0.97,
  "f1_score": 0.95,
  "confusion_matrix": [[85, 5], [3, 97]]
}
```

**Indexes**:
```sql
create index if not exists idx_training_sessions_user_id on public.training_sessions(user_id);
create index if not exists idx_training_sessions_status on public.training_sessions(status);
```

---

## Views

### View: `user_analysis_summary`

Aggregated analysis statistics per user.

```sql
create or replace view user_analysis_summary as
select
  user_id,
  count(*) as total_analyses,
  count(*) filter (where status = 'completed') as completed,
  count(*) filter (where status = 'failed') as failed,
  avg((metrics->>'cvi')::float) as avg_cvi,
  max(created_at) as last_analysis_at
from public.analyses
group by user_id;
```

---

## Remote Procedure Calls (RPCs)

### RPC: `get_user_stats`

Get comprehensive user statistics.

```sql
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
    'last_activity', max(greatest(a.created_at, r.created_at, j.created_at))
  ) into result
  from public.analyses a
  left join public.reports r on r.user_id = p_user_id
  left join public.jobs j on j.user_id = p_user_id
  where a.user_id = p_user_id;
  
  return result;
end;
$$;
```

**Usage**:
```sql
select get_user_stats('user-uuid-here');
```

---

### RPC: `cleanup_old_analyses`

Remove analyses older than specified days.

```sql
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
```

**Usage**:
```sql
-- Delete analyses older than 90 days
select cleanup_old_analyses(90);
```

---

## Supabase Storage

### Buckets

**Bucket: `images`**
- Original uploaded images
- Access: Authenticated users

**Bucket: `outputs`**
- Processed analysis images
- Access: Authenticated users

**Bucket: `reports`**
- Generated PDF reports
- Access: Authenticated users

### Storage Policies

```sql
-- Allow authenticated users to upload images
create policy "Users can upload images"
on storage.objects for insert
to authenticated
with check (bucket_id = 'images');

-- Allow users to read their own files
create policy "Users can read own files"
on storage.objects for select
to authenticated
using (auth.uid()::text = (storage.foldername(name))[1]);
```

---

## Migrations

### Migration Strategy
1. All migrations are forward-only
2. Use `IF NOT EXISTS` for idempotent operations
3. Add indexes after table creation
4. Enable RLS after policies are defined

### Example Migration File
```sql
-- Migration: 001_initial_schema.sql
-- Date: 2026-01-03

-- Extensions
create extension if not exists pgcrypto;
create extension if not exists "uuid-ossp";

-- Tables
create table if not exists public.analyses (...);
create table if not exists public.jobs (...);
-- ... etc

-- Indexes
create index if not exists idx_analyses_user_id on public.analyses(user_id);
-- ... etc

-- RLS
alter table public.analyses enable row level security;
-- ... etc

-- RPCs
create or replace function get_user_stats(...) ...;
-- ... etc
```

---

## Backup and Recovery

### Automated Backups
- **Frequency**: Daily (managed by Supabase)
- **Retention**: 7 days (free tier) / 30 days (paid tier)
- **Location**: Supabase infrastructure

### Manual Backup
```bash
pg_dump $DATABASE_URL > backup_$(date +%Y%m%d).sql
```

### Restore
```bash
psql $DATABASE_URL < backup_20260103.sql
```

---

## Performance Considerations

### Recommended Indexes
All recommended indexes are included in the schema above.

### Query Optimization
- Use `select` with specific columns instead of `select *`
- Add `where` clauses to filter early
- Use `limit` for pagination
- Create indexes on frequently queried columns

### Connection Pooling
Use connection pooling for high-traffic applications:
- **Tool**: PgBouncer (included with Supabase)
- **Max Connections**: Based on plan tier

---

## Security

### Row-Level Security (RLS)
All tables have RLS enabled with policies ensuring:
- Users can only access their own data
- Service role can access all data
- Anonymous users have no access (except via service role)

### Encryption
- **At Rest**: Managed by Supabase/Cloud Provider
- **In Transit**: TLS 1.3 required

### Audit Logging
Consider adding audit trigger:
```sql
create table if not exists audit_log (
  id uuid primary key default gen_random_uuid(),
  created_at timestamptz not null default now(),
  user_id uuid,
  action text,
  table_name text,
  record_id uuid,
  changes jsonb
);
```

---

## Data Retention

### Default Retention
- **Analyses**: Indefinite
- **Reports**: Indefinite
- **Jobs**: 90 days (recommended cleanup)
- **Training Sessions**: Indefinite

### Cleanup Schedule
```sql
-- Run monthly
select cleanup_old_analyses(90);

-- Delete old failed jobs
delete from jobs 
where status = 'failed' 
and created_at < now() - interval '30 days';
```

---

## Monitoring

### Key Metrics to Monitor
- Connection pool utilization
- Query execution time
- Table sizes
- Index usage
- Lock contention

### Useful Queries

**Table sizes**:
```sql
select
  schemaname,
  tablename,
  pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as size
from pg_tables
where schemaname = 'public'
order by pg_total_relation_size(schemaname||'.'||tablename) desc;
```

**Unused indexes**:
```sql
select
  schemaname,
  tablename,
  indexname,
  idx_scan as index_scans
from pg_stat_user_indexes
where idx_scan = 0
and indexrelname not like 'pg_toast%';
```

---

For API usage of these database contracts, see:
- API Contracts: `/specs/api-contracts.md`
- System Contract: `/docs/system-contract.md`
- Example Schema: `/payloads/01_db.sql`
