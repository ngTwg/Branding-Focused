---
name: "Naming & Coding Standards"
tags: ["antigravity", "avalonia", "c:", "coding", "development", "error", "gemini", "general", "handling", "<YOUR_USERNAME>", "naming", "specialized", "standards", "users", "zafiro"]
tier: 3
risk: "high"
estimated_tokens: 184
tools_needed: ["markdown"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["specialized", "domain"]
quality_score: 0.53
---
# Naming & Coding Standards

## General Standards

- **Explicit Names**: Favor clarity over cleverness.
- **Async Suffix**: Do **NOT** use the `Async` suffix in method names, even if they return `Task`.
- **Private Fields**: Do **NOT** use the `_` prefix for private fields.
- **Static State**: Avoid static state unless explicitly justified and documented.
- **Method Design**: Keep methods small, expressive, and with low cyclomatic complexity.

## Error Handling

- **Result & Maybe**: Use types from **CSharpFunctionalExtensions** for flow control and error handling.
- **Exceptions**: Reserved strictly for truly exceptional, unrecoverable situations.
- **Boundaries**: Never allow exceptions to leak across architectural boundaries.
