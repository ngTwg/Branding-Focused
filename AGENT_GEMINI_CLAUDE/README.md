# 🤖 AGENT_GEMINI_CLAUDE — Gemini AI + Claude (Hybrid)

[![Agent](https://img.shields.io/badge/Agent-Gemini%20+%20Claude-orange.svg)]()
[![Version](https://img.shields.io/badge/Rules-v6.2.0%20Solid--State-blue.svg)]()
[![Platform](https://img.shields.io/badge/Platform-Gemini%20CLI%20%7C%20Claude%20Code-purple.svg)]()

---

## 📋 Giới Thiệu

Thư mục này chứa **steering rules đã được scrubbed** cho setup **Gemini AI (chính) + Claude (reviewer/executor)**. Đây là cấu hình **Cross-Model Validation** tối ưu — Gemini lập kế hoạch và điều phối, Claude thực thi và review.

Theo quy tắc `FE: MODEL COLLAPSE & DATA POISONING` — dùng **2 models khác nhau** giúp giảm điểm mù và ngăn chặn AI hallucination.

---

## ⚙️ Cấu Hình Setup

### Cách hoạt động của Hybrid Setup
```
Gemini (Planner/Orchestrator)
  ↓ viết spec & plan
Claude (Executor/Reviewer)
  ↓ implement & review
Gemini (Verifier)
  ↓ xác nhận quality
```

### Cài đặt
```bash
# 1. Gemini CLI — áp dụng rules gốc
# Rules được inject vào Gemini qua GEMINI.md ở home directory

# 2. Claude Code — áp dụng rules review
cp CLAUDE.md ~/.claude/CLAUDE.md
```

---

## 📂 Nội Dung Thư Mục

| File | Mô Tả |
|------|-------|
| `CLAUDE.md` | Rules cho Claude trong hybrid setup — bao gồm reviewer role |

---

## 🔑 Rules Cốt Lõi

**Gemini (Planner)**
- Load MASTER_ROUTER, phân tích task, tạo plan
- Inject plan vào Claude prompt

**Claude (Executor + Reviewer)**  
- Thực thi plan từ Gemini
- Self-audit kết quả trước khi return
- Report issues ngược lại Gemini nếu plan có lỗi

---

## 💡 Tips Hybrid-Specific

- Setup này phù hợp với **Tier 3-4** tasks cần high accuracy
- Dùng Google AI Studio + Claude Desktop chạy song song
- Gemini 2.5 Pro có **1M token context** — lý tưởng cho Orchestrator role
- Claude 3.5 Sonnet có **strong coding** — lý tưởng cho Executor role

---

> **Version:** 6.2.0 (Solid-State) | **Last Updated:** 2026-03-26
