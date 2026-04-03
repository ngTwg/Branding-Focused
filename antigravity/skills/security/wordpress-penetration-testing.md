---
name: "🧊 Skill: WordPress Penetration Testing"
tags: ["activation", "antigravity", "backend", "benchmark", "c:", "execution", "gemini", "<YOUR_USERNAME>", "output", "penetration", "pipeline", "security", "signals", "signature", "skill", "steps", "sub", "task", "testing", "users"]
tier: 3
risk: "high"
estimated_tokens: 341
tools_needed: ["markdown", "sql", "terminal"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["platform", "api"]
quality_score: 0.58
---
# 🧊 Skill: WordPress Penetration Testing

> **PURPOSE:** Detect and exploit vulnerabilities in WordPress sites (Plugins, Themes, Core).
> **CATEGORY:** Security
> **TIER:** 2+

---

## 🚦 ACTIVATION SIGNALS

- Keywords: `WordPress pentest`, `wpscan usage`, `find vulnerable WP plugins`.
- Goal: Systematically testing WordPress security using wpscan and manual auditing.

---

## 🛠️ SUB-STEPS (EXECUTION PIPELINE)

1. **Information Extraction**: Identify version, installed plugins, and theme (Banner grabbing).
2. **Vulnerability Scanning (wpscan)**: Use `wpscan --url "url" --enumerate p,t,u` for automated scanning.
3. **API Token Integration**: Add WPVulnDB API token (`--api-token`) for up-to-date vulnerability info.
4. **User Enumeration**: Enumerate valid usernames using `wpscan -e u` or `/wp-json/wp/v2/users`.
5. **Brute Forcing**: Use `wpscan -U user -P passlist.txt` for brute-forcing `xmlrpc.php` or `wp-login.php`.
6. **Exploitation**: Use version-specific plugin/theme exploits (e.g., SQLi in older Contact Form 7).

---

## 📝 OUTPUT SIGNATURE

- wpscan vulnerability reports.
- Exploit PoCs (Requests/Responses).
- WordPress hardening recommendations (WAF, Patching).

---

## 🧪 BENCHMARK TASK

- **Input**: "How do I scan our blog for vulnerable plugins with wpscan?"
- **Output**: `wpscan --url "http://blog.com" --enumerate vp --api-token XXX`.
