---
name: "Antigravity Workflows Implementation Playbook"
tags: ["antigravity", "artifact", "c:", "completion", "contract", "examples", "execution", "format", "frontend", "gemini", "guardrails", "implementation", "<YOUR_USERNAME>", "playbook", "resources", "safety", "specialized", "step", "suggested", "users"]
tier: 3
risk: "medium"
estimated_tokens: 251
tools_needed: ["markdown"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["web", "product"]
quality_score: 0.57
---
# Antigravity Workflows Implementation Playbook

This document explains how an agent should execute workflow-based orchestration.

## Execution Contract

For every workflow:

1. Confirm objective and scope.
2. Select the best-matching workflow.
3. Execute workflow steps in order.
4. Produce one concrete artifact per step.
5. Validate before continuing.

## Step Artifact Examples

- Plan step -> scope document or milestone checklist.
- Build step -> code changes and implementation notes.
- Test step -> test results and failure triage.
- Release step -> rollout checklist and risk log.

## Safety Guardrails

- Never run destructive actions without explicit user approval.
- If a required skill is missing, state the gap and fallback to closest available skill.
- When security testing is involved, ensure authorization is explicit.

## Suggested Completion Format

At workflow completion, return:

1. Completed steps
2. Artifacts produced
3. Validation evidence
4. Open risks
5. Suggested next action
