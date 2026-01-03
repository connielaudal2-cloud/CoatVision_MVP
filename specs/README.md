# Technical Specifications

**API and Database contracts for ForgeOS platform**

---

## Overview

This directory contains detailed technical specifications and contracts for the ForgeOS platform. These documents define the exact interfaces, data structures, and behaviors that all components must adhere to.

---

## 📄 Documents

### [API Contracts](./api-contracts.md)
**Complete REST API specification**

#### Contents:
- Authentication and authorization
- All API endpoints with full documentation
- Request/response formats
- Error handling and codes
- Rate limiting policies
- Pagination and filtering
- WebHooks (planned)
- Example usage for all endpoints

#### Use Cases:
- Frontend/mobile developers integrating with the API
- Third-party developers building integrations
- Testing and validation
- API versioning and deprecation tracking

**When to update**: Any time API endpoints change, new endpoints are added, or response formats change.

---

### [Database Contracts](./db-contracts.md)
**Complete database schema and operations**

#### Contents:
- PostgreSQL schema definition
- All tables with full column specifications
- Indexes for performance optimization
- Foreign key relationships
- Row-Level Security (RLS) policies
- Stored procedures and functions
- Views for common queries
- Migration strategy
- Backup and recovery procedures

#### Use Cases:
- Database administrators setting up new instances
- Backend developers querying the database
- Understanding data relationships
- Performance optimization
- Security policy implementation

**When to update**: Any time database schema changes, new tables are added, or RLS policies are modified.

---

## 🎯 Contract Philosophy

### What is a Contract?

A **contract** is a formal agreement about how a component behaves:
- **Input requirements**: What you must provide
- **Output guarantees**: What you will receive
- **Error conditions**: When and how it fails
- **Performance expectations**: How fast it should be

### Why Contracts Matter

1. **Predictability**: Know exactly what to expect
2. **Independence**: Components can be developed separately
3. **Testing**: Clear expectations make testing easier
4. **Documentation**: Serves as authoritative reference
5. **Versioning**: Track changes over time

### Contract Rules

All contracts in this directory must:
- ✅ Be complete and unambiguous
- ✅ Use concrete examples
- ✅ Define error conditions
- ✅ Specify data types and formats
- ✅ Include performance expectations
- ✅ Use environment variable placeholders for secrets

---

## 🔗 Relationship to Other Documentation

```
System Contract (/docs/system-contract.md)
    │
    ├─ Defines WHAT the system does
    │
    └─► API Contracts (./api-contracts.md)
        └─ Defines HOW to call the API
    
    └─► Database Contracts (./db-contracts.md)
        └─ Defines HOW data is stored
```

### Read Order:
1. **System Contract** (`/docs/system-contract.md`) - High-level architecture
2. **API Contracts** (`./api-contracts.md`) - How to interact with the API
3. **Database Contracts** (`./db-contracts.md`) - How data is structured

---

## 📚 Quick Reference

### API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/health` | GET | Health check |
| `/api/analyze/` | POST | Upload and analyze image |
| `/api/analyze/base64` | POST | Analyze base64 image |
| `/api/reports/` | POST | Generate report |
| `/api/jobs/` | POST | Create async job |
| `/api/lyxbot/status` | GET | LYXbot agent status |
| `/api/lyxbot/command` | POST | Send command to LYXbot |

See [API Contracts](./api-contracts.md) for complete documentation.

### Database Tables

| Table | Purpose |
|-------|---------|
| `analyses` | Image analysis results and metrics |
| `jobs` | Asynchronous job tracking |
| `reports` | Generated report metadata |
| `training_sessions` | AI training data and metrics |

See [Database Contracts](./db-contracts.md) for complete schema.

---

## 🛠️ Using the Contracts

### For Backend Development

**API Implementation**:
```python
# Backend must implement exactly what API contract specifies
@router.post("/api/analyze/")
async def analyze_image(file: UploadFile):
    # Must return format specified in api-contracts.md
    return {
        "analysis_id": str(uuid.uuid4()),
        "status": "completed",
        "metrics": {...}
    }
```

**Database Access**:
```python
# Use schema defined in db-contracts.md
result = await supabase.table('analyses').insert({
    'filename': filename,
    'metrics': metrics,
    'user_id': user_id
}).execute()
```

### For Frontend Development

**API Calls**:
```typescript
// Call API as documented in api-contracts.md
const response = await fetch(`${API_URL}/api/analyze/`, {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${token}`
  },
  body: formData
});
```

### For Testing

**Contract Testing**:
```python
# Verify API returns format specified in contract
def test_analyze_endpoint():
    response = client.post("/api/analyze/", files={"file": image})
    assert response.status_code == 200
    assert "analysis_id" in response.json()
    assert "metrics" in response.json()
```

---

## 🔄 Versioning

### Current Version: 1.0.0

### Version Policy:
- **Major version** (1.x.x → 2.x.x): Breaking changes to API or schema
- **Minor version** (x.1.x → x.2.x): New endpoints or tables (backward compatible)
- **Patch version** (x.x.1 → x.x.2): Documentation updates, clarifications

### Breaking Changes:
When breaking changes are necessary:
1. Increment major version
2. Maintain old version for 6 months
3. Update all documentation
4. Notify all consumers
5. Provide migration guide

### Change Log:
Track in each contract document under "Version History" section.

---

## 📋 Validation

### API Contract Validation
- OpenAPI 3.1 specification compliance
- Automated tests for all endpoints
- Response format validation
- Error code verification

### Database Contract Validation
- SQL syntax validation
- Foreign key integrity
- RLS policy testing
- Performance benchmarking

---

## 🔒 Security

### API Security Requirements:
- JWT authentication on all endpoints (except `/health`)
- TLS 1.3 for all communications
- Input validation on all parameters
- Rate limiting on all endpoints
- CORS policy enforcement

### Database Security Requirements:
- Row-Level Security enabled on all tables
- Encrypted connections required
- Service role key for backend only
- Anon key for client applications
- No secrets in schema files

---

## 📈 Performance Standards

### API Performance:
- Health check: < 100ms
- Non-analysis endpoints: < 500ms
- Image analysis: < 5 seconds
- Report generation: < 10 seconds

### Database Performance:
- Simple queries: < 50ms
- Complex queries: < 200ms
- Write operations: < 100ms
- Indexed lookups: < 10ms

---

## 🧪 Testing

### API Testing:
```bash
# Test against contract
pytest backend/tests/test_api_contracts.py -v

# Load testing
locust -f tests/loadtest.py --host $API_URL
```

### Database Testing:
```bash
# Validate schema
psql $DATABASE_URL < tests/validate_schema.sql

# Test RLS policies
psql $DATABASE_URL < tests/test_rls.sql
```

---

## 📞 Support

### Questions about API Contracts:
- Check the [API Contracts](./api-contracts.md) document first
- Review examples in `/payloads/02_edge_functions.json`
- See system-level context in `/docs/system-contract.md`

### Questions about Database Contracts:
- Check the [Database Contracts](./db-contracts.md) document first
- Review schema example in `/payloads/01_db.sql`
- See system-level context in `/docs/system-contract.md`

### Reporting Issues:
If you find discrepancies between:
- Contract documentation and actual implementation
- Examples and specifications
- Current behavior and expected behavior

Please open a GitHub issue with:
1. Which contract is affected
2. What the contract says
3. What actually happens
4. Proposed fix

---

## ✅ Checklist for New Features

When adding new features, update contracts:

### API Changes:
- [ ] Update endpoint documentation in `api-contracts.md`
- [ ] Add request/response examples
- [ ] Document error cases
- [ ] Update version number
- [ ] Add to API quick reference
- [ ] Update OpenAPI spec if exists

### Database Changes:
- [ ] Update table definitions in `db-contracts.md`
- [ ] Add migration SQL
- [ ] Update indexes if needed
- [ ] Update RLS policies if needed
- [ ] Document in quick reference
- [ ] Update example in `/payloads/01_db.sql`

---

**These contracts are binding. All implementations must conform to these specifications.**

**Version:** 1.0.0  
**Last Updated:** 2026-01-03
