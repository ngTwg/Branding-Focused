---
name: "personal-tool-builder"
tags: ["ai", "antigravity", "builder", "c:", "core", "criteria", "development", "frontend", "gemini", "<YOUR_USERNAME>", "personal", "philosophy", "product", "related", "skills", "slim", "specialized", "success", "templates", "tool"]
tier: 2
risk: "medium"
estimated_tokens: 355
tools_needed: ["markdown", "sql", "terminal"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["web", "product"]
quality_score: 0.62
description: "Guide for building personal/local CLI tools and small SaaS applications for individual use. Focuses on local-first architecture and developer experience."
---
# Personal Tool Builder (v6.5.0-SLIM)

Guide for designing and building highly effective personal utilities, CLI tools, and local-first applications.

## Product Philosophy
- **Solved Problems:** Don't build for "what if." Build to solve a task you performed manually **at least twice** this week.
- **Local-First:** Prefer local file storage (JSON, SQLite) over remote databases unless syncing is core to the feature.
- **CLI Over GUI:** Lead with a CLI. Faster to build, easier to integrate into workflows (shortcuts, cron).

## Development Workflow
1. **MVP (v0.1):** Single file script to solve the core task.
2. **Configuration:** Add `.json` or `.yaml` config support.
3. **Distribution:** Use `bin` entry in `package.json` for easy `npm link` behavior.

## Core Templates
- **Node.js CLI:** Use `commander` or `yargs` for argument parsing.
- **Shell Scripts:** Use `bash` for simple automation.
- **Python:** Use `click` or `argparse` for complex data tools.

## Success Criteria
- Speed: Can you run the tool in < 1 second?
- Reliability: 100% success on valid inputs.
- Maintainability: Simple enough to fix in 5 minutes after 6 months of no use.

## Related Skills
`backend-patterns`, `automation-blockrun`.
