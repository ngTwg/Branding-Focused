# 🤖 AGENT_KIRO — Kiro IDE (Amazon)

[![Agent](https://img.shields.io/badge/Agent-Kiro-yellow.svg)]()
[![Version](https://img.shields.io/badge/Rules-v6.2.0%20Solid--State-blue.svg)]()
[![Platform](https://img.shields.io/badge/Platform-Kiro%20IDE%20(Amazon)-orange.svg)]()

---

## 📋 Giới Thiệu

Thư mục này chứa **steering rules đã được scrubbed** dành cho **Kiro IDE** — AI IDE mới nhất của Amazon, tích hợp sâu với AWS và các dịch vụ Amazon. Các rules này nhúng hệ thống trí tuệ **Antigravity Solid-State v6.2.0** vào mọi phiên làm việc.

---

## ⚙️ Cách Cài Đặt

### Kiro Steering Files
```bash
# Copy vào thư mục steering của project
mkdir -p .kiro/steering
cp KIRO.md .kiro/steering/antigravity.md
```

### Hoặc: Đặt là default steering
```bash
# Tạo file steering chính
cp KIRO.md .kiro/steering/KIRO.md
```

**Lưu ý:** Kiro đọc tất cả `.md` files trong `.kiro/steering/` và áp dụng vào mọi agent request.

---

## 📂 Nội Dung Thư Mục

| File | Mô Tả |
|------|-------|
| `KIRO.md` | Rules chính — nhúng Antigravity v6.2.0 |

---

## 🔑 Rules Cốt Lõi (Tóm Tắt)

1. **Load MASTER_ROUTER trước** mọi task
2. **Context Pruning** khi chuyển sang task mới
3. **Systematic Debugging** — không guess-and-check
4. **E2E Autonomous Loop** v6.2.0 — tự phát hiện và sửa lỗi
5. **Test trước khi báo hoàn thành**

---

## 💡 Tips Kiro-Specific

- Kiro hỗ trợ `spec-driven development` — kết hợp tốt với Tier system của Antigravity
- Dùng Kiro's "Vibe" mode để xây dựng từ spec, sau đó áp dụng rules để tối ưu
- Các steering files được load tự động cho mọi agent task trong workspace

---

## 🌐 Liên Kết

- **Brain chung:** `../antigravity/skills/MASTER_ROUTER.md`
- **Core Rules:** `../ANTIGRAVITY_CORE_RULES.md`
- **Kiro Docs:** https://kiro.dev/docs/steering/

---

> **Version:** 6.2.0 (Solid-State) | **Last Updated:** 2026-03-26

