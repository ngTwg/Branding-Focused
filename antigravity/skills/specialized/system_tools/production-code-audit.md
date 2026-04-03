---
name: "Production Code Audit"
tags: ["antigravity", "audit", "c:", "check", "code", "for", "frontend", "gemini", "json", "<YOUR_USERNAME>", "outdated", "overview", "package", "packages", "production", "rules", "specialized", "system", "tools", "users"]
tier: 2
risk: "medium"
estimated_tokens: 2473
tools_needed: ["git", "markdown", "sql", "terminal"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["web", "product"]
quality_score: 0.95
---
# Production Code Audit

> **Tier:** 2-3  
> **Tags:** `audit`, `code-quality`, `security`, `performance`, `review`  
> **When to use:** Code reviews, security audits, performance optimization, pre-production checks

---

## Overview

Comprehensive code audit checklist covering security vulnerabilities (OWASP Top 10), performance bottlenecks, code quality issues, best practices violations, and dependency audits. Essential for production-ready code.

---

## Rules

**RULE-001: Security Audit (OWASP Top 10)**
Check for common vulnerabilities: injection, broken authentication, sensitive data exposure, XXE, broken access control, security misconfiguration, XSS, insecure deserialization, insufficient logging.

```typescript
❌ Bad: SQL Injection vulnerability
const query = `SELECT * FROM users WHERE email = '${email}'`;
await db.query(query); // User input directly in query

❌ Bad: XSS vulnerability
res.send(`<h1>Welcome ${username}</h1>`); // Unescaped user input

❌ Bad: Hardcoded secrets
const API_KEY = 'sk_live_abc123xyz'; // Secret in code

✅ Good: Secure practices
// Parameterized queries
const query = 'SELECT * FROM users WHERE email = $1';
await db.query(query, [email]);

// Escaped output
res.send(`<h1>Welcome ${escapeHtml(username)}</h1>`);

// Environment variables
const API_KEY = process.env.API_KEY;
if (!API_KEY) throw new Error('API_KEY not configured');
```

**RULE-002: Authentication & Authorization**
Verify proper authentication on all endpoints. Check authorization for resource access. Validate JWT tokens correctly. Use secure session management.

```typescript
❌ Bad: Missing authentication
app.get('/api/users/:id', async (req, res) => {
  const user = await db.users.findById(req.params.id);
  res.json(user); // Anyone can access any user
});

❌ Bad: Weak JWT validation
const decoded = jwt.decode(token); // No verification!
req.user = decoded;

✅ Good: Proper auth & authz
app.get('/api/users/:id', 
  authenticate, // Middleware verifies JWT
  async (req, res) => {
    const requestedId = req.params.id;
    
    // Authorization: users can only access their own data
    if (req.user.id !== requestedId && !req.user.isAdmin) {
      return res.status(403).json({ error: 'Forbidden' });
    }
    
    const user = await db.users.findById(requestedId);
    res.json(user);
  }
);

// Proper JWT verification
function authenticate(req, res, next) {
  const token = req.headers.authorization?.split(' ')[1];
  if (!token) return res.status(401).json({ error: 'No token' });
  
  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    req.user = decoded;
    next();
  } catch (error) {
    res.status(401).json({ error: 'Invalid token' });
  }
}
```

**RULE-003: Input Validation**
Validate all user input. Use schema validation libraries. Sanitize before processing. Reject invalid input early.

```typescript
❌ Bad: No validation
app.post('/api/users', async (req, res) => {
  const user = await db.users.create(req.body);
  res.json(user); // Accepts any data
});

✅ Good: Schema validation
import { z } from 'zod';

const UserSchema = z.object({
  email: z.string().email(),
  name: z.string().min(2).max(100),
  age: z.number().int().min(18).max(120),
  role: z.enum(['user', 'admin'])
});

app.post('/api/users', async (req, res) => {
  try {
    const validated = UserSchema.parse(req.body);
    const user = await db.users.create(validated);
    res.json(user);
  } catch (error) {
    res.status(400).json({ error: error.errors });
  }
});
```

**RULE-004: Error Handling & Logging**
Handle all errors gracefully. Don't expose stack traces to users. Log errors with context. Monitor error rates.

```typescript
❌ Bad: Exposed errors
app.get('/api/data', async (req, res) => {
  const data = await db.query('SELECT * FROM sensitive_table');
  res.json(data); // Throws unhandled error with stack trace
});

✅ Good: Proper error handling
app.get('/api/data', async (req, res) => {
  try {
    const data = await db.query('SELECT * FROM sensitive_table');
    res.json(data);
  } catch (error) {
    // Log with context
    logger.error('Database query failed', {
      endpoint: '/api/data',
      userId: req.user?.id,
      error: error.message,
      stack: error.stack
    });
    
    // Generic error to user
    res.status(500).json({ 
      error: 'Internal server error',
      requestId: req.id
    });
  }
});

// Global error handler
app.use((error, req, res, next) => {
  logger.error('Unhandled error', { error, req: req.path });
  res.status(500).json({ error: 'Internal server error' });
});
```

**RULE-005: Performance Audit**
Check for N+1 queries, missing indexes, inefficient algorithms, memory leaks, blocking operations.

```typescript
❌ Bad: N+1 query problem
const users = await db.users.findAll();
for (const user of users) {
  user.posts = await db.posts.findByUserId(user.id); // N queries
}

❌ Bad: Blocking operation
const data = fs.readFileSync('large-file.json'); // Blocks event loop

✅ Good: Optimized queries
// Single query with join
const users = await db.users.findAll({
  include: [{ model: db.posts }]
});

// Or use DataLoader for batching
const users = await db.users.findAll();
const userIds = users.map(u => u.id);
const posts = await db.posts.findByUserIds(userIds);

✅ Good: Non-blocking I/O
const data = await fs.promises.readFile('large-file.json');
```

**RULE-006: Code Quality**
Check for: code duplication, long functions, high complexity, poor naming, missing tests, outdated dependencies.

```typescript
❌ Bad: Code smells
// Long function (>50 lines)
function processOrder(order) {
  // 100 lines of mixed concerns
}

// High complexity (cyclomatic > 10)
function calculate(a, b, c, d, e) {
  if (a) {
    if (b) {
      if (c) {
        if (d) {
          if (e) {
            // deeply nested
          }
        }
      }
    }
  }
}

✅ Good: Clean code
// Single responsibility, short functions
function processOrder(order: Order): Promise<void> {
  validateOrder(order);
  const total = calculateTotal(order);
  return saveOrder(order, total);
}

// Low complexity, early returns
function calculate(params: Params): number {
  if (!params.a) return 0;
  if (!params.b) return params.a;
  return params.a + params.b;
}
```

**RULE-007: Dependency Audit**
Check for: outdated packages, known vulnerabilities, unused dependencies, license issues.

```bash
❌ Bad: Outdated dependencies
# package.json
"dependencies": {
  "express": "4.16.0", // 5 years old
  "lodash": "4.17.15"  // Has known vulnerabilities
}

✅ Good: Regular audits
# Check for vulnerabilities
npm audit
npm audit fix

# Check for outdated packages
npm outdated

# Update dependencies
npm update

# Check licenses
npx license-checker --summary

# Remove unused dependencies
npx depcheck
```

**RULE-008: Configuration & Secrets**
Verify: no secrets in code, environment-specific configs, secure defaults, proper secret management.

```typescript
❌ Bad: Secrets in code
const config = {
  database: {
    host: 'prod-db.example.com',
    password: 'super-secret-password' // Hardcoded!
  },
  apiKey: 'sk_live_abc123' // In version control!
};

✅ Good: Environment-based config
// config.ts
export const config = {
  database: {
    host: process.env.DB_HOST || 'localhost',
    password: process.env.DB_PASSWORD, // From environment
    ssl: process.env.NODE_ENV === 'production'
  },
  apiKey: process.env.API_KEY
};

// Validate on startup
if (!config.apiKey) {
  throw new Error('API_KEY environment variable required');
}

// .env.example (committed)
DB_HOST=localhost
DB_PASSWORD=your-password-here
API_KEY=your-api-key-here

// .env (not committed, in .gitignore)
DB_HOST=prod-db.example.com
DB_PASSWORD=actual-secret
API_KEY=actual-key
```

---

## Quick Reference

### Security Audit Checklist

- [ ] No SQL injection (use parameterized queries)
- [ ] No XSS (escape output, use CSP)
- [ ] No CSRF (use tokens, SameSite cookies)
- [ ] Authentication on all endpoints
- [ ] Authorization checks for resources
- [ ] Secure password hashing (bcrypt, argon2)
- [ ] HTTPS enforced
- [ ] Secrets in environment variables
- [ ] Input validation on all endpoints
- [ ] Rate limiting implemented
- [ ] Security headers set (HSTS, X-Frame-Options, etc.)
- [ ] Dependencies audited for vulnerabilities

### Performance Audit Checklist

- [ ] No N+1 queries
- [ ] Database indexes on queried columns
- [ ] Caching for expensive operations
- [ ] Pagination for large datasets
- [ ] Async/await for I/O operations
- [ ] Connection pooling
- [ ] Compression enabled (gzip)
- [ ] Static assets on CDN
- [ ] Image optimization
- [ ] Bundle size optimized

### Code Quality Checklist

- [ ] Functions < 50 lines
- [ ] Cyclomatic complexity < 10
- [ ] No code duplication
- [ ] Descriptive variable names
- [ ] Comments for complex logic
- [ ] Tests for critical paths
- [ ] Error handling everywhere
- [ ] Logging with context
- [ ] Type safety (TypeScript)
- [ ] Linter passing

### Automated Audit Tools

```bash
# Security
npm audit
snyk test
bandit -r . # Python

# Code quality
eslint .
pylint **/*.py
sonarqube

# Performance
lighthouse https://example.com
clinic doctor -- node app.js

# Dependencies
npm outdated
npx license-checker
npx depcheck
```

### Critical Issues (Fix Immediately)

1. **SQL Injection** - Parameterize all queries
2. **XSS** - Escape all user input in output
3. **Hardcoded Secrets** - Move to environment variables
4. **Missing Authentication** - Add auth middleware
5. **Exposed Stack Traces** - Generic error messages
6. **Known Vulnerabilities** - Update dependencies
7. **Missing Input Validation** - Add schema validation
8. **No Rate Limiting** - Prevent abuse

---

## Metadata

- **Related Skills:** [security-middleware-stack.md], [error-handling-patterns.md], [performance-optimization.md]
- **Dependencies:** None
- **Version:** 1.0.0
- **Last Updated:** 2024-03-26
