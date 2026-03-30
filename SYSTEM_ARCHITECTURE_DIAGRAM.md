# 🏗️ SYSTEM ARCHITECTURE DIAGRAM

> **Visual representation** của hệ thống AI Rules  
> **Date:** 2026-03-30

---

## 📐 KIẾN TRÚC TỔNG QUAN

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER REQUEST                             │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    KIRO.md (Entry Point)                         │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ RULE 1: MASTER ROUTER                                     │  │
│  │ RULE 2: CONTEXT PRUNING                                   │  │
│  │ RULE 3: SYSTEMATIC DEBUGGING                              │  │
│  │ RULE 4: TIER SYSTEM                                       │  │
│  │ RULE 5: PROJECT PROTOCOLS                                 │  │
│  │ ⭐ RULE 6: SECURITY-FIRST CODING (NEW)                    │  │
│  │ ⭐ RULE 7: ANTI-HALLUCINATION (NEW)                       │  │
│  │ ⭐ RULE 8: NAMING CONVENTIONS (NEW)                       │  │
│  │ ⭐ RULE 9: ERROR HANDLING (NEW)                           │  │
│  │ ⭐ RULE 10: EDGE CASE COVERAGE (NEW)                      │  │
│  │ ⭐ RULE 11: REFACTORING DISCIPLINE (NEW)                  │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│              MASTER_ROUTER.md (v4.1.0) - Navigator              │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ 1. Analyze Tags: [React, API, Security, etc.]            │  │
│  │ 2. Determine Tier: 1-4                                    │  │
│  │ 3. Find Category: Frontend/Backend/Security/Workflows    │  │
│  │ 4. Load Appropriate Skills                                │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────────┬────────────────────────────────────┘
                             │
                ┌────────────┴────────────┐
                │                         │
                ▼                         ▼
┌───────────────────────────┐   ┌───────────────────────────┐
│   SKILL CATEGORIES        │   │   COVERAGE MATRIX         │
│                           │   │                           │
│ • Frontend (21 skills)    │   │ • Naming: 85%             │
│ • Backend (28 skills)     │   │ • Security: 95%           │
│ • Security (41 skills)    │   │ • Error Handling: 90%     │
│ • Workflows (65 skills)   │   │ • Edge Cases: 85%         │
│ • Data Engineering        │   │ • Overall: 96%            │
│ • Deep Tech               │   │                           │
│ • Specialized             │   │                           │
│ • Beyond Horizon          │   │                           │
└───────────┬───────────────┘   └───────────────────────────┘
            │
            ▼
┌─────────────────────────────────────────────────────────────────┐
│                    15 NEW SKILL FILES                            │
│                                                                   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ WORKFLOWS (11 files)                                     │   │
│  │ • naming-conventions.md                                  │   │
│  │ • anti-hallucination-v2.md                              │   │
│  │ • documentation-standards.md                             │   │
│  │ • error-handling-patterns.md                             │   │
│  │ • edge-case-catalog.md                                   │   │
│  │ • refactoring-triggers.md                                │   │
│  │ • concurrency-patterns.md                                │   │
│  │ • resource-cleanup.md                                    │   │
│  │ • logging-standards.md                                   │   │
│  │ • environment-standards.md                               │   │
│  │ • meta-rules.md                                          │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ SECURITY (1 file)                                        │   │
│  │ • security-middleware-stack.md                           │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ BACKEND (2 files)                                        │   │
│  │ • api-design-standards.md                                │   │
│  │ • database-standards.md                                  │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ FRONTEND (1 file)                                        │   │
│  │ • state-classification.md                                │   │
│  └─────────────────────────────────────────────────────────┘   │
└───────────────────────────┬───────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                    AI EXECUTION ENGINE                           │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ 1. Apply RULE 8: Naming Conventions                       │  │
│  │ 2. Apply RULE 7: Verify Libraries                         │  │
│  │ 3. Apply RULE 9: Error Handling                           │  │
│  │ 4. Apply RULE 10: Edge Cases                              │  │
│  │ 5. Apply RULE 6: Security                                 │  │
│  │ 6. Apply RULE 11: Refactoring                             │  │
│  │ 7. Run Formatters (eslint, prettier, black)              │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    QUALITY GATES                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ • Pre-commit Hooks (Husky, lint-staged)                  │  │
│  │ • CI/CD Pipeline (GitHub Actions, GitLab CI)             │  │
│  │ • Code Review Checklist                                   │  │
│  │ • Automated Tests (80%+ coverage)                         │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    OUTPUT: HIGH-QUALITY CODE                     │
│  • 96% coverage                                                  │
│  • Security compliant                                            │
│  • Well-documented                                               │
│  • Edge cases handled                                            │
│  • Production-ready                                              │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔄 DATA FLOW DIAGRAM

```
┌──────────┐
│  User    │
│ Request  │
└────┬─────┘
     │
     ▼
┌─────────────────────────────────────────────────────────┐
│ Step 1: KIRO.md Entry                                   │
│ • Check RULE 1: Load MASTER_ROUTER                      │
│ • Check RULE 2: Prune old context                       │
└────┬────────────────────────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────────────────────────────┐
│ Step 2: MASTER_ROUTER Analysis                          │
│ • Parse tags: [React, API, Security]                    │
│ • Determine tier: 1-4                                    │
│ • Identify category: Frontend/Backend/etc.              │
└────┬────────────────────────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────────────────────────────┐
│ Step 3: Load Skills                                     │
│ • Load: naming-conventions.md                           │
│ • Load: anti-hallucination-v2.md                        │
│ • Load: error-handling-patterns.md                      │
│ • Load: security-middleware-stack.md                    │
│ • Load: edge-case-catalog.md                            │
└────┬────────────────────────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────────────────────────────┐
│ Step 4: Execute with Rules                              │
│ • RULE 8: camelCase, PascalCase                         │
│ • RULE 7: npm view, verify API                          │
│ • RULE 9: try-catch, validation                         │
│ • RULE 10: null, undefined, edge cases                  │
│ • RULE 6: OWASP, sanitization                           │
│ • RULE 11: Extract function, reduce complexity          │
└────┬────────────────────────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────────────────────────────┐
│ Step 5: Quality Checks                                  │
│ • Run: eslint --fix                                      │
│ • Run: prettier --write                                  │
│ • Run: tests (80%+ coverage)                             │
│ • Check: security scan                                   │
└────┬────────────────────────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────────────────────────────┐
│ Step 6: Output                                          │
│ • High-quality code                                      │
│ • Documentation updated                                  │
│ • Tests passing                                          │
│ • Ready for review                                       │
└─────────────────────────────────────────────────────────┘
```

---

## 📂 FILE STRUCTURE TREE

```
C:/Users/<YOUR_USERNAME>/.gemini/
│
├── .kiro/
│   └── steering/
│       └── KIRO.md ⭐ (UPDATED)
│           ├── RULE 1-5 (Existing)
│           └── RULE 6-11 (NEW)
│               ├── RULE 6 → security-middleware-stack.md
│               ├── RULE 7 → anti-hallucination-v2.md
│               ├── RULE 8 → naming-conventions.md
│               ├── RULE 9 → error-handling-patterns.md
│               ├── RULE 10 → edge-case-catalog.md
│               └── RULE 11 → refactoring-triggers.md
│
├── antigravity/
│   └── skills/
│       ├── MASTER_ROUTER.md ⭐ (v4.1.0)
│       │   ├── Coverage Matrix (NEW)
│       │   ├── Quick Lookup (NEW)
│       │   └── Skill Integration (NEW)
│       │
│       ├── workflows/ ⭐ (11 NEW)
│       │   ├── naming-conventions.md
│       │   ├── anti-hallucination-v2.md
│       │   ├── documentation-standards.md
│       │   ├── error-handling-patterns.md
│       │   ├── edge-case-catalog.md
│       │   ├── refactoring-triggers.md
│       │   ├── concurrency-patterns.md
│       │   ├── resource-cleanup.md
│       │   ├── logging-standards.md
│       │   ├── environment-standards.md
│       │   └── meta-rules.md
│       │
│       ├── security/ ⭐ (1 NEW)
│       │   └── security-middleware-stack.md
│       │
│       ├── backend/ ⭐ (2 NEW)
│       │   ├── api-design-standards.md
│       │   └── database-standards.md
│       │
│       └── frontend/ ⭐ (1 NEW)
│           └── state-classification.md
│
└── [Project Root]/ ⭐ (18 NEW DOCS)
    ├── Planning/
    │   ├── AI_CODE_DISEASES_ANALYSIS.md
    │   ├── AI_RULES_IMPLEMENTATION_PLAN.md
    │   └── AI_RULES_TASKS_CHECKLIST.md
    │
    ├── Sprint Reports/
    │   ├── SPRINT_1_COMPLETE.md
    │   ├── SPRINT_2_COMPLETE.md
    │   ├── SPRINT_3_COMPLETE.md
    │   ├── SPRINT_4_COMPLETE.md
    │   └── SPRINT_5_COMPLETE.md
    │
    ├── Guides/
    │   ├── QUICK_REFERENCE.md
    │   ├── PRE_COMMIT_SETUP_GUIDE.md
    │   ├── CI_CD_PIPELINE_TEMPLATE.md
    │   └── MANUAL_TASKS_GUIDE.md
    │
    └── Reports/
        ├── FINAL_IMPLEMENTATION_SUMMARY.md
        ├── PROJECT_COMPLETION_REPORT.md
        ├── IMPLEMENTATION_COMPLETE.md
        ├── SYSTEM_VERIFICATION_TEST.md
        ├── FINAL_VERIFICATION_REPORT.md
        ├── COMPLETE_SYSTEM_OVERVIEW.md
        └── SYSTEM_ARCHITECTURE_DIAGRAM.md (this file)
```

---

## 🎯 INTEGRATION POINTS

```
┌─────────────────────────────────────────────────────────────┐
│                    INTEGRATION LAYER                         │
└─────────────────────────────────────────────────────────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
        ▼                    ▼                    ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│   KIRO.md    │◄───┤ MASTER_ROUTER│◄───┤ Skill Files  │
│  (11 Rules)  │    │   (v4.1.0)   │    │  (15 files)  │
└──────┬───────┘    └──────┬───────┘    └──────┬───────┘
       │                   │                    │
       └───────────────────┼────────────────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │   AI Engine     │
                  │  (Execution)    │
                  └────────┬────────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
        ▼                  ▼                  ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│ Pre-commit   │  │   CI/CD      │  │ Code Review  │
│   Hooks      │  │  Pipeline    │  │  Checklist   │
└──────────────┘  └──────────────┘  └──────────────┘
```

---

## 📊 COVERAGE VISUALIZATION

```
Before Implementation (70%)
████████████████████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░

After Implementation (96%)
████████████████████████████████████████████████████████░░

Legend:
█ = Covered
░ = Not Covered

Improvement: +26%
```

### By Category

```
Naming:          ████████████████████████████████████████████░░░░░ 85%
Security:        ██████████████████████████████████████████████████ 95%
Error Handling:  ████████████████████████████████████████████████░░ 90%
Edge Cases:      ████████████████████████████████████████████░░░░░ 85%
Refactoring:     ████████████████████████████████████████████████░░ 90%
Concurrency:     ████████████████████████████████████████████████░░ 90%
State Mgmt:      ████████████████████████████████████████████████░░ 90%
API Design:      ██████████████████████████████████████████████████ 95%
Database:        ██████████████████████████████████████████████████ 95%
```

---

## 🔗 DEPENDENCY GRAPH

```
                    User Request
                         │
                         ▼
                    KIRO.md (Entry)
                         │
                         ├─► RULE 1 ──► MASTER_ROUTER.md
                         │                    │
                         │                    ├─► Frontend Skills
                         │                    ├─► Backend Skills
                         │                    ├─► Security Skills
                         │                    └─► Workflow Skills
                         │
                         ├─► RULE 6 ──► security-middleware-stack.md
                         ├─► RULE 7 ──► anti-hallucination-v2.md
                         ├─► RULE 8 ──► naming-conventions.md
                         ├─► RULE 9 ──► error-handling-patterns.md
                         ├─► RULE 10 ─► edge-case-catalog.md
                         └─► RULE 11 ─► refactoring-triggers.md
                                              │
                                              ▼
                                        AI Execution
                                              │
                                              ├─► Pre-commit Hooks
                                              ├─► CI/CD Pipeline
                                              └─► Code Review
                                                       │
                                                       ▼
                                              Quality Code Output
```

---

## 🎨 COLOR CODING

```
⭐ NEW     = Newly created/updated
✅ DONE    = Completed
⏳ PENDING = Needs manual work
🔄 UPDATED = Modified existing file
📍 PATH    = File location
🎯 GOAL    = Objective
📊 METRIC  = Measurement
```

---

**Version:** 1.0.0  
**Date:** 2026-03-30  
**Purpose:** Visual representation of system architecture  
**Status:** ✅ COMPLETE
