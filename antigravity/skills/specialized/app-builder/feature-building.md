---
name: "Feature Building"
tags: ["analysis", "antigravity", "app", "builder", "building", "c:", "enhancement", "error", "feature", "frontend", "gemini", "handling", "iterative", "<YOUR_USERNAME>", "process", "recovery", "specialized", "strategy", "users"]
tier: 2
risk: "medium"
estimated_tokens: 263
tools_needed: ["markdown"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["web", "product"]
quality_score: 0.66
---
# Feature Building

> How to analyze and implement new features.

## Feature Analysis

```
Request: "add payment system"

Analysis:
├── Required Changes:
│   ├── Database: orders, payments tables
│   ├── Backend: /api/checkout, /api/webhooks/stripe
│   ├── Frontend: CheckoutForm, PaymentSuccess
│   └── Config: Stripe API keys
│
├── Dependencies:
│   ├── stripe package
│   └── Existing user authentication
│
└── Estimated Time: 15-20 minutes
```

## Iterative Enhancement Process

```
1. Analyze existing project
2. Create change plan
3. Present plan to user
4. Get approval
5. Apply changes
6. Test
7. Show preview
```

## Error Handling

| Error Type | Solution Strategy |
|------------|-------------------|
| TypeScript Error | Fix type, add missing import |
| Missing Dependency | Run npm install |
| Port Conflict | Suggest alternative port |
| Database Error | Check migration, validate connection |

## Recovery Strategy

```
1. Detect error
2. Try automatic fix
3. If failed, report to user
4. Suggest alternative
5. Rollback if necessary
```
