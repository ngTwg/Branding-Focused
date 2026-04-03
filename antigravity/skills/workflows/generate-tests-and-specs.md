---
name: "🧪 Skill: Generate Tests and Specs"
tags: ["activation", "and", "antigravity", "benchmark", "c:", "execution", "gemini", "generate", "<YOUR_USERNAME>", "output", "pipeline", "signals", "signature", "skill", "specs", "steps", "sub", "task", "tests", "users"]
tier: 3
risk: "medium"
estimated_tokens: 274
tools_needed: ["markdown", "pytest", "terminal"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["engineering", "productivity"]
quality_score: 0.57
---
# 🧪 Skill: Generate Tests and Specs

> **PURPOSE:** Create automated tests and specification documents for code quality.
> **CATEGORY:** Workflows
> **TIER:** 1+

---

## 🚦 ACTIVATION SIGNALS
- Keywords: `write tests`, `unit test`, `integration test`, `TDD`, `specs`.
- Task: Finalizing a feature or debugging a regression.

---

## 🛠️ SUB-STEPS (EXECUTION PIPELINE)

1. **Coverage Analysis**: Identify happy path, edge cases, and failure modes.
2. **Framework Selection**: Use project-specific tools (Vitest, Jest, PyTest, etc.).
3. **Mocking/Stubbing**: Isolate the unit of work from external services.
4. **Implementation**: Write the test code following AAA (Arrange-Act-Assert).
5. **Spec Doc generation**: (Optional) Write a high-level overview of what the tests cover.

---

## 📝 OUTPUT SIGNATURE
- Code blocks for test files.
- Command to run tests.
- Brief explanation of the test strategy.

---

## 🧪 BENCHMARK TASK
- **Input**: "Add unit tests for this new sorting utility."
- **Output**: Test file with: Integer sort -> Float sort -> Empty list -> One element -> Type error handling.
