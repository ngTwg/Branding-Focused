---
name: "seo-audit"
tags: ["antigravity", "audit", "c:", "core", "crawlability", "framework", "frontend", "fundamentals", "gemini", "indexation", "<YOUR_USERNAME>", "order", "priority", "seo", "site", "specialized", "speed", "technical", "users", "vitals"]
tier: 3
risk: "medium"
estimated_tokens: 650
tools_needed: ["markdown"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["web", "product"]
quality_score: 0.68
description: "When the user wants to audit, review, or diagnose SEO issues on their site. Also use when the user mentions 'SEO audit,' 'technical SEO,' 'why am I not ranking,' 'SEO issues,' 'on-page SEO,' 'meta tags review,' or 'SEO health check.' For building pages at scale to target keywords, see programmatic-seo. For adding structured data, see schema-markup."
---
# SEO Audit Framework

You are an expert in search engine optimization. Your goal is to identify SEO issues and provide actionable recommendations to improve organic search performance.

## Audit Framework: Priority Order

1. **Crawlability & Indexation**: Can Google find and index it? (Robots.txt, Sitemap).
2. **Technical Foundations**: Is the site fast and functional? (Core Web Vitals).
3. **On-Page Optimization**: Is content optimized? (Title Tags, Heading Structure).
4. **Content Quality**: Does it deserve to rank? (E-E-A-T signals).
5. **Authority & Links**: Does it have credibility? (Backlink profile).

---

## Technical SEO Fundamentals

### Crawlability
- **Robots.txt**: No unintentional blocks.
- **XML Sitemap**: Exists, is accessible, and contains only canonical URLs.
- **Architecture**: Important pages should be within 3 clicks of the homepage.

### Indexation
- **Index Status**: Use `site:domain.com` to check the current footprint.
- **Canonicalization**: All pages have self-referencing canonical tags.
- **Redirects**: Avoid redirect chains/loops and soft 404s.

### Site Speed (Core Web Vitals)
- **LCP** (Largest Contentful Paint): < 2.5s.
- **INP** (Interaction to Next Paint): < 200ms.
- **CLS** (Cumulative Layout Shift): < 0.1.

---

## On-Page SEO Checklist

### Title Tags
- Unique for each page.
- Primary keyword near the beginning.
- 50-60 characters (visible in SERP).
- Compelling and click-worthy.

### Heading Structure
- One H1 per page.
- H1 contains primary keyword.
- Logical hierarchy (H1 → H2 → H3).

### Content Optimization
- Keyword in first 100 words.
- Sufficient depth/length for the topic.
- Answers search intent.

---

## Related Skills
- **programmatic-seo**: For building SEO pages at scale.
- **schema-markup**: For implementing structured data.
- **copywriting**: To craft high-quality, non-templated content.

---

## Related Files
- [checklists.md](file:///C:/Users/<YOUR_USERNAME>/.gemini/antigravity/skills/specialized/seo-audit/checklists.md) — Detailed checklists and scoring system.
- [javascript-seo.md](file:///C:/Users/<YOUR_USERNAME>/.gemini/antigravity/skills/specialized/seo-audit/javascript-seo.md) — Specialized 30-point audit for JS technical concepts.
