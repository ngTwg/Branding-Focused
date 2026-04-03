---
name: "🗒️ Skill: Concise Planning"
tags: ["activation", "antigravity", "benchmark", "c:", "concise", "execution", "frontend", "gemini", "<YOUR_USERNAME>", "output", "pipeline", "planning", "signals", "signature", "skill", "steps", "sub", "task", "users", "workflows"]
tier: 3
risk: "medium"
estimated_tokens: 305
tools_needed: ["markdown", "terminal"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["web", "product"]
quality_score: 0.58
---
# 🗒️ Skill: Concise Planning

> **PURPOSE:** Turn complex user requests into a single, actionable plan with atomic steps.
> **CATEGORY:** Workflows
> **TIER:** 1+

---

## 🚦 ACTIVATION SIGNALS

- Keywords: `plan`, `roadmap`, `how will you build this?`, `action items`.
- Goal: Structured approach for a non-trivial task.

---

## 🛠️ SUB-STEPS (EXECUTION PIPELINE)

1. **Context Scan**: Read README, docs, and relevant code. Identify constraints.
2. **Minimal Clarification**: Ask max 1-2 questions only if blocking.
3. **Drafting Approach**: 1-3 sentences on what and why.
4. **Scope Definition**: Explicitly state what is IN and OUT.
5. **Itemization**: 6-10 atomic, Verb-first tasks (e.g., "Add...", "Refactor...").
6. **Validation Step**: Include at least one task for testing/verification.

---

## 📝 OUTPUT SIGNATURE

- Comprehensive plan with headers: Approach, Scope, Action Items, Open Questions.
- Each item is a checkbox [ ].

---

## 🧪 BENCHMARK TASK

- **Input**: "Plan the migration of this project from CommonJS to ESM."
- **Output**: Approach (migration strategy) -> Scope (files/folders) -> Action Items: package.json update -> file extension changes -> import/export rewrite -> test run -> verification.
