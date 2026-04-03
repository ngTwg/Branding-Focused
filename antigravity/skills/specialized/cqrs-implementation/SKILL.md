---
name: "cqrs-implementation"
tags: ["antigravity", "c:", "cqrs", "frontend", "gemini", "implementation", "instructions", "<YOUR_USERNAME>", "not", "resources", "skill", "specialized", "this", "use", "users", "when"]
tier: 2
risk: "medium"
estimated_tokens: 317
tools_needed: ["markdown"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["web", "product"]
quality_score: 0.60
date_added: "2026-02-27"
description: "Implement Command Query Responsibility Segregation for scalable architectures. Use when separating read and write models, optimizing query performance, or building event-sourced systems."
source: "community"
---
# CQRS Implementation

Comprehensive guide to implementing CQRS (Command Query Responsibility Segregation) patterns.

## Use this skill when

- Separating read and write concerns
- Scaling reads independently from writes
- Building event-sourced systems
- Optimizing complex query scenarios
- Different read/write data models are needed
- High-performance reporting is required

## Do not use this skill when

- The domain is simple and CRUD is sufficient
- You cannot operate separate read/write models
- Strong immediate consistency is required everywhere

## Instructions

- Identify read/write workloads and consistency needs.
- Define command and query models with clear boundaries.
- Implement read model projections and synchronization.
- Validate performance, recovery, and failure modes.
- If detailed patterns are required, open `resources/implementation-playbook.md`.

## Resources

- `resources/implementation-playbook.md` for detailed CQRS patterns and templates.
