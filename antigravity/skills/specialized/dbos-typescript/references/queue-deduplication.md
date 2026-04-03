---
name: "Deduplicate Queued Workflows"
tags: ["queue, deduplication, idempotent, duplicate"]
tier: 1
risk: "medium"
estimated_tokens: 405
tools_needed: ["markdown"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["web", "product"]
quality_score: 0.57
impact: "HIGH"
impactDescription: "Prevents duplicate workflow executions"
title: "Deduplicate Queued Workflows"
---
## Deduplicate Queued Workflows

Set a deduplication ID when enqueuing to prevent duplicate workflow executions. If a workflow with the same deduplication ID is already enqueued or executing, a `DBOSQueueDuplicatedError` is thrown.

**Incorrect (no deduplication):**

```typescript
// Multiple clicks could enqueue duplicates
async function handleClick(userId: string) {
  await DBOS.startWorkflow(processTask, { queueName: queue.name })("task");
}
```

**Correct (with deduplication):**

```typescript
const queue = new WorkflowQueue("task_queue");

async function processTaskFn(task: string) {
  // ...
}
const processTask = DBOS.registerWorkflow(processTaskFn);

async function handleClick(userId: string) {
  try {
    await DBOS.startWorkflow(processTask, {
      queueName: queue.name,
      enqueueOptions: { deduplicationID: userId },
    })("task");
  } catch (e) {
    // DBOSQueueDuplicatedError - workflow already active for this user
    console.log("Task already in progress for user:", userId);
  }
}
```

Deduplication is per-queue. The deduplication ID is active while the workflow has status `ENQUEUED` or `PENDING`. Once the workflow completes, a new workflow with the same deduplication ID can be enqueued.

This is useful for:
- Ensuring one active task per user
- Preventing duplicate form submissions
- Idempotent event processing

Reference: [Deduplication](https://docs.dbos.dev/typescript/tutorials/queue-tutorial#deduplication)
