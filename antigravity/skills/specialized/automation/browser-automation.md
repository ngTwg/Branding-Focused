---
name: "browser-automation"
tags: ["antigravity", "auto", "automation", "browser", "c:", "core", "facing", "framework", "frontend", "gemini", "isolation", "<YOUR_USERNAME>", "locator", "pattern", "patterns", "playwright", "puppeteer", "selection", "slim", "specialized"]
tier: 2
risk: "medium"
estimated_tokens: 468
tools_needed: ["markdown", "playwright"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["web", "product"]
quality_score: 0.69
description: "Browser automation powers web testing, scraping, and AI agent interactions. The difference between a flaky script and a reliable system comes down to understanding selectors, waiting strategies, and anti-detection patterns. Key insight: Playwright is the 2025 standard."
---
# Browser Automation - Playwright & Puppeteer (v6.5.0-SLIM)

Expert browser automation for web testing, scraping, and agentic interactions.

## Framework Selection
- **Playwright:** Recommended for most users. Built-in auto-waiting, multi-browser support, and traces.
- **Puppeteer:** Recommended for stealth-heavy scraping using `puppeteer-extra-stealth`.

## Core Patterns

### 1. User-Facing Locator Pattern
Select elements as users see them (text, roles, labels). Avoid fragile CSS/XPath selectors.
```javascript
await page.getByRole('button', { name: 'Submit' }).click();
```

### 2. Auto-Wait Pattern
Eliminate `waitForTimeout`. Let the framework handle availability, visibility, and clickability automatically.
- **NEVER** use: `await page.waitForTimeout(3000);`
- **ALWAYS** use: `await page.waitForSelector('.success-message');`

### 3. Test Isolation
Each test context must be isolated with a clean session, cookies, and local storage.

## Anti-Patterns (Sharp Edges)
- **❌ CSS/XPath First:** They break when the UI changes slightly.
- **❌ Arbitrary Timeouts:** Leads to flaky tests and slow execution.
- **❌ Single Browser Context:** State pollution between tests.

## Common Issues & Solutions
| Issue | Solution |
|-------|----------|
| Captcha/Detection | Use `playwright-extra` + stealth plugin. |
| Flaky Dropdowns | Use `.selectOption()` over manual clicks. |
| Popups | Wait for the popup event *before* triggering it. |

## Related Skills
Works with: `agent-tool-builder`, `workflow-automation`, `computer-use-agents`, `test-architect`.
