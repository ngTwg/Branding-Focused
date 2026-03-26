# 🤖 AGENT_CLINE — Cline (VSCode Extension)

[![Agent](https://img.shields.io/badge/Agent-Cline-green.svg)]()
[![Version](https://img.shields.io/badge/Rules-v6.2.0%20Solid--State-blue.svg)]()
[![Platform](https://img.shields.io/badge/Platform-VSCode%20Extension-blue.svg)]()

---

## 📋 Giới Thiệu

Thư mục này chứa **steering rules đã được scrubbed** dành cho **Cline** (formerly Claude Dev) — VSCode extension AI agent hỗ trợ autonomous coding với computer use capabilities. Các rules này nhúng hệ thống trí tuệ **Antigravity Solid-State v6.2.0** vào mọi phiên làm việc.

---

## ⚙️ Cách Cài Đặt

### Option 1: Project-level Rules (khuyên dùng)
```bash
# Tạo thư mục rules trong project
mkdir -p .cline/rules
cp CLINE.md .cline/rules/antigravity.md
```

### Option 2: Cline Custom Instructions
Trong Cline → Settings → Custom Instructions → paste nội dung từ `CLINE.md`.

### Option 3: `.clinerules` file
```bash
# Tạo file rules ở root project
cp CLINE.md ./.clinerules
```

---

## 📂 Nội Dung Thư Mục

| File | Mô Tả |
|------|-------|
| `CLINE.md` | Rules chính — nhúng Antigravity v6.2.0 |

---

## 🔑 Rules Cốt Lõi (Tóm Tắt)

1. **Load MASTER_ROUTER trước** mọi task
2. **Context Pruning** khi chuyển sang task mới
3. **Systematic Debugging** — không guess-and-check
4. **E2E Autonomous Loop** v6.2.0 — tự phát hiện và sửa lỗi
5. **Test trước khi báo hoàn thành**
6. **Git Persistence** — tự lưu và Discovery link.git
6. **Git Persistence** — tự lưu và Discovery link.git

---

## 💡 Tips Cline-Specific

- Cline có **computer use** capabilities — Antigravity's EQ rules (Computer Use & Visual Cognition) phát huy tác dụng tối đa
- Dùng **checkpoint** feature để save state trước khi chạy autonomous loops
- Kết hợp với **MCP servers** từ `antigravity/skills/deep-tech/mcp-builder/` để mở rộng khả năng
- Cline hỗ trợ nhiều models — chọn Claude 3.5 Sonnet/Gemini 2.5 Pro cho task phức tạp

---

## 🌐 Liên Kết

- **Brain chung:** `../antigravity/skills/MASTER_ROUTER.md`
- **Core Rules:** `../Antigravity_CORE_RULES.md`
- **Cline Docs:** https://github.com/cline/cline

---

> **Version:** 6.2.0 (Solid-State) | **Last Updated:** 2026-03-26

