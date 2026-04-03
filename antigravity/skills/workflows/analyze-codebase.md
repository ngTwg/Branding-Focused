---
name: "🔍 Skill: Analyze Codebase"
tags: ["activation", "analyze", "antigravity", "benchmark", "c:", "codebase", "execution", "frontend", "gemini", "<YOUR_USERNAME>", "output", "pipeline", "signals", "signature", "skill", "steps", "sub", "task", "users", "workflows"]
tier: 3
risk: "medium"
estimated_tokens: 316
tools_needed: ["markdown", "terminal"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["web", "product"]
quality_score: 0.58
---
# 🔍 Skill: Analyze Codebase

> **PURPOSE:** Holistic understanding of complex code repositories before making modifications.
> **CATEGORY:** Workflows
> **TIER:** 2+

---

## 🚦 ACTIVATION SIGNALS

- Keywords: `analyze`, `understand`, `review architecture`, `how does X work?`
- Task: Onboarding a new repository or major cross-file feature.

---

## 🛠️ SUB-STEPS (EXECUTION PIPELINE)

1. **Holistic Scan**: Read entry points (README, index, main, package.json) to understand top-level structure.
2. **Entity Mapping**: Identify core classes, functions, and their relationships (mental graph).
3. **Control Flow Analysis**: Trace how data flows from user input/CLI to core logic and back.
4. **Pattern Recognition**: Detect architectural patterns (MVC, Hexagonal, Singleton, etc.).
5. **Constraint Extraction**: Identify coding standards, lints, and performance requirements.

---

## 📝 OUTPUT SIGNATURE

- High-level architecture summary.
- List of core components and their roles.
- "Action Plan" for subsequent tasks.
- (Optional) Mermaid diagram for critical flows.

---

## 🧪 BENCHMARK TASK

- **Input**: "Analyze the authentication flow in this Express app."
- **Output**: Diagram of middleware chain -> Auth controller logic -> DB query -> Session management.
