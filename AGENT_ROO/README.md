# 🤖 AGENT_ROO — Roo Code (VSCode Extension)

[![Agent](https://img.shields.io/badge/Agent-Roo%20Code-teal.svg)]()
[![Version](https://img.shields.io/badge/Rules-v6.2.0%20Solid--State-blue.svg)]()
[![Platform](https://img.shields.io/badge/Platform-VSCode%20Extension-blue.svg)]()

---

## 📋 Giới Thiệu

Thư mục này chứa **steering rules đã được scrubbed** dành cho **Roo Code** — VSCode extension AI agent mạnh mẽ hỗ trợ multi-model (Claude, GPT, Gemini, local models). Các rules này nhúng hệ thống trí tuệ **Antigravity Solid-State v6.2.0** vào mọi phiên làm việc.

---

## ⚙️ Cách Cài Đặt

### Option 1: Project-level Rules
```bash
# Tạo thư mục rules trong project
mkdir -p .roo/rules
cp ROO.md .roo/rules/antigravity.md
```

### Option 2: Roo Settings
Trong Roo Code → Settings → Custom Instructions → paste nội dung từ `ROO.md`.

### Option 3: Workspace Rules
```bash
# Global workspace rules
cp ROO.md ~/.config/roo/rules/antigravity.md
```

---

## 📂 Nội Dung Thư Mục

| File | Mô Tả |
|------|-------|
| `ROO.md` | Rules chính — nhúng Antigravity v6.2.0 |

---

## 🔑 Rules Cốt Lõi (Tóm Tắt)

1. **Load MASTER_ROUTER trước** mọi task
2. **Context Pruning** khi chuyển sang task mới
3. **Systematic Debugging** — không guess-and-check
4. **E2E Autonomous Loop** v6.2.0 — tự phát hiện và sửa lỗi
5. **Test trước khi báo hoàn thành**

---

## 💡 Tips Roo-Specific

- Roo Code hỗ trợ **multiple AI models** — chọn model phù hợp với Tier
- Dùng **Boomerang Tasks** để chia nhỏ task phức tạp
- Roo's **orchestrator mode** hoạt động tốt với Multi-Agent rules của Antigravity
- Kết hợp với **MCP servers** từ `antigravity/skills/deep-tech/mcp-builder/`

---

## 🌐 Liên Kết

- **Brain chung:** `../antigravity/skills/MASTER_ROUTER.md`
- **Core Rules:** `../ANTIGRAVITY_CORE_RULES.md`
- **Roo Docs:** https://roo.dev/docs

---

> **Version:** 6.2.0 (Solid-State) | **Last Updated:** 2026-03-26
