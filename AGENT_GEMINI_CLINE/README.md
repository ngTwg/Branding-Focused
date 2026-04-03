# 🤖 AGENT_GEMINI_CLINE — Gemini AI + Cline (Hybrid)

[![Agent](https://img.shields.io/badge/Agent-Gemini%20+%20Cline-green.svg)]()
[![Version](https://img.shields.io/badge/Rules-v6.2.0%20Solid--State-blue.svg)]()
[![Platform](https://img.shields.io/badge/Platform-Gemini%20CLI%20%7C%20Cline%20VSCode-green.svg)]()

---

## 📋 Giới Thiệu

Thư mục này chứa **rules đã được scrubbed** cho setup **Gemini AI (orchestrator) + Cline (executor)**. Cline hỗ trợ Gemini API và có **computer use** capabilities — kết hợp tốt với Gemini's planning để tạo ra autonomous coding workflow mạnh mẽ.

---

## ⚙️ Cấu Hình

```bash
# Cài đặt rules cho Cline
mkdir -p .cline/rules
cp CLINE.md .cline/rules/antigravity.md

# Trong Cline settings: chọn Gemini 2.5 Pro làm model
```

---

## 📂 Nội Dung Thư Mục

| File | Mô Tả |
|------|-------|
| `CLINE.md` | Rules cho Cline trong hybrid setup với Gemini |

---

## 💡 Tips

- Cline + Gemini = **autonomous computer use** với AI planning mạnh nhất
- Dùng Cline's **checkpoint** trước mỗi autonomous action để safe rollback
- Gemini 2.5 Pro + Cline là combo mạnh nhất cho Tier 3-4 tasks

---

> **Version:** 6.2.0 (Solid-State) | **Last Updated:** 2026-03-26
