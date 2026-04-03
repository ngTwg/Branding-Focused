---
name: "📚 Skill: Research and Synthesis"
tags: ["activation", "and", "antigravity", "backend", "benchmark", "c:", "execution", "gemini", "<YOUR_USERNAME>", "output", "pipeline", "research", "signals", "signature", "skill", "specialized", "steps", "sub", "synthesis", "task"]
tier: 3
risk: "medium"
estimated_tokens: 294
tools_needed: ["markdown"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["platform", "api"]
quality_score: 0.57
---
# 📚 Skill: Research and Synthesis

> **PURPOSE:** Deep information retrieval and multi-source consolidation.
> **CATEGORY:** Specialized
> **TIER:** 2+

---

## 🚦 ACTIVATION SIGNALS
- Keywords: `research`, `search`, `find info`, `summarize multiple sources`, `what is the state of X`.
- Task: Market analysis, technical literature review, competitive research.

---

## 🛠️ SUB-STEPS (EXECUTION PIPELINE)

1. **Query Expansion**: Generate 3-5 distinct search queries for the same topic.
2. **Deep Retrieval**: Use `search_web` or `tavily-web` to gather raw results.
3. **Credibility Filter**: Rank sources by authority (official docs > peer-reviewed > reputable blogs > forums).
4. **Information Extraction**: Pull relevant snippets, stats, and quotes.
5. **Synthesis**: Create a cohesive report thematic grouping, resolving contradictions between sources.

---

## 📝 OUTPUT SIGNATURE
- Executive Summary.
- Key Findings (bulleted).
- Sources / Bibliography.
- (Optional) Comparison Matrix.

---

## 🧪 BENCHMARK TASK
- **Input**: "Research the current pricing models for AI vector databases."
- **Output**: Pinecone vs Weaviate vs Milvus vs Neon (Pricing tiers, storage costs).
