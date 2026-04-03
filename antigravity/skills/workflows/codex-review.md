---
name: "🧬 Skill: Codex Review"
tags: ["activation", "antigravity", "benchmark", "c:", "codex", "execution", "gemini", "<YOUR_USERNAME>", "output", "pipeline", "review", "signals", "signature", "skill", "steps", "sub", "task", "users", "workflows"]
tier: 3
risk: "medium"
estimated_tokens: 257
tools_needed: ["markdown", "terminal"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["engineering", "productivity"]
quality_score: 0.57
---
# 🧬 Skill: Codex Review

> **PURPOSE:** Professional code review with auto CHANGELOG generation, integrated with Codex AI.
> **CATEGORY:** Workflows
> **TIER:** 3+

---

## 🚦 ACTIVATION SIGNALS

- Keywords: `/codex-review`, `codex review`, `generate changelog`.
- Goal: Professional review before commits or large refactoring.

---

## 🛠️ SUB-STEPS (EXECUTION PIPELINE)

1. **Tool Setup**: Ensure `npx skills add -g BenedictKing/codex-review` and Codex CLI are available.
2. **Review Execution**: Run the review on changed files.
3. **Changelog Generation**: Automatically generate/update `CHANGELOG.md`.
4. **Validation**: Verify that the review comments are actionable and the changelog is accurate.

---

## 📝 OUTPUT SIGNATURE

- Codex-powered review comments.
- Updated `CHANGELOG.md` in project root.
- Summary of architectural impact.

---

## 🧪 BENCHMARK TASK

- **Input**: "/codex-review this 500-line refactor."
- **Output**: Review with: Summary of changes -> Detailed file comments -> Auto-generated CHANGELOG entry.
