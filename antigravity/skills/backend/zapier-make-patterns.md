---
name: "⚡ Skill: Zapier and Make Patterns"
tags: ["activation", "and", "antigravity", "backend", "benchmark", "c:", "execution", "frontend", "gemini", "<YOUR_USERNAME>", "make", "output", "patterns", "pipeline", "signals", "signature", "skill", "steps", "sub", "task"]
tier: 3
risk: "medium"
estimated_tokens: 303
tools_needed: ["markdown", "terminal"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["web", "product"]
quality_score: 0.58
---
# ⚡ Skill: Zapier and Make Patterns

> **PURPOSE:** Low-code/No-code automation for multi-app connectors (Zapier, Make.com).
> **CATEGORY:** Backend
> **TIER:** 2+

---

## 🚦 ACTIVATION SIGNALS

- Keywords: `Zapier`, `Make`, `automation`, `connect App A to App B`.
- Goal: Integrating external services via triggers, webhooks, and actions.

---

## 🛠️ SUB-STEPS (EXECUTION PIPELINE)

1. **Trigger Definition**: Set up webhook or app-specific polling (e.g., New Email in Gmail).
2. **Logic Flow**: Implement Filters and Routers for conditional steps.
3. **Action Formatting**: Clean data (text/number/date) for target tool requirements.
4. **App Connection**: Authenticate and map required/optional fields to target actions (e.g., Create Row in Sheets).
5. **Durable Testing**: Run step-by-step to verify mapping and error handling.
6. **Maintenance**: Set up alerts for failed task executions.

---

## 📝 OUTPUT SIGNATURE

- Zapier/Make blueprint (JSON).
- Mapping documentation.
- Error handling policy.

---

## 🧪 BENCHMARK TASK

- **Input**: "Sync New Stripe Customers to a Discord Notification channel."
- **Output**: Stripe Trigger (New Customer) -> Filter (if amount > $X) -> Discord Action (Send Message).
