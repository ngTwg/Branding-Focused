---
name: "🕵️‍♂️ Skill: Ethical Hacking Methodology"
tags: ["activation", "antigravity", "backend", "benchmark", "c:", "ethical", "execution", "gemini", "hacking", "<YOUR_USERNAME>", "methodology", "output", "pipeline", "security", "signals", "signature", "skill", "steps", "sub", "task"]
tier: 3
risk: "critical"
estimated_tokens: 405
tools_needed: ["markdown", "terminal"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["platform", "api"]
quality_score: 0.58
---
# 🕵️‍♂️ Skill: Ethical Hacking Methodology

> **PURPOSE:** Systematic multi-phase penetration testing (Recon -> Gaining Access -> Post-Exploitation).
> **CATEGORY:** Security
> **TIER:** 3+

---

## 🚦 ACTIVATION SIGNALS

- Keywords: `penetration test`, `vulnerability assessment`, `red team`, `reconnaissance`.
- Goal: Systematically testing target security from the attacker's perspective within ethical boundaries.

---

## 🛠️ SUB-STEPS (EXECUTION PIPELINE)

1. **Reconnaissance**: Passive (whois, google dorking) and Active (nmap, masscan, subfinder) information gathering.
2. **Vulnerability Analysis**: Use tools like Nessus, OpenVAS, or manual OSINT to find vulnerability windows.
3. **Exploitation (Gaining Access)**: Use Metasploit, custom shellcode, or manual bypasses to gain entry (privileged/non-privileged).
4. **Privilege Escalation**: Use local exploit suggestors (linpeas, winpeas) to move from User to Admin/Root.
5. **Post-Exploitation (Maintaining Access)**: Set up persistence (cronjobs, backdoors) and pivot to internal networks.
6. **Clearing Tracks**: Remove logs, temporary files, and artifacts (within legal boundaries of the engagement).
7. **Reporting**: Document: Vulnerability -> Evidence -> Business Impact -> Remediation.

---

## 📝 OUTPUT SIGNATURE

- Penetration Test Report (Vulnerability report).
- Exploitation/Payload scripts.
- Network diagram of internal movement (Pivoting).

---

## 🧪 BENCHMARK TASK

- **Input**: "Test our internal staging server for weak points."
- **Output**: Nmap scan (Open ports) -> Vulnerability found (smb-vuln-ms17-010) -> Mitigation (Patch + Firewall).
