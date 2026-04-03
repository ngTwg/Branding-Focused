---
name: "🔍 Skill: Algolia Search Integration"
tags: ["activation", "algolia", "antigravity", "backend", "benchmark", "c:", "execution", "frontend", "gemini", "integration", "<YOUR_USERNAME>", "output", "pipeline", "search", "signals", "signature", "skill", "steps", "sub", "task"]
tier: 3
risk: "medium"
estimated_tokens: 340
tools_needed: ["markdown", "terminal"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["web", "product"]
quality_score: 0.58
---
# 🔍 Skill: Algolia Search Integration

> **PURPOSE:** Expert patterns for Algolia search implementation, indexing strategies, and React InstantSearch.
> **CATEGORY:** Backend
> **TIER:** 2+

---

## 🚦 ACTIVATION SIGNALS

- Keywords: `Algolia`, `InstantSearch`, `search indexing`, `search API`.
- Task: Adding search functionality, tuning relevance, or implementing type-ahead search.

---

## 🛠️ SUB-STEPS (EXECUTION PIPELINE)

1. **Information Extraction**: Identify data sources and search requirements (facets, filters, sorting).
2. **Indexing Strategy**: Choose between Full Reindexing, Full Record Updates, or Partial Updates.
3. **Frontend Integration**: Implement React InstantSearch with hooks (`useSearchBox`, `useHits`, `useRefinementList`).
4. **Next.js SSR**: Use `InstantSearchNext` for server-side rendering and URL synchronization.
5. **Relevance Tuning**: Configure searchable attributes, custom ranking, and typo tolerance in Algolia dashboard/API.

---

## 📝 OUTPUT SIGNATURE

- Algolia indexing scripts.
- React/Next.js search components.
- Search configuration exports (JSON).

---

## 🧪 BENCHMARK TASK

- **Input**: "Implement a real-time product search with categories and price filters using Algolia."
- **Output**: Algolia indexing script for products -> useSearchBox for input -> useRefinementList for categories -> useHits for results.
