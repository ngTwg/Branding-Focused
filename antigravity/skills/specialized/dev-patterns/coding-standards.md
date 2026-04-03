---
name: "coding-standards"
tags: ["antigravity", "best", "c:", "coding", "conventions", "core", "critical", "dev", "error", "frontend", "gemini", "handling", "immutability", "javascript", "<YOUR_USERNAME>", "naming", "patterns", "practices", "principles", "slim"]
tier: 2
risk: "medium"
estimated_tokens: 463
tools_needed: ["markdown"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["web", "product"]
quality_score: 0.66
description: "Universal coding standards, best practices, and patterns for TypeScript, JavaScript, React, and Node.js."
---
# Coding Standards & Best Practices (v6.5.0-SLIM)

Universal coding standards applicable across all projects.

## Core Principles
1. **Readability First:** Code is read more than written. Clear variable and function names.
2. **KISS (Keep It Simple, Stupid):** Simplest solution that works. Avoid over-engineering.
3. **DRY (Don't Repeat Yourself):** Extract common logic. No copy-paste.
4. **YAGNI (You Aren't Gonna Need It):** Don't build features until they are needed.

## TypeScript/JavaScript Standards

### 1. Immutability (CRITICAL)
**ALWAYS** use spread operators: `{ ...user, name: 'New' }`.
**NEVER** mutate directly: `user.name = 'New'`.

### 2. Naming Conventions
- **Variables:** camelCase (`marketSearchQuery`).
- **Functions:** Verb-noun camelCase (`fetchMarketData`).
- **Interfaces/Types:** PascalCase (`MarketModel`).
- **Components:** PascalCase (`MarketCard.tsx`).

### 3. Error Handling
**ALWAYS** wrap external calls (fetch, DB, API) in `try/catch`. Throw descriptive errors or return structured responses.

### 4. Async/Await
**Parallelize:** Use `Promise.all()` for independent calls.
**NEVER** use sequential await for independent tasks: `await fetch1(); await fetch2();`.

### 5. Type Safety
**NO `any`:** Define strict interfaces for models, inputs, and outputs. Use Union types for statuses: `'active' | 'closed'`.

## Documentation
- **Explain WHY (Intention):** Not what the code is doing (self-documenting).
- **Public APIs:** Use JSDoc for functions to enable IDE hover support.

## Code Smells to Avoid
- **Long Functions:** Keep functions < 50 lines.
- **Deep Nesting:** Use early returns (Guard Clauses).
- **Magic Numbers:** Use named constants: `MAX_RETRIES = 3`.
