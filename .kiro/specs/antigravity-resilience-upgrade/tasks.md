# Implementation Plan: Antigravity Resilience Upgrade (v6.2)

## Overview

Nâng cấp v6.2 focus vào **production resilience** thay vì chỉ production-grade. Các tasks được sắp xếp theo **impact/effort ratio** - ưu tiên Learning Loop (highest impact) trước.

---

## Tasks

### PHASE 1: LEARNING LOOP (Highest Impact) ✅ COMPLETE

- [x] 1. FailureMemory Core ✅
  - Tạo `antigravity/core/failure_memory.py`
  - Implement `FailureEntry` dataclass
  - Implement `record_failure(patch, error_delta, session_id)`
  - Implement `extract_pattern(patch, error_delta)` với regex patterns
  - Implement `persist()` và `load()` (JSON storage)
  - _Requirements: 3.1, 3.7_
  - **Status:** COMPLETE - All functionality implemented with JSONL storage

- [x] 2. FailureMemory Search ✅
  - Implement `search_similar(error, top_k)` với cosine similarity
  - Implement `format_for_prompt(failures)` cho LLM injection
  - Implement `purge_expired()` với TTL logic
  - Implement `get_statistics()` cho monitoring
  - _Requirements: 3.5, 3.6_
  - **Status:** COMPLETE - Relevance-based search with multi-factor scoring

- [x] 3. Orchestrator Learning Integration ✅
  - Inject `FailureMemory` vào `Orchestrator.__init__()`
  - Call `record_failure()` trong `replan_repair()` khi regression
  - Call `search_similar()` và inject vào repair prompt
  - Track `retry_reduction_rate` metric
  - _Requirements: 3.3, 3.6_
  - **Status:** COMPLETE - Integrated in execute loop and replan_repair

- [x] 4. Learning Loop Tests ✅
  - Unit tests: pattern extraction, similarity search, TTL
  - Integration test: full learning cycle (fail → record → reuse)
  - Property test: similar errors → similar patterns
  - _Requirements: 3.1-3.8_
  - **Status:** COMPLETE - 13/13 tests passing

**Phase 1 Completion:** 2026-03-26  
**Implementation Time:** 4 days (as planned)  
**Documentation:** `antigravity/docs/FAILURE_MEMORY_IMPLEMENTATION_COMPLETE.md`

---

### PHASE 2: INDEX LIFECYCLE

- [ ] 5. IndexManager Core
  - Tạo `antigravity/core/index_manager.py`
  - _Requirements: 1.1, 1.2, 1.3_
  
  - [ ] 5.1 Implement `__init__(skills_dir, cache_path)`
    - Load existing checksums từ `cache_path/index_checksums.json`
    - Initialize `_checksums: dict[str, str]` (file_path → SHA-256)
    - Initialize `_stale_files: set[str]`
  
  - [ ] 5.2 Implement `detect_changes() -> list[str]`
    - Scan tất cả `.md` files trong `skills_dir`
    - Compute SHA-256 cho mỗi file
    - So sánh với cached checksums
    - Return list files đã thay đổi
  
  - [ ] 5.3 Implement `mark_stale(files: list[str])`
    - Add files vào `_stale_files` set
    - Update internal tracking
  
  - [ ] 5.4 Implement `get_stale_ratio() -> float`
    - Return `len(_stale_files) / total_files`
    - Handle edge case: total_files = 0
  
  - [ ] 5.5 Implement `should_reindex(threshold: float = 0.2) -> bool`
    - Return `get_stale_ratio() > threshold`
    - Log decision với current ratio

- [ ] 6. IndexManager Reindex
  - _Requirements: 1.4, 1.5, 1.7_
  
  - [ ] 6.1 Implement `reindex(retriever: HybridRetriever, mode='incremental')`
    - Mode 'incremental': chỉ re-index stale files
    - Mode 'full': re-index tất cả files
    - Call `retriever.index()` với filtered documents
    - Update checksums sau khi reindex thành công
  
  - [ ] 6.2 Implement `save_checkpoint(version: int)`
    - Save checksums to `cache_path/index_checksums_v{version}.json`
    - Save metadata: timestamp, total_files, version
  
  - [ ] 6.3 Implement `rollback_index(version: int)`
    - Load checksums từ checkpoint version
    - Restore `_checksums` và `_stale_files`
    - Log rollback event
  
  - [ ] 6.4 Implement `get_health_metrics() -> dict`
    - Return:
      - `total_skills`: int
      - `stale_embeddings`: int
      - `last_index_time`: datetime
      - `index_version`: int
      - `stale_ratio`: float

- [ ] 7. HybridRetriever Integration
  - _Requirements: 1.6_
  
  - [ ] 7.1 Add `IndexManager` parameter to `HybridRetriever.__init__()`
    - Optional parameter: `index_manager: IndexManager | None = None`
    - Store as `self._index_manager`
  
  - [ ] 7.2 Modify `retrieve()` method
    - BEFORE retrieval: call `_index_manager.detect_changes()` if available
    - Check `should_reindex()`
    - If True: log warning, suggest reindex
  
  - [ ] 7.3 Add `auto_reindex()` method
    - Check `should_reindex()`
    - If True: call `_index_manager.reindex(self, mode='incremental')`
    - Log reindex completion
  
  - [ ] 7.4 Add health logging
    - Log index health metrics mỗi 100 retrievals
    - Emit WARNING khi stale_ratio > 20%
    - Emit CRITICAL khi stale_ratio > 50%

- [ ] 8. Index Lifecycle Tests
  - _Requirements: 1.1-1.7_
  
  - [ ] 8.1 Unit test: `test_detect_changes()`
    - Tạo temp skills với known checksums
    - Modify một file
    - Verify `detect_changes()` returns modified file
  
  - [ ] 8.2 Unit test: `test_stale_ratio()`
    - Mark 2/10 files stale
    - Verify `get_stale_ratio() == 0.2`
  
  - [ ] 8.3 Unit test: `test_incremental_reindex()`
    - Mark 3 files stale
    - Call `reindex(mode='incremental')`
    - Verify only 3 files re-indexed
  
  - [ ] 8.4 Integration test: `test_full_lifecycle()`
    - Initial index
    - Modify skill file
    - Detect change
    - Auto-reindex
    - Verify retrieval quality maintained
  
  - [ ] 8.5 Property test: `test_checksum_stability()`
    - `@given(file_content=st.text())`
    - Verify SHA-256 deterministic
    - Verify unchanged file → unchanged checksum

---

### PHASE 3: BUDGET STRATEGY

- [ ] 9. BudgetStrategy Core
  - Tạo `antigravity/core/budget_strategy.py`
  - _Requirements: 4.1, 4.5, 4.8_
  
  - [ ] 9.1 Implement `BudgetZone` enum
    - Define zones: `GREEN`, `YELLOW`, `RED`
    - Add zone descriptions
  
  - [ ] 9.2 Implement `StrategyConfig` dataclass
    - Fields:
      - `top_k: int` (số skills retrieve)
      - `use_expansion: bool` (contextual summary)
      - `prompt_mode: str` ("full" | "short" | "minimal")
      - `prefer_slm: bool` (SLM routing preference)
      - `enable_repair: bool` (repair loop enabled)
    - Add `__str__()` for logging
  
  - [ ] 9.3 Implement `BudgetStrategy.__init__(yellow_threshold, red_threshold)`
    - Default thresholds: yellow=0.5, red=0.2
    - Initialize zone configs:
      - GREEN: `StrategyConfig(top_k=5, use_expansion=True, prompt_mode="full", prefer_slm=False, enable_repair=True)`
      - YELLOW: `StrategyConfig(top_k=3, use_expansion=False, prompt_mode="short", prefer_slm=True, enable_repair=True)`
      - RED: `StrategyConfig(top_k=1, use_expansion=False, prompt_mode="minimal", prefer_slm=True, enable_repair=False)`
    - Initialize `_current_zone: BudgetZone = GREEN`
    - Initialize `_zone_stats: dict[BudgetZone, ZoneStats]` (success counts)
  
  - [ ] 9.4 Implement `get_current_zone(remaining_ratio: float) -> BudgetZone`
    - If `remaining_ratio > yellow_threshold`: return GREEN
    - Elif `remaining_ratio > red_threshold`: return YELLOW
    - Else: return RED
  
  - [ ] 9.5 Implement `get_strategy(zone: BudgetZone) -> StrategyConfig`
    - Return config for given zone
    - Log if zone changed from `_current_zone`
  
  - [ ] 9.6 Implement `log_zone_transition(old_zone, new_zone, remaining_ratio)`
    - Log format: `[BUDGET] Entering {new_zone} zone: {remaining_ratio:.1%} tokens remaining`
    - Log strategy changes: `[BUDGET] Strategy: top_k={config.top_k}, prompt_mode={config.prompt_mode}`
  
  - [ ] 9.7 Implement `record_task_result(zone: BudgetZone, success: bool)`
    - Update `_zone_stats[zone]` với success/failure count
  
  - [ ] 9.8 Implement `get_zone_statistics() -> dict[str, float]`
    - Return:
      - `green_zone_success_rate`
      - `yellow_zone_success_rate`
      - `red_zone_success_rate`
      - `total_tasks_per_zone`

- [ ] 10. Orchestrator Strategy Integration
  - _Requirements: 4.2, 4.3, 4.4, 4.6, 4.7_
  
  - [ ] 10.1 Add `BudgetStrategy` to `Orchestrator.__init__()`
    - Parameter: `budget_strategy: BudgetStrategy | None = None`
    - Default: `BudgetStrategy()` if None
    - Store as `self._budget_strategy`
  
  - [ ] 10.2 Modify `route_task()` method
    - Get current zone: `zone = self._budget_strategy.get_current_zone(self._budget.remaining_ratio)`
    - Get strategy: `config = self._budget_strategy.get_strategy(zone)`
    - Apply `prefer_slm` to routing decision:
      - If `config.prefer_slm`: force SLM routing
      - Else: use normal routing logic
  
  - [ ] 10.3 Modify `plan_execution()` method
    - Apply `top_k` to retrieval:
      - `skills = self._retriever.retrieve(query, top_k=config.top_k)`
    - Apply `use_expansion`:
      - If False: skip contextual summary generation
    - Apply `prompt_mode`:
      - "full": normal prompts with examples
      - "short": remove examples, keep core instructions
      - "minimal": ≤ 200 tokens, essential only
  
  - [ ] 10.4 Modify `replan_repair()` method
    - Check `config.enable_repair`:
      - If False (RED zone): skip repair loop, return failure immediately
      - Log: `[BUDGET] Repair disabled in RED zone, failing fast`
  
  - [ ] 10.5 Add zone tracking in `execute()` method
    - BEFORE execution: detect zone, log transition if changed
    - AFTER execution: call `self._budget_strategy.record_task_result(zone, success)`
  
  - [ ] 10.6 Add zone statistics logging
    - Log zone stats mỗi 20 tasks
    - Format: `[BUDGET] Zone Stats: Green=0.95, Yellow=0.80, Red=0.60`

- [ ] 11. Budget Strategy Tests
  - _Requirements: 4.1-4.8_
  
  - [ ] 11.1 Unit test: `test_zone_detection()`
    - Test remaining_ratio=0.8 → GREEN
    - Test remaining_ratio=0.4 → YELLOW
    - Test remaining_ratio=0.1 → RED
  
  - [ ] 11.2 Unit test: `test_strategy_configs()`
    - Verify GREEN config: top_k=5, full prompts
    - Verify YELLOW config: top_k=3, short prompts
    - Verify RED config: top_k=1, minimal prompts, no repair
  
  - [ ] 11.3 Unit test: `test_zone_transitions()`
    - Simulate budget depletion: 100% → 45% → 15%
    - Verify transitions logged correctly
    - Verify strategy changes applied
  
  - [ ] 11.4 Integration test: `test_full_degradation_flow()`
    - Start with full budget (GREEN)
    - Execute tasks until YELLOW zone
    - Verify top_k reduced, SLM preferred
    - Execute more tasks until RED zone
    - Verify repair disabled, minimal prompts
  
  - [ ] 11.5 Integration test: `test_zone_statistics()`
    - Execute 10 tasks in each zone
    - Record success/failure
    - Verify statistics computed correctly
  
  - [ ] 11.6 Property test: `test_zone_monotonicity()`
    - `@given(remaining_ratio=st.floats(0.0, 1.0))`
    - Verify zone never "upgrades" as budget depletes
    - Verify GREEN → YELLOW → RED order maintained

---

### PHASE 4: ERROR PRIORITIZATION

- [ ] 12. ErrorPrioritizer Core
  - Tạo `antigravity/core/error_prioritizer.py`
  - _Requirements: 2.1, 2.2_
  
  - [ ] 12.1 Implement `ErrorSeverity` enum
    - SYNTAX = 1 (blocking)
    - RUNTIME = 2 (critical)
    - LINT = 3 (minor)
  
  - [ ] 12.2 Implement `PrioritizedError` dataclass
    - Fields:
      - `error_text: str`
      - `severity: ErrorSeverity`
      - `line_number: int | None`
      - `file_path: str`
      - `is_root_cause: bool = False`
      - `dependent_errors: list[str] = []`
      - `context_tokens: int = 0`
  
  - [ ] 12.3 Implement `_classify_error(error_text: str) -> ErrorSeverity`
    - Regex patterns:
      - SYNTAX: `SyntaxError|IndentationError|TabError|unexpected EOF`
      - RUNTIME: `RuntimeError|NameError|TypeError|AttributeError|ImportError`
      - LINT: `W\d{3}|C\d{3}|R\d{3}` (pylint codes)
    - Default: RUNTIME if no match
  
  - [ ] 12.4 Implement `estimate_context_size(error: PrioritizedError) -> int`
    - Count tokens in error_text (rough: len(text.split()) * 1.3)
    - Add 50 tokens for metadata (file, line)
    - Add 100 tokens for code context (±3 lines)
  
  - [ ] 12.5 Implement `prioritize_errors(errors: list[str], max_k: int = 3) -> list[PrioritizedError]`
    - Parse each error string
    - Classify severity
    - Estimate context size
    - Sort by severity (SYNTAX > RUNTIME > LINT)
    - Take top-k errors
    - Return list of `PrioritizedError`

- [ ] 13. ErrorPrioritizer Advanced
  - _Requirements: 2.3, 2.4, 2.6_
  
  - [ ] 13.1 Implement `ErrorCluster` dataclass
    - Fields:
      - `cluster_id: str`
      - `error_type: str` (e.g., "NameError")
      - `affected_functions: list[str]`
      - `error_count: int`
      - `representative_error: PrioritizedError`
      - `summary: str`
  
  - [ ] 13.2 Implement `detect_error_chains(errors: list[PrioritizedError]) -> list[PrioritizedError]`
    - Pattern detection:
      - ImportError → NameError (missing import causes undefined name)
      - SyntaxError → multiple downstream errors
    - Algorithm:
      - Group errors by file
      - Sort by line number
      - If error A precedes error B and A.type causes B.type:
        - Mark A as root_cause=True
        - Add B.error_text to A.dependent_errors
        - Remove B from list
    - Return filtered list (only root causes)
  
  - [ ] 13.3 Implement `cluster_errors(errors: list[PrioritizedError]) -> list[ErrorCluster]`
    - Group by error type (NameError, TypeError, etc.)
    - Group by affected function (extract from traceback)
    - Create cluster for each group with ≥2 errors
    - Select representative error (first occurrence)
    - Generate summary: `"{count}x {error_type} in {function}"`
  
  - [ ] 13.4 Implement `format_clusters_for_llm(clusters: list[ErrorCluster]) -> str`
    - Format: `[ERROR CLUSTER] {summary}\n  Representative: {error_text}`
    - Limit to 500 tokens total

- [ ] 14. ASTAnalyzer Integration
  - _Requirements: 2.5_
  
  - [ ] 14.1 Add `ErrorPrioritizer` to `ASTAnalyzer.__init__()`
    - Parameter: `error_prioritizer: ErrorPrioritizer | None = None`
    - Default: `ErrorPrioritizer()` if None
    - Store as `self._error_prioritizer`
  
  - [ ] 14.2 Modify `analyze()` method - error extraction
    - Extract all errors from AST/linter output
    - Convert to list of error strings
  
  - [ ] 14.3 Modify `analyze()` method - prioritization
    - Call `self._error_prioritizer.prioritize_errors(errors, max_k=3)`
    - Call `self._error_prioritizer.detect_error_chains(prioritized)`
    - Get final prioritized list (root causes only)
  
  - [ ] 14.4 Modify `analyze()` method - clustering (optional)
    - If len(errors) > 5: call `cluster_errors()`
    - Use cluster summaries instead of individual errors
  
  - [ ] 14.5 Modify `analyze()` method - context limiting
    - Estimate total context: sum of `estimate_context_size()` for all errors
    - If total > 1000 tokens: reduce max_k or use clustering
    - Log: `[ERROR] Context limited to {actual} tokens (target: 1000)`
  
  - [ ] 14.6 Update `ASTContract` dataclass
    - Add field: `error_priority_info: dict[str, Any]`
    - Include:
      - `prioritized_errors: list[PrioritizedError]`
      - `total_errors: int` (before filtering)
      - `root_causes: int`
      - `clusters: list[ErrorCluster]` (if used)

- [ ] 15. Error Prioritization Tests
  - _Requirements: 2.1-2.6_
  
  - [ ] 15.1 Unit test: `test_error_classification()`
    - Test SyntaxError → SYNTAX
    - Test NameError → RUNTIME
    - Test pylint W0612 → LINT
  
  - [ ] 15.2 Unit test: `test_prioritization_order()`
    - Input: [LINT, SYNTAX, RUNTIME, LINT]
    - Expected output: [SYNTAX, RUNTIME, LINT] (top-3)
  
  - [ ] 15.3 Unit test: `test_error_chains()`
    - Input: ImportError at line 5, NameError at line 10
    - Expected: ImportError marked as root_cause
    - Expected: NameError in dependent_errors
  
  - [ ] 15.4 Unit test: `test_error_clustering()`
    - Input: 5x NameError in function "foo"
    - Expected: 1 cluster with count=5
    - Expected: summary = "5x NameError in foo"
  
  - [ ] 15.5 Integration test: `test_multi_error_scenario()`
    - Create file with 10 errors (mixed types)
    - Run ASTAnalyzer.analyze()
    - Verify only top-3 root causes returned
    - Verify total context ≤ 1000 tokens
  
  - [ ] 15.6 Property test: `test_priority_ordering()`
    - `@given(errors=st.lists(st.sampled_from([SYNTAX, RUNTIME, LINT])))`
    - Verify output always sorted by severity
    - Verify SYNTAX always before RUNTIME before LINT

---

### PHASE 5: HEALTH MONITORING

- [ ] 16. HealthMonitor Core
  - Tạo `antigravity/core/health_monitor.py`
  - _Requirements: 5.1, 5.2, 5.3_
  
  - [ ] 16.1 Implement `TaskMetrics` dataclass
    - Fields:
      - `task_id: str`
      - `success: bool`
      - `patches_count: int`
      - `rollback: bool`
      - `tokens_used: int`
      - `no_op_patch: bool`
      - `timestamp: datetime`
  
  - [ ] 16.2 Implement `DerivedMetrics` dataclass
    - Fields:
      - `avg_patches_per_success: float`
      - `rollback_rate: float`
      - `no_op_patch_rate: float`
      - `slm_vs_llm_ratio: float`
      - `token_per_task: float`
      - `success_rate: float`
  
  - [ ] 16.3 Implement `BaselineMetrics` dataclass
    - Fields:
      - `baseline_token_per_task: float`
      - `baseline_patches: float`
      - `baseline_success_rate: float`
      - `established_at: datetime`
      - `task_count: int` (số tasks dùng để tính baseline)
  
  - [ ] 16.4 Implement `HealthMonitor.__init__()`
    - Initialize `_task_history: list[TaskMetrics] = []`
    - Initialize `_baseline: BaselineMetrics | None = None`
    - Initialize `_health_score: float = 100.0`
    - Initialize `_health_category: str = "excellent"`
    - Initialize weights: `w1=20, w2=10, w3=5` (rollback, retry, token)
  
  - [ ] 16.5 Implement `record_task(success, patches, rollback, tokens, no_op)`
    - Create `TaskMetrics` instance
    - Append to `_task_history`
    - If len(history) == 50 and baseline is None: call `establish_baseline()`
  
  - [ ] 16.6 Implement `compute_health_score() -> float`
    - Formula:
      ```python
      health_score = (
          success_rate * 100
          - rollback_rate * w1
          - (avg_patches - 1) * w2
          - (token_per_task / baseline_token) * w3
      )
      ```
    - Clamp to [0, 100]
    - Update `_health_score`
  
  - [ ] 16.7 Implement `categorize_health(score: float) -> str`
    - 80-100: "excellent"
    - 60-79: "good"
    - 40-59: "fair"
    - 0-39: "poor"
    - Update `_health_category`

- [ ] 17. HealthMonitor Analytics
  - _Requirements: 5.1, 5.4, 5.8_
  
  - [ ] 17.1 Implement `get_derived_metrics(window: str = "last_10") -> DerivedMetrics`
    - Windows: "last_10", "last_hour", "last_24h", "all"
    - Filter `_task_history` by window
    - Compute:
      - `success_rate = successes / total`
      - `rollback_rate = rollbacks / total`
      - `no_op_patch_rate = no_ops / total`
      - `avg_patches_per_success = sum(patches) / successes`
      - `token_per_task = sum(tokens) / total`
    - Return `DerivedMetrics` instance
  
  - [ ] 17.2 Implement `establish_baseline()`
    - Take first 50 successful tasks
    - Compute baseline metrics:
      - `baseline_token_per_task`
      - `baseline_patches`
      - `baseline_success_rate`
    - Store as `_baseline`
    - Log: `[HEALTH] Baseline established: {baseline}`
  
  - [ ] 17.3 Implement `detect_anomalies() -> list[str]`
    - Compare current metrics vs baseline:
      - Success rate drop > 20%: "Success rate dropped significantly"
      - Token usage spike > 50%: "Token usage increased significantly"
      - Patches increase > 100%: "Retry count increased significantly"
    - Return list of anomaly descriptions
  
  - [ ] 17.4 Implement `suggest_actions() -> list[str]`
    - Rule-based suggestions:
      - High rollback_rate (>15%): "Review error detection logic"
      - High token_per_task (>baseline*1.5): "Optimize prompt length"
      - Low success_rate (<70%): "Check skill retrieval quality"
      - Anomaly detected: "Investigate recent changes"
    - Return list of actionable suggestions
  
  - [ ] 17.5 Implement `generate_report() -> str`
    - Format:
      ```
      [HEALTH REPORT]
      Health Score: {score} ({category})
      
      Metrics (last 10 tasks):
      - Success Rate: {success_rate:.1%}
      - Rollback Rate: {rollback_rate:.1%}
      - Avg Patches: {avg_patches:.1f}
      - Token/Task: {token_per_task:.0f}
      
      Top Issue: {top_issue}
      Suggestion: {top_suggestion}
      Top Strength: {top_strength}
      ```
    - Identify top issue (highest deviation from baseline)
    - Identify top strength (best metric vs baseline)

- [ ] 18. Orchestrator Health Integration
  - _Requirements: 5.4, 5.7_
  
  - [ ] 18.1 Add `HealthMonitor` to `Orchestrator.__init__()`
    - Parameter: `health_monitor: HealthMonitor | None = None`
    - Default: `HealthMonitor()` if None
    - Store as `self._health_monitor`
    - Initialize task counter: `_task_count = 0`
  
  - [ ] 18.2 Modify `execute()` method - record task
    - In finally block:
      - Extract metrics: success, patches_count, rollback, tokens_used, no_op
      - Call `self._health_monitor.record_task(...)`
      - Increment `_task_count`
  
  - [ ] 18.3 Modify `execute()` method - periodic logging
    - If `_task_count % 10 == 0`:
      - Call `self._health_monitor.compute_health_score()`
      - Get score and category
      - Log: `[HEALTH] Score: {score:.1f} ({category})`
  
  - [ ] 18.4 Implement health alerts
    - After computing score:
      - If score < 60: log WARNING with suggestions
      - If score < 40: log CRITICAL with anomalies
    - Format: `[HEALTH] WARNING: Score={score}, Suggestions: {suggestions}`
  
  - [ ] 18.5 Add health report generation
    - Mỗi 100 tasks: call `generate_report()`
    - Log full report
    - Optionally save to file: `antigravity/reports/health_{timestamp}.txt`

- [ ] 19. Health Monitoring Tests
  - _Requirements: 5.1-5.9_
  
  - [ ] 19.1 Unit test: `test_health_score_computation()`
    - Record 10 tasks: 8 success, 2 rollback
    - Verify score computed correctly
    - Verify category = "good" or "excellent"
  
  - [ ] 19.2 Unit test: `test_derived_metrics()`
    - Record 20 tasks with known metrics
    - Verify rollback_rate, token_per_task, etc. computed correctly
  
  - [ ] 19.3 Unit test: `test_baseline_establishment()`
    - Record 50 tasks
    - Verify baseline established automatically
    - Verify baseline values reasonable
  
  - [ ] 19.4 Unit test: `test_anomaly_detection()`
    - Establish baseline with success_rate=0.9
    - Record new tasks with success_rate=0.6
    - Verify anomaly detected: "Success rate dropped"
  
  - [ ] 19.5 Unit test: `test_actionable_suggestions()`
    - High rollback_rate → "Review error detection"
    - High token_usage → "Optimize prompt length"
    - Verify suggestions generated correctly
  
  - [ ] 19.6 Integration test: `test_full_monitoring_cycle()`
    - Execute 100 tasks through Orchestrator
    - Verify health score tracked
    - Verify periodic logging (every 10 tasks)
    - Verify alerts emitted when score < 60
  
  - [ ] 19.7 Property test: `test_health_score_monotonicity()`
    - `@given(success_rate=st.floats(0.0, 1.0))`
    - Verify higher success_rate → higher health_score
    - Verify score always in [0, 100]

---

### PHASE 6: SELF-EVALUATION

- [ ] 20. Self-Evaluation Report
  - _Requirements: 6.1_
  
  - [ ] 20.1 Implement `generate_self_eval_report() -> str` in `HealthMonitor`
    - Trigger: mỗi 100 tasks
    - Compute current metrics
    - Identify top issue (worst metric vs baseline)
    - Identify top strength (best metric vs baseline)
    - Generate actionable suggestion
    - Format:
      ```
      [SELF-EVALUATION] Performance Report
      
      Health Score: {score} ({category})
      Tasks Analyzed: {count}
      
      Top Issue: {issue}
      - Current: {current_value}
      - Baseline: {baseline_value}
      - Impact: {impact_description}
      
      Suggestion: {actionable_suggestion}
      
      Top Strength: {strength}
      - Current: {current_value}
      - Baseline: {baseline_value}
      - Improvement: {improvement_percentage}
      
      Anomalies Detected: {anomalies}
      ```
  
  - [ ] 20.2 Implement report persistence
    - Save report to `antigravity/reports/self_eval_{timestamp}.md`
    - Create reports directory if not exists
    - Keep last 10 reports, delete older ones
  
  - [ ] 20.3 Implement report triggering in `Orchestrator`
    - Check `_task_count % 100 == 0`
    - Call `self._health_monitor.generate_self_eval_report()`
    - Log report to console
    - Save to file

- [ ] 21. Performance Baseline
  - _Requirements: 6.4_
  
  - [ ] 21.1 Implement baseline update logic
    - Add `_baseline_update_interval: timedelta` (default: 90 days)
    - Add `_last_baseline_update: datetime`
  
  - [ ] 21.2 Implement `should_update_baseline() -> bool`
    - Check if `datetime.now() - _last_baseline_update > _baseline_update_interval`
    - Check if sufficient new data (≥50 tasks since last update)
    - Return True if both conditions met
  
  - [ ] 21.3 Implement `update_baseline()`
    - Take last 50 successful tasks
    - Recompute baseline metrics
    - Log: `[BASELINE] Updated: old={old_baseline}, new={new_baseline}`
    - Update `_last_baseline_update`
  
  - [ ] 21.4 Implement automatic baseline updates
    - In `record_task()`: check `should_update_baseline()`
    - If True: call `update_baseline()`
  
  - [ ] 21.5 Implement baseline persistence
    - Save baseline to `antigravity/data/baseline.json`
    - Load baseline on `HealthMonitor.__init__()`
    - Include metadata: established_at, task_count, version

- [ ] 22. Actionable Suggestions
  - _Requirements: 6.3_
  
  - [ ] 22.1 Implement `SuggestionEngine` class
    - Rule-based system với priority scoring
  
  - [ ] 22.2 Implement suggestion rules
    - Rule 1: High stale_ratio (>20%)
      - Condition: `index_manager.get_stale_ratio() > 0.2`
      - Suggestion: "Re-index skills to maintain retrieval quality"
      - Priority: HIGH
    
    - Rule 2: High rollback_rate (>15%)
      - Condition: `derived_metrics.rollback_rate > 0.15`
      - Suggestion: "Review error detection logic in ASTAnalyzer"
      - Priority: HIGH
    
    - Rule 3: Frequent Red zone (>30% of time)
      - Condition: `budget_stats.red_zone_ratio > 0.3`
      - Suggestion: "Increase budget limits or optimize token usage"
      - Priority: MEDIUM
    
    - Rule 4: Low SLM usage (<20%)
      - Condition: `derived_metrics.slm_vs_llm_ratio < 0.2`
      - Suggestion: "Check SLM router configuration and thresholds"
      - Priority: LOW
    
    - Rule 5: High token per task (>baseline*1.5)
      - Condition: `token_per_task > baseline * 1.5`
      - Suggestion: "Optimize prompt length and retrieval top_k"
      - Priority: MEDIUM
    
    - Rule 6: Low success rate (<70%)
      - Condition: `success_rate < 0.7`
      - Suggestion: "Review skill retrieval quality and repair logic"
      - Priority: CRITICAL
  
  - [ ] 22.3 Implement `get_top_suggestions(max_count: int = 3) -> list[str]`
    - Evaluate all rules
    - Sort by priority (CRITICAL > HIGH > MEDIUM > LOW)
    - Return top-N suggestions
  
  - [ ] 22.4 Integrate suggestions into self-eval report
    - Call `get_top_suggestions()` in `generate_self_eval_report()`
    - Include in report output

- [ ] 23. Self-Evaluation Tests
  - _Requirements: 6.1-6.4_
  
  - [ ] 23.1 Unit test: `test_self_eval_report_generation()`
    - Record 100 tasks with known metrics
    - Call `generate_self_eval_report()`
    - Verify report contains: score, top issue, suggestion, top strength
  
  - [ ] 23.2 Unit test: `test_baseline_update_logic()`
    - Establish initial baseline
    - Simulate 90 days passing
    - Record 50 new tasks
    - Verify `should_update_baseline()` returns True
    - Verify baseline updated correctly
  
  - [ ] 23.3 Unit test: `test_suggestion_rules()`
    - Test each rule individually:
      - High stale_ratio → "Re-index skills"
      - High rollback_rate → "Review error detection"
      - Frequent Red zone → "Increase budget"
    - Verify priority ordering
  
  - [ ] 23.4 Integration test: `test_full_self_eval_cycle()`
    - Execute 100 tasks
    - Verify self-eval report generated automatically
    - Verify report saved to file
    - Verify suggestions actionable
  
  - [ ] 23.5 Unit test: `test_report_persistence()`
    - Generate 15 reports
    - Verify only last 10 kept
    - Verify older reports deleted

---

### PHASE 7: METRICS API (Optional)

- [ ] 24. Metrics API Endpoint
  - _Requirements: 5.5, 5.6_
  
  - [ ] 24.1 Create `antigravity/api/metrics.py`
    - Setup FastAPI app
    - Add CORS middleware
    - Add error handling
  
  - [ ] 24.2 Implement `GET /metrics/health` endpoint
    - Query params:
      - `window: str = "last_10"` (last_10 | last_hour | last_24h | all)
    - Response:
      ```json
      {
        "health_score": 85.3,
        "category": "excellent",
        "metrics": {
          "success_rate": 0.92,
          "rollback_rate": 0.08,
          "avg_patches": 1.5,
          "token_per_task": 2500,
          "no_op_patch_rate": 0.05
        },
        "window": "last_10",
        "timestamp": "2026-03-30T10:00:00Z"
      }
      ```
    - Get metrics from `HealthMonitor.get_derived_metrics(window)`
    - Compute health score
  
  - [ ] 24.3 Implement `GET /metrics/derived` endpoint
    - Query params:
      - `window: str = "last_10"`
    - Response:
      ```json
      {
        "avg_patches_per_success": 1.5,
        "rollback_rate": 0.08,
        "no_op_patch_rate": 0.05,
        "slm_vs_llm_ratio": 0.35,
        "token_per_task": 2500,
        "success_rate": 0.92,
        "window": "last_10"
      }
      ```
  
  - [ ] 24.4 Implement `GET /metrics/trends` endpoint
    - Query params:
      - `metric: str` (health_score | success_rate | token_per_task | rollback_rate)
      - `window: str = "last_24h"`
    - Response:
      ```json
      {
        "metric": "health_score",
        "data_points": [
          {"timestamp": "2026-03-30T09:00:00Z", "value": 85.3},
          {"timestamp": "2026-03-30T10:00:00Z", "value": 87.1},
          ...
        ],
        "trend": "improving",
        "change_percentage": 2.1
      }
      ```
    - Aggregate metrics by time buckets
    - Compute trend direction (improving | stable | degrading)
  
  - [ ] 24.5 Implement `GET /metrics/baseline` endpoint
    - Response:
      ```json
      {
        "baseline_token_per_task": 2000,
        "baseline_patches": 1.2,
        "baseline_success_rate": 0.90,
        "established_at": "2026-03-01T00:00:00Z",
        "task_count": 50,
        "last_updated": "2026-03-30T00:00:00Z"
      }
      ```
  
  - [ ] 24.6 Implement `GET /metrics/suggestions` endpoint
    - Response:
      ```json
      {
        "suggestions": [
          {
            "priority": "HIGH",
            "message": "Re-index skills to maintain retrieval quality",
            "reason": "Stale ratio: 25%"
          },
          ...
        ],
        "anomalies": [
          "Success rate dropped significantly"
        ]
      }
      ```

- [ ] 25. Metrics Export
  - _Requirements: 5.9_
  
  - [ ] 25.1 Implement `GET /metrics/export/json` endpoint
    - Export all metrics as JSON
    - Include: health, derived, baseline, trends
    - Response: downloadable JSON file
  
  - [ ] 25.2 Implement `GET /metrics/export/csv` endpoint
    - Export task history as CSV
    - Columns: task_id, timestamp, success, patches, rollback, tokens, no_op
    - Response: downloadable CSV file
  
  - [ ] 25.3 Implement `GET /metrics/export/prometheus` endpoint (optional)
    - Export metrics in Prometheus format
    - Metrics:
      - `antigravity_health_score`
      - `antigravity_success_rate`
      - `antigravity_rollback_rate`
      - `antigravity_token_per_task`
    - Response: Prometheus text format
  
  - [ ] 25.4 Add export CLI command
    - `antigravity metrics export --format json --output metrics.json`
    - `antigravity metrics export --format csv --output tasks.csv`
    - `antigravity metrics export --format prometheus --output metrics.prom`
  
  - [ ] 25.5 Implement API tests
    - Test each endpoint with sample data
    - Test query parameters
    - Test error handling (invalid window, missing data)
    - Test export formats

---

### PHASE 8: INTEGRATION & VALIDATION

- [ ] 26. Full System Integration Test
  - _Requirements: All_
  
  - [ ] 26.1 Setup integration test environment
    - Create test workspace với sample skills
    - Initialize all components:
      - HybridRetriever với IndexManager
      - ASTAnalyzer với ErrorPrioritizer
      - Orchestrator với FailureMemory, BudgetStrategy, HealthMonitor
      - TracingService
    - Setup test database/storage
  
  - [ ] 26.2 Test Learning Loop integration
    - Execute 20 tasks với intentional failures
    - Verify failures recorded in FailureMemory
    - Execute similar tasks again
    - Verify retry reduction (measure before/after)
    - Target: ≥30% retry reduction
  
  - [ ] 26.3 Test Index Lifecycle integration
    - Initial index với 50 skills
    - Modify 10 skills (add/edit/delete)
    - Verify stale detection
    - Trigger reindex
    - Verify retrieval quality maintained
    - Measure retrieval accuracy before/after
  
  - [ ] 26.4 Test Budget Strategy integration
    - Start with full budget (GREEN zone)
    - Execute tasks until YELLOW zone
    - Verify strategy changes: top_k reduced, SLM preferred
    - Execute more tasks until RED zone
    - Verify repair disabled, minimal prompts
    - Measure success rate per zone
  
  - [ ] 26.5 Test Error Prioritization integration
    - Create files với multiple errors (10+ errors)
    - Run ASTAnalyzer
    - Verify only top-3 root causes returned
    - Verify context ≤ 1000 tokens
    - Verify repair focuses on root causes
  
  - [ ] 26.6 Test Health Monitoring integration
    - Execute 100 tasks với mixed success/failure
    - Verify health score computed correctly
    - Verify periodic logging (every 10 tasks)
    - Verify alerts emitted when score < 60
    - Verify self-eval report generated at task 100
  
  - [ ] 26.7 Test component interactions
    - FailureMemory + ErrorPrioritizer: similar errors avoided
    - BudgetStrategy + IndexManager: no reindex in RED zone
    - HealthMonitor + all components: metrics collected correctly
    - Verify no conflicts or race conditions

- [ ] 27. Performance Benchmarking
  - _Requirements: Success Metrics_
  
  - [ ] 27.1 Setup benchmark suite
    - Create 100 test tasks với varying complexity
    - Mix of: syntax errors, runtime errors, logic bugs
    - Known ground truth (expected fixes)
  
  - [ ] 27.2 Benchmark v6.1 (baseline)
    - Run 100 tasks on v6.1 system
    - Measure:
      - Success rate
      - Avg retries per task
      - Total tokens used
      - Avg time per task
    - Record baseline metrics
  
  - [ ] 27.3 Benchmark v6.2 (upgraded)
    - Run same 100 tasks on v6.2 system
    - Measure same metrics
    - Record v6.2 metrics
  
  - [ ] 27.4 Compute improvements
    - Retry reduction rate: `(v6.1_retries - v6.2_retries) / v6.1_retries`
    - Token savings: `(v6.1_tokens - v6.2_tokens) / v6.1_tokens`
    - Success rate change: `v6.2_success - v6.1_success`
    - Health score: v6.2 only (new metric)
  
  - [ ] 27.5 Validate success criteria
    - ✅ Retry reduction rate > 30%
    - ✅ Token savings > 20%
    - ✅ Health score consistently > 70
    - ✅ Zero silent failures (index staleness detected)
    - Generate benchmark report
  
  - [ ] 27.6 Performance regression check
    - Verify v6.2 not slower than v6.1
    - Verify memory usage reasonable
    - Verify no resource leaks

- [ ] 28. Documentation
  - _Requirements: All_
  
  - [ ] 28.1 Update `ARCHITECTURE_UPGRADE_COMPLETE.md`
    - Add v6.2 Resilience Upgrade section
    - Document new components:
      - FailureMemory
      - IndexManager
      - BudgetStrategy
      - ErrorPrioritizer
      - HealthMonitor
    - Update architecture diagrams
  
  - [ ] 28.2 Create `RESILIENCE_UPGRADE_GUIDE.md`
    - User guide for v6.2 features
    - How to:
      - Configure budget thresholds
      - Trigger manual reindex
      - Interpret health scores
      - Use self-eval reports
      - Export metrics
    - Best practices
  
  - [ ] 28.3 Document configuration options
    - Create `CONFIG_REFERENCE.md`
    - Document all new config options:
      - `AG_FAILURE_MEMORY_TTL`
      - `AG_INDEX_STALE_THRESHOLD`
      - `AG_BUDGET_YELLOW_THRESHOLD`
      - `AG_BUDGET_RED_THRESHOLD`
      - `AG_ERROR_MAX_K`
      - `AG_HEALTH_BASELINE_INTERVAL`
    - Include examples and defaults
  
  - [ ] 28.4 Create migration guide
    - Create `MIGRATION_v6.1_to_v6.2.md`
    - Breaking changes (if any)
    - New dependencies
    - Configuration changes
    - Step-by-step upgrade process
    - Rollback procedure
  
  - [ ] 28.5 Update API documentation
    - Document new metrics endpoints
    - Add OpenAPI/Swagger spec
    - Include example requests/responses
    - Document export formats
  
  - [ ] 28.6 Create troubleshooting guide
    - Common issues and solutions:
      - High stale ratio → reindex
      - Low health score → check suggestions
      - Frequent RED zone → increase budget
      - High rollback rate → review error detection
    - Debug logging tips
    - Performance tuning guide

- [ ] 29. Final Validation
  - _Requirements: All_
  
  - [ ] 29.1 Run full test suite
    - Unit tests: all phases (target: 150+ tests)
    - Integration tests: all phases (target: 30+ tests)
    - Property tests: all phases (target: 20+ tests)
    - Target: 300+ total tests passing
    - Verify 100% pass rate
  
  - [ ] 29.2 Verify requirements coverage
    - Create requirements traceability matrix
    - Map each requirement to tests
    - Verify all 5 requirements fully covered:
      - ✅ Req 1: Index Lifecycle (1.1-1.7)
      - ✅ Req 2: Error Prioritization (2.1-2.6)
      - ✅ Req 3: Learning Loop (3.1-3.8)
      - ✅ Req 4: Budget Strategy (4.1-4.8)
      - ✅ Req 5: Health Monitoring (5.1-5.9)
      - ✅ Req 6: Self-Evaluation (6.1-6.4)
  
  - [ ] 29.3 Verify backward compatibility
    - Test v6.1 code still works with v6.2
    - Test graceful degradation (components optional)
    - Test migration path (v6.1 data → v6.2)
  
  - [ ] 29.4 Code quality checks
    - Run linters: ruff, mypy, pylint
    - Check code coverage (target: >80%)
    - Review code complexity (cyclomatic < 10)
    - Check for security issues (bandit)
  
  - [ ] 29.5 Final performance validation
    - Run benchmark suite one more time
    - Verify all success criteria met
    - Generate final performance report
    - Compare with initial goals
  
  - [ ] 29.6 Release preparation
    - Update version to v6.2.0
    - Update CHANGELOG.md
    - Tag release in git
    - Create release notes
    - Prepare deployment artifacts

---

## Notes

### Priority Order (Impact/Effort):
1. **Learning Loop** (Phase 1) - HIGHEST IMPACT, moderate effort
2. **Index Lifecycle** (Phase 2) - High impact, low effort
3. **Budget Strategy** (Phase 3) - High impact, low effort
4. **Error Prioritization** (Phase 4) - Medium impact, low effort
5. **Health Monitoring** (Phase 5) - Medium impact, moderate effort

### Dependencies:
- Phase 1-5 can run in parallel (independent)
- Phase 6 depends on Phase 5 (HealthMonitor)
- Phase 7 optional (nice-to-have)
- Phase 8 depends on all previous phases

### Estimated Timeline:
- Phase 1: 3 days
- Phase 2: 2 days
- Phase 3: 2 days
- Phase 4: 2 days
- Phase 5: 3 days
- Phase 6: 2 days
- Phase 7: 2 days (optional)
- Phase 8: 2 days
- **Total: 16-18 days** (3-4 weeks)

### Success Criteria:
- [ ] Retry reduction rate > 30%
- [ ] Health score consistently > 70
- [ ] Token savings > 20%
- [ ] Zero silent failures (index staleness detected)
- [ ] All tests passing (target: 300+ tests)

---

**Version:** v6.2.0-RESILIENCE-UPGRADE  
**Status:** READY TO IMPLEMENT  
**Next Action:** Start Phase 1 (Learning Loop)
