# 🤖 AGENT_AIDER — Aider CLI

[![Agent](https://img.shields.io/badge/Agent-Aider-red.svg)]()
[![Version](https://img.shields.io/badge/Rules-v6.2.0%20Solid--State-blue.svg)]()
[![Platform](https://img.shields.io/badge/Platform-Terminal%20%7C%20CLI-black.svg)]()

---

## 📋 Giới Thiệu

Thư mục này chứa **steering rules đã được scrubbed** dành cho **Aider** — AI pair programming tool chạy trực tiếp trên terminal, hỗ trợ Git-native workflow. Các rules này nhúng hệ thống trí tuệ **Antigravity Solid-State v6.2.0** vào mọi phiên làm việc.

---

## ⚙️ Cách Cài Đặt

### Option 1: `.aider.conf.yml` (khuyên dùng)
```yaml
# .aider.conf.yml trong project root
read: AIDER.md
```

### Option 2: Inline flag
```bash
aider --read AIDER.md --model claude-3-5-sonnet
```

### Option 3: Convention file
```bash
# Đổi tên thành CONVENTIONS.md và aider sẽ tự đọc
cp AIDER.md ./CONVENTIONS.md
```

---

## 📂 Nội Dung Thư Mục

| File | Mô Tả |
|------|-------|
| `AIDER.md` | Rules chính — nhúng Antigravity v6.2.0 |

---

## 🔑 Rules Cốt Lõi (Tóm Tắt)

1. **Load MASTER_ROUTER trước** mọi task
2. **Context Pruning** khi chuyển sang task mới
3. **Systematic Debugging** — không guess-and-check
4. **E2E Autonomous Loop** v6.2.0 — tự phát hiện và sửa lỗi
5. **Test trước khi báo hoàn thành**

---

## 💡 Tips Aider-Specific

- Aider tích hợp Git natively — kết hợp tốt với Antigravity's git workflow rules
- Dùng `--auto-commits` với caution — đảm bảo rules về Conventional Commits được tuân thủ
- Aider hoạt động tốt nhất với các file nhỏ, focused — theo đúng triết lý Context Pruning
- Kết hợp `/run` command để chạy test sau mỗi thay đổi (Test Before Claim Complete)

---

## 🌐 Liên Kết

- **Brain chung:** `../antigravity/skills/MASTER_ROUTER.md`
- **Core Rules:** `../ANTIGRAVITY_CORE_RULES.md`
- **Aider Docs:** https://aider.chat/docs

---

> **Version:** 6.2.0 (Solid-State) | **Last Updated:** 2026-03-26
