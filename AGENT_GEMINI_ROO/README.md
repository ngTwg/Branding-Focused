# 🤖 AGENT_GEMINI_ROO — Gemini AI + Roo Code (Hybrid)

[![Agent](https://img.shields.io/badge/Agent-Gemini%20+%20Roo-teal.svg)]()
[![Version](https://img.shields.io/badge/Rules-v6.2.0%20Solid--State-blue.svg)]()
[![Platform](https://img.shields.io/badge/Platform-Gemini%20CLI%20%7C%20Roo%20Code-teal.svg)]()

---

## 📋 Giới Thiệu

Thư mục này chứa **rules đã được scrubbed** cho setup **Gemini AI (orchestrator) + Roo Code (executor)**. Roo Code hỗ trợ Gemini API trực tiếp — đây là setup mạnh mẽ vì cả hai chia sẻ cùng một brain nhưng Roo Code có thêm computer use và autonomous execution capabilities.

---

## ⚙️ Cấu Hình

```bash
# Roo Code — set model = Gemini 2.5 Pro trong settings
# Áp dụng rules vào Roo
mkdir -p .roo/rules
cp ROO.md .roo/rules/antigravity.md
```

---

## 📂 Nội Dung Thư Mục

| File | Mô Tả |
|------|-------|
| `ROO.md` | Rules cho Roo trong hybrid setup với Gemini |

---

## 💡 Tips

- Roo có thể dùng **Gemini model trực tiếp** — single-brain, double-capability
- Roo's **orchestrator mode** + Gemini = perfect multi-agent setup
- Kết hợp với Gemini CLI cho planning, Roo cho execution

---

> **Version:** 6.2.0 (Solid-State) | **Last Updated:** 2026-03-26
