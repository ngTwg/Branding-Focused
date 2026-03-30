# 📋 KẾ HOẠCH TRIỂN KHAI HỆ THỐNG RULES CHỐNG "BỆNH AI CODING"

> **Mục tiêu:** Nâng coverage từ 70% lên 95%+  
> **Timeline:** 4 sprints (8 tuần)  
> **Phương pháp:** Chia nhỏ, triển khai dần, automated enforcement

---

## 🎯 TỔNG QUAN

### Metrics mục tiêu
- **Coverage:** 70% → 95%
- **Files cần tạo:** 20 files
- **Automated checks:** 15+ checks
- **Team adoption:** 90%+ compliance

### Phân chia công việc
- **Phase 1 (Sprint 1-2):** Foundation - 8 files URGENT
- **Phase 2 (Sprint 3-4):** Safety & Quality - 6 files
- **Phase 3 (Sprint 5-6):** Excellence - 6 files
- **Phase 4 (Sprint 7-8):** Automation & Polish

---

## 📦 PHASE 1: FOUNDATION (Sprint 1-2) - URGENT

### Sprint 1: Core Standards (Tuần 1-2)

#### Task 1.1: Naming Conventions ⚡ CRITICAL
**File:** `antigravity/skills/workflows/naming-conventions.md`  
**Priority:** P0 (Highest)  
**Estimate:** 4 hours  
**Dependencies:** None

**Subtasks:**
- [ ] 1.1.1 Viết rules cho JavaScript/TypeScript (camelCase, PascalCase, UPPER_SNAKE_CASE)
- [ ] 1.1.2 Viết rules cho Python (snake_case, PascalCase)
- [ ] 1.1.3 Thêm examples ✅ và ❌ cho mỗi rule
- [ ] 1.1.4 Thêm enforcement commands (eslint, prettier, ruff, black)
- [ ] 1.1.5 Tạo checklist validation

**Acceptance Criteria:**
- Có rules cụ thể cho ít nhất 3 ngôn ngữ
- Mỗi rule có ít nhất 2 examples (good/bad)
- Có automated enforcement commands


#### Task 1.2: Anti-Hallucination Protocol V2 ⚡ CRITICAL
**File:** `antigravity/skills/workflows/anti-hallucination-v2.md`  
**Priority:** P0  
**Estimate:** 6 hours  
**Dependencies:** None

**Subtasks:**
- [ ] 1.2.1 Tầng 1: Library/Package verification (npm view, pip show)
- [ ] 1.2.2 Tầng 2: API signature verification (copy từ docs)
- [ ] 1.2.3 Tầng 3: Logic hallucination detection (dry-run protocol)
- [ ] 1.2.4 Tầng 4: Configuration hallucination (validate config)
- [ ] 1.2.5 Tạo verification checklist
- [ ] 1.2.6 Thêm common hallucination examples

**Acceptance Criteria:**
- 4 tầng verification đầy đủ
- Có protocol cụ thể cho mỗi tầng
- Có ít nhất 10 common hallucination examples

#### Task 1.3: Documentation Standards ⚡ CRITICAL
**File:** `antigravity/skills/workflows/documentation-standards.md`  
**Priority:** P0  
**Estimate:** 5 hours  
**Dependencies:** None

**Subtasks:**
- [ ] 1.3.1 Template README.md (mandatory)
- [ ] 1.3.2 Template PROJECT_MAP.md (mandatory)
- [ ] 1.3.3 Template ADR (Architecture Decision Records)
- [ ] 1.3.4 JSDoc/docstring standards
- [ ] 1.3.5 API documentation standards (OpenAPI)
- [ ] 1.3.6 Comment guidelines (when/what to comment)

**Acceptance Criteria:**
- 3 mandatory templates (README, PROJECT_MAP, ADR)
- JSDoc examples cho functions
- OpenAPI spec examples cho APIs

#### Task 1.4: Error Handling Patterns 🔥 HIGH
**File:** `antigravity/skills/workflows/error-handling-patterns.md`  
**Priority:** P1  
**Estimate:** 4 hours  
**Dependencies:** None

**Subtasks:**
- [ ] 1.4.1 Pattern 1: Early Return (Guard Clauses)
- [ ] 1.4.2 Pattern 2: Result Type (No Exceptions)
- [ ] 1.4.3 Pattern 3: Centralized Error Handler
- [ ] 1.4.4 Pattern 4: Error Boundaries (React)
- [ ] 1.4.5 Try-catch best practices
- [ ] 1.4.6 Error logging standards

**Acceptance Criteria:**
- Ít nhất 4 patterns với code examples
- Có comparison good/bad cho mỗi pattern
- Có integration với logging system

---

### Sprint 2: Security & Quality (Tuần 3-4)

#### Task 2.1: Security Middleware Stack 🔥 HIGH
**File:** `antigravity/skills/security/security-middleware-stack.md`  
**Priority:** P1  
**Estimate:** 5 hours  
**Dependencies:** None

**Subtasks:**
- [ ] 2.1.1 Helmet.js configuration
- [ ] 2.1.2 CORS configuration (whitelist origins)
- [ ] 2.1.3 Rate limiting (express-rate-limit)
- [ ] 2.1.4 CSRF protection
- [ ] 2.1.5 Input sanitization (express-mongo-sanitize, hpp)
- [ ] 2.1.6 Security headers checklist
- [ ] 2.1.7 Pre-commit security hooks

**Acceptance Criteria:**
- Setup guide cho 6+ middleware
- Configuration examples cho production
- Pre-commit hook script

#### Task 2.2: Edge Case Catalog 🔥 HIGH
**File:** `antigravity/skills/workflows/edge-case-catalog.md`  
**Priority:** P1  
**Estimate:** 6 hours  
**Dependencies:** None

**Subtasks:**
- [ ] 2.2.1 Authentication edge cases (15+ cases)
- [ ] 2.2.2 E-commerce edge cases (10+ cases)
- [ ] 2.2.3 Form validation edge cases (20+ cases)
- [ ] 2.2.4 File upload edge cases (10+ cases)
- [ ] 2.2.5 Date/time edge cases (timezone, DST)
- [ ] 2.2.6 Numeric edge cases (overflow, precision)
- [ ] 2.2.7 String edge cases (Unicode, emoji, SQL injection)

**Acceptance Criteria:**
- Ít nhất 70+ edge cases được catalog
- Mỗi domain có checklist riêng
- Có test case examples

#### Task 2.3: Refactoring Triggers 🔥 HIGH
**File:** `antigravity/skills/workflows/refactoring-triggers.md`  
**Priority:** P1  
**Estimate:** 4 hours  
**Dependencies:** None

**Subtasks:**
- [ ] 2.3.1 Trigger 1: Rule of Three (copy-paste 3 lần)
- [ ] 2.3.2 Trigger 2: Function > 50 lines
- [ ] 2.3.3 Trigger 3: File > 300 lines
- [ ] 2.3.4 Trigger 4: Cyclomatic Complexity > 10
- [ ] 2.3.5 Trigger 5: Nested Depth > 3
- [ ] 2.3.6 Code smell detection
- [ ] 2.3.7 Refactoring patterns catalog

**Acceptance Criteria:**
- 5+ triggers với thresholds cụ thể
- Mỗi trigger có before/after examples
- Có automated detection tools

#### Task 2.4: Cập nhật KIRO.md với Rules mới ⚡ CRITICAL
**File:** `.kiro/steering/KIRO.md`  
**Priority:** P0  
**Estimate:** 2 hours  
**Dependencies:** Tasks 1.1, 1.2, 1.3

**Subtasks:**
- [ ] 2.4.1 Thêm RULE 6: SECURITY-FIRST CODING
- [ ] 2.4.2 Thêm RULE 7: ANTI-HALLUCINATION PROTOCOL
- [ ] 2.4.3 Cập nhật RULE 5: PROJECT PROTOCOLS (thêm ADR)
- [ ] 2.4.4 Thêm RULE 8: NAMING CONVENTIONS ENFORCEMENT
- [ ] 2.4.5 Update MASTER_ROUTER.md references

**Acceptance Criteria:**
- 3 rules mới được thêm vào
- Mỗi rule có examples cụ thể
- Links đến skill files tương ứng

---

## 📦 PHASE 2: SAFETY & QUALITY (Sprint 3-4)

### Sprint 3: Concurrency & Resources (Tuần 5-6)

#### Task 3.1: Concurrency Patterns 🟡 MEDIUM
**File:** `antigravity/skills/workflows/concurrency-patterns.md`  
**Priority:** P2  
**Estimate:** 6 hours  
**Dependencies:** None

**Subtasks:**
- [ ] 3.1.1 Race condition detection checklist
- [ ] 3.1.2 Pattern 1: Atomic Operations ($inc, INCREMENT)
- [ ] 3.1.3 Pattern 2: Optimistic Locking (version field)
- [ ] 3.1.4 Pattern 3: Pessimistic Locking (SELECT FOR UPDATE)
- [ ] 3.1.5 Pattern 4: Idempotency Keys
- [ ] 3.1.6 Pattern 5: Distributed Locks (Redis SETNX)
- [ ] 3.1.7 Testing concurrent scenarios

**Acceptance Criteria:**
- 5 patterns với code examples
- Có comparison khi nào dùng pattern nào
- Có test examples cho race conditions

#### Task 3.2: Resource Cleanup Standards 🟡 MEDIUM
**File:** `antigravity/skills/workflows/resource-cleanup.md`  
**Priority:** P2  
**Estimate:** 4 hours  
**Dependencies:** None

**Subtasks:**
- [ ] 3.2.1 Frontend cleanup (React useEffect)
- [ ] 3.2.2 Backend cleanup (connections, files, streams)
- [ ] 3.2.3 Memory leak detection tools
- [ ] 3.2.4 Cleanup checklist by resource type
- [ ] 3.2.5 Common leak patterns
- [ ] 3.2.6 Testing for leaks

**Acceptance Criteria:**
- Checklist cho 10+ resource types
- Detection tools cho frontend & backend
- Có leak examples với fixes

#### Task 3.3: State Management Classification 🟡 MEDIUM
**File:** `antigravity/skills/frontend/state-classification.md`  
**Priority:** P2  
**Estimate:** 4 hours  
**Dependencies:** None

**Subtasks:**
- [ ] 3.3.1 State types classification table
- [ ] 3.3.2 UI State (useState, useReducer)
- [ ] 3.3.3 Form State (React Hook Form, Formik)
- [ ] 3.3.4 Server State (TanStack Query, SWR)
- [ ] 3.3.5 Global State (Zustand, Context)
- [ ] 3.3.6 URL State (URLSearchParams)
- [ ] 3.3.7 Realtime State (WebSocket + Zustand)
- [ ] 3.3.8 Anti-patterns (useState cho server state)

**Acceptance Criteria:**
- Classification table đầy đủ
- Mỗi loại state có tool recommendations
- Có anti-patterns examples

---

### Sprint 4: API & Database (Tuần 7-8)

#### Task 4.1: API Design Standards 🟡 MEDIUM
**File:** `antigravity/skills/backend/api-design-standards.md`  
**Priority:** P2  
**Estimate:** 5 hours  
**Dependencies:** None

**Subtasks:**
- [ ] 4.1.1 URL naming conventions (REST)
- [ ] 4.1.2 Response envelope standard
- [ ] 4.1.3 HTTP status codes guide
- [ ] 4.1.4 Pagination standard
- [ ] 4.1.5 Filtering & sorting standard
- [ ] 4.1.6 Versioning strategy
- [ ] 4.1.7 Error response format
- [ ] 4.1.8 OpenAPI spec template

**Acceptance Criteria:**
- Complete API design guide
- Response envelope examples
- OpenAPI template file

#### Task 4.2: Database Standards 🟡 MEDIUM
**File:** `antigravity/skills/backend/database-standards.md`  
**Priority:** P2  
**Estimate:** 5 hours  
**Dependencies:** None

**Subtasks:**
- [ ] 4.2.1 Migration rules (idempotent, rollback)
- [ ] 4.2.2 Schema design checklist
- [ ] 4.2.3 Naming conventions (tables, columns, indexes)
- [ ] 4.2.4 Query performance rules
- [ ] 4.2.5 Index strategy
- [ ] 4.2.6 Foreign key strategies
- [ ] 4.2.7 Soft delete pattern

**Acceptance Criteria:**
- Migration best practices
- Schema checklist
- Query optimization guide

#### Task 4.3: Logging Standards 🟡 MEDIUM
**File:** `antigravity/skills/workflows/logging-standards.md`  
**Priority:** P2  
**Estimate:** 4 hours  
**Dependencies:** None

**Subtasks:**
- [ ] 4.3.1 Log levels guide (FATAL, ERROR, WARN, INFO, DEBUG)
- [ ] 4.3.2 What to log / what NOT to log
- [ ] 4.3.3 Structured logging format (JSON)
- [ ] 4.3.4 Correlation IDs (traceId)
- [ ] 4.3.5 PII handling in logs
- [ ] 4.3.6 Log aggregation setup

**Acceptance Criteria:**
- Log level decision tree
- Structured logging examples
- PII sanitization guide

---

## 📦 PHASE 3: EXCELLENCE (Sprint 5-6)

### Sprint 5: Environment & Monitoring (Tuần 9-10)

#### Task 5.1: Environment Standards 🟢 LOW
**File:** `antigravity/skills/workflows/environment-standards.md`  
**Priority:** P3  
**Estimate:** 3 hours  
**Dependencies:** None

**Subtasks:**
- [ ] 5.1.1 Env validation with Zod
- [ ] 5.1.2 .env file structure (.env.example, .env.development, etc.)
- [ ] 5.1.3 Secrets management (never commit, never log)
- [ ] 5.1.4 Environment-specific configs
- [ ] 5.1.5 Type-safe env access

**Acceptance Criteria:**
- Zod validation example
- .env.example template
- Secrets checklist

#### Task 5.2: Meta-Rules Documentation 🟢 LOW
**File:** `antigravity/skills/workflows/meta-rules.md`  
**Priority:** P3  
**Estimate:** 3 hours  
**Dependencies:** All previous tasks

**Subtasks:**
- [ ] 5.2.1 Rule hierarchy (Security > Data > Business > Performance > Style)
- [ ] 5.2.2 When to override rules
- [ ] 5.2.3 Rule decay protocol (review every 3 months)
- [ ] 5.2.4 Rule adoption strategy
- [ ] 5.2.5 Measuring rule effectiveness

**Acceptance Criteria:**
- Clear hierarchy documented
- Override decision tree
- Review schedule template

---

## 📦 PHASE 4: AUTOMATION & POLISH (Sprint 7-8)

### Sprint 6: Automated Enforcement (Tuần 11-12)

#### Task 6.1: Pre-commit Hooks Setup ⚡ CRITICAL
**File:** `.husky/pre-commit`  
**Priority:** P0  
**Estimate:** 4 hours  
**Dependencies:** Tasks 1.1, 2.1

**Subtasks:**
- [ ] 6.1.1 Install husky
- [ ] 6.1.2 Prettier format check
- [ ] 6.1.3 ESLint with max-warnings 0
- [ ] 6.1.4 TypeScript type check
- [ ] 6.1.5 Secret scanning (secretlint)
- [ ] 6.1.6 Run affected tests
- [ ] 6.1.7 Documentation

**Acceptance Criteria:**
- Pre-commit hook chạy được
- Tất cả checks pass
- Documentation cho team

#### Task 6.2: CI Pipeline Setup ⚡ CRITICAL
**File:** `.github/workflows/ci.yml`  
**Priority:** P0  
**Estimate:** 6 hours  
**Dependencies:** Task 6.1

**Subtasks:**
- [ ] 6.2.1 Lint job
- [ ] 6.2.2 Type check job
- [ ] 6.2.3 Unit tests with coverage (80% threshold)
- [ ] 6.2.4 Security audit (npm audit)
- [ ] 6.2.5 Secret scan (trufflehog)
- [ ] 6.2.6 Bundle size check
- [ ] 6.2.7 Lighthouse CI (performance)

**Acceptance Criteria:**
- CI pipeline chạy được
- Tất cả jobs pass
- Coverage report

#### Task 6.3: PR Review Automation 🔥 HIGH
**File:** `.github/workflows/pr-review.yml`  
**Priority:** P1  
**Estimate:** 4 hours  
**Dependencies:** Task 6.2

**Subtasks:**
- [ ] 6.3.1 PR size check (warn if > 400 lines)
- [ ] 6.3.2 Documentation check (PROJECT_MAP.md updated?)
- [ ] 6.3.3 Migration check (schema changed → migration added?)
- [ ] 6.3.4 Test coverage check
- [ ] 6.3.5 Breaking change detection

**Acceptance Criteria:**
- Automated checks chạy trên mọi PR
- Warnings/errors hiển thị rõ ràng
- Documentation cho team

---

### Sprint 7: Integration & Training (Tuần 13-14)

#### Task 7.1: Update MASTER_ROUTER.md 🔥 HIGH
**File:** `antigravity/skills/MASTER_ROUTER.md`  
**Priority:** P1  
**Estimate:** 3 hours  
**Dependencies:** All skill files

**Subtasks:**
- [ ] 7.1.1 Thêm mapping cho 20 files mới
- [ ] 7.1.2 Update decision tree
- [ ] 7.1.3 Thêm examples cho mỗi category
- [ ] 7.1.4 Update token optimization guide

**Acceptance Criteria:**
- Tất cả files mới được map
- Decision tree updated
- Examples đầy đủ

#### Task 7.2: Create Quick Reference Guide 🟡 MEDIUM
**File:** `QUICK_REFERENCE_AI_RULES.md`  
**Priority:** P2  
**Estimate:** 4 hours  
**Dependencies:** All tasks

**Subtasks:**
- [ ] 7.2.1 1-page cheat sheet
- [ ] 7.2.2 Common mistakes & fixes
- [ ] 7.2.3 Checklist trước khi commit
- [ ] 7.2.4 Checklist khi review AI code
- [ ] 7.2.5 Emergency troubleshooting

**Acceptance Criteria:**
- 1-page printable cheat sheet
- Checklist format
- Easy to scan

#### Task 7.3: Team Training Materials 🟡 MEDIUM
**File:** `docs/AI_RULES_TRAINING.md`  
**Priority:** P2  
**Estimate:** 6 hours  
**Dependencies:** All tasks

**Subtasks:**
- [ ] 7.3.1 Presentation slides (30 min)
- [ ] 7.3.2 Hands-on exercises (5 scenarios)
- [ ] 7.3.3 Video walkthrough (15 min)
- [ ] 7.3.4 FAQ document
- [ ] 7.3.5 Onboarding checklist

**Acceptance Criteria:**
- Complete training package
- 5 hands-on exercises
- Video recorded

---

## 📊 TRACKING & METRICS

### Sprint Velocity Tracking
```markdown
| Sprint | Tasks Planned | Tasks Completed | Velocity |
|--------|---------------|-----------------|----------|
| 1      | 4             | ?               | ?        |
| 2      | 4             | ?               | ?        |
| 3      | 3             | ?               | ?        |
| 4      | 3             | ?               | ?        |
| 5      | 2             | ?               | ?        |
| 6      | 3             | ?               | ?        |
| 7      | 3             | ?               | ?        |
```

### Coverage Metrics
```markdown
| Category | Before | Target | Current |
|----------|--------|--------|---------|
| Logic & Edge Case | 80% | 90% | ? |
| Security | 75% | 92% | ? |
| Naming & Style | 30% | 85% | ? |
| Error Handling | 70% | 90% | ? |
| Hallucination | 10% | 75% | ? |
| Module & Refactor | 40% | 80% | ? |
| Documentation | 20% | 85% | ? |
| Concurrency | 0% | 80% | ? |
| Memory Leak | 0% | 80% | ? |
| State Management | 0% | 75% | ? |
| API Design | 0% | 85% | ? |
| Database | 0% | 80% | ? |
| Logging | 0% | 85% | ? |
| Environment | 0% | 80% | ? |
```

### Team Adoption Metrics
```markdown
- Pre-commit hooks enabled: ?/? developers
- CI passing rate: ?%
- Average PR review time: ? hours
- Rules violation rate: ?%
- Code quality score: ?/10
```

---

## 🚀 GETTING STARTED

### Immediate Actions (Today)
1. ✅ Review this plan với team
2. ✅ Assign tasks cho Sprint 1
3. ✅ Setup project tracking (Jira/Linear)
4. ✅ Create branch: `feature/ai-rules-system`

### Sprint 1 Kickoff (Tuần 1)
1. ✅ Team meeting: Giới thiệu mục tiêu
2. ✅ Assign Task 1.1 - 1.4
3. ✅ Daily standup: Track progress
4. ✅ Mid-sprint review: Adjust if needed

---

## 📝 NOTES

### Risk Mitigation
- **Risk:** Team overwhelmed với quá nhiều rules
  - **Mitigation:** Phased rollout, training sessions
  
- **Risk:** Automated checks quá strict, block productivity
  - **Mitigation:** Start with warnings, gradually enforce

- **Risk:** Rules không được follow
  - **Mitigation:** Automated enforcement, peer review

### Success Criteria
- ✅ 95%+ coverage achieved
- ✅ 90%+ team adoption
- ✅ CI/CD pipeline stable
- ✅ Code quality improved measurably
- ✅ Bug rate decreased by 30%+

---

**Created:** 2026-03-30  
**Version:** 1.0.0  
**Owner:** Engineering Team  
**Status:** READY TO START
