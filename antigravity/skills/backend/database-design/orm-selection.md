---
name: "ORM Selection (2025)"
tags: ["2025", "antigravity", "backend", "c:", "comparison", "database", "decision", "design", "frontend", "gemini", "<YOUR_USERNAME>", "orm", "selection", "tree", "users"]
tier: 2
risk: "medium"
estimated_tokens: 177
tools_needed: ["markdown", "sql", "terminal"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["web", "product"]
quality_score: 0.55
---
# ORM Selection (2025)

> Choose ORM based on deployment and DX needs.

## Decision Tree

```
What's the context?
│
├── Edge deployment / Bundle size matters
│   └── Drizzle (smallest, SQL-like)
│
├── Best DX / Schema-first
│   └── Prisma (migrations, studio)
│
├── Maximum control
│   └── Raw SQL with query builder
│
└── Python ecosystem
    └── SQLAlchemy 2.0 (async support)
```

## Comparison

| ORM | Best For | Trade-offs |
|-----|----------|------------|
| **Drizzle** | Edge, TypeScript | Newer, less examples |
| **Prisma** | DX, schema management | Heavier, not edge-ready |
| **Kysely** | Type-safe SQL builder | Manual migrations |
| **Raw SQL** | Complex queries, control | Manual type safety |
