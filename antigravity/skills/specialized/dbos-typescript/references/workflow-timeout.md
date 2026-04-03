---
name: "Set Workflow Timeouts"
tags: ["workflow, timeout, cancellation, duration"]
tier: 1
risk: "medium"
estimated_tokens: 339
tools_needed: ["markdown"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["web", "product"]
quality_score: 0.57
impact: "CRITICAL"
impactDescription: "Prevents workflows from running indefinitely"
title: "Set Workflow Timeouts"
---
## Set Workflow Timeouts

Set a timeout for a workflow by passing `timeoutMS` to `DBOS.startWorkflow`. When the timeout expires, the workflow and all its children are cancelled.

**Incorrect (no timeout for potentially long workflow):**

```typescript
// No timeout - could run indefinitely
const handle = await DBOS.startWorkflow(processTask)("data");
```

**Correct (with timeout):**

```typescript
async function processTaskFn(data: string) {
  // ...
}
const processTask = DBOS.registerWorkflow(processTaskFn);

// Timeout after 5 minutes (in milliseconds)
const handle = await DBOS.startWorkflow(processTask, {
  timeoutMS: 5 * 60 * 1000,
})("data");
```

Key timeout behaviors:
- Timeouts are **start-to-completion**: the timeout begins when the workflow starts execution, not when it's enqueued
- Timeouts are **durable**: they persist across restarts, so workflows can have very long timeouts (hours, days, weeks)
- Cancellation happens at the **beginning of the next step** - the current step completes first
- Cancelling a workflow also cancels all **child workflows**

Reference: [Workflow Timeouts](https://docs.dbos.dev/typescript/tutorials/workflow-tutorial#workflow-timeouts)
