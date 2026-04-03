---
name: "📶 Skill: Wireshark Analysis"
tags: ["activation", "analysis", "antigravity", "benchmark", "c:", "execution", "frontend", "gemini", "<YOUR_USERNAME>", "output", "pipeline", "security", "signals", "signature", "skill", "steps", "sub", "task", "users", "wireshark"]
tier: 3
risk: "high"
estimated_tokens: 352
tools_needed: ["markdown", "terminal"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["web", "product"]
quality_score: 0.58
---
# 📶 Skill: Wireshark Analysis

> **PURPOSE:** Network packet analysis and traffic forensics (Wireshark, tshark).
> **CATEGORY:** Security
> **TIER:** 3+

---

## 🚦 ACTIVATION SIGNALS

- Keywords: `Wireshark`, `analyze pcap`, `intercept network traffic`, `tshark commands`.
- Goal: Systematically analyzing network traffic for sensitive data, unusual patterns, or attacks.

---

## 🛠️ SUB-STEPS (EXECUTION PIPELINE)

1. **Traffic Capture**: Use Wireshark UI or `tcpdump -w capture.pcap` to gather raw packets.
2. **Filter Application**: Use Display Filters (e.g., `ip.addr ==`, `http.request`, `tcp.flags.reset == 1`) to isolate traffic.
3. **Flow Reassembly**: Right-click -> "Follow TCP Stream" or "Follow HTTP Stream" to read application-level data.
4. **Credential Extraction**: Capture cleartext passwords (FTP, Telnet, HTTP) or extract session cookies.
5. **Attack Fingerprinting**: Identify Syn Floods, Nmap scans (TCP Xmas), or SMB exploitation patterns.
6. **Decryption**: Use SSL/TLS keylogs to decrypt HTTPS traffic for deep-packet inspection.

---

## 📝 OUTPUT SIGNATURE

- PCAP analysis reports.
- Extracted artifacts (Files, Passwords, Cookies).
- Visualization of network flow (IO Graphs).

---

## 🧪 BENCHMARK TASK

- **Input**: "How do I find cleartext POST data in this PCAP using Wireshark?"
- **Output**: Filter: `http.request.method == "POST"` -> Follow HTTP Stream -> View JSON/Form-data.
