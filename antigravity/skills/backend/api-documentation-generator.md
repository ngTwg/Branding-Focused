---
name: "📖 Skill: API Documentation Generator"
tags: ["activation", "antigravity", "api", "backend", "benchmark", "c:", "documentation", "execution", "frontend", "gemini", "generator", "<YOUR_USERNAME>", "output", "pipeline", "signals", "signature", "skill", "steps", "sub", "task"]
tier: 3
risk: "medium"
estimated_tokens: 310
tools_needed: ["markdown", "terminal"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["web", "product"]
quality_score: 0.57
---
# 📖 Skill: API Documentation Generator

> **PURPOSE:** Create comprehensive, developer-friendly API documentation from your codebase.
> **CATEGORY:** Backend
> **TIER:** 1+

---

## 🚦 ACTIVATION SIGNALS

- Keywords: `document API`, `API reference`, `OpenAPI`, `Swagger`.
- Goal: Systematizing API documentation for internal or external developers.

---

## 🛠️ SUB-STEPS (EXECUTION PIPELINE)

1. **Context Extraction**: Examine codebase to identify endpoints, methods, headers, and schemas.
2. **Endpoint Specification**: Create detailed entries with descriptions, parameters, and success/error responses.
3. **Template Application**: Structure the documentation into sections (Authentication, Quick Start, Endpoints, etc.).
4. **Interactive Generation**: Create Postman collections or OpenAPI/Swagger specifications.
5. **Quality Check**: Ensure all examples (cURL, JS, Python) are working and accurate.

---

## 📝 OUTPUT SIGNATURE

- API reference artifacts (Markdown, HTML, JSON).
- Postman collections.
- OpenAPI/Swagger specifications.

---

## 🧪 BENCHMARK TASK

- **Input**: "Document our new user authentication and profile API."
- **Output**: Markdown reference with: GET /users/me -> Request/Response example -> 401 Unauthorized case.
