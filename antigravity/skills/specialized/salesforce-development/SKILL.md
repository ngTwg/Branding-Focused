---
name: "salesforce-development"
tags: ["anti", "antigravity", "apex", "async", "bulkified", "c:", "component", "development", "for", "frontend", "gemini", "handler", "<YOUR_USERNAME>", "lightning", "pattern", "patterns", "processing", "queueable", "salesforce", "service"]
tier: 2
risk: "medium"
estimated_tokens: 382
tools_needed: ["markdown"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["web", "product"]
quality_score: 0.67
date_added: "2026-02-27"
description: "Use @wire decorator for reactive data binding with Lightning Data Service or Apex methods. @wire fits LWC's reactive architecture and enables Salesforce performance optimizations."
source: "vibeship-spawner-skills (Apache 2.0)"
---
# Salesforce Development

## Patterns

### Lightning Web Component with Wire Service

Use @wire decorator for reactive data binding with Lightning Data Service
or Apex methods. @wire fits LWC's reactive architecture and enables
Salesforce performance optimizations.

### Bulkified Apex Trigger with Handler Pattern

Apex triggers must be bulkified to handle 200+ records per transaction.
Use handler pattern for separation of concerns, testability, and
recursion prevention.

### Queueable Apex for Async Processing

Use Queueable Apex for async processing with support for non-primitive
types, monitoring via AsyncApexJob, and job chaining. Limit: 50 jobs
per transaction, 1 child job when chaining.

## Anti-Patterns

### ❌ SOQL Inside Loops

### ❌ DML Inside Loops

### ❌ Hardcoding IDs

## ⚠️ Sharp Edges

| Issue | Severity | Solution |
|-------|----------|----------|
| Issue | critical | See docs |
| Issue | high | See docs |
| Issue | medium | See docs |
| Issue | high | See docs |
| Issue | critical | See docs |
| Issue | high | See docs |
| Issue | high | See docs |
| Issue | critical | See docs |

## When to Use
This skill is applicable to execute the workflow or actions described in the overview.
