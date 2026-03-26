# 🤖 AGENT_CLAUDE — Claude Code / Claude Desktop

[![Agent](https://img.shields.io/badge/Agent-Claude-orange.svg)]()
[![Version](https://img.shields.io/badge/Rules-v6.2.0%20Solid--State-blue.svg)]()
[![Platform](https://img.shields.io/badge/Platform-Claude%20Desktop%20%7C%20Claude%20Code-purple.svg)]()

---

## 📋 Giới Thiệu

Thư mục này chứa **steering rules đã được scrubbed** (loại bỏ PII/credentials) dành cho **Claude Code** (CLI) và **Claude Desktop**. Các rules này nhúng hệ thống trí tuệ **Antigravity Solid-State v6.2.0** vào mọi phiên làm việc với Claude.

---

## ⚙️ Cách Cài Đặt

### Claude Desktop
```bash
# Copy vào đúng vị trí cấu hình
cp CLAUDE.md ~/.claude/CLAUDE.md

# Hoặc trên Windows
copy CLAUDE.md %USERPROFILE%\.claude\CLAUDE.md
```

### Claude Code (CLI)
```bash
# Thêm vào project root
cp CLAUDE.md ./CLAUDE.md

# Hoặc dùng --system-prompt flag
claude --system-prompt "$(cat CLAUDE.md)"
```

---

## 📂 Nội Dung Thư Mục

| File | Mô Tả |
|------|-------|
| `CLAUDE.md` | Rules chính — nhúng Antigravity v6.2.0 |

---

## 🔑 Rules Cốt Lõi (Tóm Tắt)

1. **Load MASTER_ROUTER trước** mọi task
2. **Context Pruning** khi chuyển sang task mới
3. **Systematic Debugging** — không guess-and-check
4. **E2E Autonomous Loop** — tự phát hiện và sửa lỗi
5. **Test trước khi báo hoàn thành**
6. **Git Persistence** — tự lưu và Discovery link.git
6. **Git Persistence** — tự lưu và Discovery link.git

---

## 🌐 Liên Kết

- **Brain chung:** `../antigravity/skills/MASTER_ROUTER.md`
- **Core Rules:** `../Antigravity_CORE_RULES.md`
- **Hướng dẫn skills:** `../SKILLS_GUIDE.md`

---

> **Version:** 6.2.0 (Solid-State) | **Last Updated:** 2026-03-26

