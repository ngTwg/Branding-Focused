---
name: "Rate Limit Queue Execution"
tags: ["queue, rate-limit, throttle, api"]
tier: 2
risk: "medium"
estimated_tokens: 310
tools_needed: ["markdown"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["platform", "api"]
quality_score: 0.60
impact: "HIGH"
impactDescription: "Prevents overwhelming external APIs with too many requests"
title: "Rate Limit Queue Execution"
---
## Rate Limit Queue Execution

Set rate limits on a queue to control how many workflows start in a given period. Rate limits are global across all DBOS processes.

**Incorrect (no rate limiting):**

```go
queue := dbos.NewWorkflowQueue(ctx, "llm_tasks")
// Could send hundreds of requests per second to a rate-limited API
```

**Correct (rate-limited queue):**

```go
queue := dbos.NewWorkflowQueue(ctx, "llm_tasks",
	dbos.WithRateLimiter(&dbos.RateLimiter{
		Limit:  50,
		Period: 30 * time.Second,
	}),
)
```

This queue starts at most 50 workflows per 30 seconds.

**Combining rate limiting with concurrency:**

```go
// At most 5 concurrent and 50 per 30 seconds
queue := dbos.NewWorkflowQueue(ctx, "api_tasks",
	dbos.WithWorkerConcurrency(5),
	dbos.WithRateLimiter(&dbos.RateLimiter{
		Limit:  50,
		Period: 30 * time.Second,
	}),
)
```

Common use cases:
- LLM API rate limiting (OpenAI, Anthropic, etc.)
- Third-party API throttling
- Preventing database overload

Reference: [Rate Limiting](https://docs.dbos.dev/golang/tutorials/queue-tutorial#rate-limiting)
