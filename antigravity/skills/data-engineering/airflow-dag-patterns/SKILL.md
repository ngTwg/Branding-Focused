---
name: "airflow-dag-patterns"
tags: ["airflow", "antigravity", "apache", "c:", "dag", "data", "data-engineering", "engineering", "frontend", "gemini", "instructions", "<YOUR_USERNAME>", "not", "patterns", "resources", "safety", "skill", "this", "use", "users"]
tier: 3
risk: "medium"
estimated_tokens: 369
tools_needed: ["markdown"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["web", "product"]
quality_score: 0.62
date_added: "2026-02-27"
description: "Build production Apache Airflow DAGs with best practices for operators, sensors, testing, and deployment. Use when creating data pipelines, orchestrating workflows, or scheduling batch jobs."
source: "community"
---
# Apache Airflow DAG Patterns

Production-ready patterns for Apache Airflow including DAG design, operators, sensors, testing, and deployment strategies.

## Use this skill when

- Creating data pipeline orchestration with Airflow
- Designing DAG structures and dependencies
- Implementing custom operators and sensors
- Testing Airflow DAGs locally
- Setting up Airflow in production
- Debugging failed DAG runs

## Do not use this skill when

- You only need a simple cron job or shell script
- Airflow is not part of the tooling stack
- The task is unrelated to workflow orchestration

## Instructions

1. Identify data sources, schedules, and dependencies.
2. Design idempotent tasks with clear ownership and retries.
3. Implement DAGs with observability and alerting hooks.
4. Validate in staging and document operational runbooks.

Refer to `resources/implementation-playbook.md` for detailed patterns, checklists, and templates.

## Safety

- Avoid changing production DAG schedules without approval.
- Test backfills and retries carefully to prevent data duplication.

## Resources

- `resources/implementation-playbook.md` for detailed patterns, checklists, and templates.
