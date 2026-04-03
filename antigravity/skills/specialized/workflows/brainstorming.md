---
name: "brainstorming"
tags: ["antigravity", "approaches", "brainstorming", "c:", "concept", "design", "exploring", "frontend", "gemini", "intent", "key", "<YOUR_USERNAME>", "post", "presenting", "principles", "slim", "specialized", "the", "understanding", "users"]
tier: 2
risk: "medium"
estimated_tokens: 440
tools_needed: ["git", "markdown"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["web", "product"]
quality_score: 0.62
description: "You MUST use this before any creative work - creating features, building components, adding functionality, or modifying behavior. Explores user intent, requirements and design before implementation."
---
# Brainstorming - Concept to Design (v6.5.0-SLIM)

Turn ideas into fully formed designs through natural collaborative dialogue.

## 1. Understanding Intent
- **Initial check:** Review current project state (files, docs, recent commits) first.
- **Refinement:** Ask one clarifying question at a time to narrow down the idea.
- **Question Priority:** Multiple-choice or specific constraints. No "blue sky" open questions unless necessary.
- **Focus:** Purpose, constraints, success criteria.

## 2. Exploring Approaches
- Propose 2-3 different approaches with trade-offs.
- **Recommendation First:** Lead with your recommended option and reasoning.
- **Comparison Table:** Always present a visual comparison of options if they are technically distinct.

## 3. Presenting the Design
- Break design into sections (200-300 words).
- **Validation:** Ask for feedback after each section.
- **Coverage:** Architecture, components, data flow, error handling, testing.

## 4. Post-Design Workflow
- **Documentation:** Write the validated design to `docs/plans/YYYY-MM-DD-<topic>-design.md`.
- **Git:** Commit the design doc immediately after validation.
- **Handover:** Use `superpowers:writing-plans` to create the detailed implementation plan.

## Key Principles
- **One question at a time:** Don't overwhelm the user.
- **YAGNI ruthlessly:** Remove unnecessary features from all designs.
- **Check-ins:** Present designs in sections, validate each.
- **Flexibility:** Be ready to pivot if design assumptions are challenged.
