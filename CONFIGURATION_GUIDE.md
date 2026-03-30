# 🔧 HƯỚNG DẪN CẤU HÌNH ĐẦY ĐỦ - ANTIGRAVITY SYSTEM

> **Version:** 1.0.0  
> **Last Updated:** 2026-03-26  
> **Status:** ✅ Ollama Models Detected

---

## 📊 TÌNH TRẠNG HỆ THỐNG HIỆN TẠI

### ✅ Đã Cài Đặt
- **Ollama:** ✅ Đang chạy
- **Models đã tải:**
  - `smollm2:1.7b` (1.8 GB) - Model nhỏ, nhanh
  - `llama3.2:3b` (2.0 GB) - Model cân bằng
  - `qwen2.5:3b-instruct` (1.9 GB) - Model instruction-tuned

### ⚠️ Cần Cấu Hình
- LLM API Keys (Gemini, OpenAI, Anthropic)
- MCP Server Configuration
- Environment Variables
- Model Routing Rules

---

## 🎯 BƯỚC 1: CẤU HÌNH LLM API KEYS

### 1.1. Tạo File Environment Variables

Tạo file `.env` tại thư mục gốc project:

```bash
# .env
# ==========================================
# LLM API KEYS
# ==========================================

# Google Gemini API
GOOGLE_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-2.0-flash-exp

# OpenAI API (Optional)
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4o-mini

# Anthropic Claude API (Optional)
ANTHROPIC_API_KEY=your_anthropic_api_key_here
ANTHROPIC_MODEL=claude-3-5-sonnet-20241022

# ==========================================
# OLLAMA CONFIGURATION
# ==========================================
OLLAMA_HOST=http://localhost:11434
OLLAMA_DEFAULT_MODEL=llama3.2:3b

# ==========================================
# ROUTING CONFIGURATION
# ==========================================
# Complexity thresholds
SIMPLE_TASK_MODEL=smollm2:1.7b
MODERATE_TASK_MODEL=llama3.2:3b
COMPLEX_TASK_MODEL=qwen2.5:3b-instruct

# Fallback to cloud LLM if local fails
FALLBACK_TO_CLOUD=true
CLOUD_FALLBACK_MODEL=gemini-2.0-flash-exp

# ==========================================
# BUDGET & LIMITS
# ==========================================
MAX_TOKENS_PER_REQUEST=4096
DAILY_TOKEN_BUDGET=1000000
MAX_RETRIES=3
TIMEOUT_SECONDS=30
```

### 1.2. Lấy API Keys

#### Google Gemini API:
1. Truy cập: https://aistudio.google.com/app/apikey
2. Tạo API key mới
3. Copy và paste vào `GOOGLE_API_KEY`

#### OpenAI API (Optional):
1. Truy cập: https://platform.openai.com/api-keys
2. Tạo API key mới
3. Copy và paste vào `OPENAI_API_KEY`

#### Anthropic Claude API (Optional):
1. Truy cập: https://console.anthropic.com/settings/keys
2. Tạo API key mới
3. Copy và paste vào `ANTHROPIC_API_KEY`

---

## 🔌 BƯỚC 2: CẤU HÌNH MCP SERVER

### 2.1. Tạo File MCP Configuration

Tạo file `.kiro/settings/mcp.json`:

```json
{
  "mcpServers": {
    "ollama-local": {
      "command": "python",
      "args": ["-m", "antigravity.mcp.ollama_server"],
      "env": {
        "OLLAMA_HOST": "http://localhost:11434",
        "OLLAMA_MODELS": "smollm2:1.7b,llama3.2:3b,qwen2.5:3b-instruct"
      },
      "disabled": false,
      "autoApprove": ["list_models", "generate_text"]
    },
    "antigravity-core": {
      "command": "python",
      "args": ["-m", "antigravity.mcp.core_server"],
      "env": {
        "ANTIGRAVITY_DIR": "C:/Users/<YOUR_USERNAME>/.gemini/antigravity"
      },
      "disabled": false,
      "autoApprove": ["analyze_code", "route_task", "check_budget"]
    }
  }
}
```

### 2.2. Tạo User-Level MCP Config (Global)

Tạo file `~/.kiro/settings/mcp.json`:

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "uvx",
      "args": ["mcp-server-filesystem", "C:/Users/<YOUR_USERNAME>/.gemini"],
      "disabled": false,
      "autoApprove": ["read_file", "list_directory"]
    },
    "git": {
      "command": "uvx",
      "args": ["mcp-server-git"],
      "disabled": false,
      "autoApprove": ["git_status", "git_log"]
    }
  }
}
```

---

## 🧠 BƯỚC 3: CẤU HÌNH MODEL ROUTING

### 3.1. Kiểm Tra Models Ollama

```bash
# Kiểm tra models đã tải
ollama list

# Test model
ollama run llama3.2:3b "Hello, how are you?"
```

### 3.2. Tải Thêm Models (Optional)

```bash
# Models nhỏ cho routing nhanh
ollama pull phi3:mini          # 2.3GB - Microsoft Phi-3
ollama pull mistral:7b-instruct # 4.1GB - Mistral 7B

# Models lớn cho tasks phức tạp
ollama pull llama3.1:8b        # 4.7GB - Meta Llama 3.1
ollama pull qwen2.5:7b         # 4.7GB - Alibaba Qwen 2.5
```

### 3.3. Cấu Hình Routing Rules

Tạo file `antigravity/config/routing_rules.yaml`:

```yaml
# Model Routing Configuration
routing:
  # Simple tasks (< 100 tokens, basic queries)
  simple:
    primary: "smollm2:1.7b"
    fallback: "llama3.2:3b"
    max_tokens: 512
    temperature: 0.3
    
  # Moderate tasks (100-500 tokens, standard coding)
  moderate:
    primary: "llama3.2:3b"
    fallback: "qwen2.5:3b-instruct"
    max_tokens: 2048
    temperature: 0.5
    
  # Complex tasks (> 500 tokens, architecture, debugging)
  complex:
    primary: "qwen2.5:3b-instruct"
    fallback: "gemini-2.0-flash-exp"  # Cloud fallback
    max_tokens: 4096
    temperature: 0.7

# Task classification keywords
keywords:
  simple:
    - "hello"
    - "what is"
    - "define"
    - "list"
    - "show"
    
  moderate:
    - "create"
    - "write"
    - "implement"
    - "fix"
    - "update"
    
  complex:
    - "debug"
    - "architecture"
    - "refactor"
    - "optimize"
    - "design system"
```

---

## 🔍 BƯỚC 4: KIỂM TRA CẤU HÌNH

### 4.1. Test Ollama Connection

```python
# test_ollama.py
import subprocess
import json

def test_ollama():
    """Test Ollama connection and models."""
    
    # Check if Ollama is running
    try:
        result = subprocess.run(
            ["ollama", "list"],
            capture_output=True,
            text=True,
            timeout=5
        )
        print("✅ Ollama is running")
        print(result.stdout)
    except Exception as e:
        print(f"❌ Ollama error: {e}")
        return False
    
    # Test model inference
    models = ["smollm2:1.7b", "llama3.2:3b", "qwen2.5:3b-instruct"]
    
    for model in models:
        try:
            result = subprocess.run(
                ["ollama", "run", model, "Say 'OK' if you work"],
                capture_output=True,
                text=True,
                timeout=10
            )
            print(f"✅ {model}: {result.stdout.strip()}")
        except Exception as e:
            print(f"❌ {model} failed: {e}")
    
    return True

if __name__ == "__main__":
    test_ollama()
```

### 4.2. Test LLM API Keys

```python
# test_api_keys.py
import os
from dotenv import load_dotenv

load_dotenv()

def test_api_keys():
    """Test if API keys are configured."""
    
    keys = {
        "Google Gemini": os.getenv("GOOGLE_API_KEY"),
        "OpenAI": os.getenv("OPENAI_API_KEY"),
        "Anthropic": os.getenv("ANTHROPIC_API_KEY"),
    }
    
    for name, key in keys.items():
        if key and key != "your_*_api_key_here":
            print(f"✅ {name}: Configured")
        else:
            print(f"⚠️  {name}: Not configured")

if __name__ == "__main__":
    test_api_keys()
```

### 4.3. Test SLM Router

```bash
# Run benchmark
cd antigravity
python benchmarks/slm_routing_benchmark.py
```

---

## 🚀 BƯỚC 5: TÍCH HỢP VÀO WORKFLOW

### 5.1. Update llm_client.py

Thêm hỗ trợ Ollama vào `antigravity/core/llm_client.py`:

```python
def _detect_provider(self) -> str:
    """Detect LLM provider from model name."""
    model = self.model.lower()
    
    # Ollama models (local)
    if any(x in model for x in ["llama", "qwen", "smollm", "phi", "mistral"]):
        return "ollama"
    
    # Cloud providers
    if "gemini" in model or "palm" in model:
        return "google"
    elif "gpt" in model or "o1" in model:
        return "openai"
    elif "claude" in model:
        return "anthropic"
    
    return "unknown"
```

### 5.2. Tạo Ollama Client Wrapper

```python
# antigravity/core/ollama_client.py
import subprocess
from typing import Optional

class OllamaClient:
    """Client for local Ollama models."""
    
    def __init__(self, model: str, host: str = "http://localhost:11434"):
        self.model = model
        self.host = host
    
    def generate(self, prompt: str, max_tokens: int = 2048) -> str:
        """Generate text using Ollama."""
        try:
            result = subprocess.run(
                ["ollama", "run", self.model, prompt],
                capture_output=True,
                text=True,
                timeout=30
            )
            return result.stdout.strip()
        except Exception as e:
            raise RuntimeError(f"Ollama generation failed: {e}")
    
    def is_available(self) -> bool:
        """Check if Ollama is running."""
        try:
            subprocess.run(
                ["ollama", "list"],
                capture_output=True,
                timeout=5
            )
            return True
        except:
            return False
```

---

## 📝 BƯỚC 6: BEST PRACTICES

### 6.1. Token Budget Management

```python
# Ưu tiên local models để tiết kiệm chi phí
ROUTING_STRATEGY = {
    "default": "local_first",  # Try Ollama first
    "fallback": "cloud",       # Use cloud if local fails
    "budget_limit": 1_000_000, # Daily token limit
}
```

### 6.2. Model Selection Strategy

```
Simple Task (< 100 tokens):
  → smollm2:1.7b (local, fast, free)

Moderate Task (100-500 tokens):
  → llama3.2:3b (local, balanced)

Complex Task (> 500 tokens):
  → qwen2.5:3b-instruct (local, powerful)
  → gemini-2.0-flash-exp (cloud fallback)

Critical Task (architecture, security):
  → gemini-2.0-flash-thinking-exp (cloud, reasoning)
```

### 6.3. Error Handling

```python
def generate_with_fallback(prompt: str, complexity: str):
    """Generate with automatic fallback."""
    
    # Try local first
    try:
        local_model = get_local_model(complexity)
        return ollama_client.generate(prompt, model=local_model)
    except Exception as e:
        logger.warning(f"Local model failed: {e}")
    
    # Fallback to cloud
    try:
        cloud_model = get_cloud_model(complexity)
        return llm_client.generate(prompt, model=cloud_model)
    except Exception as e:
        logger.error(f"Cloud model failed: {e}")
        raise
```

---

## 🎯 CHECKLIST HOÀN THÀNH

- [ ] Tạo file `.env` với API keys
- [ ] Cấu hình `.kiro/settings/mcp.json`
- [ ] Test Ollama connection (`ollama list`)
- [ ] Test models (`python test_ollama.py`)
- [ ] Test API keys (`python test_api_keys.py`)
- [ ] Run SLM benchmark (`python benchmarks/slm_routing_benchmark.py`)
- [ ] Update `llm_client.py` với Ollama support
- [ ] Tạo `ollama_client.py` wrapper
- [ ] Test end-to-end workflow

---

## 🔗 TÀI LIỆU THAM KHẢO

- **Ollama Docs:** https://ollama.ai/docs
- **Gemini API:** https://ai.google.dev/docs
- **MCP Protocol:** https://modelcontextprotocol.io
- **Antigravity Skills:** `antigravity/skills/MASTER_ROUTER.md`

---

**Maintained by:** Antigravity System  
**Version:** 1.0.0  
**Last Updated:** 2026-03-26
