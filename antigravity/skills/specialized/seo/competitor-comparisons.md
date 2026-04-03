---
name: "competitor-comparisons"
tags: ["alternatives", "antigravity", "architecture", "c:", "comparisons", "competitor", "content", "formats", "frontend", "gemini", "intent", "<YOUR_USERNAME>", "optimization", "page", "pages", "principles", "related", "seo", "skills", "slim"]
tier: 3
risk: "medium"
estimated_tokens: 632
tools_needed: ["markdown"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["web", "product"]
quality_score: 0.68
description: "Master guide for creating competitor comparison and alternatives pages for SEO and sales enablement."
---
# Competitor & Alternatives Pages (v6.5.0-SLIM)

Expert strategy for building pages that rank for competitor interest and convert evaluators.

## 1. Page Formats & Intent
- **Singular Alternative:** User is looking to switch. URL: `/alternatives/[competitor]`.
- **Plural Alternatives:** User is researching options. URL: `/best-[competitor]-alternatives`.
- **You vs [Competitor]:** Direct comparison. URL: `/vs/[competitor]`.
- **[A] vs [B]:** Objective analyst role. URL: `/compare/[a]-vs-[b]`.

## 2. Content Architecture
**Centralized YAML Repository:** Maintain a single source of truth for each competitor (Pricing, Features, Strengths, Weaknesses, Best For).

## 3. SEO Optimization
- **Keyword Targets:** "[Competitor] alternative", "tools like [Competitor]", "[You] vs [Competitor]".
- **Internal Linking:** Link from feature pages and blog posts to comparisons.
- **Schema Markup:** Use FAQ schema for common "Why switch?" question and answer pairs.

## 4. Writing Principles
- **Honesty Builds Trust:** Acknowledge where the competitor is better.
- **Depth Over Surface:** Explain *why* differences matter (e.g., "Our API is 2x faster because...").
- **Clear Call-to-Action:** Focus on migration ease and free trials.

## Related Skills
`seo-audit`, `schema-markup`, `copywriting`.
---
name: research-automation
description: Automated research and documentation fetching using Context7 and Exa APIs.
---

# Research Automation Tools (v6.5.0-SLIM)

Leverage specialized APIs for real-time documentation and semantic search.

## 1. Context7 Auto Research
- **Purpose:** Automatically fetch latest library/framework documentation for AI context.
- **Usage:** Trigger when asking about recent updates to React, Next.js, Prisma, etc.
- **Install:** `npx skills add -g BenedictKing/context7-auto-research`.

## 2. Exa Search
- **Purpose:** Semantic search and similar content discovery.
- **Capabilities:** Search by category (research papers, companies, people), find similar URLs, structured data extraction.
- **Usage:** "Find 5 research papers similar to [URL] about LLM memory."

## 3. Best Practices
- **API Keys:** Store in `.env` for rate-limit management.
- **Search Logic:** Use specific categories in Exa to prune noise.
- **Integration:** Pipe results directly into code comments or documentation files.

## Related Skills
`browser-automation`, `skill-lookup`.
