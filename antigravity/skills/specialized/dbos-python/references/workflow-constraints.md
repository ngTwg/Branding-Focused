---
name: "Follow Workflow Constraints"
tags: ["workflow, step, constraints, rules"]
tier: 1
risk: "medium"
estimated_tokens: 419
tools_needed: ["markdown"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["engineering", "productivity"]
quality_score: 0.64
impact: "CRITICAL"
impactDescription: "Violating constraints causes failures or incorrect behavior"
title: "Follow Workflow Constraints"
---
## Follow Workflow Constraints

DBOS workflows and steps have specific constraints that must be followed for correct operation.

**Incorrect (calling start_workflow from step):**

```python
@DBOS.step()
def my_step():
    # Never start workflows from inside a step!
    DBOS.start_workflow(another_workflow)
```

**Incorrect (modifying global state):**

```python
results = []  # Global variable

@DBOS.workflow()
def my_workflow():
    # Don't modify globals from workflows!
    results.append("done")
```

**Incorrect (using recv outside workflow):**

```python
@DBOS.step()
def my_step():
    # recv can only be called from workflows!
    msg = DBOS.recv("topic")
```

**Correct (following constraints):**

```python
@DBOS.workflow()
def parent_workflow():
    result = my_step()
    # Start child workflow from workflow, not step
    handle = DBOS.start_workflow(child_workflow, result)
    # Use recv from workflow
    msg = DBOS.recv("topic")
    return handle.get_result()

@DBOS.step()
def my_step():
    # Steps just do their work and return
    return process_data()

@DBOS.workflow()
def child_workflow(data):
    return transform(data)
```

Key constraints:
- Do NOT call `DBOS.start_workflow` from a step
- Do NOT call `DBOS.recv` from a step
- Do NOT call `DBOS.set_event` from outside a workflow
- Do NOT modify global variables from workflows or steps
- Do NOT use threads to start workflows

Reference: [DBOS Workflows](https://docs.dbos.dev/python/tutorials/workflow-tutorial)
