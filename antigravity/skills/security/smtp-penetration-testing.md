---
name: "📧 Skill: SMTP Penetration Testing"
tags: ["activation", "antigravity", "backend", "benchmark", "c:", "execution", "gemini", "<YOUR_USERNAME>", "output", "penetration", "pipeline", "security", "signals", "signature", "skill", "smtp", "steps", "sub", "task", "testing"]
tier: 3
risk: "high"
estimated_tokens: 333
tools_needed: ["markdown", "terminal"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["platform", "api"]
quality_score: 0.58
---
# 📧 Skill: SMTP Penetration Testing

> **PURPOSE:** Detect and exploit vulnerabilities in email servers (Relay, Spoofing, User Enumeration).
> **CATEGORY:** Security
> **TIER:** 3+

---

## 🚦 ACTIVATION SIGNALS

- Keywords: `SMTP penetration testing`, `open relay`, `enumerate email users`, `spoofed email`.
- Goal: Systematically testing email server security (Port 25/587).

---

## 🛠️ SUB-STEPS (EXECUTION PIPELINE)

1. **Information Extraction**: Identify version (Banner grabbing) and capabilities (EHLO).
2. **User Enumeration**: Use `VRFY john`, `EXPN members`, or `RCPT TO: john@domain.com` to find valid users.
3. **Open Relay Testing**: Test if the server allows sending mail from/to external domains without auth.
4. **Spoofing Assessment**: Check SPF, DKIM, and DMARC records to see if external mail can be spoofed.
5. **Brute Forcing**: Use Hydra to test for weak SMTP-AUTH credentials.
6. **Automation**: Use Nmap scripts (`smtp-*`) to automate the enumeration and relay tests.

---

## 📝 OUTPUT SIGNATURE

- Vulnerability findings (PoC of open relay/spoofing).
- User enumeration reports.
- SPF/DKIM/DMARC recommendations.

---

## 🧪 BENCHMARK TASK

- **Input**: "Test our internal SMTP server for open relay."
- **Output**: telnet 25 -> RCPT TO: victim@external.com -> 250 OK (Relay Vulnerable) -> Evidence collected.
