# DOCUMENTATION STANDARDS - CHUẨN TÀI LIỆU BẮT BUỘC

> **Tier:** 1-4 (All projects)  
> **Tags:** `[documentation, readme, adr, comments, maintainability]`  
> **Khi nào dùng:** Mọi project mới, mọi thay đổi architecture

---

## 🎯 OVERVIEW

Thiếu documentation là một trong những nguyên nhân chính khiến onboarding mất 2 tháng thay vì 1-2 tuần. AI code thường thiếu hoặc có documentation kém chất lượng.

**Mục tiêu:** 
- Onboarding developer mới trong < 2 tuần
- Hiểu architecture trong < 1 ngày
- Tìm được code cần sửa trong < 30 phút

---

## 📋 REQUIRED FILES - BẮT BUỘC

### 1. README.md (MANDATORY)

#### Template
```markdown
# Project Name

> One-line description of what this project does

## What it does

[2-3 sentences explaining the purpose and main features]

## Quick Start

\`\`\`bash
# Install dependencies
npm install

# Setup environment
cp .env.example .env
# Edit .env with your values

# Run development server
npm run dev
\`\`\`

Open [http://localhost:3000](http://localhost:3000)

## Tech Stack

- **Frontend:** React 18 + TypeScript + Tailwind CSS
- **Backend:** Node.js 20 + Express + Prisma
- **Database:** PostgreSQL 15
- **Auth:** NextAuth.js
- **Deployment:** Vercel

## Project Structure

See [PROJECT_MAP.md](PROJECT_MAP.md) for detailed architecture.

## Development

\`\`\`bash
npm run dev          # Start dev server
npm run build        # Build for production
npm run test         # Run tests
npm run lint         # Lint code
npm run type-check   # TypeScript check
\`\`\`

## Environment Variables

See [.env.example](.env.example) for all required variables.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md)

## License

MIT
```

#### Checklist:
- [ ] Project name và description
- [ ] Quick start commands (< 5 steps)
- [ ] Tech stack list
- [ ] Link to PROJECT_MAP.md
- [ ] Development commands
- [ ] Environment variables reference
- [ ] License

---

### 2. PROJECT_MAP.md (MANDATORY)

#### Template
```markdown
# Project Map - [Project Name]

> Architectural overview and navigation guide

## Tech Stack Details

### Frontend
- **Framework:** React 18.2.0
- **Language:** TypeScript 5.3
- **Styling:** Tailwind CSS 3.4
- **State:** Zustand + TanStack Query
- **Forms:** React Hook Form + Zod
- **Routing:** Next.js 14 App Router

### Backend
- **Runtime:** Node.js 20 LTS
- **Framework:** Express 4.18
- **ORM:** Prisma 5.8
- **Validation:** Zod
- **Auth:** JWT + bcrypt

### Database
- **Primary:** PostgreSQL 15
- **Cache:** Redis 7
- **Search:** (if applicable)

### Infrastructure
- **Hosting:** Vercel (frontend), Railway (backend)
- **CDN:** Cloudflare
- **Monitoring:** Sentry
- **Analytics:** (if applicable)

## Folder Structure

\`\`\`
project-root/
├── src/
│   ├── app/                 # Next.js App Router pages
│   │   ├── (auth)/         # Auth-protected routes
│   │   ├── api/            # API routes
│   │   └── layout.tsx      # Root layout
│   │
│   ├── components/          # React components
│   │   ├── ui/             # Reusable UI components
│   │   ├── forms/          # Form components
│   │   └── layouts/        # Layout components
│   │
│   ├── lib/                 # Utilities & helpers
│   │   ├── db.ts           # Database connection
│   │   ├── auth.ts         # Auth utilities
│   │   ├── api.ts          # API client
│   │   └── utils.ts        # General utilities
│   │
│   ├── types/               # TypeScript types
│   │   ├── api.ts          # API types
│   │   ├── models.ts       # Database models
│   │   └── index.ts        # Exported types
│   │
│   ├── hooks/               # Custom React hooks
│   │   ├── useAuth.ts
│   │   ├── useUser.ts
│   │   └── useOrders.ts
│   │
│   └── styles/              # Global styles
│       └── globals.css
│
├── prisma/                  # Database schema & migrations
│   ├── schema.prisma
│   └── migrations/
│
├── public/                  # Static assets
├── tests/                   # Test files
└── docs/                    # Additional documentation
    └── adr/                # Architecture Decision Records
\`\`\`

## Key Files & Their Purpose

### Core Application
- \`src/app/layout.tsx\` - Root layout, providers, global setup
- \`src/lib/db.ts\` - Prisma client singleton
- \`src/lib/auth.ts\` - Authentication logic (JWT, session)
- \`src/lib/api.ts\` - API client with interceptors

### API Routes
- \`src/app/api/auth/[...nextauth]/route.ts\` - NextAuth endpoints
- \`src/app/api/users/route.ts\` - User CRUD
- \`src/app/api/orders/route.ts\` - Order management

### Database
- \`prisma/schema.prisma\` - Database schema
- \`src/lib/db.ts\` - Connection & query helpers

## Data Flow

### Authentication Flow
\`\`\`
1. User submits login form
   → POST /api/auth/login
   
2. Server validates credentials
   → Check bcrypt hash
   → Generate JWT token
   
3. Return token to client
   → Store in httpOnly cookie
   
4. Client includes token in requests
   → Middleware validates JWT
   → Attach user to request
\`\`\`

### Order Creation Flow
\`\`\`
1. User fills order form
   → React Hook Form validation
   
2. Submit to API
   → POST /api/orders
   
3. Server validation
   → Zod schema validation
   → Check inventory
   → Check user permissions
   
4. Database transaction
   → Create order record
   → Update inventory
   → Create audit log
   
5. Send confirmation
   → Email notification
   → Return order data
   
6. Update UI
   → TanStack Query invalidates cache
   → Refetch orders list
\`\`\`

## Environment Variables

### Required
- \`DATABASE_URL\` - PostgreSQL connection string
- \`NEXTAUTH_SECRET\` - Auth secret (32+ chars)
- \`NEXTAUTH_URL\` - App URL (http://localhost:3000)

### Optional
- \`REDIS_URL\` - Redis connection (for caching)
- \`SENTRY_DSN\` - Error tracking
- \`SMTP_HOST\` - Email server

See [.env.example](.env.example) for full list.

## Common Tasks

### Add a new API endpoint
1. Create file in \`src/app/api/[resource]/route.ts\`
2. Define Zod schema for validation
3. Implement handler (GET/POST/PUT/DELETE)
4. Add tests in \`tests/api/[resource].test.ts\`
5. Update API documentation

### Add a new database table
1. Update \`prisma/schema.prisma\`
2. Run \`npx prisma migrate dev --name add_table_name\`
3. Generate types: \`npx prisma generate\`
4. Create TypeScript types in \`src/types/models.ts\`
5. Document in ADR if significant change

### Add a new page
1. Create file in \`src/app/[route]/page.tsx\`
2. Add metadata export
3. Implement page component
4. Add to navigation if needed
5. Add tests

## Architecture Decisions

See \`docs/adr/\` for all Architecture Decision Records:
- [ADR-001: Use PostgreSQL](docs/adr/ADR-001-use-postgresql.md)
- [ADR-002: Use Next.js App Router](docs/adr/ADR-002-nextjs-app-router.md)
- [ADR-003: Use Prisma ORM](docs/adr/ADR-003-prisma-orm.md)

## Troubleshooting

### Database connection fails
- Check \`DATABASE_URL\` in .env
- Ensure PostgreSQL is running
- Run \`npx prisma db push\` to sync schema

### Build fails
- Clear \`.next\` folder: \`rm -rf .next\`
- Clear node_modules: \`rm -rf node_modules && npm install\`
- Check TypeScript errors: \`npm run type-check\`

### Tests fail
- Ensure test database is setup
- Run migrations: \`npx prisma migrate deploy\`
- Clear test cache: \`npm run test -- --clearCache\`

## Performance Considerations

- **Database:** Indexes on \`user_id\`, \`created_at\`, \`status\`
- **Caching:** Redis for session data, TanStack Query for API responses
- **Images:** Next.js Image component with optimization
- **Bundle:** Code splitting with dynamic imports

## Security Notes

- All passwords hashed with bcrypt (12 rounds)
- JWT tokens expire after 7 days
- CSRF protection enabled
- Rate limiting on auth endpoints (5 req/15min)
- Input validation with Zod on all endpoints
- SQL injection prevented by Prisma parameterized queries

---

**Last Updated:** 2026-03-30  
**Maintainer:** [Team Name]
```

#### Checklist:
- [ ] Tech stack với versions
- [ ] Folder structure với explanations
- [ ] Key files list
- [ ] Data flow diagrams
- [ ] Environment variables
- [ ] Common tasks guide
- [ ] Troubleshooting section
- [ ] Performance notes
- [ ] Security notes

---

### 3. ADR Template (Architecture Decision Records)

#### When to create ADR:
- Choosing database (SQL vs NoSQL)
- Choosing framework (React vs Vue)
- Choosing architecture pattern (monolith vs microservices)
- Major library decisions (ORM, state management)
- Infrastructure decisions (hosting, CI/CD)

#### Template: docs/adr/ADR-XXX-title.md
```markdown
# ADR-XXX: [Decision Title]

## Status

[Proposed | Accepted | Deprecated | Superseded by ADR-YYY]

## Context

[Describe the problem/situation that requires a decision]

Example:
We need to choose a database for our user management system. 
Requirements:
- Store user profiles, orders, products
- Support transactions
- Handle 10K+ users
- Need strong data consistency
- Team familiar with SQL

## Decision

[State the decision clearly]

Example:
We will use PostgreSQL with Prisma ORM.

## Rationale

[Explain WHY this decision was made]

Example:
- PostgreSQL provides ACID transactions
- Prisma gives type-safe database access
- Team has SQL experience
- Strong ecosystem and community
- Excellent performance for our scale

## Consequences

### Positive
- [List benefits]
- Strong typing with Prisma
- ACID transactions guarantee data consistency
- Rich query capabilities
- Good tooling (Prisma Studio, migrations)

### Negative
- [List drawbacks]
- Less flexible schema than NoSQL
- Requires migrations for schema changes
- Vertical scaling limits (though sufficient for our needs)

### Neutral
- [List neutral impacts]
- Need to learn Prisma if not familiar
- PostgreSQL hosting required

## Alternatives Considered

### MongoDB
- **Pros:** Flexible schema, horizontal scaling
- **Cons:** No ACID transactions, team unfamiliar, overkill for our needs
- **Why rejected:** Need strong consistency, relational data

### MySQL
- **Pros:** Similar to PostgreSQL, widely used
- **Cons:** Less modern features than PostgreSQL
- **Why rejected:** PostgreSQL has better JSON support and extensions

### SQLite
- **Pros:** Simple, no server needed
- **Cons:** Not suitable for production, no concurrent writes
- **Why rejected:** Need production-grade database

## Implementation Notes

- Use Prisma 5.x
- Setup connection pooling (max 10 connections)
- Enable query logging in development
- Use migrations for all schema changes
- Backup strategy: daily automated backups

## References

- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Prisma Documentation](https://www.prisma.io/docs/)
- [Why Postgres](https://www.postgresql.org/about/)

---

**Date:** 2026-03-30  
**Author:** [Your Name]  
**Reviewers:** [Team Members]
```

#### Checklist:
- [ ] Clear problem statement (Context)
- [ ] Clear decision (Decision)
- [ ] Reasoning explained (Rationale)
- [ ] Pros and cons listed (Consequences)
- [ ] Alternatives considered
- [ ] Implementation notes
- [ ] References/links

---

## 📝 CODE DOCUMENTATION

### JSDoc/TSDoc Standards (TypeScript/JavaScript)

#### RULE-DOC-001: Every exported function MUST have JSDoc
```typescript
/**
 * Fetches user data from database by ID
 * 
 * @param userId - The unique identifier of the user
 * @returns User object if found, null otherwise
 * @throws {DatabaseError} If database connection fails
 * @throws {ValidationError} If userId is invalid format
 * 
 * @example
 * ```typescript
 * const user = await getUser('user-123');
 * if (user) {
 *   console.log(user.email);
 * }
 * ```
 */
export async function getUser(userId: string): Promise<User | null> {
  // Implementation
}
```

#### RULE-DOC-002: Complex algorithms MUST have explanation
```typescript
/**
 * Implements Dijkstra's shortest path algorithm
 * 
 * **Algorithm:** Dijkstra's shortest path
 * **Time complexity:** O((V + E) log V) where V = vertices, E = edges
 * **Space complexity:** O(V) for priority queue and distances
 * 
 * **Why this algorithm:**
 * - Need to find shortest path in weighted graph
 * - All edge weights are positive (requirement)
 * - Graph is sparse (E << V²), so Dijkstra is optimal
 * 
 * **Alternative considered:** A* algorithm
 * - Rejected: Overkill for our use case, no heuristic available
 * 
 * @param graph - Adjacency list representation
 * @param start - Starting vertex ID
 * @param end - Target vertex ID
 * @returns Shortest path as array of vertex IDs, or null if no path
 */
function dijkstra(
  graph: Graph,
  start: string,
  end: string
): string[] | null {
  // Implementation
}
```

#### RULE-DOC-003: Classes MUST have description
```typescript
/**
 * Service for managing user authentication and sessions
 * 
 * Handles:
 * - User login/logout
 * - JWT token generation and validation
 * - Session management
 * - Password hashing and verification
 * 
 * @example
 * ```typescript
 * const authService = new AuthService(db, config);
 * const token = await authService.login(email, password);
 * ```
 */
export class AuthService {
  // Implementation
}
```

---

### Python Docstrings (Google Style)

#### RULE-DOC-004: Every public function MUST have docstring
```python
def get_user(user_id: str) -> User | None:
    """Fetches user data from database by ID.
    
    Args:
        user_id: The unique identifier of the user.
        
    Returns:
        User object if found, None otherwise.
        
    Raises:
        DatabaseError: If database connection fails.
        ValidationError: If user_id is invalid format.
        
    Example:
        >>> user = get_user('user-123')
        >>> if user:
        ...     print(user.email)
    """
    # Implementation
```

---

## 💬 COMMENT GUIDELINES

### When to Comment

#### ✅ DO Comment:
1. **WHY, not WHAT** - Explain reasoning, not obvious code
2. **Complex logic** - Algorithm explanation
3. **Workarounds** - Why this hack exists
4. **TODOs** - What needs to be done
5. **Warnings** - Potential pitfalls

#### ❌ DON'T Comment:
1. **Obvious code** - `x = x + 1 // increment x`
2. **Redundant** - Repeating function name
3. **Outdated** - Comments that don't match code
4. **Commented code** - Delete it, use git history

### Examples

```typescript
✅ GOOD - Explains WHY
// Add 1 because API returns 0-indexed pages but UI displays 1-indexed
const displayPage = apiPage + 1;

// Use setTimeout instead of setInterval to prevent overlapping requests
// if previous request takes longer than interval
setTimeout(fetchData, 5000);

// HACK: Workaround for Safari bug where flexbox doesn't respect min-height
// See: https://bugs.webkit.org/show_bug.cgi?id=137730
// TODO: Remove when Safari fixes this (check in Q2 2026)
.container {
  min-height: 1px;
}

❌ BAD - States the obvious
// Increment x by 1
x = x + 1;

// Get user by ID
const user = await getUser(id);

// Loop through array
for (const item of items) {
  // Process item
  process(item);
}
```

---

## 🔗 API DOCUMENTATION

### OpenAPI/Swagger (REST APIs)

#### RULE-DOC-005: Every endpoint MUST have OpenAPI spec
```yaml
/api/users/{id}:
  get:
    summary: Get user by ID
    description: Fetches a single user's data by their unique identifier
    tags:
      - Users
    parameters:
      - name: id
        in: path
        required: true
        description: User's unique identifier
        schema:
          type: string
          format: uuid
    responses:
      '200':
        description: User found
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/User'
            example:
              id: "user-123"
              email: "john@example.com"
              name: "John Doe"
              createdAt: "2026-03-30T10:00:00Z"
      '404':
        description: User not found
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/Error'
            example:
              error: "USER_NOT_FOUND"
              message: "User with ID 'user-123' not found"
      '401':
        description: Unauthorized - missing or invalid token
      '500':
        description: Internal server error
    security:
      - bearerAuth: []
```

---

## ✅ DOCUMENTATION CHECKLIST

### New Project Checklist
- [ ] README.md created with quick start
- [ ] PROJECT_MAP.md created with architecture
- [ ] .env.example created with all variables
- [ ] First ADR created (major tech decisions)
- [ ] CONTRIBUTING.md created (if open source)
- [ ] LICENSE file added

### Before Merge Checklist
- [ ] README updated if new features added
- [ ] PROJECT_MAP updated if architecture changed
- [ ] ADR created if major decision made
- [ ] JSDoc/docstrings added to new functions
- [ ] Comments added to complex logic
- [ ] API docs updated if endpoints changed

### Quarterly Review Checklist
- [ ] README still accurate
- [ ] PROJECT_MAP reflects current architecture
- [ ] ADRs up to date
- [ ] Outdated comments removed
- [ ] Documentation links still work

---

## 🎯 AI LEVERAGE

### Documentation Generation Prompt
```markdown
Generate documentation for this code:

1. README.md section:
   - Feature description
   - Usage example
   - Configuration options

2. JSDoc/docstring:
   - Function purpose
   - Parameters with types
   - Return value
   - Exceptions
   - Example usage

3. Comments:
   - Explain WHY for complex logic
   - No obvious comments
   - Include references if applicable

Format: [Language-specific style]
```

---

## 📚 QUICK REFERENCE

| Document | When | Required | Format |
|----------|------|----------|--------|
| README.md | New project | ✅ Yes | Markdown |
| PROJECT_MAP.md | New project | ✅ Yes | Markdown |
| ADR | Major decision | ✅ Yes | Markdown |
| JSDoc | Public function | ✅ Yes | JSDoc |
| Comments | Complex logic | ⚠️ When needed | Inline |
| OpenAPI | API endpoint | ✅ Yes | YAML/JSON |

---

## 🔗 RELATED SKILLS

- `workflows/code-review.md` - Documentation review checklist
- `backend/api-design-standards.md` - API documentation standards
- `workflows/refactoring-triggers.md` - When to update docs

---

**Version:** 1.0.0  
**Last Updated:** 2026-03-30  
**Status:** ✅ MANDATORY - All projects must have proper documentation
