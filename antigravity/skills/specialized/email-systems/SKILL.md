---
name: "email-systems"
tags: ["antigravity", "c:", "checklist", "critical", "deliverability", "email", "event", "frontend", "gemini", "<YOUR_USERNAME>", "patterns", "queue", "specialized", "systems", "template", "tracking", "transactional", "users", "versioning"]
tier: 2
risk: "medium"
estimated_tokens: 451
tools_needed: ["git", "markdown"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["web", "product"]
quality_score: 0.66
description: "Technical infrastructure, deliverability, and architecture for marketing and transactional email."
---
# Email Systems

You are an email systems engineer focused on deliverability, inbox placement, and infrastructure.

## Deliverability Checklist (Critical)

| Issue | Severity | Solution |
|-------|----------|----------|
| Missing SPF, DKIM, or DMARC | Critical | Set up required DNS records immediately. |
| Shared IP for Transactional | High | Use dedicated IP or segmented subdomains. |
| Bounce Handling | High | Process and suppress bounces automatically. |
| Hidden Unsubscribe | Critical | Enforce clear, one-click unsubscribe links. |
| No Plain Text Alternative | Medium | Always send multipart (HTML + Text). |
| IP Warming | High | Gradually increase volume for new IPs. |
| Non-Opt-In Sending | Critical | Enforce strict permission-based lists. |

## Patterns

### 1. Transactional Queue
Queue all transactional emails with retry logic and monitoring. Do not block main application threads.

### 2. Event Tracking
Track delivery, opens, clicks, bounces, and complaints. Feed this data back into user engagement scores.

### 3. Template Versioning
Version email templates for safe rollbacks and systematic A/B testing.

## Anti-Patterns

- **❌ HTML soup**: Using overly complex HTML that breaks in Outlook. Keep it simple.
- **❌ No plain text fallback**: Accessibility and spam signal issues.
- **❌ Huge image-only emails**: Images blocked by default; high spam risk.

## DNS Infrastructure Basics
- **SPF**: Specifies which mail servers are allowed to send mail on behalf of your domain.
- **DKIM**: Adds a digital signature to emails, ensuring they haven't been altered.
- **DMARC**: Instructions for receiving servers on what to do if SPF/DKIM fail.
