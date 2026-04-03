---
name: "🔑 Skill: SSH Penetration Testing"
tags: ["activation", "antigravity", "backend", "benchmark", "c:", "execution", "gemini", "<YOUR_USERNAME>", "output", "penetration", "pipeline", "security", "signals", "signature", "skill", "ssh", "steps", "sub", "task", "testing"]
tier: 3
risk: "high"
estimated_tokens: 359
tools_needed: ["markdown", "terminal"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["platform", "api"]
quality_score: 0.58
---
# 🔑 Skill: SSH Penetration Testing

> **PURPOSE:** Detect and exploit vulnerabilities in SSH (Brute forcing, Key logic, Config flaws).
> **CATEGORY:** Security
> **TIER:** 3+

---

## 🚦 ACTIVATION SIGNALS

- Keywords: `SSH penetration testing`, `brute force SSH`, `crack SSH keys`, `find weak SSH config`.
- Goal: Systematically testing SSH server security (Port 22/2222).

---

## 🛠️ SUB-STEPS (EXECUTION PIPELINE)

1. **Information Extraction**: Identify version (Banner grabbing) and capabilities.
2. **Brute Force Testing**: Use `hydra -l user -P passlist.txt ssh://target` to test for weak passwords.
3. **Key Leakage Assessment**: Scan for leaked/standard private keys (`id_rsa`) in public repos or misconfigured shares.
4. **Configuration Audit**: Check for `PermitRootLogin yes`, password authentication (vs keys), and weak algorithms.
5. **Exploitation**: Use known version-specific exploits (e.g., `libssh` bypass, CVE-2024-3094, CVE-2018-15473).
6. **Persistence Strategy**: Add your public key to `~/.ssh/authorized_keys` for persistence.

---

## 📝 OUTPUT SIGNATURE

- SSH vulnerability findings (Hash cracking evidence).
- Proof of Concept (PoC) with successful login.
- SSH hardening recommendations (CIS Benchmarks).

---

## 🧪 BENCHMARK TASK

- **Input**: "Test our internal staging SSH for weak 'admin' password."
- **Output**: `hydra -l admin -P common_passwords.txt ssh://192.168.1.50` -> Login found (admin/password).
