---
name: "Saga Orchestration Playbook"
tags: ["antigravity", "c:", "checklist", "choose", "choreography", "design", "failure", "frontend", "gemini", "handling", "implementation", "<YOUR_USERNAME>", "orchestration", "playbook", "resources", "saga", "specialized", "users", "verification", "when"]
tier: 3
risk: "medium"
estimated_tokens: 214
tools_needed: ["markdown"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["web", "product"]
quality_score: 0.57
---
# Saga Orchestration Playbook

## When to choose orchestration vs choreography

- Choose orchestration when business flow visibility and centralized control are required.
- Choose choreography when autonomy is high and coupling is low.

## Saga design checklist

- Define explicit saga state machine.
- Define timeout policy per step.
- Define compensation action for each irreversible step.
- Use idempotency keys for command handling.
- Store correlation IDs across all events and logs.

## Failure handling

- Retry transient failures with bounded exponential backoff.
- Escalate non-recoverable failures to compensation state.
- Capture operator-visible failure reason and current step.

## Verification

- Simulate failure at every step and confirm compensation path.
- Validate duplicate message handling.
- Validate recovery from orchestrator restart.
