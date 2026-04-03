---
name: "dbt-transformation-patterns"
tags: ["antigravity", "c:", "dbt", "frontend", "gemini", "instructions", "<YOUR_USERNAME>", "not", "patterns", "resources", "skill", "specialized", "this", "transformation", "use", "users", "when"]
tier: 2
risk: "medium"
estimated_tokens: 325
tools_needed: ["markdown", "sql"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["web", "product"]
quality_score: 0.60
date_added: "2026-02-27"
description: "Production-ready patterns for dbt (data build tool) including model organization, testing strategies, documentation, and incremental processing."
source: "community"
---
# dbt Transformation Patterns

Production-ready patterns for dbt (data build tool) including model organization, testing strategies, documentation, and incremental processing.

## Use this skill when

- Building data transformation pipelines with dbt
- Organizing models into staging, intermediate, and marts layers
- Implementing data quality tests and documentation
- Creating incremental models for large datasets
- Setting up dbt project structure and conventions

## Do not use this skill when

- The project is not using dbt or a warehouse-backed workflow
- You only need ad-hoc SQL queries
- There is no access to source data or schemas

## Instructions

- Define model layers, naming, and ownership.
- Implement tests, documentation, and freshness checks.
- Choose materializations and incremental strategies.
- Optimize runs with selectors and CI workflows.
- If detailed patterns are required, open `resources/implementation-playbook.md`.

## Resources

- `resources/implementation-playbook.md` for detailed dbt patterns and examples.
