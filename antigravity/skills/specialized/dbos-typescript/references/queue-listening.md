---
name: "Control Which Queues a Worker Listens To"
tags: ["queue, listen, worker, process, configuration"]
tier: 2
risk: "medium"
estimated_tokens: 446
tools_needed: ["markdown"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["web", "product"]
quality_score: 0.61
impact: "HIGH"
impactDescription: "Enables heterogeneous worker pools"
title: "Control Which Queues a Worker Listens To"
---
## Control Which Queues a Worker Listens To

Configure `listenQueues` in DBOS configuration to make a process only dequeue from specific queues. This enables heterogeneous worker pools.

**Incorrect (all workers process all queues):**

```typescript
import { DBOS, WorkflowQueue } from "@dbos-inc/dbos-sdk";

const cpuQueue = new WorkflowQueue("cpu_queue");
const gpuQueue = new WorkflowQueue("gpu_queue");

// Every worker processes both CPU and GPU tasks
// GPU tasks on CPU workers will fail or be slow!
DBOS.setConfig({
  name: "my-app",
  systemDatabaseUrl: process.env.DBOS_SYSTEM_DATABASE_URL,
});
await DBOS.launch();
```

**Correct (selective queue listening):**

```typescript
import { DBOS, WorkflowQueue } from "@dbos-inc/dbos-sdk";

const cpuQueue = new WorkflowQueue("cpu_queue");
const gpuQueue = new WorkflowQueue("gpu_queue");

async function main() {
  const workerType = process.env.WORKER_TYPE; // "cpu" or "gpu"

  const config: any = {
    name: "my-app",
    systemDatabaseUrl: process.env.DBOS_SYSTEM_DATABASE_URL,
  };

  if (workerType === "gpu") {
    config.listenQueues = [gpuQueue];
  } else if (workerType === "cpu") {
    config.listenQueues = [cpuQueue];
  }

  DBOS.setConfig(config);
  await DBOS.launch();
}
```

`listenQueues` only controls dequeuing. A CPU worker can still enqueue tasks onto the GPU queue:

```typescript
// From a CPU worker, enqueue onto the GPU queue
await DBOS.startWorkflow(gpuTask, { queueName: gpuQueue.name })("data");
```

Reference: [Explicit Queue Listening](https://docs.dbos.dev/typescript/tutorials/queue-tutorial#explicit-queue-listening)
