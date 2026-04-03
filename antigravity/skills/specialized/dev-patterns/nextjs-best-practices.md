---
name: "nextjs-best-practices"
tags: ["actions", "antigravity", "best", "c:", "component", "data", "dev", "fetching", "frontend", "gemini", "<YOUR_USERNAME>", "next", "nextjs", "optimization", "patterns", "performance", "practices", "related", "server", "skills"]
tier: 2
risk: "medium"
estimated_tokens: 379
tools_needed: ["markdown"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["web", "product"]
quality_score: 0.61
description: "Best practices for Next.js (App Router), focusing on server components, client components, and data fetching."
---
# Next.js Best Practices (v6.5.0-SLIM)

Guidelines for performant and maintainable Next.js 14/15 applications.

## Component Strategy
- **Server Components (Default):** Use for data fetching and static content. Keep them thin and pure.
- **Client Components ('use client'):** Only for interactivity (hooks, event listeners). Keep them leaf-level if possible.

## Data Fetching
- **Fetching on the Server:** Fetch directly in Server Components using `async/await`. No need for `useEffect` for initial data.
- **Suspense & Streaming:** Wrap slow-loading components in `Suspense` with skeletons to prevent blocking the entire page.
- **Route Segment Config:** Set `dynamic = 'force-dynamic'` or `revalidate = 3600` depending on data staleness requirements.

## Server Actions
- Use `action` prop on forms for progressive enhancement.
- Implement `useFormStatus` and `useFormState` for feedback and validation errors.
- **Optimistic Updates:** Use `useOptimistic` to show the expected result immediately.

## Performance Optimization
- **Image Component:** Always use `next/image` with `placeholder="blur"` and responsive sizes.
- **Caching:** Understand `revalidateTag` and `revalidatePath` for granular cache invalidation.
- **Metadata API:** Use static and dynamic metadata for SEO.

## Related Skills
`frontend-patterns`, `backend-patterns`, `react-core`.
