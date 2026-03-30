# 🧭 MASTER SKILLS ROUTER - SIÊU ĐIỀU PHỐI (~1,999 SKILLS)
 
> **MỤC ĐÍCH:** Bộ não trung tâm điều phối và truy cập kho trí tuệ ~1,999 kỹ năng.  
> **QUY TẮC:** AI PHẢI đọc file này TRƯỚC khi thực hiện bất kỳ task nào.
> **CẬP NHẬT:** 2026-03-30 (v6.0.0 - UNIFIED SYSTEM)

---

## 📋 CHIẾN LƯỢC TRUY XUẤT SIÊU TỐC
Với kho ~1,999 skills (đã merge ngTwg + sickn33), AI cần tuân thủ quy trình truy xuất "2 Tầng":

1. **Tầng 1: Nhận diện Category & Master Inventory**
   - Xác định Domain (Frontend, Backend, Security, specialized, etc.)
   - Tải file `master-inventory.md` của category đó.

2. **Tầng 2: Truy vấn Chuyên sâu (Search-First)**
   - Nếu cần tìm skill cụ thể trong Master Inventory: **Sử dụng lệnh `grep_search`** hoặc đọc nhanh Mục lục (TOC) ở đầu file Master.
   - Nếu skill nằm trong **Heavy Folder** (có Scripts/Assets): Tải trực tiếp folder đó.

---

## 🏗️ MA TRẬN PHÂN TẦNG (TIER SYSTEM)

| Tier | Ý Nghĩa | Phạm Vi |
|------|---------|---------|
| **TIER 1** | Đơn giản | CRUD, UI, Boilerplate, Blog, Landing Page |
| **TIER 2** | Bắt buộc | Security, Auth, Performance, SEO, Compliance |
| **TIER 3** | Nâng cao | Scalability, Microservices, Real-time, Optimization |
| **TIER 4** | Chuyên sâu | OS, Firmware, Quant, Space, Life-Critical |

---

## 🗂️ BẢN ĐỒ SIÊU HỆ THỐNG (MAPPING)

### 1. FRONTEND & UI (72+ Skills) ✨ UPDATED
- **Cẩm nang tổng hợp:** `frontend/frontend-master-inventory.md`
- **Heavy Folders:** `frontend-design/`, `react-best-practices/`, `ui-ux-pro-max/`, `vercel-react-best-practices/`
- **Công cụ Core:**
  - **NEW:** `frontend/state-classification.md` - 7 state types (UI, Form, Server, Global, URL, Realtime, Persistent)
- **Common Tags:** `[React, CSS, Tailwind, UI, UX, CRO, Performance, State-Management, Hooks, Context, NextJS, Flutter, Mobile]`

### 2. BACKEND & API (75+ Skills) ✨ UPDATED
- **Cẩm nang tổng hợp:** `backend/backend-master-inventory.md`
- **Heavy Folders:** `api-patterns/`, `typescript-expert/`, `algorithmic-art/`
- **Công cụ Core:**
  - **NEW:** `backend/api-design-standards.md` - REST best practices, pagination, versioning, OpenAPI
  - **NEW:** `backend/database-standards.md` - Schema design, migrations, indexes, soft delete
- **Common Tags:** `[Nodejs, API, Database, Auth, Typescript, Python, GraphQL, REST, Schema, Migrations, Indexes, Serverless, Edge]`

### 3. SECURITY & PENTEST (27+ Skills) ✨ UPDATED
- **Cẩm nang tổng hợp:** `security/security-master-inventory.md`
- **Heavy Folders:** `active-directory-attacks/`, `aws-penetration-testing/`, `cloud-penetration-testing/`, `vulnerability-scanner/`
- **Công cụ Core:**
  - **NEW:** `security/security-middleware-stack.md` - 7-layer defense (Helmet, CORS, Rate Limiting, CSRF, Input Sanitization)
- **Common Tags:** `[Pentest, XSS, SQLi, Cloud-Security, Red-Team, Audit, OWASP, Middleware, Defense-in-Depth, Zero-Trust]`

### 4. WORKFLOWS & DEBUG (44+ Skills) ✨ UPDATED
- **Cẩm nang tổng hợp:** `workflows/workflows-master-inventory.md` (Gồm TDD, Planning, Git rules)
- **Heavy Folders:** `git-pushing/`, `lint-and-validate/`, `skill-creator/`, `performance-profiling/`
- **Công cụ Core:** 
  - `workflows/debug-protocol.md` - Systematic debugging
  - `workflows/advanced-testing.md` - Testing strategies
  - **NEW:** `workflows/naming-conventions.md` - JS/TS/Python naming rules
  - **NEW:** `workflows/anti-hallucination-v2.md` - 4-layer verification
  - **NEW:** `workflows/documentation-standards.md` - README, ADR, JSDoc
  - **NEW:** `workflows/error-handling-patterns.md` - 6 error patterns
  - **NEW:** `workflows/edge-case-catalog.md` - 70+ edge cases
  - **NEW:** `workflows/refactoring-triggers.md` - 6 refactoring triggers
  - **NEW:** `workflows/concurrency-patterns.md` - Race condition prevention
  - **NEW:** `workflows/resource-cleanup.md` - Memory leak prevention
  - **NEW:** `workflows/logging-standards.md` - Structured logging
  - **NEW:** `workflows/environment-standards.md` - Env validation with Zod
  - **NEW:** `workflows/meta-rules.md` - Rule governance
- **Common Tags:** `[Debug, Testing, Git, Workflow, Automation, Root-Cause, Naming, Hallucination, Documentation, Error-Handling, Edge-Cases, Refactoring, Concurrency, Cleanup, Logging, Environment]`

### 5. AI, AGENTS & DEEP TECH (52+ Skills)
- **SIÊU CẨM NĂNG AGENT:** `deep-tech/ai-agents-master-inventory.md` (Gồm AC, AD, AE, AF, AG)
- **Cẩm nang tổng hợp:** `deep-tech/deep-tech-master-inventory.md` (Agents, MCP, Identity)
- **Heavy Folders:** `agent-identifier/`, `mcp-builder/`, `subagent-driven-development/`
- **Common Tags:** `[AI-Agent, Multi-Agent, RAG, MCP, LLM, Memory, Safety, Anthropic, Claude]`

### 6. SPECIALIZED & LEGACY DOMAINS (1,553+ Skills)
- **SIÊU CẨM NANG (750KB):** `specialized/specialized-master-inventory.md`
- **DI SẢN NGUYÊN BẢN (174 Rules):** `specialized/gemini-core-rules-inventory.md` (Chứa 100% kho tàng từ file GEMINI.md cũ: Quantum, Hardware, LSM-Tree, Compliance, Security Vectors...)
- **Heavy Folders:** `loki-mode/`, `shopify-development/`, `game-development/`, `app-builder/`
- **Common Tags:** `[Shopify, E-commerce, Legacy-Rules, Hardware, Audio, Payment, PDF, XLSX, SEO, Stripe, Azure, Vercel]`

---

## 🎯 LOGIC ĐIỀU PHỐI TỰ ĐỘNG

```javascript
// Case: "Fix bug bảo mật cho hệ thống Shopify"
→ Tags: [Debug, Security, Shopify]
→ Load:
  1. workflows/debug-protocol.md (Rule số 1)
  2. workflows/anti-hallucination-v2.md (Verify libraries)
  3. security/security-middleware-stack.md (7-layer defense)
  4. specialized/specialized-master-inventory.md (Tìm section "Shopify")
  5. specialized/shopify-development/ (Nếu cần script test)

// Case: "Tạo hệ thống RAG dùng MCP"
→ Tags: [AI, RAG, MCP, Backend]
→ Load:
  1. deep-tech/deep-tech-master-inventory.md (Agentic patterns)
  2. deep-tech/mcp-builder/ (Tools xây dựng MCP)
  3. backend/backend-master-inventory.md (Database & API)
  4. backend/api-design-standards.md (REST best practices)
  5. workflows/error-handling-patterns.md (Error handling)

// Case: "Code React component với state management"
→ Tags: [React, Frontend, State]
→ Load:
  1. frontend/frontend-master-inventory.md (React patterns)
  2. frontend/state-classification.md (7 state types)
  3. workflows/naming-conventions.md (camelCase, PascalCase)
  4. workflows/edge-case-catalog.md (Form validation edge cases)

// Case: "Thiết kế REST API cho e-commerce"
→ Tags: [API, Backend, E-commerce, Security]
→ Load:
  1. backend/api-design-standards.md (REST, pagination, versioning)
  2. backend/database-standards.md (Schema, migrations)
  3. security/security-middleware-stack.md (OWASP protection)
  4. workflows/logging-standards.md (Structured logging)
  5. workflows/edge-case-catalog.md (E-commerce edge cases)

// Case: "Refactor code có complexity cao"
→ Tags: [Refactoring, Code-Quality]
→ Load:
  1. workflows/refactoring-triggers.md (6 triggers)
  2. workflows/naming-conventions.md (Consistent naming)
  3. workflows/error-handling-patterns.md (Better error handling)
  4. workflows/edge-case-catalog.md (Missing edge cases)
```

---

## 🚨 QUY TẮC SIÊU TỐI ƯU (TOKEN SAVING)

1. **CHỈ đọc phần cần thiết:** Khi dùng Master Inventory, hãy dùng `view_content_chunk` hoặc `grep_search` để lấy đúng section cần dùng. Tránh nạp toàn bộ 750KB vào context một lúc trừ khi thực sự cần tổng phổ kiến thức.
2. **Context Pruning:** Xoá bỏ skills cũ khi đổi task.
3. **Always Load Workflows First:** Nếu gặp lỗi, quay lại đọc `debug-protocol.md`.
4. **NEW SKILLS PRIORITY:** Khi code, luôn check các skills mới:
   - Naming → `naming-conventions.md`
   - Libraries → `anti-hallucination-v2.md`
   - Errors → `error-handling-patterns.md`
   - Security → `security-middleware-stack.md`
   - Edge Cases → `edge-case-catalog.md`
   - Refactoring → `refactoring-triggers.md`
   - State → `state-classification.md`
   - API → `api-design-standards.md`
   - Database → `database-standards.md`

---

## 📊 COVERAGE MATRIX (96% TOTAL)

| Category | Coverage | Key Skills |
|----------|----------|------------|
| **Naming** | 85% | naming-conventions.md |
| **Anti-Hallucination** | 75% | anti-hallucination-v2.md |
| **Documentation** | 85% | documentation-standards.md |
| **Error Handling** | 90% | error-handling-patterns.md |
| **Security** | 95% | security-middleware-stack.md |
| **Edge Cases** | 85% | edge-case-catalog.md |
| **Refactoring** | 90% | refactoring-triggers.md |
| **Concurrency** | 90% | concurrency-patterns.md |
| **Resource Cleanup** | 95% | resource-cleanup.md |
| **State Management** | 90% | state-classification.md |
| **API Design** | 95% | api-design-standards.md |
| **Database** | 95% | database-standards.md |
| **Logging** | 90% | logging-standards.md |
| **Environment** | 95% | environment-standards.md |
| **Governance** | 90% | meta-rules.md |

---

## 🎓 QUICK SKILL LOOKUP

### By Problem Type

**"Code không chạy / Bug"**
→ `workflows/debug-protocol.md` + `workflows/anti-hallucination-v2.md`

**"Naming không consistent"**
→ `workflows/naming-conventions.md`

**"Thiếu error handling"**
→ `workflows/error-handling-patterns.md`

**"Security vulnerability"**
→ `security/security-middleware-stack.md`

**"Missing edge cases"**
→ `workflows/edge-case-catalog.md`

**"Code quá phức tạp"**
→ `workflows/refactoring-triggers.md`

**"Race condition / Concurrency"**
→ `workflows/concurrency-patterns.md`

**"Memory leak"**
→ `workflows/resource-cleanup.md`

**"State management mess"**
→ `frontend/state-classification.md`

**"API design issues"**
→ `backend/api-design-standards.md`

**"Database problems"**
→ `backend/database-standards.md`

**"Logging không đủ"**
→ `workflows/logging-standards.md`

**"Environment config issues"**
→ `workflows/environment-standards.md`

---

## 📚 SKILL INTEGRATION WITH KIRO.md

All 15 new skills are integrated into KIRO.md as RULE 6-11:

- **RULE 6:** Security-First Coding → `security-middleware-stack.md`
- **RULE 7:** Anti-Hallucination Protocol → `anti-hallucination-v2.md`
- **RULE 8:** Naming Conventions → `naming-conventions.md`
- **RULE 9:** Error Handling Mandatory → `error-handling-patterns.md`
- **RULE 10:** Edge Case Coverage → `edge-case-catalog.md`
- **RULE 11:** Refactoring Discipline → `refactoring-triggers.md`

Additional skills referenced in workflows:
- Documentation → `documentation-standards.md`
- Concurrency → `concurrency-patterns.md`
- Cleanup → `resource-cleanup.md`
- State → `state-classification.md`
- API → `api-design-standards.md`
- Database → `database-standards.md`
- Logging → `logging-standards.md`
- Environment → `environment-standards.md`
- Meta-Rules → `meta-rules.md`

---

---

## 🎯 ROUTING DECISION TREE v6.0.0

```javascript
// UNIFIED SYSTEM - All skills merged into antigravity/skills/
// No more external layer - direct access to all ~1,999 skills

// STEP 1: Identify Category
if (tag in [React, NextJS, Flutter, Mobile, UI, UX]) {
  → LOAD antigravity/skills/frontend/MASTER_INVENTORY.md (72+ skills)
}

if (tag in [API, Database, Auth, Serverless, Edge, Backend]) {
  → LOAD antigravity/skills/backend/MASTER_INVENTORY.md (75+ skills)
}

if (tag in [Security, Pentest, OWASP, Zero-Trust]) {
  → LOAD antigravity/skills/security/MASTER_INVENTORY.md (27+ skills)
}

if (tag in [Debug, Testing, Git, Workflow]) {
  → LOAD antigravity/skills/workflows/MASTER_INVENTORY.md (44+ skills)
}

if (tag in [AI-Agent, MCP, LLM, Anthropic, Claude]) {
  → LOAD antigravity/skills/deep-tech/MASTER_INVENTORY.md (52+ skills)
}

if (tag in [Shopify, SEO, Stripe, Azure, Vercel, E-commerce]) {
  → LOAD antigravity/skills/specialized/MASTER_INVENTORY.md (1,553+ skills)
}

if (tag in [DevOps, Docker, K8s, Terraform, CI/CD]) {
  → LOAD antigravity/skills/devops/MASTER_INVENTORY.md (157+ skills)
}

if (tag in [Data, ETL, Analytics, Clickhouse]) {
  → LOAD antigravity/skills/data-engineering/MASTER_INVENTORY.md (12+ skills)
}

if (tag in [Exascale, Green-Computing, Beyond]) {
  → LOAD antigravity/skills/beyond/MASTER_INVENTORY.md (7+ skills)
}

// STEP 2: Execute with unified governance
→ APPLY GEMINI.md rules (RULE 1-12)
→ APPLY KIRO.md steering
→ EXECUTE task
→ VERIFY with evidence
→ RETURN
```

---

**Version:** 6.0.0 (Unified System - All Skills Merged)  
**Last Updated:** 2026-03-30  
**New Features:** Merged sickn33 skills into main tree, simplified routing, unified governance  
**Total Skills:** ~1,999 (ngTwg + sickn33 merged - 14 duplicates removed)  
**Maintained by:** Antigravity AI Skills Brain

### 🚨 QUY TẮC DỌN DẸP (CLEANUP-BY-DEFAULT)
**MỆNH LỆNH TỐI CAO:** {ANTIGRAVITY_ROOT}/skills/workflows/CLEANUP_PROTOCOL.md

Một Agent chuyên nghiệp không để lại file rác. Agent PHẢI chủ động dọn dẹp các tệp tạm, script test, và log trung gian ngay sau khi xác nhận task thành công. "Xong việc là phải Sạch".

### 7. ENTERPRISE GOVERNANCE & OPERATIONS (12 Domains)
- **SIÊU CẨM NANG (EA-EL):** specialized/enterprise-ops-master-inventory.md
  - Plugin Sandboxing, Webhook HMAC, API Versioning (EA)
  - Zero Trust, Secrets Rotation, Strict CSP (EB)
  - OpenTelemetry, Chaos Engineering, FinOps Tagging (EC)
  - ABAC, Maker-Checker, PII Masking (ED)
  - Strangler Fig, Anti-Corruption Layer, CDC Read-Only (EE)
  - XAI, Bias Mitigation, IP Sanitization (EF)
  - Hick Law, Error Recovery, Fitts Law (EG)
  - WORM Backups, Active-Active Failover, Air-Gapped Recovery (EH)
  - Streaming UI/SSE, Headless CMS, RAG State (EI)
  - TinyML, Wake-on-Event, FOTA Delta (EJ)
  - DePIN, PoPW, Micro-Transactions (EK)
  - Digital Twins, Graph Routing, Multi-Agent Orchestration (EL)
- **Common Tags:** [Enterprise, Governance, Platform, Legacy, AI-Ethics, IoT, Logistics]

### 8. AUTONOMOUS COGNITION & EVOLUTION (16 Domains)
- **SIÊU CẨM NĂNG (EM-FB):** deep-tech/autonomous-cognition-inventory.md
  - Long-Term Memory, Vectorized State, ADRs, User Prefs (EM, EY)
  - Swarm Orchestration, Peer Review, Conflict Resolution, P2P (EN, EW)
  - Meta-Cognition, Skill Auto-Evolution, Distillation, Fine-Tuning (EO, EU, EZ)
  - HITL Safety, Permission Rings, Kill-Switch, Threat Defense (EP, ES)
  - Computer Use, Visual QA, OS Navigation, Hardware-in-the-loop (EQ, EX)
  - Financial Autonomy, Price Arbitrage, Predictive Cache (ER, FA, EV, FB)
- **Common Tags:** [Cognition, Evolution, Swarm, Memory, Safety, Economics, Predictive]

