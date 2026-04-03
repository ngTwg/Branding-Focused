---
name: "🏗️ Skill: System Architecture Design"
tags: ["activation", "antigravity", "architecture", "backend", "benchmark", "c:", "design", "execution", "gemini", "<YOUR_USERNAME>", "output", "pipeline", "signals", "signature", "skill", "steps", "sub", "system", "task", "users"]
tier: 3
risk: "medium"
estimated_tokens: 357
tools_needed: ["markdown", "terminal"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["platform", "api"]
quality_score: 0.58
---
# 🏗️ Skill: System Architecture Design

> **PURPOSE:** High-level architectural planning for scalability, availability, and performance.
> **CATEGORY:** Backend
> **TIER:** 4+

---

## 🚦 ACTIVATION SIGNALS

- Keywords: `design system`, `scalability`, `load balancing`, `caching strategy`.
- Goal: Architecting large-scale applications with multiple services/databases.

---

## 🛠️ SUB-STEPS (EXECUTION PIPELINE)

1. **Constraint Analysis**: Parse functional/non-functional constraints and infer scale (DAU/TPS).
2. **Architecture Search**: Generate **3 discrete variants** (e.g., Monolithic vs. Microservices vs. Serverless).
3. **Tradeoff Analysis**: Compare variants across Cost, Complexity, and Scalability using a matrix.
4. **Component Mapping**: Define Services, Load Balancers, API Gateways, and Message Queues.
5. **Data Flow Modeling**: Diagram the flow with complex Mermaid visualizations.
6. **Recommended Stack**: Select the best path with a technical rationale.

---

## 📝 OUTPUT SIGNATURE

- **Architecture Proposal**: Detailed document with ## sections.
- **Mermaid Diagrams**: Component interactions and data flows.
- **Tradeoff Table**: Pros/Cons matrix for the 3 variants.
- **Component Table**: Breakdown of each stack element.

---

## 🧪 BENCHMARK TASK

- **Input**: "Chat app 1M DAU architecture"
- **Output**: Multi-variant proposal -> Load balancer -> Services -> DB -> Cache diagram -> Selection rationale.
