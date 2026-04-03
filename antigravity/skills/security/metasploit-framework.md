---
name: "🏴 Skill: Metasploit Framework"
tags: ["activation", "antigravity", "benchmark", "c:", "execution", "framework", "frontend", "gemini", "<YOUR_USERNAME>", "metasploit", "output", "pipeline", "security", "signals", "signature", "skill", "steps", "sub", "task", "users"]
tier: 3
risk: "high"
estimated_tokens: 358
tools_needed: ["markdown", "terminal"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["web", "product"]
quality_score: 0.58
---
# 🏴 Skill: Metasploit Framework

> **PURPOSE:** Professional vulnerability exploitation and post-exploitation (MSF, msfvenom).
> **CATEGORY:** Security
> **TIER:** 3+

---

## 🚦 ACTIVATION SIGNALS

- Keywords: `Metasploit`, `msfconsole`, `exploit`, `shellcode`, `msfvenom`.
- Goal: Using the world's most popular exploitation framework to gain system access and pivot.

---

## 🛠️ SUB-STEPS (EXECUTION PIPELINE)

1. **Reconnaissance Integration**: Import nmap (db_nmap) scans into Metasploit's database.
2. **Module Selection**: Choose correct `exploit/`, `auxiliary/`, or `post/` module based on vulnerability fingerprints.
3. **Payload Configuration (LHOST/LPORT)**: Set up reverse shell payloads (meterpreter, generic, stageless).
4. **Encoding (msfvenom)**: Use encoders (shikata_ga_nai) or custom stagers to bypass AV/EDR.
5. **Session Management (Meterpreter)**: Elevate privileges (getsystem), dump hashes (hashdump), and pivot (autoroute).
6. **Automation**: Use resource files (`.rc`) for repeatable, automated penetration testing tasks.

---

## 📝 OUTPUT SIGNATURE

- Metasploit session reports.
- msfvenom-generated payloads.
- Post-exploitation artifacts (Hashes, pivoting info).

---

## 🧪 BENCHMARK TASK

- **Input**: "Test our internal SMB server for EternalBlue (ms17-010) using Metasploit."
- **Output**: use auxiliary/scanner/smb/smb_ms17_010 (Vulnerable) -> use exploit/windows/smb/ms17_010_eternalbinary (Shell).
