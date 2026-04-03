---
name: "🏁 Skill: Verification Before Completion"
tags: ["activation", "antigravity", "before", "benchmark", "c:", "completion", "execution", "frontend", "gemini", "<YOUR_USERNAME>", "output", "pipeline", "signals", "signature", "skill", "steps", "sub", "task", "users", "verification"]
tier: 3
risk: "medium"
estimated_tokens: 264
tools_needed: ["markdown", "terminal"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["web", "product"]
quality_score: 0.57
---
# 🏁 Skill: Verification Before Completion

> **PURPOSE:** Ensure every success claim is backed by fresh, complete evidence.
> **CATEGORY:** Workflows
> **TIER:** 1+

---

## 🚦 ACTIVATION SIGNALS

- Keywords: `complete`, `fixed`, `all passing`, `ready for review`.
- Goal: Final validation before a commit or task closure.

---

## 🛠️ SUB-STEPS (EXECUTION PIPELINE)

1. **Identification**: What command (test, build, lint) proves the claim?
2. **Fresh Run**: Execute the FULL verification suite immediately before claiming.
3. **Observation**: Read all output and check exit codes.
4. **Conclusion**: State the claim CLEARLY WITH EVIDENCE (e.g., "34/34 tests pass").
5. **Red Flag Prevention**: Stop if using "should", "seems to", or "probably."

---

## 📝 OUTPUT SIGNATURE

- Evidence (test output, build status, lint report).
- Direct claim of completion with failure count.

---

## 🧪 BENCHMARK TASK

- **Input**: "Tell the user everything is fixed."
- **Output**: Run `npm test` -> Success -> "All 56 tests pass, fixed the regression. Ready to commit."
