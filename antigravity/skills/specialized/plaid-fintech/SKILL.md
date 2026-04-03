---
name: "plaid-fintech"
tags: ["and", "anti", "antigravity", "c:", "creation", "error", "exchange", "fintech", "frontend", "gemini", "handling", "item", "<YOUR_USERNAME>", "link", "mode", "patterns", "plaid", "specialized", "sync", "token"]
tier: 3
risk: "medium"
estimated_tokens: 375
tools_needed: ["markdown"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["web", "product"]
quality_score: 0.67
date_added: "2026-02-27"
description: "Create a linktoken for Plaid Link, exchange publictoken for accesstoken. Link tokens are short-lived, one-time use. Access tokens don't expire but may need updating when users change passwords."
source: "vibeship-spawner-skills (Apache 2.0)"
---
# Plaid Fintech

## Patterns

### Link Token Creation and Exchange

Create a link_token for Plaid Link, exchange public_token for access_token.
Link tokens are short-lived, one-time use. Access tokens don't expire but
may need updating when users change passwords.

### Transactions Sync

Use /transactions/sync for incremental transaction updates. More efficient
than /transactions/get. Handle webhooks for real-time updates instead of
polling.

### Item Error Handling and Update Mode

Handle ITEM_LOGIN_REQUIRED errors by putting users through Link update mode.
Listen for PENDING_DISCONNECT webhook to proactively prompt users.

## Anti-Patterns

### ❌ Storing Access Tokens in Plain Text

### ❌ Polling Instead of Webhooks

### ❌ Ignoring Item Errors

## ⚠️ Sharp Edges

| Issue | Severity | Solution |
|-------|----------|----------|
| Issue | critical | See docs |
| Issue | high | See docs |
| Issue | high | See docs |
| Issue | high | See docs |
| Issue | medium | See docs |
| Issue | medium | See docs |
| Issue | medium | See docs |
| Issue | medium | See docs |

## When to Use
This skill is applicable to execute the workflow or actions described in the overview.
