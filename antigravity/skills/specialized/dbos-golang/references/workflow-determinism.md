---
name: "Keep Workflows Deterministic"
tags: ["workflow, determinism, recovery, reliability"]
tier: 2
risk: "medium"
estimated_tokens: 374
tools_needed: ["markdown"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["platform", "api"]
quality_score: 0.57
impact: "CRITICAL"
impactDescription: "Non-deterministic workflows cannot recover correctly"
title: "Keep Workflows Deterministic"
---
## Keep Workflows Deterministic

Workflow functions must be deterministic: given the same inputs and step return values, they must invoke the same steps in the same order. Non-deterministic operations must be moved to steps.

**Incorrect (non-deterministic workflow):**

```go
func exampleWorkflow(ctx dbos.DBOSContext, input string) (string, error) {
	// Random value in workflow breaks recovery!
	// On replay, rand.Intn returns a different value,
	// so the workflow may take a different branch.
	if rand.Intn(2) == 0 {
		return stepOne(ctx)
	}
	return stepTwo(ctx)
}
```

**Correct (non-determinism in step):**

```go
func exampleWorkflow(ctx dbos.DBOSContext, input string) (string, error) {
	// Step result is checkpointed - replay uses the saved value
	choice, err := dbos.RunAsStep(ctx, func(ctx context.Context) (int, error) {
		return rand.Intn(2), nil
	}, dbos.WithStepName("generateChoice"))
	if err != nil {
		return "", err
	}
	if choice == 0 {
		return stepOne(ctx)
	}
	return stepTwo(ctx)
}
```

Non-deterministic operations that must be in steps:
- Random number generation
- Getting current time (`time.Now()`)
- Accessing external APIs (`http.Get`, etc.)
- Reading files
- Database queries

Reference: [Workflow Determinism](https://docs.dbos.dev/golang/tutorials/workflow-tutorial#determinism)
