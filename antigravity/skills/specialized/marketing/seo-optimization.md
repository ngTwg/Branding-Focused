---
name: "SEO Optimization"
tags: ["antigravity", "audit", "c:", "checklist", "frontend", "gemini", "<YOUR_USERNAME>", "marketing", "optimization", "overview", "playbooks", "programmatic", "quick", "reference", "rules", "seo", "specialized", "users"]
tier: 3
risk: "medium"
estimated_tokens: 1076
tools_needed: ["markdown"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["web", "product"]
quality_score: 0.79
---
# SEO Optimization

> **Tier:** 2  
> **Tags:** `[seo, search-optimization, programmatic-seo, seo-audit, organic-traffic]`  
> **When to use:** SEO strategy, programmatic SEO, SEO audits, search optimization

---

## Overview

Expert guidance for SEO optimization including programmatic SEO at scale, comprehensive SEO audits, and search optimization strategies. Covers both technical and content SEO with actionable frameworks.

---

## Rules

**RULE-001: Programmatic SEO Must Provide Unique Value**
Every programmatic page must offer genuine value beyond variable substitution. Use proprietary data, product-derived insights, or unique analysis. Avoid thin content penalties.

```markdown
❌ Bad: Just swapping city names in identical content
✅ Good: City-specific data, local insights, unique providers per location
```

**RULE-002: Use Subfolders Not Subdomains**
Always use subfolders for SEO content to pass authority to main domain.

```
✅ Good: yoursite.com/templates/resume/
❌ Bad: templates.yoursite.com/resume/
```

**RULE-003: Match Search Intent Genuinely**
Pages must actually answer what people are searching for. Don't over-optimize for keywords at expense of usefulness.

**RULE-004: Scalable Quality Over Quantity**
Better to have 100 great pages than 10,000 thin ones. Build quality checks into the process.

**RULE-005: Technical SEO Fundamentals**
- Unique titles and meta descriptions per page
- Proper heading structure (H1, H2, H3)
- Schema markup implemented
- Canonical tags correct
- Page speed optimized
- Mobile-friendly
- XML sitemap updated

**RULE-006: Internal Linking Architecture**
Use hub-and-spoke model: main category pages (hubs) link to individual pages (spokes), with cross-links between related spokes. Avoid orphan pages.

**RULE-007: Monitor Index Health**
Track indexation rate, rankings by pattern, traffic by pattern, engagement metrics, and watch for thin content warnings in Search Console.

**RULE-008: SEO Audit Scoring System**
Use weighted scoring: Technical SEO (30%), On-Page SEO (30%), Content Quality (25%), User Experience (15%). Score 80+ = Excellent, 60-79 = Good, 40-59 = Needs Work, <40 = Critical Issues.

**RULE-009: Prioritize Fixes by Impact**
Focus on: Critical technical issues first, then high-traffic pages, then quick wins, then long-term improvements.

**RULE-010: Featured Snippet Optimization**
Structure content to answer questions directly: use lists, tables, definitions, and step-by-step formats. Target position zero opportunities.

---

## Quick Reference

### 12 Programmatic SEO Playbooks

1. **Templates** - "[Type] template" searches
2. **Curation** - "best [category]" lists
3. **Conversions** - "[X] to [Y]" tools
4. **Comparisons** - "[X] vs [Y]" pages
5. **Examples** - "[type] examples" galleries
6. **Locations** - "[service] in [location]" pages
7. **Personas** - "[product] for [audience]" pages
8. **Integrations** - "[product] + [product]" pages
9. **Glossary** - "what is [term]" definitions
10. **Translations** - Multi-language content
11. **Directory** - "[category] tools" listings
12. **Profiles** - Entity/person profile pages

### SEO Audit Checklist

**Technical SEO:**
- [ ] Site crawlable and indexable
- [ ] XML sitemap present and submitted
- [ ] Robots.txt configured correctly
- [ ] HTTPS implemented
- [ ] Page speed < 3 seconds
- [ ] Mobile-friendly
- [ ] No broken links
- [ ] Canonical tags correct

**On-Page SEO:**
- [ ] Unique title tags (50-60 chars)
- [ ] Unique meta descriptions (150-160 chars)
- [ ] H1 tags present and unique
- [ ] Keyword in URL, title, H1, first paragraph
- [ ] Images have alt text
- [ ] Internal linking present
- [ ] Schema markup implemented

**Content Quality:**
- [ ] Content > 300 words (ideally 1000+)
- [ ] Original, not duplicate
- [ ] Answers search intent
- [ ] Readable (Flesch score > 60)
- [ ] Updated regularly
- [ ] Multimedia included

### URL Structure Best Practices

```
✅ Good URL patterns:
/templates/[type]/
/compare/[x]-vs-[y]/
/[service]/[city]/
/glossary/[term]/

❌ Bad URL patterns:
/page?id=123&cat=5
/templates.yoursite.com/
/very-long-url-with-many-unnecessary-words/
```

---

## Metadata

- **Related Skills:** content-strategy.md, analytics-tracking.md
- **Dependencies:** None
- **Version:** 1.0.0
- **Last Updated:** 2024-03-26
