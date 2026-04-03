---
name: "Configure Step Retries for Transient Failures"
tags: ["step, retry, exponential-backoff, resilience"]
tier: 2
risk: "medium"
estimated_tokens: 489
tools_needed: ["markdown"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["web", "product"]
quality_score: 0.61
impact: "HIGH"
impactDescription: "Automatic retries handle transient failures without manual code"
title: "Configure Step Retries for Transient Failures"
---
## Configure Step Retries for Transient Failures

Steps can automatically retry on failure with exponential backoff. This handles transient failures like network issues.

**Incorrect (manual retry logic):**

```typescript
async function fetchData() {
  for (let attempt = 0; attempt < 3; attempt++) {
    try {
      return await fetch("https://api.example.com").then(r => r.json());
    } catch (e) {
      if (attempt === 2) throw e;
      await new Promise(r => setTimeout(r, 2 ** attempt * 1000));
    }
  }
}
```

**Correct (built-in retries with `DBOS.runStep`):**

```typescript
async function fetchData() {
  return await fetch("https://api.example.com").then(r => r.json());
}

async function myWorkflowFn() {
  const data = await DBOS.runStep(fetchData, {
    name: "fetchData",
    retriesAllowed: true,
    maxAttempts: 10,
    intervalSeconds: 1,
    backoffRate: 2,
  });
}
const myWorkflow = DBOS.registerWorkflow(myWorkflowFn);
```

With an inline arrow function:

```typescript
async function myWorkflowFn() {
  const data = await DBOS.runStep(
    () => fetch("https://api.example.com").then(r => r.json()),
    { name: "fetchData", retriesAllowed: true, maxAttempts: 10 }
  );
}
```

Retry parameters:
- `retriesAllowed`: Enable automatic retries (default: `false`)
- `maxAttempts`: Maximum retry attempts (default: `3`)
- `intervalSeconds`: Initial delay between retries in seconds (default: `1`)
- `backoffRate`: Multiplier for exponential backoff (default: `2`)

With defaults, retry delays are: 1s, 2s, 4s, 8s, 16s...

If all retries are exhausted, a `DBOSMaxStepRetriesError` is thrown to the calling workflow.

Reference: [Configurable Retries](https://docs.dbos.dev/typescript/tutorials/step-tutorial#configurable-retries)
