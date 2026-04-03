# 🤖 AGENT_CONTINUE — Continue.dev (VSCode/JetBrains)

[![Agent](https://img.shields.io/badge/Agent-Continue.dev-blue.svg)]()
[![Version](https://img.shields.io/badge/Rules-v6.2.0%20Solid--State-blue.svg)]()
[![Platform](https://img.shields.io/badge/Platform-VSCode%20%7C%20JetBrains-blue.svg)]()

---

## 📋 Giới Thiệu

Thư mục này chứa **steering rules đã được scrubbed** dành cho **Continue.dev** — open-source AI coding assistant hỗ trợ VSCode và JetBrains, tích hợp với nhiều providers (Ollama, Claude, GPT, Gemini). Các rules này nhúng hệ thống trí tuệ **Antigravity Solid-State v6.2.0** vào mọi phiên làm việc.

---

## ⚙️ Cách Cài Đặt

### Config JSON
Thêm vào `~/.continue/config.json`:
```json
{
  "customCommands": [],
  "systemMessage": "// Paste nội dung CONTINUE.md vào đây"
}
```

### Hoặc dùng `rules` section trong config:
```json
{
  "rules": [
    "// Nội dung từ CONTINUE.md"
  ]
}
```

### Project-level Override
```bash
# Tạo file config trong project
mkdir -p .continue
# Thêm rules vào .continue/config.json
```

---

## 📂 Nội Dung Thư Mục

| File | Mô Tả |
|------|-------|
| `CONTINUE.md` | Rules chính — nhúng Antigravity v6.2.0 |

---

## 🔑 Rules Cốt Lõi (Tóm Tắt)

1. **Load MASTER_ROUTER trước** mọi task
2. **Context Pruning** khi chuyển sang task mới
3. **Systematic Debugging** — không guess-and-check
4. **E2E Autonomous Loop** v6.2.0 — tự phát hiện và sửa lỗi
5. **Test trước khi báo hoàn thành**

---

## 💡 Tips Continue-Specific

- Continue hỗ trợ **local models** qua Ollama — phù hợp với EU: Knowledge Distillation rules
- Dùng `@codebase` context để reference toàn bộ project khi apply rules
- Continue's **slash commands** có thể được customize để run MASTER_ROUTER workflow
- Kết hợp với **reranking** feature để tối ưu context retrieval

---

## 🌐 Liên Kết

- **Brain chung:** `../antigravity/skills/MASTER_ROUTER.md`
- **Core Rules:** `../ANTIGRAVITY_CORE_RULES.md`
- **Continue Docs:** https://docs.continue.dev

---

> **Version:** 6.2.0 (Solid-State) | **Last Updated:** 2026-03-26

