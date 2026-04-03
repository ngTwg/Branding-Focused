---
name: "✅ Skill: Code Review Checklist"
tags: ["activation", "antigravity", "benchmark", "c:", "checklist", "code", "execution", "frontend", "gemini", "<YOUR_USERNAME>", "output", "pipeline", "review", "signals", "signature", "skill", "steps", "sub", "task", "users"]
tier: 3
risk: "medium"
estimated_tokens: 321
tools_needed: ["markdown", "sql", "terminal"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["web", "product"]
quality_score: 0.58
---
# ✅ Skill: Code Review Checklist

> **PURPOSE:** Comprehensive checklist for conducting thorough code reviews covering functionality, security, performance, and maintainability.
> **CATEGORY:** Workflows
> **TIER:** 1+

---

## 🚦 ACTIVATION SIGNALS

- Keywords: `review code`, `PR audit`, `checklist`, `quality check`.
- Task: Reviewing a pull request or codebase audit.

---

## 🛠️ SUB-STEPS (EXECUTION PIPELINE)

1. **Context Understanding**: What problem does this solve? What are the requirements?
2. **Functionality Review**: Does it work? Are edge cases handled?
3. **Architecture & Standards**: Does it follow project patterns? Is it readable?
4. **Security Audit**: SQLi, XSS, CSRF, sensitive data exposure, dependency vulnerabilities.
5. **Performance Check**: N+1 queries, memory leaks, unnecessary loops.
6. **Test Verification**: Are there meaningful tests for new logic?

---

## 📝 OUTPUT SIGNATURE

- Systematic checklist with items marked as [Pass/Fail/N/A].
- Specific comments on problematic code blocks.
- Actionable suggestions for improvement.

---

## 🧪 BENCHMARK TASK

- **Input**: "Review this new user registration logic."
- **Output**: Checklist covering: Input validation -> Password hashing -> DB transaction logic -> Error messaging -> Unit test coverage.
