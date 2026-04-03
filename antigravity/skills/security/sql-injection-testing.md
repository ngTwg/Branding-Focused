---
name: "💉 Skill: SQL Injection Testing"
tags: ["activation", "antigravity", "backend", "benchmark", "c:", "execution", "gemini", "injection", "<YOUR_USERNAME>", "output", "pipeline", "security", "signals", "signature", "skill", "sql", "steps", "sub", "task", "testing"]
tier: 3
risk: "high"
estimated_tokens: 325
tools_needed: ["markdown", "sql", "terminal"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["platform", "api"]
quality_score: 0.58
---
# 💉 Skill: SQL Injection Testing

> **PURPOSE:** Detect and exploit SQLi (Classic, Blind, Time-based, OOB).
> **CATEGORY:** Security
> **TIER:** 3+

---

## 🚦 ACTIVATION SIGNALS

- Keywords: `SQLi testing`, `blind SQLi`, `find SQL injection`, `dump database`.
- Goal: Systematically testing for database exposure via input parameters.

---

## 🛠️ SUB-STEPS (EXECUTION PIPELINE)

1. **Endpoint Identification**: Find endpoints with numeric or sensitive parameters (`?id=`, `/user/`, `search=`).
2. **Standard Error-Based Testing**: Use `' OR '1'='1` or `'` to check for DB errors.
3. **Boolean-Based Blind Testing**: Use `' AND 1=1` vs `' AND 1=2` to observe response differences.
4. **Time-Based Blind Testing**: Use `'; WAITFOR DELAY '0:0:5'--` (SQL Server) or `' AND sleep(5)` (MySQL).
5. **Automation (sqlmap)**: Use `sqlmap -u "url" --dbs --dump` for professional database dumping.
6. **Remediation**: Use parameterized queries, ORMs (Prisma, TypeORM), or prepared statements.

---

## 📝 OUTPUT SIGNATURE

- SQLi evidence (DB data).
- Proof of Concept (PoC) with time-latency or boolean-state change.
- Patch recommendations.

---

## 🧪 BENCHMARK TASK

- **Input**: "Test our search bar for SQL injection."
- **Output**: Payload (`' OR '1'='1`) -> Results (All rows leaked) -> Evidence collected.
