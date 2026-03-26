# 🤖 AGENT_AGENTS — OpenAI Agents SDK / Generic Agents

[![Agent](https://img.shields.io/badge/Agent-OpenAI%20Agents%20SDK-green.svg)]()
[![Version](https://img.shields.io/badge/Rules-v6.2.0%20Solid--State-blue.svg)]()
[![Platform](https://img.shields.io/badge/Platform-OpenAI%20%7C%20Generic%20Agents-purple.svg)]()

---

## 📋 Giới Thiệu

Thư mục này chứa **steering rules đã được scrubbed** dành cho **OpenAI Agents SDK** và **generic AI agents** tuân theo chuẩn `AGENTS.md`. Chuẩn `AGENTS.md` được nhiều frameworks nhận diện tự động. Các rules này nhúng hệ thống trí tuệ **Antigravity Solid-State v6.2.0** vào mọi phiên chạy agent.

---

## ⚙️ Cách Cài Đặt

### OpenAI Agents SDK
```bash
# Đặt AGENTS.md ở root project
cp AGENTS.md ./AGENTS.md
```

OpenAI Agents SDK và nhiều frameworks tự động đọc `AGENTS.md` nếu có trong project root.

### Generic Agent Framework
```python
# Python example — load rules vào system prompt
with open("AGENTS.md", "r") as f:
    rules = f.read()

agent = Agent(
    name="MyAgent",
    instructions=rules,
    model="gpt-4o"  # hoặc claude-3-5-sonnet, gemini-2.5-pro...
)
```

### Codex / Custom Agent
```bash
# Bất kỳ agent nào đọc AGENTS.md theo convention
cp AGENTS.md ./AGENTS.md
```

---

## 📂 Nội Dung Thư Mục

| File | Mô Tả |
|------|-------|
| `AGENTS.md` | Rules chính — nhúng Antigravity v6.2.0, theo chuẩn AGENTS.md |

---

## 🔑 Rules Cốt Lõi (Tóm Tắt)

1. **Load MASTER_ROUTER trước** mọi task
2. **Context Pruning** khi chuyển sang task mới
3. **Systematic Debugging** — không guess-and-check
4. **E2E Autonomous Loop** v6.2.0 — tự phát hiện và sửa lỗi
5. **Test trước khi báo hoàn thành**
6. **Git Persistence** — tự lưu và Discovery link.git
6. **Git Persistence** — tự lưu và Discovery link.git
6. **Multi-Agent Orchestration** — Orchestrator + Subagents pattern

---

## 💡 Tips Agents-Specific

- `AGENTS.md` convention được hỗ trợ bởi: OpenAI Codex, Devin, SWE-agent, và nhiều frameworks
- Kết hợp với **Handoffs** trong OpenAI Agents SDK để phân công task giữa các agents
- Antigravity's **EN: Multi-Agent Swarm** rules được thiết kế đặc biệt cho pattern này
- Dùng **Guardrails** để enforce các AFC (AI Safety) rules từ nhóm H

---

## 🌐 Liên Kết

- **Brain chung:** `../antigravity/skills/MASTER_ROUTER.md`
- **Core Rules:** `../Antigravity_CORE_RULES.md`
- **OpenAI Agents SDK:** https://openai.github.io/openai-agents-python/

---

> **Version:** 6.2.0 (Solid-State) | **Last Updated:** 2026-03-26

