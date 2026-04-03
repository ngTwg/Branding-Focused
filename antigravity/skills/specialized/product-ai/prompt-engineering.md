---
name: "prompt-engineering"
tags: ["ai", "antigravity", "c:", "constraints", "context", "design", "engineering", "examples", "few", "framework", "gemini", "how", "<YOUR_USERNAME>", "personas", "product", "prompt", "prompting", "role", "security", "shot"]
tier: 2
risk: "medium"
estimated_tokens: 649
tools_needed: ["markdown"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["security", "compliance"]
quality_score: 0.68
description: "Structured prompt design for large language models. Covers System Prompting, Few-Shot, CoT, and Tool-calling strategies."
---
# Prompt Engineering - Design & Strategy (v6.5.0-SLIM)

Expert prompt engineering for structured, reliable LLM outputs (Claude, GPT, Gemini).

## Structured Prompting (The Framework)

### 1. Role (Personas)
Assign a specific role: "You are a Senior Security Architect."

### 2. Context (What)
Provide background data and the specific problem to solve.

### 3. Constraints (How)
Limits on length, tone, formatting, and disallowed topics.

### 4. Examples (Few-Shot)
Provide 3-5 high-quality examples of input/output pairs.

### 5. Format (Output)
Specify JSON, Markdown, or Pydantic schema structure.

## Advanced Patterns

### Chain-of-Thought (CoT)
Ask the model to "think step-by-step" before providing the final answer. This improves performance on complex reasoning tasks.

### Structured Feedback Loop
Prompt the model to "critique your own output and propose improvements."

### XML Tagging (Claude Special)
Use `<context>`, `<rules>`, and `<output>` tags to isolate prompt blocks for clearer parsing.

## Tool-Calling Optimization
- **Schema Design:** Keep parameters minimal and well-documented.
- **Fail-Safes:** Provide instructions for when a tool fails or is unavailable.

## Success Criteria
- **Predictability:** Always get the same output format for the same input.
- **Accuracy:** Zero hallucinations on provided data.
- **Speed:** Minimal tokens for the same task.

## Related Skills
`behavioral-modes`, `blockrun`.
---
name: ai-agent-skills
description: AI Agent Skill Architecture and Lookup. Defines the structure and management of modular capabilities.
---

# AI Agent Skills (v6.5.0-SLIM)

Modular capability framework for agentic systems.

## Skill Structure
Each skill resides in a directory with a standard `SKILL.md` file containing metadata (Name, Description, Tools) and instructions.

| Component | Purpose |
|-----------|---------|
| `SKILL.md` | Core instructions and metadata. |
| `tools/` | Tool definitions and execution logic. |
| `resources/` | Supporting data and templates. |

## Lookup Protocol
The orchestrator uses semantic matching to find relevant skills based on the user's task.
1. Parse user intent.
2. Search `MASTER_ROUTER`.
3. Load the matched `SKILL.md` into context.

## Best Practices
- **Atomic:** Each skill solves one core problem.
- **Lazy-Loading:** Skills are loaded only when needed to save tokens.
- **Standardized:** Use consistent naming and metadata for easy routing.
