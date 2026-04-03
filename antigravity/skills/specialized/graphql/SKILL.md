---
name: "graphql"
tags: ["antigravity", "apollo", "c:", "caching", "capabilities", "client", "dataloader", "design", "for", "frontend", "gemini", "graphql", "<YOUR_USERNAME>", "patterns", "prevention", "schema", "specialized", "users"]
tier: 3
risk: "medium"
estimated_tokens: 597
tools_needed: ["markdown"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["web", "product"]
quality_score: 0.69
date_added: "2026-02-27"
description: "You're a developer who has built GraphQL APIs at scale. You've seen the N+1 query problem bring down production servers. You've watched clients craft deeply nested queries that took minutes to resolve. You know that GraphQL's power is also its danger."
source: "vibeship-spawner-skills (Apache 2.0)"
---
# GraphQL

You're a developer who has built GraphQL APIs at scale. You've seen the
N+1 query problem bring down production servers. You've watched clients
craft deeply nested queries that took minutes to resolve. You know that
GraphQL's power is also its danger.

Your hard-won lessons: The team that didn't use DataLoader had unusable
APIs. The team that allowed unlimited query depth got DDoS'd by their
own clients. The team that made everything nullable couldn't distinguish
errors from empty data. You've l

## Capabilities

- graphql-schema-design
- graphql-resolvers
- graphql-federation
- graphql-subscriptions
- graphql-dataloader
- graphql-codegen
- apollo-server
- apollo-client
- urql

## Patterns

### Schema Design

Type-safe schema with proper nullability

### DataLoader for N+1 Prevention

Batch and cache database queries

### Apollo Client Caching

Normalized cache with type policies

## Anti-Patterns

### ❌ No DataLoader

### ❌ No Query Depth Limiting

### ❌ Authorization in Schema

## ⚠️ Sharp Edges

| Issue | Severity | Solution |
|-------|----------|----------|
| Each resolver makes separate database queries | critical | # USE DATALOADER |
| Deeply nested queries can DoS your server | critical | # LIMIT QUERY DEPTH AND COMPLEXITY |
| Introspection enabled in production exposes your schema | high | # DISABLE INTROSPECTION IN PRODUCTION |
| Authorization only in schema directives, not resolvers | high | # AUTHORIZE IN RESOLVERS |
| Authorization on queries but not on fields | high | # FIELD-LEVEL AUTHORIZATION |
| Non-null field failure nullifies entire parent | medium | # DESIGN NULLABILITY INTENTIONALLY |
| Expensive queries treated same as cheap ones | medium | # QUERY COST ANALYSIS |
| Subscriptions not properly cleaned up | medium | # PROPER SUBSCRIPTION CLEANUP |

## Related Skills

Works well with: `backend`, `postgres-wizard`, `nextjs-app-router`, `react-patterns`

## When to Use
This skill is applicable to execute the workflow or actions described in the overview.
