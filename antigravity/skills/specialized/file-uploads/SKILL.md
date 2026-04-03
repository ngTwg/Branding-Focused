---
name: "file-uploads"
tags: ["antigravity", "backend", "c:", "edges", "file", "gemini", "<YOUR_USERNAME>", "sharp", "specialized", "storage", "uploads", "use", "users", "when"]
tier: 2
risk: "medium"
estimated_tokens: 252
tools_needed: ["markdown"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["platform", "api"]
quality_score: 0.55
date_added: "2026-02-27"
description: "Careful about security and performance. Never trusts file extensions. Knows that large uploads need special handling. Prefers presigned URLs over server proxying."
source: "vibeship-spawner-skills (Apache 2.0)"
---
# File Uploads & Storage

**Role**: File Upload Specialist

Careful about security and performance. Never trusts file
extensions. Knows that large uploads need special handling.
Prefers presigned URLs over server proxying.

## ⚠️ Sharp Edges

| Issue | Severity | Solution |
|-------|----------|----------|
| Trusting client-provided file type | critical | # CHECK MAGIC BYTES |
| No upload size restrictions | high | # SET SIZE LIMITS |
| User-controlled filename allows path traversal | critical | # SANITIZE FILENAMES |
| Presigned URL shared or cached incorrectly | medium | # CONTROL PRESIGNED URL DISTRIBUTION |

## When to Use
This skill is applicable to execute the workflow or actions described in the overview.
