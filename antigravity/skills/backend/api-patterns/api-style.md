---
name: "API Style Selection (2025)"
tags: ["2025", "antigravity", "api", "backend", "c:", "comparison", "decision", "frontend", "gemini", "<YOUR_USERNAME>", "patterns", "questions", "selection", "style", "tree", "users"]
tier: 3
risk: "medium"
estimated_tokens: 269
tools_needed: ["markdown", "terminal"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["web", "product"]
quality_score: 0.58
---
# API Style Selection (2025)

> REST vs GraphQL vs tRPC - Hangi durumda hangisi?

## Decision Tree

```
Who are the API consumers?
│
├── Public API / Multiple platforms
│   └── REST + OpenAPI (widest compatibility)
│
├── Complex data needs / Multiple frontends
│   └── GraphQL (flexible queries)
│
├── TypeScript frontend + backend (monorepo)
│   └── tRPC (end-to-end type safety)
│
├── Real-time / Event-driven
│   └── WebSocket + AsyncAPI
│
└── Internal microservices
    └── gRPC (performance) or REST (simplicity)
```

## Comparison

| Factor | REST | GraphQL | tRPC |
|--------|------|---------|------|
| **Best for** | Public APIs | Complex apps | TS monorepos |
| **Learning curve** | Low | Medium | Low (if TS) |
| **Over/under fetching** | Common | Solved | Solved |
| **Type safety** | Manual (OpenAPI) | Schema-based | Automatic |
| **Caching** | HTTP native | Complex | Client-based |

## Selection Questions

1. Who are the API consumers?
2. Is the frontend TypeScript?
3. How complex are the data relationships?
4. Is caching critical?
5. Public or internal API?
