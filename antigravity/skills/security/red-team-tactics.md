---
name: "🚩 Skill: Red Team Tactics"
tags: ["activation", "antigravity", "benchmark", "c:", "execution", "gemini", "<YOUR_USERNAME>", "output", "pipeline", "red", "security", "signals", "signature", "skill", "steps", "sub", "tactics", "task", "team", "users"]
tier: 3
risk: "critical"
estimated_tokens: 357
tools_needed: ["markdown", "terminal"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["engineering", "productivity"]
quality_score: 0.58
---
# 🚩 Skill: Red Team Tactics

> **PURPOSE:** Realistic adversary emulation, stealth, and persistence (MITRE ATT&CK).
> **CATEGORY:** Security
> **TIER:** 4+

---

## 🚦 ACTIVATION SIGNALS

- Keywords: `red teaming`, `APT emulation`, `stealth persistence`.
- Goal: Mimicking high-tier attackers to test organizational resilience.

---

## 🛠️ SUB-STEPS (EXECUTION PIPELINE)

1. **Information Extraction**: Map the environment (AD, Cloud, Network) to the MITRE ATT&CK framework.
2. **Initial Access Strategy**: Phishing, Supply chain, Exploiting public apps.
3. **Execution & Stealth**: Use beaconing (Cobalt Strike, Sliver), In-memory execution (PowerShell Reflective Loading).
4. **Persistence Strategy**: Registry keys, scheduled tasks, WMI events, or hidden backdoors.
5. **Privilege Escalation & Lateral Movement**: Mimikatz (Pass-the-hash), Kerberoasting, and BloodHound analysis.
6. **Data Exfiltration**: Encrypted channels (DNS tunneling, ICMP, HTTPS) to hide patterns.
7. **Simulation Assessment**: Conduct "White" (notified) or "Black" (unnotified) tests to check SOC response.

---

## 📝 OUTPUT SIGNATURE

- Emulated APT reports (MITRE ATT&CK mapping).
- C2 (Command & Control) configuration details.
- Stealth/Persistence artifacts.

---

## 🧪 BENCHMARK TASK

- **Input**: "Test our Active Directory for lateral movement using BloodHound."
- **Output**: Path analysis (User -> Group -> Domain Admin) -> Kerberoasting PoC.
