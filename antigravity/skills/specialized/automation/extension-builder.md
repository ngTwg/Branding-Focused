---
name: "browser-extension-builder"
tags: ["antigravity", "architecture", "automation", "browser", "builder", "c:", "capabilities", "communication", "core", "extension", "frontend", "gemini", "<YOUR_USERNAME>", "manifest", "mv3", "pattern", "policies", "project", "publishing", "slim"]
tier: 2
risk: "medium"
estimated_tokens: 463
tools_needed: ["markdown"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["web", "product"]
quality_score: 0.67
description: "Expert in building browser extensions - Chrome, Firefox, and cross-browser. Covers architecture, manifest v3, content scripts, popup UIs, and publishing."
---
# Browser Extension Builder (v6.5.0-SLIM)

Architect and build browser extensions that solve problems and give users superpowers.

## Architecture & Manifest V3 (MV3)

Modern extensions use background service workers over persistent background pages.

### MV3 Project Structure
```text
extension/
├── manifest.json      # Extension config (Manifest v3)
├── popup/
│   ├── popup.html     # Popup UI
│   ├── popup.css
│   └── popup.js
├── content/
│   └── content.js     # Runs on web pages (DOM access)
├── background/
│   └── service-worker.js  # Persistent background logic
└── icons/           # 16, 48, 128px
```

### Communication Pattern
Message passing is the primary bridge between context isolated segments.
- **Popup ←→ Background (Service Worker) ←→ Content Script**
- **Storage:** Use `chrome.storage.local` to sync data across components.

## Core Capabilities
- **Content Scripts:** Inject logic into existing web pages to modify the DOM.
- **Background Workers:** Handle events, network requests, and message routing.
- **Permissions:** Principle of Least Privilege: only request what's needed for the feature.
- **Options Management:** Provide an options page for user configuration.

## Publishing & Store Policies
- **Security:** CSP (Content Security Policy) enforcement. Avoid `eval()`.
- **Review Readiness:** Provide clear justification for each permission during store submission.
- **Monetization:** Stripe integration within extension windows (Stripe Checkout).
- **Cross-Browser:** Use `webextension-poly-fill` for Firefox/Safari compatibility.

## Related Skills
`frontend-design`, `javascript-core`, `web-security`.
