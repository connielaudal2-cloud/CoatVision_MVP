# API Contracts - ForgeOS Platform

**Version:** 1.0.0  
**Last Updated:** 2026-01-03  
**Base URL:** `${API_URL}/api/`

---

## Overview

This document defines the API contracts for the ForgeOS platform. All endpoints follow REST principles and use JSON for request/response bodies unless otherwise specified.

## Authentication

### Bearer Token Authentication
All endpoints except `/health` require authentication via JWT tokens issued by Supabase Auth.

```http
Authorization: Bearer <jwt_token>
```

### Token Lifecycle
- **Access Token**: 1 hour lifetime
- **Refresh Token**: 30 days lifetime
- **Renewal**: Use Supabase Auth client to refresh

---

## Global Response Codes

| Code | Meaning | Description |
|------|---------|-------------|
| 200 | OK | Request successful |
| 201 | Created | Resource created successfully |
| 400 | Bad Request | Invalid request parameters |
| 401 | Unauthorized | Missing or invalid authentication |
| 403 | Forbidden | Insufficient permissions |
| 404 | Not Found | Resource not found |
| 422 | Unprocessable Entity | Validation error |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Internal Server Error | Server error |
| 503 | Service Unavailable | Service temporarily unavailable |

---

## Error Response Format

All error responses follow this structure:

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": {
      "field": "Additional context"
    }
  }
}
```

### Common Error Codes
- `AUTHENTICATION_REQUIRED`: Missing or invalid token
- `INVALID_REQUEST`: Malformed request body
- `VALIDATION_ERROR`: Input validation failed
- `RESOURCE_NOT_FOUND`: Requested resource doesn't exist
- `RATE_LIMIT_EXCEEDED`: Too many requests
- `INTERNAL_ERROR`: Server error

---

## Health & Status Endpoints

### GET /health
Health check endpoint (no authentication required).

**Response: 200 OK**
```json
{
  "status": "healthy",
  "timestamp": "2026-01-03T12:00:00Z",
  "version": "0.1.0",
  "services": {
    "database": "connected",
    "storage": "available"
  }
}
```

### GET /
Root endpoint returning API information.

**Response: 200 OK**
```json
{
  "name": "CoatVision Core",
  "version": "0.1.0",
  "docs": "/docs",
  "health": "/health"
}
```

---

## Analysis Endpoints

### POST /api/analyze/
Analyze an uploaded image for coating quality.

**Authentication**: Required

**Request: multipart/form-data**
```
file: <binary image data>
```

**Supported Formats**:
- JPEG (.jpg, .jpeg)
- PNG (.png)
- WebP (.webp)

**File Size Limit**: 50MB

**Response: 200 OK**
```json
{
  "analysis_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "completed",
  "filename": "image.jpg",
  "output_filename": "image_analyzed.jpg",
  "metrics": {
    "cvi": 0.85,
    "cqi": 0.78,
    "coverage_percent": 82.5,
    "edge_coverage_ratio": 0.75,
    "defects_detected": 3,
    "severity": "medium"
  },
  "output_url": "https://storage.example.com/outputs/abc123.jpg",
  "created_at": "2026-01-03T12:00:00Z"
}
```

**Errors**:
- `400`: Invalid file format or size
- `422`: Image processing error
- `500`: Analysis failure

---

### POST /api/analyze/base64
Analyze a base64-encoded image.

**Authentication**: Required

**Request: application/json**
```json
{
  "image": "data:image/jpeg;base64,/9j/4AAQSkZJRg...",
  "options": {
    "sensitivity": "high",
    "include_visualization": true
  }
}
```

**Options**:
- `sensitivity`: `"low"` | `"medium"` | `"high"` (default: `"medium"`)
- `include_visualization`: boolean (default: `true`)

**Response**: Same as `POST /api/analyze/`

---

### GET /api/analyze/{analysis_id}
Retrieve a specific analysis result.

**Authentication**: Required

**Parameters**:
- `analysis_id`: UUID of the analysis

**Response: 200 OK**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "created_at": "2026-01-03T12:00:00Z",
  "filename": "image.jpg",
  "output_filename": "image_analyzed.jpg",
  "metrics": {
    "cvi": 0.85,
    "cqi": 0.78,
    "coverage_percent": 82.5
  },
  "status": "completed",
  "user_id": "user-uuid",
  "job_id": "job-uuid"
}
```

**Errors**:
- `404`: Analysis not found

---

### GET /api/analyze/
List all analyses for the authenticated user.

**Authentication**: Required

**Query Parameters**:
- `limit`: Integer (default: 20, max: 100)
- `offset`: Integer (default: 0)
- `status`: Filter by status (`completed`, `failed`, `processing`)
- `from_date`: ISO 8601 date (filter from date)
- `to_date`: ISO 8601 date (filter to date)

**Response: 200 OK**
```json
{
  "analyses": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "filename": "image.jpg",
      "created_at": "2026-01-03T12:00:00Z",
      "status": "completed",
      "metrics": {
        "cvi": 0.85
      }
    }
  ],
  "total": 42,
  "limit": 20,
  "offset": 0
}
```

---

## Report Endpoints

### POST /api/reports/
Generate a PDF report for an analysis.

**Authentication**: Required

**Request: application/json**
```json
{
  "analysis_id": "550e8400-e29b-41d4-a716-446655440000",
  "template": "standard",
  "options": {
    "include_images": true,
    "include_recommendations": true
  }
}
```

**Templates**:
- `standard`: Standard report format
- `detailed`: Detailed analysis report
- `summary`: Executive summary

**Response: 201 Created**
```json
{
  "report_id": "650e8400-e29b-41d4-a716-446655440000",
  "analysis_id": "550e8400-e29b-41d4-a716-446655440000",
  "url": "https://storage.example.com/reports/report-123.pdf",
  "created_at": "2026-01-03T12:00:00Z",
  "metadata": {
    "pages": 5,
    "size_bytes": 245760
  }
}
```

---

### GET /api/reports/{report_id}
Retrieve a specific report.

**Authentication**: Required

**Response: 200 OK**
```json
{
  "id": "650e8400-e29b-41d4-a716-446655440000",
  "analysis_id": "550e8400-e29b-41d4-a716-446655440000",
  "url": "https://storage.example.com/reports/report-123.pdf",
  "created_at": "2026-01-03T12:00:00Z",
  "metadata": {
    "pages": 5,
    "size_bytes": 245760
  }
}
```

---

### GET /api/reports/
List all reports for the authenticated user.

**Authentication**: Required

**Query Parameters**: Same as analysis list

**Response: 200 OK**
```json
{
  "reports": [
    {
      "id": "650e8400-e29b-41d4-a716-446655440000",
      "analysis_id": "550e8400-e29b-41d4-a716-446655440000",
      "url": "https://storage.example.com/reports/report-123.pdf",
      "created_at": "2026-01-03T12:00:00Z"
    }
  ],
  "total": 15,
  "limit": 20,
  "offset": 0
}
```

---

## Job Endpoints

### POST /api/jobs/
Create a new asynchronous job.

**Authentication**: Required

**Request: application/json**
```json
{
  "type": "batch_analysis",
  "params": {
    "image_ids": ["id1", "id2", "id3"],
    "options": {}
  }
}
```

**Job Types**:
- `batch_analysis`: Process multiple images
- `model_training`: Train custom ML model
- `report_generation`: Generate multiple reports

**Response: 201 Created**
```json
{
  "job_id": "750e8400-e29b-41d4-a716-446655440000",
  "status": "pending",
  "created_at": "2026-01-03T12:00:00Z",
  "params": {}
}
```

---

### GET /api/jobs/{job_id}
Get job status and results.

**Authentication**: Required

**Response: 200 OK**
```json
{
  "id": "750e8400-e29b-41d4-a716-446655440000",
  "status": "completed",
  "created_at": "2026-01-03T12:00:00Z",
  "completed_at": "2026-01-03T12:05:00Z",
  "params": {},
  "results": {
    "processed": 3,
    "successful": 3,
    "failed": 0,
    "outputs": ["id1", "id2", "id3"]
  }
}
```

**Job Statuses**:
- `pending`: Queued for processing
- `running`: Currently processing
- `completed`: Successfully completed
- `failed`: Processing failed
- `cancelled`: Cancelled by user

---

## LYXbot Agent Endpoints

### GET /api/lyxbot/status
Get LYXbot agent status.

**Authentication**: Required

**Response: 200 OK**
```json
{
  "status": "online",
  "version": "0.1.0",
  "capabilities": [
    "image_analysis",
    "recommendations",
    "reporting"
  ],
  "uptime_seconds": 86400
}
```

---

### POST /api/lyxbot/command
Send a command to LYXbot agent.

**Authentication**: Required

**Request: application/json**
```json
{
  "command": "analyze recent images",
  "context": {
    "user_id": "user-uuid",
    "conversation_id": "conv-uuid"
  }
}
```

**Response: 200 OK**
```json
{
  "status": "received",
  "command": "analyze recent images",
  "response": "I found 5 recent images. Would you like me to analyze them?",
  "actions": [
    {
      "type": "analysis_batch",
      "image_ids": ["id1", "id2", "id3", "id4", "id5"]
    }
  ]
}
```

**Note**: Currently returns placeholder responses. Full implementation pending.

---

## Training Endpoints

### POST /api/training/
Create a new training session.

**Authentication**: Required (admin role)

**Request: application/json**
```json
{
  "notes": "Training session for defect detection",
  "data": {
    "images": ["id1", "id2"],
    "labels": ["good", "defect"]
  }
}
```

**Response: 201 Created**
```json
{
  "session_id": "850e8400-e29b-41d4-a716-446655440000",
  "created_at": "2026-01-03T12:00:00Z",
  "notes": "Training session for defect detection"
}
```

---

## Rate Limiting

**Current Limits** (subject to change):
- **Authenticated**: 1000 requests/hour per user
- **Analysis Endpoints**: 100 requests/hour per user
- **Health Check**: Unlimited

**Rate Limit Headers**:
```http
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1704283200
```

**Rate Limit Exceeded Response: 429**
```json
{
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Too many requests. Please try again later.",
    "details": {
      "retry_after": 3600
    }
  }
}
```

---

## Webhooks (Future)

### Event Types (Planned)
- `analysis.completed`: Analysis finished
- `analysis.failed`: Analysis failed
- `report.generated`: Report ready
- `job.completed`: Async job finished

### Webhook Payload Format (Planned)
```json
{
  "event": "analysis.completed",
  "timestamp": "2026-01-03T12:00:00Z",
  "data": {
    "analysis_id": "550e8400-e29b-41d4-a716-446655440000",
    "status": "completed"
  }
}
```

---

## Pagination

All list endpoints support pagination with:
- `limit`: Items per page (default: 20, max: 100)
- `offset`: Number of items to skip (default: 0)

Response includes:
```json
{
  "items": [...],
  "total": 100,
  "limit": 20,
  "offset": 0,
  "has_more": true
}
```

---

## Filtering and Sorting

List endpoints support:
- **Filtering**: Query parameters (e.g., `status=completed`)
- **Sorting**: `sort` parameter (e.g., `sort=-created_at` for descending)
- **Date Range**: `from_date` and `to_date` (ISO 8601 format)

---

## CORS Policy

**Allowed Origins**: Configured via environment variable
**Allowed Methods**: GET, POST, PUT, DELETE, OPTIONS
**Allowed Headers**: Authorization, Content-Type
**Max Age**: 86400 seconds

---

## Versioning

**Current Version**: v1 (implicit in path)
**Future Versions**: Will use `/api/v2/` prefix
**Deprecation Policy**: 6 months notice before removal

---

## OpenAPI Specification

Full OpenAPI 3.1 specification available at:
- Development: `http://localhost:8000/docs`
- Production: `${API_URL}/docs`

Interactive documentation (Swagger UI): `${API_URL}/docs`
ReDoc alternative: `${API_URL}/redoc`

---

## Examples

### Complete Analysis Flow

```bash
# 1. Upload and analyze image
curl -X POST ${API_URL}/api/analyze/ \
  -H "Authorization: Bearer ${TOKEN}" \
  -F "file=@coating-sample.jpg"

# Response: {"analysis_id": "abc-123", "status": "completed", ...}

# 2. Generate report
curl -X POST ${API_URL}/api/reports/ \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"analysis_id": "abc-123", "template": "standard"}'

# Response: {"report_id": "def-456", "url": "https://...", ...}

# 3. Download report
curl -O -H "Authorization: Bearer ${TOKEN}" \
  "https://storage.example.com/reports/report-123.pdf"
```

---

## Client SDKs (Future)

Planned SDKs:
- **Python**: `pip install forgeos-sdk`
- **JavaScript**: `npm install @forgeos/sdk`
- **Go**: `go get github.com/forgeos/sdk-go`

---

For implementation details, see:
- Database Contracts: `/specs/db-contracts.md`
- System Contract: `/docs/system-contract.md`
- Example Payloads: `/payloads/`
