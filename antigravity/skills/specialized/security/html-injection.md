---
name: "html-injection-testing"
tags: ["advanced", "antigravity", "bypass", "c:", "core", "evasion", "frontend", "gemini", "governance", "html", "injection", "<YOUR_USERNAME>", "payloads", "principles", "remediation", "security", "slim", "specialized", "techniques", "testing"]
tier: 3
risk: "high"
estimated_tokens: 638
tools_needed: ["markdown"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["web", "product"]
quality_score: 0.67
description: "Strategy and payloads for identifying and exploiting HTML Injection vulnerabilities."
---
# HTML Injection Testing (v6.5.0-SLIM)

Methodology for identifying and testing content injection vulnerabilities that allow for page defacement and phishing.

## 1. Governance & Core Principles
- **Injection vs XSS:** HTML injection renders tags; XSS executes JavaScript. HTML injection is often a stepping stone to XSS.
- **Attack Surfaces:** Search bars, comment sections, profiles, and URL parameters.

## 2. Testing Payloads
- **Basic:** `<h1>Test</h1>`, `<b>Bold</b>`.
- **Structural:** `<div style="background:red;padding:10px">Injected</div>`.
- **Phishing Forms:** Injected `<form>` overlays to steal credentials.
- **Defacement:** Full-page overlays using `<style>` or high-z-index `<div>` blocks.

## 3. Advanced Techniques
- **CSS Injection:** Using `background: url()` with tracked parameters.
- **Meta Tag Injection:** Meta refresh for unauthorized redirects.
- **Iframe Injection:** Embedding malicious external content.

## 4. Bypass & Evasion
- **URL Encoding:** `%3Ch1%3E` for `<h1>`.
- **Case Jumbling:** `<ScRiPt>` instead of `<script>`.
- **Null Bytes:** `<h1%00>` to terminate string filters.

## 5. Remediation
- **Output Escaping:** Always use `htmlspecialchars()` or equivalent context-aware escaping.
- **Sanitization:** Use libraries like `DOMPurify` for client-side HTML rendering.

## Related Skills
`web-vulnerabilities`, `recon-scanning`.
---
name: langfuse-observability
description: LLM observability, tracing, and prompt management using Langfuse.
---

# Langfuse Observability (v6.5.0-SLIM)

Framework for monitoring, tracing, and evaluating LLM applications in production.

## 1. Core Capabilities
- **LLM Tracing:** Monitor model inputs, outputs, latency, and cost.
- **Prompt Management:** Version and manage prompts centrally.
- **Evaluation:** Score generations based on quality, safety, or user feedback.

## 2. Integration Patterns
- **OpenAI:** Use `langfuse.openai` wrapper for automatic tracing.
- **LangChain:** Use `CallbackHandler` for seamless trace capture.
- **SDKs:** Support for Python and TypeScript/JavaScript.

## 3. Best Practices
- **Flush in Serverless:** Always call `langfuse.flush()` before function exit.
- **User & Session IDs:** Always attach `user_id` and `session_id` to traces for debugging.
- **Granular Scoring:** Implement A/B testing for prompt versions based on performance metrics.

## Related Skills
`prompt-engineering`, `behavioral-modes`.
