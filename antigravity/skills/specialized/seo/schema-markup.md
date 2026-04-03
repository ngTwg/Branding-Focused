---
name: "schema-markup"
tags: ["antigravity", "business", "c:", "core", "data", "faq", "frontend", "gemini", "governance", "howto", "<YOUR_USERNAME>", "local", "markup", "most", "principles", "product", "reviews", "schema", "seo", "slim"]
tier: 2
risk: "medium"
estimated_tokens: 388
tools_needed: ["markdown"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["web", "product"]
quality_score: 0.68
description: "Use when building or auditing website structured data (JSON-LD). Covers Schema.org types for Local Business, Product, FAQ, and Rich Results."
---
# Schema Markup - Structured Data (v6.5.0-SLIM)

Guidelines and templates for implementing JSON-LD structured data for Google and other search engines.

## 1. Governance & Core Principles
- **JSON-LD Only:** Do not use Microdata or RDFa.
- **Accuracy:** Match content exactly. No "phantom" markup.
- **Validation:** Use `validator.schema.org` and `Google Rich Results Test`.

## 2. Most Used Types

### Local Business
Use for physical locations. Requires name, image, address, and geo-coordinates.
```json
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "Zenith AI",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "123 Tech Lane",
    "addressLocality": "Silicon Valley",
    "addressRegion": "CA",
    "postalCode": "94025"
  }
}
```

### Product & Reviews
Enables price, availability, and rating stars in search results.
- **AggregatedRating:** Require `ratingValue` and `reviewCount`.
- **Offer:** Require `price`, `priceCurrency`, and `availability`.

### FAQ & HowTo
Maximize real estate on the Search Results Page (SERP).
- **FAQPage:** Include question and answer pairs.

## 3. Implementation Workflow
1. Identify target content page type.
2. Select schema templates from `schema-patterns.md`.
3. Validate JSON structure.
4. Test with Google's Rich Results tool.

## Related Skills
`seo-audit`, `programmatic-seo`.
