---
name: "Rate Limiting Principles"
tags: ["antigravity", "api", "backend", "c:", "gemini", "headers", "<YOUR_USERNAME>", "limit", "limiting", "patterns", "principles", "rate", "response", "selection", "strategy", "users", "why"]
tier: 2
risk: "medium"
estimated_tokens: 169
tools_needed: ["markdown", "terminal"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["platform", "api"]
quality_score: 0.60
---
# Rate Limiting Principles

> Protect your API from abuse and overload.

## Why Rate Limit

```
Protect against:
├── Brute force attacks
├── Resource exhaustion
├── Cost overruns (if pay-per-use)
└── Unfair usage
```

## Strategy Selection

| Type | How | When |
|------|-----|------|
| **Token bucket** | Burst allowed, refills over time | Most APIs |
| **Sliding window** | Smooth distribution | Strict limits |
| **Fixed window** | Simple counters per window | Basic needs |

## Response Headers

```
Include in headers:
├── X-RateLimit-Limit (max requests)
├── X-RateLimit-Remaining (requests left)
├── X-RateLimit-Reset (when limit resets)
└── Return 429 when exceeded
```
