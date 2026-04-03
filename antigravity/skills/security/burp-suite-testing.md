---
name: "🕵️ Skill: Burp Suite Testing"
tags: ["activation", "antigravity", "benchmark", "burp", "c:", "execution", "frontend", "gemini", "<YOUR_USERNAME>", "output", "pipeline", "security", "signals", "signature", "skill", "steps", "sub", "suite", "task", "testing"]
tier: 3
risk: "high"
estimated_tokens: 362
tools_needed: ["markdown", "terminal"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["web", "product"]
quality_score: 0.58
---
# 🕵️ Skill: Burp Suite Testing

> **PURPOSE:** Web application penetration testing with Burp Suite (Proxy, Repeater, Intruder, Scanner).
> **CATEGORY:** Security
> **TIER:** 3+

---

## 🚦 ACTIVATION SIGNALS

- Keywords: `Burp Suite`, `web application penetration testing`, `intercept traffic`.
- Goal: Systematically testing web applications for vulnerabilities (OWASP Top 10).

---

## 🛠️ SUB-STEPS (EXECUTION PIPELINE)

1. **Proxy Analysis**: Intercept and analyze HTTP requests/responses for sensitive data or suspicious parameters.
2. **Repeater Manipulation**: Manually manipulate request headers and payloads to test for auth bypass and logic flaws.
3. **Intruder Fuzzing**: Use Intruder for automated fuzzing (brute forcing, parameter enumeration, payload testing).
4. **Scanner & Audit**: Utilize Burp Scanner for automated vulnerability detection and manual audit.
5. **Collaborator Integration**: Use Burp Collaborator to detect out-of-band (OOB) vulnerabilities (SSRF, RCE).
6. **Report Synthesis**: Consolidate findings with evidence (requests/responses) and mitigation steps.

---

## 📝 OUTPUT SIGNATURE

- Vulnerability findings (Markdown/HTML).
- Evidence captured in Burp (Requests/Responses).
- Exploit/Fuzzing payloads.

---

## 🧪 BENCHMARK TASK

- **Input**: "Test our login page for username enumeration using Burp Intruder."
- **Output**: Intruder results for wordlist -> Different response code/length for valid/invalid users.
