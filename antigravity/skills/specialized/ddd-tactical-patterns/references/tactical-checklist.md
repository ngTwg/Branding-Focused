---
name: "Tactical Pattern Checklist"
tags: ["aggregate", "antigravity", "c:", "checklist", "ddd", "design", "domain", "events", "gemini", "<YOUR_USERNAME>", "objects", "pattern", "patterns", "references", "repositories", "specialized", "tactical", "users", "value"]
tier: 3
risk: "high"
estimated_tokens: 152
tools_needed: ["markdown"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["specialized", "domain"]
quality_score: 0.56
---
# Tactical Pattern Checklist

## Aggregate design

- One aggregate root per transaction boundary
- Invariants enforced inside aggregate methods
- Avoid cross-aggregate synchronous consistency rules

## Value objects

- Immutable by default
- Validation at construction
- Equality by value, not identity

## Repositories

- Persist and load aggregate roots only
- Expose domain-friendly query methods
- Avoid leaking ORM entities into domain layer

## Domain events

- Past-tense event names (for example, `OrderSubmitted`)
- Include minimal, stable event payloads
- Version event schema before breaking changes
