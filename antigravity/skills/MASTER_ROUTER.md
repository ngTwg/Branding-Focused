---
name: "🧭 MASTER SKILLS ROUTER - SIÊU ĐIỀU PHỐI (v7.0-WAVE1 FOUNDATION)"
tags: ["antigravity", "api", "atomized", "backend", "bản", "c:", "chiến", "foundation", "frontend", "gemini", "<YOUR_USERNAME>", "lược", "mapping", "master", "phân", "phối", "root", "router", "siêu", "skills"]
tier: 4
risk: "high"
estimated_tokens: 1420
tools_needed: ["docker", "git", "kubernetes", "markdown", "sql", "terraform"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["web", "product"]
quality_score: 0.73
---
# 🧭 MASTER SKILLS ROUTER - SIÊU ĐIỀU PHỐI (v7.0-WAVE1 FOUNDATION)

> **MỤC ĐÍCH:** Bộ não trung tâm điều phối và truy cập kho trí tuệ modular.
> **MỆNH LỆNH:** AI PHẢI đọc file này TRƯỚC khi thực hiện bất kỳ task nào (Rule 1).
> **CẬP NHẬT:** 2026-04-02 (v7.0-WAVE1 - FOUNDATION FIXES)
> **SNAPSHOT:** 5,535 skills | 12 synced repos | 9 core domains (+ Beyond Horizon extension)

---

## 📋 CHIẾN LƯỢC TRUY XUẤT SIÊU TỐC (2 TẦNG)

1. **Tầng 1: Nhận diện Category & Master Inventory**
   - Xác định Domain (Frontend, Backend, Security, Workflows, Specialized, Marketing, AI-Agents, Data, DevOps).
   - Tải file `master-inventory.md` của category đó.

2. **Tầng 2: Truy vấn Chuyên sâu (Search-First)**
   - Sử dụng lệnh `grep_search` để lấy đúng skill block hoặc đọc nhanh Mục lục.
   - Nếu skill yêu cầu logic cực cao (Tier 3/4), tải: **`specialized/cognitive-behavior-framework.md`**.

---

## 🏗️ MA TRẬN PHÂN TẦNG (TIER SYSTEM)

| Tier | Ý Nghĩa | Phạm Vi | Cơ Chế Load |
|------|---------|---------|-------------|
| **TIER 1** | Snippet/Refactor | CRUD, Type fixes, Typo, Read | Skip `MASTER_ROUTER.md`. |
| **TIER 2** | Bắt buộc | New Feature, Bugfix, Security, SEO | Load `MASTER_ROUTER.md` + Inventory. |
| **TIER 3** | Nâng cao | Scalability, Architecture, Multi-agent | Full Chain + `cognitive-behavior-framework.md`. |
| **TIER 4** | Chuyên sâu | Deep Tech, Firmware, Quant, OS | Full Chain + `gemini-extended-rules.md`. |

---

## 🗂️ BẢN ĐỒ SIÊU HỆ THỐNG (MAPPING)

### 1. FRONTEND & UI (Atomized) ✨
- **Cẩm nang tổng hợp:** `frontend/frontend-master-inventory.md`
- **Core Skills:** `3d-web-experience`, `ab-test-setup`, `cro-skills`, `tailwind-patterns`, `react-patterns`.
- **Tags:** `[React, NextJS, CSS, UI/UX, State, Animation, Flutter, Mobile]`

### 2. BACKEND & API (Atomized) ✨
- **Cẩm nang tổng hợp:** `backend/backend-master-inventory.md`
- **Core Skills:** `nestjs-expert`, `prisma-expert`, `algolia-search`, `api-documentation-generator`.
- **Tags:** `[Nodejs, Python, API, DB, Auth, Schema, Serverless, Edge]`

### 3. SECURITY & PENTEST (Atomized) ✨
- **Cẩm nang tổng hợp:** `security/security-master-inventory.md`
- **Core Skills:** `api-security-best-practices`, `burp-suite-testing`, `sql-injection-testing`, `red-team-tactics`.
- **Tags:** `[XSS, SQLi, IDOR, Pentest, Red-Team, Audit, OWASP]`

### 4. WORKFLOWS & DEBUG (Atomized) ✨
- **Cẩm nang tổng hợp:** `workflows/workflows-master-inventory.md`
- **Core Skills:** `analyze-codebase`, `refactor-code`, `debug-errors`, `documentation-templates`.
- **Protocol:** `../workflows/evaluate-ai-behavior.md` (/evaluate-ai-behavior)
- **Tags:** `[Debug, Testing, Git, Planning, Automation, Documentation]`

### 5. SPECIALIZED & COGNITIVE (v6.5-SLIM) ✨
- **Cẩm nang tổng hợp:** `specialized/specialized-master-inventory.md`
- **Core Core:** `specialized/cognitive-behavior-framework.md` (MUST load for Tier 3/4)
- **Skills:** `conversational-guidance`, `doc-synthesis`, `technical-writing`.
- **Tags:** `[Reasoning, Analysis, Writing, Synthesis, Problem-Solving]`

### 6. MARKETING & GROWTH (v6.5-SLIM) ✨
- **Cẩm nang tổng hợp:** `specialized/marketing-master-inventory.md`
- **Core Skills:** `programmatic-seo`, `social-content`, `email-sequence`, `launch-strategy`, `referral-programs`.
- **Tags:** `[Marketing, SEO, Social, Email, Growth, Campaigns, Ads]`

### 7. AI AGENTS & ORCHESTRATION (New) ✨
- **Cẩm nang tổng hợp:** `ai-agents/ai-agents-master-inventory.md`
- **Core Skills:** `orchestrate-workflows`, `autonomous-agents-design`, `llm-coordination`.
- **Tags:** `[Agents, Orchestration, LangGraph, CrewAI, AutoGen, Multi-Agent]`

### 8. DATA ENGINEERING & ANALYTICS (New) ✨
- **Cẩm nang tổng hợp:** `data-engineering/data-engineering-master-inventory.md`
- **Core Skills:** `clickhouse-io`, `data-transformation`, `segment-cdp`, `data-quality-frameworks`.
- **Tags:** `[Data, ETL, ELT, SQL, Spark, Pandas, Analytics, CDO]`

### 9. DEVOPS & PLATFORM RELIABILITY (New) ✨
- **Cẩm nang tổng hợp:** `devops/devops-master-inventory.md`
- **Core Skills:** `cicd-pipelines`, `containerization`, `observability`, `terraform-skill`, `kubernetes-architect`.
- **Tags:** `[DevOps, CI/CD, IaC, Docker, Kubernetes, Terraform, Observability, SRE]`

### 9+. BEYOND HORIZON (Deep Tech Annex) ✨
- **Cẩm nang tổng hợp:** `beyond/SKILL.md`
- **Core Skills:** `exascale-computing`, `green-computing`, `blockchain-developer`, `solidity-security`.
- **Tags:** `[Beyond, Exascale, Green Computing, Web3, Quantum, Frontier Research]`

---

## ❓ CLARIFICATION-FIRST PROTOCOL (MANDATORY)

When the request has multiple plausible interpretations or missing constraints, routing MUST load:
- `specialized/ask-questions-if-underspecified/SKILL.md`

Execution policy:
1. Ask 1-5 must-have questions before implementation.
2. Do not edit files or run irreversible commands before clarification.
3. If user replies `defaults`, proceed using recommended defaults and state assumptions.
4. If user explicitly requests assumption-based execution, restate assumptions before proceeding.

---

## 🚨 QUY TẮC SIÊU TỐI ƯU (TOKEN SAVING)

1. **CHỈ đọc phần cần thiết:** Khi dùng Master Inventory, hãy dùng `grep_search` để lấy đúng skill.
2. **Context Pruning:** Xoá bỏ skills cũ khi hoàn thành task để tránh "Stagnation".
3. **Always Load Workflows First on Error:** Gặp lỗi? Tải ngay `debug-protocol.md`.
4. **Clean-by-Default:** Xoá file tạm, test scripts ngay sau khi task thành công.

---

**Version:** 7.0-WAVE1 (Foundation Fixes)  
**Last Updated:** 2026-04-02  
**Total Capacity:** 5,535 modular skills across 12 synced repositories  
**Domain Coverage:** 9 core domains + Beyond Horizon extension  
**Maintained by:** Antigravity System
