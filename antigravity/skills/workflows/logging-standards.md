---
name: "LOGGING STANDARDS - CHUẨN MỰC GHI LOG"
tags: ["antigravity", "c:", "checklist", "chuẩn", "each", "frontend", "gemini", "ghi", "<YOUR_USERNAME>", "level", "levels", "log", "logging", "mực", "overview", "pattern", "standard", "standards", "use", "users"]
tier: 3
risk: "medium"
estimated_tokens: 2548
tools_needed: ["markdown", "sql", "terminal"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["web", "product"]
quality_score: 0.95
---
# LOGGING STANDARDS - CHUẨN MỰC GHI LOG

> **Tier:** 2-3  
> **Tags:** `[logging, observability, debugging, monitoring, structured-logging]`  
> **Khi nào dùng:** Mọi application (frontend, backend), đặc biệt production systems

---

## 📋 OVERVIEW

**Bad logging** dẫn đến:
- Cannot debug production issues
- No audit trail (security risk)
- Performance degradation (too many logs)
- PII leaks (GDPR violations)
- Log storage costs explode

**Thống kê:**
- 60% production incidents take 2+ hours to debug without proper logs
- Average app generates 1GB logs/day

---

## 🎯 LOGGING CHECKLIST

```markdown
[ ] Log levels used correctly (FATAL, ERROR, WARN, INFO, DEBUG, TRACE)
[ ] Structured logging (JSON format)
[ ] Correlation IDs (traceId, requestId)
[ ] No PII in logs (email, password, credit card)
[ ] Error logs include stack traces
[ ] Request/response logging (API)
[ ] Database query logging (slow queries only)
[ ] Performance metrics logged
[ ] Log rotation configured
[ ] Log aggregation setup (ELK, Datadog, CloudWatch)
```

---

## 📊 PATTERN 1: LOG LEVELS

### Standard Levels

```javascript
// ⭐ Log Levels (from most to least severe)
FATAL  // Application crash, cannot continue
ERROR  // Error occurred, but app continues
WARN   // Something unexpected, but not error
INFO   // Important business events
DEBUG  // Detailed information for debugging
TRACE  // Very detailed (function entry/exit)
```

### When to Use Each Level

```javascript
// FATAL: Application cannot continue
logger.fatal('Database connection failed, shutting down');
process.exit(1);

// ERROR: Error occurred, but app continues
try {
  await processPayment(orderId);
} catch (error) {
  logger.error('Payment processing failed', { orderId, error });
  // Send error to user, but app continues
}

// WARN: Unexpected but not error
if (user.age < 18) {
  logger.warn('Underage user attempted purchase', { userId: user.id });
}

// INFO: Important business events
logger.info('User registered', { userId: user.id, email: user.email });
logger.info('Order placed', { orderId, userId, total });

// DEBUG: Detailed debugging info
logger.debug('Fetching user from database', { userId });
logger.debug('Cache hit', { key, value });

// TRACE: Very detailed (usually disabled)
logger.trace('Entering function', { functionName: 'processOrder', args });
```

---

## 📦 PATTERN 2: STRUCTURED LOGGING (JSON)

### ✅ Structured Format

```javascript
// ❌ BAD: Unstructured string
console.log('User 123 placed order 456 for $99.99');

// ✅ GOOD: Structured JSON
logger.info('Order placed', {
  userId: 123,
  orderId: 456,
  total: 99.99,
  currency: 'USD',
  timestamp: new Date().toISOString()
});

// Output (JSON):
{
  "level": "info",
  "message": "Order placed",
  "userId": 123,
  "orderId": 456,
  "total": 99.99,
  "currency": "USD",
  "timestamp": "2024-03-30T10:00:00.000Z",
  "service": "order-service",
  "environment": "production"
}
```

### Implementation (Winston)

```javascript
const winston = require('winston');

const logger = winston.createLogger({
  level: process.env.LOG_LEVEL || 'info',
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.errors({ stack: true }),
    winston.format.json()
  ),
  defaultMeta: {
    service: 'order-service',
    environment: process.env.NODE_ENV
  },
  transports: [
    new winston.transports.File({ filename: 'error.log', level: 'error' }),
    new winston.transports.File({ filename: 'combined.log' })
  ]
});

// Development: Pretty print
if (process.env.NODE_ENV !== 'production') {
  logger.add(new winston.transports.Console({
    format: winston.format.simple()
  }));
}
```

---

## 🔗 PATTERN 3: CORRELATION IDs

### Request Tracing

```javascript
// Express middleware: Add requestId
const { v4: uuidv4 } = require('uuid');

app.use((req, res, next) => {
  req.id = req.headers['x-request-id'] || uuidv4();
  res.setHeader('X-Request-ID', req.id);
  next();
});

// Log with requestId
app.get('/api/users/:id', async (req, res) => {
  logger.info('Fetching user', {
    requestId: req.id,
    userId: req.params.id,
    ip: req.ip
  });
  
  try {
    const user = await db.users.findOne({ id: req.params.id });
    
    logger.info('User fetched successfully', {
      requestId: req.id,
      userId: user.id
    });
    
    res.json({ success: true, data: user });
    
  } catch (error) {
    logger.error('Error fetching user', {
      requestId: req.id,
      userId: req.params.id,
      error: error.message,
      stack: error.stack
    });
    
    res.status(500).json({
      success: false,
      error: 'Internal server error',
      requestId: req.id  // ⭐ Return to client for support
    });
  }
});
```

### Distributed Tracing

```javascript
// Microservices: Propagate traceId
const axios = require('axios');

async function callDownstreamService(traceId, data) {
  logger.info('Calling downstream service', { traceId });
  
  const response = await axios.post('https://api.example.com/process', data, {
    headers: {
      'X-Trace-ID': traceId  // ⭐ Propagate traceId
    }
  });
  
  logger.info('Downstream service responded', {
    traceId,
    statusCode: response.status
  });
  
  return response.data;
}
```

---

## 🔒 PATTERN 4: PII HANDLING

### ❌ NEVER Log PII

```javascript
// ❌ BAD: Logging PII
logger.info('User login', {
  email: 'john@example.com',  // ❌ PII
  password: 'secret123',  // ❌ CRITICAL!
  ssn: '123-45-6789',  // ❌ PII
  creditCard: '4111-1111-1111-1111'  // ❌ PII
});

// ✅ GOOD: Mask or omit PII
logger.info('User login', {
  userId: 123,  // ✓ OK (not PII)
  emailDomain: 'example.com',  // ✓ OK (masked)
  ipAddress: '192.168.1.1'  // ✓ OK (for security)
});
```

### Auto-Redact PII

```javascript
// Redact sensitive fields
function redactPII(obj) {
  const sensitiveFields = ['password', 'ssn', 'creditCard', 'token'];
  const redacted = { ...obj };
  
  for (const field of sensitiveFields) {
    if (redacted[field]) {
      redacted[field] = '[REDACTED]';
    }
  }
  
  // Mask email
  if (redacted.email) {
    redacted.email = redacted.email.replace(/(.{2})(.*)(@.*)/, '$1***$3');
    // john@example.com → jo***@example.com
  }
  
  return redacted;
}

// Usage
logger.info('User data', redactPII({
  email: 'john@example.com',
  password: 'secret123',
  name: 'John Doe'
}));
// Output: { email: 'jo***@example.com', password: '[REDACTED]', name: 'John Doe' }
```

---

## 🌐 PATTERN 5: REQUEST/RESPONSE LOGGING

### API Logging Middleware

```javascript
// Express middleware
app.use((req, res, next) => {
  const start = Date.now();
  
  // Log request
  logger.info('Incoming request', {
    requestId: req.id,
    method: req.method,
    path: req.path,
    query: req.query,
    ip: req.ip,
    userAgent: req.headers['user-agent']
  });
  
  // Capture response
  const originalSend = res.send;
  res.send = function(data) {
    const duration = Date.now() - start;
    
    logger.info('Outgoing response', {
      requestId: req.id,
      statusCode: res.statusCode,
      duration,
      contentLength: data?.length
    });
    
    // Performance warning
    if (duration > 1000) {
      logger.warn('Slow request', {
        requestId: req.id,
        duration,
        path: req.path
      });
    }
    
    originalSend.call(this, data);
  };
  
  next();
});
```

---

## 🗄️ PATTERN 6: DATABASE QUERY LOGGING

### Log Slow Queries Only

```javascript
// Sequelize: Log slow queries
const sequelize = new Sequelize('database', 'username', 'password', {
  logging: (sql, timing) => {
    if (timing > 1000) {  // ⭐ Only log if > 1 second
      logger.warn('Slow query', {
        sql,
        duration: timing,
        threshold: 1000
      });
    }
  },
  benchmark: true
});

// Mongoose: Log slow queries
mongoose.set('debug', (collectionName, method, query, doc, options) => {
  const start = Date.now();
  
  return function() {
    const duration = Date.now() - start;
    
    if (duration > 100) {  // ⭐ Only log if > 100ms
      logger.warn('Slow MongoDB query', {
        collection: collectionName,
        method,
        query,
        duration
      });
    }
  };
});
```

---

## 📊 QUICK REFERENCE

| Level | When to Use | Example |
|-------|-------------|---------|
| **FATAL** | App crash | Database connection failed |
| **ERROR** | Error occurred | Payment processing failed |
| **WARN** | Unexpected | Deprecated API used |
| **INFO** | Business events | User registered, Order placed |
| **DEBUG** | Debugging | Cache hit, Query executed |
| **TRACE** | Very detailed | Function entry/exit |

---

## 🚨 COMMON MISTAKES

### ❌ Mistake 1: Logging Passwords

```javascript
// ❌ NEVER
logger.info('User login', { email, password });

// ✅ ALWAYS redact
logger.info('User login', { userId });
```

### ❌ Mistake 2: Too Many Logs

```javascript
// ❌ BAD: Log every iteration
for (let i = 0; i < 1000000; i++) {
  logger.debug('Processing item', { i });  // 1M logs!
}

// ✅ GOOD: Log summary
logger.info('Processing items', { count: 1000000 });
// ... process ...
logger.info('Items processed', { count: 1000000, duration });
```

### ❌ Mistake 3: No Context

```javascript
// ❌ BAD
logger.error('Error occurred');

// ✅ GOOD
logger.error('Error processing payment', {
  orderId,
  userId,
  error: error.message,
  stack: error.stack
});
```

---

## 🎯 AI LEVERAGE

### Prompt for AI

```
"Add logging to Express API with:
- Winston structured logging (JSON)
- Request/response logging with requestId
- Error logging with stack traces
- Slow query logging (> 1 second)
- PII redaction (email, password)
- Log levels: INFO for business events, ERROR for failures"
```

### AI Should

1. ✅ Use Winston or Pino (structured logging)
2. ✅ Add requestId middleware
3. ✅ Log request/response with duration
4. ✅ Redact PII automatically
5. ✅ Log errors with stack traces
6. ✅ Use appropriate log levels
7. ✅ Add slow query logging

---

## 🔗 RELATED SKILLS

- `error-handling-patterns.md` - Error logging
- `api-design-standards.md` - API request logging
- `database-standards.md` - Query logging

---

**Version:** 1.0.0  
**Last Updated:** 2026-03-30  
**Complexity:** Medium  
**Impact:** Critical (debugging & monitoring)
