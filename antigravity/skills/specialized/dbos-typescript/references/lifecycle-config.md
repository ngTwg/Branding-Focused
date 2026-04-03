---
name: "Configure and Launch DBOS Properly"
tags: ["configuration, launch, setup, initialization"]
tier: 2
risk: "medium"
estimated_tokens: 297
tools_needed: ["markdown"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["platform", "api"]
quality_score: 0.56
impact: "CRITICAL"
impactDescription: "Application won't function without proper setup"
title: "Configure and Launch DBOS Properly"
---
## Configure and Launch DBOS Properly

Every DBOS application must configure and launch DBOS before running any workflows. All workflows and steps must be registered before calling `DBOS.launch()`.

**Incorrect (missing configuration or launch):**

```typescript
import { DBOS } from "@dbos-inc/dbos-sdk";

// No configuration or launch!
async function myWorkflowFn() {
  // This will fail - DBOS is not launched
}
const myWorkflow = DBOS.registerWorkflow(myWorkflowFn);
await myWorkflow();
```

**Correct (configure and launch in main):**

```typescript
import { DBOS } from "@dbos-inc/dbos-sdk";

async function myWorkflowFn() {
  // workflow logic
}
const myWorkflow = DBOS.registerWorkflow(myWorkflowFn);

async function main() {
  DBOS.setConfig({
    name: "my-app",
    systemDatabaseUrl: process.env.DBOS_SYSTEM_DATABASE_URL,
  });
  await DBOS.launch();
  await myWorkflow();
}

main().catch(console.log);
```

Reference: [DBOS Lifecycle](https://docs.dbos.dev/typescript/reference/dbos-class)
