---
name: "⛓️ Skill: Workflow Automation"
tags: ["activation", "antigravity", "automation", "benchmark", "c:", "execution", "frontend", "gemini", "<YOUR_USERNAME>", "output", "pipeline", "signals", "signature", "skill", "steps", "sub", "task", "users", "workflow", "workflows"]
tier: 3
risk: "medium"
estimated_tokens: 275
tools_needed: ["markdown", "terminal"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["web", "product"]
quality_score: 0.57
---
# ⛓️ Skill: Workflow Automation

> **PURPOSE:** Infrastructure for reliable, durable AI agent execution (n8n, Temporal, Inngest).
> **CATEGORY:** Workflows
> **TIER:** 3+

---

## 🚦 ACTIVATION SIGNALS

- Keywords: `workflow orchestration`, `durable execution`, `n8n`, `Inngest`.
- Goal: Moving brittle scripts to production-grade automation.

---

## 🛠️ SUB-STEPS (EXECUTION PIPELINE)

1. **Information Extraction**: Identify triggers, inputs, and external dependencies.
2. **Platform Selection**: (n8n = accessible, Temporal = correct, Inngest = developer experience).
3. **Pattern Design**: Sequential, Parallel, or Orchestrator-Worker patterns.
4. **Idempotency**: Ensure external calls use keys for safe retry.
5. **Observability**: Set up onFailure handlers and metrics.

---

## 📝 OUTPUT SIGNATURE

- Workflow configurations (YAML, JSON, JS).
- Diagram of the flow (Mermaid).
- Backoff and retry policy definitions.

---

## 🧪 BENCHMARK TASK

- **Input**: "Build a durable 10-step payment flow with Inngest."
- **Output**: Workflow with idempotency keys -> Step-by-step logic -> Failure handling.
