# ForgeOS System Contract

**Version:** 1.0.0  
**Last Updated:** 2026-01-03  
**Status:** Active

---

## Purpose

This document defines the system contract for ForgeOS, the AI-powered coating analysis platform. It serves as the authoritative specification for system behavior, interfaces, and guarantees.

## System Overview

ForgeOS is a distributed application platform consisting of:
- **Backend API**: FastAPI-based REST service
- **Web Dashboard**: React-based administrative interface
- **Mobile Application**: React Native field application
- **Database**: PostgreSQL with Supabase extensions
- **AI Services**: OpenAI GPT-4 Vision integration

## Service Contracts

### Backend API Service

#### Responsibilities
- Process image uploads and analysis requests
- Execute AI-powered coating quality assessments
- Generate and serve PDF reports
- Manage user authentication and authorization
- Persist analysis data and metadata

#### Interface Contract
- **Protocol**: HTTP/HTTPS REST
- **Base Path**: `/api/`
- **Authentication**: Bearer token (JWT)
- **Content Types**: `application/json`, `multipart/form-data`
- **API Version**: v1 (implicit in path)

#### Endpoint Categories
- **Health**: `/health` - Service health check
- **Analysis**: `/api/analyze/` - Image analysis operations
- **Reports**: `/api/reports/` - Report generation and retrieval
- **Jobs**: `/api/jobs/` - Asynchronous job management
- **LYXbot**: `/api/lyxbot/` - AI agent interactions
- **Auth**: Handled via Supabase Auth

#### Performance Guarantees
- **Health Check**: < 100ms response time
- **Image Analysis**: < 5 seconds for standard images (< 10MB)
- **Report Generation**: < 10 seconds
- **API Endpoints**: < 500ms for non-processing operations

#### Availability
- **Target SLA**: 99.5% uptime
- **Monitoring**: Health endpoint polled every 30 seconds
- **Failover**: Automatic restart on failure
- **Graceful Degradation**: Read-only mode if database unavailable

### Web Dashboard Service

#### Responsibilities
- Provide web-based user interface
- Display analysis results and reports
- Manage user workflows
- Administrative functions

#### Interface Contract
- **Protocol**: HTTPS
- **Technology**: Single Page Application (SPA)
- **Build Output**: Static assets
- **API Integration**: Via `VITE_API_URL` environment variable

#### Browser Support
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

### Mobile Application Service

#### Responsibilities
- Image capture from device camera
- Upload images for analysis
- Display analysis results
- Offline data persistence (future)

#### Interface Contract
- **Platform**: iOS 13+, Android 8+
- **Framework**: React Native with Expo
- **API Integration**: Via `EXPO_PUBLIC_API_URL` environment variable

### Database Service

#### Responsibilities
- Persist analysis data and metadata
- Store user authentication data
- Manage file references
- Provide real-time subscriptions

#### Interface Contract
- **Protocol**: PostgreSQL wire protocol
- **Extensions**: pgcrypto, uuid-ossp
- **Authentication**: Connection string with credentials
- **Row-Level Security**: Enabled on all tables

#### Schema Contract
See `/specs/db-contracts.md` for detailed schema.

Key tables:
- `analyses` - Analysis records and metrics
- `jobs` - Asynchronous job tracking
- `reports` - Generated report metadata
- `training_sessions` - AI training data

## Data Contracts

### Image Analysis Request
```json
{
  "file": "binary data or base64 string",
  "options": {
    "sensitivity": "high|medium|low",
    "output_format": "json|pdf"
  }
}
```

### Image Analysis Response
```json
{
  "analysis_id": "uuid",
  "status": "completed|failed",
  "metrics": {
    "cvi": 0.0-1.0,
    "cqi": 0.0-1.0,
    "coverage_percent": 0.0-100.0,
    "edge_coverage_ratio": 0.0-1.0
  },
  "output_url": "string",
  "created_at": "ISO 8601 timestamp"
}
```

### Error Response
```json
{
  "error": {
    "code": "string",
    "message": "string",
    "details": {}
  }
}
```

## Security Contract

### Authentication
- **Method**: JWT tokens issued by Supabase Auth
- **Token Lifetime**: 1 hour (access token), 30 days (refresh token)
- **Token Delivery**: `Authorization: Bearer <token>` header
- **Anonymous Access**: Health endpoint only

### Authorization
- **User Roles**: Authenticated users can access their own data
- **Row-Level Security**: Enforced at database level
- **Service Role**: Backend uses service role key for admin operations

### Data Protection
- **Transport**: TLS 1.3 required for all communications
- **At Rest**: Database encrypted by hosting provider
- **Secrets**: Stored in environment variables, never in code
- **PII**: Handled according to GDPR requirements (if applicable)

### Input Validation
- **File Size**: Max 50MB per image upload
- **File Types**: JPEG, PNG, WebP only
- **SQL Injection**: Parameterized queries only
- **XSS Protection**: Input sanitization on frontend
- **CSRF Protection**: Token-based

## Environment Configuration Contract

### Required Environment Variables

All deployments must provide:

#### Backend
```bash
DATABASE_URL=postgresql://[user]:[password]@[host]:[port]/[database]
SUPABASE_URL=https://[project-id].supabase.co
SUPABASE_SERVICE_KEY=[service-role-key]
SECRET_KEY=[generated-secret]
OPENAI_API_KEY=sk-[api-key]  # When AI features enabled
```

#### Frontend
```bash
VITE_API_URL=https://[backend-url]
VITE_SUPABASE_URL=https://[project-id].supabase.co
VITE_SUPABASE_ANON_KEY=[anon-public-key]
```

#### Mobile
```bash
EXPO_PUBLIC_API_URL=https://[backend-url]
EXPO_PUBLIC_SUPABASE_URL=https://[project-id].supabase.co
EXPO_PUBLIC_SUPABASE_ANON_KEY=[anon-public-key]
```

### Optional Environment Variables
```bash
NODE_ENV=development|production
LOG_LEVEL=DEBUG|INFO|WARNING|ERROR
SENTRY_DSN=[sentry-dsn]
API_PORT=8000
```

## Deployment Contract

### Build Requirements
- **Backend**: Python 3.10+ with pip
- **Frontend**: Node.js 18+ with npm
- **Mobile**: Node.js 18+ with npm and Expo CLI
- **Database**: PostgreSQL 15+

### Build Commands
```bash
# Backend
cd backend && pip install -r requirements.txt

# Frontend
cd frontend && npm ci && npm run build

# Mobile
cd mobile && npm ci
```

### Start Commands
```bash
# Backend
uvicorn main:app --host 0.0.0.0 --port $PORT

# Frontend (production)
# Serve static files from ./dist

# Mobile
expo start
```

### Health Checks
- **Endpoint**: `GET /health`
- **Expected Response**: `200 OK` with `{"status": "healthy"}`
- **Timeout**: 5 seconds

## Versioning and Changes

### API Versioning
- **Current Version**: v1 (implicit)
- **Breaking Changes**: Will introduce v2 path prefix
- **Deprecation**: 6 months notice before removal

### Schema Versioning
- **Migration Strategy**: Forward-only migrations
- **Rollback**: Via database backups
- **Tools**: Supabase migrations or manual SQL scripts

### Contract Changes
- **Minor Changes**: Additive only, no breaking changes
- **Major Changes**: New version number, deprecation period
- **Communication**: Update this document and notify stakeholders

## Support and Maintenance

### Monitoring
- Health check endpoint at `/health`
- Application logs to stdout/stderr
- Error tracking via Sentry (if configured)

### Backup and Recovery
- **Database**: Automated daily backups by Supabase
- **Files**: Stored in Supabase Storage with replication
- **Recovery Time Objective**: 24 hours
- **Recovery Point Objective**: 24 hours

### Updates
- **Security Patches**: Applied within 7 days
- **Feature Updates**: Monthly release cycle
- **Breaking Changes**: Quarterly with deprecation period

## Compliance

### Standards
- REST API design principles
- OpenAPI 3.1 specification
- JSON RFC 8259
- JWT RFC 7519

### Accessibility
- WCAG 2.1 Level AA for web interface (target)
- Mobile accessibility guidelines

## Testing Contract

### Unit Tests
- Backend: pytest with >80% coverage target
- Frontend: Vitest/Jest with >70% coverage target

### Integration Tests
- API endpoint tests
- Database integration tests
- End-to-end user flows

### Performance Tests
- Load testing for concurrent users
- Stress testing for peak loads
- Analysis time benchmarks

## Documentation

### Required Documentation
- API documentation (OpenAPI spec)
- Database schema (ERD and SQL)
- Deployment guides
- User guides

### Documentation Locations
- System contract: `/docs/system-contract.md`
- API contracts: `/specs/api-contracts.md`
- DB contracts: `/specs/db-contracts.md`
- Examples: `/payloads/`

---

**This system contract is binding for all ForgeOS components and must be maintained with any system changes.**
