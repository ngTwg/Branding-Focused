---
name: "AI Agents Master Inventory"
tags: ["agents", "ai", "ai-agents"]
tier: 3
risk: "high"
estimated_tokens: 256
tools_needed: ["markdown"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["ai"]
quality_score: 0.55
---
# AI Agents Master Inventory

> **Tier-Based Routing**: Load this inventory for Tier 3/4 tasks involving autonomous agents, task decomposition, or multi-step coordination.

## 📋 Table of Contents

- [Orchestrate AI Agent Workflows](#orchestrate-workflowsi-agent-workflows)

---

<a id="orchestrate-workflowsi-agent-workflows"></a>

## Orchestrate AI Agent Workflows

---
name: orchestrate-workflows
description: "Patterns for multi-agent coordination, orchestration (Sequential, Parallel, Hierarchical, Loop), failure management, and state persistence. Trigger: agent orchestration, multi-agent systems, LangGraph, CrewAI, AutoGen."
author: Antigravity System
version: "1.0"
tier: 3
---

### Activation Patterns
- "How do I coordinate multiple agents?"
- "Build a multi-agent system for [Task]"
- "Implement failure recovery in agent workflows"
- "Manage state across multiple LLM calls"

### Implementation Logic
1. **Analyze Workflow Depth**: Identify if task is Sequential (Pipeline) or Parallel (MapReduce).
2. **Setup State Schema**: Define a Pydantic `State` class for shared memory.
3. **Configure Circuit Breakers**: Set `max_retries` and `max_steps` for loops.
4. **Link Nodes/Edges**: Define agent nodes and tool edges for routing.

[View full implementation: ./orchestrate-workflows.md](./orchestrate-workflows.md)
