---
name: "conversation-memory"
tags: ["agents", "ai", "antigravity", "c:", "conversation", "core", "design", "frontend", "gemini", "governance", "implementation", "<YOUR_USERNAME>", "memory", "principles", "related", "skills", "slim", "specialized", "system", "systems"]
tier: 2
risk: "medium"
estimated_tokens: 654
tools_needed: ["markdown"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["web", "product"]
quality_score: 0.68
description: "Long-term and short-term memory systems for LLM conversations. Covers entity tracking, persistence, and tiered storage."
---
# Conversation Memory Systems (v6.5.0-SLIM)

Design and implement persistent memory to improve relevance and context across sessions.

## 1. Governance & Core Principles
- **Tiered Memory:** Short-term (buffer), long-term (summary/DB), and entity-based.
- **Intelligent Retrieval:** Only surface relevant memories for the current prompt.
- **Privacy:** Strict user isolation. No cross-contaminating memories between users.

## 2. Memory Types
- **Short-Term:** The last 10-20 messages in the current thread.
- **Long-Term:** Significant events, preferences, and outcomes summarized in a persistent store.
- **Entity Memory:** Facts about people, products, or concepts mentioned in the chat.

## 3. Implementation Workflow
1. Identify high-value information to remember.
2. Store information in a structure like: `Entity: [User], Property: [Preferred Language], Value: [TypeScript]`.
3. Consolidate and summarize old memories to fit in context windows.

## Related Skills
`rag-implementation`, `prompt-engineering`, `llm-npc-dialogue`.
---
name: design-system-core
description: Core component library and design tokens for UI development (React/Next.js/Native).
---

# Design System Core (v6.5.0-SLIM)

Foundational tokens and layout components for building consistent, performant user interfaces.

## 1. Design Tokens (Never Hard-Code)
| Token | Type | Use For |
|-------|------|---------|
| `$textPrimary` | Color | Main headings and body. |
| `$backgroundSecondary` | Color | Cards, sidebars, backgrounds. |
| `$2` | Spacing | 8px padding/margin. |
| `$4` | Spacing | 16px padding/margin (Standard). |
| `$md` | Typography | 16px font size. |

## 2. Layout Components
- **Box:** Base container with token support. `<Box padding="$4" />`.
- **HStack / VStack:** Horizontal/Vertical flex layouts with gap support. `<VStack gap="$3" />`.
- **Screen:** Root container for pages and mobile screens.

## 3. UI Components
- **Text:** Typography with `$xs` to `$2xl` sizing.
- **Button:** Variants (solid, outline, ghost) and states (loading, disabled).
- **Input:** Form inputs with integrated Zod validation support.
- **Card:** Self-contained content container with `CardHeader` and `CardBody`.

## 4. Best Practices
- **Composition over Inheritance:** Build complex UI from smaller, specialized components.
- **Standardized Prototyping:** Use core components for all new feature development.

## Related Skills
`frontend-patterns`, `react-ui-patterns`.

---

## 5. Multi-Agent Orchestration Templates (Wave 3)

### Template A: CrewAI-style planner -> coder -> reviewer loop

```python
from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class AgentResult:
	output: str
	meta: Dict[str, Any]

def planner_agent(task: str) -> AgentResult:
	plan = f"1) Decompose task: {task}\n2) Identify constraints\n3) Produce implementation steps"
	return AgentResult(output=plan, meta={"agent": "planner"})

def coder_agent(plan: str) -> AgentResult:
	code = f"# Generated from plan\n# {plan.splitlines()[0]}\nprint('implementation-ready')"
	return AgentResult(output=code, meta={"agent": "coder"})

def reviewer_agent(code: str) -> AgentResult:
	issues = []
	if "TODO" in code:
		issues.append("Unfinished implementation")
	verdict = "approve" if not issues else "reject"
	return AgentResult(output=verdict, meta={"issues": issues, "agent": "reviewer"})

def run_multi_agent(task: str) -> Dict[str, Any]:
	plan = planner_agent(task)
	candidate = coder_agent(plan.output)
	review = reviewer_agent(candidate.output)

	return {
		"task": task,
		"plan": plan.output,
		"code": candidate.output,
		"review": review.output,
		"issues": review.meta.get("issues", []),
	}

print(run_multi_agent("add JWT auth middleware"))
```

### Template B: LangGraph-style stateful workflow with memory checkpoints

```python
from typing import TypedDict, List

class AgentState(TypedDict):
	user_query: str
	steps: List[str]
	draft: str
	memory_notes: List[str]

def retrieve_memory(state: AgentState) -> AgentState:
	state["memory_notes"].append("User prefers concise production-ready snippets")
	return state

def plan_step(state: AgentState) -> AgentState:
	state["steps"] = [
		"parse intent",
		"select patterns",
		"produce answer",
	]
	return state

def generate_draft(state: AgentState) -> AgentState:
	state["draft"] = f"Plan for: {state['user_query']}\\n- " + "\\n- ".join(state["steps"])
	return state

def run_graph(user_query: str) -> AgentState:
	state: AgentState = {
		"user_query": user_query,
		"steps": [],
		"draft": "",
		"memory_notes": [],
	}
	for node in [retrieve_memory, plan_step, generate_draft]:
		state = node(state)
	return state

print(run_graph("design a resilient payment API"))
```

### Template C: Routing policy for multi-agent execution

```yaml
routing_policy:
  low_risk:
	chain: [planner, coder]
  medium_risk:
	chain: [planner, coder, reviewer]
  high_risk:
	chain: [planner, security_reviewer, coder, reviewer, approver]
  stop_conditions:
	- "reviewer rejects >= 2 rounds"
	- "missing required evidence"
```
