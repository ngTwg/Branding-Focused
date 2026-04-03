---
name: "Context Mapping Patterns"
tags: ["acl", "antigravity", "c:", "checklist", "common", "context", "ddd", "frontend", "gemini", "<YOUR_USERNAME>", "map", "mapping", "patterns", "references", "relationship", "specialized", "template", "users"]
tier: 4
risk: "medium"
estimated_tokens: 168
tools_needed: ["markdown"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["web", "product"]
quality_score: 0.54
---
# Context Mapping Patterns

## Common relationship patterns

- Partnership
- Shared Kernel
- Customer-Supplier
- Conformist
- Anti-Corruption Layer
- Open Host Service
- Published Language

## Mapping template

| Upstream context | Downstream context | Pattern | Contract owner | Translation needed |
| --- | --- | --- | --- | --- |
| Billing | Checkout | Customer-Supplier | Billing | Yes |
| Identity | Checkout | Conformist | Identity | No |

## ACL checklist

- Define canonical domain model for receiving context.
- Translate external terms into local ubiquitous language.
- Keep ACL code at boundary, not inside domain core.
- Add contract tests for mapped behavior.
