---
name: "backend-patterns"
tags: ["antigravity", "api", "architecture", "backend", "based", "c:", "core", "database", "design", "dev", "development", "error", "frontend", "gemini", "handling", "layered", "<YOUR_USERNAME>", "optimization", "patterns", "resource"]
tier: 2
risk: "medium"
estimated_tokens: 479
tools_needed: ["markdown"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["web", "product"]
quality_score: 0.66
description: "Backend architecture patterns, API design, database optimization, and server-side best practices for Node.js, Express, and Next.js."
---
# Backend Development Patterns (v6.5.0-SLIM)

Architecture patterns and best practices for scalable server-side applications.

## API Design Patterns

### 1. Resource-Based REST
- Use nouns for resources: `/api/markets`, not `/api/getMarkets`.
- Use HTTP verbs: GET (fetch), POST (create), PATCH (update), DELETE.
- Filter/Sort via query params: `/api/markets?status=active&limit=10`.

### 2. Layered Architecture
- **Repository Pattern:** Abstract data access logic (e.g., Supabase, Prisma).
- **Service Layer:** House business logic separate from delivery mechanisms.
- **Middleware:** Request/response processing pipeline (Auth, Logging, Validation).

## Database Optimization
- **Column Selection:** Only select needed columns. Avoid `SELECT *`.
- **N+1 Prevention:** Use batch fetching or joins instead of looping over queries.
- **Transactions:** Use for multi-step operations to ensure data integrity.

## Error Handling
- **Centralized Handler:** Use custom `ApiError` classes and a global catch-all.
- **Retries:** Implement exponential backoff for external API calls.
- **Validation:** Use Zod or Pydantic for strict request/response body validation.

## Auth & Security
- **JWT:** Use signed tokens for stateless authentication.
- **RBAC:** Implement Role-Based Access Control at the middleware or service level.
- **Rate Limiting:** Protect endpoints with IP-based or user-based limits.

## Background Processing
- **Job Queues:** Offload heavy tasks (email, indexing) to a background worker.
- **Status Polling:** Return a job ID and have the client poll for completion.

## Monitoring
- **Structured Logging:** Use JSON logs with context (requestId, userId, method).
- **Performance:** Log slow queries and API response times.
