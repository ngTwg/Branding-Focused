---
name: "SECURITY MIDDLEWARE STACK - BẢO MẬT TOÀN DIỆN"
tags: ["antigravity", "backend", "bảo", "c:", "checklist", "chuẩn", "code", "diện", "gemini", "gặp", "hay", "<YOUR_USERNAME>", "middleware", "mật", "như", "này", "overview", "security", "sinh", "stack"]
tier: 2
risk: "medium"
estimated_tokens: 3715
tools_needed: ["markdown", "sql", "terminal"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["platform", "api"]
quality_score: 0.95
---
# SECURITY MIDDLEWARE STACK - BẢO MẬT TOÀN DIỆN

> **Tier:** 2-4 (Mandatory for production)  
> **Tags:** `[security, middleware, owasp, helmet, cors, rate-limit]`  
> **Khi nào dùng:** Mọi web application, API server

---

## 🎯 OVERVIEW

45% code AI có lỗ hổng bảo mật nghiêm trọng. AI thường quên thêm security headers, CORS config, rate limiting, và CSRF protection.

**Mục tiêu:** 
- Zero security vulnerabilities từ missing middleware
- OWASP Top 10 compliance
- Production-ready security setup

---

## 🔴 VẤN ĐỀ THƯỜNG GẶP

### ❌ AI hay sinh code như thế này:
```typescript
// Không có security middleware
const app = express();
app.use(express.json());

app.post('/api/login', async (req, res) => {
  // No rate limiting - brute force attack possible
  // No CSRF protection
  // No security headers
  const { email, password } = req.body;
  // ...
});

app.listen(3000);
```

### ✅ Đúng chuẩn:
```typescript
import express from 'express';
import helmet from 'helmet';
import cors from 'cors';
import rateLimit from 'express-rate-limit';
import csrf from 'csurf';

const app = express();

// Security middleware stack
app.use(helmet());  // Security headers
app.use(cors({ origin: ['https://myapp.com'] }));  // CORS
app.use(express.json({ limit: '10mb' }));  // Body size limit

// Rate limiting
const authLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 5,
  message: 'Too many login attempts',
});

app.post('/api/login', authLimiter, async (req, res) => {
  // Protected endpoint
});
```

---

## 📋 SECURITY MIDDLEWARE CHECKLIST

### ✅ MANDATORY (Tier 2+)
- [ ] Helmet.js - Security headers
- [ ] CORS - Origin whitelist
- [ ] Rate limiting - Brute force protection
- [ ] Body size limit - DoS protection
- [ ] Input validation - Zod/Joi schema
- [ ] HTTPS enforcement - Redirect HTTP to HTTPS

### ✅ RECOMMENDED (Tier 2+)
- [ ] CSRF protection - For form submissions
- [ ] HPP - HTTP Parameter Pollution
- [ ] express-mongo-sanitize - NoSQL injection
- [ ] Content Security Policy - XSS protection

### ✅ ADVANCED (Tier 3+)
- [ ] WAF - Web Application Firewall
- [ ] DDoS protection - Cloudflare/AWS Shield
- [ ] API key authentication
- [ ] JWT token validation

---

## 🛡️ MIDDLEWARE SETUP

### 1. HELMET.JS - Security Headers

#### Installation
```bash
npm install helmet
```

#### Basic Setup
```typescript
import helmet from 'helmet';

app.use(helmet());  // Enables all default protections
```

#### Custom Configuration
```typescript
app.use(
  helmet({
    // Content Security Policy
    contentSecurityPolicy: {
      directives: {
        defaultSrc: ["'self'"],
        styleSrc: ["'self'", "'unsafe-inline'", "https://fonts.googleapis.com"],
        fontSrc: ["'self'", "https://fonts.gstatic.com"],
        imgSrc: ["'self'", "data:", "https:"],
        scriptSrc: ["'self'"],
        connectSrc: ["'self'", "https://api.myapp.com"],
      },
    },
    
    // Strict Transport Security (HSTS)
    hsts: {
      maxAge: 31536000,  // 1 year
      includeSubDomains: true,
      preload: true,
    },
    
    // X-Frame-Options
    frameguard: {
      action: 'deny',  // Prevent clickjacking
    },
    
    // X-Content-Type-Options
    noSniff: true,  // Prevent MIME sniffing
    
    // Referrer-Policy
    referrerPolicy: {
      policy: 'strict-origin-when-cross-origin',
    },
  })
);
```

#### Headers Set by Helmet
```
Content-Security-Policy: default-src 'self'
Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 0
Referrer-Policy: strict-origin-when-cross-origin
```

---

### 2. CORS - Cross-Origin Resource Sharing

#### Installation
```bash
npm install cors
```

#### ❌ BAD - Allow all origins
```typescript
app.use(cors());  // DANGEROUS in production
```

#### ✅ GOOD - Whitelist specific origins
```typescript
import cors from 'cors';

const corsOptions = {
  origin: function (origin, callback) {
    const whitelist = [
      'https://myapp.com',
      'https://www.myapp.com',
      'https://admin.myapp.com',
    ];
    
    // Allow requests with no origin (mobile apps, Postman)
    if (!origin) return callback(null, true);
    
    if (whitelist.indexOf(origin) !== -1) {
      callback(null, true);
    } else {
      callback(new Error('Not allowed by CORS'));
    }
  },
  credentials: true,  // Allow cookies
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'PATCH'],
  allowedHeaders: ['Content-Type', 'Authorization'],
  exposedHeaders: ['X-Total-Count'],
  maxAge: 86400,  // 24 hours
};

app.use(cors(corsOptions));
```

#### Environment-based CORS
```typescript
const allowedOrigins = process.env.NODE_ENV === 'production'
  ? ['https://myapp.com']
  : ['http://localhost:3000', 'http://localhost:5173'];

app.use(cors({
  origin: allowedOrigins,
  credentials: true,
}));
```

---

### 3. RATE LIMITING - Brute Force Protection

#### Installation
```bash
npm install express-rate-limit
```

#### Basic Setup
```typescript
import rateLimit from 'express-rate-limit';

// Global rate limit
const globalLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,  // 15 minutes
  max: 100,  // 100 requests per window
  message: 'Too many requests from this IP',
  standardHeaders: true,  // Return rate limit info in headers
  legacyHeaders: false,
});

app.use(globalLimiter);
```

#### Endpoint-Specific Limits
```typescript
// Strict limit for auth endpoints
const authLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 5,  // Only 5 attempts per 15 minutes
  skipSuccessfulRequests: true,  // Don't count successful logins
  message: {
    error: 'TOO_MANY_ATTEMPTS',
    message: 'Too many login attempts. Please try again later.',
    retryAfter: 900,  // seconds
  },
});

app.post('/api/auth/login', authLimiter, loginHandler);
app.post('/api/auth/register', authLimiter, registerHandler);

// Moderate limit for API endpoints
const apiLimiter = rateLimit({
  windowMs: 60 * 1000,  // 1 minute
  max: 60,  // 60 requests per minute
});

app.use('/api/', apiLimiter);

// Relaxed limit for public endpoints
const publicLimiter = rateLimit({
  windowMs: 60 * 1000,
  max: 300,
});

app.use('/public/', publicLimiter);
```

#### Redis-based Rate Limiting (Distributed)
```typescript
import rateLimit from 'express-rate-limit';
import RedisStore from 'rate-limit-redis';
import { createClient } from 'redis';

const redisClient = createClient({
  url: process.env.REDIS_URL,
});

await redisClient.connect();

const limiter = rateLimit({
  store: new RedisStore({
    client: redisClient,
    prefix: 'rate-limit:',
  }),
  windowMs: 15 * 60 * 1000,
  max: 100,
});

app.use(limiter);
```

---

### 4. CSRF PROTECTION

#### Installation
```bash
npm install csurf cookie-parser
```

#### Setup (for server-rendered apps)
```typescript
import csrf from 'csurf';
import cookieParser from 'cookie-parser';

app.use(cookieParser());

const csrfProtection = csrf({
  cookie: {
    httpOnly: true,
    secure: process.env.NODE_ENV === 'production',
    sameSite: 'strict',
  },
});

// Apply to state-changing routes
app.post('/api/orders', csrfProtection, createOrderHandler);
app.put('/api/users/:id', csrfProtection, updateUserHandler);
app.delete('/api/posts/:id', csrfProtection, deletePostHandler);

// Endpoint to get CSRF token
app.get('/api/csrf-token', csrfProtection, (req, res) => {
  res.json({ csrfToken: req.csrfToken() });
});
```

#### Client-side Usage
```typescript
// Fetch CSRF token
const response = await fetch('/api/csrf-token');
const { csrfToken } = await response.json();

// Include in requests
await fetch('/api/orders', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'CSRF-Token': csrfToken,
  },
  body: JSON.stringify(orderData),
});
```

#### Alternative: Double Submit Cookie Pattern
```typescript
// For SPA/API-only apps
app.use((req, res, next) => {
  if (!req.cookies.csrfToken) {
    const token = crypto.randomBytes(32).toString('hex');
    res.cookie('csrfToken', token, {
      httpOnly: false,  // Client needs to read it
      secure: true,
      sameSite: 'strict',
    });
  }
  next();
});

// Validation middleware
function validateCsrf(req, res, next) {
  const cookieToken = req.cookies.csrfToken;
  const headerToken = req.headers['x-csrf-token'];
  
  if (!cookieToken || cookieToken !== headerToken) {
    return res.status(403).json({ error: 'Invalid CSRF token' });
  }
  
  next();
}

app.post('/api/orders', validateCsrf, createOrderHandler);
```

---

### 5. INPUT SANITIZATION

#### Installation
```bash
npm install express-mongo-sanitize hpp
```

#### Setup
```typescript
import mongoSanitize from 'express-mongo-sanitize';
import hpp from 'hpp';

// Prevent NoSQL injection
app.use(mongoSanitize({
  replaceWith: '_',  // Replace $ and . with _
}));

// Prevent HTTP Parameter Pollution
app.use(hpp({
  whitelist: ['sort', 'filter'],  // Allow these params to be arrays
}));
```

#### Example Attack Prevention
```typescript
// ❌ Without sanitization - NoSQL injection
// POST /api/login
// { "email": { "$gt": "" }, "password": { "$gt": "" } }
// → Bypasses authentication!

// ✅ With mongoSanitize
// { "email": { "_gt": "" }, "password": { "_gt": "" } }
// → Treated as literal strings, safe
```

---

### 6. BODY SIZE LIMITS

```typescript
// Prevent large payload DoS
app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true, limit: '10mb' }));

// File upload limits (with multer)
import multer from 'multer';

const upload = multer({
  limits: {
    fileSize: 5 * 1024 * 1024,  // 5MB
    files: 5,  // Max 5 files
  },
  fileFilter: (req, file, cb) => {
    // Only allow images
    if (!file.mimetype.startsWith('image/')) {
      return cb(new Error('Only images allowed'));
    }
    cb(null, true);
  },
});

app.post('/api/upload', upload.array('photos', 5), uploadHandler);
```

---

### 7. HTTPS ENFORCEMENT

```typescript
// Redirect HTTP to HTTPS
app.use((req, res, next) => {
  if (process.env.NODE_ENV === 'production' && !req.secure) {
    return res.redirect(301, `https://${req.headers.host}${req.url}`);
  }
  next();
});

// Or use express-sslify
import enforce from 'express-sslify';

if (process.env.NODE_ENV === 'production') {
  app.use(enforce.HTTPS({ trustProtoHeader: true }));
}
```

---

## 🔒 COMPLETE SECURITY STACK

### Production-Ready Setup
```typescript
import express from 'express';
import helmet from 'helmet';
import cors from 'cors';
import rateLimit from 'express-rate-limit';
import mongoSanitize from 'express-mongo-sanitize';
import hpp from 'hpp';
import csrf from 'csurf';
import cookieParser from 'cookie-parser';

const app = express();

// 1. Trust proxy (if behind reverse proxy)
app.set('trust proxy', 1);

// 2. Security headers
app.use(helmet({
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      styleSrc: ["'self'", "'unsafe-inline'"],
      scriptSrc: ["'self'"],
      imgSrc: ["'self'", "data:", "https:"],
    },
  },
  hsts: {
    maxAge: 31536000,
    includeSubDomains: true,
    preload: true,
  },
}));

// 3. CORS
const allowedOrigins = process.env.ALLOWED_ORIGINS?.split(',') || [];
app.use(cors({
  origin: allowedOrigins,
  credentials: true,
}));

// 4. Body parsing with size limits
app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true, limit: '10mb' }));

// 5. Cookie parser (for CSRF)
app.use(cookieParser());

// 6. Input sanitization
app.use(mongoSanitize());
app.use(hpp());

// 7. Rate limiting
const globalLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 100,
  standardHeaders: true,
});
app.use(globalLimiter);

const authLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 5,
  skipSuccessfulRequests: true,
});

// 8. CSRF protection
const csrfProtection = csrf({ cookie: true });

// 9. Routes
app.post('/api/auth/login', authLimiter, loginHandler);
app.post('/api/orders', csrfProtection, createOrderHandler);

// 10. Error handler
app.use((err, req, res, next) => {
  if (err.code === 'EBADCSRFTOKEN') {
    return res.status(403).json({ error: 'Invalid CSRF token' });
  }
  
  console.error(err);
  res.status(500).json({ error: 'Internal server error' });
});

app.listen(3000);
```

---

## ✅ SECURITY CHECKLIST

### Pre-Deployment Checklist
- [ ] Helmet.js installed and configured
- [ ] CORS whitelist configured (no wildcard *)
- [ ] Rate limiting on all endpoints
- [ ] CSRF protection on state-changing routes
- [ ] Input sanitization (mongoSanitize, hpp)
- [ ] Body size limits set
- [ ] HTTPS enforced in production
- [ ] Security headers verified (securityheaders.com)
- [ ] No secrets in code (use env vars)
- [ ] Error messages don't expose internals

### Testing Checklist
- [ ] Test CORS with different origins
- [ ] Test rate limiting (trigger limit)
- [ ] Test CSRF protection (missing token)
- [ ] Test input sanitization (NoSQL injection)
- [ ] Test large payload rejection
- [ ] Scan with OWASP ZAP or Burp Suite

---

## 🚨 COMMON MISTAKES & FIXES

### Mistake 1: CORS wildcard in production
```typescript
❌ BAD
app.use(cors());  // Allows ALL origins

✅ FIX
app.use(cors({
  origin: ['https://myapp.com'],
}));
```

### Mistake 2: No rate limiting on auth
```typescript
❌ BAD
app.post('/api/login', loginHandler);  // Brute force possible

✅ FIX
const authLimiter = rateLimit({ max: 5, windowMs: 15 * 60 * 1000 });
app.post('/api/login', authLimiter, loginHandler);
```

### Mistake 3: Exposing error details
```typescript
❌ BAD
app.use((err, req, res, next) => {
  res.status(500).json({ error: err.stack });  // Exposes internals
});

✅ FIX
app.use((err, req, res, next) => {
  console.error(err);  // Log internally
  res.status(500).json({ error: 'Internal server error' });
});
```

---

## 🎯 AI LEVERAGE

### Security Setup Prompt
```markdown
Setup production-ready security middleware:

1. Install: helmet, cors, express-rate-limit, mongoSanitize, hpp
2. Configure:
   - Helmet with CSP
   - CORS with whitelist: [ORIGINS]
   - Rate limiting: 5 req/15min for auth, 100 req/15min global
   - Input sanitization
   - Body size limit: 10MB
3. Apply to Express app
4. Add error handler for CSRF
```

---

## 📚 QUICK REFERENCE

| Middleware | Purpose | Priority |
|------------|---------|----------|
| helmet | Security headers | ✅ Critical |
| cors | Origin control | ✅ Critical |
| rate-limit | Brute force | ✅ Critical |
| mongoSanitize | NoSQL injection | ✅ Critical |
| csrf | CSRF attacks | ⚠️ If forms |
| hpp | Parameter pollution | 🟢 Nice to have |

---

## 🔗 RELATED SKILLS

- `workflows/anti-hallucination-v2.md` - Verify security packages
- `backend/api-design-standards.md` - Secure API design
- `workflows/error-handling-patterns.md` - Secure error handling

---

**Version:** 1.0.0  
**Last Updated:** 2026-03-30  
**Status:** ✅ MANDATORY - All production apps must have security middleware
