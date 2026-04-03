---
name: "Section Definitions"
tags: ["antigravity", "c:", "comm", "communication", "dbos", "definitions", "frontend", "gemini", "<YOUR_USERNAME>", "lifecycle", "python", "queue", "references", "section", "sections", "specialized", "step", "users", "workflow"]
tier: 2
risk: "medium"
estimated_tokens: 353
tools_needed: ["markdown", "pytest"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["web", "product"]
quality_score: 0.64
---
# Section Definitions

This file defines the rule categories for DBOS Python best practices. Rules are automatically assigned to sections based on their filename prefix.

---

## 1. Lifecycle (lifecycle)
**Impact:** CRITICAL
**Description:** DBOS configuration, initialization, and launch patterns. Foundation for all DBOS applications.

## 2. Workflow (workflow)
**Impact:** CRITICAL
**Description:** Workflow creation, determinism requirements, background execution, and workflow IDs.

## 3. Step (step)
**Impact:** HIGH
**Description:** Step creation, retries, transactions, and when to use steps vs workflows.

## 4. Queue (queue)
**Impact:** HIGH
**Description:** Queue creation, concurrency limits, rate limiting, partitioning, and priority.

## 5. Communication (comm)
**Impact:** MEDIUM
**Description:** Workflow events, messages, and streaming for inter-workflow communication.

## 6. Pattern (pattern)
**Impact:** MEDIUM
**Description:** Common patterns including idempotency, scheduled workflows, debouncing, and classes.

## 7. Testing (test)
**Impact:** LOW-MEDIUM
**Description:** Testing DBOS applications with pytest, fixtures, and best practices.

## 8. Client (client)
**Impact:** MEDIUM
**Description:** DBOSClient for interacting with DBOS from external applications.

## 9. Advanced (advanced)
**Impact:** LOW
**Description:** Async workflows, workflow versioning, patching, and code upgrades.
