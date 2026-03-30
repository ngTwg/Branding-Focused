# 🚀 QUICK START - ANTIGRAVITY SYSTEM

> **Thời gian:** 10 phút  
> **Mục tiêu:** Cấu hình và chạy hệ thống ngay lập tức

---

## ✅ TÌNH TRẠNG HIỆN TẠI

### Đã Sẵn Sàng:
- ✅ **Ollama:** Đang chạy
- ✅ **Models hoạt động:**
  - `smollm2:1.7b` - Nhanh, nhẹ (1.8 GB)
  - `qwen2.5:3b-instruct` - Mạnh, instruction-tuned (1.9 GB)
- ⚠️  **llama3.2:3b** - Cần nhiều RAM hơn (tạm thời không dùng)

### Cần Làm:
- [ ] Cấu hình API keys
- [ ] Test API connections
- [ ] Cấu hình MCP servers
- [ ] Chạy benchmark

---

## 🎯 BƯỚC 1: CẤU HÌNH NHANH (2 phút)

### Option A: Tự động (Khuyến nghị)

```bash
# Chạy wizard tự động
python setup_config.py
```

Wizard sẽ hỏi bạn từng bước và tạo file cấu hình.

### Option B: Thủ công

```bash
# Copy template
cp .env.example .env

# Mở và chỉnh sửa
notepad .env
```

Thêm API key của bạn vào file `.env`:

```env
# Ít nhất cần 1 trong 3:
GOOGLE_API_KEY=AIza...your_key_here
OPENAI_API_KEY=sk-...your_key_here
ANTHROPIC_API_KEY=sk-ant-...your_key_here
```

---

## 🧪 BƯỚC 2: KIỂM TRA (3 phút)

### Test 1: Ollama Models

```bash
python test_ollama.py
```

**Kết quả mong đợi:**
```
✅ Working models: 2/3
   • smollm2:1.7b
   • qwen2.5:3b-instruct
```

### Test 2: API Keys

```bash
python test_api_keys.py
```

**Kết quả mong đợi:**
```
✅ Google Gemini: Configured
✅ Configured API keys: 1/3
```

### Test 3: Routing Benchmark

```bash
cd antigravity
python benchmarks/slm_routing_benchmark.py
```

**Kết quả mong đợi:**
```
Testing smollm2:1.7b...
Accuracy: 85%
Avg latency: 1.2s
```

---

## 🔧 BƯỚC 3: CẤU HÌNH MCP (2 phút)

### Tạo MCP Config

```bash
# Tạo thư mục
mkdir -p .kiro/settings

# Tạo file config
notepad .kiro/settings/mcp.json
```

Paste nội dung sau:

```json
{
  "mcpServers": {
    "ollama-local": {
      "command": "python",
      "args": ["-m", "antigravity.mcp.ollama_server"],
      "env": {
        "OLLAMA_HOST": "http://localhost:11434",
        "OLLAMA_MODELS": "smollm2:1.7b,qwen2.5:3b-instruct"
      },
      "disabled": false,
      "autoApprove": ["list_models", "generate_text"]
    }
  }
}
```

---

## 🎮 BƯỚC 4: SỬ DỤNG (3 phút)

### Test Routing Thực Tế

Tạo file `test_routing.py`:

```python
from antigravity.core.slm_router import SLMRouter

# Khởi tạo router
router = SLMRouter()

# Test các queries
queries = [
    "What is Python?",                    # Simple
    "Write a function to sort array",     # Moderate
    "Debug this complex async code",      # Complex
]

for query in queries:
    decision = router.classify(query)
    print(f"\nQuery: {query}")
    print(f"Model: {decision.model}")
    print(f"Complexity: {decision.complexity}")
    print(f"Confidence: {decision.confidence:.2f}")
```

Chạy:

```bash
python test_routing.py
```

**Kết quả mong đợi:**
```
Query: What is Python?
Model: smollm2:1.7b
Complexity: simple
Confidence: 0.92

Query: Write a function to sort array
Model: qwen2.5:3b-instruct
Complexity: moderate
Confidence: 0.85
```

---

## 💡 TIPS & TRICKS

### 1. Tiết Kiệm RAM

Nếu RAM không đủ cho `llama3.2:3b`, dùng models nhỏ hơn:

```bash
# Unload model lớn
ollama stop llama3.2:3b

# Hoặc pull model nhỏ hơn
ollama pull phi3:mini  # Chỉ 2.3GB
```

### 2. Tối Ưu Routing

Chỉnh sửa `.env`:

```env
# Ưu tiên model nhanh cho simple tasks
SIMPLE_TASK_MODEL=smollm2:1.7b

# Dùng model mạnh cho complex tasks
COMPLEX_TASK_MODEL=qwen2.5:3b-instruct

# Fallback sang cloud nếu local fail
FALLBACK_TO_CLOUD=true
CLOUD_FALLBACK_MODEL=gemini-2.0-flash-exp
```

### 3. Debug Mode

Bật debug để xem chi tiết:

```env
LOG_LEVEL=DEBUG
DEBUG_MODE=true
TRACE_ENABLED=true
```

### 4. Kiểm Tra Token Usage

```python
from antigravity.core.budget_guard import BudgetGuard

guard = BudgetGuard(daily_limit=1_000_000)
print(f"Used today: {guard.get_usage()}")
print(f"Remaining: {guard.get_remaining()}")
```

---

## 🚨 TROUBLESHOOTING

### Problem: Ollama không chạy

```bash
# Windows
ollama serve

# Hoặc restart service
```

### Problem: Model out of memory

```bash
# Giảm context window
ollama run smollm2:1.7b --ctx-size 2048

# Hoặc dùng model nhỏ hơn
ollama pull tinyllama  # Chỉ 637MB
```

### Problem: API key không hoạt động

```bash
# Test trực tiếp
python -c "import os; print(os.getenv('GOOGLE_API_KEY'))"

# Reload environment
source .env  # Linux/Mac
# Hoặc restart terminal trên Windows
```

### Problem: Import error

```bash
# Cài đặt dependencies
pip install -r requirements.txt

# Hoặc cài từng package
pip install google-generativeai openai anthropic
```

---

## 📊 CHECKLIST HOÀN THÀNH

- [ ] ✅ Ollama đang chạy
- [ ] ✅ Ít nhất 2 models hoạt động
- [ ] ✅ File `.env` đã tạo với API key
- [ ] ✅ Test API keys pass
- [ ] ✅ MCP config đã tạo
- [ ] ✅ Routing benchmark chạy thành công
- [ ] ✅ Test routing thực tế hoạt động

---

## 🎉 HOÀN THÀNH!

Bạn đã sẵn sàng sử dụng Antigravity System với:

- **Local Models:** smollm2:1.7b, qwen2.5:3b-instruct
- **Cloud Fallback:** Gemini/OpenAI/Claude
- **Smart Routing:** Tự động chọn model phù hợp
- **Budget Control:** Giới hạn token usage

### Next Steps:

1. **Đọc docs:** `CONFIGURATION_GUIDE.md`
2. **Xem skills:** `antigravity/skills/MASTER_ROUTER.md`
3. **Chạy examples:** `antigravity/examples/`
4. **Join community:** GitHub Issues

---

**Happy Coding! 🚀**
