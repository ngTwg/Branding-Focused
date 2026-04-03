---
name: "API DESIGN STANDARDS - THIẾT KẾ API CHUẨN MỰC"
tags: ["antigravity", "api", "backend", "best", "c:", "checklist", "chuẩn", "conventions", "design", "frontend", "gemini", "<YOUR_USERNAME>", "mực", "naming", "overview", "pattern", "practices", "rest", "rules", "standards"]
tier: 2
risk: "medium"
estimated_tokens: 5003
tools_needed: ["markdown", "terminal"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["web", "product"]
quality_score: 0.95
---
# API DESIGN STANDARDS - THIẾT KẾ API CHUẨN MỰC

> **Tier:** 2-3  
> **Tags:** `[api, rest, graphql, openapi, versioning, pagination]`  
> **Khi nào dùng:** Khi thiết kế bất kỳ API nào (REST, GraphQL), đặc biệt cho public APIs hoặc microservices

---

## 📋 OVERVIEW

**Bad API design** dẫn đến:
- Breaking changes → Client apps crash
- Inconsistent responses → Hard to parse
- Poor performance → Slow queries
- Security vulnerabilities → Data leaks
- Poor developer experience → Low adoption

**Thống kê:**
- 70% API failures do thiết kế kém (Postman State of API 2023)
- Average API có 15+ inconsistencies

---

## 🎯 API DESIGN CHECKLIST

```markdown
[ ] URL naming conventions (plural nouns, kebab-case)
[ ] HTTP methods used correctly (GET, POST, PUT, PATCH, DELETE)
[ ] Response envelope consistent
[ ] HTTP status codes appropriate
[ ] Pagination implemented (cursor or offset)
[ ] Filtering & sorting supported
[ ] Versioning strategy defined
[ ] Error responses standardized
[ ] Rate limiting implemented
[ ] Authentication/authorization required
[ ] CORS configured properly
[ ] OpenAPI/Swagger documentation
[ ] Request/response validation
[ ] Idempotency for mutations
[ ] Caching headers set
```

---

## 🔗 PATTERN 1: URL NAMING CONVENTIONS

### ✅ REST Best Practices

```
✅ GOOD URLs:
GET    /api/v1/users              # List users
GET    /api/v1/users/123          # Get user by ID
POST   /api/v1/users              # Create user
PUT    /api/v1/users/123          # Replace user (full update)
PATCH  /api/v1/users/123          # Update user (partial)
DELETE /api/v1/users/123          # Delete user

GET    /api/v1/users/123/posts   # Get user's posts (nested resource)
POST   /api/v1/users/123/posts   # Create post for user

GET    /api/v1/posts?author=123  # Alternative: filter by author

❌ BAD URLs:
GET    /api/v1/getUsers           # ❌ Verb in URL
POST   /api/v1/user               # ❌ Singular noun
GET    /api/v1/users/delete/123   # ❌ Action in URL (use DELETE method)
GET    /api/v1/user_posts         # ❌ Snake_case (use kebab-case)
POST   /api/v1/createNewUser      # ❌ Verbose, verb in URL
```

### Rules

1. **Use plural nouns:** `/users` not `/user`
2. **Use kebab-case:** `/user-profiles` not `/user_profiles` or `/userProfiles`
3. **No verbs in URLs:** Use HTTP methods instead
4. **Nested resources max 2 levels:** `/users/123/posts` ✓, `/users/123/posts/456/comments` ❌
5. **Use query params for filters:** `/products?category=electronics&price_max=1000`

---

## 📦 PATTERN 2: RESPONSE ENVELOPE STANDARD

### ✅ Consistent Response Format

```javascript
// Success response (200, 201)
{
  "success": true,
  "data": {
    "id": 123,
    "name": "John Doe",
    "email": "john@example.com"
  },
  "meta": {
    "timestamp": "2024-03-30T10:00:00Z",
    "requestId": "req_abc123"
  }
}

// List response with pagination
{
  "success": true,
  "data": [
    { "id": 1, "name": "User 1" },
    { "id": 2, "name": "User 2" }
  ],
  "pagination": {
    "page": 1,
    "pageSize": 20,
    "totalPages": 5,
    "totalItems": 100,
    "hasNext": true,
    "hasPrev": false
  },
  "meta": {
    "timestamp": "2024-03-30T10:00:00Z",
    "requestId": "req_abc123"
  }
}

// Error response (400, 404, 500)
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": [
      {
        "field": "email",
        "message": "Invalid email format"
      },
      {
        "field": "age",
        "message": "Must be at least 18"
      }
    ]
  },
  "meta": {
    "timestamp": "2024-03-30T10:00:00Z",
    "requestId": "req_abc123"
  }
}
```

### ❌ Anti-Pattern: Inconsistent Responses

```javascript
// ❌ BAD: Different formats
// Endpoint 1
{ "user": { "id": 1 } }

// Endpoint 2
{ "data": { "id": 1 } }

// Endpoint 3
{ "id": 1, "name": "John" }  // No wrapper

// ✅ GOOD: Always use same envelope
{ "success": true, "data": { ... } }
```

---

## 🚦 PATTERN 3: HTTP STATUS CODES

### Standard Status Codes

```javascript
// ✅ Success (2xx)
200 OK              // GET, PATCH, DELETE success
201 Created         // POST success (resource created)
204 No Content      // DELETE success (no response body)

// ✅ Client Errors (4xx)
400 Bad Request     // Invalid input, validation error
401 Unauthorized    // Missing or invalid authentication
403 Forbidden       // Authenticated but no permission
404 Not Found       // Resource doesn't exist
409 Conflict        // Duplicate resource, version conflict
422 Unprocessable   // Validation error (semantic)
429 Too Many Requests  // Rate limit exceeded

// ✅ Server Errors (5xx)
500 Internal Server Error  // Unexpected error
502 Bad Gateway           // Upstream service error
503 Service Unavailable   // Maintenance, overload
504 Gateway Timeout       // Upstream timeout
```

### Implementation

```javascript
// Express.js example
app.post('/api/v1/users', async (req, res) => {
  try {
    // Validation
    const { error, value } = userSchema.validate(req.body);
    if (error) {
      return res.status(400).json({
        success: false,
        error: {
          code: 'VALIDATION_ERROR',
          message: 'Invalid input data',
          details: error.details.map(d => ({
            field: d.path.join('.'),
            message: d.message
          }))
        }
      });
    }
    
    // Check duplicate
    const existing = await db.users.findOne({ email: value.email });
    if (existing) {
      return res.status(409).json({
        success: false,
        error: {
          code: 'DUPLICATE_EMAIL',
          message: 'Email already exists'
        }
      });
    }
    
    // Create user
    const user = await db.users.create(value);
    
    return res.status(201).json({
      success: true,
      data: user
    });
    
  } catch (error) {
    console.error('Error creating user:', error);
    return res.status(500).json({
      success: false,
      error: {
        code: 'INTERNAL_ERROR',
        message: 'An unexpected error occurred'
      }
    });
  }
});
```

---

## 📄 PATTERN 4: PAGINATION

### Cursor-Based Pagination (Recommended)

```javascript
// Request
GET /api/v1/posts?limit=20&cursor=eyJpZCI6MTIzfQ

// Response
{
  "success": true,
  "data": [
    { "id": 124, "title": "Post 1" },
    { "id": 125, "title": "Post 2" }
  ],
  "pagination": {
    "limit": 20,
    "nextCursor": "eyJpZCI6MTQ0fQ",  // Base64 encoded { "id": 144 }
    "prevCursor": "eyJpZCI6MTAzfQ",
    "hasNext": true,
    "hasPrev": true
  }
}

// Implementation
app.get('/api/v1/posts', async (req, res) => {
  const limit = parseInt(req.query.limit) || 20;
  const cursor = req.query.cursor 
    ? JSON.parse(Buffer.from(req.query.cursor, 'base64').toString())
    : null;
  
  // Query with cursor
  const query = cursor 
    ? { id: { $gt: cursor.id } }  // After cursor
    : {};
  
  const posts = await db.posts
    .find(query)
    .sort({ id: 1 })
    .limit(limit + 1);  // Fetch 1 extra to check hasNext
  
  const hasNext = posts.length > limit;
  const data = hasNext ? posts.slice(0, limit) : posts;
  
  const nextCursor = hasNext
    ? Buffer.from(JSON.stringify({ id: data[data.length - 1].id })).toString('base64')
    : null;
  
  res.json({
    success: true,
    data,
    pagination: {
      limit,
      nextCursor,
      hasNext
    }
  });
});
```

### Offset-Based Pagination (Simple)

```javascript
// Request
GET /api/v1/posts?page=2&pageSize=20

// Response
{
  "success": true,
  "data": [...],
  "pagination": {
    "page": 2,
    "pageSize": 20,
    "totalPages": 10,
    "totalItems": 200,
    "hasNext": true,
    "hasPrev": true
  }
}

// Implementation
app.get('/api/v1/posts', async (req, res) => {
  const page = parseInt(req.query.page) || 1;
  const pageSize = parseInt(req.query.pageSize) || 20;
  const skip = (page - 1) * pageSize;
  
  const [posts, totalItems] = await Promise.all([
    db.posts.find().skip(skip).limit(pageSize),
    db.posts.countDocuments()
  ]);
  
  const totalPages = Math.ceil(totalItems / pageSize);
  
  res.json({
    success: true,
    data: posts,
    pagination: {
      page,
      pageSize,
      totalPages,
      totalItems,
      hasNext: page < totalPages,
      hasPrev: page > 1
    }
  });
});
```

### Comparison

| Feature | Cursor-Based | Offset-Based |
|---------|--------------|--------------|
| **Performance** | ✅ Fast (indexed) | ⚠️ Slow (large offsets) |
| **Consistency** | ✅ No duplicates | ❌ Duplicates if data changes |
| **Jump to page** | ❌ No | ✅ Yes |
| **Total count** | ❌ Expensive | ✅ Easy |
| **Use case** | Infinite scroll, feeds | Admin tables, reports |

---

## 🔍 PATTERN 5: FILTERING & SORTING

### Query Parameters

```javascript
// Filtering
GET /api/v1/products?category=electronics&price_min=100&price_max=500&in_stock=true

// Sorting
GET /api/v1/products?sort=price:asc,created_at:desc

// Combined
GET /api/v1/products?category=electronics&sort=price:asc&page=1&pageSize=20

// Implementation
app.get('/api/v1/products', async (req, res) => {
  // Build filter
  const filter = {};
  
  if (req.query.category) {
    filter.category = req.query.category;
  }
  
  if (req.query.price_min || req.query.price_max) {
    filter.price = {};
    if (req.query.price_min) filter.price.$gte = parseFloat(req.query.price_min);
    if (req.query.price_max) filter.price.$lte = parseFloat(req.query.price_max);
  }
  
  if (req.query.in_stock === 'true') {
    filter.stock = { $gt: 0 };
  }
  
  // Build sort
  const sort = {};
  if (req.query.sort) {
    req.query.sort.split(',').forEach(field => {
      const [key, order] = field.split(':');
      sort[key] = order === 'desc' ? -1 : 1;
    });
  } else {
    sort.created_at = -1;  // Default sort
  }
  
  // Query
  const products = await db.products
    .find(filter)
    .sort(sort)
    .limit(20);
  
  res.json({
    success: true,
    data: products
  });
});
```

### Advanced Filtering (Search)

```javascript
// Full-text search
GET /api/v1/products?search=laptop&category=electronics

// Implementation
app.get('/api/v1/products', async (req, res) => {
  const filter = {};
  
  if (req.query.search) {
    filter.$text = { $search: req.query.search };
  }
  
  if (req.query.category) {
    filter.category = req.query.category;
  }
  
  const products = await db.products.find(filter);
  
  res.json({ success: true, data: products });
});
```

---

## 🔢 PATTERN 6: API VERSIONING

### URL Versioning (Recommended)

```javascript
// ✅ GOOD: Version in URL
GET /api/v1/users
GET /api/v2/users  // Breaking change

// Implementation
const express = require('express');
const app = express();

// V1 routes
const v1Router = express.Router();
v1Router.get('/users', (req, res) => {
  res.json({ version: 1, data: [...] });
});
app.use('/api/v1', v1Router);

// V2 routes (breaking change)
const v2Router = express.Router();
v2Router.get('/users', (req, res) => {
  res.json({ version: 2, data: [...] });  // Different format
});
app.use('/api/v2', v2Router);
```

### Header Versioning (Alternative)

```javascript
// Request
GET /api/users
Accept: application/vnd.myapi.v2+json

// Implementation
app.get('/api/users', (req, res) => {
  const version = req.headers.accept?.includes('v2') ? 2 : 1;
  
  if (version === 2) {
    res.json({ version: 2, data: [...] });
  } else {
    res.json({ version: 1, data: [...] });
  }
});
```

### Deprecation Strategy

```javascript
// Announce deprecation
GET /api/v1/users
Response Headers:
  Deprecation: true
  Sunset: Sat, 31 Dec 2024 23:59:59 GMT
  Link: </api/v2/users>; rel="successor-version"

// Implementation
app.use('/api/v1', (req, res, next) => {
  res.set({
    'Deprecation': 'true',
    'Sunset': 'Sat, 31 Dec 2024 23:59:59 GMT',
    'Link': '</api/v2>; rel="successor-version"'
  });
  next();
});
```

---

## ❌ PATTERN 7: ERROR RESPONSE FORMAT

### Standardized Error Response

```javascript
// Validation error (400)
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": [
      {
        "field": "email",
        "message": "Invalid email format",
        "value": "invalid-email"
      }
    ]
  },
  "meta": {
    "timestamp": "2024-03-30T10:00:00Z",
    "requestId": "req_abc123",
    "path": "/api/v1/users"
  }
}

// Not found (404)
{
  "success": false,
  "error": {
    "code": "NOT_FOUND",
    "message": "User not found",
    "resourceType": "User",
    "resourceId": "123"
  }
}

// Server error (500)
{
  "success": false,
  "error": {
    "code": "INTERNAL_ERROR",
    "message": "An unexpected error occurred",
    "reference": "ERR-2024-03-30-001"  // For support
  }
}
```

### Error Handler Middleware

```javascript
// Custom error class
class APIError extends Error {
  constructor(statusCode, code, message, details = null) {
    super(message);
    this.statusCode = statusCode;
    this.code = code;
    this.details = details;
  }
}

// Error handler middleware
app.use((err, req, res, next) => {
  // Log error
  console.error('API Error:', {
    code: err.code,
    message: err.message,
    stack: err.stack,
    requestId: req.id,
    path: req.path
  });
  
  // Determine status code
  const statusCode = err.statusCode || 500;
  
  // Build error response
  const response = {
    success: false,
    error: {
      code: err.code || 'INTERNAL_ERROR',
      message: statusCode === 500 
        ? 'An unexpected error occurred'  // Hide internal errors
        : err.message,
      ...(err.details && { details: err.details })
    },
    meta: {
      timestamp: new Date().toISOString(),
      requestId: req.id,
      path: req.path
    }
  };
  
  // Send response
  res.status(statusCode).json(response);
});

// Usage
app.post('/api/v1/users', async (req, res, next) => {
  try {
    const { error } = userSchema.validate(req.body);
    if (error) {
      throw new APIError(400, 'VALIDATION_ERROR', 'Invalid input', 
        error.details.map(d => ({
          field: d.path.join('.'),
          message: d.message
        }))
      );
    }
    
    // ... create user
    
  } catch (error) {
    next(error);  // Pass to error handler
  }
});
```

---

## 📖 PATTERN 8: OPENAPI DOCUMENTATION

### OpenAPI 3.0 Spec

```yaml
openapi: 3.0.0
info:
  title: My API
  version: 1.0.0
  description: API for managing users and posts

servers:
  - url: https://api.example.com/v1
    description: Production
  - url: https://staging-api.example.com/v1
    description: Staging

paths:
  /users:
    get:
      summary: List users
      tags:
        - Users
      parameters:
        - name: page
          in: query
          schema:
            type: integer
            default: 1
        - name: pageSize
          in: query
          schema:
            type: integer
            default: 20
      responses:
        '200':
          description: Success
          content:
            application/json:
              schema:
                type: object
                properties:
                  success:
                    type: boolean
                  data:
                    type: array
                    items:
                      $ref: '#/components/schemas/User'
                  pagination:
                    $ref: '#/components/schemas/Pagination'
    
    post:
      summary: Create user
      tags:
        - Users
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateUserRequest'
      responses:
        '201':
          description: Created
          content:
            application/json:
              schema:
                type: object
                properties:
                  success:
                    type: boolean
                  data:
                    $ref: '#/components/schemas/User'
        '400':
          description: Validation error
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ErrorResponse'

components:
  schemas:
    User:
      type: object
      properties:
        id:
          type: integer
        name:
          type: string
        email:
          type: string
          format: email
        createdAt:
          type: string
          format: date-time
    
    CreateUserRequest:
      type: object
      required:
        - name
        - email
      properties:
        name:
          type: string
          minLength: 2
        email:
          type: string
          format: email
    
    Pagination:
      type: object
      properties:
        page:
          type: integer
        pageSize:
          type: integer
        totalPages:
          type: integer
        totalItems:
          type: integer
    
    ErrorResponse:
      type: object
      properties:
        success:
          type: boolean
        error:
          type: object
          properties:
            code:
              type: string
            message:
              type: string
            details:
              type: array
              items:
                type: object
```

### Generate from Code (Express + Swagger)

```javascript
const swaggerJsdoc = require('swagger-jsdoc');
const swaggerUi = require('swagger-ui-express');

const options = {
  definition: {
    openapi: '3.0.0',
    info: {
      title: 'My API',
      version: '1.0.0'
    }
  },
  apis: ['./routes/*.js']  // Files with annotations
};

const specs = swaggerJsdoc(options);
app.use('/api-docs', swaggerUi.serve, swaggerUi.setup(specs));

// In routes/users.js
/**
 * @swagger
 * /users:
 *   get:
 *     summary: List users
 *     responses:
 *       200:
 *         description: Success
 */
app.get('/users', (req, res) => {
  // ...
});
```

---

## 📊 QUICK REFERENCE

| Aspect | Standard | Example |
|--------|----------|---------|
| **URL Format** | `/api/v{version}/{resource}` | `/api/v1/users` |
| **Resource Names** | Plural nouns, kebab-case | `/user-profiles` |
| **Success Status** | 200 (GET), 201 (POST), 204 (DELETE) | `201 Created` |
| **Error Status** | 400 (validation), 404 (not found), 500 (server) | `400 Bad Request` |
| **Pagination** | Cursor or offset-based | `?cursor=abc` or `?page=2` |
| **Filtering** | Query parameters | `?category=electronics` |
| **Sorting** | `sort=field:order` | `?sort=price:asc` |
| **Versioning** | URL versioning | `/api/v1/`, `/api/v2/` |

---

## 🚨 COMMON MISTAKES

### ❌ Mistake 1: Verbs in URLs

```javascript
// ❌ BAD
POST /api/createUser
GET  /api/getUser/123
POST /api/deleteUser/123

// ✅ GOOD
POST   /api/users
GET    /api/users/123
DELETE /api/users/123
```

### ❌ Mistake 2: Inconsistent Response Format

```javascript
// ❌ BAD: Different formats
// Endpoint 1
{ "user": { "id": 1 } }

// Endpoint 2
{ "data": { "id": 1 } }

// ✅ GOOD: Consistent envelope
{ "success": true, "data": { "id": 1 } }
```

### ❌ Mistake 3: Wrong Status Codes

```javascript
// ❌ BAD
res.status(200).json({ error: 'Not found' });  // Should be 404

// ✅ GOOD
res.status(404).json({ 
  success: false, 
  error: { code: 'NOT_FOUND', message: 'User not found' }
});
```

---

## 🎯 AI LEVERAGE

### Prompt for AI

```
"Design REST API for e-commerce with:
- Products CRUD (list, get, create, update, delete)
- Pagination (cursor-based)
- Filtering (category, price range, in stock)
- Sorting (price, created_at)
- Versioning (v1)
- OpenAPI documentation
- Follow REST best practices"
```

### AI Should

1. ✅ Use plural nouns in URLs (`/products` not `/product`)
2. ✅ Implement consistent response envelope
3. ✅ Use appropriate HTTP status codes
4. ✅ Add pagination with cursor
5. ✅ Support filtering and sorting
6. ✅ Include OpenAPI spec
7. ✅ Add error handling middleware

---

## 🔗 RELATED SKILLS

- `database-standards.md` - Database design for APIs
- `error-handling-patterns.md` - Error handling
- `security-middleware-stack.md` - API security

---

**Version:** 1.0.0  
**Last Updated:** 2026-03-30  
**Complexity:** Medium  
**Impact:** Critical (API is the contract)
