# 🤖 AGENT_COPILOT — GitHub Copilot

[![Agent](https://img.shields.io/badge/Agent-GitHub%20Copilot-black.svg)]()
[![Version](https://img.shields.io/badge/Rules-v6.2.0%20Solid--State-blue.svg)]()
[![Platform](https://img.shields.io/badge/Platform-GitHub%20%7C%20VSCode%20%7C%20JetBrains-darkblue.svg)]()

---

## 📋 Giới Thiệu

Thư mục này chứa **steering rules đã được scrubbed** dành cho **GitHub Copilot** — AI coding assistant của GitHub/Microsoft, tích hợp sâu với VSCode, JetBrains, và GitHub.com. Các rules này nhúng hệ thống trí tuệ **Antigravity Solid-State v6.2.0** vào mọi phiên làm việc.

---

## ⚙️ Cách Cài Đặt

### Option 1: Repository Instructions (khuyên dùng)
```bash
# Tạo file instructions cho Copilot
mkdir -p .github
cp COPILOT.md .github/copilot-instructions.md
```

Copilot sẽ tự động đọc `.github/copilot-instructions.md` trong mọi repository.

### Option 2: VSCode Settings
Thêm vào `.vscode/settings.json`:
```json
{
  "github.copilot.chat.codeGeneration.instructions": [
    {
      "file": "COPILOT.md"
    }
  ]
}
```

### Option 3: User-level Instructions
Trong VSCode → Copilot Settings → Custom Instructions → paste nội dung từ `COPILOT.md`.

---

## 📂 Nội Dung Thư Mục

| File | Mô Tả |
|------|-------|
| `COPILOT.md` | Rules chính — nhúng Antigravity v6.2.0 |

---

## 🔑 Rules Cốt Lõi (Tóm Tắt)

1. **Load MASTER_ROUTER trước** mọi task
2. **Context Pruning** khi chuyển sang task mới
3. **Systematic Debugging** — không guess-and-check
4. **E2E Autonomous Loop** v6.2.0 — tự phát hiện và sửa lỗi
5. **Test trước khi báo hoàn thành**

---

## 💡 Tips Copilot-Specific

- GitHub Copilot đọc `.github/copilot-instructions.md` tự động — setup một lần, chạy mãi
- Dùng **Copilot Chat** với `/explain` và `/fix` để trigger Systematic Debugging workflow
- Copilot **Workspace** agent hoạt động tốt nhất khi có đầy đủ context từ MASTER_ROUTER
- Kết hợp với **GitHub Actions** để chạy automated checks sau mỗi PR

---

## 🌐 Liên Kết

- **Brain chung:** `../antigravity/skills/MASTER_ROUTER.md`
- **Core Rules:** `../ANTIGRAVITY_CORE_RULES.md`
- **Copilot Docs:** https://docs.github.com/copilot

---

> **Version:** 6.2.0 (Solid-State) | **Last Updated:** 2026-03-26

