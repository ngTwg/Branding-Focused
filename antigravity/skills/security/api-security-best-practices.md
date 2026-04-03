---
name: "🛡️ Skill: API Security Best Practices"
tags: ["activation", "antigravity", "api", "benchmark", "best", "c:", "execution", "frontend", "gemini", "<YOUR_USERNAME>", "output", "pipeline", "practices", "security", "signals", "signature", "skill", "steps", "sub", "task"]
tier: 3
risk: "medium"
estimated_tokens: 365
tools_needed: ["markdown", "sql", "terminal"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["web", "product"]
quality_score: 0.58
---
# 🛡️ Skill: API Security Best Practices

> **PURPOSE:** Implement secure API design patterns (Auth, Validation, Rate Limiting).
> **CATEGORY:** Security
> **TIER:** 2+

---

## 🚦 ACTIVATION SIGNALS

- Keywords: `secure API`, `JWT auth`, `input validation`, `rate limiting`.
- Task: Designing new endpoints, securing existing APIs, or preparing for security audits.

---

## ✅ OWASP API TOP 10 CHECKLIST (2023)

| ID | Risk | Production Control |
| --- | --- | --- |
| API1 | Broken Object Level Authorization | Enforce ownership checks on every object read/write |
| API2 | Broken Authentication | Short-lived access token + rotation refresh token |
| API3 | Broken Object Property Level Authorization | Field-level allowlist for read/write payloads |
| API4 | Unrestricted Resource Consumption | Rate limit, payload limits, and timeout budgets |
| API5 | Broken Function Level Authorization | RBAC/ABAC middleware per endpoint |
| API6 | Unrestricted Access to Sensitive Business Flows | Step-up auth, anti-automation, anomaly detection |
| API7 | SSRF | URL allowlist and internal address blocking |
| API8 | Security Misconfiguration | Hardened headers, CORS allowlist, non-default configs |
| API9 | Improper Inventory Management | Versioned API catalog and deprecation policy |
| API10 | Unsafe Consumption of APIs | Validate third-party responses and fail closed |

---

## 🛠️ SUB-STEPS (EXECUTION PIPELINE)

1. **Information Extraction**: Identify API type (REST, GraphQL, WebSocket) and sensitivity of data handled.
2. **Authentication & Authorization**: Choose method (JWT, OAuth 2.0) and implement RBAC (Role-Based Access Control).
3. **Input Validation**: Use schemas (Zod, Pydantic) to validate all incoming data; use parameterized queries to prevent SQLi.
4. **Rate Limiting**: Implement per-user/IP limits using Redis or middleware (e.g., `express-rate-limit`).
5. **Data Protection**: Ensure TLS/HTTPS for transit, encryption at rest for sensitive fields, and sanitized error messages.
6. **Security Headers**: Implement `Helmet.js` or equivalent to set CSP, HSTS, and frameguard headers.

---

## 🔐 PRODUCTION EXAMPLES

### 1) Baseline middleware stack

```typescript
import express from 'express';
import helmet from 'helmet';
import cors from 'cors';
import rateLimit from 'express-rate-limit';

const app = express();

app.use(helmet());
app.use(cors({ origin: ['https://app.example.com'], credentials: true }));
app.use(express.json({ limit: '1mb' }));

app.use(
  rateLimit({
    windowMs: 60_000,
    max: 120,
    standardHeaders: true,
    legacyHeaders: false,
  })
);
```

### 2) Schema validation + canonical error contract

```typescript
import { z } from 'zod';
import type { Request, Response, NextFunction } from 'express';

const UpdateUserSchema = z.object({
  displayName: z.string().min(2).max(80),
  timezone: z.string().min(2).max(64),
});

function validateBody<T extends z.ZodTypeAny>(schema: T) {
  return (req: Request, res: Response, next: NextFunction) => {
    const parsed = schema.safeParse(req.body);
    if (!parsed.success) {
      return res.status(400).json({
        error: 'VALIDATION_ERROR',
        details: parsed.error.flatten(),
      });
    }
    req.body = parsed.data;
    next();
  };
}
```

### 3) JWT auth + RBAC scope gate

```typescript
import jwt from 'jsonwebtoken';
import type { Request, Response, NextFunction } from 'express';

type AuthClaims = { sub: string; scopes: string[] };

function requireAuth(req: Request, res: Response, next: NextFunction) {
  const token = req.headers.authorization?.replace('Bearer ', '');
  if (!token) return res.status(401).json({ error: 'UNAUTHORIZED' });

  try {
    const claims = jwt.verify(token, process.env.JWT_PUBLIC_KEY!, {
      algorithms: ['RS256'],
      issuer: 'https://auth.example.com',
      audience: 'api://core',
    }) as AuthClaims;

    (req as any).auth = claims;
    next();
  } catch {
    res.status(401).json({ error: 'INVALID_TOKEN' });
  }
}

function requireScope(scope: string) {
  return (req: Request, res: Response, next: NextFunction) => {
    const scopes = ((req as any).auth?.scopes ?? []) as string[];
    if (!scopes.includes(scope)) {
      return res.status(403).json({ error: 'FORBIDDEN' });
    }
    next();
  };
}
```

### 4) Write endpoint with idempotency + strict rate limiting

```typescript
import rateLimit from 'express-rate-limit';

const paymentsLimiter = rateLimit({
  windowMs: 15 * 60_000,
  max: 20,
  message: { error: 'TOO_MANY_REQUESTS' },
});

app.post(
  '/api/payments/charge',
  requireAuth,
  requireScope('payments:write'),
  paymentsLimiter,
  async (req, res) => {
    const idemKey = req.headers['idempotency-key'];
    if (!idemKey || typeof idemKey !== 'string') {
      return res.status(400).json({ error: 'MISSING_IDEMPOTENCY_KEY' });
    }

    const existing = await findPaymentByIdempotencyKey(idemKey);
    if (existing) return res.status(200).json(existing);

    const created = await createPayment(req.body, idemKey);
    res.status(201).json(created);
  }
);
```

### 5) Parameterized query + object-level authorization

```typescript
import { prisma } from '../db';

app.patch('/api/users/:id', requireAuth, validateBody(UpdateUserSchema), async (req, res) => {
  const actorId = (req as any).auth.sub as string;
  const targetId = req.params.id;

  if (actorId !== targetId) {
    return res.status(403).json({ error: 'OBJECT_ACCESS_DENIED' });
  }

  const user = await prisma.user.update({
    where: { id: targetId },
    data: {
      displayName: req.body.displayName,
      timezone: req.body.timezone,
    },
    select: { id: true, displayName: true, timezone: true },
  });

  res.json(user);
});
```

---

## 📝 OUTPUT SIGNATURE

- Secure API implementation code (JS/TS/Python).
- Authentication middleware.
- Rate limiting configurations.

---

## 🔍 QUICK VERIFICATION

```bash
# Validate security headers and CORS behavior
curl -I https://api.example.com/health

# Verify unauthorized and forbidden paths
curl -i https://api.example.com/api/users/me
curl -i -H "Authorization: Bearer <token-without-scope>" https://api.example.com/api/admin/reports
```

---

## 🧪 BENCHMARK TASK

- **Input**: "Secure our new /api/user/update endpoint against common attacks."
- **Output**: Endpoint with: JWT verification -> Zod schema validation -> Parameterized SQL update -> Rate limiting.
