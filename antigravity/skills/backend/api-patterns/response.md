---
name: "Response Format Principles"
tags: ["antigravity", "api", "backend", "c:", "common", "error", "format", "frontend", "gemini", "<YOUR_USERNAME>", "pagination", "patterns", "principles", "questions", "response", "selection", "types", "users"]
tier: 2
risk: "medium"
estimated_tokens: 218
tools_needed: ["markdown", "terminal"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["web", "product"]
quality_score: 0.63
---
# Response Format Principles

> Consistency is key - choose a format and stick to it.

## Common Patterns

```
Choose one:
├── Envelope pattern ({ success, data, error })
├── Direct data (just return the resource)
└── HAL/JSON:API (hypermedia)
```

## Error Response

```
Include:
├── Error code (for programmatic handling)
├── User message (for display)
├── Details (for debugging, field-level errors)
├── Request ID (for support)
└── NOT internal details (security!)
```

## Pagination Types

| Type | Best For | Trade-offs |
|------|----------|------------|
| **Offset** | Simple, jumpable | Performance on large datasets |
| **Cursor** | Large datasets | Can't jump to page |
| **Keyset** | Performance critical | Requires sortable key |

### Selection Questions

1. How large is the dataset?
2. Do users need to jump to specific pages?
3. Is data frequently changing?
