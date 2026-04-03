---
name: "async-python-patterns"
tags: ["antigravity", "async", "c:", "frontend", "gemini", "instructions", "<YOUR_USERNAME>", "not", "patterns", "python", "resources", "skill", "specialized", "this", "use", "users", "when"]
tier: 3
risk: "medium"
estimated_tokens: 429
tools_needed: ["markdown"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["web", "product"]
quality_score: 0.61
date_added: "2026-02-27"
description: "Comprehensive guidance for implementing asynchronous Python applications using asyncio, concurrent programming patterns, and async/await for building high-performance, non-blocking systems."
source: "community"
---
# Async Python Patterns

Comprehensive guidance for implementing asynchronous Python applications using asyncio, concurrent programming patterns, and async/await for building high-performance, non-blocking systems.

## Use this skill when

- Building async web APIs (FastAPI, aiohttp, Sanic)
- Implementing concurrent I/O operations (database, file, network)
- Creating web scrapers with concurrent requests
- Developing real-time applications (WebSocket servers, chat systems)
- Processing multiple independent tasks simultaneously
- Building microservices with async communication
- Optimizing I/O-bound workloads
- Implementing async background tasks and queues

## Do not use this skill when

- The workload is CPU-bound with minimal I/O.
- A simple synchronous script is sufficient.
- The runtime environment cannot support asyncio/event loop usage.

## Instructions

- Clarify workload characteristics (I/O vs CPU), targets, and runtime constraints.
- Pick concurrency patterns (tasks, gather, queues, pools) with cancellation rules.
- Add timeouts, backpressure, and structured error handling.
- Include testing and debugging guidance for async code paths.
- If detailed examples are required, open `resources/implementation-playbook.md`.

Refer to `resources/implementation-playbook.md` for detailed patterns and examples.

## Resources

- `resources/implementation-playbook.md` for detailed patterns and examples.
