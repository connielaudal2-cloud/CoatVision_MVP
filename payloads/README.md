# Example Payloads

**Practical examples for quick setup and integration**

---

## Overview

This directory contains ready-to-use example files that you can copy and adapt for your ForgeOS deployment. These are practical, working examples that demonstrate real-world usage patterns.

---

## 📁 Files

### [01_db.sql](./01_db.sql)
**Complete database setup script**

#### What it does:
- Creates all required PostgreSQL extensions
- Defines all tables with proper types and constraints
- Creates performance-optimized indexes
- Sets up Row-Level Security (RLS) policies
- Implements database triggers
- Creates stored procedures (RPCs)
- Includes verification queries

#### How to use:

**Option 1: Direct PostgreSQL**
```bash
# Apply entire schema
psql $DATABASE_URL < payloads/01_db.sql

# Or connect and run interactively
psql $DATABASE_URL
\i payloads/01_db.sql
```

**Option 2: Supabase SQL Editor**
1. Log in to your Supabase dashboard
2. Go to SQL Editor
3. Click "New Query"
4. Copy contents of `01_db.sql`
5. Click "Run"

**Option 3: Supabase CLI**
```bash
supabase db push
# Or apply via migration
supabase migration new initial_schema
# Copy 01_db.sql contents to the migration file
supabase db push
```

#### Features:
- ✅ Idempotent - safe to run multiple times
- ✅ Complete - everything needed for basic operation
- ✅ Commented - explains each section
- ✅ Tested - verified working schema
- ✅ Secure - RLS enabled by default
- ✅ Optimized - includes performance indexes

#### What's included:
- Extensions: pgcrypto, uuid-ossp
- Tables: analyses, jobs, reports, training_sessions
- Indexes: user_id, created_at, status, etc.
- RLS Policies: user-based access control
- Triggers: auto-update timestamps
- Functions: get_user_stats, cleanup_old_analyses
- Verification queries

---

### [02_edge_functions.json](./02_edge_functions.json)
**Supabase Edge Functions examples and reference**

#### What it contains:
- Complete edge function definitions
- Deployment instructions
- Example handler code
- Environment variable configuration
- Testing procedures
- Common patterns and best practices

#### Use cases:

**1. Image Analysis Function**
```bash
# Create function
supabase functions new analyze-image

# Copy handler code from 02_edge_functions.json
# Deploy
supabase functions deploy analyze-image

# Set secrets
supabase secrets set OPENAI_API_KEY=sk-your-key
```

**2. Report Generation Function**
```bash
supabase functions new generate-report
# Deploy and configure as above
```

**3. Webhook Handler**
```bash
supabase functions new webhook-handler
# For receiving external webhooks
```

**4. Batch Processor**
```bash
supabase functions new batch-processor
# For processing multiple items
```

#### Features:
- ✅ Production-ready examples
- ✅ TypeScript/Deno code samples
- ✅ Environment variable handling
- ✅ Error handling patterns
- ✅ CORS configuration
- ✅ Authentication examples
- ✅ Testing procedures

#### What's included:
- 5 complete function examples
- Handler code structure
- Deployment commands
- Environment variable setup
- Local testing instructions
- Monitoring setup
- Best practices guide

---

## 🚀 Quick Start

### Step 1: Set Up Database
```bash
# Export your database connection string
export DATABASE_URL="postgresql://user:pass@host:port/database"

# Apply schema
psql $DATABASE_URL < payloads/01_db.sql

# Verify
psql $DATABASE_URL -c "\dt"
```

### Step 2: Deploy Edge Functions (Optional)
```bash
# Install Supabase CLI
npm install -g supabase

# Login
supabase login

# Link to project
supabase link --project-ref your-project-id

# Create function
supabase functions new analyze-image

# Copy code from 02_edge_functions.json to the handler

# Deploy
supabase functions deploy analyze-image

# Set environment variables
supabase secrets set OPENAI_API_KEY=your-key
```

### Step 3: Test
```bash
# Test database
psql $DATABASE_URL -c "SELECT get_user_stats('your-user-uuid');"

# Test edge function
curl -X POST \
  https://your-project.supabase.co/functions/v1/analyze-image \
  -H "Authorization: Bearer your-anon-key" \
  -H "Content-Type: application/json" \
  -d '{"image_url": "https://example.com/image.jpg"}'
```

---

## 🎯 Usage Patterns

### For New Deployments

**Complete setup from scratch:**
```bash
# 1. Create Supabase project (via dashboard)

# 2. Get connection details
export DATABASE_URL="postgres://..."
export SUPABASE_URL="https://xxx.supabase.co"
export SUPABASE_SERVICE_KEY="..."
export SUPABASE_ANON_KEY="..."

# 3. Apply database schema
psql $DATABASE_URL < payloads/01_db.sql

# 4. Verify setup
psql $DATABASE_URL -c "\dt"
psql $DATABASE_URL -c "SELECT * FROM pg_policies;"

# 5. Optional: Deploy edge functions
# (Follow steps in 02_edge_functions.json)
```

### For Development

**Local testing:**
```bash
# Use local Supabase instance
supabase start

# Apply schema
supabase db reset
psql $(supabase db url) < payloads/01_db.sql

# Test locally
supabase functions serve
```

### For Production

**Production deployment:**
```bash
# Production database
psql $PROD_DATABASE_URL < payloads/01_db.sql

# Production edge functions
supabase link --project-ref prod-project-id
supabase functions deploy --project-ref prod-project-id

# Set production secrets
supabase secrets set OPENAI_API_KEY=prod-key --project-ref prod-project-id
```

---

## 🔧 Customization

### Modifying the Database Schema

**To add custom fields:**
```sql
-- Add to 01_db.sql or create a new migration
alter table public.analyses 
add column custom_field text;

-- Add index if frequently queried
create index idx_analyses_custom_field 
on public.analyses(custom_field);
```

**To add custom tables:**
```sql
-- Add to 01_db.sql after existing tables
create table if not exists public.custom_table (
  id uuid primary key default gen_random_uuid(),
  created_at timestamptz not null default now(),
  -- your columns here
);

-- Enable RLS
alter table public.custom_table enable row level security;

-- Add policies
create policy custom_read on public.custom_table
  for select using (auth.role() = 'authenticated');
```

### Modifying Edge Functions

**To customize function logic:**
1. Copy the example from `02_edge_functions.json`
2. Modify the handler code
3. Add any required dependencies
4. Update environment variables
5. Deploy with `supabase functions deploy`

---

## 📋 Validation

### Database Validation

After applying `01_db.sql`, verify:

```sql
-- Check tables exist
SELECT table_name FROM information_schema.tables 
WHERE table_schema = 'public';

-- Check RLS is enabled
SELECT tablename, rowsecurity FROM pg_tables 
WHERE schemaname = 'public';

-- Check indexes exist
SELECT indexname FROM pg_indexes 
WHERE schemaname = 'public';

-- Check functions exist
SELECT routine_name FROM information_schema.routines 
WHERE routine_schema = 'public';

-- Test a function
SELECT get_user_stats('00000000-0000-0000-0000-000000000000');
```

### Edge Function Validation

```bash
# Test locally
supabase functions serve analyze-image

# In another terminal
curl -X POST http://localhost:54321/functions/v1/analyze-image \
  -H "Authorization: Bearer anon-key" \
  -d '{"test": true}'

# Check logs
supabase functions logs analyze-image
```

---

## 🔒 Security Notes

### Database Security
- ✅ All tables have RLS enabled
- ✅ No default public access
- ✅ User-based access policies
- ✅ Service role for backend only

### Edge Function Security
- ✅ Environment variables for secrets
- ✅ JWT token validation
- ✅ CORS properly configured
- ✅ Input validation required

### Secrets Management
**Never commit these to Git:**
```bash
# Bad - Don't do this
OPENAI_API_KEY=sk-real-key-here

# Good - Use placeholders
OPENAI_API_KEY=${OPENAI_API_KEY}
```

---

## 📊 Examples Reference

### Sample Analysis Record
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "created_at": "2026-01-03T12:00:00Z",
  "filename": "coating-sample.jpg",
  "output_filename": "coating-sample-analyzed.jpg",
  "metrics": {
    "cvi": 0.85,
    "cqi": 0.78,
    "coverage_percent": 82.5,
    "edge_coverage_ratio": 0.75
  },
  "status": "completed",
  "user_id": "user-uuid"
}
```

### Sample Job Record
```json
{
  "id": "job-uuid",
  "created_at": "2026-01-03T12:00:00Z",
  "status": "completed",
  "job_type": "batch_analysis",
  "params": {
    "image_ids": ["id1", "id2", "id3"]
  },
  "results": {
    "processed": 3,
    "successful": 3,
    "failed": 0
  }
}
```

### Sample Edge Function Request
```bash
curl -X POST https://project.supabase.co/functions/v1/analyze-image \
  -H "Authorization: Bearer anon-key" \
  -H "Content-Type: application/json" \
  -d '{
    "image_url": "https://example.com/coating.jpg",
    "options": {
      "sensitivity": "high"
    }
  }'
```

---

## 🔗 Related Documentation

- **System Contract**: `/docs/system-contract.md` - Architecture overview
- **API Contracts**: `/specs/api-contracts.md` - API documentation
- **Database Contracts**: `/specs/db-contracts.md` - Detailed schema
- **Status**: `/docs/status.md` - Current platform status
- **Roadmap**: `/docs/roadmap.md` - Future plans

---

## 📞 Support

### Issues with Database Setup
1. Check PostgreSQL version (need 15+)
2. Verify extensions are available
3. Check permissions (need CREATE, ALTER, etc.)
4. Review error messages in SQL output

### Issues with Edge Functions
1. Check Supabase CLI version
2. Verify you're logged in: `supabase login`
3. Verify project is linked: `supabase link`
4. Check function logs: `supabase functions logs`

### Common Problems

**"Extension does not exist"**
```sql
-- Enable extensions manually if needed
CREATE EXTENSION IF NOT EXISTS pgcrypto CASCADE;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp" CASCADE;
```

**"Permission denied"**
```bash
# Use service role key for admin operations
export SUPABASE_SERVICE_ROLE_KEY="your-service-role-key"
```

**"Function not found"**
```bash
# Redeploy function
supabase functions deploy function-name --no-verify-jwt
```

---

## ✅ Checklist

### Before Using These Files:
- [ ] Read the documentation in `/docs/`
- [ ] Understand the contracts in `/specs/`
- [ ] Have Supabase project created
- [ ] Have environment variables ready
- [ ] Have database connection string
- [ ] Have Supabase CLI installed (for edge functions)

### After Applying:
- [ ] Verify tables were created
- [ ] Check RLS policies are active
- [ ] Test database functions work
- [ ] Verify edge functions deploy
- [ ] Test end-to-end flow
- [ ] Review logs for errors

---

**These files are production-ready and thoroughly tested. Use them as starting points for your deployment.**

**Version:** 1.0.0  
**Last Updated:** 2026-01-03
