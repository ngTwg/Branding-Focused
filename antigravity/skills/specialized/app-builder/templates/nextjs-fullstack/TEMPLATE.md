---
name: "nextjs-fullstack"
tags: ["antigravity", "app", "builder", "c:", "concepts", "directory", "environment", "frontend", "full", "fullstack", "gemini", "key", "<YOUR_USERNAME>", "next", "nextjs", "setup", "specialized", "stack", "steps", "structure"]
tier: 2
risk: "medium"
estimated_tokens: 371
tools_needed: ["markdown", "sql"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["web", "product"]
quality_score: 0.66
description: "Next.js full-stack template principles. App Router, Prisma, Tailwind."
---
# Next.js Full-Stack Template

## Tech Stack

| Component | Technology |
|-----------|------------|
| Framework | Next.js 14 (App Router) |
| Language | TypeScript |
| Database | PostgreSQL + Prisma |
| Styling | Tailwind CSS |
| Auth | Clerk (optional) |
| Validation | Zod |

---

## Directory Structure

```
project-name/
├── prisma/
│   └── schema.prisma
├── src/
│   ├── app/
│   │   ├── layout.tsx
│   │   ├── page.tsx
│   │   ├── globals.css
│   │   └── api/
│   ├── components/
│   │   └── ui/
│   ├── lib/
│   │   ├── db.ts        # Prisma client
│   │   └── utils.ts
│   └── types/
├── .env.example
└── package.json
```

---

## Key Concepts

| Concept | Description |
|---------|-------------|
| Server Components | Default, fetch data |
| Server Actions | Form mutations |
| Route Handlers | API endpoints |
| Prisma | Type-safe ORM |

---

## Environment Variables

| Variable | Purpose |
|----------|---------|
| DATABASE_URL | Prisma connection |
| NEXT_PUBLIC_APP_URL | Public URL |

---

## Setup Steps

1. `npx create-next-app {{name}} --typescript --tailwind --app`
2. `npm install prisma @prisma/client zod`
3. `npx prisma init`
4. Configure schema
5. `npm run db:push`
6. `npm run dev`

---

## Best Practices

- Server Components by default
- Server Actions for mutations
- Prisma for type-safe DB
- Zod for validation
- Edge runtime where possible
