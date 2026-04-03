---
name: "Specialized Skills (Master Inventory)"
tags: ["specialized"]
tier: 4
risk: "high"
estimated_tokens: 726
tools_needed: ["markdown"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["specialized"]
quality_score: 0.55
---
# Specialized Skills (Master Inventory)

> **PURPOSE:** Group focused, domain-specific skills for high-tier or niche tasks.
> **CATEGORY:** Specialized
> **TIER:** 2+

---

## 📋 Table of Contents

- [Cognitive Behavior Framework](#cognitive-behavior-framework)
- [Clarification Protocol](#clarification-protocol)
- [Conversational Guidance](#conversational-guidance)
- [Data Interpretation](#data-interpretation)
- [Research and Synthesis](#research-and-synthesis)
- [Technical Writing](#technical-writing)
- [Document Synthesis](#document-synthesis)
- [Enterprise Ops (External)](#enterprise-ops)
- [Marketing (External)](#marketing)
- [System Tools (External)](#system-tools)

---

<a id="cognitive-behavior-framework"></a>

## 🧠 Cognitive Behavior Framework

> **PURPOSE:** Strategic reasoning, depth calibration, and adaptive problem decomposition core.
> **FILE:** `antigravity/skills/specialized/cognitive-behavior-framework.md`

### 🛠️ Key Rules

1. **Adaptive Depth**: Scale response prose/tech based on constraints.
2. **Decomposition**: Trigger headers/tables/diagrams for complex tasks.
3. **Uncertainty Calibration**: Explicit "low-confidence" markers.

---

<a id="clarification-protocol"></a>

## ❓ Clarification Protocol

> **PURPOSE:** Prevent assumption-driven implementation when requests are underspecified.
> **FILE:** `antigravity/skills/specialized/ask-questions-if-underspecified/SKILL.md`

### 🛠️ Key Rules

1. **Detect Ambiguity Early**: If objective/scope/constraints are unclear, trigger clarification mode.
2. **Ask Minimum Questions**: Ask 1-5 must-have questions before implementation.
3. **Safe Pause**: Do not apply code changes until answers or explicit assumption approval.
4. **Defaults Path**: If user replies `defaults`, proceed with recommended defaults and restated assumptions.

---

<a id="conversational-guidance"></a>

## 💬 Conversational Guidance

> **PURPOSE:** Optimize interactions, minimize performative noise, and maximize technical clarity.
> **FILE:** `antigravity/skills/specialized/conversational-guidance.md`

### 🛠️ Execution Pipeline

1. **Audit**: Detect performative agreement or "filler" prose.
2. **Standardization**: Apply YAGNI to conversation (Technical > Social).
3. **Drafting**: Use bulleted lists, tables, and concise summaries.

---

<a id="data-interpretation"></a>

## 📈 Data Interpretation

> **PURPOSE:** Convert raw data (JSON, CSV, SQL) into actionable insights.
> **FILE:** `antigravity/skills/specialized/data-interpretation.md`

### 🛠️ Execution Pipeline

1. **Context Mapping**: Identify types and ranges.
2. **Standardization**: Clean nulls/outliers.
3. **Hypothesis**: Compare theory vs data.
4. **Statistical Summarization**: Min/Max/Avg/p99.
5. **Insights Synthesis**: Draw 3-5 conclusions.

---

<a id="research-and-synthesis"></a>

## 🔍 Research and Synthesis

> **PURPOSE:** Deep information retrieval and multi-source consolidation.
> **FILE:** `antigravity/skills/specialized/research-and-synthesis.md`

### 🛠️ Execution Pipeline

1. **Query Expansion**: 3-5 distinct search queries.
2. **Retrieval**: Gather raw results via search tools.
3. **Credibility Filter**: Rank by authority types.
4. **Synthesis**: Cohesive report with thematic grouping.

---

<a id="technical-writing"></a>

## ✍️ Technical Writing

> **PURPOSE:** Convert raw info/code into production-grade documentation.
> **FILE:** `antigravity/skills/specialized/technical-writing.md`

### 🛠️ Execution Pipeline

1. **Profiling**: Newbie vs Dev vs Exec vs Expert.
2. **Structural Design**: Choose template (Reference, Guide, etc.).
3. **Drafting**: Active voice, no filler words.
4. **Visuals**: Code/Mermaid/Tables.
5. **Clarity**: Simplify and use 2nd person instruction.

---

<a id="document-synthesis"></a>

## 📑 Document Synthesis

> **PURPOSE:** Analyze and synthesize info from multiple source files.
> **FILE:** `antigravity/skills/specialized/doc-synthesis.md`

### 🛠️ Execution Pipeline

1. **Extraction**: Identify claims/entities/relationships.
2. **Context Mapping**: Correlate across documents.
3. **Thematic Organization**: Group by finding, not source.
4. **Insight Synthesis**: Actionable conclusions.
5. **Quality Review**: Filter citations and hallucinations.

---

<a id="enterprise-ops"></a>

## 🏢 Enterprise Ops (Inventory)

> **PURPOSE:** Large-scale operational and management skills.
> **FILE:** `antigravity/skills/specialized/enterprise-ops-master-inventory.md`

---

<a id="marketing"></a>

## 📣 Marketing (Inventory)

> **PURPOSE:** Content strategy, psychology, and campaign management.
> **FILE:** `antigravity/skills/specialized/marketing-master-inventory.md`

---

<a id="system-tools"></a>

## 🛠️ System Tools (Inventory)

> **PURPOSE:** Low-level OS, CLI, and infrastructure management tools.
> **FILE:** `antigravity/skills/specialized/system_tools-master-inventory.md`
