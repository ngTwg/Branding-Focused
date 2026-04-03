---
name: "wiki-qa"
tags: ["antigravity", "c:", "format", "gemini", "<YOUR_USERNAME>", "procedure", "qa", "response", "rules", "specialized", "use", "users", "when", "wiki", "workflows"]
tier: 2
risk: "medium"
estimated_tokens: 333
tools_needed: ["markdown"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["engineering", "productivity"]
quality_score: 0.63
date_added: "2026-02-27"
description: "Answer repository questions grounded entirely in source code evidence. Use when user asks a question about the codebase, user wants to understand a specific file, function, or component, or user asks \\\"how does X work\\\" or \\\"where is Y defined\\\"."
source: "community"
---
# Wiki Q&A

Answer repository questions grounded entirely in source code evidence.

## When to Use
- User asks a question about the codebase
- User wants to understand a specific file, function, or component
- User asks "how does X work" or "where is Y defined"

## Procedure

1. Detect the language of the question; respond in the same language
2. Search the codebase for relevant files
3. Read those files to gather evidence
4. Synthesize an answer with inline citations

## Response Format

- Use `##` headings, code blocks with language tags, tables, bullet lists
- Cite sources inline: `(src/path/file.ts:42)`
- Include a "Key Files" table mapping files to their roles
- If information is insufficient, say so and suggest files to examine

## Rules

- ONLY use information from actual source files
- NEVER invent, guess, or use external knowledge
- Think step by step before answering

## When to Use
This skill is applicable to execute the workflow or actions described in the overview.
