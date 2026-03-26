# Requirements: Antigravity Final Polish v6.3.0

> **Goal:** Hoàn thiện 3 mục còn thiếu để đạt 10/10
> **Timeline:** 2-3 tuần
> **Priority:** HIGH

---

## 🎯 OBJECTIVES

Dựa trên Architecture Review Progress Report, cần hoàn thành:

### 1. HybridRetriever Properties (CRITICAL - Phase 1 Final Safety)
**Priority:** P0 (BLOCKING Phase 2)
**Effort:** 2-3 hours
**Impact:** Prevents self-reinforcing wrong patterns

**Requirements:**
- Monotonicity: better match → not worse score
- Stability: small input change → small ranking change
- Filter correctness: confidence threshold predictable
- Diversity preservation: top-k không collapse

### 2. SLMRouter Properties (CRITICAL - Phase 1 Final Safety)
**Priority:** P0 (BLOCKING Phase 2)
**Effort:** 1 hour
**Impact:** Prevents cost explosion & quality degradation

**Requirements:**
- Budget respect: never exceed budget
- Quality degradation bounds: graceful tradeoff

### 3. Integration Test (CRITICAL - Phase 1 Final Safety)
**Priority:** P0 (BLOCKING Phase 2)
**Effort:** 1 hour
**Impact:** Proves learning convergence

**Requirements:**
- Pattern used → success → score increases
- System learns over time
- No silent regression

### 4. Tree-sitter Integration (HIGH PRIORITY)
**Priority:** P1
**Effort:** 1-2 days
**Impact:** Better code verification

**Requirements:**
- Parse Python/JS/TS AST
- Verify function signatures
- Check imports correctness
- Structured AST output (JSON schema)

### 5. SLM Model Benchmark (HIGH PRIORITY)
**Priority:** P1
**Effort:** 1 day
**Impact:** Optimize routing cost/quality

**Requirements:**
- Benchmark Qwen2.5-3B vs Llama-3.2-3B vs SmolLM2-1.7B
- Measure: accuracy, latency, cost
- Choose best model for routing

### 6. Reasoning Models Integration (MEDIUM PRIORITY)
**Priority:** P2
**Effort:** 2-3 days
**Impact:** Handle complex tasks better

**Requirements:**
- Integrate o1-mini/o3-mini for complex reasoning
- Cascading logic: simple → Sonnet, complex → o1
- Cost-aware routing

---

## 📋 SUCCESS CRITERIA

### Phase 1 Final Safety (P0):
- ✅ All HybridRetriever properties pass (100 runs)
- ✅ All SLMRouter properties pass (100 runs)
- ✅ Integration test shows learning convergence
- ✅ No flaky failures

### Production Readiness (P1):
- ✅ Tree-sitter integrated and tested
- ✅ SLM benchmark complete with recommendation
- ✅ All tests green

### Advanced Features (P2):
- ✅ Reasoning models integrated
- ✅ Cascading logic working
- ✅ Cost tracking accurate

---

## 🚫 NON-GOALS

- ❌ GraphRAG (over-engineering for 250 files)
- ❌ LangGraph migration (working code, don't refactor)
- ❌ SetFit classifier (need real data first)
- ❌ Synthetic data pipeline (need Langfuse data first)

---

## 📊 METRICS

### Before (v6.2.0):
- Property tests: 60% coverage
- Learning convergence: untested
- AST analysis: basic only
- SLM routing: not benchmarked

### After (v6.3.0):
- Property tests: 95% coverage
- Learning convergence: proven
- AST analysis: full Tree-sitter
- SLM routing: benchmarked & optimized

---

## 🔗 DEPENDENCIES

- Hypothesis (property testing)
- py-tree-sitter (AST parsing)
- Ollama (local SLM testing)
- pytest-benchmark (performance testing)

---

**Created:** 2026-03-26
**Owner:** Antigravity Team
**Status:** READY TO START
