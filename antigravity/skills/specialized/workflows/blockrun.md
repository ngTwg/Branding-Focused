---
name: "blockrun"
tags: ["antigravity", "blockrun", "c:", "capability", "extensions", "gemini", "generation", "governance", "image", "implementation", "<YOUR_USERNAME>", "llm", "philosophy", "real", "sdk", "search", "slim", "specialized", "time", "twitter"]
tier: 3
risk: "medium"
estimated_tokens: 481
tools_needed: ["markdown", "terminal"]
applies_to_agents: ["cursor", "claude", "copilot", "cline", "continue", "kiro", "roo"]
industry: ["engineering", "productivity"]
quality_score: 0.69
allowed-tools: "Read, Bash(python:*), Bash(python3:*), Bash(pip:*), Bash(source:*)"
description: "Use when user needs capabilities Claude lacks (image generation, real-time X/Twitter data) or explicitly requests external models (\"blockrun\", \"use grok\", \"use gpt\", \"dall-e\", \"deepseek\")"
---
# BlockRun - AI Capability Extensions (v6.5.0-SLIM)

BlockRun provides real-time access to X/Twitter, image generation, and secondary model opinions (GPT, Grok, DeepSeek) through an autonomous micropayment system.

## Philosophy
You lack certain native capabilities (DALL-E, live X/Twitter). BlockRun gives you a wallet to "pay" for what you're missing autonomously via x402 micropayments.

| Capability | Model | Pricing |
|-----------|-------|---------|
| Image generation | DALL-E | $0.04/image |
| Real-time X data | Grok + Live Search | $0.025/source |
| Critical Reasoning | GPT-5.2 | $1.75/M input, $14/M output |
| Efficient Processing | DeepSeek | $0.14/M input, $0.28/M output |

## Governance
- **Budget Control:** Track spending against a user-defined budget. Stop if threshold reached.
- **When to Use:**
  - Explicit user request ("use Grok", "generate image").
  - Suggest when native tools are insufficient (images, live social data).
  - Don't mention BlockRun for everyday tasks.

## SDK Implementation (blockrun-llm)
```python
from blockrun_llm import setup_agent_wallet
client = setup_agent_wallet()

# Real-time X/Twitter search
response = client.chat("xai/grok-3", "What's trending?", search=True)

# Image generation
from blockrun_llm import ImageClient
result = ImageClient().generate("A minimalist tech logo")

# Wallet monitoring
balance = client.get_balance()
```

## Model Selection (v2025)
- `xai/grok-3`: Real-time X/web data.
- `openai/gpt-5-mini`: Cost-optimized reasoning.
- `openai/o3`: Advanced reasoning for complex problems.
- `google/nano-banana`: Fast, low-cost artistic images.
