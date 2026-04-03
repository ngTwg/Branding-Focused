# 🤖 AGENT_GEMINI_CURSOR — Gemini AI + Cursor (Hybrid)

[![Agent](https://img.shields.io/badge/Agent-Gemini%20+%20Cursor-blue.svg)]()
[![Version](https://img.shields.io/badge/Rules-v6.2.0%20Solid--State-blue.svg)]()
[![Platform](https://img.shields.io/badge/Platform-Gemini%20CLI%20%7C%20Cursor%20IDE-darkblue.svg)]()

---

## 📋 Giới Thiệu

Thư mục này chứa **steering rules đã được scrubbed** cho setup **Gemini AI (orchestrator) + Cursor IDE (executor)**. Gemini chạy qua CLI/API để lập kế hoạch và điều phối, Cursor IDE được dùng để implement và refactor code với sự hỗ trợ AI trong IDE.

---

## ⚙️ Cấu Hình Setup

### Workflow Hybrid
```
Gemini CLI (Planning)
  ↓ tạo spec/plan chi tiết
Cursor IDE (Implementation)
  ↓ Composer/Agent mode implement
Gemini CLI (Verification)
  ↓ review kết quả cuối
```

### Cài đặt
```bash
# 1. Cursor — áp dụng rules
cp CURSOR.md ./.cursorrules

# 2. Gemini CLI — dùng home GEMINI.md
# (đã được cài sẵn ở ~/.gemini/GEMINI.md)
```

---

## 📂 Nội Dung Thư Mục

| File | Mô Tả |
|------|-------|
| `CURSOR.md` | Rules cho Cursor trong hybrid setup |

---

## 💡 Tips Gemini+Cursor Hybrid

- **Gemini 2.5 Pro** với 1M token context: load toàn bộ codebase để phân tích
- **Cursor Composer**: implement code theo plan từ Gemini
- Dùng `@file` trong Cursor để reference files được Gemini đề xuất
- Gemini CLI (`gemini`) + Cursor IDE chạy song song trong 2 terminal/window

---

> **Version:** 6.2.0 (Solid-State) | **Last Updated:** 2026-03-26
