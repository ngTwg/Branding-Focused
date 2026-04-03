---
name: "♻️ Skill: TDD Workflow"
tags: ["activation", "antigravity", "benchmark", "c:", "execution", "frontend", "gemini", "<YOUR_USERNAME>", "output", "pipeline", "signals", "signature", "skill", "steps", "sub", "task", "tdd", "users", "workflow", "workflows"]
tier: 3
risk: "medium"
estimated_tokens: 283
tools_needed: ["markdown", "terminal"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["web", "product"]
quality_score: 0.58
---
# ♻️ Skill: TDD Workflow

> **PURPOSE:** Test-Driven Development workflow (Red-Green-Refactor) for code quality and reliability.
> **CATEGORY:** Workflows
> **TIER:** 1+

---

## 🚦 ACTIVATION SIGNALS

- Keywords: `TDD`, `write tests first`, `Red-Green-Refactor`.
- Goal: Implementing critical features or bug fixes with a safety net.

---

## 🛠️ SUB-STEPS (EXECUTION PIPELINE)

1. **🔴 Red Phase**: Write a failing test for the next piece of behavior. Run it and watch it fail.
2. **🟢 Green Phase**: Write only enough code to make the failing test pass.
3. **🔵 Refactor Phase**: Clean up the current code while ensuring tests stay green.
4. **Pattern Application**: Use AAA (Arrange-Act-Assert) for each test.
5. **Simplicity Verification**: If a test can't be written, rethink the requirements.

---

## 📝 OUTPUT SIGNATURE

- Test files and implementation files created in sequence.
- Test run output showing 0 failures.
- Record of incremental commits.

---

## 🧪 BENCHMARK TASK

- **Input**: "Add a function to calculate Fibonacci numbers using TDD."
- **Output**: Test for fib(0) -> Red -> Impl -> Green -> Test for fib(1) -> etc.
