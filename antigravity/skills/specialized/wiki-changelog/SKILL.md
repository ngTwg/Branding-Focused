---
name: "wiki-changelog"
tags: ["antigravity", "backend", "c:", "changelog", "constraints", "gemini", "<YOUR_USERNAME>", "procedure", "specialized", "use", "users", "when", "wiki"]
tier: 2
risk: "medium"
estimated_tokens: 286
tools_needed: ["git", "markdown"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["platform", "api"]
quality_score: 0.60
date_added: "2026-02-27"
description: "Generate structured changelogs from git history. Use when user asks \\\"what changed recently\\\", \\\"generate a changelog\\\", \\\"summarize commits\\\" or user wants to understand recent development activity."
source: "community"
---
# Wiki Changelog

Generate structured changelogs from git history.

## When to Use
- User asks "what changed recently", "generate a changelog", "summarize commits"
- User wants to understand recent development activity

## Procedure

1. Examine git log (commits, dates, authors, messages)
2. Group by time period: daily (last 7 days), weekly (older)
3. Classify each commit: Features (🆕), Fixes (🐛), Refactoring (🔄), Docs (📝), Config (🔧), Dependencies (📦), Breaking (⚠️)
4. Generate concise user-facing descriptions using project terminology

## Constraints

- Focus on user-facing changes
- Merge related commits into coherent descriptions
- Use project terminology from README
- Highlight breaking changes prominently with migration notes

## When to Use
This skill is applicable to execute the workflow or actions described in the overview.
