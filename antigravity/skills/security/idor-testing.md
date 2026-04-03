---
name: "🆔 Skill: IDOR Testing"
tags: ["activation", "antigravity", "benchmark", "c:", "execution", "frontend", "gemini", "idor", "<YOUR_USERNAME>", "output", "pipeline", "security", "signals", "signature", "skill", "steps", "sub", "task", "testing", "users"]
tier: 3
risk: "high"
estimated_tokens: 381
tools_needed: ["markdown", "terminal"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["web", "product"]
quality_score: 0.59
---
# 🆔 Skill: IDOR Testing

> **PURPOSE:** Detect and exploit Insecure Direct Object Reference (IDOR) vulnerabilities.
> **CATEGORY:** Security
> **TIER:** 2+

---

## 🚦 ACTIVATION SIGNALS

- Keywords: `IDOR`, `access other users' data`, `BOLA`, `broken object level authorization`.
- Goal: Systematically testing for unauthorized access to non-owned objects (GET /api/user/123 -> 200 of someone else).

---

## 🛠️ SUB-STEPS (EXECUTION PIPELINE)

1. **Endpoint Identification**: Find endpoints using numeric, UUID, or sensitive IDs (e.g., `?id=102`, `/api/order/500`, `/users/me`).
2. **Horizontal IDOR Testing**: Change your ID to another user's (e.g., Change 102 to 101) to see if you can access their data.
3. **Vertical IDOR Testing**: Change your role or permissions (e.g., add `admin=true` to query/JSON body).
4. **ID Manipulation Techniques**: Use UUID v4 brute forcing, Array wrapping (`id=[101]`), or Parameter pollution (`?id=102&id=101`).
5. **Method Manipulation**: Switch HTTP methods (GET -> POST, PUT -> DELETE) on IDs.
6. **Remediation**: Use strong authorization at the data-access layer (e.g., `where: { id: id, userId: currentUser.id }`).

---

## 📝 OUTPUT SIGNATURE

- Vulnerability findings (IDOR evidence).
- Proof of Concept (PoC) with two separate user tokens.
- Secure design patterns for authorization.

---

## 🧪 BENCHMARK TASK

- **Input**: "Test our /orders/{id} endpoint for BOLA/IDOR."
- **Output**: User A session -> GET /orders/501 (User B order) -> 200 OK (Unauthorized) -> Evidence collected.
