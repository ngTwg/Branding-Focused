---
name: "🎨 Skill: Skill Creator"
tags: ["activation", "antigravity", "benchmark", "c:", "creator", "execution", "frontend", "gemini", "<YOUR_USERNAME>", "output", "pipeline", "signals", "signature", "skill", "steps", "sub", "task", "users", "workflows"]
tier: 3
risk: "medium"
estimated_tokens: 316
tools_needed: ["markdown", "playwright", "terminal"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["web", "product"]
quality_score: 0.58
---
# 🎨 Skill: Skill Creator

> **PURPOSE:** Guide for creating effective, modular, and token-efficient atomic skills.
> **CATEGORY:** Workflows
> **TIER:** 4+

---

## 🚦 ACTIVATION SIGNALS

- Keywords: `create a new skill`, `update existing skill`, `skill framework`.
- Goal: Systematizing specialized knowledge or tool usage.

---

## 🛠️ SUB-STEPS (EXECUTION PIPELINE)

1. **Information Extraction**: Identify concrete examples and patterns for the skill's usage.
2. **Resource Selection**: Determine necessary `scripts/`, `references/`, and `assets/`.
3. **Drafting SKILL.md**: Write YAML frontmatter (only `name` and `description`).
4. **Instruction Writing**: Create the body with clear, imperative steps.
5. **Progressive Disclosure**: Move detailed reference material to separate files to keep SKILL.md under 500 lines.
6. **Packaging**: Validate naming conventions and description completeness.

---

## 📝 OUTPUT SIGNATURE

- `SKILL.md` with appropriate TIER and CATEGORY.
- Optional resource folder structure.
- Benchmarks for the new skill.

---

## 🧪 BENCHMARK TASK

- **Input**: "Create a new skill for scraping dynamic web pages with Playwright."
- **Output**: SKILL.md with: Purpose -> Activation (Keywords) -> Pipeline (Setup -> Logic -> Verification).
