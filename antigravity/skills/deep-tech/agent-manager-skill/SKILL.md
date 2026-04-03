---
name: "agent-manager-skill"
tags: ["agent", "antigravity", "c:", "commands", "common", "deep", "deep-tech", "frontend", "gemini", "<YOUR_USERNAME>", "manager", "notes", "prerequisites", "skill", "tech", "use", "users", "when"]
tier: 2
risk: "medium"
estimated_tokens: 278
tools_needed: ["git", "markdown", "terminal"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["web", "product"]
quality_score: 0.66
date_added: "2026-02-27"
description: "Manage multiple local CLI agents via tmux sessions (start/stop/monitor/assign) with cron-friendly scheduling."
source: "community"
---
# Agent Manager Skill

## When to Use
Use this skill when you need to:

- run multiple local CLI agents in parallel (separate tmux sessions)
- start/stop agents and tail their logs
- assign tasks to agents and monitor output
- schedule recurring agent work (cron)

## Prerequisites

Install `agent-manager-skill` in your workspace:

```bash
git clone https://github.com/fractalmind-ai/agent-manager-skill.git
```

## Common commands

```bash
python3 agent-manager/scripts/main.py doctor
python3 agent-manager/scripts/main.py list
python3 agent-manager/scripts/main.py start EMP_0001
python3 agent-manager/scripts/main.py monitor EMP_0001 --follow
python3 agent-manager/scripts/main.py assign EMP_0002 <<'EOF'
Follow teams/fractalmind-ai-maintenance.md Workflow
EOF
```

## Notes

- Requires `tmux` and `python3`.
- Agents are configured under an `agents/` directory (see the repo for examples).
