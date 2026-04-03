---
name: "🏙️ Skill: System Architecture Design"
tags: ["activation", "antigravity", "architecture", "backend", "benchmark", "c:", "design", "execution", "gemini", "<YOUR_USERNAME>", "output", "pipeline", "signals", "signature", "skill", "steps", "sub", "system", "task", "users"]
tier: 3
risk: "medium"
estimated_tokens: 330
tools_needed: ["markdown", "sql", "terminal"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["platform", "api"]
quality_score: 0.58
---
# 🏙️ Skill: System Architecture Design

> **PURPOSE:** Design scalable, resilient, and cost-effective system blueprints.
> **CATEGORY:** Backend
> **TIER:** 3+

---

## 🚦 ACTIVATION SIGNALS
- Keywords: `architecture`, `design system`, `scale to 1M users`, `microservices`, `infra`.
- Task: Defining high-level relationships between multiple services/databases.

---

## 🛠️ SUB-STEPS (EXECUTION PIPELINE)

1. **Constraint Discovery**: Scale targets (DAU, RPS), latency, consistency (ACID vs BASE), and budget.
2. **Variant Generation**: Enumerate 3 architecture options (e.g., Monolith, Serverless, Event-Driven).
3. **Tradeoff Analysis**: Compare options by complexity, cost, developer speed, and scale.
4. **Strategic Recommendation**: Propose the best "minimum viable architecture" (MVA).
5. **Component Detail**: Define databases (SQL vs NoSQL), caches, queues, and protocols (gRPC, REST, GraphQL).
6. **Resilience Plan**: Map failure modes and disaster recovery strategies.

---

## 📝 OUTPUT SIGNATURE
- Mermaid `graph TD` or `sequenceDiagram`.
- "Component Table": Name, Responsibility, Tech Stack.
- "Tradeoff Matrix": Comparison Across Dimensions.

---

## 🧪 BENCHMARK TASK
- **Input**: "Design a real-time chat system for 10M active users."
- **Output**: WebSockets -> Redis PubSub -> Sharded SQL/NoSQL -> Diagram.
