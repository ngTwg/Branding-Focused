---
name: "🐞 Skill: Debug Errors"
tags: ["activation", "antigravity", "benchmark", "c:", "debug", "errors", "execution", "gemini", "<YOUR_USERNAME>", "output", "pipeline", "signals", "signature", "skill", "steps", "sub", "task", "users", "workflows"]
tier: 3
risk: "medium"
estimated_tokens: 280
tools_needed: ["markdown", "terminal"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["engineering", "productivity"]
quality_score: 0.57
---
# 🐞 Skill: Debug Errors

> **PURPOSE:** Systematic root cause analysis and resolution of errors/bugs.
> **CATEGORY:** Workflows
> **TIER:** 1-2+

---

## 🚦 ACTIVATION SIGNALS
- Keywords: `error`, `bug`, `fix`, `not working`, `traceback`, `fail`.
- Task: Failing tests, runtime exceptions, reported regressions.

---

## 🛠️ SUB-STEPS (EXECUTION PIPELINE)

1. **Reproduction**: Isolate the failing component and trigger the error deterministically.
2. **Context Enrichment**: Map stack trace to source code lines and variables.
3. **Hypothesis Formulation**: Identify potential root causes (off-by-one, null reference, async race, missing env, etc.).
4. **Isolate & Patch**: Apply a minimal fix to the root cause without touching collateral code.
5. **Regression Check**: Re-run the reproduction sequence and verify success.

---

## 📝 OUTPUT SIGNATURE
- Description of the root cause.
- Fixed code snippet/patch.
- Recommendation for prevention (e.g., add check, add test).

---

## 🧪 BENCHMARK TASK
- **Input**: "Fix 'undefined is not a function' in this checkout flow."
- **Output**: Null check -> fallback -> error log.
