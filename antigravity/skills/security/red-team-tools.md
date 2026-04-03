---
name: "🛠️ Skill: Red Team Tools"
tags: ["activation", "antigravity", "benchmark", "c:", "execution", "frontend", "gemini", "<YOUR_USERNAME>", "output", "pipeline", "red", "security", "signals", "signature", "skill", "steps", "sub", "task", "team", "tools"]
tier: 3
risk: "medium"
estimated_tokens: 297
tools_needed: ["markdown", "terminal"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["web", "product"]
quality_score: 0.58
---
# 🛠️ Skill: Red Team Tools

> **PURPOSE:** Essential Red Team CLI/Tools (Cobalt Strike, BloodHound, Responder).
> **CATEGORY:** Security
> **TIER:** 2+

---

## 🚦 ACTIVATION SIGNALS

- Keywords: `Cobalt Strike usage`, `BloodHound collectors`, `Responder commands`, `Empire usage`.
- Goal: Quick access to complex Red Team tool syntax (LMNR, Kerberos, AD).

---

## 🛠️ SUB-STEPS (EXECUTION PIPELINE)

1. **Information Extraction**: Identify target (e.g., AD environment, C2 server).
2. **Tool Selection**: Use BloodHound for graph analysis, Responder for LLMNR spoofing, or Cobalt Strike for Beacons.
3. **Execution Planning**: Setup C2 profile, configure listeners (HTTP/S, DNS), and deploy stagers.
4. **Stealth Pass**: Use Malleable C2 profiles to hide beacon traffic in normal web requests.
5. **Collection Strategy**: SharpHound (AD collection), Mimikatz (Credential dumping), or PowerView (AD Enumeration).

---

## 📝 OUTPUT SIGNATURE

- Copy-pasteable Red Team tool commands.
- C2 profile artifacts.
- AD graph analysis reports.

---

## 🧪 BENCHMARK TASK

- **Input**: "How do I start LLMNR/NBT-NS poisoning with Responder on our network?"
- **Output**: `sudo responder -I eth0 -rdw`.
