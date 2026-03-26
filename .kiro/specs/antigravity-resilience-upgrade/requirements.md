# Tài Liệu Yêu Cầu: Antigravity Resilience Upgrade (v6.2)

## Giới Thiệu

Hệ thống Antigravity v6.1.0 đã đạt **production-grade** về mặt engineering discipline (223 tests passing, 60+ requirements fulfilled). Tuy nhiên, để đạt **production resilience** cho real workload, cần nâng cấp 5 khía cạnh quan trọng:

1. **Index Lifecycle Management** - HybridRetriever adaptive
2. **Multi-Error Prioritization** - ASTAnalyzer intelligent
3. **Learning Loop** - Patch failure memory
4. **Budget-Aware Strategy** - Degraded mode
5. **Actionable Metrics** - Self-evaluable system

---

## Yêu Cầu 1: Index Lifecycle Management

**User Story:** Là một AI agent, tôi muốn retrieval quality không degrade theo thời gian khi skills thay đổi, để tôi luôn tìm đúng skill mới nhất.

### Tiêu Chí Chấp Nhận

1.1. THE HybridRetriever SHALL detect when skill files change (add/modify/delete) via filesystem watch hoặc version hash comparison.

1.2. WHEN a skill file changes, THE HybridRetriever SHALL mark the corresponding embedding as stale và trigger incremental re-indexing.

1.3. THE HybridRetriever SHALL maintain an embedding cache với checksum (SHA-256) để detect content changes without re-embedding unchanged files.

1.4. THE HybridRetriever SHALL support background re-index trigger với hai modes:
   - Manual: via `reindex()` method call
   - Automatic: khi stale_ratio > threshold (default: 20%)

1.5. THE HybridRetriever SHALL log index health metrics:
   - `total_skills`: số skills hiện có
   - `stale_embeddings`: số embeddings cũ
   - `last_index_time`: timestamp lần index cuối
   - `index_version`: incremental version number

1.6. WHEN retrieval quality degrades (detected via low confidence scores), THE system SHALL emit warning và suggest re-indexing.

1.7. THE HybridRetriever SHALL support index versioning để rollback về index cũ nếu re-index fail.

---

## Yêu Cầu 2: Multi-Error Prioritization

**User Story:** Là một AI agent, tôi muốn focus vào root cause error quan trọng nhất khi có nhiều lỗi, để không bị overload context và fix đúng vấn đề.

### Tiêu Chí Chấp Nhận

2.1. THE ASTAnalyzer SHALL sort errors theo severity priority:
   - Priority 1: SyntaxError (blocking)
   - Priority 2: RuntimeError (critical)
   - Priority 3: Lint warnings (minor)

2.2. WHEN multiple errors exist in same file, THE ASTAnalyzer SHALL pick top-k errors (default: k=3) theo priority order.

2.3. THE ASTAnalyzer SHALL detect error dependency chains:
   - Nếu error A gây ra error B → chỉ report error A (root cause)
   - Example: missing import → undefined name

2.4. THE ASTAnalyzer SHALL include error context score trong ASTContract:
   - `error_priority`: 1-3 (syntax/runtime/lint)
   - `is_root_cause`: boolean
   - `dependent_errors`: list error IDs bị ảnh hưởng

2.5. WHEN feeding LLM repair prompt, THE Orchestrator SHALL prioritize root cause errors và limit total error context ≤ 1000 tokens.

2.6. THE ASTAnalyzer SHALL support error clustering:
   - Group similar errors (same type, same function)
   - Report cluster summary thay vì individual errors

---

## Yêu Cầu 3: Learning Loop (Patch Failure Memory)

**User Story:** Là một AI agent, tôi muốn học từ failed patches để không lặp lại sai lầm, giảm retry ngu và tiết kiệm token.

### Tiêu Chí Chấp Nhận

3.1. THE system SHALL maintain a `FailureMemory` store lưu trữ failed patch signatures với format:
   ```python
   {
     "patch_hash": "sha256(patch_content)",
     "error_delta": ErrorDelta,
     "failure_pattern": str,  # extracted pattern
     "timestamp": datetime,
     "session_id": str
   }
   ```

3.2. WHEN a patch fails (net_improvement=False), THE system SHALL extract failure pattern:
   - Syntax pattern: regex từ error message
   - Semantic pattern: AST diff signature
   - Context pattern: affected functions/classes

3.3. THE system SHALL inject failure memory vào repair prompt:
   ```
   [FAILURE MEMORY]
   Previous failed attempts:
   - Patch X caused SyntaxError at foo.py:12
     Pattern: missing closing bracket in list comprehension
   - Patch Y caused RuntimeError: undefined variable
     Pattern: forgot to import module

   AVOID similar patterns in your repair.
   ```

3.4. THE FailureMemory SHALL support TTL (time-to-live):
   - Default: 24 hours
   - Expired entries auto-purged
   - Configurable via `AG_FAILURE_MEMORY_TTL`

3.5. THE FailureMemory SHALL support similarity search:
   - Query: current error context
   - Return: top-3 similar past failures
   - Similarity metric: cosine similarity trên error embeddings

3.6. THE system SHALL track learning effectiveness metrics:
   - `retry_reduction_rate`: % giảm retry sau khi có memory
   - `pattern_match_rate`: % lần memory được sử dụng
   - `token_savings`: token tiết kiệm được

3.7. THE FailureMemory SHALL persist to disk (JSON/SQLite) để survive restarts.

3.8. THE system SHALL support manual failure pattern injection:
   - Admin có thể add known bad patterns
   - Format: regex hoặc AST pattern

---

## Yêu Cầu 4: Budget-Aware Strategy Switching

**User Story:** Là một AI agent, tôi muốn thay đổi hành vi khi budget thấp để maximize success rate với tài nguyên còn lại.

### Tiêu Chí Chấp Nhận

4.1. THE BudgetGuard SHALL define budget zones:
   - **Green Zone**: remaining > 50% → normal mode
   - **Yellow Zone**: 20% < remaining ≤ 50% → conservative mode
   - **Red Zone**: remaining ≤ 20% → degraded mode

4.2. WHEN entering Yellow Zone, THE system SHALL:
   - Reduce `top_k` skills từ 5 → 3
   - Skip retrieval expansion (no contextual summary)
   - Use shorter system prompts (remove examples)
   - Prefer SLM routing over LLM

4.3. WHEN entering Red Zone, THE system SHALL:
   - Force `top_k=1` (single best skill)
   - Skip all retrieval (use deterministic fallback)
   - Use minimal prompts (≤ 200 tokens)
   - Disable repair loop (fail fast)

4.4. THE BudgetGuard SHALL log zone transitions:
   ```
   [BUDGET] Entering YELLOW zone: 45% tokens remaining
   [BUDGET] Strategy: reduced top_k=3, shorter prompts
   ```

4.5. THE system SHALL expose budget zone via `BudgetStatus`:
   ```python
   class BudgetStatus:
       zone: Literal["green", "yellow", "red"]
       strategy: str  # "normal" | "conservative" | "degraded"
   ```

4.6. THE Orchestrator SHALL adapt behavior based on budget zone:
   - Green: full features
   - Yellow: optimize for efficiency
   - Red: optimize for completion

4.7. THE system SHALL track zone-specific success rates:
   - `green_zone_success_rate`
   - `yellow_zone_success_rate`
   - `red_zone_success_rate`

4.8. THE BudgetGuard SHALL support custom zone thresholds via config:
   ```python
   BudgetGuard(
       yellow_threshold=0.5,  # 50%
       red_threshold=0.2      # 20%
   )
   ```

---

## Yêu Cầu 5: Actionable Metrics & System Health Score

**User Story:** Là một developer, tôi muốn dashboard không chỉ đẹp mà còn giúp tôi optimize system, với derived metrics và health score.

### Tiêu Chí Chấp Nhận

5.1. THE TracingService SHALL compute derived metrics:
   - `avg_patches_per_success`: trung bình số patches cần để thành công
   - `rollback_rate`: % patches bị rollback
   - `no_op_patch_rate`: % patches không thay đổi gì
   - `slm_vs_llm_ratio`: tỷ lệ SLM routing vs LLM routing
   - `token_per_task`: trung bình token tiêu thụ mỗi task

5.2. THE system SHALL compute System Health Score:
   ```python
   health_score = (
       success_rate * 100
       - rollback_rate * w1
       - retry_count * w2
       - (token_per_task / baseline) * w3
   )
   # Weights: w1=20, w2=10, w3=5
   # Range: 0-100
   ```

5.3. THE health score SHALL be categorized:
   - **Excellent**: 80-100
   - **Good**: 60-79
   - **Fair**: 40-59
   - **Poor**: 0-39

5.4. THE system SHALL log health score mỗi 10 tasks hoặc mỗi session end.

5.5. THE system SHALL expose health metrics via API endpoint:
   ```
   GET /metrics/health
   {
     "health_score": 85.3,
     "category": "excellent",
     "metrics": {
       "success_rate": 0.92,
       "rollback_rate": 0.08,
       "avg_patches": 1.5,
       "token_per_task": 2500
     }
   }
   ```

5.6. THE TracingService SHALL support metric aggregation windows:
   - Last 10 tasks
   - Last hour
   - Last 24 hours
   - All time

5.7. THE system SHALL emit alerts khi health score drops:
   - Score < 60: WARNING
   - Score < 40: CRITICAL

5.8. THE system SHALL track metric trends:
   - Health score over time (line chart)
   - Rollback rate trend
   - Token efficiency trend

5.9. THE TracingService SHALL support metric export:
   - JSON format
   - Prometheus format (optional)
   - CSV format

---

## Yêu Cầu Xuyên Suốt: Self-Evaluation

**User Story:** Là một autonomous system, tôi muốn tự đánh giá performance và suggest improvements.

### Tiêu Chí Chấp Nhận

6.1. THE system SHALL generate self-evaluation report mỗi 100 tasks:
   ```
   [SELF-EVAL] Performance Report
   - Health Score: 78 (Good)
   - Top Issue: High rollback rate (15%)
   - Suggestion: Review error detection logic
   - Top Strength: Low token usage (avg 2000/task)
   ```

6.2. THE system SHALL detect performance anomalies:
   - Sudden drop in success rate
   - Spike in token usage
   - Increase in retry count

6.3. THE system SHALL suggest concrete actions:
   - "Consider re-indexing skills (stale_ratio=25%)"
   - "Review failed patches in session X"
   - "Budget zone entering Red frequently - increase limits?"

6.4. THE system SHALL maintain performance baseline:
   - Computed from first 50 successful tasks
   - Updated quarterly
   - Used for anomaly detection

---

## Tổng Kết

Nâng cấp v6.2 biến Antigravity từ:
- **v6.1**: Production-grade (correct, tested, observable)
- **v6.2**: Production-resilient (adaptive, self-improving, self-evaluable)

### Impact Cao Nhất (Priority Order):
1. **Learning Loop** (Req 3) - Giảm retry ngu, tiết kiệm token
2. **Index Lifecycle** (Req 1) - Maintain retrieval quality
3. **Budget Strategy** (Req 4) - Maximize success với limited resources
4. **Actionable Metrics** (Req 5) - Enable optimization
5. **Error Prioritization** (Req 2) - Focus on root cause

### Success Criteria:
- Retry reduction rate > 30%
- Health score consistently > 70
- Token savings > 20%
- Zero silent failures (index staleness, etc.)

---

**Version:** v6.2.0-RESILIENCE-UPGRADE
**Target:** Self-healing autonomous debugging runtime
**Philosophy:** "Observable" → "Self-evaluable" → "Self-improving"
