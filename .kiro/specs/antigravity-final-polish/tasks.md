# Tasks: Antigravity Final Polish v6.3.0

> **Sprint:** 2-3 tuần
> **Focus:** Phase 1 Final Safety → Production Readiness

---

## 🚨 PHASE 1 FINAL SAFETY (P0 - BLOCKING)

### Task 1: HybridRetriever Properties ✅ COMPLETE
**Priority:** P0
**Effort:** 2 hours (actual)
**Blocking:** Phase 2 evolution

**Subtasks:**
- [x] 1.1: Property P1 - Monotonicity ✅
  - [x] Write Hypothesis test: results sorted by score
  - [x] Test with 50 random queries
  - [x] PASS - No violations

- [x] 1.2: Property P2 - Determinism ✅
  - [x] Write Hypothesis test: same query → same results
  - [x] Test score identity (< 1e-6 difference)
  - [x] PASS - Perfect determinism

- [x] 1.3: Property P3 - Top-k Correctness ✅
  - [x] Write Hypothesis test: returns at most top_k
  - [x] Test with k=1 to k=10
  - [x] PASS - Always respects limit

- [x] 1.4: Property P4 - Score Bounds ✅
  - [x] Write Hypothesis test: all scores in [0,1]
  - [x] Test bm25_norm, cosine_norm, final_score
  - [x] PASS - All normalized

- [x] 1.5: Property P5 - Non-empty Results ✅
  - [x] Test reasonable queries return results
  - [x] PASS - Never empty

- [x] 1.6: Property P6 - Domain Filter ✅
  - [x] Test domain filtering works
  - [x] PASS - Correct filtering

- [x] 1.7: Integration Test ✅
  - [x] All properties together
  - [x] PASS - System coherent

**Files:**
- `antigravity/tests/test_hybrid_retriever_properties_v2.py` (NEW - 350 lines)
- `antigravity/docs/TASK1_HYBRID_RETRIEVER_PROPERTIES_COMPLETE.md` (NEW)

**Results:**
- ✅ 10/10 tests passing
- ✅ 50-100 examples per property
- ✅ No flaky failures
- ✅ Execution time: 1.27s
- ✅ **PHASE 2 UNBLOCKED**

---

### Task 2: SLMRouter Properties ⏳ TODO
**Priority:** P0
**Effort:** 1 hour
**Blocking:** Phase 2 evolution

**Subtasks:**
- [x] 2.1: Property P1 - Budget Respect
  - [ ] Write Hypothesis test: never exceed budget
  - [ ] Test with various budget constraints
  - [ ] Verify estimated_cost <= budget

- [x] 2.2: Property P2 - Quality Degradation Bounds
  - [ ] Write Hypothesis test: graceful quality tradeoff
  - [ ] Budget cut 50% → quality drop < 30%
  - [ ] No catastrophic collapse

**Files:**
- `antigravity/tests/test_slm_router_properties.py` (NEW)
- `antigravity/core/slm_router.py` (UPDATE)

**Acceptance:**
- ✅ Both properties pass 100 runs
- ✅ Budget never exceeded
- ✅ Quality degradation predictable

---

### Task 3: Integration Test - Learning Convergence ⏳ TODO
**Priority:** P0
**Effort:** 1 hour
**Blocking:** Phase 2 evolution

**Subtasks:**
- [x] 3.1: Setup test environment
  - [ ] Generate random patterns
  - [ ] Create test tasks
  - [ ] Mock feedback system

- [x] 3.2: Test learning loop
  - [ ] Run 5 tasks with feedback
  - [ ] Track pattern rankings
  - [ ] Verify successful patterns move up

- [x] 3.3: Test convergence
  - [ ] Run 20 iterations
  - [ ] Verify rankings stabilize
  - [ ] Ensure no regression

**Files:**
- `antigravity/tests/integration/test_learning_convergence.py` (NEW)

**Acceptance:**
- ✅ Successful patterns rank higher after feedback
- ✅ System converges within 20 iterations
- ✅ No silent regression

---

## 🔧 PRODUCTION READINESS (P1)

### Task 4: Tree-sitter Integration ⏳ TODO
**Priority:** P1
**Effort:** 1-2 days
**Impact:** Better code verification

**Subtasks:**
- [x] 4.1: Install dependencies
  - [ ] `pip install tree-sitter tree-sitter-python tree-sitter-javascript`
  - [ ] Build language parsers
  - [ ] Test basic parsing

- [x] 4.2: Create ASTAnalyzer
  - [ ] Parse Python code
  - [ ] Parse JavaScript/TypeScript code
  - [ ] Extract function signatures
  - [ ] Extract imports

- [x] 4.3: Integrate with Checker
  - [ ] Add `verify_python_ast()` method
  - [ ] Add `verify_js_ast()` method
  - [ ] Structured JSON output

- [x] 4.4: Write tests
  - [ ] Test valid code parsing
  - [ ] Test invalid code detection
  - [ ] Test edge cases

**Files:**
- `antigravity/core/ast_analyzer.py` (UPDATE)
- `antigravity/core/checker.py` (UPDATE)
- `antigravity/tests/test_ast_analyzer.py` (UPDATE)

**Acceptance:**
- ✅ Parse Python/JS/TS correctly
- ✅ Detect missing return types
- ✅ Detect invalid imports
- ✅ JSON schema output

---

### Task 5: SLM Model Benchmark ⏳ TODO
**Priority:** P1
**Effort:** 1 day
**Impact:** Optimize routing

**Subtasks:**
- [x] 5.1: Setup benchmark environment
  - [ ] Install Ollama
  - [ ] Pull Qwen2.5-3B-Instruct
  - [ ] Pull Llama-3.2-3B
  - [ ] Pull SmolLM2-1.7B

- [x] 5.2: Create benchmark suite
  - [ ] 100 routing tasks (varied complexity)
  - [ ] Ground truth labels
  - [ ] Evaluation metrics

- [x] 5.3: Run benchmarks
  - [ ] Measure accuracy
  - [ ] Measure latency
  - [ ] Measure memory usage

- [x] 5.4: Analyze results
  - [ ] Compare models
  - [ ] Choose best model
  - [ ] Document recommendation

**Files:**
- `antigravity/benchmarks/slm_routing_benchmark.py` (NEW)
- `antigravity/benchmarks/results/slm_comparison.md` (NEW)

**Acceptance:**
- ✅ All 3 models benchmarked
- ✅ Clear winner identified
- ✅ Recommendation documented

---

## 🚀 ADVANCED FEATURES (P2)

### Task 6: Reasoning Models Integration ⏳ TODO
**Priority:** P2
**Effort:** 2-3 days
**Impact:** Handle complex tasks

**Subtasks:**
- [x] 6.1: Add OpenAI provider
  - [ ] Integrate o1-mini
  - [ ] Integrate o3-mini (when available)
  - [ ] Test API calls

- [x] 6.2: Implement cascading logic
  - [ ] Complexity scorer
  - [ ] Route simple → Sonnet
  - [ ] Route complex → o1

- [x] 6.3: Cost tracking
  - [ ] Track o1 usage
  - [ ] Compare costs
  - [ ] Optimize thresholds

- [x] 6.4: Write tests
  - [ ] Test cascading logic
  - [ ] Test cost tracking
  - [ ] Test quality improvement

**Files:**
- `antigravity/core/llm_client.py` (UPDATE)
- `antigravity/core/slm_router.py` (UPDATE)
- `antigravity/tests/test_reasoning_models.py` (NEW)

**Acceptance:**
- ✅ o1-mini integrated
- ✅ Cascading works correctly
- ✅ Cost tracking accurate
- ✅ Quality improvement measurable

---

## 📊 PROGRESS TRACKING

### Week 1: Phase 1 Final Safety (P0)
- Day 1-2: Task 1 (HybridRetriever Properties)
- Day 3: Task 2 (SLMRouter Properties)
- Day 4: Task 3 (Integration Test)
- Day 5: Review & fix issues

**Milestone:** Phase 1 Complete, Phase 2 unblocked

### Week 2: Production Readiness (P1)
- Day 1-2: Task 4 (Tree-sitter Integration)
- Day 3-4: Task 5 (SLM Benchmark)
- Day 5: Documentation & cleanup

**Milestone:** Production-ready v6.3.0

### Week 3: Advanced Features (P2)
- Day 1-3: Task 6 (Reasoning Models)
- Day 4: Integration testing
- Day 5: Release v6.3.0

**Milestone:** Full feature set complete

---

## 🎯 DEFINITION OF DONE

### Per Task:
- ✅ Code written and reviewed
- ✅ Tests passing (>90% coverage)
- ✅ Documentation updated
- ✅ No regressions

### Per Phase:
- ✅ All tasks complete
- ✅ Integration tests passing
- ✅ Performance benchmarks met
- ✅ Ready for next phase

### Final Release (v6.3.0):
- ✅ All P0 + P1 tasks complete
- ✅ All tests green (unit + integration + property)
- ✅ Documentation complete
- ✅ Benchmarks documented
- ✅ Ready for production

---

**Created:** 2026-03-26
**Sprint Start:** 2026-03-26
**Target Completion:** 2026-04-16
