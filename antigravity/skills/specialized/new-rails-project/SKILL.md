---
name: "new-rails-project"
tags: ["antigravity", "background", "c:", "code", "database", "frontend", "gemini", "guidance", "jobs", "<YOUR_USERNAME>", "maintenace", "new", "project", "rails", "specialized", "stack", "tech", "testing", "users"]
tier: 2
risk: "medium"
estimated_tokens: 550
tools_needed: ["docker", "markdown", "mcp", "playwright", "sql", "terminal"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["web", "product"]
quality_score: 0.68
allowed-tools: "Bash(rails *), Bash(bundle *), Bash(bin/*), Bash(npm *), Bash(yarn *)"
argument-hint: "[project name]"
author: "Shpigford"
context: "fork"
description: "Create a new Rails project"
metadata: ""
source: "community"
version: "1.0"
---
Generate a new Rails project named $1 in the current directory. You may reference @CLAUDE.md for general guidance, though the guidance here takes precedence.

# Tech Stack
Set up the following tech stack:
- **Rails ~8** with PostgreSQL - Server-side framework and database
- **Inertia.js ~2.3** - Bridges Rails and React for SPA-like experience without API
- **React ~19.2** - Frontend UI framework
- **Vite ~5** - JavaScript bundler with HMR
- **Tailwind CSS ~4** - Utility-first CSS framework
- **Sidekiq 8** - Background job processing with scheduled jobs via sidekiq-scheduler
- **Redis** - Sessions, caching, and job queue

# Rails guidance
- Do not use Kamal or Docker
- Do not use Rails "solid_*" components/systems
- Development should generally match production settings where possible
- Use Redis for caching

# Database
- All tables use UUID primary keys (pgcrypto extension)
- Timestamps use `timestamptz` for timezone awareness
- JSONB columns for flexible metadata storage
- Comprehensive indexing strategy for performance
- Encrypted fields for sensitive data (OAuth tokens, API keys)

# Background jobs
- Use Sidekiq 8 with Redis

# Testing
- Always use minitest
- Use `mocha` gem and VCR for external services (only in the providers layer)
- Prefer `OpenStruct` for mock instances
- Only mock what's necessary

# Code maintenace
- Run `bundle exec rubocop -a` after significant code changes
- Use `.rubocop.yml` for style configuration
- Security scanning with `bundle exec brakeman`

# Frontend
- All React components and views should be TSX

# General guidance
- Ask lots of clarifying questions when planning. The more the better. Make extensive use of AskUserQuestionTool to gather requirements and specifications. You can't ask too many questions.

# Verify
Verify the boilerplate is working by running `bin/rails server` and accessing the application at `http://localhost:3000` via playwright MCP.
