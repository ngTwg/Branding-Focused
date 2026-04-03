---
name: "Use Set/Map for O(1) Lookups"
tags: ["javascript, set, map, data-structures, performance"]
tier: 2
risk: "medium"
estimated_tokens: 133
tools_needed: ["markdown"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["web", "product"]
quality_score: 0.55
impact: "LOW-MEDIUM"
impactDescription: "O(n) to O(1)"
title: "Use Set/Map for O(1) Lookups"
---
## Use Set/Map for O(1) Lookups

Convert arrays to Set/Map for repeated membership checks.

**Incorrect (O(n) per check):**

```typescript
const allowedIds = ['a', 'b', 'c', ...]
items.filter(item => allowedIds.includes(item.id))
```

**Correct (O(1) per check):**

```typescript
const allowedIds = new Set(['a', 'b', 'c', ...])
items.filter(item => allowedIds.has(item.id))
```
