---
name: "API Design Patterns"
tags: ["antigravity", "api", "atomic", "c:", "common", "design", "example", "frontend", "gemini", "http", "<YOUR_USERNAME>", "method", "overview", "patterns", "quick", "reference", "rules", "templates", "url", "usage"]
tier: 3
risk: "medium"
estimated_tokens: 1637
tools_needed: ["markdown"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["web", "product"]
quality_score: 0.91
---
# API Design Patterns

> **Tier:** 2  
> **Tags:** `[api, rest, design-patterns, best-practices, http]`  
> **When to use:** Designing REST APIs, API architecture, endpoint design, HTTP best practices

---

## Overview

Expert guidance for designing clean, maintainable REST APIs. Covers resource modeling, endpoint design, error handling, versioning strategies, and common API patterns. Focuses on practical patterns that scale from MVP to production.

---

## Rules

**RULE-001: Resources Over Actions in URLs**
URLs should represent resources (nouns), not actions (verbs). Use HTTP methods to indicate actions. This makes APIs predictable and RESTful.

```http
❌ Bad: POST /api/createUser
❌ Bad: GET /api/getUserById/123
✅ Good: POST /api/users
✅ Good: GET /api/users/123
```

**RULE-002: Use Plural Nouns for Collections**
Always use plural nouns for resource collections, even when retrieving a single item. This creates consistency across your API.

```http
✅ Good: GET /api/users (list)
✅ Good: GET /api/users/123 (single)
✅ Good: POST /api/users (create)
❌ Bad: GET /api/user/123
```

**RULE-003: Nest Resources for Relationships**
Use nested URLs to represent relationships, but limit nesting to 2 levels maximum to avoid complexity.

```http
✅ Good: GET /api/users/123/posts
✅ Good: GET /api/posts/456/comments
❌ Bad: GET /api/users/123/posts/456/comments/789/likes
     (too deep - use /api/comments/789/likes instead)
```

**RULE-004: Use HTTP Status Codes Correctly**
Return appropriate status codes to indicate success, client errors, and server errors. Don't return 200 OK for everything.

```http
200 OK - Successful GET, PUT, PATCH
201 Created - Successful POST
204 No Content - Successful DELETE
400 Bad Request - Invalid input
401 Unauthorized - Missing/invalid auth
403 Forbidden - Valid auth but insufficient permissions
404 Not Found - Resource doesn't exist
422 Unprocessable Entity - Validation failed
500 Internal Server Error - Server-side error
```

**RULE-005: Return Consistent Error Responses**
Use a standard error format across all endpoints. Include error code, message, and optional details.

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid email format",
    "details": {
      "field": "email",
      "value": "not-an-email"
    }
  }
}
```

**RULE-006: Version Your API from Day One**
Include version in URL or header. URL versioning is simpler and more visible. Increment major version for breaking changes only.

```http
✅ Good: GET /api/v1/users
✅ Good: GET /api/v2/users (breaking change)
❌ Bad: GET /api/users (no version)
```

**RULE-007: Use Query Parameters for Filtering and Pagination**
Keep URLs clean by using query parameters for optional operations like filtering, sorting, and pagination.

```http
GET /api/users?status=active&sort=created_at&page=2&limit=20
GET /api/posts?author=123&published=true
```

**RULE-008: Support Partial Updates with PATCH**
Use PATCH for partial updates (only changed fields) and PUT for full replacement. This reduces payload size and prevents accidental data loss.

```http
PATCH /api/users/123
{
  "email": "new@example.com"  // Only update email
}

PUT /api/users/123
{
  "name": "John",
  "email": "new@example.com",
  "status": "active"  // Must include all fields
}
```

**RULE-009: Include Metadata in List Responses**
When returning collections, include pagination metadata to help clients navigate results.

```json
{
  "data": [...],
  "meta": {
    "page": 2,
    "limit": 20,
    "total": 157,
    "total_pages": 8
  }
}
```

**RULE-010: Design for Idempotency**
GET, PUT, DELETE should be idempotent (same result when called multiple times). POST creates new resources each time. Use idempotency keys for critical POST operations.

```http
POST /api/payments
Headers: Idempotency-Key: unique-key-123

// Calling twice with same key = same payment, not duplicate
```

---

## Quick Reference

### HTTP Method Usage

| Method | Purpose | Idempotent | Safe | Request Body | Response Body |
|--------|---------|------------|------|--------------|---------------|
| GET | Retrieve resource(s) | Yes | Yes | No | Yes |
| POST | Create new resource | No | No | Yes | Yes (created resource) |
| PUT | Replace entire resource | Yes | No | Yes | Yes (updated resource) |
| PATCH | Update partial resource | No* | No | Yes | Yes (updated resource) |
| DELETE | Remove resource | Yes | No | No | Optional |

*PATCH can be designed to be idempotent

### Common URL Patterns

| Pattern | Example | Use Case |
|---------|---------|----------|
| Collection | `GET /api/users` | List all users |
| Single Resource | `GET /api/users/123` | Get specific user |
| Nested Resource | `GET /api/users/123/posts` | Get user's posts |
| Action (rare) | `POST /api/users/123/verify` | Trigger action |
| Search | `GET /api/search?q=term` | Search across types |

### Status Code Decision Tree

```
Request successful?
├─ Yes → Resource returned?
│   ├─ Yes → 200 OK
│   └─ No → 204 No Content
└─ No → Client error?
    ├─ Yes → Auth issue?
    │   ├─ Missing auth → 401 Unauthorized
    │   ├─ Insufficient permissions → 403 Forbidden
    │   └─ Other → Validation failed?
    │       ├─ Yes → 422 Unprocessable Entity
    │       └─ No → 400 Bad Request
    └─ No → 500 Internal Server Error
```

### Pagination Strategies

**Offset-based (simple):**
```http
GET /api/users?page=2&limit=20
```
- Pros: Simple, familiar
- Cons: Inconsistent with real-time data, slow for large offsets

**Cursor-based (recommended):**
```http
GET /api/users?cursor=eyJpZCI6MTIzfQ&limit=20
```
- Pros: Consistent results, fast for any position
- Cons: Can't jump to arbitrary page

**Keyset-based (best for sorted data):**
```http
GET /api/users?after_id=123&limit=20
```
- Pros: Fast, consistent, simple
- Cons: Only works with sortable unique keys

### Common API Patterns

**Bulk Operations:**
```http
POST /api/users/bulk
{
  "operations": [
    {"action": "create", "data": {...}},
    {"action": "update", "id": 123, "data": {...}},
    {"action": "delete", "id": 456}
  ]
}
```

**Batch Requests:**
```http
POST /api/batch
{
  "requests": [
    {"method": "GET", "url": "/api/users/123"},
    {"method": "GET", "url": "/api/posts/456"}
  ]
}
```

**Webhooks:**
```http
POST /api/webhooks
{
  "url": "https://example.com/webhook",
  "events": ["user.created", "user.updated"]
}
```

---

## Metadata

- **Related Skills:** backend-patterns.md, database-design.md, authentication.md
- **Dependencies:** None
- **Version:** 1.0.0
- **Last Updated:** 2024-03-26

