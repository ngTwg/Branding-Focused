---
name: "code-review-excellence"
tags: ["antigravity", "c:", "code", "excellence", "format", "frontend", "gemini", "instructions", "<YOUR_USERNAME>", "not", "output", "resources", "review", "skill", "this", "use", "users", "when", "workflows"]
tier: 2
risk: "medium"
estimated_tokens: 349
tools_needed: ["markdown", "terminal"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["web", "product"]
quality_score: 0.62
date_added: "2026-02-27"
description: "Transform code reviews from gatekeeping to knowledge sharing through constructive feedback, systematic analysis, and collaborative improvement."
source: "community"
---
# Code Review Excellence

Transform code reviews from gatekeeping to knowledge sharing through constructive feedback, systematic analysis, and collaborative improvement.

## Use this skill when

- Reviewing pull requests and code changes
- Establishing code review standards
- Mentoring developers through review feedback
- Auditing for correctness, security, or performance

## Do not use this skill when

- There are no code changes to review
- The task is a design-only discussion without code
- You need to implement fixes instead of reviewing

## Instructions

- Read context, requirements, and test signals first.
- Review for correctness, security, performance, and maintainability.
- Provide actionable feedback with severity and rationale.
- Ask clarifying questions when intent is unclear.
- If detailed checklists are required, open `resources/implementation-playbook.md`.

## Output Format

- High-level summary of findings
- Issues grouped by severity (blocking, important, minor)
- Suggestions and questions
- Test and coverage notes

## Resources

- `resources/implementation-playbook.md` for detailed review patterns and templates.
