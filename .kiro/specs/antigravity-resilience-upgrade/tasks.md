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
  - Implement `detect_changes()` với SHA-256 checksums
  - Implement `mark_stale(files)` và `get_stale_ratio()`
  - Implement `should_reindex()` với threshold logic
  - _Requirements: 1.1, 1.2, 1.3_

- [ ] 6. IndexManager Reindex
  - Implement `reindex(retriever)` incremental mode
  - Implement `save_checkpoint()` và `rollback_index(version)`
  - Implement `get_health_metrics()`
  - _Requirements: 1.4, 1.5, 1.7_

- [ ] 7. HybridRetriever Integration
  - Add `IndexManager` vào `HybridRetriever.__init__()`
  - Call `detect_changes()` before each `retrieve()`
  - Auto-trigger reindex khi `should_reindex()` returns True
  - Log index health warnings
  - _Requirements: 1.6_

- [ ] 8. Index Lifecycle Tests
  - Unit tests: change detection, stale ratio, incremental reindex
  - Integration test: full lifecycle (change → detect → reindex)
  - Property test: checksum stability
  - _Requirements: 1.1-1.7_

---

### PHASE 3: BUDGET STRATEGY

- [ ] 9. BudgetStrategy Core
  - Tạo `antigravity/core/budget_strategy.py`
  - Implement `StrategyConfig` dataclass
  - Implement `get_current_zone()` với thresholds
  - Implement `get_strategy()` mapping
  - Implement `log_zone_transition()`
  - _Requirements: 4.1, 4.5, 4.8_

- [ ] 10. Orchestrator Strategy Integration
  - Inject `BudgetStrategy` vào `Orchestrator.__init__()`
  - Apply strategy trong `route_task()` (prefer_slm)
  - Apply strategy trong `plan_execution()` (top_k, prompt length)
  - Disable repair loop trong Red zone
  - Track zone-specific success rates
  - _Requirements: 4.2, 4.3, 4.4, 4.6, 4.7_

- [ ] 11. Budget Strategy Tests
  - Unit tests: zone detection, strategy selection, transitions
  - Integration test: full degradation flow (Green → Yellow → Red)
  - Property test: zone monotonicity
  - _Requirements: 4.1-4.8_

---

### PHASE 4: ERROR PRIORITIZATION

- [ ] 12. ErrorPrioritizer Core
  - Tạo `antigravity/core/error_prioritizer.py`
  - Implement `prioritize_errors(errors, max_k)` với severity weights
  - Implement `_classify_error(text)` với regex patterns
  - Implement `estimate_context_size(errors)`
  - _Requirements: 2.1, 2.2_

- [ ] 13. ErrorPrioritizer Advanced
  - Implement `detect_error_chains(errors)` cho root cause detection
  - Implement `cluster_errors(errors)` cho grouping
  - Implement `PrioritizedError` và `ErrorCluster` dataclasses
  - _Requirements: 2.3, 2.4, 2.6_

- [ ] 14. ASTAnalyzer Integration
  - Inject `ErrorPrioritizer` vào `ASTAnalyzer.analyze()`
  - Filter `affected_nodes` theo prioritized errors
  - Add `error_priority_info` vào `ASTContract`
  - Limit total error context ≤ 1000 tokens
  - _Requirements: 2.5_

- [ ] 15. Error Prioritization Tests
  - Unit tests: classification, chains, clustering
  - Integration test: multi-error scenario
  - Property test: priority ordering
  - _Requirements: 2.1-2.6_

---

### PHASE 5: HEALTH MONITORING

- [ ] 16. HealthMonitor Core
  - Tạo `antigravity/core/health_monitor.py`
  - Implement `TaskMetrics`, `DerivedMetrics`, `BaselineMetrics` dataclasses
  - Implement `record_task(success, patches, rollback, tokens, no_op)`
  - Implement `compute_health_score()` với weighted formula
  - Implement `categorize_health(score)`
  - _Requirements: 5.1, 5.2, 5.3_

- [ ] 17. HealthMonitor Analytics
  - Implement `get_derived_metrics()` (rollback_rate, token_per_task, etc.)
  - Implement `detect_anomalies()` với baseline comparison
  - Implement `suggest_actions()` với rule-based logic
  - Implement `generate_report()` formatting
  - Implement `establish_baseline()` từ first 50 tasks
  - _Requirements: 5.1, 5.4, 5.8_

- [ ] 18. Orchestrator Health Integration
  - Inject `HealthMonitor` vào `Orchestrator.__init__()`
  - Call `record_task()` trong `execute()` finally block
  - Log health score mỗi 10 tasks
  - Emit alerts khi score < 60
  - _Requirements: 5.4, 5.7_

- [ ] 19. Health Monitoring Tests
  - Unit tests: score computation, anomaly detection, suggestions
  - Integration test: full monitoring cycle
  - Property test: health score monotonicity
  - _Requirements: 5.1-5.9_

---

### PHASE 6: SELF-EVALUATION

- [ ] 20. Self-Evaluation Report
  - Implement `generate_self_eval_report()` trong `HealthMonitor`
  - Include: health score, top issue, suggestion, top strength
  - Auto-generate mỗi 100 tasks
  - Save report to `antigravity/reports/self_eval_{timestamp}.md`
  - _Requirements: 6.1_

- [ ] 21. Performance Baseline
  - Implement baseline establishment logic
  - Track baseline metrics: avg_tokens, avg_patches, success_rate
  - Update baseline quarterly (configurable)
  - Use baseline cho anomaly detection
  - _Requirements: 6.4_

- [ ] 22. Actionable Suggestions
  - Implement rule-based suggestion engine:
    - High stale_ratio → "Re-index skills"
    - High rollback_rate → "Review error detection"
    - Frequent Red zone → "Increase budget limits"
    - Low SLM usage → "Check SLM router config"
  - _Requirements: 6.3_

- [ ] 23. Self-Evaluation Tests
  - Unit tests: report generation, baseline, suggestions
  - Integration test: full self-eval cycle
  - _Requirements: 6.1-6.4_

---

### PHASE 7: METRICS API (Optional)

- [ ] 24. Metrics API Endpoint
  - Tạo `antigravity/api/metrics.py` (FastAPI)
  - Implement `GET /metrics/health` endpoint
  - Implement `GET /metrics/derived` endpoint
  - Implement `GET /metrics/trends` endpoint
  - Support query params: window (10/hour/24h/all)
  - _Requirements: 5.5, 5.6_

- [ ] 25. Metrics Export
  - Implement JSON export
  - Implement Prometheus format export (optional)
  - Implement CSV export
  - _Requirements: 5.9_

---

### PHASE 8: INTEGRATION & VALIDATION

- [ ] 26. Full System Integration Test
  - Test all 5 components working together
  - Simulate real workload: 100 tasks với mixed complexity
  - Verify learning loop reduces retries
  - Verify budget strategy adapts correctly
  - Verify health score tracks performance
  - _Requirements: All_

- [ ] 27. Performance Benchmarking
  - Measure retry reduction rate (target: > 30%)
  - Measure token savings (target: > 20%)
  - Measure health score stability (target: > 70)
  - Compare v6.1 vs v6.2 metrics
  - _Requirements: Success Metrics_

- [ ] 28. Documentation
  - Update `ARCHITECTURE_UPGRADE_COMPLETE.md` với v6.2 changes
  - Create `RESILIENCE_UPGRADE_GUIDE.md` user guide
  - Document new config options
  - Create migration guide từ v6.1 → v6.2
  - _Requirements: All_

- [ ] 29. Final Validation
  - Run full test suite (unit + integration + property)
  - Verify all requirements met
  - Verify backward compatibility
  - Performance regression check
  - _Requirements: All_

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
