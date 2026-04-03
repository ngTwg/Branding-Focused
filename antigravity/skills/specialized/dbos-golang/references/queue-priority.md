---
name: "Set Queue Priority for Workflows"
tags: ["queue, priority, ordering, importance"]
tier: 1
risk: "medium"
estimated_tokens: 305
tools_needed: ["markdown"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["engineering", "productivity"]
quality_score: 0.57
impact: "HIGH"
impactDescription: "Prioritizes important workflows over lower-priority ones"
title: "Set Queue Priority for Workflows"
---
## Set Queue Priority for Workflows

Enable priority on a queue to process higher-priority workflows first. Lower numbers indicate higher priority.

**Incorrect (no priority - FIFO only):**

```go
queue := dbos.NewWorkflowQueue(ctx, "tasks")
// All tasks processed in FIFO order regardless of importance
```

**Correct (priority-enabled queue):**

```go
queue := dbos.NewWorkflowQueue(ctx, "tasks",
	dbos.WithPriorityEnabled(),
)

// High priority task (lower number = higher priority)
dbos.RunWorkflow(ctx, processTask, "urgent-task",
	dbos.WithQueue(queue.Name),
	dbos.WithPriority(1),
)

// Low priority task
dbos.RunWorkflow(ctx, processTask, "background-task",
	dbos.WithQueue(queue.Name),
	dbos.WithPriority(100),
)
```

Priority rules:
- Range: `1` to `2,147,483,647`
- Lower number = higher priority
- Workflows **without** assigned priorities have the highest priority (run first)
- Workflows with the same priority are dequeued in FIFO order

Reference: [Priority](https://docs.dbos.dev/golang/tutorials/queue-tutorial#priority)
