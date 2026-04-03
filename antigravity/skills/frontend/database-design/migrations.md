---
name: "Migration Principles"
tags: ["antigravity", "c:", "database", "databases", "design", "edge", "frontend", "gemini", "<YOUR_USERNAME>", "migration", "migrations", "neon", "philosophy", "postgresql", "principles", "safe", "serverless", "sqlite", "strategy", "turso"]
tier: 3
risk: "medium"
estimated_tokens: 257
tools_needed: ["markdown", "sql"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["web", "product"]
quality_score: 0.62
---
# Migration Principles

> Safe migration strategy for zero-downtime changes.

## Safe Migration Strategy

```
For zero-downtime changes:
│
├── Adding column
│   └── Add as nullable → backfill → add NOT NULL
│
├── Removing column
│   └── Stop using → deploy → remove column
│
├── Adding index
│   └── CREATE INDEX CONCURRENTLY (non-blocking)
│
└── Renaming column
    └── Add new → migrate data → deploy → drop old
```

## Migration Philosophy

- Never make breaking changes in one step
- Test migrations on data copy first
- Have rollback plan
- Run in transaction when possible

## Serverless Databases

### Neon (Serverless PostgreSQL)

| Feature | Benefit |
|---------|---------|
| Scale to zero | Cost savings |
| Instant branching | Dev/preview |
| Full PostgreSQL | Compatibility |
| Autoscaling | Traffic handling |

### Turso (Edge SQLite)

| Feature | Benefit |
|---------|---------|
| Edge locations | Ultra-low latency |
| SQLite compatible | Simple |
| Generous free tier | Cost |
| Global distribution | Performance |
