---
name: "attack-tree-construction"
tags: ["antigravity", "attack", "c:", "construction", "frontend", "gemini", "instructions", "<YOUR_USERNAME>", "not", "resources", "safety", "skill", "specialized", "this", "tree", "use", "users", "when"]
tier: 2
risk: "medium"
estimated_tokens: 373
tools_needed: ["markdown"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["web", "product"]
quality_score: 0.62
date_added: "2026-02-27"
description: "Build comprehensive attack trees to visualize threat paths. Use when mapping attack scenarios, identifying defense gaps, or communicating security risks to stakeholders."
source: "community"
---
> AUTHORIZED USE ONLY: Use this skill only for authorized security assessments, defensive validation, or controlled educational environments.

# Attack Tree Construction

Systematic attack path visualization and analysis.

## Use this skill when

- Visualizing complex attack scenarios
- Identifying defense gaps and priorities
- Communicating risks to stakeholders
- Planning defensive investments or test scopes

## Do not use this skill when

- You lack authorization or a defined scope to model the system
- The task is a general risk review without attack-path modeling
- The request is unrelated to security assessment or design

## Instructions

- Confirm scope, assets, and the attacker goal for the root node.
- Decompose into sub-goals with AND/OR structure.
- Annotate leaves with cost, skill, time, and detectability.
- Map mitigations per branch and prioritize high-impact paths.
- If detailed templates are required, open `resources/implementation-playbook.md`.

## Safety

- Share attack trees only with authorized stakeholders.
- Avoid including sensitive exploit details unless required.

## Resources

- `resources/implementation-playbook.md` for detailed patterns, templates, and examples.
