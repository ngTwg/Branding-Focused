---
name: "Use Covering Indexes to Avoid Table Lookups"
tags: ["indexes, covering-index, include, index-only-scan"]
tier: 2
risk: "medium"
estimated_tokens: 321
tools_needed: ["markdown", "sql"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["platform", "api"]
quality_score: 0.60
impact: "MEDIUM-HIGH"
impactDescription: "2-5x faster queries by eliminating heap fetches"
title: "Use Covering Indexes to Avoid Table Lookups"
---
## Use Covering Indexes to Avoid Table Lookups

Covering indexes include all columns needed by a query, enabling index-only scans that skip the table entirely.

**Incorrect (index scan + heap fetch):**

```sql
create index users_email_idx on users (email);

-- Must fetch name and created_at from table heap
select email, name, created_at from users where email = 'user@example.com';
```

**Correct (index-only scan with INCLUDE):**

```sql
-- Include non-searchable columns in the index
create index users_email_idx on users (email) include (name, created_at);

-- All columns served from index, no table access needed
select email, name, created_at from users where email = 'user@example.com';
```

Use INCLUDE for columns you SELECT but don't filter on:

```sql
-- Searching by status, but also need customer_id and total
create index orders_status_idx on orders (status) include (customer_id, total);

select status, customer_id, total from orders where status = 'shipped';
```

Reference: [Index-Only Scans](https://www.postgresql.org/docs/current/indexes-index-only-scans.html)
