# 🤖 AGENT_GEMINI_COPILOT — Gemini AI + GitHub Copilot (Hybrid)

[![Agent](https://img.shields.io/badge/Agent-Gemini%20+%20Copilot-black.svg)]()
[![Version](https://img.shields.io/badge/Rules-v6.2.0%20Solid--State-blue.svg)]()
[![Platform](https://img.shields.io/badge/Platform-Gemini%20CLI%20%7C%20GitHub%20Copilot-darkblue.svg)]()

---

## 📋 Giới Thiệu

Thư mục này chứa **rules đã được scrubbed** cho setup **Gemini AI (planning/review) + GitHub Copilot (inline completion)**. Đây là setup lý tưởng cho developers dùng Copilot hàng ngày nhưng muốn bổ sung planning capability từ Gemini.

---

## ⚙️ Cấu Hình

```bash
# Copilot instructions — đặt vào repo
mkdir -p .github
cp COPILOT.md .github/copilot-instructions.md
```

**Workflow:**
1. Dùng Gemini CLI để lập kế hoạch và tạo spec
2. Copilot tự động hoàn thiện code theo spec
3. Gemini review kết quả cuối

---

## 📂 Nội Dung Thư Mục

| File | Mô Tả |
|------|-------|
| `COPILOT.md` | Rules cho Copilot trong hybrid setup |

---

## 💡 Tips

- Copilot rất mạnh ở **inline completion** — để Gemini xử lý phần "what to build"
- Dùng Copilot Chat với context từ Gemini's plan
- `.github/copilot-instructions.md` áp dụng cho toàn bộ repo tự động

---

> **Version:** 6.2.0 (Solid-State) | **Last Updated:** 2026-03-26
