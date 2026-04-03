---
name: "GraphQL Principles"
tags: ["antigravity", "api", "backend", "c:", "considerations", "design", "frontend", "gemini", "graphql", "<YOUR_USERNAME>", "patterns", "principles", "schema", "security", "use", "users", "when"]
tier: 2
risk: "medium"
estimated_tokens: 214
tools_needed: ["markdown", "terminal"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["web", "product"]
quality_score: 0.64
---
# GraphQL Principles

> Flexible queries for complex, interconnected data.

## When to Use

```
✅ Good fit:
├── Complex, interconnected data
├── Multiple frontend platforms
├── Clients need flexible queries
├── Evolving data requirements
└── Reducing over-fetching matters

❌ Poor fit:
├── Simple CRUD operations
├── File upload heavy
├── HTTP caching important
└── Team unfamiliar with GraphQL
```

## Schema Design Principles

```
Principles:
├── Think in graphs, not endpoints
├── Design for evolvability (no versions)
├── Use connections for pagination
├── Be specific with types (not generic "data")
└── Handle nullability thoughtfully
```

## Security Considerations

```
Protect against:
├── Query depth attacks → Set max depth
├── Query complexity → Calculate cost
├── Batching abuse → Limit batch size
├── Introspection → Disable in production
```
