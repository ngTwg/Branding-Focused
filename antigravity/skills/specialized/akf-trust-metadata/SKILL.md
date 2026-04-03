---
name: "AKF — The AI Native File Format"
tags: ["after", "akf", "antigravity", "auditing", "backend", "before", "c:", "classification", "compliance", "creating", "existing", "file", "files", "format", "gemini", "<YOUR_USERNAME>", "metadata", "modifying", "native", "specialized"]
tier: 2
risk: "medium"
estimated_tokens: 414
tools_needed: ["git", "markdown", "terminal"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["platform", "api"]
quality_score: 0.77
---
---
name: akf-trust-metadata
description: "The AI native file format. EXIF for AI — stamps every file with trust scores, source provenance, and compliance metadata. Embeds into 20+ formats (DOCX, PDF, images, code). EU AI Act, SOX, HIPAA auditing."
risk: safe
source: community
date_added: "2026-03-27"
author: HMAKT99
tags:
- trust
- metadata
- provenance
- compliance
- file-format
- ai-native
---

# AKF — The AI Native File Format

Every photo has EXIF. Every song has ID3. AKF is the native metadata format for AI-generated content.

## When to Use

Use this skill when you need to stamp, inspect, or audit provenance and trust metadata on AI-generated or AI-modified files for compliance, review, or handoff workflows.

## After creating or modifying files

```bash
akf stamp <file> --agent <agent-name> --evidence "<what you did>"
```

Evidence examples:
- "generated from user prompt"
- "refactored existing code"
- "tests pass"
- "docs reviewed"

## Before modifying existing files

```bash
akf read <file>          # Check existing trust metadata
akf inspect <file>       # See detailed trust scores
```

## Compliance auditing

```bash
akf audit <file> --regulation eu_ai_act    # EU AI Act Article 50
akf audit <file> --regulation hipaa         # HIPAA
akf audit <file> --regulation sox           # SOX
akf audit <file> --regulation nist_ai       # NIST AI RMF
```

## Classification

- `--label confidential` for finance/secret/internal paths
- `--label public` for README, docs, examples
- Default: `internal`

## Install

```bash
pip install akf
```

## Links

- https://akf.dev
- https://github.com/HMAKT99/AKF
- npm: `npm install akf-format`
