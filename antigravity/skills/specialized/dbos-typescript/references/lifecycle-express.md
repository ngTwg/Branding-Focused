---
name: "Integrate DBOS with Express"
tags: ["express, http, integration, server"]
tier: 2
risk: "medium"
estimated_tokens: 372
tools_needed: ["markdown"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["platform", "api"]
quality_score: 0.57
impact: "CRITICAL"
impactDescription: "Proper integration ensures workflows survive server restarts"
title: "Integrate DBOS with Express"
---
## Integrate DBOS with Express

Configure and launch DBOS before starting your Express server. Register all workflows and steps before calling `DBOS.launch()`.

**Incorrect (DBOS not launched before server starts):**

```typescript
import express from "express";
import { DBOS } from "@dbos-inc/dbos-sdk";

const app = express();

async function processTaskFn(data: string) {
  // ...
}
const processTask = DBOS.registerWorkflow(processTaskFn);

// Server starts without launching DBOS!
app.listen(3000);
```

**Correct (launch DBOS first, then start Express):**

```typescript
import express from "express";
import { DBOS } from "@dbos-inc/dbos-sdk";

const app = express();

async function processTaskFn(data: string) {
  // ...
}
const processTask = DBOS.registerWorkflow(processTaskFn);

app.post("/process", async (req, res) => {
  const handle = await DBOS.startWorkflow(processTask)(req.body.data);
  res.json({ workflowID: handle.workflowID });
});

async function main() {
  DBOS.setConfig({
    name: "my-app",
    systemDatabaseUrl: process.env.DBOS_SYSTEM_DATABASE_URL,
  });
  await DBOS.launch();
  app.listen(3000, () => {
    console.log("Server running on port 3000");
  });
}

main().catch(console.log);
```

Reference: [Integrating DBOS](https://docs.dbos.dev/typescript/integrating-dbos)
