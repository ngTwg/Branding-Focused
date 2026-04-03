---
name: "🛠️ Skill: Refactor Code"
tags: ["activation", "antigravity", "backend", "benchmark", "c:", "code", "execution", "gemini", "<YOUR_USERNAME>", "output", "pipeline", "refactor", "signals", "signature", "skill", "steps", "sub", "task", "users", "workflows"]
tier: 3
risk: "medium"
estimated_tokens: 298
tools_needed: ["markdown", "terminal"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["platform", "api"]
quality_score: 0.57
---
# 🛠️ Skill: Refactor Code

> **PURPOSE:** Improving code internal structure without changing external behavior.
> **CATEGORY:** Workflows
> **TIER:** 2+

---

## 🚦 ACTIVATION SIGNALS
- Keywords: `refactor`, `clean up`, `modularize`, `reorganize`, `dry-up`, `tech debt`.
- Task: Long monolithic files, redundant logic, outdated patterns.

---

## 🛠️ SUB-STEPS (EXECUTION PIPELINE)

1. **Impact Analysis**: Identify all calling sites to ensure zero regression.
2. **Atomic Inlining/Extraction**: Break down complex methods or combine redundant ones.
3. **Pattern Integration**: Replace ad-hoc logic with standard design patterns (Factory, Strategy, Observer).
4. **Naming Consistency**: Apply `camelCase`, `PascalCase`, or `snake_case` according to repository standards.
5. **Zero-Change Verification**: Perform dry-runs and compare outputs with original state.

---

## 📝 OUTPUT SIGNATURE
- Before-and-after diff (if small).
- Logic breakdown of restructured modules.
- (Optional) Verification script or manual test results.

---

## 🧪 BENCHMARK TASK
- **Input**: "Modularize this 500-line controller into separate services."
- **Output**: Clean controller -> 3 focused services -> Shared types.
