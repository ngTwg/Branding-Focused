---
name: "[Rule Title]"
tags: ["indexes, query-optimization, performance"]
tier: 2
risk: "medium"
estimated_tokens: 260
tools_needed: ["markdown", "sql"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["platform", "api"]
quality_score: 0.56
impact: "MEDIUM"
impactDescription: "5-20x query speedup for filtered queries"
title: "Clear, Action-Oriented Title (e.g., \"Use Partial Indexes for Filtered Queries\")"
---
## [Rule Title]

[1-2 sentence explanation of the problem and why it matters. Focus on performance impact.]

**Incorrect (describe the problem):**

```sql
-- Comment explaining what makes this slow/problematic
CREATE INDEX users_email_idx ON users(email);

SELECT * FROM users WHERE email = 'user@example.com' AND deleted_at IS NULL;
-- This scans deleted records unnecessarily
```

**Correct (describe the solution):**

```sql
-- Comment explaining why this is better
CREATE INDEX users_active_email_idx ON users(email) WHERE deleted_at IS NULL;

SELECT * FROM users WHERE email = 'user@example.com' AND deleted_at IS NULL;
-- Only indexes active users, 10x smaller index, faster queries
```

[Optional: Additional context, edge cases, or trade-offs]

Reference: [Postgres Docs](https://www.postgresql.org/docs/current/)
