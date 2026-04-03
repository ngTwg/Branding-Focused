---
name: "💎 Skill: Prisma Expert"
tags: ["activation", "antigravity", "backend", "benchmark", "c:", "execution", "expert", "gemini", "<YOUR_USERNAME>", "output", "pipeline", "prisma", "signals", "signature", "skill", "steps", "sub", "task", "users"]
tier: 3
risk: "medium"
estimated_tokens: 304
tools_needed: ["markdown", "sql", "terminal"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["platform", "api"]
quality_score: 0.58
---
# 💎 Skill: Prisma Expert

> **PURPOSE:** Professional Type-Safe Database ORM (Prisma) for migrations, queries, and schema design.
> **CATEGORY:** Backend
> **TIER:** 2+

---

## 🚦 ACTIVATION SIGNALS

- Keywords: `Prisma`, `db push`, `db migrate`, `prisma-client`.
- Task: Database schema design, query optimization, or complex relations.

---

## 🛠️ SUB-STEPS (EXECUTION PIPELINE)

1. **Schema Design**: Create `schema.prisma` with models, enums, and relations (1:1, 1:n, m:n).
2. **Migrations**: Apply `prisma migrate dev` or `prisma db push` depending on the environment.
3. **Query Implementation**: Use `PrismaClient` with `include`, `select`, and `where` for type-safe data access.
4. **Relations Management**: Map complex relationships (composite keys, self-relations).
5. **Optimization**: Check query performance and implement indexing and raw SQL if necessary.

---

## 📝 OUTPUT SIGNATURE

- `schema.prisma` files.
- Prisma query implementations.
- Raw SQL migration scripts.

---

## 🧪 BENCHMARK TASK

- **Input**: "Design a many-to-many relationship between Products and Categories with Prisma."
- **Output**: schema.prisma with joint table (implicit or explicit) -> Query fetching categories for a product.
