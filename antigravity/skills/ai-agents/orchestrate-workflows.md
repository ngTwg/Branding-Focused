---
name: "orchestrate-workflows"
tags: ["agent", "agents", "ai", "ai-agents", "antigravity", "c:", "correction", "fan", "frontend", "gemini", "hierarchical", "iterative", "<YOUR_USERNAME>", "linear", "loop", "manager", "orchestrate", "orchestration", "out", "parallel"]
tier: 3
risk: "medium"
estimated_tokens: 865
tools_needed: ["markdown"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["web", "product"]
quality_score: 0.70
author: "Antigravity System"
description: "Comprehensive patterns for multi-agent coordination, orchestration (Sequential, Parallel, Hierarchical, Loop), failure management, and state persistence. Trigger: agent orchestration, multi-agent systems, LangGraph, CrewAI, AutoGen patterns."
version: "1.0"
---
# 🤖 ORCHESTRATE AI AGENT WORKFLOWS

> **MANDATORY:** Apply these patterns when designing or debugging systems involving 2+ autonomous agents or complex tool-use loops.

---

## 🏗️ ORCHESTRATION PATTERNS

### 1. Sequential (Linear Pipeline)
Tasks flow in a fixed order. Output of Agent A becomes input for Agent B.
*   **Best Use:** Standardized processes (e.g., `Research -> Draft -> Review -> Finalize`).
*   **Risk:** Latency accumulation; if one step fails, the pipeline breaks.

### 2. Parallel (Fan-Out/Fan-In)
Independent sub-tasks are distributed simultaneously.
*   **Best Use:** Independent data processing or multi-source research.
*   **Risk:** Requires complex synthesis ("Fan-In") logic to merge disparate results.

### 3. Hierarchical (Supervisor/Manager)
A central "Manager" agent delegates to specialized "Workers".
*   **Best Use:** Complex projects where the path isn't known upfront.
*   **Risk:** Manager becomes a bottleneck or fails to decompose correctly.

### 4. Loop (Iterative/Self-Correction)
Agents cycle through steps until a "Validator" or "User" approves.
*   **Best Use:** Code generation, creative writing, or high-accuracy tasks.
*   **Risk:** Infinite loops (Stagnation). Requires a `max_retries` circuit breaker.

---

## 🛡️ FAILURE MANAGEMENT & RESILIENCE

| Strategy | Technical Implementation | Goal |
|:---|:---|:---|
| **Checkpointing** | Save state to DB/Disk at every node transition. | Resume from failure without restarting. |
| **Circuit Breakers** | Stop execution after N consecutive failures. | Prevent token drain and cascading errors. |
| **Exponential Backoff** | Wait `2^n * base` ms between retries. | Handle rate limits or temporary API outages. |
| **Fallbacks** | Switch to a "dumb" agent or prompt if "smart" fails. | Maintain basic functionality. |

---

## 🧠 STATE & MEMORY MANAGEMENT

### 1. Short-Term (Context Window)
*   **Mechanism:** Append interaction history to the current prompt.
*   **Limit:** Token window size. Requires truncation/summarization logic.

### 2. Long-Term (RAG/Persistent)
*   **Mechanism:** Vector stores (Pinecone/Chroma) or Structured DBs (Postgres).
*   **Use Case:** Cross-session history, global preferences, learned facts.

### 3. Shared Blackboard (Central State)
*   **Mechanism:** A shared JSON object/dictionary that all agents can read/write.
*   **Best Practice:** Use Pydantic schemas to ensure state data consistency.

---

## 🛠️ FRAMEWORK SELECTION MATRIX

| Framework | Core Philosophy | Best For |
|:---|:---|:---|
| **LangGraph** | Graph-based (Nodes/Edges) | Production, stateful, complex routing. |
| **CrewAI** | Role-based collaboration | Business process automation, team-sim. |
| **AutoGen** | Conversational dialogue | Dynamic research, exploratory problem solving. |

---

## 🚦 ANTI-PATTERNS (REJECT THESE)

- **Unbounded Loops**: Never allow agents to loop without a hard exit condition.
- **Silent Failures**: Always log/raise when an agent fails to parse or call a tool.
- **Global State Contention**: Avoid multiple agents writing to the same state field simultaneously without locking/serialization.
