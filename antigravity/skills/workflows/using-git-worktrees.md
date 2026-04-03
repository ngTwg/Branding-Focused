---
name: "🌳 Skill: Using Git Worktrees"
tags: ["activation", "antigravity", "benchmark", "c:", "execution", "frontend", "gemini", "git", "<YOUR_USERNAME>", "output", "pipeline", "signals", "signature", "skill", "steps", "sub", "task", "users", "using", "workflows"]
tier: 3
risk: "medium"
estimated_tokens: 288
tools_needed: ["git", "markdown", "terminal"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["web", "product"]
quality_score: 0.58
---
# 🌳 Skill: Using Git Worktrees

> **PURPOSE:** Create isolated workspaces sharing the same repository for parallel feature work.
> **CATEGORY:** Workflows
> **TIER:** 2+

---

## 🚦 ACTIVATION SIGNALS

- Keywords: `worktrees`, `git worktree`, `isolated workspace`.
- Goal: Feature work that shouldn't pollute the current workspace or requires a clean baseline.

---

## 🛠️ SUB-STEPS (EXECUTION PIPELINE)

1. **Directory Selection**: Check `.worktrees/`, then `worktrees/`, or consult `CLAUDE.md`.
2. **Safety Verification**: Ensure the selected directory is NOT tracked in git (check `.gitignore`).
3. **Creation**: Create the worktree linked to a new branch.
4. **Environment Setup**: Detect and run node_modules/poetry/cargo installs.
5. **Baseline Verification**: Run tests to ensure the base state is clean.

---

## 📝 OUTPUT SIGNATURE

- New worktree directory created.
- `git status` showing all files are ignored if inside the project.
- Report of baseline test status.

---

## 🧪 BENCHMARK TASK

- **Input**: "Start working on the v2 API in a new worktree."
- **Output**: Worktree `api-v2` created in `.worktrees/` -> npm install -> Tests passing.
