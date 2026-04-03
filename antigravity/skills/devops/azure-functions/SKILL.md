---
name: "azure-functions"
tags: ["anti", "antigravity", "azure", "c:", "devops", "functions", "gemini", "isolated", "<YOUR_USERNAME>", "model", "net", "node", "patterns", "programming", "python", "users", "worker", "workflows"]
tier: 2
risk: "medium"
estimated_tokens: 314
tools_needed: ["markdown", "terminal"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["engineering", "productivity"]
quality_score: 0.66
date_added: "2026-02-27"
description: "Modern .NET execution model with process isolation"
source: "vibeship-spawner-skills (Apache 2.0)"
---
# Azure Functions

## Patterns

### Isolated Worker Model (.NET)

Modern .NET execution model with process isolation

### Node.js v4 Programming Model

Modern code-centric approach for TypeScript/JavaScript

### Python v2 Programming Model

Decorator-based approach for Python functions

## Anti-Patterns

### ❌ Blocking Async Calls

### ❌ New HttpClient Per Request

### ❌ In-Process Model for New Projects

## ⚠️ Sharp Edges

| Issue | Severity | Solution |
|-------|----------|----------|
| Issue | high | ## Use async pattern with Durable Functions |
| Issue | high | ## Use IHttpClientFactory (Recommended) |
| Issue | high | ## Always use async/await |
| Issue | medium | ## Configure maximum timeout (Consumption) |
| Issue | high | ## Use isolated worker for new projects |
| Issue | medium | ## Configure Application Insights properly |
| Issue | medium | ## Check extension bundle (most common) |
| Issue | medium | ## Add warmup trigger to initialize your code |

## When to Use
This skill is applicable to execute the workflow or actions described in the overview.
