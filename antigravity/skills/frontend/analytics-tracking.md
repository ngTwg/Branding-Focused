---
name: "📊 Skill: Analytics Tracking"
tags: ["activation", "analytics", "antigravity", "benchmark", "c:", "execution", "frontend", "gemini", "<YOUR_USERNAME>", "output", "pipeline", "signals", "signature", "skill", "steps", "sub", "task", "tracking", "users"]
tier: 3
risk: "medium"
estimated_tokens: 357
tools_needed: ["markdown"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["web", "product"]
quality_score: 0.58
---
# 📊 Skill: Analytics Tracking

> **PURPOSE:** Design and implement reliable, cross-platform event tracking and measurement.
> **CATEGORY:** Frontend
> **TIER:** 1+

---

## 🚦 ACTIVATION SIGNALS

- Keywords: `Google Analytics`, `GA4`, `Segment`, `event tracking`, `conversion pixel`.
- Task: Setting up new properties, implementing purchase events, or tracking user journeys.

---

## 🛠️ SUB-STEPS (EXECUTION PIPELINE)

1. **Information Extraction**: Identify business goals and required KPIs (Key Performance Indicators).
2. **Implementation Strategy**: Choose between Google Tag Manager (GTM), Direct Snippets, or Customer Data Platforms (Segment).
3. **Event Planning**: Define: Category -> Action -> Label -> Value (Universal) or Event Name -> Parameters (GA4).
4. **Data Layer Setup**: implement `window.dataLayer.push({ ... })` for consistent data transfer.
5. **Validation**: Use Debuggers (GTM Preview, GA4 DebugView) to verify event firing and parameter accuracy.
6. **Cross-Platform Measurement**: Ensure UTM parameters and identity stitching are handled across domains/devices.

---

## 📝 OUTPUT SIGNATURE

- Tracking plans (Google Sheets, Markdown).
- GTM configurations (JSON).
- Event implementation code (JS/TS).

---

## 🧪 BENCHMARK TASK

- **Input**: "Implement a purchase event for our checkout flow in GA4."
- **Output**: `gtag('event', 'purchase', { ... })` with: transaction_id -> value -> currency -> items.
