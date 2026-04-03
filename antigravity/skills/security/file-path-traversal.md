---
name: "📁 Skill: File Path Traversal"
tags: ["activation", "antigravity", "benchmark", "c:", "execution", "file", "frontend", "gemini", "<YOUR_USERNAME>", "output", "path", "pipeline", "security", "signals", "signature", "skill", "steps", "sub", "task", "traversal"]
tier: 3
risk: "high"
estimated_tokens: 353
tools_needed: ["markdown", "terminal"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["web", "product"]
quality_score: 0.58
---
# 📁 Skill: File Path Traversal

> **PURPOSE:** Detect and exploit directory traversal (../) in file-handling applications.
> **CATEGORY:** Security
> **TIER:** 2+

---

## 🚦 ACTIVATION SIGNALS

- Keywords: `file path traversal`, `../ traversal`, `find arbitrary file read`.
- Goal: Systematically testing for sensitive file exposure (config, passwd, logs).

---

## 🛠️ SUB-STEPS (EXECUTION PIPELINE)

1. **Endpoint Identification**: Find functions that read files (e.g., `?file=`, `image.php?src=`, `/download?filename=`).
2. **Standard Payload Testing**: Use `../../../../etc/passwd` (Linux) or `../../../../windows/win.ini` (Windows).
3. **Encoding Bypass**: Use URL encoding (`%2e%2e%2f`), Double URL encoding (`%252e%252e%252f`), or Null Bytes (`%00`).
4. **Absolute Path Testing**: Use `/etc/passwd` or `C:\Windows\win.ini` directly if the app doesn't prepend a base directory.
5. **Automation**: Use Burp Intruder with custom wordlists to brute force directories.
6. **Remediation**: Use `path.basename()` (Node), `realpath()` (PHP), or allow-lists to fix the vulnerability.

---

## 📝 OUTPUT SIGNATURE

- Vulnerability evidence (File content).
- Payload evidence (Interpreted URL).
- Patch recommendations.

---

## 🧪 BENCHMARK TASK

- **Input**: "Test our image download feature for directory traversal."
- **Output**: Payload (../../config.json) -> Evidence (DB credentials leaked) -> Filter-based patch.
