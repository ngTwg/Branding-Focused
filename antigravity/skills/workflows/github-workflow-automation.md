---
name: "🔧 Skill: GitHub Workflow Automation"
tags: ["activation", "antigravity", "automation", "benchmark", "c:", "execution", "frontend", "gemini", "github", "<YOUR_USERNAME>", "output", "pipeline", "signals", "signature", "skill", "steps", "sub", "task", "users", "workflow"]
tier: 3
risk: "medium"
estimated_tokens: 314
tools_needed: ["git", "markdown", "terminal"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["web", "product"]
quality_score: 0.58
---
# 🔧 Skill: GitHub Workflow Automation

> **PURPOSE:** Automate GitHub workflows with AI assistance, covering PR reviews, issue triage, and CI/CD integration.
> **CATEGORY:** Workflows
> **TIER:** 2+

---

## 🚦 ACTIVATION SIGNALS

- Keywords: `GitHub Actions`, `PR automation`, `issue triage`, `CI/CD pipeline`.
- Task: Setting up automated review bots, triage scripts, or maintenance workflows.

---

## 🛠️ SUB-STEPS (EXECUTION PIPELINE)

1. **Workflow Design**: Define triggers (push, pull_request, schedule, issue_comment).
2. **Action Selection**: Use official/vetted actions (e.g., `actions/checkout`, `actions/github-script`).
3. **AI Integration**: Design prompts for review, triage, or risk assessment within the workflow.
4. **Secret Management**: Inject required API keys (e.g., `ANTHROPIC_API_KEY`) via GitHub Secrets.
5. **Validation**: Test the workflow with representative events.

---

## 📝 OUTPUT SIGNATURE

- `.github/workflows/*.yml` files.
- Prompt templates for AI actions.
- Maintenance/Stale policy definitions.

---

## 🧪 BENCHMARK TASK

- **Input**: "Automate PR reviews with Claude 3.5 Sonnet for all new code changes."
- **Output**: `.github/workflows/ai-review.yml` with: Diff extraction -> AI review prompt -> PR comment posting.
