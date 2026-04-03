---
name: "web-vulnerabilities"
tags: ["access", "antigravity", "application", "c:", "control", "core", "cross", "deep", "direct", "dive", "exploitation", "framework", "frontend", "gemini", "governance", "idor", "injection", "insecure", "<YOUR_USERNAME>", "object"]
tier: 2
risk: "high"
estimated_tokens: 436
tools_needed: ["markdown", "sql"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["web", "product"]
quality_score: 0.66
description: "Deep-dive into Web Application Security. Covers TOP 100 vulnerabilities, OWASP framework, and exploitation methodology."
---
# Web Application Vulnerabilities (v6.5.0-SLIM)

Reference for identifying, testing, and mitigating web-based security flaws.

## 1. Governance & OWASP Framework
- **OWASP Top 10:** Injection 💉, Broken Auth 🔑, Exposure 💎, XML 📦, Access Control ⚡, Misconfig 🛠️, XSS 🛡️, Deserialization 🧬, Vulnerable Deps 💉, Logging 📋.
- **Severity Impact:** Confidentiality (C), Integrity (I), Availability (A).

## 2. Core Exploitation (Deep Dive)

### SQL Injection (Injection)
- **Classic:** `' OR 1=1 --`.
- **Blind/Time-based:** `'; IF (1=1) WAITFOR DELAY '0:0:5'--`.
- **Out-of-Band (OOB):** Triggering DNS/HTTP requests to external servers.

### Cross-Site Scripting (XSS)
- **Stored:** Persistent in database/page.
- **Reflected:** Payload in URL/params.
- **DOM-based:** Client-side script execution.
- **Evasion:** Polyglot payloads, encoding (hex, base64).

### Insecure Direct Object References (IDOR/Access Control)
- Accessing `userId=2` when authorized as `userId=1`.
- Mass Assignment (overwriting internal object properties via JSON).

### Authentication & Sessions
- JWT Header Injection / None algorithm.
- Weak session IDs (entropy) and session fixation.

## 3. Advanced API Vulnerabilities
- BOLA (Broken Object Level Authorization).
- NoSQL Injection ($gt, $ne).
- SSRF (Server-Side Request Forgery) against cloud metadata (169.254.169.254).

## 4. Operational Checklist (Burp/ZAP)
1. Sitemap & Discovery.
2. Parameter Fuzzing.
3. Auth/Session Test.
4. Logic/Workflow Check.
5. Infrastructure Audit.

## Related Skills
`recon-scanning`, `linux-privesc`, `windows-privesc`.
