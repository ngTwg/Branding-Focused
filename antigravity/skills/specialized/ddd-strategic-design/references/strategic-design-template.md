---
name: "Strategic Design Template"
tags: ["antigravity", "bounded", "c:", "catalog", "classification", "context", "ddd", "design", "frontend", "gemini", "language", "<YOUR_USERNAME>", "references", "specialized", "strategic", "subdomain", "template", "ubiquitous", "users"]
tier: 2
risk: "medium"
estimated_tokens: 188
tools_needed: ["markdown"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["web", "product"]
quality_score: 0.54
---
# Strategic Design Template

## Subdomain classification

| Capability | Subdomain type | Why | Owner team |
| --- | --- | --- | --- |
| Pricing | Core | Differentiates business value | Commerce |
| Identity | Supporting | Needed but not differentiating | Platform |

## Bounded context catalog

| Context | Responsibility | Upstream dependencies | Downstream consumers |
| --- | --- | --- | --- |
| Catalog | Product data lifecycle | Supplier feed | Checkout, Search |
| Checkout | Order placement and payment authorization | Catalog, Pricing | Fulfillment, Billing |

## Ubiquitous language

| Term | Definition | Context |
| --- | --- | --- |
| Order | Confirmed purchase request | Checkout |
| Reservation | Temporary inventory hold | Fulfillment |
