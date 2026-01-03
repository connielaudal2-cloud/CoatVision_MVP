# ForgeOS Documentation Index

**Complete documentation for building and deploying ForgeOS (CoatVision MVP)**

This directory contains all documentation needed to understand, deploy, and extend the ForgeOS platform.

---

## 📚 Documentation Structure

### Core Documents

#### [System Contract](./system-contract.md)
**The definitive specification** for ForgeOS platform behavior, interfaces, and guarantees.

- Service contracts for all components
- API and data contracts
- Security requirements
- Performance guarantees
- Deployment specifications
- Environment configuration

**Read this first** to understand system architecture and requirements.

---

#### [Status Document](./status.md)
**Current state** of the ForgeOS platform.

- Component status (Backend, Frontend, Mobile, Database)
- Implemented features
- Features in development
- Known issues and limitations
- Performance metrics
- Recent changes

**Check this** to understand what's working and what's not.

---

#### [Roadmap](./roadmap.md)
**Development plan** and future direction.

- Phase 1: Foundation (Q1 2026) - Current
- Phase 2: AI Enhancement (Q2 2026)
- Phase 3: Platform Maturity (Q3 2026)
- Phase 4: Scale & Optimize (Q4 2026)
- Phase 5: Ecosystem (2027+)

**Review this** to understand future plans and priorities.

---

### Legacy Documentation

These documents were created before the ForgeOS structure:

- `RENDER_BACKEND_CHECKLIST.md` - Render deployment steps
- `SUPABASE_SQL_EDITOR.md` - Supabase SQL setup guide
- `VERCEL_FRONTEND_CHECKLIST.md` - Vercel deployment steps

These are still valid but are being superseded by the new comprehensive documentation.

---

## 🔧 Technical Specifications

Located in `/specs/` directory:

### [API Contracts](../specs/api-contracts.md)
Complete REST API documentation including:
- All endpoints and methods
- Request/response formats
- Authentication requirements
- Error codes and handling
- Rate limiting
- Example usage

### [Database Contracts](../specs/db-contracts.md)
Database schema and operations:
- Table definitions
- Relationships and foreign keys
- Indexes for performance
- Row-Level Security policies
- Stored procedures and functions
- Example queries

---

## 💾 Example Payloads

Located in `/payloads/` directory:

### [01_db.sql](../payloads/01_db.sql)
**Practical database setup example**
- Complete schema creation
- Indexes and constraints
- Row-Level Security setup
- Sample data (commented)
- Verification queries

**Use this** to quickly set up your database.

### [02_edge_functions.json](../payloads/02_edge_functions.json)
**Edge function examples**
- Function definitions
- Deployment instructions
- Example handler code
- Environment variables
- Testing procedures

**Use this** to implement serverless functions.

---

## 🚀 Quick Start Guide

### 1. Understand the System
Read in this order:
1. [System Contract](./system-contract.md) - Architecture and requirements
2. [Status Document](./status.md) - Current state
3. [API Contracts](../specs/api-contracts.md) - API reference
4. [Database Contracts](../specs/db-contracts.md) - Database schema

### 2. Set Up Database
```bash
# Apply database schema
psql $DATABASE_URL < payloads/01_db.sql

# Or via Supabase SQL Editor
# Copy contents of payloads/01_db.sql and run in editor
```

### 3. Configure Environment
Create `.env` files in root and component directories:

**Backend `.env`:**
```bash
DATABASE_URL=postgresql://[user]:[pass]@[host]:[port]/[db]
SUPABASE_URL=https://[project].supabase.co
SUPABASE_SERVICE_KEY=[service-role-key]
SECRET_KEY=[generated-secret]
OPENAI_API_KEY=sk-[your-key]
```

**Frontend `.env`:**
```bash
VITE_API_URL=https://[backend-url]
VITE_SUPABASE_URL=https://[project].supabase.co
VITE_SUPABASE_ANON_KEY=[anon-key]
```

**Mobile `.env`:**
```bash
EXPO_PUBLIC_API_URL=https://[backend-url]
EXPO_PUBLIC_SUPABASE_URL=https://[project].supabase.co
EXPO_PUBLIC_SUPABASE_ANON_KEY=[anon-key]
```

### 4. Deploy Services
See deployment guides in repository root:
- `QUICK_DEPLOY.md` - Fast deployment guide
- `DEPLOYMENT.md` - Complete deployment instructions
- `DEPLOYMENT_CHECKLIST.md` - Step-by-step checklist

### 5. Verify Deployment
```bash
# Check backend health
curl https://your-backend.onrender.com/health

# Test API endpoint
curl -X GET https://your-backend.onrender.com/api/lyxbot/status \
  -H "Authorization: Bearer $TOKEN"
```

---

## 📖 Documentation Standards

### All Documentation Must:
1. ✅ Use environment variable placeholders (never hardcode secrets)
2. ✅ Include version numbers and last updated dates
3. ✅ Provide practical examples
4. ✅ Be self-contained and complete
5. ✅ Reference related documents

### Environment Variable Format:
```bash
# Good - placeholder
OPENAI_API_KEY=${OPENAI_API_KEY}
DATABASE_URL=postgresql://[user]:[pass]@[host]:[port]/[db]

# Bad - hardcoded
OPENAI_API_KEY=sk-abc123xyz
DATABASE_URL=postgresql://admin:password123@db.example.com:5432/prod
```

---

## 🎯 Single Source of Truth

This documentation serves as the **complete manual** for ForgeOS. Everything needed to:

- ✅ Understand the architecture
- ✅ Set up development environment
- ✅ Deploy to production
- ✅ Integrate APIs
- ✅ Extend functionality
- ✅ Troubleshoot issues

**No external resources or undocumented dependencies required.**

---

## 🔄 Update Process

### When to Update Documentation:
- New features are added
- APIs change
- Database schema changes
- Deployment process changes
- Issues are discovered and fixed

### How to Update:
1. Update the relevant document(s)
2. Update version number
3. Update "Last Updated" date
4. Update the Status document if status changed
5. Update the Roadmap if plans changed

### Responsibility:
- **System Contract**: Update for any breaking changes
- **Status**: Update weekly or when significant changes occur
- **Roadmap**: Review monthly, update quarterly
- **API Contracts**: Update when endpoints change
- **DB Contracts**: Update when schema changes

---

## 📞 Getting Help

### Step 1: Check Documentation
- Read System Contract for architecture questions
- Check Status Document for current state
- Review API Contracts for endpoint usage
- See Database Contracts for schema details

### Step 2: Review Examples
- Check example payloads in `/payloads/`
- Review deployment guides in repository root
- See example code in API documentation

### Step 3: Check Root Documentation
Repository root contains:
- `README.md` - Project overview and setup
- `ARCHITECTURE.md` - Architecture diagrams
- `CONTRIBUTING.md` - Contribution guidelines
- `DEPLOYMENT*.md` - Various deployment guides

### Step 4: Open an Issue
If documentation doesn't answer your question:
1. Open a GitHub issue
2. Reference which documentation you checked
3. Describe what's missing or unclear

---

## 📝 Contributing to Documentation

See `CONTRIBUTING.md` in repository root for:
- Code style guidelines
- Documentation standards
- Pull request process
- Testing requirements

---

## 🗂️ File Organization

```
CoatVision_MVP/
├── docs/                          # Documentation (you are here)
│   ├── README.md                  # This file - documentation index
│   ├── system-contract.md         # System specification
│   ├── status.md                  # Current status
│   └── roadmap.md                 # Development roadmap
├── specs/                         # Technical specifications
│   ├── api-contracts.md           # API documentation
│   └── db-contracts.md            # Database schema
├── payloads/                      # Example files
│   ├── 01_db.sql                  # Database setup
│   └── 02_edge_functions.json     # Edge functions
├── backend/                       # Backend code
├── frontend/                      # Frontend code
├── mobile/                        # Mobile app code
└── [deployment guides]            # Various deployment docs
```

---

**This is your complete manual for ForgeOS. Start with the System Contract and follow the Quick Start Guide.**

**Version:** 1.0.0  
**Last Updated:** 2026-01-03
