---
name: "📥 Skill: Receiving Code Review"
tags: ["activation", "antigravity", "benchmark", "c:", "code", "execution", "frontend", "gemini", "<YOUR_USERNAME>", "output", "pipeline", "receiving", "review", "signals", "signature", "skill", "steps", "sub", "task", "users"]
tier: 3
risk: "medium"
estimated_tokens: 357
tools_needed: ["markdown", "terminal"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["web", "product"]
quality_score: 0.58
---
# 📥 Skill: Receiving Code Review

> **PURPOSE:** Professional and technically rigorous handling of code review feedback.
> **CATEGORY:** Workflows
> **TIER:** 1+

---

## 🚦 ACTIVATION SIGNALS

- Keywords: `review comments`, `incorporate feedback`, `fix items 1-X`.
- Goal: Responding to and implementing suggestions from a human partner or external reviewer.

---

## 🛠️ SUB-STEPS (EXECUTION PIPELINE)

1. **Read & Understand**: Complete feedback without reacting. Restate the requirement in your own words.
2. **Verify Context**: Check the suggestion against the actual codebase reality.
3. **Technical Evaluation**: Is it sound for THIS codebase? Does it violate YAGNI or project patterns?
4. **Structured Response**: Use technical acknowledgment or reasoned pushback.
5. **Incremental Fixes**: Implement suggestions one at a time, testing each.
6. **Pushback Strategy**: Push back if a suggestion breaks functionality, lacks context, or is technically incorrect.

---

## 📝 OUTPUT SIGNATURE

- Technical acknowledgment (e.g., "Fixed. [Brief description]").
- Reasoned pushback with evidence if a suggestion is declined.
- Commits for each resolved thread.

---

## 🧪 BENCHMARK TASK

- **Input**: "Fix items 1-3. Item 2: Use a more efficient sorting algorithm."
- **Output**: Implementation of 1 and 3 -> Analysis of item 2 (is a faster sort actually better for this data size?) -> Response with data-backed decision in item 2.
