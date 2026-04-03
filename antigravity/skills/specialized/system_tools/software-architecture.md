---
name: "Software Architecture"
tags: ["analysis", "antigravity", "app", "architecture", "c:", "crud", "decision", "frontend", "gemini", "<YOUR_USERNAME>", "needs", "overview", "requirements", "rules", "scaling", "simple", "software", "specialized", "system", "team"]
tier: 3
risk: "medium"
estimated_tokens: 2806
tools_needed: ["markdown", "sql"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["web", "product"]
quality_score: 0.95
---
# Software Architecture

> **Tier:** 3-4  
> **Tags:** `architecture`, `design`, `patterns`, `scalability`, `system-design`  
> **When to use:** Designing systems, architecture decisions, scaling applications, technical leadership

---

## Overview

Software architecture patterns, principles, and practices for building scalable, maintainable systems. Covers layered architecture, microservices, event-driven design, SOLID principles, and architectural decision-making.

---

## Rules

**RULE-001: Architecture Follows Requirements**
Design architecture based on actual requirements, not trends. Consider scalability needs, team size, deployment constraints, and business goals.

```markdown
❌ Bad: Architecture for resume
"Let's use microservices because it's trendy"
# Team of 3, simple CRUD app, no scaling needs

✅ Good: Architecture for requirements
## Requirements Analysis
- Team: 3 developers
- Users: <10,000
- Traffic: <100 req/s
- Deployment: Single cloud region
- Budget: Limited

## Architecture Decision
Monolith with modular design
- Simpler deployment
- Faster development
- Lower operational cost
- Can split later if needed
```

**RULE-002: SOLID Principles**
Apply SOLID for maintainable code: Single Responsibility, Open/Closed, Liskov Substitution, Interface Segregation, Dependency Inversion.

```typescript
❌ Bad: Violates multiple SOLID principles
class UserService {
  // Violates SRP: too many responsibilities
  async createUser(data) {
    // Validate
    if (!data.email) throw new Error('Invalid');
    
    // Hash password
    const hashed = await bcrypt.hash(data.password, 10);
    
    // Save to database
    await db.query('INSERT INTO users...');
    
    // Send email
    await sendEmail(data.email, 'Welcome!');
    
    // Log
    console.log('User created');
  }
}

✅ Good: Follows SOLID
// Single Responsibility
class UserValidator {
  validate(data: UserData): void {
    if (!data.email) throw new ValidationError('Email required');
  }
}

class PasswordHasher {
  async hash(password: string): Promise<string> {
    return bcrypt.hash(password, 10);
  }
}

class UserRepository {
  async save(user: User): Promise<void> {
    await db.users.insert(user);
  }
}

class EmailService {
  async sendWelcome(email: string): Promise<void> {
    await this.send(email, 'Welcome!');
  }
}

// Dependency Inversion: depend on abstractions
class UserService {
  constructor(
    private validator: UserValidator,
    private hasher: PasswordHasher,
    private repository: UserRepository,
    private emailService: EmailService
  ) {}
  
  async createUser(data: UserData): Promise<User> {
    this.validator.validate(data);
    const hashedPassword = await this.hasher.hash(data.password);
    const user = new User({ ...data, password: hashedPassword });
    await this.repository.save(user);
    await this.emailService.sendWelcome(user.email);
    return user;
  }
}
```

**RULE-003: Layered Architecture**
Separate concerns into layers: Presentation, Application, Domain, Infrastructure. Dependencies flow inward (Dependency Inversion).

```
❌ Bad: Tangled dependencies
┌─────────────────┐
│   Controllers   │──┐
└─────────────────┘  │
         │           │
         ↓           ↓
┌─────────────────┐ ┌──────────┐
│    Database     │←│  Domain  │
└─────────────────┘ └──────────┘
# Domain depends on database (tight coupling)

✅ Good: Clean layered architecture
┌──────────────────────────────┐
│   Presentation Layer         │
│   (Controllers, Views)       │
└──────────────────────────────┘
              ↓
┌──────────────────────────────┐
│   Application Layer          │
│   (Use Cases, Services)      │
└──────────────────────────────┘
              ↓
┌──────────────────────────────┐
│   Domain Layer               │
│   (Entities, Business Logic) │
└──────────────────────────────┘
              ↑
┌──────────────────────────────┐
│   Infrastructure Layer       │
│   (Database, External APIs)  │
└──────────────────────────────┘
# Dependencies point inward
```

**RULE-004: Microservices When Needed**
Use microservices for: independent scaling, team autonomy, technology diversity. Avoid for: small teams, simple domains, tight coupling.

```markdown
❌ Bad: Premature microservices
# 3-person team, simple app
- User Service
- Auth Service
- Email Service
- Notification Service
- Analytics Service
# Result: distributed monolith, operational nightmare

✅ Good: Start modular monolith
# Single deployable with clear modules
src/
  modules/
    users/
      domain/
      application/
      infrastructure/
    auth/
    email/
    
# Split to microservices when:
- Module needs independent scaling
- Different team owns module
- Technology requirements differ
- Clear bounded context
```

**RULE-005: Event-Driven Architecture**
Use events for loose coupling, async processing, audit trails. Ensure idempotency and handle failures.

```typescript
❌ Bad: Tight coupling with sync calls
class OrderService {
  async createOrder(data: OrderData) {
    const order = await this.repository.save(data);
    
    // Tight coupling to other services
    await this.inventoryService.reserve(order.items);
    await this.paymentService.charge(order.total);
    await this.emailService.sendConfirmation(order.email);
    
    // If any fails, order is in inconsistent state
    return order;
  }
}

✅ Good: Event-driven with eventual consistency
class OrderService {
  async createOrder(data: OrderData) {
    const order = await this.repository.save(data);
    
    // Publish event (fire and forget)
    await this.eventBus.publish('order.created', {
      orderId: order.id,
      items: order.items,
      total: order.total,
      email: order.email
    });
    
    return order;
  }
}

// Separate handlers (can retry, scale independently)
class InventoryHandler {
  @Subscribe('order.created')
  async handle(event: OrderCreatedEvent) {
    await this.inventoryService.reserve(event.items);
  }
}

class PaymentHandler {
  @Subscribe('order.created')
  async handle(event: OrderCreatedEvent) {
    await this.paymentService.charge(event.total);
  }
}
```

**RULE-006: API Design Principles**
Design APIs for: consistency, versioning, backward compatibility, clear contracts, proper error handling.

```typescript
❌ Bad: Inconsistent API design
// Inconsistent naming
GET /getUsers
POST /user/create
DELETE /removeUser/:id

// No versioning
GET /api/users

// Unclear responses
{ success: true, data: [...] }
{ error: 'Something went wrong' }

✅ Good: RESTful API design
// Consistent resource-based URLs
GET    /api/v1/users
POST   /api/v1/users
GET    /api/v1/users/:id
PUT    /api/v1/users/:id
DELETE /api/v1/users/:id

// Versioning in URL
GET /api/v1/users
GET /api/v2/users  // New version, v1 still works

// Consistent response format
{
  "data": [...],
  "meta": {
    "page": 1,
    "total": 100
  }
}

// Structured errors
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid email format",
    "field": "email"
  }
}
```

**RULE-007: Database Architecture**
Choose database strategy: single database, database per service, CQRS. Consider consistency, transactions, and query patterns.

```markdown
❌ Bad: Shared database across services
┌─────────┐   ┌─────────┐   ┌─────────┐
│ Service │   │ Service │   │ Service │
│    A    │   │    B    │   │    C    │
└────┬────┘   └────┬────┘   └────┬────┘
     │             │             │
     └─────────────┼─────────────┘
                   ↓
            ┌─────────────┐
            │   Database  │
            └─────────────┘
# Tight coupling, schema changes affect all services

✅ Good: Database per service
┌─────────┐       ┌─────────┐       ┌─────────┐
│ Service │       │ Service │       │ Service │
│    A    │       │    B    │       │    C    │
└────┬────┘       └────┬────┘       └────┬────┘
     ↓                 ↓                 ↓
┌─────────┐       ┌─────────┐       ┌─────────┐
│   DB A  │       │   DB B  │       │   DB C  │
└─────────┘       └─────────┘       └─────────┘

# Loose coupling, independent evolution
# Use events for cross-service data needs
```

**RULE-008: Document Architecture Decisions**
Use Architecture Decision Records (ADRs) to document significant decisions, context, and rationale.

```markdown
# ADR-001: Use PostgreSQL for Primary Database

## Status
Accepted

## Context
Need to choose primary database for user data, orders, and inventory.

Requirements:
- ACID transactions
- Complex queries with joins
- < 100k users initially
- Budget: $200/month

Options considered:
1. PostgreSQL
2. MongoDB
3. MySQL

## Decision
Use PostgreSQL

## Rationale
- Strong ACID guarantees for financial data
- Excellent query optimizer for complex joins
- JSON support for flexible schemas where needed
- Mature ecosystem and tooling
- Cost-effective on managed services

## Consequences
Positive:
- Data consistency guaranteed
- Rich query capabilities
- Well-known by team

Negative:
- Vertical scaling limits (can address later with read replicas)
- Schema migrations require planning

## Alternatives Rejected
- MongoDB: Eventual consistency not suitable for financial data
- MySQL: PostgreSQL has better JSON support and query optimizer
```

---

## Quick Reference

### Architecture Patterns

| Pattern | Use Case | Pros | Cons |
|---------|----------|------|------|
| Monolith | Small teams, simple domains | Simple deployment, fast development | Scaling limits, tight coupling |
| Microservices | Large teams, complex domains | Independent scaling, team autonomy | Operational complexity, distributed challenges |
| Serverless | Event-driven, variable load | Auto-scaling, pay-per-use | Cold starts, vendor lock-in |
| Event-Driven | Async workflows, loose coupling | Scalability, resilience | Eventual consistency, complexity |

### SOLID Principles

```typescript
// S: Single Responsibility
class UserRepository { /* only data access */ }
class UserValidator { /* only validation */ }

// O: Open/Closed
interface PaymentProcessor {
  process(amount: number): Promise<void>;
}
class StripeProcessor implements PaymentProcessor { }
class PayPalProcessor implements PaymentProcessor { }

// L: Liskov Substitution
class Bird { fly() {} }
class Penguin extends Bird { 
  fly() { throw new Error('Cannot fly'); } // Violates LSP
}

// I: Interface Segregation
interface Printer { print(): void; }
interface Scanner { scan(): void; }
class AllInOne implements Printer, Scanner { }

// D: Dependency Inversion
class UserService {
  constructor(private repo: IUserRepository) {} // Depend on interface
}
```

### Scalability Patterns

```typescript
// Horizontal Scaling
// Add more servers behind load balancer

// Vertical Scaling
// Increase server resources (CPU, RAM)

// Caching
const cached = await cache.get(key);
if (cached) return cached;
const data = await db.query();
await cache.set(key, data, ttl);

// Database Replication
// Write to primary, read from replicas

// Sharding
// Partition data across multiple databases

// CDN
// Serve static assets from edge locations
```

---

## Metadata

- **Related Skills:** [api-design.md], [database-patterns.md], [microservices.md]
- **Dependencies:** None
- **Version:** 1.0.0
- **Last Updated:** 2024-03-26
