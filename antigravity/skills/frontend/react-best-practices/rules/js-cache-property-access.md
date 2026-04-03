---
name: "Cache Property Access in Loops"
tags: ["javascript, loops, optimization, caching"]
tier: 2
risk: "medium"
estimated_tokens: 132
tools_needed: ["markdown"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["web", "product"]
quality_score: 0.55
impact: "LOW-MEDIUM"
impactDescription: "reduces lookups"
title: "Cache Property Access in Loops"
---
## Cache Property Access in Loops

Cache object property lookups in hot paths.

**Incorrect (3 lookups × N iterations):**

```typescript
for (let i = 0; i < arr.length; i++) {
  process(obj.config.settings.value)
}
```

**Correct (1 lookup total):**

```typescript
const value = obj.config.settings.value
const len = arr.length
for (let i = 0; i < len; i++) {
  process(value)
}
```
