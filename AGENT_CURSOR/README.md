# 🤖 AGENT_CURSOR — Cursor IDE

[![Agent](https://img.shields.io/badge/Agent-Cursor-blue.svg)]()
[![Version](https://img.shields.io/badge/Rules-v6.2.0%20Solid--State-blue.svg)]()
[![Platform](https://img.shields.io/badge/Platform-Cursor%20IDE-darkblue.svg)]()

---

## 📋 Giới Thiệu

Thư mục này chứa **steering rules đã được scrubbed** dành cho **Cursor IDE**. Cursor là AI code editor tích hợp GPT-4/Claude. Các rules này nhúng hệ thống trí tuệ **Antigravity Solid-State v6.2.0** vào mọi phiên làm việc.

---

## ⚙️ Cách Cài Đặt

### Option 1: Project-level (khuyên dùng)
```bash
# Copy vào root của project
cp CURSOR.md ./.cursorrules
```

### Option 2: Global (áp dụng cho mọi project)
```bash
# Copy vào thư mục cấu hình Cursor
cp CURSOR.md ~/.cursor/rules/CURSOR.md
```

### Option 3: Cursor Settings UI
Dùng **Cursor Settings → Rules for AI → Add global rule** và paste nội dung từ `CURSOR.md`.

---

## 📂 Nội Dung Thư Mục

| File | Mô Tả |
|------|-------|
| `CURSOR.md` | Rules chính — nhúng Antigravity v6.2.0 |

---

## 🔑 Rules Cốt Lõi (Tóm Tắt)

1. **Load MASTER_ROUTER trước** mọi task
2. **Context Pruning** khi chuyển sang task mới
3. **Systematic Debugging** — không guess-and-check
4. **E2E Autonomous Loop** v6.2.0 — tự phát hiện và sửa lỗi
5. **Test trước khi báo hoàn thành**

---

## 💡 Tips Cursor-Specific

- Sử dụng `@file` để reference `antigravity/skills/MASTER_ROUTER.md` trong chat
- Dùng `.cursorrules` ở project level để override global rules nếu cần
- Composer mode hoạt động tốt nhất với rules này

---

## 🌐 Liên Kết

- **Brain chung:** `../antigravity/skills/MASTER_ROUTER.md`
- **Core Rules:** `../ANTIGRAVITY_CORE_RULES.md`

---

> **Version:** 6.2.0 (Solid-State) | **Last Updated:** 2026-03-26

