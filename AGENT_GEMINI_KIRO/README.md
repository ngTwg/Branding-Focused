# 🤖 AGENT_GEMINI_KIRO — Gemini AI + Kiro (Hybrid)

[![Agent](https://img.shields.io/badge/Agent-Gemini%20+%20Kiro-yellow.svg)]()
[![Version](https://img.shields.io/badge/Rules-v6.2.0%20Solid--State-blue.svg)]()
[![Platform](https://img.shields.io/badge/Platform-Gemini%20CLI%20%7C%20Kiro%20IDE-orange.svg)]()

---

## 📋 Giới Thiệu

Thư mục này chứa **rules đã được scrubbed** cho setup **Gemini AI (orchestrator) + Kiro IDE (spec-driven executor)**. Kiro's spec-driven development kết hợp hoàn hảo với Gemini's planning capabilities. Gemini tạo high-level plan, Kiro chuyển thành spec và implement.

---

## ⚙️ Cấu Hình

```bash
# Kiro steering
mkdir -p .kiro/steering
cp KIRO.md .kiro/steering/antigravity.md
```

**Workflow:**
```
Gemini CLI → High-level plan
  ↓
Kiro → Chuyển thành spec (Requirements → Design → Tasks)
  ↓  
Kiro Agent → Implement từng task
  ↓
Gemini CLI → Review và verify
```

---

## 📂 Nội Dung Thư Mục

| File | Mô Tả |
|------|-------|
| `KIRO.md` | Rules cho Kiro trong hybrid setup |

---

## 💡 Tips

- Kiro's **spec-driven development** là cách triển khai tự nhiên nhất cho Antigravity's Plan-First principle
- Gemini 2.5 Pro cung cấp context rộng cho việc review toàn bộ codebase
- Kết hợp Kiro's **hooks** để tự động trigger Gemini review sau mỗi task

---

> **Version:** 6.2.0 (Solid-State) | **Last Updated:** 2026-03-26
