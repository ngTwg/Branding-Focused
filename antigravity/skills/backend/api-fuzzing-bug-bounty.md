---
name: "🛡️ Skill: API Fuzzing for Bug Bounty"
tags: ["activation", "antigravity", "api", "backend", "benchmark", "bounty", "bug", "c:", "execution", "for", "fuzzing", "gemini", "<YOUR_USERNAME>", "output", "pipeline", "signals", "signature", "skill", "steps", "sub"]
tier: 3
risk: "high"
estimated_tokens: 319
tools_needed: ["markdown", "sql", "terminal"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["platform", "api"]
quality_score: 0.58
---
# 🛡️ Skill: API Fuzzing for Bug Bounty

> **PURPOSE:** Security testing for REST, SOAP, and GraphQL APIs.
> **CATEGORY:** Backend
> **TIER:** 3+

---

## 🚦 ACTIVATION SIGNALS

- Keywords: `test API security`, `fuzz APIs`, `find IDOR vulnerabilities`, `API penetration testing`.
- Goal: Identifying vulnerabilities like auth bypass, injection points, or unauthorized data access.

---

## 🛠️ SUB-STEPS (EXECUTION PIPELINE)

1. **Reconnaissance**: Identify API types, enumerate hidden endpoints (Swagger, kr scan).
2. **Authentication Testing**: Check rate limiting, mobile/web API parity, and bypasses.
3. **IDOR Testing**: Systematically manipulate IDs (numeric, array wrap, wildcard) to skip checks.
4. **Injection Testing**: Fuzz for SQL, Command, XXE, and SSRF in JSON/XML payloads.
5. **Method/Content-Type Testing**: Switch HTTP methods (GET -> POST) or content-types (JSON -> XML).
6. **GraphQL Analysis**: Execute introspection queries and fuzz queries/mutations.

---

## 📝 OUTPUT SIGNATURE

- Vulnerability report with evidence.
- Exploit/Fuzzing scripts.
- Mitigation recommendations.

---

## 🧪 BENCHMARK TASK

- **Input**: "Test our GraphQL API for IDOR and information disclosure."
- **Output**: Introspection query report -> Test results for user(id: "victim_id").
