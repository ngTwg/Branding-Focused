---
name: "Per-Request Deduplication with React.cache()"
tags: ["server, cache, react-cache, deduplication"]
tier: 2
risk: "medium"
estimated_tokens: 170
tools_needed: ["markdown"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["web", "product"]
quality_score: 0.52
impact: "MEDIUM"
impactDescription: "deduplicates within request"
title: "Per-Request Deduplication with React.cache()"
---
## Per-Request Deduplication with React.cache()

Use `React.cache()` for server-side request deduplication. Authentication and database queries benefit most.

**Usage:**

```typescript
import { cache } from 'react'

export const getCurrentUser = cache(async () => {
  const session = await auth()
  if (!session?.user?.id) return null
  return await db.user.findUnique({
    where: { id: session.user.id }
  })
})
```

Within a single request, multiple calls to `getCurrentUser()` execute the query only once.
