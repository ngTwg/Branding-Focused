---
name: "shopify-apps"
tags: ["anti", "antigravity", "app", "apps", "bridge", "c:", "embedded", "frontend", "gemini", "handling", "<YOUR_USERNAME>", "patterns", "react", "router", "setup", "shopify", "specialized", "users", "webhook", "with"]
tier: 2
risk: "medium"
estimated_tokens: 291
tools_needed: ["markdown"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["web", "product"]
quality_score: 0.66
date_added: "2026-02-27"
description: "Modern Shopify app template with React Router"
source: "vibeship-spawner-skills (Apache 2.0)"
---
# Shopify Apps

## Patterns

### React Router App Setup

Modern Shopify app template with React Router

### Embedded App with App Bridge

Render app embedded in Shopify Admin

### Webhook Handling

Secure webhook processing with HMAC verification

## Anti-Patterns

### ❌ REST API for New Apps

### ❌ Webhook Processing Before Response

### ❌ Polling Instead of Webhooks

## ⚠️ Sharp Edges

| Issue | Severity | Solution |
|-------|----------|----------|
| Issue | high | ## Respond immediately, process asynchronously |
| Issue | high | ## Check rate limit headers |
| Issue | high | ## Request protected customer data access |
| Issue | medium | ## Use TOML only (recommended) |
| Issue | medium | ## Handle both URL formats |
| Issue | high | ## Use GraphQL for all new code |
| Issue | high | ## Use latest App Bridge via script tag |
| Issue | high | ## Implement all GDPR handlers |

## When to Use
This skill is applicable to execute the workflow or actions described in the overview.
