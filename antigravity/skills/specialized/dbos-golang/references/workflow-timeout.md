---
name: "Set Workflow Timeouts"
tags: ["workflow, timeout, cancellation, duration"]
tier: 1
risk: "medium"
estimated_tokens: 331
tools_needed: ["markdown"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["web", "product"]
quality_score: 0.57
impact: "CRITICAL"
impactDescription: "Prevents workflows from running indefinitely"
title: "Set Workflow Timeouts"
---
## Set Workflow Timeouts

Set a timeout for a workflow by using Go's `context.WithTimeout` or `dbos.WithTimeout` on the DBOS context. When the timeout expires, the workflow and all its children are cancelled.

**Incorrect (no timeout for potentially long workflow):**

```go
// No timeout - could run indefinitely
handle, err := dbos.RunWorkflow(ctx, processTask, "data")
```

**Correct (with timeout):**

```go
// Create a context with a 5-minute timeout
timedCtx, cancel := dbos.WithTimeout(ctx, 5*time.Minute)
defer cancel()

handle, err := dbos.RunWorkflow(timedCtx, processTask, "data")
if err != nil {
	log.Fatal(err)
}
```

Key timeout behaviors:
- Timeouts are **start-to-completion**: the timeout begins when the workflow starts execution, not when it's enqueued
- Timeouts are **durable**: they persist across restarts, so workflows can have very long timeouts (hours, days, weeks)
- Cancellation happens at the **beginning of the next step** - the current step completes first
- Cancelling a workflow also cancels all **child workflows**

Reference: [Workflow Timeouts](https://docs.dbos.dev/golang/tutorials/workflow-tutorial#workflow-timeouts)
