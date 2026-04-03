---
name: "Event Store Design Playbook"
tags: ["and", "antigravity", "c:", "checklist", "design", "event", "frontend", "gemini", "guardrails", "implementation", "<YOUR_USERNAME>", "operational", "performance", "playbook", "projection", "resources", "safety", "schema", "specialized", "store"]
tier: 2
risk: "medium"
estimated_tokens: 186
tools_needed: ["markdown"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["web", "product"]
quality_score: 0.57
---
# Event Store Design Playbook

## Schema and stream strategy

- Use append-only writes with optimistic concurrency.
- Keep per-stream ordering and global ordering indexes.
- Include metadata fields for causation and correlation IDs.

## Operational guardrails

- Never mutate historical events in production.
- Version event schema with explicit upcasters/downcasters policy.
- Define retention and archival strategy by stream type.

## Subscription and projection safety

- Track per-subscriber checkpoint positions.
- Make handlers idempotent and replay-safe.
- Support projection rebuild from a clean checkpoint.

## Performance checklist

- Index stream id + version.
- Index global position.
- Add snapshot policy for long-lived aggregates.
