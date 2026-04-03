---
name: "Agent Prompt Templates"
tags: ["agent", "antigravity", "batch", "c:", "explorer", "frontend", "gemini", "<YOUR_USERNAME>", "main", "orchestrate", "prompt", "refactor", "references", "specialized", "synthesis", "template", "templates", "thread", "users", "worker"]
tier: 2
risk: "medium"
estimated_tokens: 340
tools_needed: ["markdown"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["web", "product"]
quality_score: 0.65
---
# Agent Prompt Templates

Use these templates when spawning sub-agents.

## Explorer Prompt Template

```
Analyze the target scope and return decomposition guidance only.

Scope:
- Paths/modules: <fill>
- Goal: <refactor|rewrite|hybrid>
- Constraints: <behavior/API/test constraints>

Return:
1. Intent map (what each area currently does)
2. Coupling and dependency risks
3. Candidate work packets with non-overlapping ownership
4. Validation commands per packet
5. Recommended execution order
```

## Worker Prompt Template

```
You own this packet and are not alone in the codebase.
Ignore unrelated edits by others and do not touch files outside ownership.

Packet:
- ID: <fill>
- Objective: <fill>
- Owned files: <fill>
- Dependencies already completed: <fill>
- Invariants to preserve: <fill>
- Required checks: <fill>

Execution requirements:
1. Implement only the packet objective.
2. Preserve specified invariants and external behavior.
3. Run required checks and report exact results.
4. Summarize changed files and any integration notes.
```

## Main Thread Synthesis Prompt Template

```
Merge explorer outputs into a single dependency-aware plan.
Produce:
1. Packet table with ownership and dependencies
2. Parallel execution waves (no overlap per wave)
3. Validation matrix by packet and integration stage
4. Risk list with mitigation actions
```
