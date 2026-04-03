---
name: "⚖️ Skill: AB Test Setup"
tags: ["ab", "activation", "antigravity", "benchmark", "c:", "execution", "frontend", "gemini", "<YOUR_USERNAME>", "output", "pipeline", "setup", "signals", "signature", "skill", "steps", "sub", "task", "test", "users"]
tier: 3
risk: "medium"
estimated_tokens: 360
tools_needed: ["markdown"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["web", "product"]
quality_score: 0.58
---
# ⚖️ Skill: AB Test Setup

> **PURPOSE:** Design and implement statistically valid, actionable A/B experiments.
> **CATEGORY:** Frontend
> **TIER:** 2+

---

## 🚦 ACTIVATION SIGNALS

- Keywords: `A/B test`, `split test`, `experiment`, `variant copy`.
- Goal: Testing hypotheses to improve conversion or user experience.

---

## 🛠️ SUB-STEPS (EXECUTION PIPELINE)

1. **Hypothesis Framework**: Define: Observation -> Change -> Expected Outcome -> Audience -> Metrics.
2. **Metric Selection**: Set Primary (success), Secondary (context), and Guardrail (harm prevention) metrics.
3. **Sample Size Calculation**: Pre-determine required traffic using Evan Miller's or Optimizely's calculators.
4. **Variant Design**: Implement Control (A) and Variant (B) with a single, meaningful change.
5. **Implementation**: Choose between Client-Side (JS modification) or Server-Side (pre-rendered) testing.
6. **Execution Monitoring**: Watch for technical issues but DO NOT peek or stop early before reaching sample size.
7. **Analysis**: Check for Statistical Significance (95%) and Practical Business Impact.

---

## 📝 OUTPUT SIGNATURE

- Test plan documentation.
- Variant implementation (React/HTML/Server).
- Analysis summaries.

---

## 🧪 BENCHMARK TASK

- **Input**: "Test whether a larger 'Sign Up' button increases conversion."
- **Output**: Plan with: Hypothesis -> Metrics (CTR) -> Control vs. Variant (large button) -> PostHog/Optimizely setup.
